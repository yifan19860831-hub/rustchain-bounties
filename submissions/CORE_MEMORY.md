# IBM 703 Stretch Magnetic-Core Memory

## Overview

The IBM 703 Stretch featured one of the most advanced memory systems of its era, using **8-way interleaved magnetic-core memory** to achieve unprecedented performance.

## Technical Specifications

| Parameter | Value |
|-----------|-------|
| **Technology** | Ferrite magnetic cores |
| **Word Size** | 64 bits |
| **Base Capacity** | 16,384 words (128 KB) |
| **Maximum Capacity** | 262,144 words (2 MB) |
| **Access Time** | 2.18 microseconds |
| **Cycle Time** | 2.18 microseconds |
| **Memory Banks** | 8 (interleaved) |
| **Read Type** | Non-destructive |
| **Write Type** | Destructive (rewrite required) |

## Magnetic-Core Technology

### Core Structure

Each bit was stored in a tiny ferrite core (magnetic ring):

```
        ┌─────────┐
        │         │
    ────┤  CORE   ├────  X drive line
        │         │
        └─────────┘
            │
            │  Y drive line (perpendicular)
            │
```

### Operating Principle

1. **Magnetization**: Core can be magnetized clockwise (1) or counter-clockwise (0)
2. **Read**: Apply current to X and Y lines - if core was 1, voltage pulse induced in sense wire
3. **Write**: Apply current in opposite direction to set desired state
4. **Non-destructive read**: Unlike earlier memories, Stretch cores didn't lose data on read

### Core Characteristics

```
Core Size:        ~1-2 mm outer diameter
Material:         Ferrite (iron oxide ceramic)
Coercivity:       ~1 oersted
Remanence:        ~3000 gauss
Switching Time:   ~0.5 microseconds
Temperature Range: -55°C to +125°C
```

## 8-Way Interleaving

### Memory Organization

Memory was divided into 8 independent banks that could be accessed concurrently:

```
┌─────────────────────────────────────────────────────────────────┐
│                    IBM 703 MEMORY BANKS                          │
├──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┐
│  Bank 0  │  Bank 1  │  Bank 2  │  Bank 3  │  Bank 4  │  Bank 5  │  Bank 6  │  Bank 7  │
├──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ Word 0   │ Word 1   │ Word 2   │ Word 3   │ Word 4   │ Word 5   │ Word 6   │ Word 7   │
│ Word 8   │ Word 9   │ Word 10  │ Word 11  │ Word 12  │ Word 13  │ Word 14  │ Word 15  │
│ Word 16  │ Word 17  │ Word 18  │ Word 19  │ Word 20  │ Word 21  │ Word 22  │ Word 23  │
│ Word 24  │ Word 25  │ Word 26  │ Word 27  │ Word 28  │ Word 29  │ Word 30  │ Word 31  │
│   ...    │   ...    │   ...    │   ...    │   ...    │   ...    │   ...    │   ...    │
└──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┘

Address Mapping:
  Bank = Address MOD 8
  Offset = Address DIV 8
```

### Concurrent Access

The key advantage: **8 words can be read/written simultaneously** if they're in different banks!

```
Optimal Access Pattern (all concurrent):
  Cycle 1: Read Word 0, 1, 2, 3, 4, 5, 6, 7  (8 banks, 2.18 μs total!)
  
Suboptimal Access Pattern (serialized):
  Cycle 1: Read Word 0  (Bank 0)
  Cycle 2: Read Word 8  (Bank 0) - must wait!
  Cycle 3: Read Word 16 (Bank 0) - must wait!
  ...
  Total: 8 × 2.18 μs = 17.44 μs (8× slower!)
```

### Performance Impact

For SHA-256 mining, interleaving is crucial:

```
SHA-256 Message Schedule (16 words):
  Without interleaving: 16 × 2.18 μs = 34.88 μs
  With 8-way interleaving: 2 × 2.18 μs = 4.36 μs (8× faster!)
```

## Memory Map

### Standard Configuration (16K words)

```
Address Range      Size        Usage
─────────────────────────────────────────────────────
0x0000-0x00FF      256 words   System reserved
0x0100-0x01FF      256 words   Miner program
0x0200-0x02FF      256 words   Epoch counters
0x0300-0x03FF      256 words   Wallet address storage
0x0400-0x07FF      1024 words  Working registers
0x0800-0x0FFF      2048 words  SHA-256 message schedule
0x1000-0x1FFF      4096 words  Mining state machine
0x2000-0x3FFF      8192 words  General purpose
```

### Extended Configuration (256K words)

```
Address Range      Size         Usage
──────────────────────────────────────────────────────
0x00000-0x0FFFF    65,536 words System + miner
0x10000-0x1FFFF    65,536 words SHA-256 tables
0x20000-0x2FFFF    65,536 words Attestation buffers
0x30000-0x3FFFF    65,536 words General purpose
```

## Timing Characteristics

### Access Timing

```
Read Operation:
  t_access = 2.18 μs (address to data valid)
  
Write Operation:
  t_write = 2.18 μs (address to data stored)
  
Cycle Time:
  t_cycle = 2.18 μs (minimum between accesses)
```

### Concurrent Access Timing

```
Single Bank Access:
  ┌─────────┐
  │  2.18μs │
  └─────────┘

8-Bank Concurrent Access:
  ┌─────────────────────────────────────────┐
  │  2.18μs (all 8 banks simultaneously!)   │
  └─────────────────────────────────────────┘

Effective Bandwidth:
  Single access: 64 bits / 2.18 μs = 29.4 Mbps
  Concurrent:    512 bits / 2.18 μs = 235 Mbps (8×!)
```

## Hardware Fingerprinting

The magnetic-core memory provides unique fingerprinting opportunities:

### 1. Core Timing Variations

Each core has slightly different switching characteristics:

```
Core #1: t_switch = 0.48 μs
Core #2: t_switch = 0.52 μs
Core #3: t_switch = 0.50 μs
...

These variations create a unique "timing signature" for the memory.
```

### 2. Bank Access Patterns

Manufacturing variations between banks:

```
Bank 0: t_access = 2.17 μs
Bank 1: t_access = 2.19 μs
Bank 2: t_access = 2.18 μs
...

Pattern: [2.17, 2.19, 2.18, 2.20, 2.16, 2.19, 2.18, 2.17]
```

### 3. Temperature Coefficient

Core memory timing varies with temperature:

```
Temperature Coefficient: ~0.1% per °C

At 20°C: t_access = 2.18 μs
At 30°C: t_access = 2.20 μs
At 40°C: t_access = 2.22 μs

This creates a thermal fingerprint based on:
- Ambient temperature
- Cooling system efficiency
- Power dissipation patterns
```

### 4. Age-Related Degradation

Core properties change over decades:

```
New (1961):     t_switch = 0.50 μs
Aged (2026):    t_switch = 0.55 μs (+10%)

Degradation pattern is unique to each core!
```

## Mining Implementation

### SHA-256 Memory Layout

```
Memory Region: 0x0800-0x0FFF (2048 words)

Layout:
  0x0800-0x080F: Message schedule W[0..15]  (16 words)
  0x0810-0x083F: Extended schedule W[16..63] (48 words)
  0x0840-0x085F: Working variables a-h      (8 words)
  0x0860-0x089F: Constants K[0..63]         (64 words)
  0x08A0-0x08BF: Hash state H[0..7]         (8 words)
```

### Optimized Access Pattern

Use interleaving for maximum performance:

```assembly
; Load 8 message words concurrently (different banks)
L 1, MSG+0(0)    ; Bank 0
L 2, MSG+1(0)    ; Bank 1
L 3, MSG+2(0)    ; Bank 2
L 4, MSG+3(0)    ; Bank 3
L 5, MSG+4(0)    ; Bank 4
L 6, MSG+5(0)    ; Bank 5
L 7, MSG+6(0)    ; Bank 6
L 8, MSG+7(0)    ; Bank 7
; All 8 loads complete in 2.18 μs!

; Process while next 8 words load
; (superscalar execution)
```

## Historical Context

### Development

- **Announced**: 1956
- **First delivery**: 1961
- **Manufacturer**: IBM
- **Design goal**: 100× faster than IBM 704
- **Achieved**: 30-40× faster

### Cost

```
Base memory (16K words):  Included in $13.5M system
Extended memory (256K):   Additional ~$2M
Cost per word:            ~$0.83 (1961 dollars)
Cost per byte:            ~$0.10 (1961 dollars)

Adjusted for inflation (2026):
  Cost per word: ~$8.50
  Cost per byte: ~$1.06
```

### Legacy

Magnetic-core memory dominated computing for 20 years:

- **1950s-1970s**: Primary memory technology
- **Replaced by**: Semiconductor RAM (1970s)
- **Advantages**: Non-volatile, radiation-hardened
- **Disadvantages**: Expensive, power-hungry, slow

## References

- [IBM 703 Stretch Reference Manual](http://www.bitsavers.org/pdf/ibm/7030/A22-6688-3_7030_REF_MAN_Apr61.pdf)
- [Magnetic Core Memory - Wikipedia](https://en.wikipedia.org/wiki/Magnetic-core_memory)
- [BITSavers IBM 703 Documentation](http://www.bitsavers.org/pdf/ibm/7030/)
- [Computer History Museum: Core Memory](https://computerhistory.org/collections/catalog/102643706)

---

*The IBM 703's 8-way interleaved magnetic-core memory was revolutionary for 1961, enabling superscalar execution and pipelined operation decades before these concepts became mainstream.*
