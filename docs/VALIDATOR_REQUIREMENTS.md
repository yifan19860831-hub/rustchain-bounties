# RustChain Validator Requirements

This document specifies the hardware, software, and network requirements for running a RustChain validator node.

---

## Table of Contents

1. [Overview](#overview)
2. [Hardware Requirements](#hardware-requirements)
3. [Software Requirements](#software-requirements)
4. [Network Requirements](#network-requirements)
5. [Installation](#installation)
6. [Configuration](#configuration)
7. [Maintenance](#maintenance)
8. [Troubleshooting](#troubleshooting)

---

## Overview

RustChain uses **Proof of Antiquity (PoA)** consensus, which rewards validators based on the age and authenticity of their hardware rather than computational power. This unique approach makes running a validator accessible and environmentally sustainable.

**Key Principles:**
- 🎯 **One CPU, One Vote** - Each unique hardware device gets exactly 1 vote per epoch
- 🏆 **Older = Better** - Vintage hardware earns higher rewards (up to 2.5× multiplier)
- ✅ **Anti-Emulation** - Hardware fingerprinting prevents VM spoofing
- ⚡ **Low Resource** - No need for expensive equipment or massive energy consumption

---

## Hardware Requirements

### Minimum Requirements

| Component | Requirement | Notes |
|-----------|-------------|-------|
| **CPU** | Any x86_64 or ARM64 processor | Modern or vintage |
| **RAM** | 512 MB | 1 GB recommended |
| **Storage** | 2 GB free space | SSD preferred |
| **Network** | 1 Mbps upload/download | Stable connection required |
| **Power** | Standard power supply | UPS recommended |

### Recommended Hardware Tiers

RustChain rewards vintage hardware with multipliers based on age:

| Tier | Age (Years) | Multiplier | Example Hardware | Earnings/Epoch |
|------|-------------|------------|------------------|----------------|
| **Ancient** | 40+ | 3.0× | Intel 8086, 486 | 0.36 RTC |
| **Sacred** | 30-39 | 2.8× | Pentium, Pentium II | 0.34 RTC |
| **Vintage** | 20-29 | 2.5× | PowerPC G4, Pentium 4 | 0.30 RTC |
| **Classic** | 15-19 | 2.0× | PowerPC G5, Core 2 Duo | 0.24 RTC |
| **Retro** | 10-14 | 1.5× | IBM POWER8, Early i7 | 0.18 RTC |
| **Modern** | 5-9 | 1.2× | Apple Silicon, Ryzen 3000 | 0.14 RTC |
| **Recent** | 0-4 | 1.0× | Latest CPUs | 0.12 RTC |

**Base reward:** 0.12 RTC per epoch (10 minutes)

### Hardware Fingerprinting

RustChain performs 6 hardware checks to verify authenticity:

1. **Clock-Skew & Oscillator Drift** - Silicon aging patterns
2. **Cache Timing Fingerprint** - L1/L2/L3 latency signatures
3. **SIMD Unit Identity** - AltiVec/SSE/NEON bias detection
4. **Thermal Drift Entropy** - Unique heat curves
5. **Instruction Path Jitter** - Microarchitecture jitter mapping
6. **Anti-Emulation Checks** - VM/emulator detection

⚠️ **Note:** Virtual machines are detected and receive 0.0000000001× rewards (effectively zero).

### Supported Platforms

| Platform | Architecture | Status | Notes |
|----------|--------------|--------|-------|
| **macOS** | PowerPC G4/G5 | ✅ Full Support | Python 2.5 compatible |
| **macOS** | Apple Silicon | ✅ Full Support | M1/M2/M3 chips |
| **Ubuntu Linux** | ppc64le/POWER8 | ✅ Full Support | Best performance |
| **Ubuntu Linux** | x86_64 | ✅ Full Support | Standard miner |
| **Windows** | x86_64 | ✅ Full Support | Python 3.8+ |
| **DOS** | 8086/286/386 | 🔧 Experimental | Badge rewards only |

---

## Software Requirements

### Operating System

**Linux (Recommended):**
- Ubuntu 20.04+ or Debian 11+
- Fedora 38+
- Kernel 4.15 or newer

**macOS:**
- macOS 12+ (Monterey or newer) for Intel/Apple Silicon
- Mac OS X Tiger (10.4) or Leopard (10.5) for PowerPC

**Windows:**
- Windows 10/11 (64-bit)
- Windows Server 2016+

### Runtime Dependencies

| Component | Version | Required |
|-----------|---------|----------|
| **Python** | 3.10+ | ✅ Yes |
| **pip** | 21.0+ | ✅ Yes |
| **Git** | 2.30+ | Optional |
| **curl** | 7.68+ | ✅ Yes |

### Python Packages

The installer automatically installs required packages:

```bash
pip install clawrtc
```

**Core dependencies:**
- `requests` - HTTP client
- `cryptography` - Ed25519 signatures
- `psutil` - System monitoring
- `numpy` - Numerical operations

### Node Software

Download the RustChain node software:

```bash
# Clone the repository
git clone https://github.com/Scottcjn/Rustchain.git
cd Rustchain

# Run the universal installer
curl -sSL https://raw.githubusercontent.com/Scottcjn/Rustchain/main/install-miner.sh | bash
```

**Manual installation:**

```bash
# Install Python package
pip install clawrtc

# Verify installation
clawrtc --version
```

---

## Network Requirements

### Bandwidth

| Activity | Upload | Download |
|----------|--------|----------|
| **Idle (sync)** | 10 KB/s | 10 KB/s |
| **Active validation** | 50 KB/s | 50 KB/s |
| **Initial sync** | 100 KB/s | 500 KB/s |

**Minimum:** 1 Mbps symmetric connection  
**Recommended:** 10 Mbps symmetric connection

### Ports

| Port | Protocol | Purpose |
|------|----------|---------|
| **9333** | TCP | P2P peer communication |
| **9332** | TCP | RPC/API endpoint |
| **443** | TCP | HTTPS (node API) |

**Firewall Configuration:**
```bash
# UFW (Ubuntu)
sudo ufw allow 9333/tcp
sudo ufw allow 9332/tcp
sudo ufw allow 443/tcp

# firewalld (Fedora/CentOS)
sudo firewall-cmd --permanent --add-port=9333/tcp
sudo firewall-cmd --permanent --add-port=9332/tcp
sudo firewall-cmd --permanent --add-port=443/tcp
sudo firewall-cmd --reload
```

### Latency

- **Maximum acceptable:** 500ms to bootstrap nodes
- **Recommended:** <100ms
- **Optimal:** <50ms

### Bootstrap Nodes

Connect to these initial nodes:

```
192.168.0.160:9333  # Sophia Prime Node
192.168.0.125:9333  # G4 Mirror Door Genesis Node
192.168.0.126:9333  # G4 Mirror Door Secondary
```

### Public Node Access

If running a public node:

- **Static IP:** Recommended (or dynamic DNS)
- **Uptime:** 99%+ for optimal rewards
- **Geographic distribution:** Diverse locations preferred

---

## Installation

### Quick Install (Linux/macOS)

```bash
# One-line installer
curl -sSL https://raw.githubusercontent.com/Scottcjn/Rustchain/main/install-miner.sh | bash

# Install with specific wallet
curl -sSL https://raw.githubusercontent.com/Scottcjn/Rustchain/main/install-miner.sh | bash -s -- --wallet my-miner-wallet

# Preview actions (dry-run)
bash install-miner.sh --dry-run --wallet my-miner-wallet
```

**The installer:**
- ✅ Auto-detects your platform (Linux/macOS, x86_64/ARM/PowerPC)
- ✅ Creates an isolated Python virtualenv (no system pollution)
- ✅ Downloads the correct miner for your hardware
- ✅ Sets up auto-start on boot (systemd/launchd)
- ✅ Provides easy uninstall

### Manual Installation

#### Linux

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip python3-venv curl git

# Clone repository
git clone https://github.com/Scottcjn/Rustchain.git
cd Rustchain

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install RustChain
pip install -e .

# Check hardware profile
python3 tools/setup_validator.py --hardware-profile

# Register as validator
python3 tools/setup_validator.py --register

# Start validator
python3 tools/setup_validator.py --start
```

#### macOS

```bash
# Install Homebrew (if needed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.10

# Clone and install
git clone https://github.com/Scottcjn/Rustchain.git
cd Rustchain
pip3 install -e .

# Register and start
python3 tools/setup_validator.py --register
python3 tools/setup_validator.py --start
```

#### Windows

```powershell
# Install Python from https://python.org
# Ensure "Add to PATH" is checked

# Clone repository
git clone https://github.com/Scottcjn/Rustchain.git
cd Rustchain

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate

# Install RustChain
pip install -e .

# Register validator
python tools\setup_validator.py --register

# Start validator
python tools\setup_validator.py --start
```

### Docker Installation

```bash
# Pull Docker image
docker pull scottcjn/rustchain:latest

# Run validator
docker run -d \
  --name rustchain-validator \
  -p 9333:9333 \
  -p 9332:9332 \
  -v $HOME/.rustchain:/root/.rustchain \
  --restart unless-stopped \
  scottcjn/rustchain:latest
```

---

## Configuration

### Validator Configuration File

Location: `~/.rustchain/validator.json`

```json
{
  "validator_id": "RTC_abc123...",
  "wallet_address": "RTCdef456...",
  "hardware_profile": {
    "cpu_model": "PowerMac G4",
    "release_year": 2003,
    "tier": "vintage",
    "multiplier": 2.5
  },
  "entropy_fingerprint": "sha256_hash...",
  "antiquity_score": 23.5,
  "bootstrap_nodes": [
    "192.168.0.160:9333",
    "192.168.0.125:9333"
  ],
  "api_port": 9332,
  "p2p_port": 9333,
  "registered_at": 1709251200
}
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `RUSTCHAIN_HOME` | Data directory | `~/.rustchain` |
| `RUSTCHAIN_NETWORK` | Network (mainnet/testnet) | `mainnet` |
| `RUSTCHAIN_LOG_LEVEL` | Logging verbosity | `INFO` |
| `RUSTCHAIN_WALLET` | Wallet name | Auto-generated |

### Advanced Configuration

Edit `~/.rustchain/config.toml`:

```toml
[network]
p2p_port = 9333
api_port = 9332
max_peers = 50
bootstrap_nodes = [
  "192.168.0.160:9333",
  "192.168.0.125:9333"
]

[validator]
wallet = "my-validator-wallet"
auto_start = true
log_level = "INFO"

[hardware]
skip_fingerprint_check = false  # NEVER set to true in production
allow_vm = false                # VMs receive minimal rewards
```

---

## Maintenance

### Daily Operations

**Check validator status:**

```bash
# Linux (systemd)
systemctl --user status rustchain-miner

# macOS (launchd)
launchctl list | grep rustchain

# Check logs
journalctl --user -u rustchain-miner -f  # Linux
tail -f ~/.rustchain/miner.log          # macOS
```

**Check wallet balance:**

```bash
curl -sk "https://rustchain.org/wallet/balance?miner_id=YOUR_WALLET_NAME"
```

**Check node health:**

```bash
curl -sk https://rustchain.org/health
curl -sk https://rustchain.org/epoch
```

### Weekly Tasks

1. **Review logs** for errors or warnings
2. **Check for updates**:
   ```bash
   git pull origin main
   pip install --upgrade clawrtc
   ```
3. **Verify hardware attestation** is still valid
4. **Monitor uptime** and network connectivity

### Monthly Tasks

1. **Backup configuration:**
   ```bash
   cp -r ~/.rustchain ~/.rustchain.backup.$(date +%Y%m)
   ```
2. **Review reward earnings** and multipliers
3. **Check governance proposals** (if holding >10 RTC)
4. **Update system packages**

### Updating RustChain

```bash
# Stop validator
systemctl --user stop rustchain-miner  # Linux
launchctl stop com.rustchain.miner     # macOS

# Update software
cd ~/Rustchain
git pull origin main
pip install -e . --upgrade

# Restart validator
systemctl --user start rustchain-miner  # Linux
launchctl start com.rustchain.miner     # macOS

# Verify operation
curl -sk https://rustchain.org/health
```

---

## Troubleshooting

### Common Issues

#### "Could not reach network"

**Symptoms:** `clawrtc wallet show` fails

**Solution:**
```bash
# Verify node connectivity
curl -sk https://rustchain.org/health
curl -sk "https://rustchain.org/wallet/balance?miner_id=YOUR_WALLET"

# Check firewall
sudo ufw status
sudo firewall-cmd --list-all
```

#### "Hardware fingerprint check failed"

**Symptoms:** Validator cannot submit attestations

**Solution:**
1. Ensure you're running on **real hardware** (not VM)
2. Check system time is synchronized:
   ```bash
   timedatectl status  # Linux
   sntp -s time.apple.com  # macOS
   ```
3. Re-run hardware attestation:
   ```bash
   clawrtc attest --force
   ```

#### "Miner exits immediately"

**Symptoms:** Service starts then stops

**Solution:**
```bash
# Check if wallet exists
ls -la ~/.rustchain/validator.json

# Verify service status
systemctl --user status rustchain-miner

# View detailed logs
journalctl --user -u rustchain-miner -n 50
```

#### "HTTPS certificate errors"

**Symptoms:** curl/wget SSL errors

**Solution:**
```bash
# Test connectivity first
curl -I https://rustchain.org

# Use -sk flags for self-signed certs
curl -sk https://rustchain.org/health

# Update CA certificates
sudo update-ca-certificates  # Debian/Ubuntu
sudo trust extract-compat    # Fedora
```

#### Low rewards / wrong multiplier

**Symptoms:** Receiving less than expected

**Solution:**
1. Check hardware tier:
   ```bash
   python3 tools/setup_validator.py --hardware-profile
   ```
2. Verify hardware is not detected as VM
3. Ensure uptime is consistent (affects antiquity score)
4. Check for multiplier decay (15%/year for very old hardware)

### Getting Help

- **Documentation:** https://github.com/Scottcjn/Rustchain/tree/main/docs
- **Discord:** https://discord.gg/VqVVS2CW9Q
- **GitHub Issues:** https://github.com/Scottcjn/Rustchain/issues
- **Block Explorer:** https://rustchain.org/explorer

---

## Security Considerations

### Best Practices

1. **Never share your private keys or wallet seed**
2. **Use a dedicated machine** for validation when possible
3. **Enable firewall** and only open required ports
4. **Regular backups** of `~/.rustchain/` directory
5. **Monitor for unauthorized access** in logs
6. **Keep system updated** with security patches

### Anti-Sybil Protection

RustChain prevents multiple wallets on same hardware through:

- Hardware fingerprint binding to wallet
- Unique silicon aging patterns
- Cross-node attestation verification
- Economic disincentives for emulation

---

## Performance Optimization

### For Vintage Hardware

1. **Use lightweight OS** (Ubuntu Server, Alpine Linux)
2. **Minimize background processes**
3. **Use wired Ethernet** over WiFi when possible
4. **Configure swap** if RAM <1GB:
   ```bash
   sudo fallocate -l 2G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

### For Modern Hardware

1. **Enable multiple peer connections** (up to 100)
2. **Run as public node** to support network
3. **Consider running backup node** for redundancy
4. **Monitor network metrics** with Grafana dashboard

---

## Compliance & Legal

### Regulatory Position

RustChain validators should be aware of:

- **Tax implications** of mining rewards in your jurisdiction
- **KYC/AML requirements** for cryptocurrency operations
- **Local regulations** on cryptocurrency mining
- **Reporting requirements** for income from validation

See [docs/US_REGULATORY_POSITION.md](docs/US_REGULATORY_POSITION.md) for detailed guidance.

### License

RustChain validator software is released under the **MIT License**.

---

## Appendix A: Hardware Entropy Sources

Available entropy sources by platform:

| Platform | Entropy Sources |
|----------|----------------|
| **Linux x86_64** | /dev/urandom, /proc/cpuinfo, thermal, DMI |
| **Linux POWER8** | /dev/urandom, mftb, thermal, DMI |
| **macOS Intel** | /dev/urandom, sysctl, thermal |
| **macOS PowerPC** | /dev/urandom, AltiVec, timebase |
| **Windows** | CryptGenRandom, CPUID, thermal |

---

## Appendix B: Reward Calculation

**Formula:**
```
Reward = Base_Reward × Hardware_Multiplier × (1 - Decay_Factor)

Where:
- Base_Reward = 0.12 RTC per epoch
- Hardware_Multiplier = 1.0 to 3.0 (based on tier)
- Decay_Factor = 0.15 × (age - threshold) for ancient hardware
```

**Example Calculation:**

PowerPC G4 (2003, 23 years old):
```
Base Reward: 0.12 RTC
Multiplier: 2.5× (Vintage tier)
Decay: 0% (under 30 years)

Final Reward: 0.12 × 2.5 = 0.30 RTC per epoch
Daily: 0.30 × 144 epochs = 43.2 RTC/day
Monthly: 43.2 × 30 = 1,296 RTC/month (~$129.60 USD)
```

---

## Appendix C: Network Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    RustChain Network                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │ Validator│◄──►│ Validator│◄──►│ Validator│              │
│  │   Node 1 │    │   Node 2 │    │   Node 3 │              │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘              │
│       │               │               │                     │
│       └───────────────┼───────────────┘                     │
│                       │                                     │
│              ┌────────▼────────┐                            │
│              │  Bootstrap Node │                            │
│              │  (Sophia Prime) │                            │
│              └────────┬────────┘                            │
│                       │                                     │
│              ┌────────▼────────┐                            │
│              │  Ergo Anchor    │                            │
│              │  (R4 Register)  │                            │
│              └─────────────────┘                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Epoch Flow:**
1. Validators collect hardware entropy
2. Submit `proof_of_antiquity.json` with signatures
3. Cross-node verification (2/3 consensus)
4. Rewards distributed based on antiquity score
5. State anchored to Ergo blockchain

---

**Last Updated:** March 2026  
**Version:** 1.0.0  
**Maintained by:** RustChain Core Team
