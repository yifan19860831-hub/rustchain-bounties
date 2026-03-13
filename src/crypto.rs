//! Cryptography Module - Ed25519 Signatures

use anyhow::{Result, anyhow};
use ed25519_dalek::{Signer, SigningKey, VerifyingKey, Signature, Verifier};
use rand::rngs::OsRng;
use serde::{Serialize, Deserialize};
use std::fs;
use std::path::Path;

/// Keypair for signing attestations
pub struct Keypair {
    pub signing_key: SigningKey,
    pub verifying_key: VerifyingKey,
}

impl Keypair {
    /// Sign a message using the Ed25519 private key.
    ///
    /// # Arguments
    ///
    /// * `message` - The byte slice to sign
    ///
    /// # Returns
    ///
    /// An Ed25519 `Signature` (64 bytes)
    ///
    /// # Security
    ///
    /// Ed25519 signatures are deterministic and secure against side-channel attacks.
    /// The same message will always produce the same signature.
    ///
    /// # Example
    ///
    /// ```
    /// let message = b"RustChain attestation";
    /// let signature = keypair.sign(message);
    /// ```
    pub fn sign(&self, message: &[u8]) -> Signature {
        self.signing_key.sign(message)
    }
    
    /// Get the public key as a hexadecimal string.
    ///
    /// # Returns
    ///
    /// A 64-character lowercase hexadecimal string representing the 32-byte public key.
    ///
    /// # Usage
    ///
    /// The hex-encoded public key is used as the miner's identifier in the RustChain
    /// network and for verifying signatures.
    ///
    /// # Example
    ///
    /// ```
    /// let public_key = keypair.public_key_hex();
    /// println!("Miner ID: {}", public_key);
    /// assert_eq!(public_key.len(), 64);
    /// ```
    pub fn public_key_hex(&self) -> String {
        hex::encode(self.verifying_key.as_bytes())
    }
}

/// Load or generate Ed25519 keypair
pub fn load_or_generate_keypair(key_path: &str) -> Result<Keypair> {
    let path = Path::new(key_path);
    
    if path.exists() {
        // Load existing key
        let key_bytes = fs::read(path)
            .map_err(|e| anyhow!("Failed to read key file: {}", e))?;
        
        if key_bytes.len() == 64 {
            let signing_key = SigningKey::from_bytes(
                &key_bytes[..32].try_into()
                    .map_err(|_| anyhow!("Invalid key format"))?
            );
            let verifying_key = VerifyingKey::from_bytes(
                &key_bytes[32..].try_into()
                    .map_err(|_| anyhow!("Invalid key format"))?
            )?;
            
            Ok(Keypair {
                signing_key,
                verifying_key,
            })
        } else {
            Err(anyhow!("Invalid key file size"))
        }
    } else {
        // Generate new key
        let signing_key = SigningKey::generate(&mut OsRng);
        let verifying_key = VerifyingKey::from(&signing_key);
        
        // Save key
        let mut key_bytes = Vec::with_capacity(64);
        key_bytes.extend_from_slice(signing_key.as_bytes());
        key_bytes.extend_from_slice(verifying_key.as_bytes());
        
        if let Some(parent) = path.parent() {
            fs::create_dir_all(parent)?;
        }
        
        fs::write(path, &key_bytes)
            .map_err(|e| anyhow!("Failed to save key file: {}", e))?;
        
        // Set permissions (Unix only)
        #[cfg(unix)]
        {
            use std::os::unix::fs::PermissionsExt;
            let mut perms = fs::metadata(path)?.permissions();
            perms.set_mode(0o600);
            fs::set_permissions(path, perms)?;
        }
        
        Ok(Keypair {
            signing_key,
            verifying_key,
        })
    }
}

/// Verify a signature
pub fn verify_signature(
    public_key: &VerifyingKey,
    message: &[u8],
    signature: &Signature,
) -> Result<()> {
    public_key.verify(message, signature)
        .map_err(|e| anyhow!("Signature verification failed: {}", e))
}

// Re-export hex for public key encoding
pub use hex;
