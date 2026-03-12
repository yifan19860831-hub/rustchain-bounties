use crate::config::Config; use crate::attestation::Attestation; use log::info;
pub async fn run_miner(_config: &Config, _attestation: &Attestation, _fingerprint: &str) -> anyhow::Result<()> {
    info!("Miner running..."); loop { tokio::time::sleep(tokio::time::Duration::from_secs(60)).await; info!("Heartbeat..."); }
}
