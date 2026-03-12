use serde::{Deserialize, Serialize};
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Config { pub rpc_endpoint: String, pub miner_id: String, pub interval_seconds: u64 }
impl Default for Config {
    fn default() -> Self { Self { rpc_endpoint: "https://rustchain.org/api".to_string(), miner_id: String::new(), interval_seconds: 60 } }
}
pub fn load_config() -> anyhow::Result<Config> { Ok(Config::default()) }
