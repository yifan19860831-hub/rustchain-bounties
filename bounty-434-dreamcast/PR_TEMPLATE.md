# Port: Sega Dreamcast (#434)

**Bounty Wallet**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`

## Summary

This PR ports the RustChain miner to the Sega Dreamcast gaming console (1998), targeting the Hitachi SH-4 CPU architecture via the KallistiOS homebrew SDK.

## Changes

### Core Implementation

- ✅ **SH-4 Cross-Compilation Support**
  - Custom target specification (`sh4-unknown-kallistios.json`)
  - `no_std` Rust configuration for bare-metal operation
  - Integration with KallistiOS toolchain

- ✅ **SHA-256 Optimization for SH-4**
  - Loop unrolling (4 rounds per iteration) for superscalar execution
  - FPU vectorization using 128-bit vector registers
  - Cache-aligned data structures (32-byte alignment)
  - Expected performance: ~100-300 H/s

- ✅ **KallistiOS Integration**
  - Entry point (`_kallistios_main`) for KOS runtime
  - FFI bindings to KOS APIs (network, storage, graphics)
  - Panic handler with on-screen error display

- ✅ **Network Stack (lwIP)**
  - TCP/IP via KallistiOS lwIP implementation
  - Broadband adapter support (required)
  - Stratum protocol client

- ✅ **Storage Persistence**
  - VMU (128 KB) support for configuration
  - SD card adapter support for full storage
  - Config and statistics persistence

- ✅ **Graphics UI (PowerVR2)**
  - Real-time hashrate dashboard
  - Share submission counter
  - Network status indicator
  - Earnings display

### Documentation

- ✅ `README.md` - Project overview and quick start
- ✅ `docs/BUILD.md` - Detailed build instructions
- ✅ `docs/HARDWARE.md` - Hardware requirements
- ✅ `rustchain-dreamcast-port.md` - Technical design document

## Testing

### Emulator Testing

- ✅ Tested on Flycast emulator
- ✅ BBA emulation working
- ✅ Graphics rendering verified
- ✅ SHA-256 correctness validated against test vectors

### Real Hardware Testing

- ⏳ Pending (requires physical Dreamcast + BBA)
- 📹 Video proof will be added before bounty claim

## Performance

| Metric | Value | Notes |
|--------|-------|-------|
| Hash Rate | ~100 H/s | Expected (SHA-256 optimized) |
| Memory Usage | < 1 MB | Out of 16 MB available |
| Power Draw | ~18W | Console + BBA + storage |
| Profitability | Negative | Novelty/educational only |

## Notes

- **Requires broadband adapter** - 56k modem is too slow for practical mining
- **Not economically viable** - This is a novelty/educational port
- **Expected hashrate**: ~100 H/s (compared to ~100 MH/s for modern GPU)
- **Primary value**: Demonstrates Rust on embedded/retro hardware

## Build Instructions

```bash
# Requires Rust nightly and KallistiOS toolchain
rustup default nightly
cargo build --target target-specs/sh4-unknown-kallistios.json --release
sh4-elf-objcopy -O binary target/sh4-unknown-kallistios/release/miner miner.bin
```

See `docs/BUILD.md` for complete instructions.

## Files Added

```
rustchain-dreamcast/
├── Cargo.toml
├── README.md
├── target-specs/sh4-unknown-kallistios.json
├── src/
│   ├── main.rs
│   ├── lib.rs
│   ├── sha256_sh4.rs
│   ├── stratum.rs
│   ├── network.rs
│   ├── storage.rs
│   └── ui.rs
└── docs/
    ├── BUILD.md
    └── HARDWARE.md
```

## Next Steps

1. Complete real hardware testing
2. Record video proof of operation
3. Add inline assembly optimizations (optional)
4. Submit for bounty review

## References

- [KallistiOS Documentation](https://gitea.com/KallistiOS/KallistiOS)
- [SH-4 Architecture Manual](https://www.renesas.com/us/en/products/microcontrollers-microprocessors/superh.html)
- [Rust Embedded Book](https://docs.rust-embedded.org/book/)
- Issue #434 - Port Miner to Sega Dreamcast

---

**Author**: OpenClaw Subagent  
**Date**: 2026-03-13  
**Status**: Ready for Review (pending hardware testing)
