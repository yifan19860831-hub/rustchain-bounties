# ACE 1950 Miner (Turing's Design)

**RustChain miner for the ACE (Automatic Computing Engine)** — Alan Turing's pioneering stored-program computer design from 1945-1950.

![Pilot ACE](https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Pilot_ACE_Exhibit_Overview.webp/640px-Pilot_ACE_Exhibit_Overview.webp)

## Overview

This project ports the RustChain miner to the **ACE (Automatic Computing Engine)**, designed by **Alan Turing** at the National Physical Laboratory (NPL). The Pilot ACE ran its first program on **May 10, 1950**.

### ACE Architecture

| Feature | Specification |
|---------|--------------|
| **Word Size** | 32 bits |
| **Memory** | 128 × 32-bit words (mercury delay lines), later expanded to 352 words |
| **Clock Speed** | 1 MHz (fastest of early British computers) |
| **Vacuum Tubes** | ~800 |
| **Arithmetic** | Fixed-point (initially), later floating-point |
| **Multiplication/Division** | Software (hardware added later) |
| **Drum Memory** | 4096 words (added 1954) |

### Key Design Features

1. **Mercury Delay Line Memory**: Serial access memory using acoustic waves in mercury tubes
2. **32-bit Word**: Turing's innovative choice for precision
3. **Minimal Instruction Set**: ~28 original instructions
4. **Two-Address Format**: Most instructions specify source and destination
5. **Microprogramming**: Early use of control ROM for instruction sequencing

## Bounty Status

**🏆 LEGENDARY Tier: 200 RTC ($20 USD)**
- **5.0× multiplier** (maximum tier)
- **Wallet**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`
- **Bounty ID**: #354

## Project Structure

```
ace-1950-miner/
├── sim/              # ACE simulator (Python)
│   ├── ace_cpu.py    # CPU and memory simulation
│   ├── delay_line.py # Mercury delay line model
│   └── test_ace.py   # Test suite
├── assembler/        # Cross-assembler
│   └── ace_asm.py    # Assembly to machine code
├── firmware/         # Network bridge (planned)
├── sha256/           # SHA256 for ACE (assembly)
├── fingerprint/      # Hardware fingerprinting (vacuum tube characteristics)
└── docs/             # Technical documentation
    ├── ARCHITECTURE.md
    ├── MINING_PROTOCOL.md
    └── ASSEMBLY_GUIDE.md
```

## Quick Start

### 1. Run Simulator

```bash
cd sim
python3 ace_cpu.py
python3 test_ace.py
```

### 2. Assemble Code

```bash
cd assembler
python3 ace_asm.py examples/miner_core.asm
```

### 3. Test SHA256 Core

```bash
cd sim
python3 test_sha256.py
```

## Memory Map

| Address Range | Usage |
|---------------|-------|
| 0x00-0x1F | Boot & System (32 words) |
| 0x20-0x7F | SHA256 Constants & Working |
| 0x80-0xFF | Program & Data (up to 352 words) |

## ACE Instruction Set (Simplified)

| Opcode | Mnemonic | Description |
|--------|----------|-------------|
| 0x01 | ACH | Add to accumulator high |
| 0x02 | ACL | Add to accumulator low |
| 0x03 | ADH | Add from delay line to H |
| 0x04 | ADL | Add from delay line to L |
| 0x05 | SUB | Subtract |
| 0x06 | RND | Round |
| 0x07 | LSH | Left shift |
| 0x08 | RSH | Right shift |
| 0x09 | AND | Logical AND |
| 0x0A | OR | Logical OR |
| 0x0B | NOT | Logical NOT |
| 0x0C | LD | Load from delay line |
| 0x0D | ST | Store to delay line |
| 0x0E | JMP | Unconditional jump |
| 0x0F | JZ | Jump if zero |
| 0x10 | JN | Jump if negative |
| 0x11 | STOP | Halt |

## Key Challenges

1. **Delay Line Timing**: Serial memory requires precise timing for instruction placement
2. **32-bit SHA256**: Native word size matches SHA256 perfectly!
3. **Software Multiplication**: Must implement multiplication in software
4. **Network Bridge**: Paper tape / punch card interface to modern internet
5. **Vacuum Tube Fingerprint**: Unique thermal and timing characteristics

## Implementation Status

- [x] Project setup
- [x] CPU Simulator
- [x] Delay Line Memory Model
- [ ] Assembler
- [ ] SHA256 Implementation
- [ ] Network Bridge
- [ ] Hardware Fingerprint
- [ ] Full Documentation

## Resources

- [Pilot ACE - Wikipedia](https://en.wikipedia.org/wiki/Pilot_ACE)
- [Science Museum London - ACE](https://collection.sciencemuseumgroup.org.uk/objects/co51033/pilot-ace-computer-1950)
- [Alan Turing's ACE Report (1946)](http://www.turingarchive.org/browse.php/B/4)
- [National Physical Laboratory Archives](https://www.npl.co.uk/)

## License

MIT License — see LICENSE file.

## Contributing

This is a **bounty project**. Complete any phase to earn partial RTC rewards. Full completion = 200 RTC.

**Submit your PR with:**
- Wallet address in PR description
- Link to this bounty issue #354
- Working simulator and documentation

**Questions?** Join the [RustChain Discord](https://discord.gg/VqVVS2CW9Q).

---

**Created**: 2026-03-14  
**Bounty**: #354 - ACE 1950 Miner (LEGENDARY Tier)  
**Wallet**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`  
**Designer**: Alan Turing (1945-1950)
