## IBM 305 RAMAC RTC Miner — 200 RTC Bounty (LEGENDARY Tier)

Get an **IBM 305 RAMAC** mining RustChain tokens. The IBM 305 RAMAC was announced on **September 14, 1956** — the **first commercial computer with a hard disk drive**. If you can make this work, you earn the **5.0x antiquity multiplier**, the absolute maximum in RustChain.

This is the **holy grail** of vintage storage computing bounties.

### Why IBM 305 RAMAC?

- **1956 hardware** — First commercial computer with moving-head hard disk
- **Vacuum tube technology** — One of IBM's last vacuum tube computers
- **Revolutionary storage** — IBM 350 disk system (5 MB, 50× 24-inch disks)
- **Drum + Core memory** — 3,200 character drum + 100 character core buffer
- **BCD character architecture** — 6-bit data + 1-bit parity
- **5.0x multiplier** — Highest reward tier possible
- **1,000+ built** — Production 1956-1961, withdrawn 1969
- **Over 1 ton** — Required forklifts for movement
- **RAMAC** — "Random Access Method of Accounting and Control"

### The Ultimate Challenge

This is one of the hardest bounties we've ever posted:

1. **No networking** — Must build custom interface (card reader/punch or disk controller)
2. **Character architecture** — 6-bit BCD character processing, not binary
3. **Drum memory timing** — 6000 RPM drum with 10ms-30ms instruction cycles
4. **Magnetic disk I/O** — IBM 350 disk units for data storage (5 MB total)
5. **Vacuum tube reliability** — Hardware maintenance required
6. **Power consumption** — Significant vacuum tube power requirements
7. **Plugboard programming** — Jumpers on control panel for flow control

### Hardware Required

| Component | Notes |
|-----------|-------|
| IBM 305 CPU | With drum memory (3,200 characters) and core buffer (100 chars) |
| IBM 350 Disk Storage | 5 MB capacity (50× 24-inch disks) |
| IBM 380 Console | Card reader and operator console |
| IBM 323 Card Punch | For output interface |
| IBM 370 Printer | For hardcopy output |
| Microcontroller | Arduino Due / Raspberry Pi for network bridge |
| Custom interface | Connect microcontroller to card reader/disk controller pins |

### Technical Requirements

#### 1. Network Interface (50 RTC)
- Build card reader/punch or disk controller interface using microcontroller
- Microcontroller handles TCP/IP and HTTPS
- IBM 305 reads network response from cards or disk
- IBM 305 punches/writes request to output media

#### 2. Assembly System (50 RTC)
- Create cross-assembler for IBM 305 instruction set
- Build drum memory simulator for testing
- Document instruction set architecture
- Create memory layout optimizer

#### 3. Core Miner (75 RTC)
- Character-based SHA256 implementation (6-bit BCD)
- Hardware fingerprinting (tube drift, drum timing, disk seek time)
- Attestation protocol via card/disk interface
- Optimal drum memory programming (instruction placement)

#### 4. Proof & Documentation (25 RTC)
- Video of IBM 305 RAMAC mining
- Miner visible in rustchain.org/api/miners
- Complete documentation and source code
- Raw curl -v test evidence

### The 5.0x Multiplier

```
ibm305ramac / vacuum_tube + magnetic_disk — 5.0x base multiplier (MAXIMUM TIER)
```

An IBM 305 RAMAC from a museum = the highest-earning miner in RustChain history.

**Expected earnings**:
- Base: 0.12 RTC/epoch
- With 5.0×: **0.60 RTC/epoch**
- Per day: **86.4 RTC**
- Per month: **~2,592 RTC**

### Implementation Plan

See attached documentation for complete technical specifications and implementation phases.

### Architecture Details

**Character Format** (7-bit):
```
X O 8 4 2 1 R
│ │ └─┬─┘ │
│ │  Value Parity
│ └─ Zone bit O
└─ Zone bit X
```

**Instruction Format** (10 characters):
```
T1 A1 B1 T2 A2 B2 M N P Q
```

**Memory**:
- Drum: 32 tracks × 100 characters = 3,200 characters
- Core buffer: 100 characters
- Disk: 5 MB (IBM 350)

**Instruction Timing**:
- Typical: 30ms (3 drum revolutions)
- Optimized: 10ms (1 revolution with Improved Processing Speed option)
- Multiply: 60-190ms
- Divide: 100-370ms

### Resources

- [IBM 305 RAMAC Manual of Operation (1957)](https://bitsavers.trailing-edge.com/pdf/ibm/305_ramac/22-6264-1_305_RAMAC_Manual_of_Operation_Apr57.pdf)
- [IBM Archives: RAMAC](https://www.ibm.com/history/ramac)
- [Bitsavers IBM 305 Collection](https://bitsavers.trailing-edge.com/pdf/ibm/305_ramac/)
- [IBM 305 at Computer History Museum](https://ed-thelen.org/comp-hist/BRL61-ibm03.html#IBM-305-RAMAC)
- [IBM RAMAC Promotional Film](https://www.youtube.com/watch?v=zOD1umMX2s8)
- [IBM 305 RAMAC Documentary](https://www.youtube.com/watch?v=oyWsdS1h-TM)

### Claim Rules

- Partial claims accepted (complete any phase for its RTC amount)
- Full completion = **200 RTC total**
- Must be real IBM 305 RAMAC hardware (emulators don't count)
- Open source everything
- Multiple people can collaborate and split

### Partial Bounty Breakdown

| Phase | Reward | Deliverable |
|-------|--------|-------------|
| Network Interface | 50 RTC | Working network bridge |
| Assembly System | 50 RTC | Assembler + Simulator |
| Core Miner | 75 RTC | Working miner code |
| Proof & Docs | 25 RTC | Video + Documentation |

### Wallet for Bounty

```
RTC4325af95d26d59c3ef025963656d22af638bb96b
```

### Instruction Set Reference

**Source/Destination Track Codes**:

| Code | Function | Category |
|------|----------|----------|
| W, X, Y, Z | General storage | Storage |
| 0-9, A-I | Instruction/General storage | Storage |
| L | Read accumulator / Add to accumulator | Arithmetic |
| M | Read & clear / Subtract from accumulator | Arithmetic |
| V | Multiplicand (1-9 chars) or divisor | Arithmetic |
| N | Multiply (1-11 chars) | Arithmetic |
| P | Divide (optional) | Arithmetic |
| K | 380 Punched card input | I/O |
| S, T | 323 Card output / 370 Printer | I/O |
| Q | 380 Inquiry input/output | I/O |
| J | 350 File address | I/O |
| R | 350 File data input/output | I/O |
| - | Core buffer | Special |
| $ | 382 Paper tape input/output (optional) | I/O |

**Control Code** (Q field):

| Value | Operation |
|-------|-----------|
| (blank) | Copy (source to destination) |
| 1 | Compare |
| 2 | Field compare |
| 3 | Compare & Field compare |
| 5 | Accumulator reset |
| 6 | Blank transfer test |
| 7 | Compress & Expand |
| 8 | Expand |
| 9 | Compress |

---

*1956 meets 2026. The first computer with a hard drive mining cryptocurrency. Proof that revolutionary hardware still has computational value and dignity.*

cc: @Scottcjn
