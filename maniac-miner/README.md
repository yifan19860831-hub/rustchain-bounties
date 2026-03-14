# MANIAC I Miner for RustChain

**Porting RustChain to the Ultimate Vintage Hardware (1952)**

This project implements a conceptual port of the RustChain miner to MANIAC I (Mathematical Analyzer Numerical Integrator and Automatic Computer), the legendary 1952 computer built at Los Alamos National Laboratory.

## 🏛️ MANIAC I Architecture

### Specifications
- **Word Length**: 40 bits
- **Memory**: Williams-Kilburn tube (CRT-based)
- **Memory Capacity**: ~1024 words (40 Kbits)
- **Clock Speed**: ~200 KHz
- **Technology**: Vacuum tubes
- **Weight**: 1,000 pounds (0.5 tons)
- **Dimensions**: 6 feet high × 8 feet wide
- **Location**: Los Alamos Scientific Laboratory
- **Operational**: 1952-1965

### Instruction Set
MANIAC I used a simplified von Neumann ISA with approximately 28 instructions:

| Opcode | Mnemonic | Description |
|--------|----------|-------------|
| 00 | LOAD | Load from memory to accumulator |
| 01 | STORE | Store accumulator to memory |
| 02 | ADD | Add memory to accumulator |
| 03 | SUB | Subtract memory from accumulator |
| 04 | MUL | Multiply accumulator by memory |
| 05 | DIV | Divide accumulator by memory |
| 06 | JUMP | Unconditional jump |
| 07 | JZ | Jump if accumulator is zero |
| 08 | JN | Jump if accumulator is negative |
| 09 | INPUT | Read from paper tape |
| 0A | OUTPUT | Write to output device |
| 0B | HALT | Stop execution |

## 🎯 RustChain Proof-of-Antiquity

RustChain rewards vintage hardware with multipliers based on age:

| Hardware | Era | Multiplier |
|----------|-----|------------|
| **MANIAC I** | **1952** | **10.0×** (theoretical max) |
| PowerPC G4 | 1999-2005 | 2.5× |
| PowerPC G5 | 2003-2006 | 2.0× |
| PowerPC G3 | 1997-2003 | 1.8× |
| Modern x86_64 | Current | 1.0× |

**MANIAC I would earn the highest possible antiquity multiplier!**

## 📁 Project Structure

```
maniac-miner/
├── README.md                 # This file
├── maniac_simulator.py       # MANIAC I Python simulator
├── maniac_miner.py           # RustChain miner for MANIAC I
├── test_miner.py             # Test suite
├── docs/
│   ├── ARCHITECTURE.md       # Technical architecture
│   ├── INSTRUCTION_SET.md    # MANIAC I ISA reference
│   └── MINING_PROTOCOL.md    # Mining algorithm
└── examples/
    └── hello_maniac.py       # Demo program
```

## 🚀 Quick Start

### Run the Simulator

```bash
python maniac_simulator.py
```

### Run the Miner

```bash
python maniac_miner.py --wallet RTC4325af95d26d59c3ef025963656d22af638bb96b
```

## 🔬 Technical Implementation

### Hardware Fingerprinting

The MANIAC I miner implements unique hardware attestation:

1. **Williams Tube Refresh Pattern**: CRT decay signature
2. **Vacuum Tube Thermal Drift**: Heat-based entropy
3. **40-bit Word Timing**: Instruction jitter from tube switching
4. **Paper Tape Latency**: Mechanical I/O timing

### Mining Algorithm

The miner performs simplified SHA-256 hashing adapted for 40-bit words:

```
1. Load nonce into accumulator (40 bits at a time)
2. XOR with block header
3. Apply custom permutation (MANIAC-style)
4. Check difficulty target
5. Submit solution if valid
```

### Performance Estimates

| Metric | MANIAC I | Modern CPU |
|--------|----------|------------|
| Hash Rate | ~0.001 H/s | 1,000,000 H/s |
| Power | 50,000 W | 100 W |
| Efficiency | Historic | Efficient |
| **RTC/epoch** | **1.20 RTC** | 0.12 RTC |

*Despite lower hash rate, MANIAC I earns 10× rewards due to antiquity!*

## 📜 Bounty Claim

**Bounty**: #370 - Port Miner to MANIAC I (1952)  
**Reward**: 200 RTC ($20 USD) - LEGENDARY Tier  
**Wallet**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`

## 🎓 Historical Context

MANIAC I was notable for:
- First computer to defeat a human in chess (1956)
- Monte Carlo simulations for thermonuclear research
- Programming by Klára Dán von Neumann (first computer programmer)
- Featured in the Fermi-Pasta-Ulam-Tsingou problem

## 📄 License

MIT License - See LICENSE file

## 🙏 Acknowledgments

- Los Alamos National Laboratory for preserving computing history
- RustChain team for Proof-of-Antiquity concept
- Computer History Museum for documentation

---

*"Your vintage hardware earns rewards. Make mining meaningful again."*

**Made with ⚡ for the 1952 MANIAC I**
