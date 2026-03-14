#!/usr/bin/env python3
"""
Altair 8800 Mining Simulator - Standalone Version
=================================================================
Simple demonstration of mining on the first personal computer.
Does not require the full CPU emulator.

Run: python miner_sim.py
"""

import time


class Altair8800Miner:
    """
    Simplified mining simulation for Altair 8800.
    Demonstrates the concept without full CPU emulation.
    """
    
    def __init__(self, target_difficulty: int = 0x10):
        self.target_difficulty = target_difficulty
        self.nonce = 0
        self.hashes_computed = 0
    
    def compute_hash(self, nonce: int) -> int:
        """
        Simplified hash computation (XOR-based for 8080).
        Real SHA-256 is not feasible on 8-bit CPU.
        """
        # Simulate XOR of nonce with block header pattern
        header_pattern = 0xAA
        hash_value = header_pattern ^ ((nonce >> 8) & 0xFF) ^ (nonce & 0xFF)
        return hash_value & 0xFF
    
    def check_target(self, hash_value: int) -> bool:
        """Check if hash meets difficulty target."""
        return hash_value < self.target_difficulty
    
    def mine(self, max_nonces: int = 10000):
        """Run mining simulation."""
        print("\n" + "="*60)
        print("ALT AIR 8800 MINING SIMULATOR")
        print("="*60)
        print("First Personal Computer (1975)")
        print("Intel 8080 @ 2 MHz | 64 KB RAM | S-100 Bus")
        print("="*60)
        print(f"\nTarget difficulty: 0x{self.target_difficulty:02X} ({self.target_difficulty})")
        print(f"Max nonces to try: {max_nonces}")
        print("\nStarting mining...\n")
        
        start_time = time.time()
        
        for self.nonce in range(max_nonces):
            # Compute hash
            hash_value = self.compute_hash(self.nonce)
            self.hashes_computed += 1
            
            # Check if we found a valid proof
            if self.check_target(hash_value):
                elapsed = time.time() - start_time
                
                print(f"[SUCCESS] Mining complete!")
                print(f"{'='*60}")
                print(f"Nonce found:       {self.nonce}")
                print(f"Hash value:        0x{hash_value:02X} ({hash_value})")
                print(f"Target:            0x{self.target_difficulty:02X} ({self.target_difficulty})")
                print(f"Hashes computed:   {self.hashes_computed}")
                print(f"Time elapsed:      {elapsed:.6f} seconds")
                print(f"\nAltair 8800 Specifications:")
                print(f"  - CPU: Intel 8080 @ 2 MHz")
                print(f"  - Architecture: 8-bit")
                print(f"  - Memory: 64 KB max")
                print(f"  - Bus: S-100")
                print(f"  - Input: Front panel switches")
                print(f"  - Output: LEDs")
                print(f"\nRustChain Wallet:")
                print(f"  RTC4325af95d26d59c3ef025963656d22af638bb96b")
                print(f"{'='*60}\n")
                return self.nonce
            
            # Progress indicator
            if self.nonce % 500 == 0 and self.nonce > 0:
                print(f"  [Mining] Nonce: {self.nonce:5d}, Best hash: 0x{hash_value:02X}")
        
        elapsed = time.time() - start_time
        print(f"\n[Timeout] No valid nonce found in {max_nonces} attempts")
        print(f"Time elapsed: {elapsed:.6f} seconds")
        return None


def main():
    """Main entry point."""
    # Create miner with target difficulty 0x10 (1 in 16 chance)
    miner = Altair8800Miner(target_difficulty=0x10)
    result = miner.mine(max_nonces=10000)
    
    if result is not None:
        print("[OK] Mining simulation completed successfully!")
        return 0
    else:
        print("[ERROR] Mining simulation failed to find nonce")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
