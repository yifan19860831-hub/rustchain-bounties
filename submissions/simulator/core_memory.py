#!/usr/bin/env python3
"""
IBM 703 Stretch Magnetic-Core Memory Emulator

Emulates the 8-way interleaved magnetic-core memory system:
- 16,384 to 262,144 words × 64 bits
- 2.18 μs access time
- 8 banks for concurrent access
- Non-destructive read

Author: RustChain Bounty Hunter
License: MIT
"""

import time
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class CoreMemoryBank:
    """Single magnetic-core memory bank"""
    bank_id: int
    words: List[int]
    capacity: int
    access_time_us: float = 2.18
    
    # Statistics
    read_count: int = 0
    write_count: int = 0
    last_access_time: float = 0
    
    def read(self, offset: int) -> int:
        """Read word from core memory (non-destructive)"""
        self.read_count += 1
        self.last_access_time = time.time()
        return self.words[offset]
    
    def write(self, offset: int, value: int):
        """Write word to core memory (destructive write)"""
        self.write_count += 1
        self.last_access_time = time.time()
        self.words[offset] = value & 0xFFFFFFFFFFFFFFFF  # 64-bit mask


class InterleavedCoreMemory:
    """
    IBM 703 8-way interleaved magnetic-core memory
    
    Memory is divided into 8 banks for concurrent access:
    - Bank 0: Words 0, 8, 16, 24, ...
    - Bank 1: Words 1, 9, 17, 25, ...
    - Bank 2: Words 2, 10, 18, 26, ...
    - ...
    - Bank 7: Words 7, 15, 23, 31, ...
    
    This allows up to 8 memory accesses per 2.18 μs cycle!
    """
    
    def __init__(self, total_words: int = 16384, num_banks: int = 8):
        self.num_banks = num_banks
        self.words_per_bank = total_words // num_banks
        self.total_words = total_words
        
        # Create memory banks
        self.banks = [
            CoreMemoryBank(
                bank_id=i,
                words=[0] * self.words_per_bank,
                capacity=self.words_per_bank
            )
            for i in range(num_banks)
        ]
        
        # Statistics
        self.concurrent_accesses = 0
        self.total_accesses = 0
    
    def _get_bank_and_offset(self, address: int) -> Tuple[int, int]:
        """Calculate bank index and offset for given address"""
        bank_idx = address % self.num_banks
        offset = address // self.num_banks
        return bank_idx, offset
    
    def read(self, address: int) -> int:
        """Read from memory"""
        bank_idx, offset = self._get_bank_and_offset(address)
        self.total_accesses += 1
        return self.banks[bank_idx].read(offset)
    
    def write(self, address: int, value: int):
        """Write to memory"""
        bank_idx, offset = self._get_bank_and_offset(address)
        self.total_accesses += 1
        self.banks[bank_idx].write(offset, value)
    
    def read_concurrent(self, addresses: List[int]) -> List[int]:
        """
        Read multiple addresses concurrently (if in different banks)
        
        This is the key performance feature of interleaved memory!
        """
        # Group addresses by bank
        bank_requests = {}
        for addr in addresses:
            bank_idx, offset = self._get_bank_and_offset(addr)
            if bank_idx not in bank_requests:
                bank_requests[bank_idx] = []
            bank_requests[bank_idx].append((offset, addr))
        
        # Check for bank conflicts
        num_concurrent = len(bank_requests)
        if num_concurrent == len(addresses):
            self.concurrent_accesses += 1  # All accesses concurrent!
        
        # Execute reads
        results = {}
        for bank_idx, requests in bank_requests.items():
            for offset, addr in requests:
                results[addr] = self.banks[bank_idx].read(offset)
                self.total_accesses += 1
        
        # Return in original order
        return [results[addr] for addr in addresses]
    
    def write_concurrent(self, address_value_pairs: List[Tuple[int, int]]):
        """
        Write to multiple addresses concurrently (if in different banks)
        """
        # Group by bank
        bank_requests = {}
        for addr, value in address_value_pairs:
            bank_idx, offset = self._get_bank_and_offset(addr)
            if bank_idx not in bank_requests:
                bank_requests[bank_idx] = []
            bank_requests[bank_idx].append((offset, value))
        
        # Check for bank conflicts
        num_concurrent = len(bank_requests)
        if num_concurrent == len(address_value_pairs):
            self.concurrent_accesses += 1
        
        # Execute writes
        for bank_idx, requests in bank_requests.items():
            for offset, value in requests:
                self.banks[bank_idx].write(offset, value)
                self.total_accesses += 1
    
    def get_statistics(self) -> dict:
        """Get memory statistics"""
        total_reads = sum(b.read_count for b in self.banks)
        total_writes = sum(b.write_count for b in self.banks)
        
        return {
            'total_words': self.total_words,
            'num_banks': self.num_banks,
            'words_per_bank': self.words_per_bank,
            'total_accesses': self.total_accesses,
            'concurrent_accesses': self.concurrent_accesses,
            'total_reads': total_reads,
            'total_writes': total_writes,
            'bank_stats': [
                {
                    'bank_id': b.bank_id,
                    'reads': b.read_count,
                    'writes': b.write_count,
                }
                for b in self.banks
            ]
        }
    
    def dump(self, start: int = 0, count: int = 64):
        """Dump memory contents"""
        print(f"\nMemory Dump (words {start} to {start+count-1}):")
        print("-" * 80)
        
        for i in range(0, count, 4):
            addr = start + i
            words = []
            for j in range(4):
                word = self.read(addr + j)
                words.append(f"{word:016X}")
            
            print(f"{addr:05X}: {'  '.join(words)}")
        
        print("-" * 80)
    
    def print_statistics(self):
        """Print memory statistics"""
        stats = self.get_statistics()
        
        print("\n" + "="*60)
        print("IBM 703 Core Memory Statistics")
        print("="*60)
        print(f"Total Capacity: {stats['total_words']:,} words ({stats['total_words'] * 8:,} bytes)")
        print(f"Memory Banks: {stats['num_banks']} (interleaved)")
        print(f"Words per Bank: {stats['words_per_bank']:,}")
        print(f"\nAccess Statistics:")
        print(f"  Total Accesses: {stats['total_accesses']:,}")
        print(f"  Concurrent Accesses: {stats['concurrent_accesses']:,}")
        print(f"  Read Operations: {stats['total_reads']:,}")
        print(f"  Write Operations: {stats['total_writes']:,}")
        
        if stats['total_accesses'] > 0:
            concurrency_rate = stats['concurrent_accesses'] / stats['total_accesses'] * 100
            print(f"  Concurrency Rate: {concurrency_rate:.2f}%")
        
        print(f"\nPer-Bank Statistics:")
        for bank in stats['bank_stats']:
            print(f"  Bank {bank['bank_id']}: {bank['reads']:,} reads, {bank['writes']:,} writes")
        
        print("="*60 + "\n")


def demo():
    """Demonstrate interleaved memory"""
    print("\n" + "="*60)
    print("IBM 703 Stretch Magnetic-Core Memory Demo")
    print("="*60)
    
    # Create 16K word memory (8 banks × 2K words)
    memory = InterleavedCoreMemory(total_words=16384, num_banks=8)
    
    # Sequential access pattern
    print("\n1. Sequential Access Test:")
    for i in range(100):
        memory.write(i, i * 0x1111111111111111)
    
    for i in range(10):
        val = memory.read(i)
        print(f"  Word {i}: {val:016X}")
    
    # Concurrent access pattern (optimal for interleaved memory)
    print("\n2. Concurrent Access Test (8 addresses, different banks):")
    addresses = [0, 1, 2, 3, 4, 5, 6, 7]  # All different banks!
    values = [0xAAAAAAAAAAAAAAAA, 0xBBBBBBBBBBBBBBBB, 0xCCCCCCCCCCCCCCCC,
              0xDDDDDDDDDDDDDDDD, 0xEEEEEEEEEEEEEEEE, 0xFFFFFFFFFFFFFFFF,
              0x0000000000000000, 0x1234567890ABCDEF]
    
    # Write concurrently
    memory.write_concurrent(list(zip(addresses, values)))
    print(f"  Wrote 8 words concurrently to addresses {addresses}")
    
    # Read concurrently
    results = memory.read_concurrent(addresses)
    print(f"  Read 8 words concurrently:")
    for addr, val in zip(addresses, results):
        print(f"    Address {addr}: {val:016X}")
    
    # Bank conflict test (suboptimal)
    print("\n3. Bank Conflict Test (8 addresses, same bank):")
    addresses_conflict = [0, 8, 16, 24, 32, 40, 48, 56]  # All bank 0!
    print(f"  Addresses {addresses_conflict} all map to Bank 0")
    results_conflict = memory.read_concurrent(addresses_conflict)
    print(f"  (These accesses must be serialized)")
    
    # Print statistics
    memory.print_statistics()


if __name__ == '__main__':
    demo()
