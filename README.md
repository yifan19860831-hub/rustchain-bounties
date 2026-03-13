# RustChain PDP-8 Miner

将 RustChain 矿工移植到 DEC PDP-8 (1965) - 历史上最畅销的迷你计算机！

## 🏆 Bounty Information

- **Issue**: [#1848](https://github.com/Scottcjn/rustchain-bounties/issues/1848)
- **Reward**: 200 RTC (5.0x Multiplier) - LEGENDARY Tier
- **Wallet**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`

## 📜 Historical Significance

The PDP-8 was DEC's best-selling minicomputer:
- **Launched**: March 22, 1965 - 60 years ago!
- **Units Sold**: Over 50,000
- **Architecture**: 12-bit, magnetic-core memory
- **Memory**: 4,096 words (6 KB)
- **Instructions**: Only 8 basic instructions

## 🔧 Technical Specifications

| Component | Specification |
|-----------|---------------|
| Word Size | 12 bits |
| Memory | 6 KB |
| Clock | 0.667 MHz |
| Performance | ~0.333 MIPS |

## 🚀 Quick Start

```bash
cargo build --release
cargo run --release
cargo test
```

## 📦 Project Structure

```
rustchain-pdp8/
├── src/
│   ├── main.rs          # Entry point
│   ├── pdp8_cpu.rs      # PDP-8 CPU simulator
│   ├── arithmetic.rs    # 32-bit arithmetic on 12-bit words
│   ├── sha256.rs        # SHA256 implementation
│   └── miner.rs         # Mining program
├── Cargo.toml
└── README.md
```

## ✅ Implementation Status

- ✓ PDP-8 CPU Simulator (12-bit architecture)
- ✓ 32-bit Arithmetic Library (multi-word emulation)
- ✓ SHA256 Implementation (optimized for 12-bit)
- ✓ Mining Program with Stratum Support
- ✓ All Tests Passing (11/11)

## 🏅 Deliverables

1. **PDP-8 CPU Simulator**: Complete instruction set emulation
2. **32-bit Arithmetic**: Multi-word operations for SHA256
3. **SHA256 Implementation**: Correct hash outputs verified
4. **Mining Program**: Working proof-of-work implementation
5. **Documentation**: This README and inline code comments

## 📝 Testing

All tests pass:
```
running 11 tests
test arithmetic::tests::test_add ... ok
test arithmetic::tests::test_add_with_carry ... ok
test arithmetic::tests::test_from_u32 ... ok
test pdp8_cpu::tests::test_cpu_basic ... ok
test miner::tests::test_stratum_client ... ok
test arithmetic::tests::test_rotr ... ok
test miner::tests::test_miner_basic ... ok
test sha256::tests::test_sha256_hello ... ok
test arithmetic::tests::test_to_u32 ... ok
test sha256::tests::test_sha256_empty ... ok
test sha256::tests::test_sha256_abc ... ok

test result: ok. 11 passed; 0 failed
```

## 🎯 SHA256 Test Vectors

```
SHA256("") = e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
SHA256("abc") = ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
SHA256("hello world") = b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9
```

## 💡 Architecture Challenges

The PDP-8 presents unique challenges:
- **12-bit words** vs SHA256's 32-bit requirements
- **6 KB memory** - extremely tight constraints
- **Only 8 instructions** - minimal instruction set
- **No hardware multiplication** - software emulation required

## 🔮 Performance

Estimated hashrate on real PDP-8 hardware: ~0.0001 H/s

This is a **proof of concept** demonstrating feasibility, not a profitable mining operation!

## 📚 References

- [PDP-8 FAQ](https://homepage.cs.uiowa.edu/~jones/pdp8/)
- [SIMH PDP-8 Simulator](http://simh.trailing-edge.com/)
- [Computer History Museum PDP-8](https://computerhistory.org/collections/catalog/102643816)

---

*Built with ❤️ for the DEC PDP-8, 60 years after its launch.*
