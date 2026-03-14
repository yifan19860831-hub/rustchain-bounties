# Quick Start Guide - RustChain Miner for ColecoVision

## Prerequisites

### For Simulation (Recommended)

- Python 3.7 or later
- No additional dependencies required!

### For Real Hardware (Advanced)

- z80asm or similar Z80 assembler
- openMSX ColecoVision emulator (for testing)
- Actual ColecoVision console (for running on real hardware)
- EPROM burner (to create cartridge)

---

## Running the Simulator

### Basic Usage

```bash
cd simulator
python miner_simulator.py
```

This runs the miner indefinitely until you press `Ctrl+C`.

### Limited Run

```bash
python miner_simulator.py 1000
```

Runs exactly 1000 hash attempts, then exits.

### Expected Output

```
RustChain Miner Simulator for ColecoVision
Starting emulation...

============================================================
RUSTCHAIN MINER FOR COLECOVISION (1982)
============================================================
CPU: Z80A @ 3.58 MHz
RAM: 1 KB (Allocated: 1024 bytes)
VRAM: 16 KB (TMS9918)
Cartridge ROM: 4 KB
============================================================
Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b
============================================================

+======================================+
|     RUSTCHAIN MINER v1.0             |
|     ColecoVision (1982)              |
+--------------------------------------+
|  NONCE: 0x000001F4                   |
|  HASH:  0x000F3A2C                   |
|  BEST:  0x000F3A2C                   |
|  RATE:  680 H/s                      |
+--------------------------------------+
|                                      |
|  [>==================             ]  |
|                                      |
+======================================+

Total Hashes: 500
Successful:   0
Elapsed:      0.74s
Simulated:    2649200 CPU cycles

Press Ctrl+C to stop
```

---

## Building for Real Hardware

### Step 1: Install Z80 Assembler

#### Windows

```bash
# Download z80asm from GitHub
# https://github.com/Konamiman/Z80DotNet
```

#### Linux/Mac

```bash
# Using package manager
sudo apt-get install z80asm  # Debian/Ubuntu
brew install z80asm          # macOS (if available)

# Or build from source
git clone https://github.com/Konamiman/Z80DotNet
cd Z80DotNet
make
```

### Step 2: Assemble the Code

```bash
cd src
z80asm -i miner.asm -o miner.bin
```

This produces `miner.bin` - a 4 KB ROM image.

### Step 3: Test in Emulator

```bash
openmsx -machine ColecoVision -cart miner.bin
```

You should see the mining display on the emulated ColecoVision screen.

### Step 4: Run on Real Hardware (Optional)

**⚠️ WARNING:** Running custom code on 40+ year old hardware carries risk. Proceed at your own risk.

1. Burn `miner.bin` to a 4 KB EPROM (2732 or equivalent)
2. Install EPROM in a ColecoVision cartridge shell
3. Insert cartridge into ColecoVision
4. Power on and observe the display

---

## Understanding the Output

### Display Fields

| Field | Description |
|-------|-------------|
| **NONCE** | Current 32-bit nonce value (increments each hash) |
| **HASH** | Current hash result (first 4 bytes, hex) |
| **BEST** | Best hash found so far (lowest value) |
| **RATE** | Hash rate in hashes per second |
| **Progress Bar** | Visual indicator of nonce progress |

### Statistics

After stopping (Ctrl+C), you'll see:

```
Total Hashes:     1000
Successful:       0
Average Rate:     680.50 H/s
Elapsed Time:     1.47s
Simulated Cycles: 5262600
```

- **Total Hashes:** Number of hash attempts
- **Successful:** Number of valid hashes found (below target)
- **Average Rate:** Hashes per second
- **Simulated Cycles:** Z80 CPU cycles (at 3.58 MHz)

---

## Troubleshooting

### Simulator Issues

**Problem:** `ModuleNotFoundError: No module named 'hashlib'`

**Solution:** hashlib is built into Python 3. Make sure you're using Python 3.7+.

```bash
python --version  # Should be 3.7 or later
```

**Problem:** Display shows garbled characters

**Solution:** Your terminal may not support ASCII box-drawing. The simulator should auto-detect and use simple characters.

**Problem:** Hash rate is 0 H/s

**Solution:** The simulator needs to run for at least 100 hashes before displaying rate. Let it run longer.

### Assembly Issues

**Problem:** `z80asm: command not found`

**Solution:** z80asm is not in your PATH. Either add it to PATH or use the full path:

```bash
/path/to/z80asm -i miner.asm -o miner.bin
```

**Problem:** `Error: Undefined symbol 'VDP_CONTROL'`

**Solution:** Make sure `miner.h` is in the same directory as `miner.asm`, or specify the include path:

```bash
z80asm -i miner.asm -I . -o miner.bin
```

**Problem:** `Output file too large`

**Solution:** The code exceeds 4 KB. This shouldn't happen with the provided source, but if you modify it, check for infinite loops or excessive data.

---

## Performance Tuning

### Simulator

The simulator runs as fast as Python allows. To simulate realistic Z80 speed:

```python
# In miner_simulator.py, line ~200
time.sleep(0.001)  # Increase this value to slow down
```

### Real Hardware

The Z80 assembly is already highly optimized. Further improvements would require:

1. **Faster Z80:** Overclock the ColecoVision (not recommended!)
2. **Reduce display updates:** Update every 128 hashes instead of 64
3. **Further truncate SHA-256:** Use even fewer rounds (not recommended)

---

## Experimentation Ideas

### Easy Modifications

1. **Change difficulty:** Edit `DIFFICULTY` in `miner.h`
2. **Change display:** Modify the screen buffer in `miner.asm`
3. **Add sound:** Use the SN76489 PSG for audio feedback

### Advanced Modifications

1. **Full SHA-256:** Implement all 64 rounds (will be very slow)
2. **Network sync:** Add homebrew network adapter support
3. **Multi-cartridge:** Link multiple ColecoVisions together

---

## Learning Resources

### Z80 Assembly

- [Z80 Instruction Set Reference](http://www.z80.info/decoding.htm)
- [Programming the Z80](http://www.z80.info/programming.htm)
- [ColecoVision Technical Documentation](http://www.colecovisionzone.com/)

### ColecoVision Development

- [ColecoVision Zone](http://www.colecovisionzone.com/)
- [openMSX Emulator](https://openmsx.org/)
- [ColecoVision Homebrew Community](https://atariage.com/forums/forum/84-colecovision/)

### Cryptocurrency Mining

- [Bitcoin Wiki: Mining](https://en.bitcoin.it/wiki/Mining)
- [SHA-256 Algorithm](https://en.wikipedia.org/wiki/SHA-2)

---

## Next Steps

1. ✅ Run the simulator to see it in action
2. ✅ Read `MEMORY_MAP.md` to understand memory allocation
3. ✅ Read `ARCHITECTURE.md` to understand design decisions
4. ✅ Try assembling the code for emulator testing
5. ✅ Submit your own modifications via PR!

---

**Questions?** Check the main README.md or open an issue.

**Happy Mining!** ⛏️
