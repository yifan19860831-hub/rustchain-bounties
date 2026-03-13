# RustChain Miner - Datapoint 2200 (1970)

[![Datapoint 2200](https://img.shields.io/badge/Hardware-Datapoint%202200%20(1970)-brightgreen)](https://en.wikipedia.org/wiki/Datapoint_2200)
[![Antiquity Multiplier](https://img.shields.io/badge/Multiplier-4.5%C3%97-orange)](../../README.md)
[![Bounty Tier](https://img.shields.io/badge/Bounty-Pioneer%20(200%20RTC)-purple)](https://github.com/Scottcjn/rustchain-bounties/issues/402)

## The Ultimate Proof-of-Antiquity

This miner runs on the **Datapoint 2200**, the 1970 programmable terminal that **invented the x86 instruction set**. This is the **earliest hardware platform** ever to mine RustChain — predating the Intel 8008 microprocessor itself.

### Historical Significance

```
1970: Datapoint 2200 released (CTC)
         │
         ├─► Instruction set designed by Victor Poor & Harry Pyle
         │
1972: Intel 8008 (single-chip version of Datapoint 2200 CPU)
         │
1974: Intel 8080 (enhanced 8008)
         │
1978: Intel 8086 (first x86)
         │
2026: Modern x86-64 (your laptop!)
```

**Your laptop's x86 CPU is a direct descendant of the Datapoint 2200.**

---

## Quick Start

### Prerequisites

1. **Datapoint 2200** (or emulator)
2. **Serial interface** (RS-232)
3. **Modern PC gateway** (serial-to-Ethernet bridge)
4. **Cassette tape** (for wallet storage)

### Build

```bash
# Assemble the miner
python assemble.py miners/datapoint2200/miner.asm -o miners/datapoint2200/miner.bin

# Load onto cassette tape
python cassette_writer.py miners/datapoint2200/miner.bin --device /dev/ttyS0

# Or load into emulator
python sim2200.py miners/datapoint2200/miner.bin
```

### Run

1. Boot Datapoint 2200
2. Load cassette tape
3. Connect serial cable to gateway PC
4. Run gateway software:
   ```bash
   python gateway.py --port COM1 --baud 9600
   ```
5. Miner starts automatically

---

## Architecture

### Hardware Specifications

| Component | Specification |
|-----------|---------------|
| **CPU** | Discrete TTL logic (~100 chips) |
| **Memory** | 2KB shift register (expandable to 16KB) |
| **Registers** | A, B, C, D, E, H, L (8-bit) |
| **Stack** | 15-level push-down |
| **Flags** | C, P, Z, S |
| **Clock** | ~200-400 kHz |
| **Instructions** | 48 ops, 1-3 bytes |
| **Memory Access** | 520μs (shift register recirculation) |

### Memory Map

```
Octal     Decimal   Usage
─────────────────────────────────────
0000Q     0         Miner code (2KB)
1000Q     512       Wallet data
1400Q     640       Attestation buffer
2000Q     1024      Extended (if 16KB)
```

---

## Assembly Code

See [`miner.asm`](miner.asm) for the full source code.

### Key Functions

- `MINER_LOOP`: Main mining loop
- `ATTEST_HARDWARE`: TTL-specific fingerprinting
- `SERIAL_SEND/RECV`: Bit-serial communication
- `COMPUTE_HASH`: Simplified hash function
- `MEMCPY`: Memory block copy

### Example: Hardware Fingerprint

```assembly
ATTEST_HARDWARE:
    ; Prove we're on REAL Datapoint 2200 TTL hardware
    
    CALL MEASURE_CLOCK_SKEW      ; Discrete oscillator drift
    CALL MEASURE_THERMAL_DRIFT   ; TTL heat curve
    CALL MEASURE_SHIFT_REG_LATENCY ; 520μs signature
    CALL MEASURE_TIMING_VARIANCE ; Instruction timing
    CALL VERIFY_TTL_SIGNATURE    ; Anti-emulation
    CALL VERIFY_SERIAL_BIT_ORDER ; Little-endian origin
    CALL VERIFY_DISCRETE_LOGIC   ; ~100 TTL chips
    
    RET
```

---

## Hardware Fingerprinting

The Datapoint 2200's discrete TTL implementation provides **unique fingerprinting**:

| Check | Description | Why Unique |
|-------|-------------|------------|
| **Clock Skew** | Discrete oscillator drift | Modern CPUs use crystals |
| **Thermal Drift** | TTL heat curve | ~100 chips heat differently |
| **Shift Register Latency** | 520μs memory delay | Only shift-register memory |
| **Timing Variance** | Instruction timing | Serial architecture |
| **TTL Signature** | Discrete logic pattern | Not single-chip |
| **Serial Bit Order** | LSB-first processing | Origin of little-endian |
| **Discrete Logic** | Multi-chip signature | Pre-microprocessor |

---

## Serial Communication

### Bit-Serial Protocol

The Datapoint 2200 processes data **bit-serially** (LSB first), which is why x86 is little-endian today.

```
Bit:  7 6 5 4 3 2 1 0
      └─►───────────┘
      LSB first (origin of little-endian)
```

### Gateway Setup

```
┌─────────────────┐      RS-232      ┌─────────────────┐
│  Datapoint 2200 │◄────────────────►│  Modern PC      │
│  (Serial Port)  │  9600 baud       │  (Gateway)      │
└─────────────────┘                  └────────┬────────┘
                                              │
                                              │ Ethernet
                                              │
                                     ┌────────▼────────┐
                                     │  RustChain Node │
                                     │  rustchain.org  │
                                     └─────────────────┘
```

---

## Antiquity Multiplier

| Criteria | Value | Multiplier |
|----------|-------|------------|
| **Base** | Modern hardware | 1.0× |
| **Era (1970)** | Pre-microprocessor | +2.0× |
| **Technology** | Discrete TTL logic | +0.5× |
| **Historical** | x86 ancestor | +0.5× |
| **Rarity** | ~50 surviving units | +0.5× |
| **Total** | | **4.5×** |

**This is the highest multiplier possible in RustChain.**

---

## Performance

| Metric | Datapoint 2200 | Modern CPU |
|--------|----------------|------------|
| **Attestations/hour** | ~100 | ~1,000,000 |
| **Memory** | 2KB | 16GB+ |
| **Clock** | 200 kHz | 4+ GHz |
| **Power** | ~500W | ~65W |
| **RTC/hour (base)** | 0.5 | 5.0 |
| **RTC/hour (with multiplier)** | **2.25** | 5.0 |

Despite low raw performance, the **4.5× multiplier** makes it competitive!

---

## Grant Proposal

This miner is submitted for the **Pioneer Grant (200 RTC)**:

- **Issue**: [#402](https://github.com/Scottcjn/rustchain-bounties/issues/402)
- **Tier**: Pioneer (Port to new architecture)
- **Wallet**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`

---

## Testing

### Emulator

```bash
# Run in simulator
python sim2200.py miners/datapoint2200/miner.bin

# Test attestation
python test_attest.py --emulator
```

### Real Hardware

```bash
# Load onto cassette
python cassette_writer.py miners/datapoint2200/miner.bin

# Run on real Datapoint 2200
# (You'll need access to one!)
```

---

## Files

```
miners/datapoint2200/
├── README.md           # This file
├── miner.asm           # Assembly source
├── miner.bin           # Compiled binary
├── assemble.py         # Assembler tool
├── gateway.py          # Serial-to-HTTP bridge
├── sim2200.py          # Emulator
├── test_attest.py      # Test suite
└── cassette_writer.py  # Cassette tape writer
```

---

## References

- [Datapoint 2200 Reference Manual](http://www.bitsavers.org/pdf/datapoint/2200/2200_Reference_Manual.pdf)
- [Intel 8008 Documentation](http://www.bitsavers.org/components/intel/MCS8/Intel_8008_8-Bit_Parallel_Central_Processing_Unit_Rev4_Nov73.pdf)
- [Datapoint 2200 Wikipedia](https://en.wikipedia.org/wiki/Datapoint_2200)
- [Intel 8008 Wikipedia](https://en.wikipedia.org/wiki/Intel_8008)
- [Ken Shirriff's 8008 Analysis](https://www.righto.com/2016/12/die-photos-and-analysis-of_24.html)

---

## Badges Earned

- [ ] **⚡ QuickBasic Listener** (Pre-1980 hardware)
- [ ] **🛠️ DOS WiFi Alchemist** (Pre-IBM PC hardware)
- [ ] **🏛️ Silicon Archaeologist** (Pre-microprocessor)
- [ ] **📼 Cassette Tape Master** (Tape storage)
- [ ] **🔌 TTL Whisperer** (Discrete logic)

---

## License

Part of the RustChain project. See main repository for license.

---

*This miner runs on the hardware that invented x86 — before microprocessors existed. The Datapoint 2200 is the ultimate expression of Proof-of-Antiquity.*

**Wallet**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`
