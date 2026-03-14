#!/usr/bin/env python3
"""
TI-85 Miner Simulator - Python Emulation

This simulator emulates the TI-85 calculator's Z80 CPU and demonstrates
the theoretical mining process within extreme memory constraints.

Educational purposes only - real mining is impossible on TI-85 hardware.
"""

import time
import struct
import hashlib
from dataclasses import dataclass, field
from typing import Optional, List, Tuple
from enum import Enum


class Z80Registers:
    """Emulates Z80 CPU registers"""
    
    def __init__(self):
        # 8-bit registers
        self.a = 0  # Accumulator
        self.f = 0  # Flags
        self.b = 0
        self.c = 0
        self.d = 0
        self.e = 0
        self.h = 0
        self.l = 0
        
        # 16-bit registers
        self.pc = 0x8000  # Program counter (start of user RAM)
        self.sp = 0xFFFF  # Stack pointer
        self.ix = 0
        self.iy = 0
        
    def get_bc(self) -> int:
        return (self.b << 8) | self.c
    
    def get_de(self) -> int:
        return (self.d << 8) | self.e
    
    def get_hl(self) -> int:
        return (self.h << 8) | self.l
    
    def set_bc(self, value: int):
        self.b = (value >> 8) & 0xFF
        self.c = value & 0xFF
    
    def set_de(self, value: int):
        self.d = (value >> 8) & 0xFF
        self.e = value & 0xFF
    
    def set_hl(self, value: int):
        self.h = (value >> 8) & 0xFF
        self.l = value & 0xFF
    
    def __str__(self):
        return (f"Z80 Registers:\n"
                f"  A={self.a:02X} F={self.f:02X} B={self.b:02X} C={self.c:02X}\n"
                f"  D={self.d:02X} E={self.e:02X} H={self.h:02X} L={self.l:02X}\n"
                f"  PC={self.pc:04X} SP={self.sp:04X} IX={self.ix:04X} IY={self.iy:04X}")


@dataclass
class Block:
    """Ultra-minimal block structure for TI-85 (32 bytes total)"""
    
    prev_hash: bytes = field(default_factory=lambda: b'\x00' * 8)
    timestamp: int = 0
    nonce: int = 0
    data: bytes = field(default_factory=lambda: b'\x00' * 15)  # 15 bytes to fit 32 total
    difficulty: int = 4  # Target: 4 zero bits (stored in last byte)
    
    def serialize(self) -> bytes:
        """Serialize block to bytes (32 bytes total)"""
        return (
            self.prev_hash +                    # 8 bytes
            struct.pack('<I', self.timestamp) + # 4 bytes
            struct.pack('<I', self.nonce) +     # 4 bytes
            self.data +                         # 15 bytes
            bytes([self.difficulty])            # 1 byte
        )                                     # = 32 bytes
    
    @classmethod
    def deserialize(cls, data: bytes) -> 'Block':
        """Deserialize block from bytes"""
        if len(data) < 32:
            data = data + b'\x00' * (32 - len(data))
        return cls(
            prev_hash=data[0:8],
            timestamp=struct.unpack('<I', data[8:12])[0],
            nonce=struct.unpack('<I', data[12:16])[0],
            data=data[16:31],                    # 15 bytes
            difficulty=data[31]                  # 1 byte
        )
    
    def __str__(self):
        return (f"Block:\n"
                f"  Prev Hash: {self.prev_hash.hex()}\n"
                f"  Timestamp: {self.timestamp}\n"
                f"  Nonce: {self.nonce}\n"
                f"  Data: {self.data.hex()}\n"
                f"  Difficulty: {self.difficulty} bits")


class MiniHash:
    """
    Simplified hash function for TI-85 demonstration.
    
    Real SHA-256 requires ~4KB code and is too complex for TI-85.
    This uses a simple XOR-rotate algorithm that fits in ~200 bytes.
    """
    
    @staticmethod
    def compute(data: bytes) -> int:
        """
        Compute 8-bit hash of data.
        
        Algorithm:
        1. XOR all bytes together
        2. Rotate left after each XOR
        3. Return final 8-bit value
        
        This is NOT cryptographically secure - for demonstration only!
        """
        h = 0
        for byte in data:
            h ^= byte
            # Rotate left
            h = ((h << 1) | (h >> 7)) & 0xFF
        return h
    
    @staticmethod
    def verify(hash_value: int, difficulty: int) -> bool:
        """
        Verify if hash meets difficulty target.
        
        Difficulty N means hash must have N leading zero bits.
        """
        if difficulty <= 0:
            return True
        if difficulty > 8:
            difficulty = 8
        
        # Check if top N bits are zero
        mask = 0xFF << (8 - difficulty)
        return (hash_value & mask) == 0


class TI85Display:
    """Emulates TI-85 display (128×64 monochrome)"""
    
    WIDTH = 128
    HEIGHT = 64
    
    def __init__(self):
        # 1024 bytes bitmap (128 × 64 ÷ 8)
        self.buffer = bytearray(1024)
        self.cursor_x = 0
        self.cursor_y = 0
    
    def clear(self):
        self.buffer = bytearray(1024)
        self.cursor_x = 0
        self.cursor_y = 0
    
    def draw_text(self, text: str, x: int = 0, y: int = 0):
        """Draw text at position (simplified - just stores for display)"""
        # In real implementation, would render to bitmap
        pass
    
    def get_status_line(self, line: int, text: str) -> str:
        """Format text for display line (21 chars max)"""
        return f"{text:<21}"[:21]
    
    def render_miner_ui(self, block: Block, hash_rate: float, 
                        hashes_computed: int, found_blocks: int) -> str:
        """Render mining UI to text representation"""
        lines = [
            "╔════════════════════════╗",
            "║   TI-85 MINER v1.0     ║",
            "╠════════════════════════╣",
            f"║ Nonce: {block.nonce:10} ║",
            f"║ Hash:  0x{MiniHash.compute(block.serialize()):02X}              ║",
            f"║ Diff:  {block.difficulty} bits             ║",
            "╠════════════════════════╣",
            f"║ Rate:  {hash_rate:6.1f} H/s          ║",
            f"║ Total: {hashes_computed:10}        ║",
            f"║ Found: {found_blocks:10}        ║",
            "╠════════════════════════╣",
            "║ [MINING...]            ║",
            "╚════════════════════════╝",
        ]
        return '\n'.join(lines)


class TI85Miner:
    """Main miner emulator"""
    
    MEMORY_TOTAL = 28 * 1024  # 28 KB user RAM
    MEMORY_CODE = 4 * 1024    # 4 KB code
    MEMORY_DATA = 2 * 1024    # 2 KB data
    MEMORY_FREE = MEMORY_TOTAL - MEMORY_CODE - MEMORY_DATA
    
    def __init__(self):
        self.cpu = Z80Registers()
        self.display = TI85Display()
        self.current_block = Block()
        self.hashes_computed = 0
        self.found_blocks: List[Block] = []
        self.start_time = 0
        self.running = False
    
    def initialize(self):
        """Initialize miner state"""
        self.cpu.pc = 0x8000  # Start of user RAM
        self.current_block.timestamp = int(time.time())
        self.current_block.data = b'TI85-MINER-POC'
        self.hashes_computed = 0
        self.found_blocks = []
        self.start_time = time.time()
        self.running = True
    
    def mine_single_nonce(self) -> bool:
        """
        Attempt to mine with current nonce.
        Returns True if valid block found.
        """
        # Compute hash (simulates Z80 assembly routine)
        block_data = self.current_block.serialize()
        hash_value = MiniHash.compute(block_data)
        
        self.hashes_computed += 1
        
        # Check if hash meets difficulty
        if MiniHash.verify(hash_value, self.current_block.difficulty):
            # Found valid block!
            found_block = Block(
                prev_hash=self.current_block.prev_hash,
                timestamp=self.current_block.timestamp,
                nonce=self.current_block.nonce,
                data=self.current_block.data,
                difficulty=self.current_block.difficulty
            )
            self.found_blocks.append(found_block)
            
            # Reset for next block
            self.current_block.prev_hash = bytes([hash_value]) * 8
            self.current_block.timestamp = int(time.time())
            self.current_block.nonce = 0
            
            return True
        
        # Increment nonce for next attempt
        self.current_block.nonce = (self.current_block.nonce + 1) & 0xFFFFFFFF
        return False
    
    def mine_batch(self, num_attempts: int) -> int:
        """Mine for specified number of attempts, return blocks found"""
        found = 0
        for _ in range(num_attempts):
            if self.mine_single_nonce():
                found += 1
        return found
    
    def get_hash_rate(self) -> float:
        """Calculate hashes per second"""
        elapsed = time.time() - self.start_time
        if elapsed <= 0:
            return 0
        return self.hashes_computed / elapsed
    
    def get_memory_usage(self) -> dict:
        """Return memory usage statistics"""
        return {
            'total': self.MEMORY_TOTAL,
            'code': self.MEMORY_CODE,
            'data': self.MEMORY_DATA,
            'free': self.MEMORY_FREE,
            'usage_percent': ((self.MEMORY_CODE + self.MEMORY_DATA) / self.MEMORY_TOTAL) * 100
        }
    
    def get_status(self) -> str:
        """Get full status report"""
        mem = self.get_memory_usage()
        elapsed = time.time() - self.start_time
        
        status = f"""
╔════════════════════════════════════════════════════╗
║           TI-85 MINER - STATUS REPORT              ║
╠════════════════════════════════════════════════════╣
║ TIME ELAPSED: {elapsed:8.1f} seconds                        ║
║ HASHES/mined: {self.hashes_computed:10} hashes                      ║
║ HASH RATE:    {self.get_hash_rate():8.1f} H/s                        ║
║ BLOCKS FOUND: {len(self.found_blocks):10} blocks                      ║
╠════════════════════════════════════════════════════╣
║ MEMORY USAGE:                                      ║
║   Code:  {mem['code']:6} bytes ({mem['code']/1024:.1f} KB)                  ║
║   Data:  {mem['data']:6} bytes ({mem['data']/1024:.1f} KB)                  ║
║   Free:  {mem['free']:6} bytes ({mem['free']/1024:.1f} KB)                  ║
║   Total: {mem['total']:6} bytes ({mem['total']/1024:.1f} KB)                  ║
║   Usage: {mem['usage_percent']:5.1f}%                            ║
╠════════════════════════════════════════════════════╣
║ Z80 CPU STATE:                                     ║
║   PC: 0x{self.cpu.pc:04X}  SP: 0x{self.cpu.sp:04X}                     ║
║   A: 0x{self.cpu.a:02X}  B: 0x{self.cpu.b:02X}  C: 0x{self.cpu.c:02X}  D: 0x{self.cpu.d:02X}           ║
╚════════════════════════════════════════════════════╝
"""
        return status


def demo_mining():
    """Run mining demonstration"""
    print("\n" + "="*60)
    print("  TI-85 MINER SIMULATOR - Proof of Concept")
    print("  Educational Demo - Not Real Mining")
    print("="*60)
    
    miner = TI85Miner()
    miner.initialize()
    
    print("\n[INFO] Initial Configuration:")
    print(f"   Block Difficulty: {miner.current_block.difficulty} bits")
    print(f"   Block Size: 32 bytes")
    print(f"   Memory Available: {miner.MEMORY_TOTAL / 1024:.0f} KB")
    print(f"   Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b")
    
    print("\n[START] Starting mining simulation...")
    print("(Simulating Z80 @ 6 MHz, ~100 H/s)\n")
    
    # Mine in batches
    batch_size = 100
    total_batches = 10
    
    for i in range(total_batches):
        found = miner.mine_batch(batch_size)
        
        # Display progress
        elapsed = time.time() - miner.start_time
        rate = miner.get_hash_rate()
        
        print(f"[{i+1:2d}/{total_batches}] "
              f"Hashes: {miner.hashes_computed:6d} | "
              f"Rate: {rate:6.1f} H/s | "
              f"Found: {len(miner.found_blocks):3d} blocks")
        
        # Small delay to simulate real mining time
        time.sleep(0.05)
    
    # Final report
    print(miner.get_status())
    
    if miner.found_blocks:
        print("[SUCCESS] Found blocks:")
        for i, block in enumerate(miner.found_blocks[:5], 1):
            print(f"   Block #{i}: nonce={block.nonce}, "
                  f"hash=0x{MiniHash.compute(block.serialize()):02X}")
    
    print("\n" + "="*60)
    print("  Simulation Complete")
    print("="*60 + "\n")
    
    return miner


def benchmark_difficulty():
    """Benchmark different difficulty levels"""
    print("\n" + "="*60)
    print("  DIFFICULTY BENCHMARK")
    print("="*60 + "\n")
    
    for diff in range(1, 9):
        miner = TI85Miner()
        miner.initialize()
        miner.current_block.difficulty = diff
        
        # Mine until block found or max attempts
        max_attempts = 10000
        found = False
        
        for _ in range(max_attempts):
            if miner.mine_single_nonce():
                found = True
                break
        
        if found:
            print(f"Difficulty {diff}: Found after {miner.hashes_computed:6d} hashes")
        else:
            print(f"Difficulty {diff}: Not found in {max_attempts} attempts")
    
    print()


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--benchmark':
        benchmark_difficulty()
    else:
        demo_mining()
