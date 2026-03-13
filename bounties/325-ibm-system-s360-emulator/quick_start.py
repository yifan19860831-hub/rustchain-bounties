#!/usr/bin/env python3
"""
Quick start script for RustChain IBM System/360 Model 30 Miner
==============================================================

Run this to quickly start mining with default settings.

Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b
"""

import sys
from pathlib import Path

# Import miner
sys.path.insert(0, str(Path(__file__).parent))
from s360_miner import S360Miner

def main():
    """Quick start miner"""
    print("\n" + "=" * 70)
    print("RustChain IBM System/360 Model 30 Miner - Quick Start")
    print("=" * 70)
    print()
    
    # Create miner with bounty wallet
    miner = S360Miner(
        wallet="RTC4325af95d26d59c3ef025963656d22af638bb96b"
    )
    
    print("\nStarting mining in 3 seconds... (Ctrl+C to stop)")
    import time
    time.sleep(3)
    
    # Run miner (demo mode: 3 epochs)
    print("\nRunning demo mode (3 epochs)...")
    miner.run(max_epochs=3)
    
    print("\n" + "=" * 70)
    print("Demo complete!")
    print("To run full mining: python s360_miner.py")
    print("=" * 70)

if __name__ == "__main__":
    main()
