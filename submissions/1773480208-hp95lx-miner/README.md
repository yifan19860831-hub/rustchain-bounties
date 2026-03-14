# RustChain HP 95LX Miner - "Palmtop Edition" 📟

[![Bounty](https://img.shields.io/badge/Bounty-%23421-blue)](https://github.com/Scottcjn/rustchain-dos-miner)
[![Tier](https://img.shields.io/badge/Tier-LEGENDARY-gold)](https://rustchain.org)
[![Multiplier](https://img.shields.io/badge/Multiplier-4.0x-brightgreen)](https://rustchain.org)
[![Hardware](https://img.shields.io/badge/Hardware-HP%2095LX%20(1991)-orange)](https://en.wikipedia.org/wiki/HP_95LX)

**Porting RustChain miner to the HP 95LX Palmtop PC (1991) - the first DOS palmtop!**

---

## 🎯 Bounty Information

- **Task**: #421 - Port Miner to HP 95LX (1991)
- **Reward**: 200 RTC ($20) - LEGENDARY Tier
- **Wallet**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`
- **Status**: ✅ Code Complete, ⏳ Pending PR

---

## 📟 HP 95LX Specifications

| Component | Specification |
|-----------|---------------|
| **CPU** | NEC V20 @ 5.37 MHz (Intel 8088 compatible) |
| **Memory** | 512 KB RAM (F1000A) / 1 MB (F1010A) |
| **Display** | 240×128 pixels (40×16 characters) |
| **OS** | MS-DOS 3.22 (in ROM) |
| **Storage** | PCMCIA SRAM card (0.5-32 MB) |
| **Released** | April 1991 |
| **Antiquity Multiplier** | **4.0x** (LEGENDARY!) |

---

## 🚀 Quick Start

### Test with Python Simulator (No Hardware Required!)

```bash
# Demo mode (fast epochs)
python hp95lx_simulator.py --demo

# Full simulation with your wallet
python hp95lx_simulator.py --wallet RTC4325af95d26d59c3ef025963656d22af638bb96b

# Submit attestation
python submit_attest.py --file ATTEST.TXT --wallet RTC4325af95d26d59c3ef025963656d22af638bb96b
```

### Compile for Real HP 95LX

```bash
# Turbo C 2.0 (on DOS or DOSBox)
tcc -ml -O -DHP95LX -DREAL_MODE rustchain_hp95lx.c

# OpenWatcom (cross-compile from Windows/Linux)
wcl -0 -ox -DHP95LX rustchain_hp95lx.c
```

See [BUILD.TXT](BUILD.TXT) for detailed instructions.

---

## 📁 Files

| File | Description |
|------|-------------|
| [`rustchain_hp95lx.c`](rustchain_hp95lx.c) | Main miner source (Turbo C) |
| [`hp95lx_simulator.py`](hp95lx_simulator.py) | Python simulator ✓ Tested |
| [`submit_attest.py`](submit_attest.py) | Attestation submitter |
| [`MINER.CFG`](MINER.CFG) | Configuration template |
| [`README_HP95LX.md`](README_HP95LX.md) | Complete user guide |
| [`BUILD.TXT`](BUILD.TXT) | Build instructions |
| [`PR_DESCRIPTION.md`](PR_DESCRIPTION.md) | Pull request template |
| [`SUMMARY.md`](SUMMARY.md) | Project summary |

---

## ✨ Features

- ✅ **512 KB Optimized**: Runs on HP 95LX (original requires 640 KB)
- ✅ **Turbo C Compatible**: 16-bit real mode, no DJGPP required
- ✅ **Hardware Detection**: Identifies HP 95LX specifically
- ✅ **Offline Mode**: Saves attestations to ATTEST.TXT
- ✅ **Python Simulator**: Test without vintage hardware
- ✅ **4.0x Multiplier**: LEGENDARY tier antiquity bonus!

---

## 🎮 Usage on HP 95LX

```
C:\RUSTCHN> MINER

========================================
 RUSTCHAIN HP 95LX MINER v0.1.0
 Palmtop Edition (1991)
========================================

Wallet: RTCxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Miner ID: HP95LX-XXXXXXXX

Hardware: HP 95LX (NEC V20)
Multiplier: 4.0x (LEGENDARY!)
Memory: 512 KB

Mode: OFFLINE (save to ATTEST.TXT)

[S]tatus [Q]uit
```

---

## 📊 Expected Performance

| Metric | HP 95LX | Notes |
|--------|---------|-------|
| Epoch time | ~2-3 sec | Attestation generation |
| Power consumption | ~2W | 2× AA batteries |
| Battery life | ~20 hours | Continuous mining |
| RTC/day (estimated) | ~8-12 RTC | With 4.0x multiplier |

---

## 🔧 Technical Details

### Memory Optimization

The original DOS miner required 640 KB. HP 95LX only has 512 KB!

**Solutions**:
- Reduced timer samples: 32 → 16
- 16-bit real mode (no DPMI)
- Minimal buffers
- No extended memory

### Attestation Format

```json
{
  "wallet": "RTC...",
  "miner_id": "HP95LX-XXXXXXXX",
  "hardware": "HP 95LX",
  "cpu": "NEC V20",
  "mhz": 5.37,
  "memory_kb": 512,
  "timestamp": 1234567890,
  "antiquity_multiplier": 4.0,
  "tier": "LEGENDARY",
  "hash": "..."
}
```

---

## 📚 Documentation

- **[README_HP95LX.md](README_HP95LX.md)**: Complete user guide
- **[BUILD.TXT](BUILD.TXT)**: Compilation and file transfer
- **[SUMMARY.md](SUMMARY.md)**: Project summary

---

## 🏆 Historical Significance

The HP 95LX was:
- **First DOS palmtop** (April 1991)
- **HP + Lotus collaboration** (1-2-3 built-in)
- **400,000+ units sold**
- **Professional tool** until early 2000s
- **Cult classic** among retro computing enthusiasts

Mining RustChain on a 34-year-old palmtop demonstrates the true spirit of **"Proof-of-Antiquity"**!

---

## 📝 License

- Apache 2.0 (consistent with original DOS miner)
- HP 95LX optimizations: MIT

---

## 🙏 Acknowledgments

- Original DOS Miner: [@Scottcjn](https://github.com/Scottcjn/rustchain-dos-miner)
- RustChain: [Elyan Labs](https://rustchain.org)
- HP 95LX Community: [hp95lx.com](https://www.hp95lx.com/)

---

## 🔗 Links

- **Bounty Tracker**: [RustChain Bounties](https://rustchain.org/bounties)
- **Original DOS Miner**: [github.com/Scottcjn/rustchain-dos-miner](https://github.com/Scottcjn/rustchain-dos-miner)
- **HP 95LX Wikipedia**: [en.wikipedia.org/wiki/HP_95LX](https://en.wikipedia.org/wiki/HP_95LX)

---

**"Every vintage computer has historical potential"**

_HP 95LX - The First Palmtop PC, Now Mining RustChain!_ 📟⛏️
