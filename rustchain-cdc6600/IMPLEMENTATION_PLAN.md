# CDC 6600 Miner Implementation Plan

## 📋 Task: Issue #326 - Port Miner to CDC 6600 (1964)

**Bounty**: 200 RTC ($20) - LEGENDARY Tier  
**Wallet**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`

---

## 🎯 Objectives

1. Create minimal viable CDC 6600 miner in COMPASS assembly
2. Implement entropy collection using hardware timing
3. Generate wallet keys (120-bit: two 60-bit words)
4. Create attestation proof format
5. Support offline operation
6. Document the port with historical context

---

## 🏗️ CDC 6600 Architecture

### Key Specifications
| Property | Value |
|----------|-------|
| Word Size | 60 bits |
| Clock | 10 MHz (100ns cycle) |
| Memory | Up to 982 KB |
| Performance | ~3 MFLOPS |
| Registers | 8×X (60-bit), 8×A (18-bit), 8×B (18-bit) |
| PPs | 10 peripheral processors |
| Integer Format | Ones' complement |

### Memory Map
```
0x0000-0x00FF:   Bootstrap
0x0100-0x0FFF:   Code
0x1000-0x1FFF:   Wallet
0x2000-0x3FFF:   Attestations
0x4000-0x7FFF:   Working
0x8000-0xFFFF:   ECS Extended
```

---

## 📝 Implementation Phases

### Phase 1: Core Infrastructure (Days 1-3)
- [x] CDC 6600 architecture research
- [x] COMPASS instruction set study
- [ ] SIMH emulator setup
- [ ] Test harness creation

### Phase 2: Entropy Collection (Days 4-7)
- [ ] PP clock access
- [ ] Timing variance collection
- [ ] Von Neumann debiasing
- [ ] Statistical validation

### Phase 3: Wallet Generation (Days 8-10)
- [ ] 60-bit FP multiplication
- [ ] Key derivation function
- [ ] Wallet storage
- [ ] Display formatting

### Phase 4: Attestation Engine (Days 11-14)
- [ ] Hardware fingerprinting
- [ ] Attestation format (5 words)
- [ ] Epoch timer (10 min)
- [ ] Batch submission

### Phase 5: Output & Integration (Days 15-18)
- [ ] Punch card format
- [ ] Console output (PP9)
- [ ] Modern bridge (optional)
- [ ] Full loop testing

### Phase 6: Documentation & PR (Days 19-21)
- [x] README
- [x] Implementation plan
- [x] Architecture reference
- [ ] PR submission
- [ ] Bounty claim

---

## 🔧 Technical Details

### Register Usage
```
X0: Zero constant
X1: Entropy accumulator
X2: Hash state
X3: Temporary
X4: Wallet part 1
X5: Wallet part 2
X6: Output
X7: Return value
```

### Entropy Algorithm
```
1. Read PP clock
2. Execute timing-sensitive sequence
3. Capture timing variance
4. XOR into accumulator
5. Repeat 100+ times
6. Debias (von Neumann)
```

### Wallet Generation
```
wallet1 = FPU_multiply(entropy, CONST1)
wallet2 = FPU_multiply(entropy, CONST2)
```

---

## 🧪 Testing

- JavaScript emulator for development
- SIMH CDC 6600 for full testing
- Entropy quality: Chi-square, bit frequency
- Wallet uniqueness: Collision testing

---

## 📚 References

1. Thornton, J.E. "Design of a Computer: The CDC 6600" (1970)
2. CDC 6600 Reference Manual (1964)
3. SIMH Emulator: https://github.com/simh/simh

---

## 🎁 Bounty Claim

**Issue**: #326  
**Wallet**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`  
**Tier**: LEGENDARY (200 RTC / $20)  
**Multiplier**: 5.0x (pre-1970 supercomputer)

---

*Version: 1.0 | Last Updated: 2026-03-13*
