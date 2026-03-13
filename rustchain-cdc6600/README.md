# RustChain CDC 6600 Miner - LEGENDARY Tier Bounty

## 🎯 Project Overview

**Port Target**: CDC 6600 Supercomputer (1964)  
**Designer**: Seymour Cray  
**Era**: First successful supercomputer  
**Bounty**: 200 RTC ($20) - LEGENDARY Tier  
**Wallet**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`

> "Every vintage computer has historical potential"  
> The CDC 6600 was the world's fastest computer from 1964 to 1969, outperforming the IBM 7030 Stretch by 3x.

---

## 📋 CDC 6600 Architecture Summary

### Central Processor (CP)
| Component | Specification |
|-----------|---------------|
| Word Length | 60 bits |
| Clock Speed | 10 MHz (100ns cycle) |
| Performance | ~3 MFLOPS, 2 MIPS |
| Integer Format | Ones' complement |
| Memory | Up to 982 KB (131000 × 60 bits) |

### Registers
| Register | Size | Purpose |
|----------|------|---------|
| X0-X7 | 60-bit | Operand registers (X0-X5 read, X6-X7 write) |
| A0-A7 | 18-bit | Address registers (A0 no side effect, A1-A5 load, A6-A7 store) |
| B0-B7 | 18-bit | Increment registers (B0 always zero) |
| P | 18-bit | Program address |

### Peripheral Processors (PPs)
- **10 PPs** based on CDC 160-A
- **4096 × 12-bit words** each
- **Barrel and slot** execution (round-robin)
- **PP0**: Overall control, OS functions
- **PP9**: System console

---

## 🏗️ Porting Strategy

### Phase 1: Minimal Viable Port (MVP)
**Goal**: Entropy collection + wallet generation only

### Phase 2: Attestation Engine
**Goal**: Hardware fingerprinting

### Phase 3: Network Layer (Optional)
**Goal**: Submit attestations via CDC 6600 network interfaces

---

## 📁 Files

| File | Description |
|------|-------------|
| `README.md` | This file - project overview |
| `IMPLEMENTATION_PLAN.md` | Detailed implementation plan |
| `CDC6600_REFERENCE.md` | Architecture quick reference |
| `miner_compass.asm` | COMPASS assembly source code |
| `cdc6600_emulator.js` | JavaScript test emulator |
| `PR_SUBMISSION.md` | PR submission template |
| `QUICK_START.md` | Quick start guide |
| `LICENSE` | Apache-2.0 License |

---

## 🚀 Quick Start

```bash
# Run JavaScript emulator
node cdc6600_emulator.js

# Output shows generated wallet and execution stats
```

See `QUICK_START.md` for detailed instructions.

---

## 🎁 Antiquity Multiplier

| System | Era | Multiplier |
|--------|-----|------------|
| **CDC 6600** | **1964** | **5.0x** ⭐ LEGENDARY |
| 8086 | 1978 | 4.0x |
| 286 | 1982 | 3.8x |
| 386 | 1985 | 3.5x |

**CDC 6600 qualifies for maximum LEGENDARY multiplier (5.0x)!**

---

## 📚 References

1. Thornton, James E. "Design of a Computer: The CDC 6600" (1970)
2. CDC 6600 Reference Manual, Control Data Corporation (1964)
3. SIMH Emulator: https://github.com/simh/simh

---

## 👤 Bounty Claim

**Wallet Address**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`  
**Tier**: LEGENDARY (200 RTC / $20)  
**Issue**: #326

---

*"The CDC 6600 was not just a computer—it was a statement. Seymour Cray proved that a small team, focused on excellence, could outperform the giants of the industry."*
