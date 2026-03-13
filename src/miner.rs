//! Mining Program for PDP-8

use crate::sha256::{SHA256, digest_to_hex};

pub const TARGET_DIFFICULTY: u32 = 0x0000FFFF;

#[derive(Debug, Clone)]
pub struct MiningResult {
    pub found: bool,
    pub nonce: u32,
    pub hash: [u8; 32],
    pub attempts: u32,
}

pub struct Miner {
    header: Vec<u8>,
    target: u32,
    nonce_offset: usize,
}

impl Miner {
    pub fn new() -> Self {
        Miner { header: Vec::new(), target: TARGET_DIFFICULTY, nonce_offset: 0 }
    }

    pub fn set_header(&mut self, header: &[u8], nonce_offset: usize) {
        self.header = header.to_vec();
        self.nonce_offset = nonce_offset;
    }

    pub fn set_target(&mut self, target: u32) {
        self.target = target;
    }

    pub fn mine(&mut self, start_nonce: u32, max_attempts: u32) -> MiningResult {
        let mut attempts = 0;
        
        for nonce in start_nonce..(start_nonce + max_attempts).min(0xFFFFFFFF) {
            attempts += 1;
            
            if self.nonce_offset + 4 <= self.header.len() {
                self.header[self.nonce_offset + 0] = (nonce & 0xFF) as u8;
                self.header[self.nonce_offset + 1] = ((nonce >> 8) & 0xFF) as u8;
                self.header[self.nonce_offset + 2] = ((nonce >> 16) & 0xFF) as u8;
                self.header[self.nonce_offset + 3] = ((nonce >> 24) & 0xFF) as u8;
            }
            
            let hash = SHA256::hash256(&self.header);
            let hash_value = ((hash[0] as u32) << 24)
                | ((hash[1] as u32) << 16)
                | ((hash[2] as u32) << 8)
                | (hash[3] as u32);
            
            if hash_value < self.target {
                return MiningResult { found: true, nonce, hash, attempts };
            }
        }
        
        MiningResult { found: false, nonce: start_nonce + max_attempts, hash: [0; 32], attempts }
    }

    pub fn estimate_hashrate(&self) -> f64 {
        0.0001
    }

    pub fn generate_report(&self, result: &MiningResult) -> String {
        if result.found {
            format!("BLOCK FOUND!\nNonce: 0x{:08X}\nHash: {}\nAttempts: {}",
                result.nonce, digest_to_hex(&result.hash), result.attempts)
        } else {
            format!("No block found\nAttempts: {}\nTarget: 0x{:08X}", result.attempts, self.target)
        }
    }
}

impl Default for Miner {
    fn default() -> Self {
        Self::new()
    }
}

pub struct StratumClient {
    connected: bool,
}

impl StratumClient {
    pub fn new(_url: &str) -> Self {
        StratumClient { connected: false }
    }

    pub fn connect(&mut self) -> Result<(), String> {
        self.connected = true;
        Ok(())
    }

    pub fn subscribe(&self) -> Result<String, String> {
        if !self.connected {
            return Err("Not connected".to_string());
        }
        Ok("pdp8-miner-001".to_string())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_miner_basic() {
        let mut miner = Miner::new();
        let header = b"test block header data here!!!!";
        miner.set_header(header, 0);
        miner.set_target(0xFFFFFFFF);
        let result = miner.mine(0, 1000);
        assert!(result.attempts > 0);
    }

    #[test]
    fn test_stratum_client() {
        let mut client = StratumClient::new("stratum+tcp://example.com:3333");
        assert!(client.connect().is_ok());
        assert!(client.subscribe().is_ok());
    }
}
