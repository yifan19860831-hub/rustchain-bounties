# Game & Watch Hardware Specifications

## Original Hardware (1980)

### CPU: Sharp SM5xx Series
- **Architecture**: 4-bit microcontroller
- **Clock Speed**: ~500 kHz (0.5 MHz)
- **Process**: NMOS (early semiconductor technology)
- **Package**: Die-on-board (chip bonded directly to PCB)
- **Features**: Integrated LCD driver, mask-programmed ROM

### Memory
| Type | Size | Notes |
|------|------|-------|
| RAM | 260 bytes | Working memory, volatile |
| ROM | 1,792 bytes | Mask-programmed, contains game logic |
| Total | 2,052 bytes | ~2 KB total |

### Display
- **Type**: Segmented liquid crystal display (LCD)
- **Technology**: Twisted nematic (TN) LCD
- **Segments**: ~50-100 fixed segments (varies by game)
- **Refresh**: Static drive (no multiplexing needed)
- **Color**: Gray on dark background (reflective)
- **Backlight**: None (relied on ambient light)

### Power
- **Supply**: 2 × LR44 button cells (3V total)
- **Consumption**: ~0.1-0.5 mW (extremely low)
- **Battery Life**: 6-12 months typical use

### Physical
- **Dimensions**: ~10 × 8 × 2 cm (varies by model)
- **Weight**: ~80-100 grams
- **Materials**: ABS plastic case, glass LCD
- **Buttons**: 3-6 rubber membrane switches

## Modern Comparison

| Component | Game & Watch (1980) | Modern Smartphone | Ratio |
|-----------|---------------------|-------------------|-------|
| RAM | 260 bytes | 8 GB | 1 : 32,000,000 |
| ROM | 1,792 bytes | 256 GB | 1 : 150,000,000 |
| CPU | 4-bit @ 500kHz | 64-bit @ 3GHz | 1 : 600,000 |
| Display | 100 segments | 2,000,000 pixels | 1 : 20,000 |
| Power | 0.5 mW | 5,000 mW | 1 : 10,000 |

## Why Full Miner Is Impossible

### SHA256 Hash Requirements
A typical SHA256 implementation requires:
- **Code size**: ~2-4 KB (exceeds ROM)
- **Working memory**: ~256 bytes for state (uses ALL RAM)
- **No room for**: Network stack, block storage, anything else

### Network Stack Requirements
Minimal TCP/IP stack:
- **Code size**: ~10-20 KB
- **RAM for buffers**: ~2-4 KB
- **Completely impossible** on this hardware

### Block Header Storage
Single Bitcoin-style block header:
- **Size**: 80 bytes
- **Would consume**: 31% of total RAM
- **No room for**: Processing, counters, display

## Badge Only Approach

Given these constraints, the "Badge Only" solution:

### What Fits in 260 Bytes RAM
```
Memory Layout (260 bytes):
├─ Display state (16 bytes)
├─ Mining state (16 bytes)
├─ Wallet cache (16 bytes, abbreviated)
├─ Nonce counter (4 bytes)
├─ RTC balance (4 bytes)
├─ Temp space (16 bytes)
└─ General purpose (188 bytes)
Total: 260 bytes ✓
```

### What We Display
- Current time (uses existing clock hardware)
- Mining status icon (animated)
- RTC balance counter (3 digits)
- Wallet address (abbreviated, symbolic)
- Battery indicator

### Symbolic Mining
- Nonce counter increments (visual only)
- Random "share found" events (simulated)
- No actual hash computation
- No network communication
- Purely demonstrative

## Hardware Modification Requirements

To actually run this on real hardware:

### Option 1: Original Hardware (Extremely Difficult)
1. Decapsulate Sharp SM5xx chip
2. Reverse engineer mask ROM
3. Create custom ROM with miner code
4. Repackage chip
5. Solder back to PCB
6. **Risk**: High chance of destroying unit

### Option 2: Modern MCU Replacement (Recommended)
1. Remove original SM5xx (or leave in place)
2. Install STM32 or similar modern MCU
3. Wire to existing LCD segments
4. Program with badge firmware
5. **Benefit**: Preserves original unit, reversible

### Option 3: External Display (Easiest)
1. Keep Game & Watch intact (collector value)
2. Build separate display mimicking LCD
3. Run simulator on modern hardware
4. Display in Game & Watch-style case
5. **Benefit**: No risk to vintage hardware

## Attestation for Proof-of-Antiquity

To claim the bounty, we need to prove:

### Hardware Authenticity
- [ ] Serial number documentation
- [ ] Manufacturing date verification
- [ ] Original components (photos)
- [ ] Functional demonstration (video)

### Software Implementation
- [ ] Source code repository
- [ ] Build instructions
- [ ] Memory usage proof (< 260 bytes)
- [ ] Cycle-accurate emulation (if simulated)

### Mining Activity
- [ ] Wallet address displayed
- [ ] Nonce counter incrementing
- [ ] "Share found" events (even if simulated)
- [ ] Continuous operation proof (time-lapse)

## References

- Nintendo Game & Watch Wikipedia: https://en.wikipedia.org/wiki/Game_%26_Watch
- Sharp SM5xx Datasheet: (archived, contact Nintendo)
- LCD Technology History: https://en.wikipedia.org/wiki/Liquid-crystal_display
- RustChain Proof-of-Antiquity: https://github.com/Scottcjn/RustChain

---

**Note**: This document is part of the RustChain Game & Watch Miner bounty submission.
Wallet: `RTC4325af95d26d59c3ef025963656d22af638bb96b`
