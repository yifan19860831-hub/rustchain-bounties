#!/usr/bin/env python3
"""
ERA 1101 CPU Simulator

Simulates the Engineering Research Associates 1101 (1950),
later renamed UNIVAC 1101 — the first commercially available
stored-program computer.

Architecture:
- 24-bit parallel binary
- Ones' complement arithmetic
- 48-bit accumulator (subtractive design)
- Magnetic drum memory: 16,384 words
- 38 instructions
"""

class ERA1101CPU:
    """ERA 1101 CPU simulator"""
    
    def __init__(self):
        # Registers (24-bit, ones' complement)
        self.AH = 0  # Accumulator high 24 bits
        self.AL = 0  # Accumulator low 24 bits
        self.Q = 0   # Q-register (multiplier/quotient)
        self.X = 0   # X-register (index)
        
        # Program counter
        self.PC = 0
        
        # Status flags
        self.zero_flag = False
        self.neg_flag = False
        
        # Memory (16K words)
        self.memory_size = 16384
        self.memory = [0] * self.memory_size
        
        # Execution statistics
        self.instructions_executed = 0
        self.cycle_count = 0
        
    def mask24(self, value):
        """Mask to 24 bits"""
        return value & 0xFFFFFF
    
    def mask48(self, value):
        """Mask to 48 bits"""
        return value & 0xFFFFFFFFFFFF
    
    def ones_complement(self, value):
        """Compute ones' complement (bitwise NOT for 24 bits)"""
        return (~value) & 0xFFFFFF
    
    def is_negative(self, value):
        """Check if 24-bit value is negative (MSB set)"""
        return (value & 0x800000) != 0
    
    def abs_value(self, value):
        """Get absolute value in ones' complement"""
        if self.is_negative(value):
            return self.ones_complement(value)
        return value
    
    def load(self, address):
        """Load word from memory"""
        address = address % self.memory_size
        return self.memory[address]
    
    def store(self, address, value):
        """Store word to memory"""
        address = address % self.memory_size
        self.memory[address] = self.mask24(value)
    
    def set_flags(self, value):
        """Set status flags based on value"""
        value = self.mask24(value)
        self.zero_flag = (value == 0)
        self.neg_flag = self.is_negative(value)
    
    def fetch_decode(self):
        """Fetch and decode instruction"""
        instr = self.load(self.PC)
        
        # Decode: 6-bit opcode, 4-bit skip, 14-bit address
        opcode = (instr >> 18) & 0x3F
        skip = (instr >> 14) & 0x0F
        address = instr & 0x3FFF
        
        return opcode, skip, address
    
    def execute(self, opcode, skip, address):
        """Execute instruction"""
        self.instructions_executed += 1
        
        # Arithmetic instructions (00-0F)
        if opcode == 0x00:  # INS: Insert (y) in A
            value = self.load(address)
            self.AH = 0
            self.AL = value
            self.set_flags(value)
            
        elif opcode == 0x01:  # INSC: Insert complement of (y) in A
            value = self.ones_complement(self.load(address))
            self.AH = 0
            self.AL = value
            self.set_flags(value)
            
        elif opcode == 0x06:  # ADD: Add (y) to (A)
            value = self.load(address)
            # Standard addition with end-around carry for ones' complement
            result = self.AL + value
            # End-around carry: if overflow, add 1
            if result > 0xFFFFFF:
                result = (result & 0xFFFFFF) + 1
            self.AL = self.mask24(result)
            self.set_flags(self.AL)
            
        elif opcode == 0x07:  # SUB: Subtract (y) from (A)
            value = self.load(address)
            result = (self.AL - value) & 0xFFFFFF
            # End-around borrow for ones' complement
            if value > self.AL:
                result = (result - 1) & 0xFFFFFF
            self.AL = result
            self.set_flags(result)
            
        elif opcode == 0x0C:  # INSQ: Insert (Q) in A
            self.AH = 0
            self.AL = self.Q
            self.set_flags(self.Q)
            
        elif opcode == 0x0D:  # CLR: Clear right half of A
            self.AL = 0
            self.zero_flag = (self.AH == 0)
            
        elif opcode == 0x0E:  # ADDQ: Add (Q) to (A)
            result = (self.AL + self.Q) & 0xFFFFFF
            if result > 0xFFFFFF:
                result = (result + 1) & 0xFFFFFF
            self.AL = result
            self.set_flags(result)
            
        elif opcode == 0x0F:  # TRA: Transmit (A) to Q
            self.Q = self.AL
            
        # Multiply/Divide (10-14)
        elif opcode == 0x12:  # AND: Form logical product (Q) * (y) in A
            value = self.load(address)
            result = self.Q & value
            self.AL = result
            self.set_flags(result)
            
        # Logical/Control (15-1F)
        elif opcode == 0x15:  # STO: Store right half of (A) at y
            self.store(address, self.AL)
            
        elif opcode == 0x16:  # SHL: Shift (A) left
            self.AL = (self.AL << 1) & 0xFFFFFF
            self.set_flags(self.AL)
            
        elif opcode == 0x17:  # STQ: Store (Q) at y
            self.store(address, self.Q)
            
        elif opcode == 0x1A:  # JMP: Take (y) as next order
            self.PC = address
            return  # Skip normal PC increment
            
        elif opcode == 0x1C:  # JNZ: Jump if (A) is not zero
            if not self.zero_flag:
                self.PC = address
                return
                
        elif opcode == 0x1E:  # JN: Jump if (A) is negative
            if self.neg_flag:
                self.PC = address
                return
                
        elif opcode == 0x1D:  # INSX: Insert (y) in Q
            self.Q = self.load(address)
            
        # I/O and Control (20-27) - simplified
        elif opcode == 0x20:  # Print
            value = self.load(address)
            print(f"PRINT: {value:06X}")
            
        elif opcode == 0x22:  # Final Stop
            return False  # Halt
            
        # Unimplemented
        else:
            print(f"WARNING: Unimplemented opcode {opcode:02X} at PC={self.PC}")
        
        # Update PC with skip
        self.PC = (self.PC + skip + 1) % self.memory_size
        return True
    
    def run(self, start_address=0, max_instructions=1000):
        """Run program from start address"""
        self.PC = start_address
        self.instructions_executed = 0
        
        print(f"Starting execution at PC={start_address}")
        
        for i in range(max_instructions):
            opcode, skip, address = self.fetch_decode()
            result = self.execute(opcode, skip, address)
            
            if result is False:  # Halt instruction
                print(f"Halted after {i+1} instructions")
                break
                
        print(f"Execution complete: {self.instructions_executed} instructions")
    
    def load_program(self, program, start_address=0):
        """Load program into memory"""
        for i, word in enumerate(program):
            self.memory[start_address + i] = self.mask24(word)
        print(f"Loaded {len(program)} words at address {start_address}")
    
    def dump_memory(self, start=0, length=32):
        """Dump memory contents"""
        print(f"Memory dump ({start:04X}-{start+length:04X}):")
        for i in range(length):
            addr = start + i
            if addr % 8 == 0:
                print(f"\n{addr:04X}: ", end="")
            print(f"{self.memory[addr]:06X} ", end="")
        print()
    
    def dump_registers(self):
        """Dump register contents"""
        print(f"A={self.AH:06X}:{self.AL:06X}  Q={self.Q:06X}  X={self.X:06X}  PC={self.PC:04X}")
        print(f"Zero={self.zero_flag}  Neg={self.neg_flag}")


# Example program: Add two numbers
def test_basic():
    """Test basic arithmetic"""
    cpu = ERA1101CPU()
    
    # Program: Load value, add another value, store result
    program = [
        0x000000,  # 0000: INS 0x0003 (load from addr 3)
        0x060004,  # 0001: ADD 0x0004 (add from addr 4)
        0x150005,  # 0002: STO 0x0005 (store to addr 5)
        0x00002A,  # 0003: Data: 42
        0x000018,  # 0004: Data: 24
        0x000000,  # 0005: Result location
        0x220000,  # 0006: HALT
    ]
    
    cpu.load_program(program)
    cpu.run()
    cpu.dump_registers()
    print(f"Result: {cpu.memory[5]} (expected: 66)")


if __name__ == "__main__":
    test_basic()
