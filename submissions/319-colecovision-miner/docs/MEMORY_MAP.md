# ColecoVision Memory Map - RustChain Miner

## Overview

The ColecoVision has **extremely limited memory** compared to modern systems. This document details how every single byte is allocated and optimized.

## Total Available Memory

| Type | Size | Notes |
|------|------|-------|
| **System RAM** | 1 KB | Only 1024 bytes for everything! |
| **Video RAM** | 16 KB | TMS9918, not directly usable for computation |
| **Cartridge ROM** | 8 KB max | Our code + data must fit here |

## System Memory Map

```
$0000 ┌─────────────────────────────────┐
      │                                 │
      │      System ROM (BIOS)          │
      │         4 KB                    │
      │                                 │
$0FFF ├─────────────────────────────────┤
$1000 │                                 │
      │    Cartridge ROM (Our Code)     │
      │         4 KB                    │
      │                                 │
$1FFF ├─────────────────────────────────┤
$2000 │                                 │
      │      System RAM (1 KB)          │
      │    ★ OUR ONLY WORKSPACE! ★      │
      │                                 │
$23FF ├─────────────────────────────────┤
$2400 │                                 │
      │       Video RAM (16 KB)         │
      │    TMS9918 Graphics Chip        │
      │                                 │
$3FFF ├─────────────────────────────────┤
$4000 │                                 │
      │    Memory Mapped I/O            │
      │         Unused                  │
      │                                 │
$FFFF └─────────────────────────────────┘
```

## RAM Allocation Detail (1024 bytes @ $2000-$23FF)

### Stack (256 bytes) - `$2000-$20FF`

```
$2000 ┌─────────────────────────────────┐
      │         Stack Bottom            │
      │         (grows upward)          │
      │                                 │
      │  Used for:                      │
      │  - Subroutine calls (CALL)      │
      │  - Interrupt handling           │
      │  - Temporary register save      │
      │                                 │
$20FF ├─────────────────────────────────┤
      │         Stack Top               │
      │         (initial SP)            │
      └─────────────────────────────────┘
```

**Why 256 bytes?**
- Maximum call depth: ~20 levels
- Each CALL pushes 2-byte return address
- Safety margin for interrupts
- Z80 doesn't use stack for local variables (no stack frame)

### Mining State (256 bytes) - `$2100-$21FF`

```
Offset  Size  Purpose
──────  ────  ─────────────────────────────
$00     4     Nonce Counter (32-bit)
$04     4     Current Hash (4 bytes of SHA-256)
$08     4     Best Hash Found (4 bytes)
$0C     1     Hash Count (for rate calculation)
$0D     1     Hash Rate (cached value)
$0E     246   Reserved / Future expansion
```

**Memory Layout:**
```assembly
NONCE_COUNTER  EQU $2100  ; DB $00,$00,$00,$00
CURRENT_HASH   EQU $2104  ; DB $00,$00,$00,$00
BEST_HASH      EQU $2108  ; DB $FF,$FF,$FF,$FF
HASH_COUNT     EQU $210C  ; DB $00
HASH_RATE      EQU $210D  ; DB $00
```

### Hash Working Buffer (128 bytes) - `$2200-$227F`

```
Offset  Size  Purpose
──────  ────  ─────────────────────────────
$00     64    Hash Input Buffer (block header)
$40     8     Hash State (intermediate values)
$48     8     SHA-256 Constants (first 8 bytes)
$50     56    Temporary / Message Schedule
```

**SHA-256 Memory Optimization:**

Full SHA-256 requires:
- 64 × 4-byte message schedule = 256 bytes ❌
- 8 × 4-byte hash state = 32 bytes
- **Total: 288 bytes** (too large!)

Our truncated version:
- 64-byte input buffer = 64 bytes ✓
- 8-byte hash state = 8 bytes ✓
- **Total: 72 bytes** (fits!)

### Display Buffer (64 bytes) - `$2280-$22BF`

```
Offset  Size  Purpose
──────  ────  ─────────────────────────────
$00     9     Nonce Display String ("0x" + 8 hex)
$09     4     Hash Rate Display (3 digits + null)
$0D     16    Status Message
$1D     43    Reserved / Pattern Buffer
```

**Display Format:**
```
Nonce:  "0x" + 8 hex chars + null = 9 bytes
Rate:   3 digits + null = 4 bytes
Status: "MINING..." or "FOUND!" = 16 bytes
```

### Temporary Space (64 bytes) - `$22C0-$22FF`

```
Used for:
- Register save areas
- Intermediate calculations
- I/O buffer
- Function parameters
```

### Block Header Template (64 bytes) - `$22D0-$230F`

```
Offset  Size  Purpose
──────  ────  ─────────────────────────────
$00     4     "RUST" magic bytes
$04     5     "CHAIN" magic bytes
$09     3     Version/flags
$0C     32    Previous block hash (truncated)
$2C     4     Timestamp (simplified)
$30     4     Difficulty target
$34     4     Nonce (overwritten each attempt)
```

### Difficulty Target (4 bytes) - `$2310-$2313`

```
Default: $00 $00 $FF $FF
Meaning: First byte must be $00, second must be ≤ $00
         Third and fourth bytes ≤ $FF
         
This is EXTREMELY easy difficulty for demonstration.
Real mining would be: $00 $00 $00 $1F (much harder)
```

## Video RAM Layout (TMS9918)

The 16 KB VRAM is **not directly accessible** by the Z80 for computation. It's only used for display output.

```
$0000 ┌─────────────────────────────────┐
      │    Pattern Generator Table      │
      │    (Character definitions)      │
      │         8 KB                    │
$1FFF ├─────────────────────────────────┤
$2000 │                                 │
      │    Name Table (Screen)          │
      │    32 × 24 = 768 bytes          │
      │                                 │
$22FF ├─────────────────────────────────┤
$2300 │    Color Table                  │
$23FF ├─────────────────────────────────┤
      │    Sprite Attribute Table       │
      │    Sprite Pattern Table         │
      │    (Unused by miner)            │
$3FFF └─────────────────────────────────┘
```

## Optimization Techniques Used

### 1. In-Place Computation

Instead of copying data between buffers, we compute directly:

```assembly
; BAD: Uses extra memory
LD DE, TempBuffer
LDIR
CALL HashFunction

; GOOD: In-place
CALL HashFunction  ; Operates on HashBuffer directly
```

### 2. Register Reuse

Z80 has limited registers, so we reuse them aggressively:

```assembly
; Use HL for pointer, then reuse for counter
LD HL, DataPointer
; ... use HL ...
LD HL, Counter
; ... reuse HL ...
```

### 3. Bit-Level Packing

Pack multiple flags into single bytes:

```assembly
; Status byte:
; Bit 7: Mining active
; Bit 6: New hash found
; Bit 5: Display update needed
; Bit 4-0: Reserved
LD A, (StatusByte)
BIT 7, A
JR Z, NotMining
```

### 4. Unrolled Loops

Trade code size for speed (we have ROM space):

```assembly
; Instead of looping 4 times:
INC (HL)
INC (HL)
INC (HL)
INC (HL)
; Faster than loop overhead!
```

## Memory Usage Summary

| Section | Bytes | Percentage |
|---------|-------|------------|
| Stack | 256 | 25.0% |
| Mining State | 256 | 25.0% |
| Hash Buffer | 128 | 12.5% |
| Display | 64 | 6.25% |
| Temporary | 64 | 6.25% |
| Block Header | 64 | 6.25% |
| Difficulty | 4 | 0.4% |
| **Used** | **836** | **81.6%** |
| **Free** | **188** | **18.4%** |
| **Total** | **1024** | **100%** |

## Comparison to Modern Systems

| System | RAM | Ratio to ColecoVision |
|--------|-----|----------------------|
| ColecoVision | 1 KB | 1× |
| Arduino Uno | 2 KB | 2× |
| Raspberry Pi Pico | 264 KB | 264× |
| Modern Smartphone | 8 GB | 8,388,608× |
| Mining GPU | 24 GB | 25,165,824× |

**We're fitting an entire mining operation into less memory than a single emoji takes on your phone!** 😄

---

*Every byte counts when you only have 1024 of them.*
