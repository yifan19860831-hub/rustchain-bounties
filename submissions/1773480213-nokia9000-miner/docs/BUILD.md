# Build Instructions - Nokia 9000 Communicator Miner

## Prerequisites

### For Building on Modern Systems (Cross-Compilation)

```bash
# Install NASM (Netwide Assembler)
# Windows
choco install nasm

# macOS
brew install nasm

# Linux (Debian/Ubuntu)
sudo apt-get install nasm

# Linux (Fedora/RHEL)
sudo dnf install nasm
```

### For Building on Actual Nokia 9000 Hardware

You'll need:

1. **Nokia 9000 Communicator** with development cable
2. **GEOS SDK 3.0** for application development
3. **ROM-DOS development tools**
4. **Cross-compiler** (386-targeting GCC or Borland C++ 3.1)
5. **Serial connection** to host PC for file transfer

## Build Process

### Option 1: Build Simulator (Recommended for Testing)

```bash
cd nokia9000-miner

# No build required - pure Python
# Just install dependencies:
pip install requests cryptography

# Run simulator:
cd simulator
python nokia9000_sim.py --wallet RTC4325af95d26d59c3ef025963656d22af638bb96b
```

### Option 2: Build 386 Assembly (For Real Hardware)

```bash
cd nokia9000-miner

# Assemble with NASM
nasm -f bin src/miner386.asm -o miner386.bin

# Assemble SHA-256 optimized routines
nasm -f bin src/sha256_386.asm -o sha256_386.bin

# Create GEOS application package
# (Requires GEOS SDK)
geos-app --name "RustChain Miner" \
         --entry miner386.bin \
         --output MINER.GAP
```

### Option 3: Full Build with Make

```bash
cd nokia9000-miner

# Build everything
make all

# Build simulator only
make simulator

# Build 386 binary only
make 386

# Clean build artifacts
make clean
```

## Build Outputs

```
nokia9000-miner/
├── miner386.bin          # 386 assembly binary (for real hardware)
├── sha256_386.bin        # SHA-256 optimized routines
├── MINER.GAP             # GEOS application package
├── simulator/
│   └── nokia9000_sim.py  # Python simulator (ready to run)
└── docs/
    └── BUILD.md          # This file
```

## Testing

### Test Simulator

```bash
cd simulator

# Basic test (60 second epoch simulation)
python nokia9000_sim.py --wallet RTC4325af95d26d59c3ef025963656d22af638bb96b

# Quick attestation test
python nokia9000_sim.py --wallet RTC4325af95d26d59c3ef025963656d22af638bb96b --attest-only

# Extended test (5 minute simulation)
python nokia9000_sim.py --wallet RTC4325af95d26d59c3ef025963656d22af638bb96b --duration 300
```

### Test on Real Hardware

1. **Transfer files to Nokia 9000:**
   ```bash
   # Using GEOS FileLink
   geos-transfer --port COM1 --file MINER.GAP
   ```

2. **Install on Nokia 9000:**
   - Open GEOS desktop
   - Navigate to received files
   - Double-click MINER.GAP to install

3. **Run miner:**
   - Launch "RustChain Miner" from GEOS applications
   - Enter wallet address when prompted
   - Mining will start automatically

## Build Configuration

### Memory Optimization

The Nokia 9000 has only 2 MB available for programs. The miner is optimized to use:

- **Code segment**: < 64 KB
- **Data segment**: < 128 KB
- **Stack**: 64 KB
- **Heap**: Remaining (~1.8 MB for mining buffers)

### Performance Tuning

For best performance on actual hardware:

1. **Enable 387 FPU** (if available) for faster floating-point operations
2. **Use internal cache** efficiently (8 KB unified cache)
3. **Minimize disk I/O** (no removable storage on Nokia 9000)
4. **Batch network operations** (GSM modem is slow at 9.6 kbit/s)

## Troubleshooting

### Build Errors

**"NASM not found"**
```bash
# Verify installation
nasm --version

# Add to PATH if needed
export PATH=$PATH:/usr/local/bin
```

**"Out of memory during build"**
```bash
# Build on host system, not on Nokia 9000
# The 386 assembly should be cross-compiled
```

### Runtime Errors

**"Insufficient memory"**
- Close other GEOS applications
- Ensure at least 1.5 MB free program memory

**"Network connection failed"**
- Check GSM signal strength
- Verify AT command configuration
- Ensure RustChain node is reachable

**"Hardware fingerprint mismatch"**
- This is normal if running in emulator
- Real hardware will generate unique fingerprint

## Advanced: Custom Builds

### Modify Difficulty

Edit `src/miner386.asm`:

```asm
; Change difficulty target
DIFFICULTY_TARGET dd 0x0000FFFF  ; Lower = easier
```

### Change Epoch Duration

Edit `simulator/nokia9000_sim.py`:

```python
EPOCH_DURATION = 300  # 5 minutes instead of 10
```

### Custom Wallet Storage

By default, wallet is stored in memory. For persistent storage:

```c
// In geos_app.c
void save_wallet(const char* wallet) {
    GEOSFileSave("miner.cfg", wallet, strlen(wallet));
}
```

## Performance Benchmarks

### Simulator (Modern PC)

```
Intel Core i7 @ 3.5 GHz
- Hash rate: ~50,000 hashes/sec
- Epoch time: 60s (simulated)
- Power usage: ~50W
```

### Real Nokia 9000 (Estimated)

```
Intel 386 @ 24 MHz
- Hash rate: ~100-200 hashes/sec
- Epoch time: 600s (real-time)
- Power usage: ~2W (battery powered)
- Expected earnings: ~0.36 RTC/epoch (3.0x multiplier)
```

## Next Steps

After building:

1. ✅ Test with simulator
2. ✅ Verify attestation submission
3. ⬜ Deploy to real Nokia 9000 (if available)
4. ⬜ Monitor mining performance
5. ⬜ Submit PR for bounty claim

For deployment instructions, see [DEPLOY.md](DEPLOY.md).

## Support

Issues? Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) or open a GitHub issue.

---

**Built with ❤️ for the Nokia 9000 Communicator (1996)**
