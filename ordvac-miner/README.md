# RustChain ORDVAC Miner (1951)

🏛️ **LEGENDARY TIER** - Port to ORDVAC, the first stored-program computer clone!

> "Every vintage computer has historical potential"

## Overview

This project ports the RustChain Proof-of-Antiquity miner to **ORDVAC** (Ordnance Discrete Variable Automatic Computer), the 1951 IAS machine clone built at University of Illinois. With its **40-bit word length** and **Williams tube memory**, ORDVAC represents the dawn of the stored-program computing era.

## ORDVAC Architecture

| Specification | Value |
|--------------|-------|
| **Word Length** | 40 bits |
| **Memory** | 1024 words (Williams tubes) |
| **Instructions** | 2 × 20-bit per word |
| **Addition Time** | 72 microseconds |
| **Multiplication Time** | 732 microseconds |
| **Vacuum Tubes** | 2,178 |
| **Architecture** | IAS/von Neumann |
| **Registers** | AC (Accumulator), MQ (Multiplier/Quotient) |
| **Clock** | Asynchronous (no central clock) |
| **Number System** | Two's complement |
| **Hex Notation** | K S N J F L (King Sized Numbers Just For Laughs) |

## Antiquity Multiplier

**ORDVAC (1951)**: **5.0×** multiplier (75+ years old - maximum tier!)

This is the **highest possible multiplier** in RustChain, making ORDVAC the most valuable mining hardware in the network.

## Files

- `ordvac_simulator.py` - Full ORDVAC CPU simulator with Williams tube memory
- `ordvac_miner.py` - RustChain miner running on simulated ORDVAC
- `ordvac_assembler.py` - Assembly language for ORDVAC
- `mining_routine.asm` - ORDVAC assembly mining routine
- `wallet.txt` - Generated wallet address

## Quick Start

```bash
# Run the ORDVAC simulator with miner
python ordvac_simulator.py --run-miner

# Run miner directly (uses simulator internally)
python ordvac_miner.py --wallet YOUR_WALLET

# Assemble ORDVAC assembly code
python ordvac_assembler.py mining_routine.asm
```

## How It Works

The miner implements RustChain's Proof-of-Antiquity attestation protocol:

1. **Hardware Fingerprinting**: Simulates ORDVAC's unique Williams tube timing characteristics
2. **Entropy Collection**: Uses asynchronous instruction timing (72μs add, 732μs multiply)
3. **Attestation**: Submits ORDVAC hardware signature to RustChain node
4. **Epoch Enrollment**: Registers for 10-minute mining epochs
5. **Reward Collection**: Earns RTC with 5.0× antiquity multiplier

## Historical Context

ORDVAC was completed in 1952 at Aberdeen Proving Ground, Maryland. It was used for ballistic trajectory calculations and was one of the first computers to be used remotely via telephone lines. The machine and its twin ILLIAC I could exchange programs - making them the first compatible computers.

This port honors the pioneers: J.P. Nash, Abe Taub, Sylvian Ray, and Donald B. Gillies.

## Wallet Address

```
RTC4325af95d26d59c3ef025963656d22af638bb96b
```

## License

MIT License - Part of RustChain Proof-of-Antiquity ecosystem

---

**"Your vintage hardware earns rewards. Make mining meaningful again."**

*Built with ⚡ by Elyan Labs*
