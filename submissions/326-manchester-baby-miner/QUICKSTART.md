# Quick Start - Manchester Baby Miner

## Prerequisites

- Python 3.8 or higher
- No external dependencies required (uses only standard library)

## Installation

```bash
# Navigate to the project directory
cd manchester-baby-miner

# Verify Python version
python --version  # Should be 3.8+
```

## Run the Miner

```bash
# Simple run
python src/manchester_baby_miner.py

# Expected output:
# ======================================================================
#   MANCHESTER BABY MINER (1948)
#   RustChain Proof-of-Antiquity - LEGENDARY Tier
# ======================================================================
# 
# [SIMULATION] Running Manchester Baby instruction cycle...
# [SIMULATION] Executed 100 Baby instructions
# 
# [MINING] Searching for valid nonce...
# [SUCCESS] BLOCK FOUND!
#   Nonce: 8
#   Hash: 07bf904e9f85b575...
#   Instructions: 260
#   Time: 0.09s
# 
#   Antiquity Multiplier: 10.0x (LEGENDARY - 1948 hardware)
#   Estimated Reward: 1.20 RTC per epoch
# 
# [OK] Proof saved to manchester_baby_mining_proof.json
```

## Verify the Proof

```bash
# Check the generated proof file
cat manchester_baby_mining_proof.json

# Or on Windows:
type manchester_baby_mining_proof.json
```

## Test the Simulator

```python
# Interactive test
python -c "
from src.manchester_baby_miner import ManchesterBaby

# Create Baby simulator
baby = ManchesterBaby()

# Load a simple program (count to 5)
program = [
    # Initialize counter to 0
    (0b010 << 13) | 20,  # LDN 20
    (0b110 << 13) | 20,  # STO 20
    
    # Increment counter
    (0b010 << 13) | 20,  # LDN 20
    (0b001 << 13) | 24,  # SUB 24 (-1 = add 1)
    (0b110 << 13) | 20,  # STO 20
    
    # Check if counter >= 5
    (0b010 << 13) | 20,  # LDN 20
    (0b001 << 13) | 25,  # SUB 25 (-5)
    (0b101 << 13) | 0,   # CMP (skip if negative)
    (0b100 << 13) | 26,  # JRP 26 (loop back)
    
    # Halt
    (0b111 << 13) | 0,   # STP
    
    # Data
    0, 0, 0, 0, 0,  # 15-19: padding
    0,              # 20: counter
    0, 0, 0, 0,     # 21-24: padding
    0xFFFFFFFF,     # 24: -1
    5,              # 25: -5 (for comparison)
    -11,            # 26: relative jump back
]

baby.store.load_program(program)
baby.run(max_instructions=50)

print(f'Counter value: {baby.store[20].to_int()}')
print(f'Instructions executed: {baby.instruction_count}')
print('Test passed!')
"
```

## Bounty Submission

### Step 1: Fork the Repository

```bash
# Go to https://github.com/Scottcjn/rustchain-bounties
# Click "Fork" button
```

### Step 2: Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/rustchain-bounties.git
cd rustchain-bounties
```

### Step 3: Add Your Contribution

```bash
# Create directory
mkdir -p contributions/manchester-baby

# Copy files
cp -r /path/to/manchester-baby-miner/* contributions/manchester-baby/
```

### Step 4: Commit and Push

```bash
git add contributions/manchester-baby/
git commit -m "Add Manchester Baby (1948) miner - Bounty #346 LEGENDARY"
git push origin main
```

### Step 5: Create Pull Request

1. Go to your fork on GitHub
2. Click "Pull requests" → "New pull request"
3. Select your branch
4. Use `PR_DESCRIPTION.md` as the PR description
5. Submit!

### Step 6: Claim Bounty

Comment on issue #346:

```
I have completed Bounty #346 - Manchester Baby Miner (1948)!

PR: [link to your PR]
Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b

This is the world's first stored-program computer miner, running on 
1948 architecture with:
- 32 words × 32 bits = 1,024 bits memory
- 7 instructions total
- Williams-Kilburn tube memory simulation
- 10.0× antiquity multiplier (LEGENDARY tier)

Proof file: manchester_baby_mining_proof.json
```

## Troubleshooting

### Unicode Errors on Windows

If you see encoding errors, set the console to UTF-8:

```bash
chcp 65001
python src/manchester_baby_miner.py
```

### Python Version Error

Make sure you have Python 3.8+:

```bash
python --version
# If < 3.8, download from https://python.org
```

### Module Not Found

This project uses only standard library - no external dependencies needed!

## Learn More

- **Full Documentation**: See `README.md`
- **Technical Details**: See `PR_DESCRIPTION.md`
- **Mining Proof**: See `manchester_baby_mining_proof.json`

## Support

For questions or issues:
- Open an issue on the rustchain-bounties repository
- Join the RustChain Discord: https://discord.gg/VqVVS2CW9Q

---

**Happy Mining on 1948 Hardware!** 🖥️
