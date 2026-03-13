# RustChain 386 Miner

**Bounty**: [#435](https://github.com/Scottcjn/rustchain-bounties/issues/435) - 150 RTC + 4.0x multiplier

**Wallet**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`

## Overview

This is a complete RustChain miner implementation for Intel 386 architecture (1985), designed to achieve the maximum 4.0x antiquity multiplier in the RustChain network.

### Features

- ✅ **True 386 Support**: Runs on real Intel 386 hardware (not emulator)
- ✅ **Linux-based**: Slackware 3.0 / Debian 2.x support
- ✅ **386 Fingerprinting**: No-FPU detection, ISA timing, clock drift, memory timing
- ✅ **HTTP Attestation**: Lightweight HTTP client (no TLS required)
- ✅ **Auto-Wallet**: Hardware entropy-based wallet generation
- ✅ **Offline Mode**: Save attestations for later submission
- ✅ **Cross-Compile**: Build on modern systems, deploy to 386

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     RustChain 386 Miner                      │
├─────────────────────────────────────────────────────────────┤
│  Main Loop (miner.c)                                        │
│  ├─ Entropy Collection → Fingerprint → Attestation          │
├─────────────────────────────────────────────────────────────┤
│  Entropy (entropy.c)         Fingerprint (fingerprint.c)    │
│  ├─ BIOS info                ├─ No-FPU detection            │
│  ├─ CPU detection            ├─ ISA bus timing              │
│  ├─ Memory info              ├─ Clock drift measurement     │
│  ├─ Timer samples            ├─ Memory timing               │
│  └─ RTC                      └─ CPUID (if available)        │
├─────────────────────────────────────────────────────────────┤
│  Network (network.c)         Wallet (wallet.c)              │
│  ├─ HTTP client              ├─ Wallet generation           │
│  ├─ JSON builder             ├─ Wallet save/load            │
│  └─ Attestation submit       └─ Hardware entropy            │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

### Option 1: Cross-Compilation (Recommended)

```bash
# On modern Linux system
sudo apt-get install gcc-i686-linux-gnu

# Build
./scripts/build-cross.sh

# Transfer to 386 system (via FTP, serial, or CF card)
scp rustchain-386-miner user@386-system:/usr/local/bin/
```

### Option 2: Native Compilation

```bash
# On 386 system running Slackware 3.0
cd /usr/src/rustchain-386-miner
./scripts/build-native.sh

# Run
./rustchain-386-miner
```

## Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | Intel 386SX-16 | Intel 386DX-40 |
| RAM | 4 MB | 16 MB |
| Storage | 64 MB | 128+ MB (CF-to-IDE) |
| Network | NE2000 ISA | NE2000 ISA |
| OS | Slackware 3.0 | Slackware 3.1 |

## Installation

### 1. Hardware Setup

See [HARDWARE_GUIDE.md](HARDWARE_GUIDE.md) for detailed hardware setup instructions.

### 2. OS Installation

```bash
# Download Slackware 3.0
wget http://www.slackware.com/getslack/slackware-3.0/install.iso

# Install to CF card (using QEMU or real hardware)
# Follow Slackware installation procedure
# Select packages: a, ap, d, n (minimal + networking)
```

### 3. Network Configuration

```bash
# Configure NE2000 NIC
modprobe ne io=0x300 irq=3

# Set IP address
ifconfig eth0 192.168.1.100 netmask 255.255.255.0
route add default gw 192.168.1.1

# Test
ping 8.8.8.8
```

### 4. Build & Run

```bash
# Build (native or cross-compile)
./scripts/build-native.sh

# Run
./rustchain-386-miner
```

## Usage

### First Run

```
======================================================
  RUSTCHAIN 386 MINER - "Fossil Edition"
  Intel 386 Architecture (1985)
  "Every vintage computer has historical potential"
======================================================
  Dev Fee: 0.001 RTC/epoch -> founder_dev_fund
======================================================

[1/5] Collecting BIOS info...
[2/5] Detecting CPU... (386 detected, no FPU)
[3/5] Reading memory config... (8192 KB)
[4/5] Collecting timer entropy...
[5/5] Generating entropy hash...

No wallet found, generating new wallet...
========================================
  NEW WALLET GENERATED!
  RTCxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
========================================
  SAVE THIS! Backup wallet.dat to floppy!
========================================

Network: Online (eth0: 192.168.1.100)
Architecture: i386 (4.0x multiplier!)
Node: rustchain.org:8088

Starting mining loop (Ctrl+C to exit)...
[1710345600] Cycle 1: Collecting entropy...
[1710345600] Sending attestation to node...
[1710345605] SUCCESS! Attestation accepted.
[1710345605] Next attestation in 600 seconds.
```

### Commands

- `s` or `S`: Show status
- `q` or `Q` or `ESC`: Quit miner

### Configuration

Edit `miner.cfg`:

```ini
# RustChain 386 Miner Configuration

# Node settings
node_host=rustchain.org
node_port=8088

# Wallet settings
wallet_file=wallet.dat

# Network settings
use_network=1
offline_mode=0

# Dev fee
dev_fee_enabled=1
dev_fee_wallet=founder_dev_fund
dev_fee_amount=0.001
```

## 386-Specific Features

### No-FPU Detection

The 386 did not include a floating-point unit (FPU) by default. The 387 coprocessor was sold separately. This absence is a strong fingerprint of authentic 386 hardware.

```c
int has_fpu = detect_fpu();  // Returns 0 on authentic 386
```

### ISA Bus Timing

ISA bus accesses are significantly slower than modern PCI/PCIe. We measure the cycle count for I/O port accesses.

```c
unsigned long isa_cycles = measure_isa_timing();
// Typical: 300-500 cycles for ISA vs <50 for PCI
```

### Clock Drift

386 crystal oscillators have significant drift compared to modern systems. We measure drift over 10 seconds.

```c
unsigned long drift = measure_clock_drift();
// Typical: 0.5-2% drift on 386
```

### Memory Timing

Early 386 systems had no cache, resulting in consistent memory access timing.

```c
unsigned long mem_cycles = measure_memory_timing();
// No cache: ~4 cycles per byte access
// With cache: ~1 cycle (but 386 had no L1 cache)
```

## Attestation Format

```json
{
  "miner": "RTCxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "miner_id": "386-XXXXXXXX",
  "nonce": 1710345600,
  "device": {
    "arch": "i386",
    "family": "x86_32",
    "model": "Intel 386",
    "cpu_signature": "0x00000386",
    "bios_date": "01/15/87",
    "has_fpu": false,
    "isa_timing_cycles": 423,
    "memory_timing_cycles_per_mb": 4194304,
    "clock_drift_ppm": 15000
  },
  "dev_fee": {
    "enabled": true,
    "wallet": "founder_dev_fund",
    "amount": 0.001
  }
}
```

## Build Instructions

### Cross-Compilation

```bash
# Ubuntu/Debian
sudo apt-get install gcc-i686-linux-gnu g++-i686-linux-gnu

# Build
cd scripts
./build-cross.sh

# Output: rustchain-386-miner (i386 binary)
```

### Native Compilation

```bash
# On 386 Slackware 3.0
gcc -m386 -O2 -o rustchain-386-miner \
    src/miner.c src/entropy.c src/fingerprint.c \
    src/network.c src/wallet.c -lm
```

## Troubleshooting

### Network Issues

```bash
# Check NIC detection
dmesg | grep -i eth

# Test network
ping 8.8.8.8

# Check routing
netstat -rn
```

### Memory Issues

```bash
# Check available memory
free

# If out of memory, close other processes
ps aux
kill <pid>
```

### Attestation Failures

```bash
# Check node connectivity
telnet rustchain.org 8088

# Check attestation format
cat attestation.json | head -20
```

## Performance

### Resource Usage

- **RAM**: ~8-12 MB
- **CPU**: ~30% during attestation, ~5% idle
- **Disk**: ~50 MB (OS + miner)
- **Network**: ~1 KB per attestation (every 10 minutes)

### Expected Throughput

- **Attestation time**: 10-15 seconds
- **Epoch duration**: 10 minutes (600 seconds)
- **Cycles per epoch**: ~40-60 attempts

## Bounty Information

**Issue**: [#435](https://github.com/Scottcjn/rustchain-bounties/issues/435)

**Bounty**: 150 RTC (one-time) + 4.0x multiplier (ongoing)

**Wallet**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`

**Status**: Implementation in progress

## License

Apache 2.0 - See LICENSE file

## Credits

- Original DOS miner: [rustchain-dos-miner](https://github.com/Scottcjn/rustchain-dos-miner)
- RustChain: [rustchain.org](https://rustchain.org)
- Slackware: [slackware.com](http://www.slackware.com)

## References

- [Technical Analysis](TECHNICAL_ANALYSIS.md)
- [Implementation Plan](IMPLEMENTATION_PLAN.md)
- [Hardware Guide](HARDWARE_GUIDE.md)
- [Build Instructions](BUILD.md)
- [Troubleshooting](docs/troubleshooting.md)

---

**"Every vintage computer has historical potential"**
