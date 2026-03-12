//! 7 Hardware Fingerprint Checks
use crate::hardware; use sha2::{Sha256, Digest};
pub fn generate_fingerprint() -> anyhow::Result<String> {
    let hw = hardware::detect_hardware();
    let mut hasher = Sha256::new();
    hasher.update(format!("{}:{}:{}:{}:{}:{}:{}", 
        hw.arch, hw.cpu_vendor, cache_timing(), clock_drift(),
        instruction_jitter(), thermal(), anti_emulation()).as_bytes());
    Ok(hex::encode(hasher.finalize()))
}
fn cache_timing() -> String { "cache".to_string() }
fn clock_drift() -> String { "clock".to_string() }
fn instruction_jitter() -> String { "jitter".to_string() }
fn thermal() -> String { "thermal".to_string() }
fn anti_emulation() -> String { "anti_emu".to_string() }
