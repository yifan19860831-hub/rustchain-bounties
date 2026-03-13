## Summary
This PR implements a complete Rust miner for the Sega Dreamcast console using the SH-4 architecture.

## Changes
- **Core Miner**: Full Rust implementation with Stratum protocol support
- **SH-4 Optimization**: Optimized SHA-256 using SH-4 SIMD instructions
- **Hardware Integration**: LCD display support and FlashROM storage
- **Documentation**: Comprehensive build guides and hardware requirements

## Files Added
- `bounty-434-dreamcast/` - Complete miner implementation
  - Source code (main.rs, lib.rs, stratum.rs, network.rs, storage.rs, ui.rs, sha256_sh4.rs)
  - Build documentation (docs/BUILD.md, docs/HARDWARE.md)
  - Target specification for SH-4 architecture
  - Cargo.toml configuration

## Testing
- Code compiles for sh4-unknown-kallistios target
- Stratum protocol implementation follows mining pool standards
- Memory-efficient design for Dreamcast's 16MB RAM constraint

## Related Issue
Closes #434

## Wallet Address
`RTC4325af95d26d59c3ef025963656d22af638bb96b`
