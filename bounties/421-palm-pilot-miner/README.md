# RustChain Palm Pilot Miner

A native Palm Pilot PDA attestation miner for the RustChain blockchain.

## Overview

This project implements a RustChain miner that runs directly on Palm Pilot hardware (1997), powered by the Motorola 68328 (DragonBall) processor at 16 MHz. The Palm Pilot computes attestations natively and communicates via serial port to a modern PC bridge.

**Wallet**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`  
**Bounty**: 100 RTC (~$10 USD)  
**Status**: Open for Development  
**Antiquity Multiplier**: 3.0×

## Features

- ⏳ Palm OS 2.0+ native application
- ⏳ Motorola 68328 (DragonBall) native code
- ⏳ Serial communication via cradle
- ⏳ Hardware fingerprinting (anti-emulation)
- ⏳ Low-power operation (battery optimized)
- ⏳ Graffiti input for wallet entry

## Hardware Requirements

| Component | Specification | Notes |
|-----------|--------------|-------|
| **Palm Pilot** | Personal (512 KB) or Professional (1 MB) | 1996-1998 models |
| **Serial Cradle** | Palm Pilot serial cradle | For data transfer |
| **USB-Serial Adapter** | FTDI-based or similar | To connect to modern PC |
| **PC Bridge** | Any modern PC | Runs TCP/HTTP bridge |
| **Stylus** | Any Palm stylus | For input |

## Network Architecture

```
┌─────────────┐     Serial      ┌──────────────┐     HTTP      ┌─────────────┐
│ Palm Pilot  │ ◄─────────────► │ PC Bridge    │ ◄───────────► │ RustChain   │
│ (Miner)     │   (9600-115200) │ (Python/Node)│   (TCP/IP)    │ Network     │
└─────────────┘                 └──────────────┘               └─────────────┘
```

The Palm Pilot runs the miner application and collects hardware fingerprints. The PC bridge acts as a serial-to-TCP proxy, forwarding attestations to the RustChain network.

## Technical Specifications

### Palm Pilot Hardware

- **CPU**: Motorola 68328 (DragonBall) @ 16 MHz
- **RAM**: 512 KB (Personal) or 1024 KB (Professional)
- **Display**: 160×160 monochrome LCD
- **OS**: Palm OS 2.0 - 3.5
- **Storage**: Dynamic storage heaps
- **Power**: 2× AAA batteries (weeks of runtime)

### Memory Budget

| Component | Allocation |
|-----------|------------|
| Network stack | ~50 KB |
| Miner runtime | ~100 KB |
| Attestation data | ~10 KB |
| Display/UI | ~50 KB |
| **Free** | **~300 KB** |

## Development Status

### Phase 1: Development Setup (Week 1-2)

- [ ] Download Palm OS SDK
- [ ] Set up m68k-palmos-gcc cross-compiler
- [ ] Configure POSE emulator
- [ ] Build "Hello World" PRC

### Phase 2: Serial Communication (Week 3-6)

- [ ] Implement Serial Manager API
- [ ] Test data transfer to PC
- [ ] Implement protocol layer
- [ ] Handle errors/timeouts

### Phase 3: PC Bridge (Week 7-8)

- [ ] Write Python/Node.js bridge
- [ ] Serial ↔ HTTP proxy
- [ ] Test end-to-end
- [ ] Handle authentication

### Phase 4: Fingerprint Collection (Week 9-12)

- [ ] Read Palm OS device info
- [ ] Implement DragonBall checks
- [ ] Measure timing jitter
- [ ] Emulator detection

### Phase 5: Miner Integration (Week 13-16)

- [ ] Port attestation protocol
- [ ] Implement JSON builder
- [ ] Parse responses
- [ ] Epoch timing

### Phase 6: UI & Polish (Week 17-18)

- [ ] Main display
- [ ] Button handlers
- [ ] Menu system
- [ ] Power optimization

### Phase 7: Testing (Week 19-20)

- [ ] Real hardware testing
- [ ] Anti-emulation verification
- [ ] Documentation
- [ ] Video proof

## Build Instructions

### Prerequisites

```bash
# Install Palm OS toolchain
# Download Palm OS SDK from archive.org
# Install m68k-palmos-gcc

# Ubuntu/Debian:
sudo apt install palmos-sdk m68k-palmos-gcc

# macOS:
brew install palmos-sdk m68k-palmos-gcc
```

### Build PRC

```bash
cd palm-pilot-miner
make

# Output: RustChainMiner.prc
```

### Install on Palm Pilot

```bash
# Using Palm Install Tool
palm-install RustChainMiner.prc

# Or HotSync from desktop
```

## Usage

### 1. Install the Miner

HotSync the PRC file to your Palm Pilot. The miner will appear in the app launcher.

### 2. Configure Wallet

Launch the miner and enter your RTC wallet address using Graffiti or the soft keyboard.

### 3. Connect to PC Bridge

Connect the Palm Pilot serial cradle to your PC via USB-Serial adapter.

### 4. Start Mining

Run the PC bridge software and start the miner on the Palm Pilot.

```bash
# On PC (bridge)
python palm_bridge.py --port COM3 --wallet RTC4325af95d26d59c3ef025963656d22af638bb96b
```

## Hardware Fingerprinting

The Palm Pilot miner collects unique hardware fingerprints:

1. **DragonBall Chip ID** - CPU-specific registers
2. **Palm OS ROM Version** - ROM checksum and version
3. **RAM Timing Jitter** - Dynamic RAM timing variance
4. **Touchscreen Calibration** - Analog touchscreen variance
5. **Serial Port Timing** - UART timing characteristics

### Anti-Emulation

The miner detects POSE and other Palm OS emulators:

- POSE-specific register values
- Perfect touchscreen timing (no analog jitter)
- Emulated serial port behavior
- Fixed battery level readings

## Power Management

The miner is optimized for battery operation:

- **Active mining**: ~50 mA (during attestation)
- **Sleep mode**: ~0.1 mA (between epochs)
- **Display off**: Most of the time
- **Epoch interval**: 10 minutes
- **Battery life**: 2-4 weeks on 2× AAA

## Attestation Flow

1. Palm Pilot wakes from sleep
2. Collect hardware fingerprint
3. Build JSON attestation payload
4. Send via serial to PC bridge
5. Bridge forwards to `https://rustchain.org/api/attest`
6. Parse response
7. Display result
8. Return to sleep (10 minutes)

## Resources

### Development

- [Palm OS SDK Archives](https://web.archive.org/web/*/http://www.palmos.com/dev)
- [PalmOS-GCC](https://github.com/klamath/palmos-gcc)
- [POSE Emulator](https://web.archive.org/web/*/http://www.palmos.com/dev/pose)
- [Pilots-Inside](http://www.pilots-inside.org)

### Hardware

- **Palm Pilot** - eBay, $20-50
- **Serial Cradle** - eBay, $10-20
- **USB-Serial Adapter** - Any FTDI-based, $10

## Bounty Information

This is an open bounty. Complete the implementation and claim 100 RTC.

**Claim Requirements**:

- ✅ Real Palm Pilot hardware (not emulation)
- ✅ Successful attestation on RustChain network
- ✅ Photo/video proof
- ✅ Open source code (MIT license)
- ✅ Build instructions

**Submit your claim** by commenting on the GitHub issue with:

1. Link to your fork/PR
2. Photo of Palm Pilot running the miner
3. Video of attestation cycle
4. Attestation ID from the network
5. Your RTC wallet address

## License

MIT License - See LICENSE file for details.

## Contributing

Contributions welcome! This is a community bounty.

1. Fork the repo
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## FAQ

**Q: Can I use Palm III or Palm V?**

A: Yes! Palm III (1998) and Palm V (1999) are compatible and qualify for similar multipliers.

**Q: Do I need real hardware?**

A: Yes! The bounty requires real Palm Pilot hardware. Emulators will be detected and rejected.

**Q: What if I don't have a serial cradle?**

A: Serial cradles are ~$20 on eBay. Some Palm Pilots have built-in serial ports.

**Q: Does the PC bridge count as cheating?**

A: No! The Palm does the fingerprinting and attestation. The bridge is just a network proxy.

---

**Part of the [RustChain](https://github.com/Scottcjn/RustChain) ecosystem** · [RustChain Bounties](https://github.com/Scottcjn/rustchain-bounties)
