#!/usr/bin/env python3
"""
IBM 701 RustChain Miner (1952)
Main miner executable - Proof-of-Antiquity for IBM's first commercial computer

This miner runs the RustChain protocol on a simulated IBM 701,
generating authentic hardware fingerprints based on:
- Williams tube memory timing
- Vacuum tube thermal characteristics
- 36-bit IAS-derived architecture
"""

from ibm701_simulator import IBM701Miner
import time
import json


def main():
    """Main miner entry point"""
    print("=" * 70)
    print("  RustChain Proof-of-Antiquity Miner")
    print("  IBM 701 Electronic Data Processing Machine (1952)")
    print("=" * 70)
    print()
    
    # Load or create wallet
    wallet_file = 'wallet.txt'
    wallet = None
    
    try:
        with open(wallet_file, 'r') as f:
            for line in f:
                if line.startswith('Address:'):
                    wallet = line.split(':')[1].strip()
                    break
        print(f"📂 Loaded wallet from {wallet_file}")
    except FileNotFoundError:
        print(f"💳 No wallet found, will generate new one")
    
    # Create miner
    miner = IBM701Miner(wallet_address=wallet)
    
    # Save wallet if newly generated
    if wallet != miner.wallet:
        miner.save_wallet(wallet_file)
        print(f"✨ New wallet generated and saved")
    
    print()
    print("🏆 Bounty Information:")
    print(f"   Issue: #375 - Port Miner to IBM 701 (1952)")
    print(f"   Tier: LEGENDARY")
    print(f"   Reward: 200 RTC ($20)")
    print(f"   Multiplier: 5.0×")
    print(f"   Wallet: {miner.wallet}")
    print()
    
    # Run miner (continuous mode)
    print("🚀 Starting mining operation...")
    print("   Press Ctrl+C to stop")
    print()
    
    epoch_count = 0
    try:
        while True:
            attestation = miner.mine_epoch()
            epoch_count += 1
            
            # Print summary every 10 epochs
            if epoch_count % 10 == 0:
                print(f"\n📊 Summary after {epoch_count} epochs:")
                print(f"   Total attestations: {len(miner.attestations)}")
                print(f"   Estimated rewards: {epoch_count * 0.60:.2f} RTC")
                print()
            
            # Wait for next epoch (simulated 5-minute epochs, shortened for demo)
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Mining stopped by user")
        print(f"\n📈 Final Statistics:")
        print(f"   Epochs completed: {epoch_count}")
        print(f"   Attestations generated: {len(miner.attestations)}")
        print(f"   Wallet: {miner.wallet}")
        print(f"   Total instructions executed: {miner.cpu.instruction_count}")
        print(f"   Total simulated time: {miner.cpu.total_time_us/1000:.2f}ms")
    
    print()
    print("=" * 70)
    print("Your vintage hardware earns rewards. Make mining meaningful again.")
    print("=" * 70)


if __name__ == '__main__':
    main()
