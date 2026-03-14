# Atari 2600 Memory Layout - Visual Guide

## 128 Bytes of RAM - Every Byte Counts!

```
┌─────────────────────────────────────────────────────────────────┐
│                    ATARI 2600 MEMORY MAP                        │
│                         128 BYTES TOTAL                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  $00 ┌─────────────────────────────┐                           │
│  $01 │  NONCE COUNTER (16-bit)     │  ← Current mining nonce   │
│      │  Low:  $00 (0-255)          │     Increments every hash │
│      │  High: $01 (0-255)          │     Wraps at 65535        │
│      ├─────────────────────────────┤                           │
│  $02 │  HASH RESULT (32-bit)       │  ← Current hash (4 bytes) │
│  $03 │  Byte 0: Hash[0]            │     Truncated from SHA-256│
│  $04 │  Byte 1: Hash[1]            │     Compared to target    │
│  $05 │  Byte 2: Hash[2]            │                           │
│      │  Byte 3: Hash[3]            │                           │
│      ├─────────────────────────────┤                           │
│  $06 │  DIFFICULTY THRESHOLD       │  ← Target difficulty      │
│      │  (0-255, lower = harder)    │     Hash[0] < threshold   │
│      ├─────────────────────────────┤                           │
│  $07 │  STATUS FLAG                │  ← Mining state           │
│      │  0x00 = Mining              │     0x01 = Block found!   │
│      ├─────────────────────────────┤                           │
│  $08 │  DISPLAY BUFFER             │  ← Status text (8 bytes)  │
│  $09 │  "MINING..." / "FOUND!"     │     Shown on screen       │
│  $0A │                             │                           │
│  $0B │                             │                           │
│  $0C │                             │                           │
│  $0D │                             │                           │
│  $0E │                             │                           │
│  $0F │                             │                           │
│      ├─────────────────────────────┤                           │
│  $10 │  KERNEL STACK               │  ← Call stack (16 bytes)  │
│  $11 │  For subroutine calls       │     Max depth: ~8 levels  │
│  $12 │                             │                           │
│  $13 │                             │                           │
│  $14 │                             │                           │
│  $15 │                             │                           │
│  $16 │                             │                           │
│  $17 │                             │                           │
│  $18 │                             │                           │
│  $19 │                             │                           │
│  $1A │                             │                           │
│  $1B │                             │                           │
│  $1C │                             │                           │
│  $1D │                             │                           │
│  $1E │                             │                           │
│  $1F │                             │                           │
│      ├─────────────────────────────┤                           │
│  $20 │  GENERAL WORKSPACE          │  ← Free memory (96 bytes) │
│  $21 │  Temporary variables        │     Loop counters         │
│  $22 │  Computation results        │     Display prep          │
│  ... │                             │     Anything else!        │
│      │                             │                           │
│      │     [96 BYTES FREE]         │                           │
│      │                             │                           │
│  $7E │                             │                           │
│  $7F │                             │                           │
│      └─────────────────────────────┘                           │
│                                                                 │
│  TOTAL USED: 32 bytes                                           │
│  TOTAL FREE: 96 bytes                                           │
│  TOTAL:      128 bytes                                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Comparison: Modern vs Atari 2600

```
┌─────────────────────────────────────────────────────────────────┐
│                    MEMORY SIZE COMPARISON                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Atari 2600 RAM     │████░░░░░░░░░░░░░░░░│    128 bytes       │
│                     │                    │                     │
│  One Tweet          │██████████░░░░░░░░░░│    280 bytes       │
│                     │                    │                     │
│  This paragraph     │████████████████░░░░│    500 bytes       │
│                     │                    │                     │
│  Modern CPU L1      │████████████████████│  32,768 bytes      │
│  (32 KB cache)      │  (256x Atari!)     │                     │
│                     │                    │                     │
│  Modern CPU L2      │████████████████████│ 262,144 bytes      │
│  (256 KB cache)     │  (2,048x Atari!)   │                     │
│                     │                    │                     │
│  One JPEG photo     │████████████████████│   3 MB             │
│                     │  (24,000x Atari!)  │                     │
│                     │                    │                     │
│  Modern RAM (16 GB) │████████████████████│17,179,869,184 bytes│
│                     │(134 MILLION x!)    │                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## SHA-256 State Requirements vs Atari RAM

```
┌─────────────────────────────────────────────────────────────────┐
│              WHY REAL SHA-256 IS IMPOSSIBLE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SHA-256 Requirements:                                          │
│                                                                 │
│  ┌────────────────────────────────────────────────────┐        │
│  │ State Variables (8 × 32-bit)      │  32 bytes     │        │
│  ├────────────────────────────────────────────────────┤        │
│  │ Round Constants (64 × 32-bit)     │ 256 bytes     │        │
│  ├────────────────────────────────────────────────────┤        │
│  │ Message Schedule (64 × 32-bit)    │ 256 bytes     │        │
│  ├────────────────────────────────────────────────────┤        │
│  │ Working Variables (8 × 32-bit)    │  32 bytes     │        │
│  ├────────────────────────────────────────────────────┤        │
│  │ TOTAL REQUIRED                    │ 576 bytes     │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                 │
│  ┌────────────────────────────────────────────────────┐        │
│  │ Atari 2600 TOTAL RAM                │ 128 bytes   │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                 │
│  576 ÷ 128 = 4.5x MORE RAM NEEDED THAN ENTIRE SYSTEM HAS!      │
│                                                                 │
│  SOLUTION: Use full SHA-256 in Python simulator,               │
│            store only 4 bytes on Atari                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Mining Performance Timeline

```
┌─────────────────────────────────────────────────────────────────┐
│           TIME TO MINE ONE BITCOIN BLOCK                        │
│              (At Current Network Difficulty)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  System              │ Time              │ Hash Rate           │
│  ────────────────────┼───────────────────┼──────────────────   │
│  Atari 2600 (1977)   │ 317,000 years     │ 0.0001 H/s          │
│  ████████████████████│                   │                     │
│                      │                   │                     │
│  Intel 4004 (1971)   │ 3,170,000 years   │ 0.00001 H/s         │
│  ████████████████████│                   │                     │
│                      │                   │                     │
│  Raspberry Pi (2012) │ 3 years           │ 10 H/s              │
│  ████░░░░░░░░░░░░░░░░│                   │                     │
│                      │                   │                     │
│  GTX 1080 Ti (2017)  │ 22 days           │ 500,000 H/s         │
│  ██░░░░░░░░░░░░░░░░░░│                   │                     │
│                      │                   │                     │
│  RTX 4090 (2022)     │ 2.7 hours         │ 100,000,000 H/s     │
│  ░░░░░░░░░░░░░░░░░░░░│                   │                     │
│                      │                   │                     │
│  Antminer S19 (2020) │ 2.7 hours         │ 100,000,000 H/s     │
│  ░░░░░░░░░░░░░░░░░░░░│                   │                     │
│                                                                 │
│  CONCLUSION: Don't quit your day job to mine on Atari! 😄       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6507 CPU Instruction Cycles

```
┌─────────────────────────────────────────────────────────────────┐
│              MINING OPERATION CYCLE COUNT                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Operation                  │ Cycles │ Notes                    │
│  ───────────────────────────┼────────┼────────────────────────  │
│  INC $00 (increment nonce)  │   5    │ 5 cycles                 │
│  BNE :skip (branch)         │   2    │ 2 cycles if not taken    │
│  INC $01 (carry)            │   5    │ Only if low byte wraps   │
│  ───────────────────────────┼────────┼────────────────────────  │
│  LDA $00 (load)             │   3    │                          │
│  EOR #$5A (XOR hash)        │   2    │                          │
│  STA $02 (store)            │   3    │                          │
│  ───────────────────────────┼────────┼────────────────────────  │
│  CMP $06 (compare target)   │   3    │                          │
│  BCC :found (branch)        │   2    │ If below, block found!   │
│  ───────────────────────────┼────────┼────────────────────────  │
│  TOTAL PER HASH             │  ~25   │ Optimistic minimum       │
│                                                                 │
│  Cycles per frame: ~4,560 (during blanks)                      │
│  Hashes per frame: ~182                                        │
│  Frames per second: 60                                         │
│  THEORETICAL MAX: ~11,000 H/s (impossible in practice)         │
│  REALISTIC: ~100-1,000 H/s (with display overhead)             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

*Visual guide created for RustChain Atari 2600 Miner project*  
*Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b*
