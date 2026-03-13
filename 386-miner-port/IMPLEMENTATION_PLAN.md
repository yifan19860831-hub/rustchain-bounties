# RustChain 386 Miner - Implementation Plan

## Project Overview

**Goal**: Port RustChain miner to Intel 386 architecture to claim 150 RTC bounty + 4.0x antiquity multiplier

**Issue**: [#435](https://github.com/Scottcjn/rustchain-bounties/issues/435)

**Wallet**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`

## Repository Structure

```
rustchain-386-miner/
├── README.md                    # Project overview and quick start
├── TECHNICAL_ANALYSIS.md        # Detailed technical analysis (this file)
├── IMPLEMENTATION_PLAN.md       # This file
├── BUILD.md                     # Build instructions
├── HARDWARE_GUIDE.md            # Hardware setup guide
├── src/
│   ├── miner.c                  # Main miner source (C implementation)
│   ├── miner.lua                # Alternative Lua implementation
│   ├── entropy.c                # Entropy collection for 386
│   ├── fingerprint.c            # 386-specific fingerprinting
│   ├── network.c                # HTTP client for attestation
│   └── wallet.c                 # Wallet generation/management
├── include/
│   ├── miner.h
│   ├── entropy.h
│   ├── fingerprint.h
│   ├── network.h
│   └── wallet.h
├── scripts/
│   ├── build-cross.sh           # Cross-compilation script
│   ├── build-native.sh          # Native compilation script
│   └── flash-cf.sh              # Flash CF card script
├── configs/
│   ├── slackware-3.0/           # Slackware 3.0 configuration
│   └── kernel-2.0.36.config     # Kernel config for 386
├── attestations/
│   └── sample-attestation.json  # Sample attestation payload
└── docs/
    ├── troubleshooting.md
    ├── performance.md
    └── photos/                  # Hardware photos
```

## Phase 1: Hardware Acquisition (Week 1-2)

### Required Components

| Component | Specification | Qty | Est. Cost | Priority |
|-----------|---------------|-----|-----------|----------|
| 386 Motherboard | 386DX or 386SX, AT form factor | 1 | $50-80 | 🔴 Critical |
| CPU | 386DX-25/33/40 or 386SX-16/20/25 | 1 | (included) | 🔴 Critical |
| RAM | 30-pin SIMM, 1-4MB modules | 2-4 | $20-40 | 🔴 Critical |
| Video Card | VGA or SVGA, ISA | 1 | $15-25 | 🔴 Critical |
| Network Card | NE2000 compatible, ISA | 1 | $15-25 | 🔴 Critical |
| Storage | CF-to-IDE adapter + 128MB+ CF | 1 | $15-20 | 🔴 Critical |
| Power Supply | AT power supply, 200W+ | 1 | $30-40 | 🔴 Critical |
| Case | AT desktop or tower | 1 | $20-30 | 🟡 Optional |
| Keyboard | AT or PS/2 (with adapter) | 1 | $10-20 | 🔴 Critical |
| Floppy Drive | 3.5" 1.44MB (optional) | 1 | $15-25 | 🟡 Optional |

**Total Budget**: $190-305 USD

### Sourcing Strategy

1. **eBay**: Search "386 computer", "386 motherboard", "vintage PC"
2. **Local**: Computer swap meets, ham radio flea markets
3. **Forums**: VOGONS, VCFed, Reddit r/vintagecomputing

### Acceptance Criteria

- [ ] System boots successfully
- [ ] All RAM recognized (8+ MB preferred)
- [ ] NE2000 NIC detected and functional
- [ ] CF card recognized as IDE drive
- [ ] System stable for 24+ hours

## Phase 2: Operating System Setup (Week 2-3)

### Option A: Slackware 3.0 (RECOMMENDED)

**Download**: http://www.slackware.com/getslack/

**Installation Steps**:

```bash
# 1. Download Slackware 3.0 ISOs
wget http://www.slackware.com/getslack/slackware-3.0/install.iso
wget http://www.slackware.com/getslack/slackware-3.0/disks1.iso
# ... (all disk images)

# 2. Create bootable installation media
# Option: Use QEMU to install to CF card, then boot on real hardware
qemu-system-i386 -hda cf-card.img -cdrom install.iso -boot d -m 16

# 3. Partition CF card
fdisk /dev/hda
# Create: /dev/hda1 = 128MB, type 83 (Linux)

# 4. Format and install
mke2fs /dev/hda1
mount /dev/hda1 /mnt
# Follow Slackware installation procedure

# 5. Install packages (minimal)
- a (base system)
- ap (applications)
- d (development - GCC, make, etc.)
- e (GNU Emacs - optional)
- n (networking)
- t (TeX - optional, skip to save space)
- tc (TCL - optional)
- y (LILO - bootloader)
```

**Kernel Configuration**:

```bash
cd /usr/src/linux
make config

# Critical options:
CONFIG_M386=y
CONFIG_MATOM=n  # Disable modern CPU optimizations
CONFIG_BLK_DEV_IDE=y
CONFIG_NET=y
CONFIG_INET=y
CONFIG_NE2000=y
CONFIG_SERIAL=y
```

**Post-Installation**:

```bash
# Configure network
echo "192.168.1.100" > /etc/HOSTNAME
echo "127.0.0.1 localhost" > /etc/hosts
# Edit /etc/rc.d/rc.inet1.conf

# Test network
ping 8.8.8.8

# Install additional tools
# (may need to compile from source on modern system, transfer via FTP)
```

### Option B: Cross-Development Setup

**Rationale**: Compile on modern system, deploy to 386

**Setup Cross-Compiler**:

```bash
# On modern Linux (Ubuntu/Debian)
sudo apt-get install gcc-i686-linux-gnu g++-i686-linux-gnu

# Or build i386-elf toolchain
export TARGET=i386-elf
export PREFIX=/opt/cross
export PATH=$PREFIX/bin:$PATH

# Build binutils
git clone git://sourceware.org/git/binutils-gdb.git binutils
cd binutils
mkdir build && cd build
../configure --target=$TARGET --prefix=$PREFIX --disable-nls
make && make install

# Build GCC
git clone git://gcc.gnu.org/git/gcc.git
cd gcc
mkdir build && cd build
../configure --target=$TARGET --prefix=$PREFIX \
  --disable-nls --enable-languages=c --without-headers
make all-gcc && make install-gcc
```

**Compile Miner**:

```bash
i686-linux-gnu-gcc -m386 -march=i386 -O2 \
  -o miner-386 miner.c entropy.c fingerprint.c network.c wallet.c
```

## Phase 3: Miner Implementation (Week 3-4)

### Core Components

#### 1. Entropy Collection (`entropy.c`)

```c
// Key functions to implement:
void collect_bios_info(DosEntropy *entropy);
void detect_cpu(CPUInfo *cpu);
void collect_memory_info(MemInfo *mem);
void collect_timer_entropy(TimerSamples *samples);
void collect_rtc(RTCData *rtc);

// 386-specific additions:
void measure_isa_bus_timing(void);
void measure_memory_timing(void);
int detect_fpu_presence(void);
unsigned long measure_clock_drift(void);
```

#### 2. Fingerprinting (`fingerprint.c`)

```c
typedef struct {
    char arch[16];        // "i386"
    char cpu_vendor[48];  // "GenuineIntel" or "Unknown-386"
    unsigned long cpu_sig; // 0x386
    int has_fpu;          // 0 (no FPU = authentic 386)
    unsigned long isa_timing;  // ISA bus access time (cycles)
    unsigned long mem_timing;  // Memory access time (cycles/MB)
    unsigned long clock_drift; // Clock drift over 10 seconds
    char bios_date[16];   // BIOS date string
} Fingerprint386;

int generate_fingerprint(Fingerprint386 *fp);
int validate_fingerprint(const Fingerprint386 *fp);
```

#### 3. Network Client (`network.c`)

```c
// Simple HTTP client (no TLS needed)
int http_post(const char *host, int port, 
              const char *path, const char *data,
              char *response, int resp_size);

// Attestation submission
int submit_attestation(const char *wallet_id,
                       const Fingerprint386 *fp,
                       const char *entropy_hash);
```

#### 4. Wallet Management (`wallet.c`)

```c
typedef struct {
    char wallet_id[48];    // RTC + 40 hex chars
    char miner_id[32];     // DOS-XXXXXXXX
    unsigned long created; // Unix timestamp
    int initialized;
} Wallet386;

int wallet_load(Wallet386 *wallet, const char *path);
int wallet_save(const Wallet386 *wallet, const char *path);
int wallet_generate(Wallet386 *wallet, const DosEntropy *entropy);
```

#### 5. Main Miner (`miner.c`)

```c
int main(int argc, char *argv[]) {
    // 1. Print banner
    print_banner();
    
    // 2. Collect entropy
    DosEntropy entropy;
    collect_all_entropy(&entropy);
    
    // 3. Load/generate wallet
    Wallet386 wallet;
    if (!wallet_load(&wallet, "wallet.dat")) {
        wallet_generate(&wallet, &entropy);
        wallet_save(&wallet, "wallet.dat");
    }
    
    // 4. Generate fingerprint
    Fingerprint386 fp;
    generate_fingerprint(&fp);
    
    // 5. Initialize network
    if (!network_init()) {
        printf("Offline mode\n");
    }
    
    // 6. Mining loop
    while (1) {
        if (time_to_attest()) {
            refresh_entropy(&entropy);
            submit_attestation(wallet.wallet_id, &fp, entropy.hash);
        }
        sleep(1);
    }
    
    return 0;
}
```

### Build Scripts

#### Cross-Compilation (`scripts/build-cross.sh`)

```bash
#!/bin/bash
set -e

export CC=i686-linux-gnu-gcc
export CFLAGS="-m386 -march=i386 -O2 -Wall"

cd src

$CC $CFLAGS -c entropy.c -o entropy.o
$CC $CFLAGS -c fingerprint.c -o fingerprint.o
$CC $CFLAGS -c network.c -o network.o
$CC $CFLAGS -c wallet.c -o wallet.o
$CC $CFLAGS -c miner.c -o miner.o

$CC -o rustchain-386-miner \
    miner.o entropy.o fingerprint.o network.o wallet.o \
    -lm

echo "Build complete: rustchain-386-miner"
```

#### Native Compilation (`scripts/build-native.sh`)

```bash
#!/bin/bash
# Run this ON the 386 system

export CFLAGS="-m386 -O2 -Wall"

gcc $CFLAGS -o rustchain-386-miner \
    miner.c entropy.c fingerprint.c network.c wallet.c \
    -lm

echo "Native build complete"
```

## Phase 4: Testing & Validation (Week 4-5)

### Test Checklist

- [ ] **Boot Test**: System boots Slackware 3.0 successfully
- [ ] **Network Test**: Can ping external hosts
- [ ] **Compile Test**: Miner compiles without errors
- [ ] **Entropy Test**: Entropy collection completes
- [ ] **Fingerprint Test**: Fingerprint generated correctly
- [ ] **Wallet Test**: Wallet saved/loaded successfully
- [ ] **Attestation Test**: HTTP POST succeeds
- [ ] **Stability Test**: Runs for 24+ hours without crash
- [ ] **Multiplier Test**: Shows 4.0x in rustchain.org dashboard

### Debugging Tools

```bash
# Serial console (if available)
screen /dev/ttyS0 9600

# Network debugging
tcpdump -i eth0  # If available
netstat -an

# Performance monitoring
top  # If available
free
ps aux

# Log files
tail -f /var/log/messages
dmesg | tail -50
```

### Common Issues & Solutions

| Issue | Symptom | Solution |
|-------|---------|----------|
| Kernel panic on boot | "Kernel panic - not syncing" | Check kernel config, ensure 386 support |
| NIC not detected | "eth0: device not found" | Check IRQ/conflict, try different slot |
| CF card not detected | "hda: probe failed" | Check IDE cable, jumper settings |
| Out of memory | "Cannot allocate memory" | Reduce kernel footprint, add RAM |
| Network unreachable | "Network unreachable" | Check gateway, routing table |
| Attestation fails | HTTP 400/500 | Check JSON format, wallet ID |

## Phase 5: Documentation & Submission (Week 5-6)

### Required Documentation

1. **README.md**: Project overview, quick start
2. **BUILD.md**: Detailed build instructions
3. **HARDWARE_GUIDE.md**: Hardware setup guide
4. **TROUBLESHOOTING.md**: Common issues and solutions
5. **PHOTOS/**: Photos of running system

### GitHub PR Checklist

- [ ] Fork rustchain-bounties repository
- [ ] Create branch: `feature/386-miner-port`
- [ ] Add all source code
- [ ] Add documentation
- [ ] Add photos/screenshots
- [ ] Create PR referencing issue #435
- [ ] Add wallet address in PR description
- [ ] Respond to any review comments

### PR Template

```markdown
## 386 Miner Port - Bounty Claim

**Bounty**: #435 - Port Miner to Intel 386
**Wallet**: RTC4325af95d26d59c3ef025963656d22af638bb96b

### What's Included

- ✅ Complete miner implementation for Intel 386
- ✅ Runs on Slackware 3.0 (true 386 Linux)
- ✅ 386-specific fingerprinting (no-FPU, ISA timing, clock drift)
- ✅ HTTP attestation (no TLS required)
- ✅ Cross-compilation support
- ✅ Complete documentation

### Hardware Used

- 386DX-40 motherboard
- 16 MB RAM (30-pin SIMM)
- NE2000 ISA Ethernet
- CF-to-IDE adapter (128 MB)
- VGA graphics

### Proof

- Photos: See `docs/photos/`
- Attestation: Visible at https://rustchain.org/api/miners
- Architecture: Reported as "i386" with 4.0x multiplier

### Build Instructions

See BUILD.md for detailed instructions.

Quick start:
```bash
# Cross-compile
./scripts/build-cross.sh

# Or compile natively on 386
./scripts/build-native.sh
```

### Testing

Tested on real 386 hardware (not emulator).
Stable operation for 48+ hours.

---

**Multiplier**: 4.0x (maximum tier)
**Estimated Earnings**: 4x base rate
```

## Timeline Summary

| Week | Phase | Deliverables |
|------|-------|--------------|
| 1-2 | Hardware | 386 system acquired and tested |
| 2-3 | OS Setup | Slackware 3.0 installed and configured |
| 3-4 | Development | Miner code complete and compiling |
| 4-5 | Testing | All tests passing, stable operation |
| 5-6 | Documentation | README, photos, PR submitted |

## Success Metrics

- [x] Technical analysis complete
- [ ] Hardware acquired and operational
- [ ] OS installed and networked
- [ ] Miner compiles and runs
- [ ] Attestation submitted successfully
- [ ] 4.0x multiplier confirmed
- [ ] PR merged, bounty claimed

## Budget & ROI

**Investment**: ~$250 USD (hardware)
**Bounty**: 150 RTC
**Ongoing**: 4.0x mining multiplier

**Break-even**: Depends on RTC price, but bounty alone may cover hardware cost.
**Long-term**: 4.0x multiplier provides ongoing passive income.

---

**Status**: Ready for Implementation
**Next Action**: Order hardware from eBay
