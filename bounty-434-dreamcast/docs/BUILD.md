# Building RustChain Miner for Sega Dreamcast

This document describes how to build the RustChain miner for the Sega Dreamcast gaming console.

## Prerequisites

### Required Software

1. **Rust Nightly** (required for SH-4 target support)
   ```bash
   rustup default nightly
   rustup component add rust-src
   ```

2. **KallistiOS Toolchain**
   ```bash
   # Clone KallistiOS
   git clone https://gitea.com/KallistiOS/KallistiOS.git ~/toolchain/kos
   
   # Set environment variables
   export KOS_BASE=~/toolchain/kos
   export KOS_PORTS=~/toolchain/kos/ports
   export PATH=$KOS_BASE/bin:$PATH
   
   # Build toolchain
   cd ~/toolchain/kos/utils
   make
   ```

3. **SH-4 Cross-Compiler**
   ```bash
   # KallistiOS includes sh4-elf-gcc
   # Verify installation:
   sh4-elf-gcc --version
   ```

### Required Hardware

- **Sega Dreamcast** with one of the following:
  - Broadband Adapter (BBA) - **Required for network mining**
  - 56k Modem - Not recommended (extremely slow)
  
- **Storage** (one of the following):
  - SD Card Adapter (GDEMU, MODE, etc.)
  - VMU (for configuration only)
  
- **Development PC** (Windows, Linux, or macOS)

## Building

### Step 1: Clone Repository

```bash
git clone https://github.com/RustChain/rustchain-dreamcast.git
cd rustchain-dreamcast
```

### Step 2: Configure Build

Edit `src/main.rs` to set your mining pool and wallet:

```rust
let mut miner = Miner::new("YOUR_WALLET_ADDRESS");
miner.connect("pool.rustchain.org", 3333);
```

### Step 3: Build for SH-4

```bash
# Build release version
cargo build --target target-specs/sh4-unknown-kallistios.json --release

# Output: target/sh4-unknown-kallistios/release/miner
```

### Step 4: Convert to KallistiOS Binary

```bash
# Convert ELF to KOS-compatible binary
sh4-elf-objcopy -O binary \
  target/sh4-unknown-kallistios/release/miner \
  miner.bin

# Create 1ST_READ.BIN for CD-R burning
cp miner.bin 1ST_READ.BIN
```

### Step 5: Create Bootable Disc/Image

#### Option A: CD-R Burning

```bash
# Create ISO with KOS tools
$KOS_BASE/bin/kos-iso -o rustchain-miner.iso .

# Burn to CD-R
cdrdao write rustchain-miner.iso
```

#### Option B: GDEMU SD Card

```bash
# Copy to SD card
cp miner.bin /sdcard/apps/rustchain/

# Or use gditool
gditool sdcard.img add miner.bin /apps/rustchain/1ST_READ.BIN
```

#### Option C: Emulator Testing

```bash
# Load in Flycast emulator
flycast rustchain-miner.cdi
```

## Docker Build (Recommended)

For reproducible builds, use the provided Docker container:

```bash
# Build Docker image
docker build -t rustchain-dreamcast .

# Build miner
docker run --rm -v $(pwd):/src rustchain-dreamcast make

# Output: miner.bin
```

## Build Configuration

### Optimization Levels

| Profile | Command | Size | Speed | Use Case |
|---------|---------|------|-------|----------|
| Release | `--release` | Small | Fast | Production |
| Dev | (default) | Large | Slow | Development |
| Size | `--profile size` | Smallest | Medium | Limited storage |

### Feature Flags

```bash
# Enable debug logging
cargo build --features debug-logging --release

# Enable network debugging
cargo build --features net-debug --release
```

## Troubleshooting

### Build Errors

**Error: `sh4-elf-gcc: not found`**
```bash
# Ensure KallistiOS is in PATH
export KOS_BASE=/path/to/kos
export PATH=$KOS_BASE/bin:$PATH
```

**Error: `unresolved extern symbol`**
```bash
# Check KOS bindings in kos/bindings.rs
# Ensure all FFI functions are properly declared
```

### Runtime Issues

**Miner crashes on startup**
- Check broadband adapter is connected
- Verify network configuration in `storage.rs`
- Enable debug logging for diagnostics

**No shares submitted**
- Verify pool connection (check network LED on BBA)
- Confirm wallet address is correct
- Check pool stratum protocol compatibility

## Performance Tuning

### SHA-256 Optimization

The SH-4 implementation uses:
- Loop unrolling (4 rounds per iteration)
- Superscalar instruction scheduling
- FPU vectorization where applicable

To benchmark:
```bash
cargo run --example sha256_benchmark --release
```

Expected: ~100-300 H/s

### Memory Optimization

The miner uses < 1 MB RAM, leaving plenty for KOS and network stack.

To reduce memory further:
```bash
# Build with size optimization
cargo build --profile size --release
```

## Next Steps

After building successfully:

1. Test on Flycast emulator
2. Test on real Dreamcast hardware
3. Monitor hashrate and share submission
4. Report issues on GitHub

## References

- [KallistiOS Documentation](https://gitea.com/KallistiOS/KallistiOS)
- [Rust Embedded Book](https://docs.rust-embedded.org/book/)
- [SH-4 Architecture Manual](https://www.renesas.com/us/en/products/microcontrollers-microprocessors/superh.html)
