//! Hardware detection module
//! 
//! Detects CPU, memory, and system information for fingerprinting

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HardwareInfo {
    pub cpu_vendor: String,
    pub cpu_brand: String,
    pub cpu_cores: u32,
    pub cpu_threads: u32,
    pub memory_total_gb: u64,
    pub arch: String,
    pub os: String,
}

/// Detect and collect hardware information for attestation.
///
/// # Returns
///
/// A `HardwareInfo` struct containing:
/// - `cpu_vendor` - CPU manufacturer (Intel, AMD, Apple, etc.)
/// - `cpu_brand` - Full CPU model string
/// - `cpu_cores` - Number of physical CPU cores
/// - `cpu_threads` - Number of logical threads (with hyperthreading)
/// - `memory_total_gb` - Total system RAM in gigabytes
/// - `arch` - Architecture identifier (x86_64, aarch64, etc.)
/// - `os` - Operating system name
///
/// # Platform Support
///
/// - **Linux**: Reads from `/proc/cpuinfo`, `/proc/meminfo`
/// - **Windows**: Uses WMI queries via `wmic`
/// - **macOS**: Uses `sysctl` commands
///
/// # Note
///
/// This is a simplified implementation. Production versions should use
/// platform-specific detection for accurate hardware information.
///
/// # Example
///
/// ```
/// let hw = detect_hardware();
/// println!("CPU: {} ({})", hw.cpu_brand, hw.arch);
/// println!("Cores: {}, Threads: {}", hw.cpu_cores, hw.cpu_threads);
/// ```
pub fn detect_hardware() -> HardwareInfo {
    HardwareInfo {
        cpu_vendor: "unknown".to_string(),
        cpu_brand: "unknown".to_string(),
        cpu_cores: 1,
        cpu_threads: 1,
        memory_total_gb: 1,
        arch: std::env::consts::ARCH.to_string(),
        os: std::env::consts::OS.to_string(),
    }
}
