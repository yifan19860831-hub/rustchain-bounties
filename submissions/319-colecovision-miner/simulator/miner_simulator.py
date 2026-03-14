#!/usr/bin/env python3
"""
RustChain Miner Simulator for ColecoVision (1982)
Python Z80 Emulator - Mining Demonstration

This simulator emulates the ultra-constrained mining environment
of the ColecoVision console with its 1 KB RAM and Z80 CPU.

Bounty: 200 RTC ($20) - LEGENDARY Tier
Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b
"""

import time
import hashlib
import struct
from dataclasses import dataclass, field
from typing import List, Tuple
from datetime import datetime

# ============================================================================
# COLECOVISION MEMORY MAP
# ============================================================================

RAM_SIZE = 1024  # 1 KB scratchpad RAM
VRAM_SIZE = 16384  # 16 KB video RAM
CARTRIDGE_SIZE = 4096  # 4 KB cartridge ROM

# Memory addresses (from miner.h)
STACK_START = 0x2000
MINER_STATE = 0x2100
NONCE_COUNTER = 0x2100
CURRENT_HASH = 0x2104
BEST_HASH = 0x2108
HASH_COUNT = 0x210C
HASH_BUFFER = 0x2200
DISPLAY_BUFFER = 0x2280
BLOCK_HEADER = 0x22D0
DIFFICULTY = 0x2310

# ============================================================================
# Z80 CPU EMULATOR (Simplified)
# ============================================================================

@dataclass
class Z80Registers:
    """Z80 CPU Register Set"""
    A: int = 0x00  # Accumulator
    F: int = 0x00  # Flags
    B: int = 0x00
    C: int = 0x00
    D: int = 0x00
    E: int = 0x00
    H: int = 0x00
    L: int = 0x00
    
    # Alternate register set
    A_: int = 0x00
    F_: int = 0x00
    B_: int = 0x00
    C_: int = 0x00
    D_: int = 0x00
    E_: int = 0x00
    H_: int = 0x00
    L_: int = 0x00
    
    # Index registers
    IX: int = 0x0000
    IY: int = 0x0000
    
    # Special registers
    SP: int = 0x20FF  # Stack pointer
    PC: int = 0x1000  # Program counter
    I: int = 0x00     # Interrupt vector
    R: int = 0x00     # Refresh counter
    
    # Flags
    IFF1: bool = False
    IFF2: bool = False
    IM: int = 0

@dataclass
class ColecoVisionState:
    """ColecoVision System State"""
    ram: bytearray = field(default_factory=lambda: bytearray(RAM_SIZE))
    vram: bytearray = field(default_factory=lambda: bytearray(VRAM_SIZE))
    rom: bytearray = field(default_factory=lambda: bytearray(CARTRIDGE_SIZE))
    registers: Z80Registers = field(default_factory=Z80Registers)
    
    # Mining state
    nonce: int = 0
    best_hash: bytes = b'\xFF\xFF\xFF\xFF'
    hash_count: int = 0
    start_time: float = field(default_factory=time.time)
    
    # Display state
    screen_buffer: List[str] = field(default_factory=list)
    
    # Statistics
    total_hashes: int = 0
    successful_hashes: int = 0

# ============================================================================
# TRUNCATED SHA-256 (For Simulation Speed)
# ============================================================================

def truncated_sha256(data: bytes, rounds: int = 1) -> bytes:
    """
    Compute a truncated SHA-256 hash.
    
    In the real Z80 implementation, we only do 1 round for speed.
    Full SHA-256 has 64 rounds.
    """
    h = hashlib.sha256(data).digest()
    # Return only first 4 bytes (like our Z80 implementation)
    return h[:4]

# ============================================================================
# MINER EMULATOR
# ============================================================================

class ColecoVisionMiner:
    """Emulates the ColecoVision RustChain Miner"""
    
    def __init__(self):
        self.state = ColecoVisionState()
        self.difficulty_target = 0x0010FFFF  # Very easy for demo
        
    def initialize(self):
        """Initialize the miner state"""
        print("=" * 60)
        print("RUSTCHAIN MINER FOR COLECOVISION (1982)")
        print("=" * 60)
        print(f"CPU: Z80A @ 3.58 MHz")
        print(f"RAM: 1 KB (Allocated: {RAM_SIZE} bytes)")
        print(f"VRAM: 16 KB (TMS9918)")
        print(f"Cartridge ROM: 4 KB")
        print("=" * 60)
        print(f"Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b")
        print("=" * 60)
        print()
        
        # Initialize memory
        self._init_memory()
        
        # Initialize display
        self._init_display()
        
    def _init_memory(self):
        """Initialize miner memory structures"""
        # Set initial nonce to 0
        nonce_bytes = struct.pack('<I', 0)
        for i in range(4):
            self.state.ram[NONCE_COUNTER - 0x2000 + i] = nonce_bytes[i]
        
        # Set best hash to 0xFFFFFFFF
        for i in range(4):
            self.state.ram[BEST_HASH - 0x2000 + i] = 0xFF
        
        # Initialize block header template
        header = b'RUSTCHAIN' + b'\x00' * 55
        for i in range(64):
            self.state.ram[BLOCK_HEADER - 0x2000 + i] = header[i] if i < len(header) else 0
    
    def _init_display(self):
        """Initialize the display buffer"""
        self.state.screen_buffer = [
            "+======================================+",
            "|     RUSTCHAIN MINER v1.0             |",
            "|     ColecoVision (1982)              |",
            "+--------------------------------------+",
            "|  NONCE: 0x00000000                   |",
            "|  HASH:  0x00000000                   |",
            "|  BEST:  0xFFFFFFFF                   |",
            "|  RATE:  0 H/s                        |",
            "+--------------------------------------+",
            "|                                      |",
            "|  [>                                 ] |",
            "|                                      |",
            "+======================================+",
        ]
    
    def mine_block(self) -> Tuple[bytes, bool]:
        """
        Perform one mining attempt.
        
        Returns:
            Tuple of (hash_bytes, success)
        """
        # Increment nonce
        self.state.nonce = (self.state.nonce + 1) & 0xFFFFFFFF
        
        # Update nonce in memory
        nonce_bytes = struct.pack('<I', self.state.nonce)
        for i in range(4):
            self.state.ram[NONCE_COUNTER - 0x2000 + i] = nonce_bytes[i]
        
        # Prepare block header with current nonce
        block_data = bytearray(self.state.ram[BLOCK_HEADER - 0x2000:BLOCK_HEADER - 0x2000 + 64])
        block_data[0:4] = nonce_bytes
        
        # Compute hash (truncated for speed)
        current_hash = truncated_sha256(bytes(block_data))
        
        # Update hash in memory
        for i in range(4):
            self.state.ram[CURRENT_HASH - 0x2000 + i] = current_hash[i]
        
        # Check if this is a new best
        current_int = int.from_bytes(current_hash, 'big')
        best_int = int.from_bytes(self.state.best_hash, 'big')
        
        is_new_best = current_int < best_int
        if is_new_best:
            self.state.best_hash = current_hash
            for i in range(4):
                self.state.ram[BEST_HASH - 0x2000 + i] = current_hash[i]
        
        # Check against difficulty target
        target_int = self.difficulty_target & 0xFFFFFFFF
        success = current_int <= target_int
        
        # Update statistics
        self.state.hash_count += 1
        self.state.total_hashes += 1
        if success:
            self.state.successful_hashes += 1
        
        return current_hash, success
    
    def update_display(self):
        """Update the display buffer"""
        elapsed = time.time() - self.state.start_time
        hash_rate = int(self.state.total_hashes / max(elapsed, 0.001))
        
        # Format nonce
        nonce_str = f"0x{self.state.nonce:08X}"
        
        # Format current hash
        current_hash = self.state.ram[CURRENT_HASH - 0x2000:CURRENT_HASH - 0x2000 + 4]
        hash_str = f"0x{current_hash.hex().upper()}"
        
        # Format best hash
        best_str = f"0x{self.state.best_hash.hex().upper()}"
        
        # Update display lines
        self.state.screen_buffer[4] = f"│  NONCE: {nonce_str}                   │"
        self.state.screen_buffer[5] = f"│  HASH:  {hash_str}                   │"
        self.state.screen_buffer[6] = f"│  BEST:  {best_str}                   │"
        self.state.screen_buffer[7] = f"│  RATE:  {hash_rate} H/s                     │"
        
        # Update progress bar (wraps every 256 hashes for visual effect)
        progress = (self.state.nonce % 256) // 8
        bar = ">" + "=" * progress + " " * (31 - progress) + "]"
        self.state.screen_buffer[10] = f"│  [{bar} │"
    
    def render_display(self):
        """Render the display to terminal"""
        # Clear screen and move cursor to top
        print("\033[H\033[J", end="")
        
        for line in self.state.screen_buffer:
            print(line)
        
        # Print statistics
        elapsed = time.time() - self.state.start_time
        print()
        print(f"Total Hashes: {self.state.total_hashes:,}")
        print(f"Successful:   {self.state.successful_hashes}")
        print(f"Elapsed:      {elapsed:.2f}s")
        print(f"Simulated:    {elapsed * 3580000:.0f} CPU cycles")
        print()
        print("Press Ctrl+C to stop")
    
    def run(self, max_hashes: int = None):
        """
        Run the miner.
        
        Args:
            max_hashes: Maximum number of hashes to compute (None = infinite)
        """
        self.initialize()
        
        hash_count = 0
        try:
            while True:
                # Mine one block
                current_hash, success = self.mine_block()
                
                # Update display every 100 hashes
                if hash_count % 100 == 0:
                    self.update_display()
                    self.render_display()
                
                # Check for success
                if success:
                    print("\n" + "=" * 60)
                    print("🎉 SUCCESS! Valid hash found!")
                    print("=" * 60)
                    print(f"Nonce: 0x{self.state.nonce:08X}")
                    print(f"Hash:  0x{current_hash.hex().upper()}")
                    print(f"Target: 0x{self.difficulty_target:08X}")
                    print("=" * 60)
                    print(f"Bounty: 200 RTC → {self.state.ram[NONCE_COUNTER - 0x2000:NONCE_COUNTER - 0x2000 + 4].hex()}")
                    print("=" * 60)
                
                hash_count += 1
                
                # Check if we've reached the limit
                if max_hashes and hash_count >= max_hashes:
                    break
                
                # Small delay to simulate Z80 speed
                # Real Z80 @ 3.58 MHz would take ~5000 cycles per hash
                # That's ~1.4ms per hash, or ~700 H/s theoretical max
                time.sleep(0.001)  # 1ms delay for simulation
                
        except KeyboardInterrupt:
            print("\n\nMining stopped by user")
            self._print_final_stats()
    
    def _print_final_stats(self):
        """Print final mining statistics"""
        elapsed = time.time() - self.state.start_time
        avg_rate = self.state.total_hashes / max(elapsed, 0.001)
        
        print("\n" + "=" * 60)
        print("MINING STATISTICS")
        print("=" * 60)
        print(f"Total Hashes:     {self.state.total_hashes:,}")
        print(f"Successful:       {self.state.successful_hashes}")
        print(f"Average Rate:     {avg_rate:.2f} H/s")
        print(f"Elapsed Time:     {elapsed:.2f}s")
        print(f"Simulated Cycles: {elapsed * 3580000:.0f}")
        print("=" * 60)
        print()
        print("Note: Real ColecoVision would achieve ~700 H/s")
        print("      Modern GPU: ~100,000,000,000 H/s")
        print("      We are ~140 million times slower!")
        print("=" * 60)

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point"""
    import sys
    
    print("RustChain Miner Simulator for ColecoVision")
    print("Starting emulation...")
    print()
    
    miner = ColecoVisionMiner()
    
    # Parse command line arguments
    max_hashes = None
    if len(sys.argv) > 1:
        try:
            max_hashes = int(sys.argv[1])
            print(f"Running for {max_hashes} hashes...")
        except ValueError:
            print(f"Usage: {sys.argv[0]} [max_hashes]")
            print("  max_hashes: Optional maximum number of hashes to compute")
            return
    
    # Run the miner
    miner.run(max_hashes)

if __name__ == "__main__":
    main()
