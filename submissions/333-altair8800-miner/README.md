# Altair 8800 Miner - RustChain Port

🏆 **LEGENDARY TIER CHALLENGE** - Port Miner to Altair 8800 (1975)

## Overview

This project demonstrates a conceptual port of the RustChain miner to the **Altair 8800**, the first personal computer (1975) - the machine that led to the founding of Microsoft!

### Hardware Constraints

| Component | Specification |
|-----------|--------------|
| **CPU** | Intel 8080 @ 2 MHz |
| **Architecture** | 8-bit |
| **Memory** | 256 bytes base, expandable to 64KB |
| **Bus** | S-100 |
| **Input** | Front panel toggle switches |
| **Output** | LED display |
| **Storage** | Paper tape / Cassette / Floppy (8") |

### The Challenge

Modern cryptocurrency mining requires:
- SHA-256 hashing (computationally intensive)
- Network connectivity
- Gigabytes of memory
- Multi-core processors

The Altair 8800 has **none of these**. This project creates:

1. **8080 Assembly Code** - Conceptual mining implementation
2. **Python Simulator** - Emulates Altair 8800 behavior
3. **Documentation** - Explains the approach and limitations

## Wallet Address

```
RTC4325af95d26d59c3ef025963656d22af638bb96b
```

## Project Structure

```
altair8800-miner/
├── README.md
├── src/
│   └── miner.asm          # 8080 Assembly mining code
├── simulator/
│   ├── altair8800.py      # Altair 8800 emulator
│   └── miner_sim.py       # Mining simulation
└── docs/
    ├── architecture.md    # Altair 8800 architecture
    └── implementation.md  # Implementation details
```

## Quick Start

```bash
# Run the simulator
python simulator/miner_sim.py

# View the assembly code
cat src/miner.asm
```

## Technical Approach

### Why This is "Legendary"

1. **Historical Significance** - Altair 8800 sparked the PC revolution
2. **Extreme Constraints** - 8-bit, 2MHz, KB of RAM vs modern GHz, GB
3. **Educational Value** - Shows the evolution of computing
4. **Creative Solution** - Simulator bridges 1975 and 2025

### Mining on 8080

The 8080 processor lacks:
- 32-bit arithmetic (needed for SHA-256)
- Hardware multiplication
- More than 64KB addressable memory

**Solution**: Implement a simplified "proof of work" that:
- Uses 8-bit operations
- Demonstrates the concept
- Runs in the simulator

## License

MIT License - Share the spirit of the Altair!

## Acknowledgments

- Intel 8080 Architecture Manual
- Altair 8800 Documentation Archive
- RustChain Project

---

*"The Altair 8800 was the spark that lit the personal computer revolution."*
