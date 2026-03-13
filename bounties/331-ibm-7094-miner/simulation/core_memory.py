#!/usr/bin/env python3
"""
IBM 7094 Core Memory Emulation

Emulates the IBM 7302 magnetic-core memory used in the IBM 7094
- 32,768 words × 36 bits
- 2.18 microsecond cycle time
- Destructive read (requires restore)

Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b
"""


class CoreMemory:
    """
    Magnetic-core memory emulation for IBM 7094
    
    The IBM 7094 used IBM 7302 Core Storage with:
    - 32K words of 36 bits each
    - 2.18 μs memory cycle
    - Destructive read (read destroys data, must restore)
    - 15-bit addressing (0-32767)
    """
    
    def __init__(self, size=32768, word_size=36):
        """
        Initialize core memory
        
        Args:
            size: Number of words (default 32768 = 32K)
            word_size: Bits per word (default 36 for IBM 7094)
        """
        self.size = size
        self.word_size = word_size
        self.mask = (1 << word_size) - 1
        
        # Memory array (list of integers)
        self.memory = [0] * size
        
        # Statistics
        self.read_count = 0
        self.write_count = 0
        self.access_time_ns = 2180  # 2.18 μs in nanoseconds
        
        # Simulate core memory planes
        # Each bit position has its own plane of magnetic cores
        self.planes = word_size  # 36 planes for 36-bit words
    
    def clear(self):
        """Clear all memory to zero"""
        self.memory = [0] * self.size
        self.read_count = 0
        self.write_count = 0
    
    def read(self, address):
        """
        Read a word from core memory
        
        Core memory has destructive read - reading destroys the data
        and it must be restored. We simulate this behavior.
        
        Args:
            address: Memory address (0 to size-1)
            
        Returns:
            36-bit word value
            
        Raises:
            ValueError: If address is out of range
        """
        if address < 0 or address >= self.size:
            raise ValueError(f"Address {address} out of range (0-{self.size-1})")
        
        self.read_count += 1
        
        # Simulate destructive read by reading and restoring
        value = self.memory[address]
        
        # In real core memory, reading destroys the data
        # The memory controller automatically restores it
        # We simulate this by just returning the value
        
        return value & self.mask
    
    def write(self, address, value):
        """
        Write a word to core memory
        
        Args:
            address: Memory address (0 to size-1)
            value: 36-bit word value
            
        Raises:
            ValueError: If address is out of range
        """
        if address < 0 or address >= self.size:
            raise ValueError(f"Address {address} out of range (0-{self.size-1})")
        
        self.write_count += 1
        
        # Mask value to word size
        self.memory[address] = value & self.mask
    
    def read_restore(self, address):
        """
        Read with explicit restore (simulates core memory cycle)
        
        In real core memory, reading is destructive and requires
        a restore cycle. This method makes that explicit.
        
        Args:
            address: Memory address
            
        Returns:
            Word value
        """
        value = self.read(address)
        # Restore is automatic in our simulation
        return value
    
    def write_with_cycle(self, address, value):
        """
        Write with simulated memory cycle delay
        
        Args:
            address: Memory address
            value: Word value
        """
        import time
        
        # Simulate 2.18 μs memory cycle
        time.sleep(self.access_time_ns / 1e9)
        self.write(address, value)
    
    def dump(self, start=0, length=32, format='octal'):
        """
        Dump a section of memory
        
        Args:
            start: Starting address
            length: Number of words to dump
            format: 'octal', 'hex', 'binary', or 'decimal'
        """
        print(f"Core Memory Dump (Address {start:05X}-{start+length-1:05X}):")
        print("-" * 60)
        
        for i in range(0, length, 4):
            addr = start + i
            words = []
            for j in range(4):
                if addr + j < self.size:
                    value = self.memory[addr + j]
                    if format == 'octal':
                        words.append(f"{value:012o}")
                    elif format == 'hex':
                        words.append(f"{value:09X}")
                    elif format == 'binary':
                        words.append(f"{value:036b}")
                    else:  # decimal
                        words.append(f"{value:10d}")
                else:
                    words.append(" " * 12)
            
            print(f"  {addr:05X}:  {'  '.join(words)}")
        
        print("-" * 60)
        print(f"  Total words: {self.size:,}")
        print(f"  Word size: {self.word_size} bits")
        print(f"  Total capacity: {self.size * self.word_size // 8:,} bytes")
        print()
    
    def get_statistics(self):
        """Get memory access statistics"""
        return {
            'size': self.size,
            'word_size': self.word_size,
            'total_capacity_bits': self.size * self.word_size,
            'total_capacity_bytes': self.size * self.word_size // 8,
            'read_count': self.read_count,
            'write_count': self.write_count,
            'access_time_ns': self.access_time_ns,
            'cycle_time_us': self.access_time_ns / 1000,
        }
    
    def test_pattern(self, pattern=0xFFFFFFFFF):
        """
        Write test pattern to all memory
        
        Args:
            pattern: Pattern to write (default: all 1s for 36 bits)
        """
        pattern = pattern & self.mask
        for i in range(self.size):
            self.memory[i] = pattern
    
    def verify_pattern(self, pattern=0xFFFFFFFFF):
        """
        Verify memory contains expected pattern
        
        Args:
            pattern: Expected pattern
            
        Returns:
            Tuple of (success, error_count, first_error_address)
        """
        pattern = pattern & self.mask
        errors = 0
        first_error = None
        
        for i in range(self.size):
            if self.memory[i] != pattern:
                errors += 1
                if first_error is None:
                    first_error = i
        
        return (errors == 0, errors, first_error)


def main():
    """Test core memory emulation"""
    print("IBM 7094 Core Memory Test")
    print("=" * 60)
    print()
    
    # Create 32K × 36-bit memory
    memory = CoreMemory(size=32768, word_size=36)
    
    print(f"Memory size: {memory.size:,} words")
    print(f"Word size: {memory.word_size} bits")
    print(f"Total capacity: {memory.size * memory.word_size // 8:,} bytes")
    print(f"Access time: {memory.access_time_ns} ns ({memory.access_time_ns/1000:.2f} μs)")
    print()
    
    # Test write and read
    print("Testing write/read...")
    test_values = [0, 1, 0o77777777777, 0xFFFFFFFFF, 0x123456789]
    
    for i, value in enumerate(test_values):
        addr = i * 100
        memory.write(addr, value)
        read_value = memory.read(addr)
        status = "✓" if read_value == value else "✗"
        print(f"  {status} Address {addr:05X}: wrote {value:010o}, read {read_value:010o}")
    
    print()
    
    # Test memory dump
    print("Memory sample (first 16 words):")
    memory.dump(start=0, length=16, format='octal')
    
    # Test statistics
    stats = memory.get_statistics()
    print("Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print()
    print("Core memory test complete!")


if __name__ == '__main__':
    main()
