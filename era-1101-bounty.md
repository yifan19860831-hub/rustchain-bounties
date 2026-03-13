# [BOUNTY] Port RustChain Miner to ERA 1101 (1950) - 200 RTC (LEGENDARY Tier)

## ERA 1101 RTC Miner — 200 RTC Bounty (LEGENDARY Tier)

**Make the first commercially available computer mine RustChain tokens.** The ERA 1101 (Engineering Research Associates 1101), later renamed UNIVAC 1101, was introduced in 1950 — the **first stored-program computer ever sold commercially**. If you can make this work, you earn the 5.0x antiquity multiplier, the absolute maximum in RustChain.

This is computing history meets cryptocurrency: **1950 meets 2026**.

---

## Why ERA 1101?

- **1950 hardware** — the first commercially available computer
- **First installed stored-program computer** — Atlas prototype installed at Army Security Agency, December 1950
- **Magnetic drum memory** — 16,384 words × 24 bits (48 KB), rotating at 3500 RPM
- **2700 vacuum tubes** — pre-transistor computing at massive scale
- **24-bit binary architecture** — ones' complement arithmetic
- **48-bit accumulator** — subtractive design (addition via complement subtraction)
- **38 instructions** — minimal but complete instruction set
- **5.0x multiplier** — the highest reward tier possible
- **Historical significance** — designed by code-breakers from WWII Navy, founded ERA in St. Paul, Minnesota

### ERA 1101 vs SWAC (Both 1950)

| Feature | ERA 1101 (1950) | SWAC (1950) |
|---------|-----------------|-------------|
| Architecture | 24-bit parallel binary | 37-bit serial binary |
| Memory | Magnetic drum (16K words) | Williams tube (256-512 words) |
| Word size | 24 bits | 37 bits |
| Clock | ~3500 RPM drum | ~1 MHz |
| Memory capacity | 48 KB | ~1.2-2.4 KB |
| Access time | 32 μs - 17 ms (rotational) | ~300 μs (serial) |
| Storage medium | Magnetic drum | Electrostatic CRT |
| Tubes | 2700 | ~800 |
| Challenge level | ⭐⭐⭐⭐⭐ (Drum scheduling) | ⭐⭐⭐⭐⭐ (Memory instability) |

**ERA 1101 is different**: larger memory but **rotational latency optimization** is critical. You must schedule instructions to minimize drum access delays — a completely different challenge from SWAC's Williams tube instability.

---

## The Ultimate Challenge

This is genuinely the hardest bounty tier, tied with SWAC and IBM 650:

- **No networking** — must build custom interface (paper tape or drum output)
- **Drum memory scheduling** — optimal instruction placement critical for performance
- **24-bit architecture** — must implement SHA256 with 24-bit words (non-standard)
- **Ones' complement arithmetic** — different from modern two's complement
- **Subtractive accumulator** — addition done by subtracting complement
- **48 KB total memory** — tight but workable with careful optimization
- **Vacuum tube reliability** — hardware maintenance required
- **Paper tape I/O** — slow, sequential access only

### Technical Requirements

#### 1. Network Interface (50 RTC)

- Build paper tape interface using microcontroller
- Microcontroller handles TCP/IP and HTTPS
- ERA 1101 reads network response via paper tape reader
- ERA 1101 punches requests via paper tape punch
- Alternative: Drum output + camera interface

#### 2. ERA 1101 Assembler (50 RTC)

- Create ERA 1101 cross-assembler (original used octal/binary)
- Build simulator for testing (Python/C++)
- Paper tape format emulation
- Drum memory layout optimization tools

#### 3. Core Miner (75 RTC)

- 24-bit SHA256 implementation (adapted from 32-bit standard)
- Hardware fingerprinting (drum timing signature, vacuum tube characteristics)
- Attestation protocol via paper tape interface
- **Drum scheduling optimization** — minimize rotational latency
- Instruction placement for minimum access time

#### 4. Proof & Documentation (25 RTC)

- Video of ERA 1101 mining
- Miner visible in rustchain.org/api/miners
- Complete documentation
- Open source all code

---

## The 5.0x Multiplier

```
era_1101 / magnetic_drum — 5.0x base multiplier (MAXIMUM TIER)
```

An ERA 1101 from a museum = the highest-earning miner in RustChain history.

### Expected Earnings

| Metric | Value |
|--------|-------|
| Base reward | 0.12 RTC/epoch |
| With 5.0× multiplier | 0.60 RTC/epoch |
| Per day (144 epochs) | 86.4 RTC |
| Per month | ~2,592 RTC |
| Per year | ~31,104 RTC |

At $0.10/RTC: **~$3,110/year** in mining rewards.

---

## Hardware Required

| Component | Notes | Estimated Cost |
|-----------|-------|----------------|
| **ERA 1101 Console** | With magnetic drum memory (16K words) | Museum loan / Private collector |
| **Paper Tape Reader** | High-speed optical or mechanical reader | $500-2,000 |
| **Paper Tape Punch** | For output | $500-2,000 |
| **Microcontroller** | Arduino Due / Raspberry Pi for network bridge | $50-100 |
| **Custom Interface** | Connect microcontroller to paper tape pins | $200-500 |
| **Drum Monitoring** | Oscilloscope for drum timing analysis | $300-1,000 |
| **Spare Vacuum Tubes** | 2700 tubes, spares for replacement | $5,000-10,000 |
| **Power Supply** | 10-20 kW, stable | $2,000-5,000 |
| **Cooling** | Industrial HVAC for tube heat | $1,000-3,000 |

**Total estimated cost: $10,000-25,000** (excluding ERA 1101 itself, which is priceless)

---

## ERA 1101 Architecture Details

### Memory System

**Magnetic Drum:**
- 8.5" (22 cm) diameter
- 3500 RPM rotation speed
- 200 read-write heads
- 16,384 words × 24 bits = 48 KB total
- **Access time: 32 μs (minimum) to 17 ms (maximum)** — depends on rotational position
- **Critical**: Instructions must be scheduled to minimize rotational latency

### CPU Architecture

| Feature | Specification |
|---------|---------------|
| Word size | 24 bits (parallel binary) |
| Accumulator | 48 bits (double-word) |
| Q-Register | 24 bits (multiplier/quotient) |
| X-Register | 24 bits (index/operand) |
| Instructions | 24 bits (6-bit opcode, 4-bit skip, 14-bit address) |
| Add time | 96 μs |
| Multiply time | 352 μs |
| Divide time | ~1 ms |
| Negative numbers | Ones' complement |

### Instruction Set (38 Instructions)

**Arithmetic:**
```
Opcode  Mnemonic  Description
00-05   INS       Insert (y) in A (various forms: normal, complement, absolute)
06-0B   ADD       Add (y) to A (various forms)
0C      INSQ      Insert (Q) in A
0D      CLR       Clear right half of A
0E      ADDQ      Add (Q) to A
0F      TRA       Transmit (A) to Q
```

**Multiply/Divide:**
```
10      MPY       Form product (Q) * (y) in A
11      LGR       Add logical product (Q) * (y) to A
12      AND       Form logical product (Q) * (y) in A
13      DIV       Divide (A) by (y), quotient in Q, remainder in A
14      MLA       Add product (Q) * (y) to A
```

**Logical/Control:**
```
15      STO       Store right half of (A) at y
16      SHL       Shift (A) left
17      STQ       Store (Q) at y
18      SHQ       Shift (Q) left
19      RPL       Replace (y) with (A) using (Q) as operator
1A      JMP       Take (y) as next order (unconditional jump)
1B      STA       Replace (y) with (A) [address portion only]
1C      JNZ       Take (y) as next order if (A) is not zero
1D      INSX      Insert (y) in Q
1E      JN        Take (y) as next order if (A) is negative
1F      JQ        Take (y) as next order if (Q) is negative
```

**I/O and Control:**
```
20-27   Various   Print, punch, stop instructions
```

**Key Feature: Skip Field (4 bits)**
- Instructions include a "skip" value (0-15)
- Tells how many memory locations to skip to get to next instruction
- **Critical for drum optimization**: place next instruction at optimal drum position

---

## Implementation Plan

### Phase 1: Simulator Development (50 RTC)

**Goal**: Create fully functional ERA 1101 simulator

- [ ] Implement ERA 1101 CPU simulator (Python/C++)
  - 24-bit parallel arithmetic (ones' complement)
  - Magnetic drum memory model (with rotational latency simulation)
  - Paper tape I/O simulation
  - 48-bit accumulator (subtractive design)
- [ ] Create assembler
  - ERA 1101 assembly syntax
  - Symbolic label support
  - **Drum optimization**: automatic instruction placement for minimum latency
  - Paper tape format output (binary/ASCII)
- [ ] Develop debugging tools
  - Memory dump (drum visualization)
  - Single-step execution
  - Breakpoint support
  - Rotational timing analyzer

**Deliverables**:
- `era1101-sim/` — Simulator source code
- `era1101-assembler/` — Cross-assembler with drum optimization
- Documentation: Architecture reference

### Phase 2: SHA256 Implementation (75 RTC)

**Goal**: Implement SHA256 on ERA 1101

- [ ] Implement 24-bit arithmetic primitives
  - Addition/subtraction (96 μs each) — ones' complement
  - Bit rotation — 24-bit and 64-bit (multi-word)
  - XOR/AND/OR — bitwise operations
  - 64-bit operations for SHA256 constants — multi-word (3 × 24-bit)
- [ ] Implement SHA256 message scheduling
  - **Drum-optimized layout**: schedule operations to minimize rotational latency
  - Paper tape intermediate storage for constants
  - Constant table on paper tape (64 words × 32 bits → adapted to 24-bit)
- [ ] Implement SHA256 compression function
  - Optimize critical path (Σ0, Σ1, Ch, Maj)
  - Use lookup tables where possible (drum-resident)
  - Pipeline message scheduling and compression
- [ ] Test vector validation
  - NIST SHA256 test vectors
  - Incremental hashing
  - Performance measurement

**Memory Layout** (16,384 words):
```
Address Range   Usage
0x0000-0x0FFF   Boot loader and initialization (4K words)
0x1000-0x1FFF   SHA256 constants page 1 (4K words)
0x2000-0x2FFF   SHA256 constants page 2 (4K words)
0x3000-0x3007   Hash state H0-H7 (8 words)
0x3008-0x3017   Message schedule buffer (16 words active)
0x3018-0x30FF   Temporary computation buffers
0x3100-0x31FF   Network I/O buffer
0x3200-0x3FFF   Stack and variables
0x4000-0x3FFF   **Unassigned / Future expansion**
```

**Drum Scheduling Strategy**:
- Place sequential instructions at optimal drum positions
- Use skip field to account for execution time
- Example: After ADD (96 μs), next instruction should be ~3-4 positions ahead
- **Goal**: Average access time < 100 μs (vs worst-case 17 ms)

**Estimated Performance**:
- Single SHA256 hash: ~5-20 seconds (drum-optimized)
- Hash rate: 0.05-0.2 H/s
- Paper tape throughput: ~100 characters/second

### Phase 3: Network Bridge (50 RTC)

**Goal**: Build ERA 1101-to-internet network interface

- [ ] Hardware interface
  - Paper tape reader sensor (optical/mechanical)
  - Paper tape punch control
  - Microcontroller (ESP32/Arduino Due)
  - Level shifters (ERA 1101 logic levels → 3.3V/5V)
- [ ] Firmware development
  - TCP/IP stack (lwIP or similar)
  - HTTPS client (TLS 1.2/1.3)
  - Paper tape encoding/decoding
  - Error detection and correction
- [ ] Protocol design
  - ERA 1101 → Microcontroller: Mining pool request (punched tape)
  - Microcontroller → ERA 1101: Pool response (printed tape)
  - Error handling and retry logic
  - Offline mode (buffer jobs)

**Tape Protocol**:

**Request Format** (ERA 1101 punches):
```
[START][CMD][NONCE][DIFFICULTY][CHECKSUM][END]
  1      1      8         1          1       1     = 13 chars
```

**Response Format** (ERA 1101 reads):
```
[START][NONCE][HASH][CHECKSUM][END]
  1      8      32       1       1     = 43 chars
```

### Phase 4: Hardware Fingerprint & Attestation (25 RTC)

**Goal**: Implement ERA 1101-specific hardware fingerprint

- [ ] Magnetic drum characteristic extraction
  - Rotational timing signature (3500 RPM variance)
  - Head positioning delay pattern
  - Access timing variance (32 μs - 17 ms distribution)
  - Temperature-dependent drum expansion
- [ ] Vacuum tube characteristics
  - Power consumption pattern (2700 tubes)
  - Thermal signature
  - Warm-up curve
  - Tube aging fingerprint
- [ ] Attestation generation
  - Hardware signature computation
  - Timestamping
  - Node verification
- [ ] RustChain API integration
  - POST /api/miners/attest
  - Include ERA 1101-specific fields
  - Handle attestation renewal

**Fingerprint Data**:
```json
{
  "hardware_type": "era_1101",
  "year": 1950,
  "technology": "vacuum_tube",
  "memory_type": "magnetic_drum",
  "drum_timing_signature": {...},
  "rotational_variance": {...},
  "tube_power_signature": {...},
  "thermal_profile": {...}
}
```

### Phase 5: Documentation & Verification (25 RTC)

**Goal**: Complete documentation and public verification

- [ ] Video recording
  - ERA 1101 running miner (visible vacuum tubes, drum)
  - Oscilloscope showing drum timing
  - Paper tape I/O operation
  - Mining pool response
- [ ] Technical documentation
  - Architecture design document
  - Code comments (assembly + firmware)
  - User setup guide
  - Troubleshooting guide
- [ ] API verification
  - Miner appears in rustchain.org/api/miners
  - Hardware fingerprint verified
  - Rewards being earned
- [ ] Open source release
  - GitHub repository
  - MIT/Apache 2.0 license
  - Contributing guidelines
  - Issue templates

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| ERA 1101 unavailable | High | High | Use simulator for development; partner with museum |
| Drum memory failure | Medium | High | Spare drum unit; regular maintenance schedule |
| Paper tape supply | Low | Medium | Modern alternatives; 3D print sprockets |
| SHA256 too slow | Medium | Medium | Optimize drum scheduling; accept low hash rate |
| Network interface unstable | Medium | Medium | Error handling; offline batch mode |
| Power consumption | Medium | Medium | Dedicated circuit; cooling system |
| Heat management | Medium | Medium | Industrial HVAC; temperature monitoring |
| Drum timing drift | Medium | Low | Periodic recalibration; adaptive scheduling |

---

## Timeline Estimate

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| Simulator Development | 2-3 weeks | None |
| SHA256 Implementation | 3-4 weeks | Simulator complete |
| Network Bridge | 2-3 weeks | SHA256 complete |
| Hardware Fingerprint | 1-2 weeks | Network bridge complete |
| Documentation & Verification | 1-2 weeks | All phases complete |
| **Total** | **9-14 weeks** | |

---

## Resources

### Historical Documentation

- [ERA 1101 Original Manual](http://ed-thelen.org/comp-hist/ERA-1101-documents.html)
- [Unisys History Newsletter: ERA and Atlas](https://web.archive.org/web/20170913135254/https://wiki.cc.gatech.edu/folklore/index.php/Engineering_Research_Associates_and_the_Atlas_Computer_(UNIVAC_1101))
- [Computer History Museum: ERA 1101](https://www.computerhistory.org/collections/search/?q=ERA+1101)
- [Oral Histories: ERA Personnel](http://conservancy.umn.edu/handle/11299/59493)
- [Bitsavers: ERA 1101 Documentation](http://www.bitsavers.org/pdf/univac/1101/)

### Technical References

- ERA (1948). "Summary of Characteristics: Magnetic Drum Binary Computer" (Pub No. 25)
- Mathematics of Computation (1952). "Minimum Access Programming" — drum scheduling techniques
- NIST FIPS 180-4: Secure Hash Standard (SHA256 specification)

### Similar Projects

- [IBM 650 Emulator](http://www.ibm-1401.info/) — also drum memory
- [SWAC Simulator](https://github.com/Scottcjn/rustchain-bounties/tree/main/swac-miner)
- [Manchester Baby Simulator](http://www.computerhistory.org/simulation/)

---

## Claim Rules

- **Partial claims accepted** — complete any phase for its RTC amount
- **Full completion = 200 RTC total**
- **Must be real ERA 1101 hardware** (emulators don't count for full bounty)
- **Open source everything** — all code, firmware, documentation
- **Multiple people can collaborate** and split rewards
- **Museum partnerships encouraged** — ERA 1101 units exist in museums

---

## Wallet for Bounty

```
RTC4325af95d26d59c3ef025963656d22af638bb96b
```

---

## Verification Checklist

Before claiming the bounty, verify:

- [ ] Simulator passes all NIST SHA256 test vectors
- [ ] Real ERA 1101 hardware is operational and mining
- [ ] Miner appears in `rustchain.org/api/miners`
- [ ] Hardware fingerprint is verified by the network
- [ ] Video documentation is complete and public
- [ ] All source code is open-sourced on GitHub
- [ ] Technical documentation is complete

---

## Contact & Support

- **Discord**: [RustChain Discord](https://discord.gg/VqVVS2CW9Q)
- **GitHub**: [Scottcjn/Rustchain](https://github.com/Scottcjn/Rustchain)
- **Documentation**: [RustChain Docs](https://rustchain.org/docs)

**Questions?** Post in the issue comments or join the Discord.

---

## Conclusion

The ERA 1101 移植 represents the pinnacle of RustChain's Proof-of-Antiquity vision: **making history while earning crypto**. A 1950 computer — the first commercially available — mining cryptocurrency in 2026 is not just a technical achievement — it's a statement about the enduring value of computational heritage.

**76 years of computing history. One blockchain. Infinite possibilities.**

*Let's make the first commercial computer earn its keep.*

---

**Created**: 2026-03-13  
**Bounty Tier**: LEGENDARY (200 RTC / $20 USD)  
**Multiplier**: 5.0x (Maximum)  
**Wallet**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`
