# 🎮 Simon (1978) Miner - Badge Only Implementation

[![RustChain](https://img.shields.io/badge/RustChain-Proof%20of%20Antiquity-blue)](https://rustchain.org)
[![Hardware](https://img.shields.io/badge/Hardware-TMS%201000%204--bit-orange)](https://en.wikipedia.org/wiki/Texas_Instruments_TMS1000)
[![Bounty](https://img.shields.io/badge/Bounty-%23467%20LEGENDARY-red)](https://github.com/Scottcjn/rustchain-bounties)

Port of RustChain miner to the **Simon (1978)** electronic game - one of the most constrained hardware targets ever attempted for blockchain mining.

## 🏆 Bounty Information

- **Issue:** [#467](https://github.com/Scottcjn/rustchain-bounties/issues/467)
- **Tier:** LEGENDARY
- **Reward:** 200 RTC ($20 USD)
- **Wallet:** `RTC4325af95d26d59c3ef025963656d22af638bb96b`

## 📋 Overview

Simon is a classic electronic memory game from 1978, featuring:
- **CPU:** Texas Instruments TMS 1000 (4-bit)
- **RAM:** ~182 bytes
- **ROM:** 256 bytes
- **I/O:** 4 colored buttons + 4 LEDs + piezo speaker

This implementation uses a **Badge Only** approach since the hardware is fundamentally incapable of actual blockchain mining (no network, no crypto, insufficient memory).

## 🎯 Badge Details

```json
{
  "badge_id": "simon_1978_pioneer",
  "name": "🎮 Simon Memory Pioneer",
  "description": "First miner to attest via Simon (1978) electronic game",
  "rarity": "MYTHIC",
  "requirement": "Complete attestation using Simon game sequence as proof"
}
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- `requests` library (optional, falls back to urllib)

```bash
pip install requests
```

### Run Simulation

```bash
# Run 3 game simulations and submit attestations
python simon_miner.py --games 3

# Simulation only (no network submission)
python simon_miner.py --simulate-only --games 5

# Custom sequence mode
python simon_miner.py --sequence "0,1,2,3,1,0,3,2"

# Custom wallet
python simon_miner.py --wallet YOUR_WALLET_ADDRESS
```

### Example Output

```
╔═══════════════════════════════════════════════════════════╗
║           🎮 Simon (1978) Miner - Badge Only 🎮           ║
║                                                           ║
║  Texas Instruments TMS 1000 Emulation                     ║
║  4-bit CPU • 182 bytes RAM • 4 Colors                     ║
║                                                           ║
║  Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b     ║
║  Bounty: #467 - LEGENDARY Tier (200 RTC / $20)           ║
╚═══════════════════════════════════════════════════════════╝

🎮 Simon (1978) Miner Simulation
   Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b
   Games: 3

--- Game 1 ---
  Simon shows: GREEN
  Player inputs: GREEN ✓
  Simon shows: RED
  Player inputs: RED ✓
  ...
  Level reached: 5
  Score: 15
  Sequence hash: a3f2b8c9d1e4f567

📡 Submitting attestations to RustChain...
Submitting attestation 1/3...
  ✅ Success! Status: 200

==================================================
📊 Summary:
   Games played: 3
   Attestations submitted: 3
   Successful: 3/3
   Badge ID: simon_1978_pioneer
   Hardware: Simon (1978) / TMS 1000
==================================================
```

## 📁 Project Structure

```
simon_miner/
├── simon_miner.py         # Main miner implementation
├── ARCHITECTURE.md        # Detailed architecture documentation
├── README.md              # This file
└── tests/
    └── test_simon.py      # Unit tests
```

## 🏗️ Architecture

### Components

1. **TMS1000Emulator** - Texas Instruments TMS 1000 CPU emulation
   - 4-bit Harvard architecture
   - 10 opcodes
   - ROM/RAM emulation
   - I/O port simulation

2. **SimonGame** - Simon game logic
   - Sequence generation
   - Player input validation
   - Game state management
   - Score tracking

3. **AttestationEncoder** - Encode game state as RustChain attestation
   - Sequence hashing
   - Metadata encoding
   - Badge ID assignment

4. **RustChainClient** - RustChain node API client
   - Health checking
   - Attestation submission
   - Error handling

### Attestation Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Simon Game  │────▶│  Attestation │────▶│  RustChain   │
│  (Emulated)  │     │  Encoder     │     │  Node        │
└──────────────┘     └──────────────┘     └──────────────┘
      │                    │                    │
      │ Game sequence      │ JSON payload       │ Badge awarded
      │ + metadata         │ + signature        │ to wallet
```

## 🎮 Simon Color Mapping

| Color  | Position      | Value | Tone  | Frequency |
|--------|---------------|-------|-------|-----------|
| Green  | Upper Left    | 0     | E3    | 164.81 Hz |
| Red    | Upper Right   | 1     | A3    | 220.00 Hz |
| Yellow | Lower Left    | 2     | C#4   | 277.18 Hz |
| Blue   | Lower Right   | 3     | E4    | 329.63 Hz |

## 🔧 API Reference

### SimonMiner Class

```python
from simon_miner import SimonMiner

# Create miner instance
miner = SimonMiner(
    wallet="RTC4325af95d26d59c3ef025963656d22af638bb96b",
    node_url="https://rustchain.org"
)

# Run simulation only
attestations = miner.run_simulation(num_games=5)

# Submit attestations
results = miner.submit_attestations(attestations)

# Full cycle (simulate + submit)
success = miner.run_full_cycle(num_games=3)
```

### SimonGame Class

```python
from simon_miner import SimonGame

game = SimonGame()
game.new_game()

# Show sequence
while True:
    color = game.show_next_in_sequence()
    if color is None:
        break
    print(f"Simon shows: {color}")

# Player input
correct, continuing = game.player_input(color)
```

## 🧪 Testing

```bash
# Run unit tests
python -m pytest tests/

# Test TMS 1000 emulation
python -c "from simon_miner import TMS1000Emulator; e = TMS1000Emulator(); print(f'Cycles: {e.run(100)}')"

# Test Simon game logic
python -c "from simon_miner import SimonGame; g = SimonGame(); g.new_game(); print(f'Level: {g.state.game_level}')"
```

## 📝 Attestation Schema

```json
{
  "timestamp": "2026-03-14T12:34:56Z",
  "wallet": "RTC4325af95d26d59c3ef025963656d22af638bb96b",
  "game_level": 5,
  "sequence_length": 5,
  "sequence_hash": "a3f2b8c9d1e4f567",
  "score": 15,
  "hardware": "Simon (1978) Electronic Game",
  "hardware_type": "TMS1000_4bit",
  "badge_id": "simon_1978_pioneer"
}
```

## 🚨 Limitations

This is a **Badge Only** implementation due to:

1. **No Network:** Simon has no network interface
2. **No Crypto:** TMS 1000 cannot compute SHA-256/Ed25519
3. **Memory:** 182 bytes RAM insufficient for blockchain state
4. **4-bit CPU:** Cannot perform 32/64-bit arithmetic

The Python simulator acts as a bridge between the emulated hardware and RustChain.

## 📚 References

- [Simon (game) - Wikipedia](https://en.wikipedia.org/wiki/Simon_(game))
- [TMS 1000 - Wikipedia](https://en.wikipedia.org/wiki/Texas_Instruments_TMS1000)
- [US Patent 4,207,087](https://patents.google.com/patent/US4207087)
- [RustChain Documentation](https://rustchain.org)
- [ARCHITECTURE.md](./ARCHITECTURE.md) - Detailed technical documentation

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] More accurate TMS 1000 timing emulation
- [ ] Audio tone generation (pygame)
- [ ] Visual Simon interface (tkinter)
- [ ] Hardware interface (Arduino bridge)
- [ ] Additional badge tiers

## 📄 License

MIT License - Same as RustChain

## 💰 Bounty Claim

To claim the bounty:

1. Fork the RustChain repository
2. Add this `simon_miner/` directory to `miners/simon/`
3. Create a PR with the wallet address in the description
4. Tag issue #467

**Wallet:** `RTC4325af95d26d59c3ef025963656d22af638bb96b`

---

**Made with 🎮 for RustChain Bounty #467**
**Date:** 2026-03-14
