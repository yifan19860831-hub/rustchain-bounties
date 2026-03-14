# TI-85 Architecture Deep Dive

## Hardware Overview

### CPU: Zilog Z80 @ 6 MHz

The Z80 is an 8-bit microprocessor introduced in 1976. Key characteristics:

```
┌─────────────────────────────────────────────────────────┐
│                    Z80 CPU Core                         │
├─────────────────────────────────────────────────────────┤
│ Registers:                                              │
│   - A (Accumulator): 8-bit                             │
│   - F (Flags): 8-bit                                   │
│   - B, C: 8-bit general purpose                        │
│   - D, E: 8-bit general purpose                        │
│   - H, L: 8-bit general purpose                        │
│   - IX, IY: 16-bit index registers                     │
│   - SP: 16-bit stack pointer                           │
│   - PC: 16-bit program counter                         │
│                                                         │
│ Register Pairs (16-bit operations):                    │
│   - BC, DE, HL, AF                                     │
└─────────────────────────────────────────────────────────┘
```

### Memory Map

```
Address Range    Size      Purpose
─────────────────────────────────────────────────
0x0000-0x3FFF    16 KB     ROM (Operating System)
0x4000-0x7FFF    16 KB     ROM (Extended functions)
0x8000-0xDFFF    24 KB     RAM (User programs)
0xE000-0xFFFF    8 KB      RAM (System variables)
─────────────────────────────────────────────────
Total RAM:       32 KB
User Available:  28 KB (approximately)
```

### Display Controller

```
Resolution: 128 × 64 pixels
Format:     Monochrome (1 bit per pixel)
Memory:     1 KB bitmap (128 × 64 ÷ 8 = 1024 bytes)
Organization: 8 rows × 128 columns
              Each row = 128 bytes (1 bit per pixel)
```

Display memory layout:
```
Row 0:  bytes 0-127   (pixels 0-127, y=0-7)
Row 1:  bytes 128-255 (pixels 0-127, y=8-15)
Row 2:  bytes 256-383 (pixels 0-127, y=16-23)
...
Row 7:  bytes 896-1023 (pixels 0-127, y=56-63)
```

### I/O Port

```
Type:       2.5mm stereo jack
Protocol:   Proprietary TI serial
Speed:      ~9600 baud
Purpose:    Calculator-to-calculator communication
Limitation: Cannot connect to PC without TI-Graph Link
```

## Programming Environment

### TI-BASIC

Built-in interpreted language:
- Easy to use
- Slow execution
- Limited memory access
- Good for prototyping

### Z80 Assembly

Requires ZShell or similar hack:
- Direct hardware access
- Maximum performance
- Full memory control
- Complex development

Assembly program structure:
```asm
; TI-85 Assembly Program Header
.org 0x8000           ; Start of user RAM

db 0xAB, 0xCD         ; TI-85 assembly signature

Main:
    ; Program entry point
    ret               ; Return to OS
```

## Memory Optimization Strategies

### 1. Code Overlays

Load only necessary code sections:
```
┌──────────────────────┐
│ Base Runtime (2 KB)  │ Always loaded
├──────────────────────┤
│ Hash Module (2 KB)   │ Load when mining
├──────────────────────┤
│ Display Module (1 KB)│ Load when updating UI
├──────────────────────┤
│ Free Space           │ For data
└──────────────────────┘
```

### 2. Data Compression

Use bit-packing for storage:
```
Normal:  8 bits per value → 32 bytes for 4 values
Packed:  4 bits per value → 16 bytes for 4 values
```

### 3. In-Place Computation

Avoid temporary buffers:
```asm
; Bad: Uses extra memory
ld a, (value)
add a, 1
ld (temp), a
ld a, (temp)
ld (value), a

; Good: In-place
ld a, (value)
inc a
ld (value), a
```

## Power Management

```
Power Source:     4 × AAA batteries (6V total)
Backup:           CR1616/CR1620 coin cell
Consumption:      ~0.5 W during operation
Battery Life:     ~200 hours continuous use

RAM Preservation:
- Main RAM volatile (loses power when batteries removed)
- Backup battery preserves memory for ~2 weeks
- Critical for maintaining mining state
```

## Link Cable Protocol

For calculator-to-calculator communication:

```
Physical Layer:
- 3-conductor cable
- 2.5mm stereo connectors
- Signals: Data+, Data-, Ground

Protocol:
- Half-duplex serial
- ~9600 baud
- Packet-based transfer

Use Case for Miner:
- Transfer new block templates
- Share found blocks
- Distributed mining (multiple TI-85s)
```

## Development Tools

### Assemblers

1. **TASM80** - TI-specific Z80 assembler
2. **z80asm** - Generic Z80 assembler
3. **Pasmo** - Cross-platform Z80 assembler

### Emulators

1. **TI-85 Emulator** (official)
2. **VirtualTI** - Community emulator
3. **Custom Python simulator** (this project)

### Debugging

```
Techniques:
- Breakpoints via NOP sleds
- Memory dumps to link cable
- LED blink codes (via display)
- Step-through with emulator
```

## Constraints Summary

| Constraint | Value | Impact on Mining |
|------------|-------|------------------|
| RAM | 28 KB | Cannot store full blockchain |
| CPU Speed | 6 MHz | ~100 hashes/second max |
| Storage | Volatile | No persistent block storage |
| Network | None | Manual block transfer only |
| Display | 128×64 | Limited status information |
| Power | Battery | ~200 hours runtime |

## Theoretical Mining Implementation

### Block Structure (32 bytes)

```c
struct Block {
    uint8_t prev_hash[8];   // Previous block hash (truncated)
    uint32_t timestamp;      // Unix timestamp
    uint32_t nonce;          // Mining nonce
    uint8_t data[16];        // Transaction data (simplified)
    uint8_t difficulty;      // Target difficulty (1-8 bits)
};
```

### Mining Loop (Assembly Pseudocode)

```asm
MiningLoop:
    ; Load current block header
    ld hl, (BlockHeader)
    
    ; Increment nonce
    ld de, (Nonce)
    inc de
    ld (Nonce), de
    
    ; Calculate hash
    call MiniHash
    
    ; Check difficulty
    ld b, (Difficulty)
    call CheckProof
    
    ; If valid, jump to FoundBlock
    jr z, FoundBlock
    
    ; Continue loop
    jp MiningLoop

FoundBlock:
    ; Store found block
    ; Update display
    ; Signal via link cable
    ret
```

### Expected Performance

```
Hash Calculation: ~60,000 clock cycles
CPU Speed: 6,000,000 Hz
Hash Rate: 6,000,000 / 60,000 = 100 hashes/second

Difficulty 1: Find hash with 1 zero bit (50% chance)
  - Expected time: 0.01 seconds

Difficulty 4: Find hash with 4 zero bits (6.25% chance)
  - Expected time: 0.16 seconds

Difficulty 8: Find hash with 8 zero bits (0.39% chance)
  - Expected time: 2.56 seconds

Note: Real SHA-256 difficulty is ~2^254, impossible on TI-85
```

## Conclusion

The TI-85 represents an extreme constraint environment that teaches:
- **Resource optimization** at the byte level
- **Algorithm simplification** for embedded systems
- **Creative problem-solving** under hardware limitations
- **Historical computing** perspectives

While impractical for real cryptocurrency mining, this exercise demonstrates fundamental principles of blockchain and embedded systems programming.
