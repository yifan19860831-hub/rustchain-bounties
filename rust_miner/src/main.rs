//! RustChain Miner - Native Rust Implementation
mod hardware; mod fingerprint; mod attestation; mod config; mod network;
use anyhow::Result;
use log::info;
#[tokio::main]
async fn main() -> Result<()> {
    env_logger::init();
    info!("RustChain Miner starting...");
    let config = config::load_config()?;
    let fingerprint = fingerprint::generate_fingerprint()?;
    info!("Hardware fingerprint: {}", fingerprint);
    let attestation = attestation::Attestation::new(&config)?;
    network::run_miner(&config, &attestation, &fingerprint).await?;
    Ok(())
}
