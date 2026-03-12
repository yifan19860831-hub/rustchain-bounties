use ed25519_dalek::{SigningKey, Signature, Signer};
use rand::rngs::OsRng; use crate::config::Config;
pub struct Attestation { #[serde(skip)] pub signing_key: SigningKey, pub public_key: String }
impl Attestation {
    pub fn new(_config: &Config) -> anyhow::Result<Self> {
        let signing_key = SigningKey::generate(&mut OsRng);
        Ok(Self { signing_key, public_key: hex::encode(signing_key.verifying_key().as_bytes()) })
    }
    pub fn sign(&self, data: &[u8]) -> Signature { self.signing_key.sign(data) }
}
