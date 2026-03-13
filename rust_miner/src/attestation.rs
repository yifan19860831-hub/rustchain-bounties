//! Attestation Module
//! 
//! Handles Ed25519 key generation and signing

use ed25519_dalek::{SigningKey, Signature, Signer};
use rand::rngs::OsRng;
use serde::{Deserialize, Serialize};
use crate::config::Config;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Attestation {
    #[serde(skip)]
    pub signing_key: SigningKey,
    pub public_key: String,
}

impl Attestation {
    /// Create a new Attestation instance with a freshly generated Ed25519 keypair.
    ///
    /// # Arguments
    ///
    /// * `_config` - Configuration (currently unused, keys are generated fresh)
    ///
    /// # Returns
    ///
    /// A Result containing:
    /// - `Ok(Attestation)` - New attestation with generated keypair
    /// - `Err(anyhow::Error)` - If key generation fails (e.g., RNG failure)
    ///
    /// # Security
    ///
    /// Uses `OsRng` (operating system's secure random number generator) for
    /// cryptographically secure key generation. The private key is stored in
    /// memory only and should be persisted securely by the caller.
    ///
    /// # Example
    ///
    /// ```
    /// let config = Config::default();
    /// let attestation = Attestation::new(&config)?;
    /// println!("Public key: {}", attestation.public_key);
    /// ```
    pub fn new(_config: &Config) -> anyhow::Result<Self> {
        // Generate Ed25519 keypair
        let signing_key = SigningKey::generate(&mut OsRng);
        let public_key = hex::encode(signing_key.verifying_key().as_bytes());
        
        Ok(Self {
            signing_key,
            public_key,
        })
    }
    
    /// Sign arbitrary data using the Ed25519 private key.
    ///
    /// # Arguments
    ///
    /// * `data` - The byte slice to sign
    ///
    /// # Returns
    ///
    /// An Ed25519 `Signature` (64 bytes)
    ///
    /// # Example
    ///
    /// ```
    /// let message = b"Hello, RustChain!";
    /// let signature = attestation.sign(message);
    /// ```
    pub fn sign(&self, data: &[u8]) -> Signature {
        self.signing_key.sign(data)
    }
    
    /// Create an attestation signature for a fingerprint and timestamp.
    ///
    /// This is the main attestation method used to prove hardware identity
    /// at a specific point in time.
    ///
    /// # Arguments
    ///
    /// * `fingerprint` - The hardware fingerprint string to attest
    /// * `timestamp` - Unix timestamp (seconds since epoch)
    ///
    /// # Returns
    ///
    /// A Result containing:
    /// - `Ok(String)` - Hex-encoded Ed25519 signature of "fingerprint:timestamp"
    /// - `Err(anyhow::Error)` - If signing fails
    ///
    /// # Format
    ///
    /// The message format is `{fingerprint}:{timestamp}`, which is then signed
    /// and returned as a hex string (128 characters for Ed25519).
    ///
    /// # Example
    ///
    /// ```
    /// let fingerprint = "cpu:G4:mac:00:0c:29:xx:xx:xx";
    /// let timestamp = 1731234567;
    /// let signature = attestation.attest(fingerprint, timestamp)?;
    /// ```
    pub fn attest(&self, fingerprint: &str, timestamp: u64) -> anyhow::Result<String> {
        let message = format!("{}:{}", fingerprint, timestamp);
        let signature = self.sign(message.as_bytes());
        Ok(hex::encode(signature))
    }
}
