//! Configuration Module
//! 
//! Handles loading and saving miner configuration
//! from Controller Pak storage.

use alloc::string::String;

/// Miner configuration
pub struct Config {
    pub key_path: String,
    pub node_url: String,
    pub submit_attestation: bool,
    pub epoch_duration: u32,
    pub log_level: String,
}

impl Default for Config {
    fn default() -> Self {
        Self {
            key_path: String::from("n64:/rustchain/miner_key.bin"),
            node_url: String::from("http://localhost:8080"),
            submit_attestation: true,
            epoch_duration: 300,
            log_level: String::from("info"),
        }
    }
}

impl Config {
    /// Load configuration from storage
    pub fn load() -> Self {
        #[cfg(feature = "n64-homebrew")]
        {
            use n64::storage;
            
            // Try to read config file
            if let Ok(data) = storage::read_file("rustchain/config.toml") {
                return parse_toml_config(&data);
            }
            
            // Return defaults if no config found
            Self::default()
        }
        #[cfg(not(feature = "n64-homebrew"))]
        {
            Self::default()
        }
    }
    
    /// Save configuration to storage
    pub fn save(&self) -> bool {
        #[cfg(feature = "n64-homebrew")]
        {
            use n64::storage;
            
            // Serialize to TOML
            let toml = self.to_toml();
            
            // Write to Controller Pak
            storage::write_file("rustchain/config.toml", toml.as_bytes()).is_ok()
        }
        #[cfg(not(feature = "n64-homebrew"))]
        {
            false
        }
    }
    
    /// Serialize to TOML format
    fn to_toml(&self) -> String {
        let mut toml = String::new();
        toml.push_str(&format!("key_path = \"{}\"\n", self.key_path));
        toml.push_str(&format!("node_url = \"{}\"\n", self.node_url));
        toml.push_str(&format!("submit_attestation = {}\n", self.submit_attestation));
        toml.push_str(&format!("epoch_duration = {}\n", self.epoch_duration));
        toml.push_str(&format!("log_level = \"{}\"\n", self.log_level));
        toml
    }
}

/// Parse TOML configuration
fn parse_toml_config(data: &[u8]) -> Config {
    let config_str = core::str::from_utf8(data).unwrap_or("");
    
    let mut config = Config::default();
    
    // Simple TOML parsing (production should use toml crate)
    for line in config_str.lines() {
        let line = line.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        
        if let Some(eq_pos) = line.find('=') {
            let key = line[..eq_pos].trim();
            let value = line[eq_pos + 1..].trim().trim_matches('"');
            
            match key {
                "key_path" => config.key_path = String::from(value),
                "node_url" => config.node_url = String::from(value),
                "submit_attestation" => {
                    config.submit_attestation = value == "true"
                }
                "epoch_duration" => {
                    config.epoch_duration = value.parse().unwrap_or(300)
                }
                "log_level" => config.log_level = String::from(value),
                _ => {}
            }
        }
    }
    
    config
}
