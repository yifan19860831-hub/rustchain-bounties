#!/usr/bin/env python3
"""
IBM 7094 Index Registers

Emulates the 7 index registers (XR1-XR7) introduced in the IBM 7094
(upgraded from 3 on the IBM 7090)

Features:
- Seven Index Register Mode (7094 enhancement)
- Multiple Tag Mode (7090 compatibility)
- 36-bit registers

Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b
"""


class IndexRegisters:
    """
    Index register file for IBM 7094
    
    The IBM 7094 introduced 7 index registers (XR1-XR7),
    upgraded from 3 on the IBM 7090.
    
    Two operating modes:
    1. Seven Index Register Mode: Tag field selects single register (1-7)
    2. Multiple Tag Mode: Tag bits are ORed together (7090 compatible)
    """
    
    def __init__(self, count=7, word_size=36):
        """
        Initialize index registers
        
        Args:
            count: Number of registers (default 7 for IBM 7094)
            word_size: Bits per register (default 36)
        """
        self.count = count
        self.word_size = word_size
        self.mask = (1 << word_size) - 1
        
        # Register array (index 0 = XR1, index 6 = XR7)
        self.registers = [0] * count
        
        # Mode flag
        # False = Multiple Tag Mode (power-on default, 7090 compatible)
        # True = Seven Index Register Mode (7094 enhancement)
        self.seven_index_mode = False
        
        # Statistics
        self.read_count = 0
        self.write_count = 0
    
    def clear(self):
        """Clear all index registers to zero"""
        self.registers = [0] * self.count
        self.read_count = 0
        self.write_count = 0
        self.seven_index_mode = False
    
    def read(self, index):
        """
        Read an index register
        
        Args:
            index: Register number (0-6 for XR1-XR7)
            
        Returns:
            36-bit register value
            
        Raises:
            ValueError: If index is out of range
        """
        if index < 0 or index >= self.count:
            raise ValueError(f"Index {index} out of range (0-{self.count-1})")
        
        self.read_count += 1
        return self.registers[index] & self.mask
    
    def write(self, index, value):
        """
        Write to an index register
        
        Args:
            index: Register number (0-6 for XR1-XR7)
            value: 36-bit value
            
        Raises:
            ValueError: If index is out of range
        """
        if index < 0 or index >= self.count:
            raise ValueError(f"Index {index} out of range (0-{self.count-1})")
        
        self.write_count += 1
        self.registers[index] = value & self.mask
    
    def select(self, tag_field):
        """
        Select index register based on tag field
        
        In Seven Index Register Mode:
        - Tag 000: No indexing
        - Tag 001-111: Select XR1-XR7
        
        In Multiple Tag Mode:
        - Tag bits are ORed together
        
        Args:
            tag_field: 3-bit tag field (0-7)
            
        Returns:
            Combined index register value (or 0 if no indexing)
        """
        if tag_field == 0:
            return 0  # No indexing
        
        if self.seven_index_mode:
            # Seven Index Register Mode: direct selection
            index = tag_field - 1
            if index < self.count:
                return self.read(index)
            else:
                raise ValueError(f"Invalid tag {tag_field} in seven index mode")
        else:
            # Multiple Tag Mode: OR together selected registers
            # Bit 0 (value 1) = XR1, Bit 1 (value 2) = XR2, Bit 2 (value 4) = XR3
            result = 0
            if tag_field & 0b001:
                result |= self.read(0)  # XR1
            if tag_field & 0b010:
                result |= self.read(1)  # XR2
            if tag_field & 0b100:
                result |= self.read(2)  # XR3
            return result
    
    def enter_seven_index_mode(self):
        """Switch to Seven Index Register Mode (7094 enhancement)"""
        self.seven_index_mode = True
    
    def enter_multiple_tag_mode(self):
        """Switch to Multiple Tag Mode (7090 compatible, power-on default)"""
        self.seven_index_mode = False
    
    def is_seven_index_mode(self):
        """Check if in Seven Index Register Mode"""
        return self.seven_index_mode
    
    def modify_address(self, address, tag_field):
        """
        Modify an address using index registers
        
        In Seven Index Register Mode:
        - Effective address = Y - XR[tag]
        
        In Multiple Tag Mode:
        - Effective address = Y - (XR1 | XR2 | XR3) [based on tag bits]
        
        Args:
            address: Base address (Y field)
            tag_field: 3-bit tag field
            
        Returns:
            Effective address
        """
        if tag_field == 0:
            return address
        
        index_value = self.select(tag_field)
        
        # IBM 7094 subtracts index register from address
        effective_address = (address - index_value) & 0x7FFF  # 15-bit address
        
        return effective_address
    
    def dump(self):
        """Dump all index registers"""
        mode_str = "Seven Index" if self.seven_index_mode else "Multiple Tag"
        print(f"Index Registers (Mode: {mode_str}):")
        print("-" * 40)
        
        for i in range(self.count):
            value = self.registers[i]
            print(f"  XR{i+1}: {value:010o} (octal)  {value:09X} (hex)")
        
        print("-" * 40)
        print(f"  Mode: {mode_str}")
        print(f"  Reads: {self.read_count}")
        print(f"  Writes: {self.write_count}")
        print()
    
    def get_statistics(self):
        """Get register usage statistics"""
        return {
            'count': self.count,
            'word_size': self.word_size,
            'seven_index_mode': self.seven_index_mode,
            'read_count': self.read_count,
            'write_count': self.write_count,
            'register_values': [r & self.mask for r in self.registers],
        }


def main():
    """Test index register emulation"""
    print("IBM 7094 Index Register Test")
    print("=" * 60)
    print()
    
    # Create 7 index registers (IBM 7094)
    xr = IndexRegisters(count=7, word_size=36)
    
    print(f"Number of registers: {xr.count}")
    print(f"Word size: {xr.word_size} bits")
    print(f"Initial mode: {'Seven Index' if xr.seven_index_mode else 'Multiple Tag'}")
    print()
    
    # Test write and read
    print("Testing write/read...")
    test_values = [0, 1, 100, 1000, 0o77777777777]
    
    for i, value in enumerate(test_values):
        xr.write(i, value)
        read_value = xr.read(i)
        status = "✓" if read_value == value else "✗"
        print(f"  {status} XR{i+1}: wrote {value:010o}, read {read_value:010o}")
    
    print()
    
    # Test mode switching
    print("Testing mode switching...")
    xr.enter_seven_index_mode()
    print(f"  Seven Index Mode: {xr.is_seven_index_mode()}")
    
    xr.enter_multiple_tag_mode()
    print(f"  Multiple Tag Mode: {not xr.is_seven_index_mode()}")
    print()
    
    # Test address modification
    print("Testing address modification...")
    xr.write(0, 100)  # XR1 = 100
    xr.write(1, 200)  # XR2 = 200
    
    base_addr = 1000
    eff_addr = xr.modify_address(base_addr, 0b001)  # Use XR1
    print(f"  Base: {base_addr}, Tag: 001 (XR1), Effective: {eff_addr}")
    
    eff_addr = xr.modify_address(base_addr, 0b010)  # Use XR2
    print(f"  Base: {base_addr}, Tag: 010 (XR2), Effective: {eff_addr}")
    
    print()
    
    # Dump registers
    xr.dump()
    
    print("Index register test complete!")


if __name__ == '__main__':
    main()
