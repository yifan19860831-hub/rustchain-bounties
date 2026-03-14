# Joust Miner Architecture

## Overview

This document describes the technical architecture of the RustChain miner port to the Joust arcade platform (Williams Electronics, 1982).

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     JOUST ARCADE CABINET                        │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Motorola 6809 @ 1.5 MHz                      │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  6809 Assembly Miner Core                           │  │  │
│  │  │  - Hardware fingerprinting (6 checks)               │  │  │
│  │  │  - Simplified PoW computation                       │  │  │
│  │  │  - VBLANK-synchronized timing                       │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │                         │                                   │  │
│  │                         ▼                                   │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  Python Co-Processor Bridge                         │  │  │
│  │  │  - Network communication (HTTPS)                    │  │  │
│  │  │  - Attestation formatting                           │  │  │
│  │  │  - Block submission                                 │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                   │
│                              ▼                                   │
│            ┌───────────────────────────────────┐                │
│            │   Custom Network Interface        │                │
│            │   (Hardware modification req.)    │                │
│            └───────────────────────────────────┘                │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   RustChain Network │
                    │   rustchain.org     │
                    └─────────────────────┘
```

## Component Details

### 1. 6809 Assembly Core (`joust_miner.asm`)

#### Memory Map

| Address Range | Size | Purpose |
|---------------|------|---------|
| $0000-$00FF | 256 B | Zero Page (direct addressing) |
| $0100-$03FF | 768 B | System Stack |
| $0400-$07FF | 1 KB | Miner Variables |
| $0800-$0FFF | 2 KB | Shared Game RAM |
| $1000-$FFFF | 60 KB | ROM (game + miner) |

#### Key Routines

1. **INIT** - Initialize registers, calculate hardware fingerprint
2. **CALC_FINGERPRINT** - ROM checksum for hardware ID
3. **MINING_LOOP** - Main mining loop
4. **COMPUTE_HASH** - Simplified 8-bit hash function
5. **SUBMIT_PROOF** - Trigger Python bridge (via NMI)
6. **VBLANK_ISR** - VBLANK interrupt handler
7. **MEASURE_SKEW** - Clock-skew measurement
8. **ANTI_EMU_CHECK** - Anti-emulation verification

#### Instruction Set Usage

The miner uses these 6809 instructions:

| Instruction | Purpose |
|-------------|---------|
| LDA/STA | Load/store accumulator |
| ADD/SUB | Arithmetic |
| MUL | Hardware multiply (distinctive 6809 feature) |
| EOR | XOR for hashing |
| LSR/ASL | Bit shifts |
| CMP | Comparisons |
| BEQ/BNE/BGT | Conditional branches |
| PSHS/PULS | Stack operations |
| LEA | Load effective address |
| CLI/SEI | Interrupt control |
| RTI | Return from interrupt |

### 2. Python Simulator (`joust_simulator.py`)

#### Classes

1. **Motorola6809**
   - CPU register emulation
   - Memory map (RAM + ROM)
   - VBLANK interrupt simulation
   - Hash computation
   - Mining step execution

2. **RustChainBridge**
   - HTTPS communication with rustchain.org
   - Proof submission
   - Epoch retrieval
   - Balance checking
   - Signature generation (Ed25519 placeholder)

3. **JoustMiner**
   - Orchestrates 6809 emulation
   - Manages mining lifecycle
   - Progress reporting
   - Summary statistics

#### Mining Algorithm

```python
def mine_step(self):
    # 1. Increment nonce
    nonce = (nonce + 1) % 65536
    
    # 2. Compute hash (epoch ⊕ nonce ⊕ hardware_id)
    data = pack(epoch, nonce, hardware_id)
    hash = crc16_like(data)
    
    # 3. Check against target
    if hash < target:
        # 4. Submit proof
        submit_proof(epoch, nonce, hash, hardware_id)
```

### 3. Hardware Fingerprint (`joust_hardware.py`)

#### Six Hardware Checks

1. **Clock-Skew & Oscillator Drift**
   - Measures 6809 cycles per VBLANK
   - Expected: ~25,000 cycles at 1.5 MHz / 60 Hz
   - Drift indicates oscillator aging

2. **ROM Timing Fingerprint**
   - Measures ROM access latency
   - Variations from manufacturing tolerances
   - Typical: 450ns ± 50ns

3. **SIMD Unit Identity** (adapted)
   - Uses 6809 hardware multiplier
   - MUL instruction timing varies by CPU batch
   - Expected: 10-11 cycles

4. **Thermal Drift Entropy**
   - Simulated temperature measurements
   - Cabinet heat affects oscillator
   - Typical: 45°C ± 5°C

5. **Instruction Path Jitter**
   - Measures instruction timing variations
   - Micro-architectural differences
   - Acceptable: <5% jitter

6. **Anti-Emulation Checks**
   - Exploits Joust "belly flop" bug
   - VBLANK timing precision
   - Difficult to emulate accurately

#### Authenticity Scoring

```python
authenticity_score = passed_checks / total_checks

# Scoring:
# 6/6 passed = 100% (authentic hardware)
# 5/6 passed = 83%  (likely authentic)
# 4/6 passed = 67%  (uncertain)
# <4/6 passed = <67% (likely emulation)
```

## Network Protocol

### Proof Submission

```json
{
  "miner_id": "RTC4325af95d26d59c3ef025963656d22af638bb96b",
  "epoch": 12345,
  "nonce": 6789,
  "hash": "0x1a2b",
  "hardware_fingerprint": "0xdead",
  "platform": "Joust Arcade (1982)",
  "cpu": "Motorola 6809 @ 1.5 MHz",
  "timestamp": "2026-03-14T05:45:00Z",
  "signature": "ed25519_signature_hex"
}
```

### Response

```json
{
  "status": "accepted",
  "reward": 0.36,
  "multiplier": 3.0,
  "block_height": 98765
}
```

## Performance Estimates

### Theoretical Performance

| Metric | Value |
|--------|-------|
| CPU Speed | 1.5 MHz |
| Hash Rate | ~0.001 H/s (1 hash / 15 min) |
| Epoch Duration | 10 minutes |
| Expected Hashes/Epoch | ~0.67 |
| Probability of Success | ~6.7% (at target 0x000A) |
| Expected Earnings | 0.36 RTC/epoch (with 3.0× multiplier) |

### Power Consumption

| Component | Power |
|-----------|-------|
| 6809 CPU | ~2 W |
| ROM/RAM | ~3 W |
| Video Circuitry | ~15 W |
| Audio | ~5 W |
| Cabinet Lighting | ~25 W |
| **Total** | **~50 W** |

### Cost Analysis

- Power: 50W × 24h × 30 days = 36 kWh/month
- At $0.12/kWh: ~$4.32/month
- Expected earnings: ~86.4 RTC/month (~$8.64)
- **Profit: ~$4.32/month** (theoretical)

## Hardware Modifications Required

### For Real Deployment

1. **Network Interface**
   - Ethernet or WiFi adapter
   - SPI or parallel interface to 6809
   - Additional ROM for network stack

2. **Storage**
   - EEPROM for wallet keys
   - Battery-backed RAM for epoch/nonce

3. **Co-Processor**
   - Modern microcontroller (ESP32, etc.)
   - Handles HTTPS/TLS
   - Bridges 6809 to network

4. **Power**
   - Stable 5V regulation
   - Noise filtering for timing accuracy

## Security Considerations

### Anti-Cheating

1. **Hardware Fingerprinting** - Proves authentic hardware
2. **VBLANK Synchronization** - Timing-based verification
3. **ROM Checksum** - Prevents code modification
4. **Anti-Emulation** - Detects software simulation

### Attack Vectors

1. **Timing Attacks** - Mitigated by jitter tolerance
2. **Replay Attacks** - Prevented by epoch/nonce uniqueness
3. **Hardware Spoofing** - Detected by 6-check fingerprint
4. **Network Attacks** - HTTPS + signature verification

## Development Tools

### Assembly Development

- **LWASM** - 6809 assembler
- **LWDIS** - 6809 disassembler
- **MAME** - Joust emulator for testing
- **Logic Analyzer** - Hardware debugging

### Python Development

- **pytest** - Unit testing
- **requests** - HTTP client
- **black** - Code formatting
- **mypy** - Type checking

## Future Enhancements

1. **Full 6809 Emulation** - Cycle-accurate CPU model
2. **Video Output** - Display mining stats on Joust screen
3. **Audio Feedback** - Use Joust sound chip for alerts
4. **Multi-Miner** - Network multiple Joust cabinets
5. **Hardware Interface** - PCB design for network bridge

## References

- [Motorola 6809 Programming Manual](https://archive.org/details/bitsavers_motorola68_13419254)
- [Joust Arcade Schematics](https://www.arcade-museum.com/game_detail.php?game_id=8243)
- [RustChain Whitepaper](https://github.com/Scottcjn/Rustchain/blob/main/docs/RustChain_Whitepaper_v2.2.pdf)
- [Williams Defender Hardware](https://www.arcade-museum.com/game_detail.php?game_id=7926)

## License

MIT License - See LICENSE file for details

---

*Made with ⚡ for the Joust arcade platform (1982)*
