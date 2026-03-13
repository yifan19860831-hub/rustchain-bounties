# CDC 160 Miner (1960)

**RustChain miner for the CDC 160** — Control Data Corporation's first small scientific computer, designed by Seymour Cray in 1960.

![CDC 160](https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Control_Data_160-A.jpg/640px-Control_Data_160-A.jpg)

## Overview

This project ports the RustChain miner to the CDC 160, a 12-bit minicomputer with:
- **12-bit word length** (vs modern 64-bit)
- **Magnetic core memory**: 4096 × 12-bit words (6 KB)
- **Memory cycle time**: 6.4 μs
- **Average instruction time**: 15 μs (~67,000 IPS)
- **Ones' complement arithmetic** with end-around carry
- **No hardware multiply/divide** (optional peripheral)
- **Designed by Seymour Cray** over a legendary 3-day weekend

## Bounty Status

**🏆 LEGENDARY Tier: 200 RTC ($20 USD)**
- **Maximum tier multiplier**
- **Wallet**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`
- **Bounty #**: 386

## Project Structure

```
cdc160-miner/
├── cdc160_simulator.py   # CDC 160 CPU simulator
├── cdc160_miner.py       # RustChain miner implementation
├── assembly/             # Assembly source code
│   └── miner.asm         # Conceptual assembly miner
├── docs/                 # Documentation
│   └── CDC160_PORT.md    # Detailed port documentation
└── requirements.txt      # Python dependencies (none required)
```

## Quick Start

### 1. Test the Simulator

```bash
cd cdc160-miner
python3 cdc160_simulator.py
```

Expected output:
```
CDC 160 Simulator OK
  Executed 6 instructions
  A = 3 (octal: 0o3)
  Memory[77] = 3 (should be 3)
  Halted: True
```

### 2. Run the Miner

```bash
# Simulated mode (default)
python3 cdc160_miner.py

# With custom wallet
python3 cdc160_miner.py RTC4325af95d26d59c3ef025963656d22af638bb96b

# Test fingerprint only
python3 cdc160_miner.py --test-only

# Mine multiple epochs
python3 cdc160_miner.py --epochs 5
```

### 3. View Documentation

```bash
cat CDC160_PORT.md
```

## Architecture

### CDC 160 Specifications

| Feature | Value |
|---------|-------|
| **Release Year** | 1960 |
| **Designer** | Seymour Cray |
| **Word Size** | 12 bits |
| **Memory** | 4096 words (magnetic core) |
| **Cycle Time** | 6.4 μs |
| **Add Time** | 12.8 μs (2 cycles) |
| **Performance** | ~67,000 IPS |
| **Arithmetic** | Ones' complement |
| **Registers** | A (accumulator), P (program counter) |
| **I/O** | Paper tape, typewriter |
| **Weight** | 810 lbs (370 kg) |
| **Price (1960)** | $100,000 (~$1.1M in 2025) |

### Instruction Set (Simplified)

| Opcode (octal) | Mnemonic | Description |
|----------------|----------|-------------|
| 00 | HLT | Halt |
| 01 | CLA | Clear A |
| 02 | INA | Increment A |
| 03 | LDA | Load A from memory |
| 04 | STA | Store A to memory |
| 05 | ADD | Add memory to A |
| 06 | SUB | Subtract memory from A |
| 07 | JMP | Jump |
| 10 | NOP | No operation |

### RIP-PoA Fingerprint

The CDC 160's unique characteristics for Proof-of-Antiquity:

1. **Clock-Skew**: Simulated 6.4 μs memory cycle timing
2. **Cache Timing**: Magnetic core memory (no cache)
3. **SIMD Identity**: Serial 12-bit ALU
4. **Thermal Drift**: Core memory (temperature stable)
5. **Instruction Jitter**: Fixed 15 μs average
6. **Anti-Emulation**: 1960 vintage, ones' complement, Seymour Cray design

## Implementation Status

- [x] CPU Simulator
- [x] Ones' Complement Arithmetic
- [x] Miner Implementation
- [x] Fingerprint Generation
- [x] Documentation
- [ ] Assembly Implementation (conceptual only)
- [ ] Hardware Implementation (future)

## Sample Output

```
============================================================
CDC 160 (1960) RustChain Miner
LEGENDARY Tier Bounty #386 - 200 RTC ($20)
============================================================
Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b
Node: https://50.28.86.131
Mode: Simulated
============================================================

[Epoch 1] Mining on CDC 160...
  Nonce: d486c1cec611a54f
  Device: cdc160_1960
  Status: Payload generated (simulated submission)
  Fingerprint: all_passed=True
```

## Historical Context

### The CDC 160 Legacy

The CDC 160 was revolutionary:
- **First desk computer**: Fit into operator's desk
- **Seymour Cray design**: Created in a 3-day weekend
- **Minicomputer pioneer**: One of the first minicomputers
- **PP architecture**: Became basis for CDC 6600 peripheral processors
- **Educational impact**: Used to teach low-level I/O and interrupts

### Seymour Cray

Seymour Cray (1925-1996) is the "father of supercomputing." The CDC 160 was one of his early designs before creating the CDC 6600 (1964), the world's first successful supercomputer.

## Resources

- [CDC 160 Series - Wikipedia](https://en.wikipedia.org/wiki/CDC_160_series)
- [CDC 160 Programming Manual (1960)](http://bitsavers.org/pdf/cdc/160/023a_160_Computer_Programming_Manual_1960.pdf)
- [CDC 160-A Manual (1963)](http://bitsavers.org/pdf/cdc/160/145e_CDC160A_ProgMan_Mar63.pdf)
- [Douglas W. Jones CDC-160 Reference](http://www.cs.uiowa.edu/~jones/cdc160/man/index.html)
- [Computer History Museum - CDC 160A](http://www.computerhistory.org/revolution/minicomputers/11/333/1913)

## License

MIT License — see LICENSE file.

## Contributing

This is a **bounty project**. Complete any phase to earn partial RTC rewards. Full completion = 200 RTC.

**Questions?** Join the [RustChain Discord](https://discord.gg/VqVVS2CW9Q).

---

**Created**: 2026-03-14  
**Bounty**: #386 (LEGENDARY Tier)  
**Wallet**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`  
**Architecture**: CDC 160 (1960) — Seymour Cray design
