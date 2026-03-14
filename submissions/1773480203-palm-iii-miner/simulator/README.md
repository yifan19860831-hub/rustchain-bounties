# Palm III Miner Simulator

Quick test of the Palm III miner without real hardware!

## Requirements

- Python 3.7+
- No external dependencies

## Quick Start

```bash
# Generate wallet
python palm_miner.py --generate

# Run interactive UI
python palm_miner.py

# Run background mining (1 hour)
python palm_miner.py --background 3600

# Check status
python palm_miner.py --status
```

## Commands (Interactive Mode)

| Command | Description |
|---------|-------------|
| `m` | Toggle mining |
| `s` | Show status |
| `w` | Show wallet |
| `d` | Show display |
| `q` | Quit |

## Output Example

```
============================================================
RustChain Palm III Miner Simulator
DragonBall EZ @ 16 MHz Emulation
============================================================

[OK] Loaded wallet: RTC4a7b3c9d2e1f...

Controls:
  m - Toggle mining
  s - Show status
  w - Show wallet
  d - Show display
  q - Quit
============================================================

Command> s

=== Status ===
Wallet: RTC4a7b3c9d2e1f...
Attestations: 0
Mining: False
Last attest: Never
```

## Files Generated

- `palm_wallet.json` - Your wallet (BACKUP THIS!)
- `palm_attestations.db` - Attestation storage

## What It Simulates

1. **DragonBall Hardware**
   - RTC registers
   - Timer tick jitter
   - RAM power-on patterns

2. **Palm OS Behavior**
   - Event loop
   - Display (160×160 text mode)
   - Database storage

3. **Mining Process**
   - Entropy collection
   - Attestation creation
   - Wallet generation

## Limitations

- Text-based display (not graphical)
- Simplified hashing
- No network submission
- Simulated timing (not real 16 MHz)

For real Palm OS deployment, compile `MinerMain.c` with CodeWarrior!

---

**Wallet for Bounty:** `RTC4325af95d26d59c3ef025963656d22af638bb96b`
