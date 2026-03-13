# RustChain Miner for Commodore 64

**Bounty:** 150 RTC (4.0x multiplier)  
**Wallet:** `RTC4325af95d26d59c3ef025963656d22af638bb96b`  
**Status:** In Development

---

## Overview

This project ports the RustChain cryptocurrency miner to the Commodore 64 (1982), one of the most iconic home computers ever made.

**Target Hardware:**
- CPU: MOS Technology 6510 @ 1.023 MHz
- RAM: 64 KB
- Network: RR-Net Ethernet cartridge or Userport + ESP32 bridge

**Why C64?**
- 1982 hardware (44+ years old)
- Best-selling single computer model of all time (12-17 million units)
- Maximum 4.0x antiquity multiplier on RustChain network
- Extreme technical challenge: 64 KB RAM, no built-in networking

---

## Requirements

### Hardware

**Minimum:**
- Commodore 64 or 64C
- Network solution:
  - **Option A (Recommended):** RR-Net Ethernet cartridge (~$80-150)
  - **Option B (Cheaper):** ESP32 dev board + Userport cable (~$20-30)

**Optional:**
- 1541 floppy drive or SD2IEC for storage
- Real hardware for final testing (emulation for development)

### Software

**Development:**
- cc65 compiler (https://cc65.github.io)
- VICE emulator (https://vice-emu.sourceforge.io)

**Windows Installation:**
```powershell
choco install cc65
choco install vice
```

**Linux Installation:**
```bash
sudo apt install cc65 vice
```

---

## Building

### Quick Start

```bash
# Build
make

# Run in emulator
make run
```

### Manual Build

```bash
cl65 -t c64 -O -o miner.prg src/main.c src/miner.c src/network.c src/fingerprint.c src/ui.c
```

### Output

- `miner.prg` - C64 program file (loadable in VICE or on real hardware)

---

## Usage

### In VICE Emulator

1. Build the project: `make`
2. Run in VICE: `make run` or `x64 miner.prg`
3. Press any key to start
4. Use function keys:
   - **F1:** Pause/Resume mining
   - **F3:** Show menu
   - **F5:** Quit

### On Real Hardware

1. Transfer `miner.prg` to C64:
   - **SD2IEC:** Copy to SD card, load with `LOAD"MINER.PRG",8,1`
   - **1541:** Transfer via cable or floppy
   - **Cartridge:** Flash to EasyFlash or similar

2. Load and run:
   ```
   LOAD"MINER.PRG",8,1
   RUN
   ```

3. Wait for network initialization
4. Miner will automatically perform attestations every 10 minutes

---

## Network Configuration

### RR-Net Setup

The RR-Net cartridge provides Ethernet connectivity via the expansion port.

**Configuration:**
1. Edit `src/network.c` to set your network parameters
2. DHCP is supported, or set static IP
3. Default server: `rustchain.org:80`

### Userport + ESP32 Setup

**ESP32 Firmware:**
- Flash ESP32 with WiFi-to-serial bridge firmware
- Configure WiFi credentials
- Set baud rate to 9600

**Wiring:**
```
C64 Userport    ESP32
-----------     -----
PB (Pin 5)  →   TX (GPIO 1)
PA (Pin 4)  →   RX (GPIO 3)
GND (Pin 1) →   GND
```

---

## Project Structure

```
c64-miner/
├── src/
│   ├── main.c              # Entry point
│   ├── miner.c/h           # Core miner logic
│   ├── network.c/h         # Network stack interface
│   ├── fingerprint.c/h     # Hardware fingerprinting
│   └── ui.c/h              # User interface
├── asm/
│   └── (assembly routines for performance-critical code)
├── include/
│   └── (C64 hardware definitions)
├── Makefile
└── README.md
```

---

## Technical Details

### Memory Map

```
$0000-$00FF: Zero Page (critical for performance)
$0100-$01FF: Stack
$0400-$07FF: Screen memory
$0801-$9FFF: Program area (~38 KB free)
$A000-$BFFF: BASIC ROM (can be swapped for RAM)
$D000-$DFFF: I/O area (VIC-II, CIA, SID)
$E000-$FFFF: Kernal ROM (can be swapped for RAM)
```

### Hardware Fingerprinting

The miner collects unique hardware identifiers:

1. **CIA Timer Jitter:** Crystal variance creates timing differences
2. **VIC-II Raster Timing:** Analog variations in video chip
3. **SID Chip Behavior:** Register readback characteristics
4. **Kernal ROM Checksum:** Unique per ROM version

These fingerprints prove the miner is running on real C64 hardware and not an emulator.

### Anti-Emulation

The miner detects common emulators (VICE, Hoxs64, etc.) by:
- Measuring cycle-accurate timing jitter
- Testing SID register behavior
- Checking for emulator-specific quirks

Emulators will fail attestation verification.

---

## Development Phases

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Development environment setup | ✅ Complete |
| 2 | Network stack implementation | 🔄 In Progress |
| 3 | Hardware fingerprinting | 🔄 In Progress |
| 4 | Miner integration | ⏳ Pending |
| 5 | UI polish | ⏳ Pending |
| 6 | Testing on real hardware | ⏳ Pending |

---

## Testing

### Emulator Testing

```bash
# Run in VICE
x64 miner.prg

# With debug output
x64 -log miner.log miner.prg
```

### Real Hardware Testing

**Required for bounty claim:**
1. Photo of C64 running miner (with timestamp)
2. Video showing full attestation cycle (30+ seconds)
3. Screenshot of miner in rustchain.org/api/miners
4. Attestation record in network database

---

## Troubleshooting

### Build Errors

**Error: `cl65: command not found`**
- Install cc65 compiler
- Add cc65/bin to PATH

**Error: `out of memory`**
- Enable optimizations: `-O -Or -Oi`
- Bank out ROMs for extra RAM
- Reduce buffer sizes

### Network Errors

**Error: `NETWORK INIT FAILED`**
- Check RR-Net cartridge is seated properly
- Verify network cable is connected
- Check DHCP server is available

**Error: `CONNECT FAILED`**
- Verify rustchain.org is reachable
- Check firewall settings
- Try static IP configuration

### Runtime Errors

**Error: `ATTESTATION FAILED`**
- Check network connection
- Verify wallet address is correct
- Check server response for details

---

## Bounty Claim

**Total:** 150 RTC  
**Wallet:** `RTC4325af95d26d59c3ef025963656d22af638bb96b`

**Deliverables:**
- [ ] Source code on GitHub (MIT license)
- [ ] Build instructions
- [ ] Photo of real C64 running miner
- [ ] Video of attestation cycle
- [ ] Screenshot from rustchain.org/api/miners
- [ ] Attestation hash/ID

**Submit via:** GitHub issue comment or RustChain Discord

---

## Resources

- [cc65 Documentation](https://cc65.github.io/doc/)
- [C64-Wiki](https://www.c64-wiki.com)
- [CodeBase64](https://codebase64.org)
- [VICE Emulator](https://vice-emu.sourceforge.io)
- [RR-Net Documentation](https://www.c64-wiki.com/wiki/RR-Net)
- [RustChain Discord](https://discord.gg/jMAmHBpXcn)

---

## License

MIT License - See LICENSE file for details

---

## Credits

- Original concept: RustChain Bounties
- C64 development: cc65 team
- Emulator: VICE team
- This project: Open source community

---

*The computer that defined a generation, now mining cryptocurrency.*
