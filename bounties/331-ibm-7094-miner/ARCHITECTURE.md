# IBM 7094 Miner - Architecture Specification

Technical architecture document for the IBM 7094 RustChain Miner simulation.

## 1. System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    IBM 7094 MINER ARCHITECTURE                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   PUNCHED    │───▶│   CORE       │───▶│   DATA       │      │
│  │   CARDS      │    │   MEMORY     │    │   CHANNELS   │      │
│  │   (Input)    │    │   (32K×36)   │    │   (I/O)      │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│                            │                                     │
│                            ▼                                     │
│                      ┌──────────────┐                           │
│                      │     CPU      │                           │
│                      │  (36-bit)    │                           │
│                      │  7 Index Reg │                           │
│                      │  AC + MQ     │                           │
│                      └──────────────┘                           │
│                            │                                     │
│                            ▼                                     │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   MAGNETIC   │◀───│   MINING     │◀───│   PUNCHED    │      │
│  │   TAPE       │    │   STATE      │    │   CARDS      │      │
│  │   (Storage)  │    │   MACHINE    │    │   (Output)   │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 2. CPU Architecture

### 2.1 Registers

```
┌─────────────────────────────────────────────────────────────────┐
│                     IBM 7094 REGISTER SET                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ACCUMULATOR (AC)                                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ S (1) │ Exponent (8) │ Mantissa (27)                     │  │
│  │ 0     │ 1-8          │ 9-35                              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  MULTIPLIER-QUOTIENT (MQ)                                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ S (1) │ Magnitude (35)                                    │  │
│  │ 0     │ 1-35                                              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  INDEX REGISTERS (XR1-XR7)                                      │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐     │
│  │ XR1 │ │ XR2 │ │ XR3 │ │ XR4 │ │ XR5 │ │ XR6 │ │ XR7 │     │
│  │ 36b │ │ 36b │ │ 36b │ │ 36b │ │ 36b │ │ 36b │ │ 36b │     │
│  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘     │
│                                                                  │
│  INSTRUCTION COUNTER (IC)                                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Unused (21) │ Address (15)                                │  │
│  │ 0-20        │ 21-35                                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  SENSE INDICATORS (SI)                                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 36 individual sense bits                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Instruction Formats

**Type A (Standard)**:
```
┌─────────┬──────────────┬─────────┬──────────────────┐
│ Opcode  │  Decrement   │   Tag   │     Address      │
│ 3 bits  │   15 bits    │ 3 bits  │    15 bits       │
│ 0-2     │   3-17       │ 18-20   │    21-35         │
└─────────┴──────────────┴─────────┴──────────────────┘
```

**Type B (Extended Opcode)**:
```
┌──────────────┬──────┬────────┬─────────┬──────────────────┐
│    Opcode    │ Flag │ Unused │   Tag   │     Address      │
│   12 bits    │ 2b   │ 4 bits │ 3 bits  │    15 bits       │
│   0-11       │12-13 │ 14-17  │ 18-20   │    21-35         │
└──────────────┴──────┴────────┴─────────┴──────────────────┘
```

### 2.3 Core Instruction Set

| Mnemonic | Opcode | Description | Cycles |
|----------|--------|-------------|--------|
| CLA | 0100 | Clear and Add | 2 |
| ADD | 0101 | Add | 2 |
| SUB | 0110 | Subtract | 2 |
| STA | 0111 | Store Accumulator | 2 |
| LAC | 1100 | Load AC from MQ | 1 |
| CAS | 1101 | Compare AC and Store | 2 |
| TZE | 3001 | Transfer on Zero | 2 |
| TRA | 3000 | Transfer Unconditional | 2 |
| HPR | 5000 | Halt and Proceed | 1 |
| PRT | 6000 | Print (I/O) | Variable |

## 3. Memory System

### 3.1 Core Memory Organization

```
Total Capacity: 32,768 words × 36 bits = 147,456 bytes (144 KB)

Memory Plane Organization:
┌─────────────────────────────────────────────────────────────────┐
│  Plane 0   │  Plane 1   │  ...  │  Plane 35  │                 │
│  (Bit 0)   │  (Bit 1)   │       │  (Bit 35)  │                 │
│  ┌─────┐   │  ┌─────┐   │       │  ┌─────┐   │                 │
│  │ 32K │   │  │ 32K │   │       │  │ 32K │   │                 │
│  │cores│   │  │cores│   │       │  │cores│   │                 │
│  └─────┘   │  └─────┘   │       │  └─────┘   │                 │
│            │            │       │            │                 │
│  All planes addressed simultaneously for 36-bit word access     │
└─────────────────────────────────────────────────────────────────┘

Cycle Time: 2.18 μs
Access Time: ~1.5 μs
Recovery Time: ~0.68 μs
```

### 3.2 Memory Map

```
Address (Octal)    Address (Decimal)    Size      Usage
─────────────────────────────────────────────────────────────────
000000-000077      0-63                 64        System reserved
000100-000177      64-127               64        Miner entry point
000200-001777      128-1023             896       Miner program code
002000-002377      1024-1279            256       Epoch counters
002400-002777      1280-1535            256       Wallet address
003000-003777      1536-2047            512       Working registers
004000-007777      2048-4095            2048      Data channel buffers
010000-077777      4096-32767           28672     General storage
```

## 4. Data Channel I/O

### 4.1 Channel Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    8 DATA CHANNELS                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  CPU ◀───────▶ Channel Controller ◀───────▶ Devices            │
│                                                                  │
│  Channel 0: IBM 729 Tape Drives (0-9)                          │
│  Channel 1: IBM 729 Tape Drives (10-19)                        │
│  Channel 2: IBM 729 Tape Drives (20-29)                        │
│  Channel 3: IBM 729 Tape Drives (30-39)                        │
│  Channel 4: IBM 729 Tape Drives (40-49)                        │
│  Channel 5: IBM 729 Tape Drives (50-59)                        │
│  Channel 6: IBM 729 Tape Drives (60-69)                        │
│  Channel 7: IBM 711 Card Reader + IBM 716 Printer              │
│                                                                  │
│  Each channel operates independently (DMA-style)               │
│  CPU initiates transfer, channel handles data movement         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Channel Commands

| Command | Code | Description |
|---------|------|-------------|
| READ | 01 | Read from device to memory |
| WRITE | 02 | Write from memory to device |
| REWIND | 03 | Rewind tape |
| SKIP | 04 | Skip forward on tape |
| SENSE | 05 | Read channel status |

## 5. Mining State Machine

### 5.1 State Transitions

```
┌─────────────────────────────────────────────────────────────────┐
│                    MINING STATE MACHINE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                          ┌─────────┐                            │
│                   ┌──────│  IDLE   │──────┐                     │
│                   │      │  (0)    │      │                     │
│                   │      └────┬────┘      │                     │
│                   │           │           │                     │
│                   │    [epoch trigger]    │                     │
│                   │           ▼           │                     │
│                   │      ┌─────────┐      │                     │
│                   │      │ MINING  │      │                     │
│                   │      │  (1)    │      │                     │
│                   │      └────┬────┘      │                     │
│                   │           │           │                     │
│                   │    [computation       │                     │
│                   │     complete]         │                     │
│                   │           ▼           │                     │
│                   │      ┌─────────┐      │                     │
│                   │      │ATTESTING│      │                     │
│                   │      │  (2)    │      │                     │
│                   │      └────┬────┘      │                     │
│                   │           │           │                     │
│                   │    [attestation       │                     │
│                   │     generated]        │                     │
│                   │           │           │                     │
│                   │           ▼           │                     │
│                   │      ┌─────────┐      │                     │
│                   └──────│ OUTPUT  │──────┘                     │
│                          │  (3)    │                            │
│                          └─────────┘                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 State Encoding

```
State Word (36 bits):
┌─────────────────────────────────────────────────────────────────┐
│ S (1) │ Unused (33) │ State Code (2)                           │
│ 0     │ 1-33        │ 34-35                                     │
└─────────────────────────────────────────────────────────────────┘

State Codes:
00 = IDLE (waiting for epoch trigger)
01 = MINING (computing proof-of-antiquity)
10 = ATTESTING (generating attestation)
11 = OUTPUT (punching cards/writing tape)
```

## 6. Punched Card Format

### 6.1 Card Layout

```
┌─────────────────────────────────────────────────────────────────┐
│                    80-COLUMN PUNCHED CARD                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Columns 1-6:    Operation code (FAP mnemonic)                  │
│  Columns 7-15:   Label (optional)                               │
│  Columns 16-30:  Operand (address, constant)                    │
│  Columns 31-72:  Comment (optional)                             │
│  Columns 73-80:  Sequence number (optional)                     │
│                                                                  │
│  Example:                                                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │0000000011111111112222222222333333333344444444445555555555│  │
│  │0123456789012345678901234567890123456789012345678901234567│  │
│  │START    CLA      EPOCH     Load epoch counter            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Character Encoding (6-bit BCD)

```
Bit Pattern    Character    Bit Pattern    Character
─────────────────────────    ─────────────────────────
000000         (null)       100001         A
000001         1            100010         B
000010         2            100011         C
...                         ...
001001         9            111010         Z
010000         space        111011         (special)
010001         .            111100         (special)
010010         ,            111101         (special)
010011         '            111110         (special)
010100         (            111111         (special)
010101         )            110000         (special)
010110         +
010111         -
011000         *
011001         /
011010         =
011011         $
011100         %
011101         &
```

## 7. Magnetic Tape Format

### 7.1 IBM 729 Tape Specifications

```
┌─────────────────────────────────────────────────────────────────┐
│                    IBM 729 TAPE FORMAT                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Tracks: 7 (6 data + 1 parity)                                  │
│  Density: 200, 556, or 800 characters per inch                  │
│  Speed: 112.5 inches per second                                 │
│  Start/Stop Time: 7.5 ms                                        │
│  Gap Between Records: 0.6 inches                                │
│                                                                  │
│  Record Format:                                                 │
│  ┌─────────┬──────────────┬─────────┬─────────────┐            │
│  │  LEADER │    RECORD    │   GAP   │   TRAILER   │            │
│  │  (blank)│    (data)    │ (0.6")  │   (blank)   │            │
│  └─────────┴──────────────┴─────────┴─────────────┘            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 Tape File Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                    TAPE FILE STRUCTURE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  File 1: Epoch Counter                                          │
│  - Record 1: Current epoch number (binary)                      │
│  - Record 2: Timestamp (BCD)                                    │
│                                                                  │
│  File 2: Wallet Address                                         │
│  - Record 1: RTC address (packed BCD)                           │
│                                                                  │
│  File 3: Attestation Output                                     │
│  - Record 1: State code                                         │
│  - Record 2: Epoch number                                       │
│  - Record 3: Hash simulation (36-bit chunks)                    │
│  - Record 4: Checksum                                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 8. Simulation Architecture

### 8.1 Python Module Structure

```
simulation/
├── ibm7094_miner.py      # Main simulator entry point
├── core_memory.py        # 32K×36 core memory emulation
├── ibm7094_cpu.py        # CPU with 7 index registers
├── index_registers.py    # XR1-XR7 management
├── data_channels.py      # 8-channel I/O simulation
├── punched_card.py       # Card reader/punch simulation
├── magnetic_tape.py      # IBM 729 tape simulation
├── fap_assembler.py      # FAP assembly language parser
├── mining_engine.py      # Proof-of-Antiquity logic
└── test_vectors/         # Test programs
    ├── hello_world.fap
    ├── mining_test.fap
    └── attestation.fap
```

### 8.2 Timing Simulation

```
Operation              Real 7094      Simulation
─────────────────────────────────────────────────
Memory cycle           2.18 μs        Instant*
Addition               2 cycles       Instant*
Multiplication         ~10 cycles     Instant*
Tape start/stop        7.5 ms         100 ms
Card read (800/min)    75 ms/card     100 ms/card
Attestation output     ~1 second      1 second

*Simulation runs at full CPU speed with optional timing delays
```

## 9. Proof-of-Antiquity Protocol

### 9.1 Attestation Generation

```
┌─────────────────────────────────────────────────────────────────┐
│                 PROOF-OF-ANTIQUITY ATTESTATION                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Input:                                                          │
│  - Epoch number (36-bit)                                        │
│  - Wallet address (packed BCD)                                  │
│  - Timestamp (simulated)                                        │
│                                                                  │
│  Processing:                                                     │
│  1. Load epoch into AC                                          │
│  2. XOR with wallet address                                     │
│  3. Apply antiquity multiplier (2.5× for 1962)                  │
│  4. Generate 36-bit "hash" (simulated SHA-256)                  │
│  5. Store result in core memory                                 │
│                                                                  │
│  Output:                                                         │
│  - Punched card with attestation                                │
│  - Magnetic tape record                                         │
│  - Console printout                                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2 Antiquity Multiplier

```
Multiplier Calculation:
Base multiplier = 1.0×
Year bonus = (2024 - 1962) / 100 = 0.62×
Technology bonus (transistor era) = 0.5×
Historical significance bonus = 0.38×
─────────────────────────────────────────────────
Total multiplier = 2.5× (maximum tier)
```

## 10. Error Handling

### 10.1 Sense Indicators

IBM 7094 used sense indicators for error reporting:

| Indicator | Meaning | Action |
|-----------|---------|--------|
| SI 0 | Overflow | Check AC/MQ |
| SI 1 | Divide check | Halt on divide error |
| SI 2-10 | Data channel errors | Check channel status |
| SI 11-35 | User defined | Custom error codes |

### 10.2 Exception Handling

```
Exception Type          Sense Indicator    Recovery
─────────────────────────────────────────────────────────────────
Arithmetic overflow     SI 0               Check result, continue
Divide check            SI 1               Halt or trap
Channel error           SI 2-10            Retry I/O operation
Parity error            SI 11              Halt, check memory
Invalid instruction     SI 12              Halt, check program
```

## 11. Performance Metrics

### 11.1 Theoretical Performance

```
Metric                    IBM 7094        Simulation
─────────────────────────────────────────────────────────────────
Instructions per second   ~200,000        Unlimited
Memory accesses/sec       ~450,000        Unlimited
Floating-point ops/sec    ~100,000        Unlimited
Tape transfers/hour       ~48,000         Limited by simulation
Card reads/hour           ~48,000         Limited by simulation
Attestations/hour         ~100 (est.)     ~3,600
```

### 11.2 Resource Requirements

```
Core Memory:            144 KB (32K × 36 bits)
Program Size:           ~1 KB
Data Size:              ~2 KB
Stack:                  Not used (7094 had no hardware stack)
Index Registers:        7 × 36 bits = 252 bits
```

## 12. Future Enhancements

- [ ] Full IBSYS operating system simulation
- [ ] CTSS time-sharing emulation
- [ ] Multi-programming support
- [ ] 7094/7044 Direct Coupled System simulation
- [ ] Real-time "Daisy Bell" synthesis
- [ ] NASA Mercury/Gemini flight software emulation
- [ ] SHARE library program compatibility

---

**Document Version**: 1.0  
**Last Updated**: 2026-03-13  
**Author**: RustChain IBM 7094 Miner Team  
**Wallet**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`
