# ERA 1101 Miner (1950)

**RustChain miner for the ERA 1101 / UNIVAC 1101** — the first commercially available stored-program computer (1950).

![ERA 1101](https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/UNIVAC-1101BRL61-0901.jpg/640px-UNIVAC-1101BRL61-0901.jpg)

## Overview

This project ports the RustChain miner to the ERA 1101, a vacuum tube computer with:
- **2700 vacuum tubes**
- **Magnetic drum memory**: 16,384 × 24-bit words (48 KB)
- **Drum speed**: 3500 RPM
- **Access time**: 32 μs to 17 ms (rotational latency)
- **24-bit parallel binary** architecture
- **Ones' complement** arithmetic

## Bounty Status

**🏆 LEGENDARY Tier: 200 RTC ($20 USD)**
- **5.0× multiplier** (maximum tier)
- **Wallet**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`

## Project Structure

```
era-1101-miner/
├── sim/           # ERA 1101 simulator (Python)
├── assembler/     # Cross-assembler with drum optimization
├── firmware/      # Network bridge firmware (C++)
├── sha256/        # SHA256 implementation (assembly)
├── fingerprint/   # Hardware fingerprinting
└── docs/          # Technical documentation
```

## Quick Start

### 1. Run Simulator

```bash
cd sim
python3 cpu.py
python3 tests/test_sha256.py
```

### 2. Assemble Code

```bash
cd assembler
python3 era1101_asm.py examples/sha256_core.asm
```

### 3. Flash Firmware

```bash
cd firmware/bridge
# Upload to ESP32/Arduino
```

## Architecture

### Memory Map

| Address Range | Usage |
|---------------|-------|
| 0x0000-0x0FFF | Boot & System |
| 0x1000-0x2FFF | SHA256 Constants |
| 0x3000-0x3FFF | Working Memory |
| 0x4000-0x3FFF | Unassigned |

### Key Challenges

1. **Drum Scheduling**: Instructions must be placed optimally to minimize rotational latency
2. **24-bit SHA256**: Adapting 32-bit SHA256 to 24-bit words
3. **Ones' Complement**: Different arithmetic from modern two's complement
4. **Network Bridge**: Paper tape interface to modern internet

## Implementation Status

- [ ] CPU Simulator
- [ ] Drum Memory Model
- [ ] Assembler
- [ ] SHA256 Implementation
- [ ] Network Bridge
- [ ] Hardware Fingerprint
- [ ] Documentation

## Resources

- [ERA 1101 Documentation](http://ed-thelen.org/comp-hist/ERA-1101-documents.html)
- [Bitsavers Archive](http://www.bitsavers.org/pdf/univac/1101/)
- [Computer History Museum](https://www.computerhistory.org/)

## License

MIT License — see LICENSE file.

## Contributing

This is a **bounty project**. Complete any phase to earn partial RTC rewards. Full completion = 200 RTC.

**Questions?** Join the [RustChain Discord](https://discord.gg/VqVVS2CW9Q).

---

**Created**: 2026-03-13  
**Bounty**: #ERA1101 (LEGENDARY Tier)  
**Wallet**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`
