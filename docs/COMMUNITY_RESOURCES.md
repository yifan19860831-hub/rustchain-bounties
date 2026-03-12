# RustChain Community Resources List

> 🦎  curated collection of RustChain community links, tools, and documentation  
> Last updated: March 12, 2026

---

## 🌐 Official Links

| Resource | URL | Description |
|----------|-----|-------------|
| **Official Website** | https://rustchain.org | Main website with mining info, tokenomics, and documentation |
| **Main Repository** | https://github.com/Scottcjn/Rustchain | Core RustChain blockchain implementation |
| **Bounty Program** | https://github.com/Scottcjn/rustchain-bounties | Earn RTC for contributions |
| **Discord Community** | https://discord.gg/VqVVS2CW9Q | Official Discord server |

---

## 📦 Core Projects

### Blockchain & Mining

| Project | URL | Stars | Description |
|---------|-----|-------|-------------|
| **Rustchain** | https://github.com/Scottcjn/Rustchain | 156 ⭐ | Proof-of-Antiquity blockchain — vintage PowerPC hardware earns 2.5x mining rewards |
| **RustChain Monitor** | https://github.com/Scottcjn/rustchain-monitor | 41 ⭐ | Network monitoring dashboard |
| **RustChain MCP** | https://github.com/Scottcjn/rustchain-mcp | 3 ⭐ | Model Context Protocol integration |

### AI Agent Ecosystem

| Project | URL | Stars | Description |
|---------|-----|-------|-------------|
| **BoTTube** | https://github.com/Scottcjn/bottube | 123 ⭐ | AI video platform with agent integration |
| **Beacon Skill** | https://github.com/Scottcjn/beacon-skill | 86 ⭐ | Agent-to-agent protocol for social coordination and RTC payments |
| **Grazer Skill** | https://github.com/Scottcjn/grazer-skill | 60 ⭐ | Agent discovery crawler |
| **RAM Coffers** | https://github.com/Scottcjn/ram-coffers | 58 ⭐ | NUMA weight banking for LLM inference |

### Infrastructure & Tools

| Project | URL | Stars | Description |
|---------|-----|-------|-------------|
| **AMD ROCm POWER8** | https://github.com/Scottcjn/amd-rocm-power8-patches | 42 ⭐ | ROCm stack for AMD GPUs on IBM POWER8 |
| **Argon2 POWER8** | https://github.com/Scottcjn/argon2-power8 | 34 ⭐ | Optimized Argon2 password hash for POWER8 |
| **llama.cpp POWER8** | https://github.com/Scottcjn/llama-cpp-power8 | 41 ⭐ | POWER8-optimized LLM inference |

### Awesome Lists

| Project | URL | Stars | Description |
|---------|-----|-------|-------------|
| **Awesome Agents** | https://github.com/Scottcjn/awesome-agents | 38 ⭐ | Curated list of AI agent platforms, frameworks, protocols, tools |
| **Awesome AI Agents** | https://github.com/Scottcjn/awesome-ai-agents | 36 ⭐ | List of AI autonomous agents |
| **Awesome Agentic Patterns** | https://github.com/Scottcjn/awesome-agentic-patterns | 33 ⭐ | Catalogue of agentic AI patterns |

---

## 📚 Documentation & Research

### Official Documentation

- **Mining Guide**: https://rustchain.org/#how-to-start-mining
- **Proof of Antiquity**: https://rustchain.org/#proof-of-antiquity-consensus
- **Tokenomics**: https://rustchain.org/#tokenomics
- **Beacon Protocol**: https://rustchain.org/#beacon-protocol

### Research Papers (Zenodo DOI)

| Paper | DOI | Key Result |
|-------|-----|------------|
| **RustChain: One CPU, One Vote** | [10.5281/zenodo.18623592](https://doi.org/10.5281/zenodo.18623592) | 6-layer fingerprint, 0% VM bypass rate |
| **Non-Bijunctive Permutation Collapse** | [10.5281/zenodo.18623920](https://doi.org/10.5281/zenodo.18623920) | AltiVec vec_perm: 1 cycle vs 27-96 on x86/ARM |
| **PSE Hardware Entropy** | [10.5281/zenodo.18623922](https://doi.org/10.5281/zenodo.18623922) | Provable non-determinism, 0.2% overhead |
| **Neuromorphic Prompt Translation** | [10.5281/zenodo.18623594](https://doi.org/10.5281/zenodo.18623594) | Emotional prompts = 20% video diffusion gains |
| **RAM Coffers** | [10.5281/zenodo.18321905](https://doi.org/10.5281/zenodo.18321905) | NUMA weight banking, 147 t/s (8.81x speedup) |

---

## 🛠️ Developer Tools

### Installation

```bash
# Via PIP
pip install clawrtc
clawrtc install --wallet YOUR_WALLET_ID
clawrtc start

# Via NPM
npm install -g clawrtc
clawrtc install --wallet YOUR_WALLET_ID
clawrtc start

# Beacon Protocol
pip install beacon-skill
# With mnemonic seed phrase support
pip install "beacon-skill[mnemonic]"
```

### Mining Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | Any | Vintage (pre-2010) |
| **RAM** | 32 MB+ | 1 GB+ |
| **Network** | Internet | Stable connection |
| **OS** | Linux/macOS/Windows/*BSD | Linux |
| **Python** | 2.3+ / 3.6+ | 3.8+ |

### Supported Architectures

| Architecture | Devices | Base Multiplier |
|--------------|---------|-----------------|
| **68K / Amiga** | 68000, Quadra, SE/30, A500 | 3.0x |
| **x86 Ultra-Retro** | 386, 486, Pentium I/II/III | 3.0x |
| **SPARC** | SPARCstation, UltraSPARC | 2.9x |
| **PowerPC** | G3, G4, G5, POWER8 | 2.5x |
| **DEC Alpha / PA-RISC** | Alpha 21x64, HP PA-RISC | 2.9x |
| **x86_64 Vintage** | Core 2, Nehalem, Sandy | 1.3x |
| **Apple Silicon** | M1, M2, M3 | 1.2x |

---

## 💰 Token & DeFi

### Token Details

| Property | Value |
|----------|-------|
| **Token** | RTC (RustChain Token) |
| **Total Supply** | 8,300,000 RTC |
| **Epoch Reward** | 1.5 RTC / 10 min |
| **Reference Rate** | $0.10 USD / RTC |

### Wrapped RTC (Solana)

| Property | Value |
|----------|-------|
| **Token** | wRTC (Wrapped RustChain Token) |
| **Chain** | Solana |
| **Mint** | `12TAdKXxcGf6oCv4rqDz2NkgxjHq6HQKoxKZYGf5i4X` |
| **Bridge** | https://bottube.ai/bridge |

### Distribution

- **Mining Rewards**: 70% (5,810,000 RTC)
- **Community Fund**: 15% (1,245,000 RTC)
- **Development**: 8% (664,000 RTC)
- **Team/Bounties**: 7% (581,000 RTC)

---

## 🎁 Bounty Program

Earn RTC by contributing to the network!

| Contribution | Reward |
|--------------|--------|
| **Bug Report** | 10-25 RTC |
| **Feature PR** | 50-100 RTC |
| **Security Audit** | 100-150 RTC |
| **Critical Vuln** | Up to 200 RTC |
| **Easy Tasks** | 1-5 RTC |

**Current Bounties**: https://github.com/Scottcjn/rustchain-bounties/issues

---

## 🤝 Community Platforms

### Social & Communication

- **Discord**: https://discord.gg/VqVVS2CW9Q - Main community hub
- **Beacon Protocol**: Agent-to-agent communication with RTC payments
- **BoTTube**: AI video platform with social features
- **Moltbook**: Social platform integration (via Beacon)

### Beacon Agent Setup

```bash
# Create your agent identity
beacon init
beacon identity new

# Send a hello beacon on LAN
beacon udp send 255.255.255.255 38400 \
  --broadcast --envelope-kind hello \
  --text "Any agents online?"

# Listen for beacons
beacon udp listen --port 38400
```

---

## 📖 Additional Resources

### Ecosystem Overview

```
/opt/rustchain/ecosystem/
├── bottube/          # AI video platform
├── beacon-skill/     # Agent-to-agent protocol
├── grazer-skill/     # Agent discovery crawler
├── wrtc-bridge/      # RTC ↔ wRTC Solana bridge
├── raydium-pool/     # wRTC/SOL liquidity
├── x402-payments/    # Machine-to-machine payments
└── agent-wallets/    # Coinbase Base wallets
```

### Key Concepts

- **Proof of Antiquity (PoA)**: 1 CPU = 1 Vote with hardware fingerprinting
- **Tenure Multipliers**: +5% per year, capped at +50% after 10 years
- **Anti-VM Fingerprinting**: 7-point system prevents VM farms
- **Beacon Protocol**: Agent identity, 5 transports, RTC payments built-in

---

## 📝 Contributing

This resource list is community-maintained. To add or update entries:

1. Fork the repository
2. Edit this file
3. Submit a PR to https://github.com/Scottcjn/rustchain-bounties

**Questions?** Join the Discord: https://discord.gg/VqVVS2CW9Q

---

*Built with 🦎 by the RustChain Community*
