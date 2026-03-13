# [BOUNTY] Port RustChain Miner to Commodore 64 — 150 RTC (4.0x Multiplier!)

**Status:** Open
**Difficulty:** Extreme
**Estimated Effort:** 4-8 months for experienced 6502 developer

---

## Overview

Port the RustChain miner to the Commodore 64 (1982), powered by the MOS Technology 6510 @ 1.023 MHz with only **64 KB of RAM**. This is one of the most challenging vintage computing bounties ever proposed.

If successful, C64 hardware would earn a **4.0x antiquity multiplier** — the highest reward tier alongside Apple II and Intel 386.

---

## Why Commodore 64?

- **1982 hardware** — The best-selling single computer model of all time (12-17 million units)
- **MOS 6510 @ 1.023 MHz** — 8-bit CPU, derivative of legendary 6502 (same as Apple II, NES, Atari)
- **64 KB RAM** — Extremely constrained (only 38911 bytes BASIC-free for programs)
- **No MMU, no FPU** — Pure integer arithmetic, manual memory management
- **No built-in networking** — Requires custom hardware solution (the real challenge)
- **4.0x multiplier** — Maximum reward tier, justified by extreme difficulty and cultural significance

### The Unique Challenge

The C64 presents fundamentally different challenges than other vintage bounties:

1. **RAM constraint** — 64 KB must hold: Kernal ROM routines, network driver, miner runtime, screen buffer
2. **No standard networking** — Unlike PC architectures, C64 has no Ethernet standard
3. **Banked memory** — 6510 uses memory mapping for I/O; ROM can be swapped out for more RAM
4. **VIC-II graphics chip** — Cycle-exact timing required for stable display; DMA steals CPU cycles
5. **Tape/disk storage** — No standard persistent storage for wallet keys

---

## Hardware Required

| Component | Notes |
|-----------|-------|
| Commodore 64/64C | Any model. C64C has better power supply |
| **Network solution** | See options below (critical path) |
| Storage | 1541 floppy drive, Datasette, or SD2IEC |
| Real hardware | Emulation (VICE) for development only |

### Network Hardware Options

The C64 has **no built-in Ethernet**. Four viable paths exist:

#### Option A: RR-Net / Contempra Ethernet (Recommended)
- **Hardware:** RR-Net (Retro Replay) or Contempra Ethernet cartridge
- **Chip:** W5100 or W5500 Ethernet controller
- **Pros:** Standard solution, documented API, active community
- **Cons:** Requires specific hardware (~80-150 USD, sometimes rare)
- **Status:** Working TCP/IP stacks exist (tcpip.lib, Contempra library)

#### Option B: Userport RS-232 + Modern Bridge
- **Hardware:** C64 Userport → RS-232 cable → ESP32/Arduino → Ethernet
- **Pros:** Uses existing port, cheap (~20 USD for ESP32), well-documented
- **Cons:** Slow (2400-9600 baud typical), requires bridge firmware
- **Status:** Multiple projects exist (WiFi-Link, RS232 gateway)

#### Option C: Cartridge + ESP8266/ESP32
- **Hardware:** Custom cartridge or expansion port → SPI → WiFi module
- **Pros:** Modern WiFi, no cables, compact
- **Cons:** Requires cartridge design or purchase (EasyFlash, etc.)
- **Status:** Homebrew projects exist (C64 WiFi by various developers)

#### Option D: Datasette/1541 Emulation (Hack Mode)
- **Hardware:** SD2IEC or 1541 Ultimate-II+ with network capabilities
- **Pros:** Uses standard storage interface, multi-purpose device
- **Cons:** Expensive (~100-200 USD), complex protocol
- **Status:** SD2IEC has basic networking via firmware

---

## Technical Requirements

### 1. Development Environment (20 RTC)

**Toolchain:**
- **cc65** — C compiler for 6502 family (https://cc65.github.io)
- **ACME** — Cross-assembler for 6502 (https://sourceforge.net/projects/acme-cross-asm)
- **VICE** — Versatile Commodore Emulator (https://vice-emu.sourceforge.io)
- **Kick Assembler** — Modern assembler with macros (https://theweb.dk/KickAssembler)

**Setup:**
```bash
# cc65 installation (Windows via Chocolatey or manual)
choco install cc65

# Build a PRG file
cl65 -t c64 -o miner.prg miner.c

# Or assemble pure assembly
acme -o miner.prg miner.asm
```

**Memory Map:**
```
0x0000-0x00FF: Zero Page (critical for performance)
0x0100-0x01FF: Stack
0x0200-0x03FF: OS vectors, buffers
0x0400-0x07FF: Screen memory (default)
0x0801-0x9FFF: BASIC program area (~38 KB free)
0xA000-0xBFFF: BASIC ROM (can be swapped out)
0xC000-0xCFFF: I/O area (VIC-II, CIA, SID)
0xD000-0xDFFF: Character ROM / RAM
0xE000-0xFFFF: Kernal ROM (can be swapped out)
```

**With ROM swapped out:**
- Can use 0xA000-0xBFFF and 0xE000-0xFFFF as RAM
- Total usable RAM: ~60 KB

### 2. Network Stack Implementation (50 RTC)

**For RR-Net/Contempra:**
- Use existing `tcpip.lib` library (C64 TCP/IP stack)
- Minimal HTTP client (no TLS, plain HTTP to rustchain.org)
- Handle DHCP or static IP configuration

**For Userport + ESP32 Bridge:**
- Write RS-232 driver at 9600 baud
- Implement simple serial protocol for HTTP requests
- ESP32 handles WiFi, DNS, TCP connection

**Minimal Requirements:**
- TCP socket connection to rustchain.org:80 (HTTP, no TLS)
- HTTP POST with JSON attestation payload
- Response parsing (manual JSON parse)

**Memory Budget:**
```
Network stack:    ~15 KB
Miner runtime:    ~12 KB
Attestation data: ~5 KB
Screen buffer:    ~1 KB (VIC-II uses separate 16 KB)
Free:             ~31 KB (with ROM swapped)
```

### 3. Miner Implementation (50 RTC)

**Core Components:**

```c
// Pseudocode structure (cc65 C)
typedef struct {
    char device_arch[16];     // "c64_6510"
    char device_family[16];   // "commodore_64"
    uint32_t cpu_speed;       // 1023000 (1.023 MHz)
    uint16_t total_ram_kb;    // 64
    uint16_t rom_checksum;    // Kernal ROM checksum
    uint32_t hardware_id;     // Unique per-C64 ID (see below)
} C64Fingerprint;

// Hardware fingerprint sources:
// 1. CIA chip timing jitter (crystal variance)
// 2. VIC-II raster timing variations
// 3. SID chip frequency offset
// 4. DRAM refresh timing
// 5. Datasette motor control timing
```

**Anti-Emulation Checks:**
- CIA timer cycle-accuracy (emulators often have slight timing differences)
- VIC-II raster interrupt jitter (real hardware has analog variance)
- SID register readback behavior (some registers return different values)
- DRAM refresh timing (affects CPU cycle timing)
- Color burst phase (NTSC vs PAL detection)

**Attestation Flow:**
```
1. Initialize screen (40-column text mode)
2. Initialize network (Ethernet/WiFi)
3. Collect fingerprint data
4. Build JSON payload
5. POST to http://rustchain.org/api/attest
6. Parse response, display result
7. Wait 10 minutes (epoch), repeat
```

### 4. User Interface (20 RTC)

**Display Requirements:**
- 40x25 text mode (standard C64)
- Custom charset optional for nicer fonts
- PETSCII character set
- Color: 16 colors available

**Keyboard Input:**
- Restore keys for menu navigation
- Function keys for quick actions

**Example Screen:**
```
+----------------------------------------+
| #### RUSTCHAIN MINER v0.1 - C64 ####  |
+----------------------------------------+
| STATUS: ATTESTING...                   |
| EPOCH:  00:07:23 REMAINING            |
| EARNED: 0.0042 RTC                     |
|                                        |
| HARDWARE:                              |
| CPU: MOS 6510 @ 1.023 MHZ             |
| RAM: 64 KB                             |
| NET: RR-NET CONNECTED                  |
|                                        |
| [F1] PAUSE  [F3] MENU  [F5] QUIT      |
+----------------------------------------+
```

**Technical Notes:**
- Screen memory at 0x0400 (1000 bytes for 40x25)
- Color RAM at 0xD800 (1000 bytes)
- Must handle VIC-II DMA cycle stealing
- Raster interrupts for smooth updates

### 5. Prove It Works (10 RTC)

**Deliverables:**
- [ ] Photo of real C64 running miner (with timestamp)
- [ ] Video showing full attestation cycle (30+ seconds)
- [ ] Screenshot of miner in https://rustchain.org/api/miners
- [ ] Attestation record in network database
- [ ] All source code on GitHub (MIT license)
- [ ] Build instructions (cc65 setup, PRG creation)
- [ ] PRG file (.prg) for others to test

---

## The 4.0x Multiplier

**Commodore 64 / 6510 → 4.0x base multiplier (MAXIMUM TIER)**

Justification:
- **Age:** 1982 hardware (44 years old in 2026)
- **RAM constraint:** 64 KB (tied with Sega Genesis, less than Apple II's max 128 KB)
- **Networking:** No standard solution, requires cartridge or serial bridge
- **Cultural significance:** Best-selling computer of all time
- **CPU speed:** 1.023 MHz (slower than Genesis 68000 @ 7.6 MHz)
- **Market penetration:** 12-17 million units sold

**Comparison:**
| Hardware | Year | RAM | CPU | Multiplier |
|----------|------|-----|-----|------------|
| Ryzen 9 7950X | 2022 | 128 GB | 4.5 GHz | 1.0x |
| PowerPC G4 | 2003 | 1 GB | 1.42 GHz | 2.5x |
| **Commodore 64** | **1982** | **64 KB** | **1 MHz** | **4.0x** |
| Apple II (6502) | 1977 | 48 KB | 1 MHz | 4.0x |
| Intel 386 | 1985 | 4 MB | 16-40 MHz | 4.0x |
| Sega Genesis | 1988 | 64 KB | 7.6 MHz | 3.5x |
| Sega Dreamcast | 1998 | 16 MB | 200 MHz | 2.8x |

---

## The Brutal Reality

**This is genuinely one of the hardest bounties:**

### Challenge 1: 64 KB RAM
- Screen buffer: 1 KB (text) + color RAM
- Network stack: 10-15 KB (depending on solution)
- Miner runtime: 10-15 KB
- Zero page and stack: critical for performance
- Solution: Swap out BASIC/Kernal ROMs for extra RAM when needed

### Challenge 2: No Networking
- C64 has zero network hardware
- Solution: RR-Net cartridge (easiest) or Userport + ESP32 (cheapest)
- Both require driver development

### Challenge 3: 6502 Architecture
- Only 3 general-purpose registers (A, X, Y)
- No hardware multiplication (use lookup tables or shift-add)
- No division (use reciprocal multiplication or repeated subtraction)
- Page boundary crossings cost extra cycles
- BCD mode exists but slow (avoid for crypto)

### Challenge 4: Storage
- No standard persistent storage
- Wallet private key must be stored in:
  - Datasette tape (slow, unreliable)
  - 1541 floppy disk (requires drive)
  - EEPROM via cartridge (best option)
  - Or entered via keyboard each boot (not user-friendly)

### Challenge 5: Speed
- SHA-256 on 1 MHz 6510: ~2-5 minutes per hash (very slow!)
- **CRITICAL:** SHA-256 may be too slow for practical mining
- **Solution:** Server-side SHA-256, C64 only provides fingerprint
- Attestation cycle: 5-10 minutes total (acceptable)

### Challenge 6: VIC-II Cycle Timing
- VIC-II steals CPU cycles for display (DMA)
- Bad lines: every 8th raster line, CPU halted for 40 cycles
- Must disable interrupts during critical network operations
- Or use raster interrupts for precise timing

---

## Suggested Implementation Approach

### Phase 1: Development Setup (Week 1-2)
1. Install cc65 and VICE
2. Build "Hello World" PRG, test in emulator
3. Set up serial monitor for debugging
4. Acquire RR-Net or ESP32 bridge hardware

### Phase 2: Network Driver (Week 3-10)
1. Integrate RR-Net tcpip.lib or write Userport driver
2. Test basic HTTP GET to a test server
3. Implement HTTP POST with hardcoded payload
4. Handle connection errors, retries

### Phase 3: Fingerprint Collection (Week 11-16)
1. Read CIA timer values
2. Measure VIC-II raster timing jitter
3. Test SID register behavior
4. Calculate Kernal ROM checksum
5. Combine into unique hardware ID

### Phase 4: Miner Integration (Week 17-24)
1. Port attestation protocol from existing miner
2. Implement JSON builder (manual string formatting)
3. Parse attestation response
4. Handle epoch timing, retry logic
5. Add wallet key storage (EEPROM or manual entry)

### Phase 5: UI Polish (Week 25-30)
1. Create 40-column text display
2. Add keyboard input handling
3. Implement menu system
4. Add status indicators, error messages
5. Optional: custom charset for nicer fonts

### Phase 6: Testing & Documentation (Week 31-34)
1. Test on multiple C64 units (NTSC and PAL)
2. Verify anti-emulation works (test in VICE, should fail)
3. Write build instructions
4. Create video proof
5. Submit PR, claim bounty

---

## Resources

### Development
- [cc65](https://cc65.github.io) — C compiler for 6502
- [VICE](https://vice-emu.sourceforge.io) — Best C64 emulator
- [C64-Wiki](https://www.c64-wiki.com) — Comprehensive documentation
- [CodeBase64](https://codebase64.org) — Tutorials and code examples

### Hardware
- [RR-Net](https://www.c64-wiki.com/wiki/RR-Net) — Ethernet cartridge
- [Contempra](https://github.com/tehn/contempra) — Alternative Ethernet solution
- [SD2IEC](https://www.sd2iec.com) — SD card interface with networking
- [EasyFlash](https://www.c64-wiki.com/wiki/EasyFlash) — Flash cartridge for storage

### Technical Reference
- [C64 Programmer's Reference Guide](https://www.commodore.ca/gallery/magazines/pdf/Commodore-Programmers-Reference-Guide.pdf) — Official docs
- [Mapping the Commodore 64](https://www.atariarchives.org/map/index.php) — Essential memory map
- [Commodore 64 Assembly Language Programming](https://www.c64.org) — Derek Bush's book

### Community
- [Lemon64 Forum](https://www.lemon64.com/forum) — Active C64 community
- [C64 Discord](https://discord.gg/c64) — Real-time help
- [GitHub C64 Organization](https://github.com/C64) — Modern projects

---

## Claim Rules

- **Partial claims accepted** — Complete any numbered section for its RTC amount
- **Full completion = 150 RTC total**
- **Must be real C64 hardware** — Emulators don't count (and will be detected!)
- **Open source everything** — MIT or BSD license required
- **Multiple collaborators allowed** — Split bounty as agreed

---

## Wallet for Bounty Claim

**RTC Wallet:** `RTC4325af95d26d59c3ef025963656d22af638bb96b`

---

## FAQ

**Q: Can I use a Commodore 128?**
A: Yes! C128 is backward compatible with C64 mode. It has 128 KB RAM and a faster Z80 for CP/M, but in C64 mode it's identical. Still qualifies for 4.0x multiplier.

**Q: What about the VIC-20?**
A: VIC-20 has only 5 KB RAM (expandable to 32 KB). Much harder than C64! Separate bounty can be created (likely 4.5-5.0x multiplier).

**Q: Do I need to implement SHA-256?**
A: SHA-256 on 1 MHz 6510 would take 2-5 minutes per hash — too slow for practical mining. The attestation server may accept a simpler hash for fingerprinting, with SHA-256 done server-side.

**Q: Can I use pure assembly?**
A: Yes! Pure 6502 assembly will be faster and smaller than C. cc65 supports inline assembly, or use ACME/Kick Assembler for pure asm.

**Q: What if I can't afford RR-Net?**
A: Userport + ESP32 bridge is much cheaper (~20 USD for ESP32). Slower but works. Or find a local retro computing group that might have hardware.

**Q: NTSC or PAL?**
A: Both work! NTSC is 1.023 MHz, PAL is 0.985 MHz. Slight speed difference. Test on both if possible.

---

*The computer that defined a generation, now mining cryptocurrency. If you can make a C64 attest to RustChain, you've earned the maximum 4.0x multiplier.*

**Install the miner:** `pip install clawrtc && clawrtc mine`

**Questions?** Comment on this issue or join the [RustChain Discord](https://discord.gg/jMAmHBpXcn).
