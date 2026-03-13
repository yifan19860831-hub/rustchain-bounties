# [BOUNTY] Port RustChain Miner to Palm Pilot — 100 RTC

**Issue**: #421  
**Difficulty**: Extreme  
**Estimated Effort**: 2-4 months for experienced Palm OS developer  
**Reward**: 100 RTC ($10 USD)  
**Multiplier**: 3.0× antiquity multiplier  
**Status**: Open

---

## Overview

Port the RustChain miner to the Palm Pilot PDA (1997), powered by the Motorola 68328 (DragonBall) processor at 16 MHz with 512 KB - 1 MB of RAM. This is a legendary Proof-of-Antiquity mining platform.

The Palm Pilot defined the PDA category and predates smartphones by a decade. Successfully mining on this hardware demonstrates that authentic vintage devices can participate in the RustChain network.

---

## Why Palm Pilot?

| Feature | Specification | Significance |
|---------|--------------|--------------|
| **Year** | 1997 | 29 years old (2026) |
| **CPU** | Motorola 68328 @ 16 MHz | DragonBall, 68k family |
| **RAM** | 512 KB - 1 MB | Extremely constrained |
| **OS** | Palm OS 2.0+ | Single-tasking, event-driven |
| **Network** | Serial (external) | No built-in networking |
| **Power** | 2× AAA batteries | Weeks of runtime |

### The Challenge

- **RAM constraint**: 512 KB must hold OS, network stack, miner, and data
- **No networking**: Requires serial cradle + PC bridge or SD WiFi card
- **Single-tasking**: Miner must be foreground app
- **Obsolete toolchain**: Palm OS SDK is archived
- **68k architecture**: Requires cross-compilation

---

## Network Architecture

```
┌─────────────────┐     Serial      ┌──────────────┐     HTTP      ┌─────────────┐
│ Palm Pilot PDA  │ ◄─────────────► │ PC Bridge    │ ◄───────────► │ RustChain   │
│ (Miner App)     │   (9600-115200) │ (Python)     │   (TCP/IP)    │ Network     │
└─────────────────┘                 └──────────────┘               └─────────────┘
     1997                                2026                         Cloud
```

**The Palm Pilot is the miner** — it collects hardware fingerprints and builds attestations. The PC bridge is just a network proxy (like a modem).

---

## Hardware Requirements

| Component | Source | Cost |
|-----------|--------|------|
| Palm Pilot Personal/Professional | eBay | $20-50 |
| Serial Cradle | eBay | $10-20 |
| USB-Serial Adapter | Amazon | $10 |
| Stylus | Included | $0 |
| **Total** | | **~$50** |

### Alternative: SD WiFi Card (Later Models)

- **Socket Communications SD WiFi** - eBay, $30-50
- Only works on Palm OS 3.0+ (Palm III+, not original Pilot)
- Direct network access, no PC bridge needed

---

## Technical Implementation

### 1. Development Environment

**Toolchain:**

```bash
# Palm OS SDK (archived)
# Download from: https://web.archive.org/web/*/http://www.palmos.com/dev

# GCC cross-compiler
git clone https://github.com/klamath/palmos-gcc
cd palmos-gcc && ./build.sh

# POSE Emulator
# Download from archive.org
```

**Build:**

```bash
m68k-palmos-gcc -O2 -o miner.prc miner.c
palm-prc -o RustChainMiner.prc miner.prc
```

### 2. Serial Communication

**Palm OS Serial Manager API:**

```c
#include <SerialMgr.h>

// Open serial port
SndPortType *port;
SerOpen("Ser:", &port, serMode9600);

// Send data
SerSend(port, buffer, length);

// Receive data
SerReceive(port, buffer, length, timeout);
```

### 3. Hardware Fingerprinting

```c
typedef struct {
    char device_arch[16];      // "palm_68k"
    char device_family[16];    // "palm_pilot"
    uint32_t cpu_speed;        // 16000000 (16 MHz)
    uint16_t total_ram_kb;     // 512 or 1024
    uint32_t rom_checksum;     // ROM checksum
    uint32_t hardware_id;      // Unique per-device
} PalmFingerprint;
```

**Fingerprint Sources:**

1. DragonBall chip ID register
2. Palm OS ROM version + checksum
3. Dynamic RAM timing jitter
4. Touchscreen calibration variance
5. Serial port timing characteristics

### 4. Anti-Emulation

Detect POSE emulator:

```c
// POSE returns fixed values for these registers
if (read_register(0x1234) == 0xDEAD) {
    // Emulator detected!
    return ERROR_EMULATOR;
}

// Touchscreen timing (emulators have perfect timing)
// Real hardware has analog jitter
```

### 5. PC Bridge (Python)

```python
import serial
import requests

ser = serial.Serial('COM3', 9600)

while True:
    # Read attestation from Palm
    data = ser.readline()
    
    # Forward to RustChain
    response = requests.post(
        'https://rustchain.org/api/attest',
        json=json.loads(data)
    )
    
    # Send response back to Palm
    ser.write(response.text.encode())
```

---

## Memory Budget

| Component | Allocation |
|-----------|------------|
| Network stack (serial) | ~50 KB |
| Miner runtime | ~100 KB |
| Attestation data | ~10 KB |
| Display/UI | ~50 KB |
| **Free** | **~300 KB** |

---

## Power Management

| State | Current Draw | Duration |
|-------|-------------|----------|
| Active mining | ~50 mA | 1-2 min |
| Display on | ~30 mA | User interaction |
| Sleep | ~0.1 mA | 10 min (epoch) |

**Battery Life**: 2-4 weeks on 2× AAA batteries

---

## User Interface

```
┌────────────────────────────┐
│ RUSTCHAIN v0.1 - PALM    │
├────────────────────────────┤
│ Status: ATTESTING...       │
│ Epoch: 00:07:23 remaining  │
│ Earned: 0.0042 RTC         │
│                            │
│ Hardware:                  │
│ CPU: DragonBall @ 16 MHz   │
│ RAM: 512 KB                │
│ Net: Serial (9600)         │
│                            │
│ [Start] [Stop] [Menu]      │
└────────────────────────────┘
```

**Input**: Soft buttons + Graffiti handwriting

---

## Implementation Timeline

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| 1. Dev Setup | Week 1-2 | Toolchain, emulator |
| 2. Serial Comm | Week 3-6 | Serial + PC bridge |
| 3. Fingerprint | Week 9-12 | Hardware ID, anti-emulation |
| 4. Miner | Week 13-16 | Attestation protocol |
| 5. UI Polish | Week 17-18 | Display, input |
| 6. Testing | Week 19-20 | Real hardware, video |

---

## Acceptance Criteria

- ✅ Real Palm Pilot hardware (not emulation)
- ✅ Successful attestation on RustChain network
- ✅ Photo of Palm Pilot running miner (with timestamp)
- ✅ Video showing full attestation cycle (30+ seconds)
- ✅ Screenshot in `https://rustchain.org/api/miners`
- ✅ All source code on GitHub (MIT license)
- ✅ Build instructions (SDK setup, PRC installation)
- ✅ PRC file for others to test

---

## Claim Instructions

1. Complete the implementation
2. Test on real Palm Pilot hardware
3. Record photo/video proof
4. Open a PR to `rustchain-bounties` with:
   - Link to your miner repository
   - Photo of hardware running the miner
   - Video of attestation cycle
   - Attestation ID from the network
5. Comment on this issue with:
   - Link to your PR
   - Your RTC wallet address
   - Brief description of your approach

**Bounty Wallet**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`

---

## Resources

### Development

- [Palm OS SDK Archives](https://web.archive.org/web/*/http://www.palmos.com/dev)
- [PalmOS-GCC](https://github.com/klamath/palmos-gcc)
- [POSE Emulator](https://web.archive.org/web/*/http://www.palmos.com/dev/pose)
- [Pilots-Inside](http://www.pilots-inside.org)
- [PalmDB](https://www.palmdb.net)

### Hardware Reference

- [Motorola 68328 Datasheet](https://www.nxp.com/docs/en/data-sheet/MC68328.pdf)
- [Palm OS Programmer's Guide](https://web.archive.org/web/20010606034805/http://www.palmos.com/dev/docs.html)

### Community

- [Reddit r/palm](https://reddit.com/r/palm)
- [PalmOS.org Forum](https://www.palmos.org)

---

## FAQ

**Q: Can I use Palm III or Palm V instead?**

A: Yes! Palm III (1998) and Palm V (1999) are compatible and qualify for similar multipliers (2.8-3.0x).

**Q: Do I need to implement SHA-256 on the Palm?**

A: SHA-256 is slow on 16 MHz (~10-20 seconds per hash). The attestation server may accept a simpler hash for fingerprinting.

**Q: Can I use assembly?**

A: Yes! 68k assembly will be faster and smaller than C. Palm OS SDK supports inline assembly.

**Q: Does the PC bridge count as cheating?**

A: No! The Palm does the fingerprinting and attestation. The bridge is just a network proxy, like a modem.

**Q: How do I prove it's real hardware?**

A: Photo/video of the Palm running the miner. The attestation includes anti-emulation checks that fail on POSE.

---

## Comparison with Other Vintage Bounties

| Hardware | Year | RAM | Multiplier | Bounty |
|----------|------|-----|------------|--------|
| Apple II (6502) | 1977 | 48 KB | 4.0× | 150 RTC |
| Sega Genesis | 1988 | 64 KB | 3.5× | 150 RTC |
| **Palm Pilot** | **1997** | **512 KB** | **3.0×** | **100 RTC** |
| PowerPC G4 | 1999 | 256 MB | 2.5× | 75 RTC |
| Dreamcast | 1998 | 16 MB | 2.8× | 100 RTC |
| Modern x86 | 2026 | 16+ GB | 1.0× | 0 RTC |

---

*The PDA that started the mobile revolution, now mining cryptocurrency. If you can make a Palm Pilot attest to RustChain, you've earned every satoshi of that 3.0× multiplier.*

**Questions?** Comment on this issue or join the [RustChain Discord](https://discord.gg/jMAmHBpXcn).
