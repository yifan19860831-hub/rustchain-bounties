# Building RustChain Palm III Miner

## Build Options

### Option 1: Metrowerks CodeWarrior (Official)

**Requirements:**
- Metrowerks CodeWarrior for Palm OS (v5.0+)
- Palm OS SDK 3.5
- PilRC resource compiler

**Steps:**

1. Open `Miner.mcp` project in CodeWarrior
2. Select target: `Palm III Release`
3. Build → Make (F5)
4. Output: `Miner.prc`

**Project Settings:**
```
Target: Palm OS 3.5
CPU: Motorola 68328 (DragonBall EZ)
Memory Model: Small
Optimization: Size (critical for 2MB RAM)
```

### Option 2: prc-tools (Open Source)

**Requirements:**
```bash
# Ubuntu/Debian
sudo apt-get install gcc m68k-palmos-gcc prc-tools pilrc

# Or build from source:
git clone https://github.com/jgh/prc-tools
```

**Build:**
```bash
cd palm-iii-miner/
make palmos
```

**Output:** `Miner.prc`

### Option 3: Cross-compile with m68k-elf-gcc

**Toolchain:**
```bash
# Build toolchain
git clone https://github.com/m68k-mcu/m68k-gcc-toolchain
cd m68k-gcc-toolchain
./build.sh
```

**Compile:**
```bash
m68k-elf-gcc -Os -mcpu=68328 -c src/MinerMain.c
m68k-elf-ld -o Miner.elf *.o
m68k-elf-objcopy -O binary Miner.elf Miner.bin
```

## Resource Compilation

```bash
# Compile resources
pilrc resources/Miner.rcp

# Link with code
prc-link -o Miner.prc Miner.code Miner.res
```

## Memory Optimization

Target memory layout:
```
Code:        64 KB
Resources:   32 KB
Heap:        1.5 MB
Stack:       32 KB
Free:        ~400 KB
```

**Optimization flags:**
```
-Os            # Optimize for size
-fomit-frame-pointer
-mshort        # 16-bit ints
-fno-exceptions
```

## Testing

### Simulator (Python)
```bash
cd simulator/
python palm_miner.py
```

### POSE (Palm OS Emulator)
1. Download POSE from PalmSource
2. Load Palm III ROM image
3. Install `Miner.prc` via drag-drop
4. Run and test

### Real Hardware
1. HotSync `Miner.prc` to Palm III
2. Launch from app launcher
3. Generate wallet (BACKUP IT!)
4. Start mining

## Troubleshooting

### "Out of Memory"
- Reduce heap allocation
- Use dynamic loading for forms
- Check for memory leaks with MemDebug

### "Invalid Application"
- Verify creator ID: `'RtMn'`
- Check ROM version compatibility
- Ensure resource IDs don't conflict

### Build Errors
```
# Missing Palm OS headers
export PALM_OS_SDK=/path/to/sdk
make

# prc-tools not found
export PATH=$PATH:/usr/local/palm/bin
```

## Deployment

### HotSync Installation
1. Connect Palm III via serial cradle
2. Run HotSync Manager
3. Add `Miner.prc` to install list
4. Sync to device

### Direct Load (Developer)
```bash
# Using pilot-link
pilot-install -p /dev/ttyS0 Miner.prc
```

## Performance Tuning

### Hash Rate Optimization
- Use assembly for critical hash loops
- Unroll loops (trade size for speed)
- Precompute constants

### Power Management
```c
// Sleep between hash iterations
SysTaskSleep(1);

// Use wake trigger for attestation
SysSetAutoOffTime(300);  // 5 minutes
```

## Bounty Submission

After successful build and test:

1. Create GitHub repository
2. Add README with wallet address
3. Submit PR to RustChain bounty tracker
4. Include:
   - `Miner.prc` binary
   - Source code
   - Build instructions
   - Screenshot from real hardware (if possible)

**Wallet for Bounty:** `RTC4325af95d26d59c3ef025963656d22af638bb96b`

---

## Quick Start (Simulator)

Don't have a Palm III? Test with the simulator:

```bash
cd palm-iii-miner/simulator/
python palm_miner.py

# Commands:
# m - Toggle mining
# s - Status
# w - Wallet
# q - Quit
```

This emulates the DragonBall entropy collection and Palm OS behavior!
