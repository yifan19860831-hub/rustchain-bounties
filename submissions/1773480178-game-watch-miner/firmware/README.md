# Firmware Directory

## Purpose

This directory contains firmware source code for running the RustChain mining badge on actual Game & Watch hardware.

## Current Status

**⚠️ SIMULATION ONLY**

The firmware in this directory is currently **conceptual/aspirational**. Running on real hardware would require:

1. Physical Game & Watch unit for modification
2. Custom PCB or MCU replacement
3. Sharp SM5xx assembly programming (or modern MCU port)
4. EPROM burning and chip installation
5. Extensive testing

## Options for Implementation

### Option A: Original SM5xx (Expert Level)

**Difficulty**: ⚠️⚠️⚠️⚠️⚠️ (Extreme)

**Requirements**:
- Sharp SM5xx assembler
- Mask ROM programming equipment
- Chip decapsulation/repackaging tools
- Risk tolerance (high chance of destroying unit)

**Steps**:
1. Reverse engineer original ROM dump
2. Write miner code in SM5xx assembly
3. Create custom mask ROM
4. Replace original chip
5. Test and debug

**Estimated Time**: 40-80 hours
**Success Probability**: 20-30%

### Option B: Modern MCU Replacement (Advanced)

**Difficulty**: ⚠️⚠️⚠️ (Moderate-Hard)

**Requirements**:
- STM32 or similar 32-bit MCU
- Custom PCB to fit in Game & Watch case
- LCD segment driver circuitry
- Soldering equipment

**Steps**:
1. Design PCB matching original pinout
2. Program MCU with badge firmware (C/C++)
3. Install in Game & Watch case
4. Wire to LCD segments
5. Test and iterate

**Estimated Time**: 20-40 hours
**Success Probability**: 70-80%

### Option C: External Emulator (Beginner)

**Difficulty**: ⚠️ (Easy)

**Requirements**:
- Raspberry Pi Pico or Arduino
- LCD or OLED display
- 3D printed case (optional)

**Steps**:
1. Program Pico with badge simulator
2. Connect to display
3. Mount in Game & Watch-style case
4. Display as "emulated" miner

**Estimated Time**: 4-8 hours
**Success Probability**: 95%+

**Note**: This is what the Python simulator achieves, just on different hardware.

## Firmware Files

### sm5xx_asm/ (Original Hardware)

Assembly source for Sharp SM5xx (if attempting Option A).

**Status**: Not yet written - requires SM5xx datasheet and toolchain.

### stm32/ (MCU Replacement)

C source for STM32 microcontroller (Option B).

**Status**: Not yet written - would use STM32 HAL libraries.

### pico/ (External Emulator)

C/C++ source for Raspberry Pi Pico (Option C).

**Status**: Could be adapted from Python simulator.

## Memory Constraints Reference

```
Sharp SM5xx:
- RAM: 260 bytes
- ROM: 1,792 bytes
- CPU: 4-bit @ 500kHz

STM32 (modern replacement):
- RAM: 64 KB+ (250x more)
- ROM: 256 KB+ (140x more)
- CPU: 32-bit @ 72 MHz (144,000x faster)

Note: Using modern MCU defeats the "antiquity" aspect,
but may be necessary for practical demonstration.
```

## Attestation Requirements

For bounty claim, firmware must demonstrate:

1. **Memory Usage Proof**
   - Show actual RAM consumption < 260 bytes
   - Or document why modern hardware was used

2. **Functional Demonstration**
   - Video of running firmware
   - Show badge animations
   - Display wallet address

3. **Code Repository**
   - Public GitHub repo
   - Build instructions
   - Documentation

## Next Steps

To proceed with actual firmware:

1. **Decide approach** (A, B, or C above)
2. **Acquire hardware** (Game & Watch unit, MCU, etc.)
3. **Set up toolchain** (assembler, compiler, programmer)
4. **Write firmware** (adapt from Python simulator)
5. **Test and iterate**
6. **Record demonstration**
7. **Submit for bounty**

## Python Simulator Alternative

For immediate demonstration without hardware modification, use the Python simulator:

```bash
cd simulator/
python main.py
```

This provides the same visual experience and proves the concept, suitable for initial bounty submission with clear documentation that it's a simulation.

---

**Wallet**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`
**Bounty Tier**: LEGENDARY (200 RTC)
