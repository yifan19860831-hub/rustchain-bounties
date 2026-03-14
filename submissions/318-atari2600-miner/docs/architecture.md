# Atari 2600 Architecture for Mining

## 📜 MOS 6507 CPU Specifications

| Property | Value | Notes |
|----------|-------|-------|
| **Clock Speed** | 1.19 MHz | ~1 million cycles/second |
| **Data Width** | 8-bit | One byte at a time |
| **Address Width** | 13-bit | 8 KB max addressable |
| **Instructions** | 56 total | Reduced from 6502's 56 |
| **Interrupts** | NONE | Pins physically removed |
| **Transistors** | 3,510 | Modern CPU: billions |
| **Process** | ~4 μm | Modern: 3-5 nm |

### Pin Configuration (28-pin DIP)

```
        /RES  1 ┌───┐ 28  φ2 (clock out)
         Vss  2 │   │ 27  φ0 (clock in)
         RDY  3 │   │ 26  R/W (read/write)
         Vcc  4 │   │ 25  D0 (data bit 0)
          A0  5 │   │ 24  D1
          A1  6 │   │ 23  D2
          A2  7 │   │ 22  D3
          A3  8 │   │ 21  D4
          A4  9 │   │ 20  D5
          A5 10 │   │ 19  D6
          A6 11 │   │ 18  D7
          A7 12 │   │ 17  A12 (address bit 12)
          A8 13 │   │ 16  A11
          A9 14 │   │ 15  A10
          └───┘
```

**Missing vs 6502**: A13-A15 (address bits), IRQ, NMI, SYNC

---

## 💾 Memory Constraints

### 128 Bytes RAM - The Ultimate Constraint

The Atari 2600 has **128 BYTES** of RAM. Not kilobytes. Bytes.

For comparison:
- A single tweet: ~280 bytes
- This sentence: ~100 bytes
- Modern CPU L1 cache: 32-64 KB (256-512x more)
- Modern CPU L2 cache: 256 KB-1 MB (2,000-8,000x more)

### Memory Map

```
$00-$7F (0-127): System RAM

Mining Allocation:
┌────────────────────────────────────────┐
│ $00-$01: Nonce counter (16-bit)        │  ← 2 bytes
│ $02-$05: Hash result (32-bit)          │  ← 4 bytes
│ $06:     Difficulty threshold          │  ← 1 byte
│ $07:     Status flag                   │  ← 1 byte
│ $08-$0F: Display buffer                │  ← 8 bytes
│ $10-$1F: Kernel stack                  │  ← 16 bytes
│ $20-$7F: General workspace             │  ← 96 bytes
└────────────────────────────────────────┘
Total: 128 bytes
```

### Why Real SHA-256 Is Impossible

SHA-256 algorithm requirements:

```c
// SHA-256 state variables (8 x 32-bit)
uint32_t h[8] = {
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
};  // 32 bytes

// Round constants (64 x 32-bit)
const uint32_t k[64] = {
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    // ... 60 more constants
};  // 256 bytes

// Message schedule (64 x 32-bit)
uint32_t w[64];  // 256 bytes

// Working variables
uint32_t a, b, c, d, e, f, g, h;  // 32 bytes

// TOTAL: ~576 bytes minimum
```

**Atari 2600 RAM: 128 bytes**
**SHA-256 minimum: ~576 bytes**

**Conclusion**: Real SHA-256 requires **4.5x more RAM than the entire system has**.

### Our Solution: Truncated Hash

1. Use full SHA-256 in Python simulator (unlimited RAM)
2. Store only 4 bytes of result on Atari (fits in 128 bytes)
3. Compare first byte against difficulty threshold
4. This demonstrates the *concept* of mining

---

## 📺 Display: "Racing the Beam"

### The TIA Chip

The Television Interface Adaptor (TIA) generates video output. Unlike modern systems:

- **No frame buffer**: Nothing is stored in memory
- **Real-time rendering**: CPU must update graphics as beam scans
- **Cycle-exact timing**: Missing a deadline = visual glitch

### Timing Breakdown (NTSC)

```
One Frame (1/60 second = 16.67 ms)
├── Vertical Blank:  30 scanlines (2.28 ms)  ← Safe for computation
├── Visible:        192 scanlines (14.59 ms) ← Must draw pixels!
└── Overscan:        30 scanlines (2.28 ms)  ← Safe for computation
                    ────────────────────────
                    262 scanlines total

Per Scanline: 76 CPU cycles @ 1.19 MHz
```

### Kernel Structure

```assembly
Frame:
    JSR VerticalBlank   ; 30 scanlines - can compute here
    JSR VisibleKernel   ; 192 scanlines - must draw every 76 cycles
    JSR Overscan        ; 30 scanlines - can compute here
    JMP Frame
```

### Mining During Blanks

```
Vertical Blank (30 scanlines × 76 cycles = 2,280 cycles):
    - Increment nonce
    - Compute hash (simplified)
    - Check difficulty

Visible (192 scanlines × 76 cycles = 14,592 cycles):
    - Update playfield registers
    - Draw player sprites
    - NO time for mining!

Overscan (30 scanlines × 76 cycles = 2,280 cycles):
    - Prepare next frame
    - Update statistics
```

**Total mining cycles per frame: ~4,560**
**At 1.19 MHz: ~0.004 seconds of computation**

---

## ⚡ Performance Analysis

### Hash Rate Estimation

Simplified mining per attempt:
1. Increment nonce: 4 cycles
2. XOR operations (fake hash): 20 cycles
3. Compare to target: 4 cycles
4. Update display vars: 10 cycles
**Total: ~38 cycles per hash**

Cycles available per frame: ~4,560
Hashes per frame: 4,560 / 38 ≈ 120 hashes
Frames per second: 60
**Hash rate: 120 × 60 = 7,200 H/s** (optimistic theoretical max)

**Realistic** (with display overhead, timing constraints):
**~100-1,000 H/s** (0.0001 KH/s)

### Comparison Table

| System | Hash Rate | Relative Speed |
|--------|-----------|----------------|
| Atari 2600 | 0.0001 KH/s | 1x |
| Raspberry Pi Zero | 1 KH/s | 10,000x |
| Modern CPU | 1,000 KH/s | 10,000,000x |
| RTX 4090 GPU | 100,000,000 KH/s | 1,000,000,000,000x |

### Time to Find One Block

With difficulty = 1/256 (first byte < 0x0F):
- Probability: 15/256 ≈ 5.86%
- Expected attempts: 17
- Atari 2600 @ 0.0001 KH/s: **~3 minutes** (very easy!)

With real Bitcoin difficulty (~1 in 10²³):
- Expected attempts: 10²³
- Atari 2600 @ 0.0001 KH/s: **~317,000 years**

---

## 🔧 Instruction Set (56 Instructions)

### Key Instructions for Mining

```assembly
; Arithmetic
ADC  ; Add with carry
SBC  ; Subtract with carry
INC  ; Increment memory
DEC  ; Decrement memory
INX  ; Increment X register
DEX  ; Decrement X register

; Logic
AND  ; Bitwise AND
ORA  ; Bitwise OR
EOR  ; Bitwise XOR (useful for hashing!)
ASL  ; Arithmetic shift left
LSR  ; Logical shift right
ROL  ; Rotate left
ROR  ; Rotate right

; Memory
LDA  ; Load accumulator
STA  ; Store accumulator
LDX  ; Load X register
STX  ; Store X register
LDY  ; Load Y register
STY  ; Store Y register

; Control
JMP  ; Jump
BCC  ; Branch if carry clear
BCS  ; Branch if carry set
BEQ  ; Branch if equal
BNE  ; Branch if not equal
BMI  ; Branch if minus
BPL  ; Branch if plus
BVC  ; Branch if overflow clear
BVS  ; Branch if overflow set
RTS  ; Return from subroutine
```

### Example: Increment Nonce

```assembly
; 16-bit nonce increment
INC $00        ; 5 cycles - increment low byte
BNE :skip      ; 2 cycles - if not zero, skip
INC $01        ; 5 cycles - increment high byte
:skip          ; Total: 7-12 cycles
```

### Example: XOR Hash Mixing

```assembly
; Fake hash mixing (not real SHA-256)
LDA $00        ; 3 cycles - load nonce low
EOR #$5A       ; 2 cycles - XOR with constant
STA $02        ; 3 cycles - store as hash byte
; Total: 8 cycles
```

---

## 📚 References

1. [Atari 2600 Programming Guide](https://www.atariage.com/forums/topic/109971-stella-programming-guide/)
2. [6502 Datasheet](https://www.mos6502.org/datasheets/mos_6502.pdf)
3. [Visual6502](http://visual6502.org/) - Transistor-level simulation
4. [Stella Emulator Source](https://github.com/stella-emu/stella)

---

## 🎯 Conclusion

The Atari 2600 represents the **ultimate constraint programming challenge**:

- **128 bytes RAM** forces extreme optimization
- **No interrupts** means polling everything
- **Racing the beam** requires cycle-exact timing
- **8-bit CPU** limits computational complexity

Porting a blockchain miner to this platform is **technically impossible** for real mining, but serves as an excellent educational tool for understanding:

1. Cryptographic hash functions
2. Mining difficulty and probability
3. Embedded systems constraints
4. Historical computer architecture
5. Creative problem-solving under extreme limitations

**This is art, not engineering.** 🎨

---

*Document generated for RustChain Atari 2600 Miner project*
*Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b*
