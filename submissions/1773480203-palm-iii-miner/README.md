# RustChain Palm III Miner - "DragonBall Edition" 🦎

**For Palm III (1998) - Motorola DragonBall EZ @ 16 MHz**

*"The smallest blockchain miner in the world... in 1998"*

## 🏆 Bounty Claim

**Wallet Address:** `RTC4325af95d26d59c3ef025963656d22af638bb96b`

**Bounty Tier:** LEGENDARY (200 RTC / $20)

## 📋 Specifications

### Target Hardware
| Component | Specification |
|-----------|---------------|
| **CPU** | Motorola DragonBall MC68328 @ 16 MHz |
| **Architecture** | Motorola 68000 (32-bit) |
| **RAM** | 2 MB EDO SDRAM |
| **ROM** | 2 MB Flash ROM |
| **Display** | 160×160 px, 4-bit grayscale |
| **OS** | Palm OS 3.0-4.1 |
| **Connectivity** | IrDA, RS-232 (HotSync) |
| **Power** | 2× AAA batteries |

### Antiquity Multiplier: **3.5×** 🎯

Palm III (1998) qualifies for the 3.5× antiquity multiplier as a late-90s embedded device!

## 🏗️ Architecture

### Design Philosophy
Given the extreme constraints (2 MB RAM, 16 MHz CPU), this miner uses:
- **Minimalist approach**: Only essential hashing and attestation
- **Event-driven**: Uses Palm OS event loop, no busy-waiting
- **Storage-efficient**: Wallet stored in Palm DB format
- **Offline-first**: Attestations saved locally, synced via HotSync

### Components
```
palm-iii-miner/
├── src/
│   ├── MinerMain.c       # Main application entry
│   ├── MinerUI.c         # User interface (160×160)
│   ├── Entropy68k.c      # DragonBall entropy collection
│   ├── HashCore.c        # Simplified SHA-256
│   └── AttestDB.c        # Palm DB storage
├── include/
│   └── Miner.h           # Common headers
├── simulator/
│   └── palm_miner.py     # Python simulator
├── resources/
│   └── Miner.rcp         # Palm resources (icons, forms)
├── Makefile              # CodeWarrior build
└── docs/
    ├── BUILD.md          # Build instructions
    └── PALM_OS.md        # Palm OS technical notes
```

## 🔨 Build Requirements

### Official Build (Palm OS)
- **Metrowerks CodeWarrior for Palm OS**
- **Palm OS SDK 3.5**
- **Pilot-Grammer** or **PilRC** resource compiler

### Alternative (Cross-compile)
- **m68k-palmos-gcc** (GNU toolchain)
- **prc-tools**

## 📱 Installation

1. Build `Miner.prc`
2. HotSync to Palm III
3. Launch "RC Miner" from app launcher
4. First run generates wallet (save it!)

## 🎮 Usage

### Main Screen
```
┌────────────────────┐
│  RustChain Miner   │
│  Palm III Edition  │
├────────────────────┤
│ Wallet: abc123...  │
│ Attestations: 0    │
│ Last: --           │
│                    │
│ [Mine] [Status]    │
│ [Wallet] [Exit]    │
└────────────────────┘
```

### Buttons
- **Mine**: Start mining (background)
- **Status**: Show statistics
- **Wallet**: Display/backup wallet
- **Exit**: Quit miner

## 🔧 Technical Details

### Entropy Sources (DragonBall)
1. **RTC registers** - Motorolla DragonBall real-time clock
2. **Timer ticks** - System timer jitter
3. **Touchscreen** - User input timing
4. **RAM pattern** - Power-on RAM state

### Memory Layout
```
Heap:     1.5 MB (dynamic)
Stack:    64 KB (max)
Code:     256 KB
Resources: 128 KB
Free:     ~1 MB for attestations
```

### Power Management
- Uses Palm OS sleep/wake hooks
- Mining pauses during deep sleep
- Resumes on wake or HotSync

## 🖥️ Python Simulator

For testing without hardware:

```bash
cd simulator/
python palm_miner.py
```

Simulates:
- DragonBall entropy collection
- Palm OS event loop
- 160×160 display (text mode)
- Attestation storage

## 📊 Performance Estimates

| Metric | Estimate |
|--------|----------|
| Hash rate | ~50 H/s (very rough) |
| Power draw | ~0.3 W (2× AAA lasts weeks) |
| Memory usage | ~400 KB |
| Attestation size | ~256 bytes |

**Note:** This is a **proof-of-concept** for the bounty, not a production miner!

## 🏛️ Historical Context

The Palm III was revolutionary in 1998:
- First Palm with IR file sharing
- First with Flash ROM (upgradable OS!)
- Sold for $400 (~$750 today)
- Made famous by early adopters and tech enthusiasts

Porting a blockchain miner to this device demonstrates:
1. RustChain's flexibility
2. Proof-of-Antiquity for embedded systems
3. The enduring appeal of vintage computing

## 📜 License

Part of RustChain - Elyan Labs 2025

Palm OS SDK and related tools © Palm Computing/3Com

## 🙏 Acknowledgments

- Palm Computing for creating this legendary device
- RustChain community for the bounty program
- Vintage computing enthusiasts keeping these devices alive

---

**Wallet for Bounty:** `RTC4325af95d26d59c3ef025963656d22af638bb96b`

*"Every vintage computer has historical potential"* 🦎
