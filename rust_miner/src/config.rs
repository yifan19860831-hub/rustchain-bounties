//! Configuration Module

use serde::{Deserialize, Serialize};
use std::path::Path;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Config {
    pub rpc_endpoint: String,
    pub miner_id: String,
    pub private_key: Option<String>,
    pub interval_seconds: u64,
}

impl Default for Config {
    fn default() -> Self {
        Self {
            rpc_endpoint: "https://rustchain.org/api".to_string(),
            miner_id: String::new(),
            private_key: None,
            interval_seconds: 60,
        }
    }
}

/// Load miner configuration from file or use defaults.
///
/// # Returns
///
/// A Result containing:
/// - `Ok(Config)` - Loaded configuration from `config.toml` or default values
/// - `Err(anyhow::Error)` - If file exists but cannot be read or parsed
///
/// # Configuration File
///
/// Looks for `config.toml` in the current working directory. If not found,
/// returns default configuration:
/// - `rpc_endpoint`: "https://rustchain.org/api"
/// - `miner_id`: Empty string (should be set by user)
/// - `private_key`: None (will be generated if needed)
/// - `interval_seconds`: 60
///
/// # File Format
///
/// ```toml
/// rpc_endpoint = "https://your-node.example.com/api"
/// miner_id = "unique-miner-identifier"
/// private_key = "optional-hex-key"
/// interval_seconds = 60
/// ```
///
/// # Example
///
/// ```
/// let config = load_config()?;
/// println!("Connecting to: {}", config.rpc_endpoint);
/// ```
pub fn load_config() -> anyhow::Result<Config> {
    // Try to load from config file, otherwise use defaults
    let config_path = "config.toml";
    if Path::new(config_path).exists() {
        let content = std::fs::read_to_string(config_path)?;
        let config: Config = toml::from_str(&content)?;
        Ok(config)
    } else {
        Ok(Config::default())
    }
}
