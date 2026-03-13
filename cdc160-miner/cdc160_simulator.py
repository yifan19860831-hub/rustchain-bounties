#!/usr/bin/env python3
"""CDC 160 (1960) Simulator - Simplified

CDC 160 Architecture:
- 12-bit word length
- 4096 words of magnetic core memory
- Ones' complement arithmetic with end-around carry
- 12-bit accumulator (A register)
- P register (program counter)
- Memory cycle time: 6.4 μs
- Average instruction: 15 μs (~67,000 IPS)
- Designed by Seymour Cray in 1960
"""
import time

class CDC160Simulator:
    """CDC 160 Minicomputer Simulator"""
    
    MASK_12BIT = 0xFFF  # 12-bit mask
    
    def __init__(self, memory_size=4096):
        self.memory = [0] * memory_size
        self.A = 0      # 12-bit accumulator
        self.P = 0      # Program counter (12-bit)
        self.halted = False
        self.instruction_count = 0
        
    def _ones_complement_add(self, a, b):
        """Perform ones' complement addition with end-around carry"""
        result = a + b
        # If there's a carry out of bit 11, add it back (end-around carry)
        while result > self.MASK_12BIT:
            carry = result >> 12
            result = (result & self.MASK_12BIT) + carry
        return result & self.MASK_12BIT
    
    def load(self, program, addr=0):
        """Load program into memory starting at address"""
        for i, word in enumerate(program):
            if addr + i < len(self.memory):
                self.memory[addr + i] = word & self.MASK_12BIT
    
    def fetch(self):
        """Fetch instruction from memory at P"""
        return self.memory[self.P]
    
    def run(self, max_instr=0):
        """Execute instructions until halted or max_instr reached"""
        count = 0
        while not self.halted and (max_instr == 0 or count < max_instr):
            instr = self.fetch()
            opcode = (instr >> 6) & 0x3F  # 6-bit opcode
            address = instr & 0x3F        # 6-bit address
            
            # Simplified instruction set (based on CDC 160 ISA)
            if opcode == 0o00:  # HLT - Halt
                self.halted = True
            elif opcode == 0o01:  # CLA - Clear A
                self.A = 0
            elif opcode == 0o02:  # INA - Increment A
                self.A = self._ones_complement_add(self.A, 1)
            elif opcode == 0o03:  # LDA - Load A from memory
                self.A = self.memory[address]
            elif opcode == 0o04:  # STA - Store A to memory
                self.memory[address] = self.A
            elif opcode == 0o05:  # ADD - Add memory to A (ones' complement)
                self.A = self._ones_complement_add(self.A, self.memory[address])
            elif opcode == 0o06:  # SUB - Subtract memory from A
                # Ones' complement subtraction: A - M = A + ~M
                complement = (~self.memory[address]) & self.MASK_12BIT
                self.A = self._ones_complement_add(self.A, complement)
            elif opcode == 0o07:  # JMP - Jump to address
                self.P = address
                count += 1
                continue
            elif opcode == 0o10:  # NOP - No operation
                pass
            
            self.P = (self.P + 1) & 0xFFF  # Increment P (12-bit)
            self.instruction_count += 1
            count += 1
        
        return count
    
    def get_state(self):
        """Return current machine state"""
        return {
            'A': self.A,
            'P': self.P,
            'halted': self.halted,
            'instructions_executed': self.instruction_count
        }


if __name__ == '__main__':
    # Test the simulator
    sim = CDC160Simulator()
    
    # Simple test program: CLA, INA (x3), STA 0o77, HLT
    # Opcodes: CLA=0o0100, INA=0o0200, STA=0o0400+addr, HLT=0o0000
    test_program = [
        0o0100,  # CLA - Clear A
        0o0200,  # INA - A = 1
        0o0200,  # INA - A = 2
        0o0200,  # INA - A = 3
        0o0477,  # STA 77 - Store A to address 77
        0o0000,  # HLT - Halt
    ]
    
    sim.load(test_program)
    n = sim.run()
    state = sim.get_state()
    
    print(f"CDC 160 Simulator OK")
    print(f"  Executed {n} instructions")
    print(f"  A = {state['A']} (octal: {oct(state['A'])})")
    print(f"  Memory[77] = {sim.memory[0o77]} (should be 3)")
    print(f"  Halted: {state['halted']}")
