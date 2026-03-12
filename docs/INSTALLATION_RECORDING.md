# RustChain Miner Installation Recording

This directory contains installation recordings for the RustChain Miner.

## Files

- **miner-install.cast** - Asciinema recording of the complete installation process
- **miner-install.gif** - GIF animation of the installation process

## Installation Steps (Recorded)

1. **Check Rust Installation**
   ```bash
   rustc --version
   cargo --version
   ```

2. **Build the Miner**
   ```bash
   cd rust_miner
   cargo build --release
   ```

3. **Create Configuration**
   ```bash
   cp config.example.toml config.toml
   ```

4. **Verify Installation**
   ```bash
   ls target/release/rustchain-miner.exe
   ```

## Viewing the Recording

### Asciinema Format
Upload the `.cast` file to [asciinema.org](https://asciinema.org) to view interactively.

### GIF Format
Open `miner-install.gif` in any image viewer or web browser.

## Requirements

- Rust 1.70+ (rustc, cargo)
- Windows: Visual Studio Build Tools with C++ workload
- macOS: Xcode Command Line Tools
- Linux: build-essential, pkg-config

## Related Issue

- [Issue #1615: Record miner install as asciinema/GIF](https://github.com/Scottcjn/rustchain-bounties/issues/1615)
