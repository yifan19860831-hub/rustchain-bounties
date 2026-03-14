#!/usr/bin/env python3
"""
MANIAC I Simulator (1952)
Python simulation of the Los Alamos MANIAC I computer

Based on von Neumann IAS architecture:
- 40-bit word length
- Williams-Kilburn tube memory (CRT-based)
- ~1024 words memory capacity
- 28 instructions

Author: RustChain MANIAC Port Team
License: MIT
"""

import time
import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import IntEnum


class Opcode(IntEnum):
    """MANIAC I Instruction Set"""
    LOAD = 0x00    # Load from memory to accumulator
    STORE = 0x01   # Store accumulator to memory
    ADD = 0x02     # Add memory to accumulator
    SUB = 0x03     # Subtract memory from accumulator
    MUL = 0x04     # Multiply accumulator by memory
    DIV = 0x05     # Divide accumulator by memory
    JUMP = 0x06    # Unconditional jump
    JZ = 0x07      # Jump if accumulator is zero
    JN = 0x08      # Jump if accumulator is negative
    INPUT = 0x09   # Read from paper tape
    OUTPUT = 0x0A  # Write to output device
    HALT = 0x0B    # Stop execution
    AND = 0x0C     # Bitwise AND
    OR = 0x0D      # Bitwise OR
    XOR = 0x0E     # Bitwise XOR
    SHIFT_L = 0x0F # Shift left
    SHIFT_R = 0x10 # Shift right
    COMPARE = 0x11 # Compare accumulator with memory
    JPOS = 0x12    # Jump if positive
    CALL = 0x13    # Call subroutine
    RET = 0x14     # Return from subroutine
    NOP = 0x15     # No operation
    CLEAR = 0x16   # Clear accumulator
    NEG = 0x17     # Negate accumulator


@dataclass
class WilliamsTube:
    """
    Williams-Kilburn Tube Memory Simulation
    
    CRT-based memory that stores bits as charge patterns on phosphor.
    Requires periodic refresh (like DRAM).
    """
    capacity: int = 1024  # words
    word_size: int = 40   # bits
    memory: List[int] = field(default_factory=lambda: [0] * 1024)
    refresh_count: int = 0
    decay_rate: float = 0.001  # Simulated charge decay
    
    def read(self, address: int) -> int:
        """Read a 40-bit word from memory"""
        if address < 0 or address >= self.capacity:
            raise MemoryError(f"Address {address} out of range [0-{self.capacity-1}]")
        
        # Simulate Williams tube read (destructive, requires rewrite)
        value = self.memory[address]
        self.refresh_count += 1
        return value
    
    def write(self, address: int, value: int):
        """Write a 40-bit word to memory"""
        if address < 0 or address >= self.capacity:
            raise MemoryError(f"Address {address} out of range [0-{self.capacity-1}]")
        
        # Mask to 40 bits
        value = value & ((1 << self.word_size) - 1)
        self.memory[address] = value
        self.refresh_count += 1
    
    def refresh(self):
        """Simulate periodic memory refresh"""
        self.refresh_count += 1
        # In real Williams tubes, refresh prevents charge decay
        # We simulate this by occasionally checking memory integrity


@dataclass
class MANIACState:
    """CPU State Registers"""
    accumulator: int = 0          # 40-bit accumulator
    program_counter: int = 0      # Instruction pointer
    instruction_register: int = 0 # Current instruction
    multiplier_register: int = 0  # For multiplication
    quotient_register: int = 0    # For division
    halt: bool = False
    cycles: int = 0


class MANIACSimulator:
    """
    Complete MANIAC I Computer Simulator
    
    Simulates the 1952 Los Alamos computer with:
    - 40-bit word architecture
    - Williams tube memory
    - Vacuum tube timing characteristics
    - Paper tape I/O
    """
    
    def __init__(self, memory_size: int = 1024):
        self.memory = WilliamsTube(capacity=memory_size)
        self.state = MANIACState()
        self.io_buffer: List[int] = []
        self.output_log: List[str] = []
        self.timing_jitter: float = 0.0  # Simulated tube timing variation
        
    def load_program(self, program: List[int], start_address: int = 0):
        """Load a program into memory"""
        for i, instruction in enumerate(program):
            self.memory.write(start_address + i, instruction)
    
    def load_data(self, data: List[int], start_address: int = 0):
        """Load data into memory"""
        for i, value in enumerate(data):
            self.memory.write(start_address + i, value)
    
    def fetch(self) -> int:
        """Fetch instruction from memory"""
        instruction = self.memory.read(self.state.program_counter)
        self.state.program_counter += 1
        return instruction
    
    def decode(self, instruction: int) -> Tuple[Opcode, int]:
        """Decode instruction into opcode and address"""
        # MANIAC I format: 8-bit opcode + 32-bit address (simplified)
        opcode = Opcode(instruction >> 32) if instruction > 0xFFFFFFFF else Opcode(0)
        address = instruction & 0xFFFFFFFF
        return opcode, address
    
    def execute(self, opcode: Opcode, address: int):
        """Execute decoded instruction"""
        self.state.cycles += 1
        
        # Simulate vacuum tube timing jitter
        self.timing_jitter = random.uniform(-0.001, 0.001)
        
        if opcode == Opcode.LOAD:
            self.state.accumulator = self.memory.read(address)
        
        elif opcode == Opcode.STORE:
            self.memory.write(address, self.state.accumulator)
        
        elif opcode == Opcode.ADD:
            operand = self.memory.read(address)
            self.state.accumulator = (self.state.accumulator + operand) & 0xFFFFFFFFFF
        
        elif opcode == Opcode.SUB:
            operand = self.memory.read(address)
            self.state.accumulator = (self.state.accumulator - operand) & 0xFFFFFFFFFF
        
        elif opcode == Opcode.MUL:
            operand = self.memory.read(address)
            # 40-bit multiplication (simplified)
            result = self.state.accumulator * operand
            self.state.multiplier_register = result >> 40
            self.state.accumulator = result & 0xFFFFFFFFFF
        
        elif opcode == Opcode.DIV:
            operand = self.memory.read(address)
            if operand != 0:
                self.state.quotient_register = self.state.accumulator % operand
                self.state.accumulator = self.state.accumulator // operand
        
        elif opcode == Opcode.JUMP:
            self.state.program_counter = address
        
        elif opcode == Opcode.JZ:
            if self.state.accumulator == 0:
                self.state.program_counter = address
        
        elif opcode == Opcode.JN:
            # Check sign bit (bit 39 in 40-bit word)
            if self.state.accumulator & (1 << 39):
                self.state.program_counter = address
        
        elif opcode == Opcode.JPOS:
            if not (self.state.accumulator & (1 << 39)) and self.state.accumulator != 0:
                self.state.program_counter = address
        
        elif opcode == Opcode.INPUT:
            if self.io_buffer:
                self.state.accumulator = self.io_buffer.pop(0)
        
        elif opcode == Opcode.OUTPUT:
            self.output_log.append(f"OUTPUT[{address}]: {self.state.accumulator}")
            print(f"MANIAC OUTPUT: {self.state.accumulator}")
        
        elif opcode == Opcode.HALT:
            self.state.halt = True
        
        elif opcode == Opcode.AND:
            operand = self.memory.read(address)
            self.state.accumulator &= operand
        
        elif opcode == Opcode.OR:
            operand = self.memory.read(address)
            self.state.accumulator |= operand
        
        elif opcode == Opcode.XOR:
            operand = self.memory.read(address)
            self.state.accumulator ^= operand
        
        elif opcode == Opcode.SHIFT_L:
            self.state.accumulator = (self.state.accumulator << address) & 0xFFFFFFFFFF
        
        elif opcode == Opcode.SHIFT_R:
            self.state.accumulator = self.state.accumulator >> address
        
        elif opcode == Opcode.CLEAR:
            self.state.accumulator = 0
        
        elif opcode == Opcode.NEG:
            self.state.accumulator = (-self.state.accumulator) & 0xFFFFFFFFFF
        
        elif opcode == Opcode.NOP:
            pass
        
        elif opcode == Opcode.CALL:
            # Push return address (simplified - would use stack in real impl)
            self.memory.write(1023, self.state.program_counter)
            self.state.program_counter = address
        
        elif opcode == Opcode.RET:
            self.state.program_counter = self.memory.read(1023)
        
        elif opcode == Opcode.COMPARE:
            operand = self.memory.read(address)
            if self.state.accumulator < operand:
                self.state.accumulator = 0xFFFFFFFFFF  # All 1s (negative)
            elif self.state.accumulator > operand:
                self.state.accumulator = 0  # Zero (positive)
            # else remains 0 (equal)
        
        else:
            self.output_log.append(f"UNKNOWN OPCODE: {opcode}")
    
    def step(self) -> bool:
        """Execute one instruction cycle"""
        if self.state.halt:
            return False
        
        # Refresh Williams tube memory periodically
        if self.state.cycles % 100 == 0:
            self.memory.refresh()
        
        instruction = self.fetch()
        opcode, address = self.decode(instruction)
        self.execute(opcode, address)
        
        return not self.state.halt
    
    def run(self, max_cycles: int = 10000) -> int:
        """Run program until halt or max cycles"""
        cycles = 0
        while cycles < max_cycles and not self.state.halt:
            if not self.step():
                break
            cycles += 1
        
        return cycles
    
    def get_state(self) -> Dict:
        """Get current CPU state"""
        return {
            'accumulator': f"0x{self.state.accumulator:010X}",
            'program_counter': self.state.program_counter,
            'cycles': self.state.cycles,
            'halt': self.state.halt,
            'memory_refreshes': self.memory.refresh_count,
            'timing_jitter': self.timing_jitter
        }
    
    def dump_memory(self, start: int = 0, count: int = 16):
        """Dump memory contents"""
        print(f"\nMANIAC I Memory Dump (addresses {start}-{start+count-1}):")
        print("-" * 60)
        for i in range(count):
            addr = start + i
            value = self.memory.read(addr)
            print(f"  {addr:04d}: 0x{value:010X} ({value:11d})")
        print("-" * 60)


def demo():
    """Demonstrate MANIAC I simulator"""
    print("MANIAC I Simulator (1952)")
    print("=" * 60)
    print("Los Alamos Scientific Laboratory")
    print("Mathematical Analyzer Numerical Integrator and Computer")
    print("=" * 60)
    
    sim = MANIACSimulator()
    
    # Simple program: Add numbers 1-10
    # This demonstrates basic MANIAC I programming
    program = [
        0x0000000010,  # LOAD counter (addr 16)
        0x0200000011,  # ADD one (addr 17)
        0x0100000010,  # STORE counter
        0x0000000012,  # LOAD sum (addr 18)
        0x0200000010,  # ADD counter
        0x0100000012,  # STORE sum
        0x0000000010,  # LOAD counter
        0x0300000013,  # SUB ten (addr 19)
        0x0800000000,  # JN start (loop if < 10)
        0x0B00000000,  # HALT
    ]
    
    # Data section
    data = [
        0,   # addr 16: counter = 0
        1,   # addr 17: one = 1
        0,   # addr 18: sum = 0
        10,  # addr 19: ten = 10
    ]
    
    sim.load_program(program, start_address=0)
    sim.load_data(data, start_address=16)
    
    print("\nRunning: Sum numbers 1 to 10")
    print("-" * 60)
    
    cycles = sim.run(max_cycles=1000)
    
    print(f"\nProgram completed in {cycles} cycles")
    print(f"Final state: {sim.get_state()}")
    
    # Show result
    sum_result = sim.memory.read(18)
    print(f"\nResult: Sum = {sum_result} (expected: 55)")
    
    sim.dump_memory(start=16, count=4)
    
    print("\nOutput log:")
    for log in sim.output_log:
        print(f"   {log}")
    
    return sim


if __name__ == "__main__":
    demo()
