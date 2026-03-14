#!/usr/bin/env python3
"""
Colossus Computer Simulator (1943)
===================================
Simulates the 5-bit parallel architecture of the world's first electronic computer

Features:
- 5-bit parallel processing (Baudot code)
- Vacuum tube logic gate simulation (XOR, AND, OR)
- Shift registers
- Flip-flop memory
- Punched tape I/O

Author: OpenClaw Agent
Tribute: Tommy Flowers, Max Newman, Alan Turing
"""

from typing import List, Tuple
from dataclasses import dataclass
from enum import Enum


class LogicGate(Enum):
    """Vacuum tube logic gate types"""
    XOR = "xor"
    AND = "and"
    OR = "or"
    NOT = "not"


@dataclass
class VacuumTube:
    """Simulates a single vacuum tube"""
    id: int
    gate_type: LogicGate
    active: bool = True
    
    def compute(self, inputs: List[int]) -> int:
        """Execute logic gate computation"""
        if not self.active:
            return 0
        
        if self.gate_type == LogicGate.XOR:
            result = 0
            for i in inputs:
                result ^= i
            return result & 1
        elif self.gate_type == LogicGate.AND:
            result = 1
            for i in inputs:
                result &= i
            return result & 1
        elif self.gate_type == LogicGate.OR:
            result = 0
            for i in inputs:
                result |= i
            return result & 1
        elif self.gate_type == LogicGate.NOT:
            return (~inputs[0]) & 1
        return 0


class ShiftRegister:
    """Simulates Colossus shift register"""
    
    def __init__(self, bits: int = 5):
        self.bits = bits
        self.value = 0
        self.mask = (1 << bits) - 1
    
    def load(self, value: int) -> None:
        """Load value into register"""
        self.value = value & self.mask
    
    def shift_left(self, carry_in: int = 0) -> int:
        """Shift left, return shifted-out bit"""
        carry_out = (self.value >> (self.bits - 1)) & 1
        self.value = ((self.value << 1) | carry_in) & self.mask
        return carry_out
    
    def shift_right(self, carry_in: int = 0) -> int:
        """Shift right, return shifted-out bit"""
        carry_out = self.value & 1
        self.value = ((self.value >> 1) | (carry_in << (self.bits - 1))) & self.mask
        return carry_out
    
    def rotate_left(self) -> None:
        """Rotate left"""
        carry = (self.value >> (self.bits - 1)) & 1
        self.value = ((self.value << 1) | carry) & self.mask
    
    def get_bit(self, position: int) -> int:
        """Get bit at position"""
        return (self.value >> position) & 1


class FlipFlop:
    """Simulates flip-flop (1-bit storage)"""
    
    def __init__(self, initial: int = 0):
        self.state = initial & 1
    
    def set(self, value: int) -> None:
        self.state = value & 1
    
    def get(self) -> int:
        return self.state
    
    def toggle(self) -> int:
        self.state = 1 - self.state
        return self.state


class ColossusSimulator:
    """
    Colossus Computer Simulator
    
    Specs:
    - 5 parallel processing channels (A, B, C, D, E)
    - ~1,500-2,400 vacuum tubes
    - 5 kHz clock frequency
    - Punched tape I/O
    """
    
    def __init__(self, tube_count: int = 1500):
        self.tube_count = tube_count
        self.tubes: List[VacuumTube] = []
        self.registers: List[ShiftRegister] = []
        self.memory: List[FlipFlop] = []
        self.clock_speed = 5000  # Hz
        self.cycle_count = 0
        
        # Initialize hardware
        self._initialize_hardware()
    
    def _initialize_hardware(self) -> None:
        """Initialize Colossus hardware"""
        # Create vacuum tube array
        for i in range(self.tube_count):
            gate_type = [LogicGate.XOR, LogicGate.AND, LogicGate.OR][i % 3]
            self.tubes.append(VacuumTube(id=i, gate_type=gate_type))
        
        # Create 5-bit parallel registers (A-E channels)
        for _ in range(5):
            self.registers.append(ShiftRegister(bits=5))
        
        # Create simple flip-flop memory (~40 bits)
        for _ in range(40):
            self.memory.append(FlipFlop())
    
    def load_tape(self, data: bytes) -> List[int]:
        """
        Load punched tape data
        Each byte converted to 5-bit Baudot code
        """
        tape = []
        for byte in data:
            # Extract low 5 bits (Baudot code)
            tape.append(byte & 0b11111)
        return tape
    
    def process_parallel(self, inputs: List[int]) -> int:
        """
        5-bit parallel processing
        Input: 5 bits (A, B, C, D, E channels)
        Output: Processing result
        """
        if len(inputs) != 5:
            raise ValueError("Colossus requires exactly 5 parallel inputs")
        
        # Load into parallel registers
        for i, value in enumerate(inputs):
            self.registers[i].load(value & 1)
        
        # Process through vacuum tube array
        result = 0
        for i, tube in enumerate(self.tubes[:5]):  # Use first 5 tubes
            tube_input = [self.registers[j].get_bit(i % 5) for j in range(min(2, len(self.registers)))]
            if tube_input:
                result |= (tube.compute(tube_input) << i)
        
        self.cycle_count += 1
        return result & 0b11111
    
    def compute_hash(self, data: bytes) -> int:
        """
        Colossus-style hash function
        Uses XOR and shift register
        """
        tape = self.load_tape(data)
        accumulator = ShiftRegister(bits=5)
        
        for symbol in tape:
            # XOR accumulate
            acc_value = accumulator.value
            accumulator.load(acc_value ^ symbol)
            # Rotate
            accumulator.rotate_left()
        
        return accumulator.value
    
    def mine(self, header: bytes, difficulty: int = 3) -> Tuple[int, int]:
        """
        Execute mining operation
        Find nonce that satisfies difficulty
        
        Returns: (nonce, attempts)
        """
        # 5-bit nonce range: 0-31
        for nonce in range(32):
            # Combine header and nonce
            data = header + bytes([nonce])
            
            # Compute hash
            hash_result = self.compute_hash(data)
            
            # Check if difficulty met (first N bits zero)
            mask = (1 << difficulty) - 1
            if (hash_result & mask) == 0:
                return (nonce, nonce + 1)
        
        # Not found, return max
        return (31, 32)
    
    def display_lamp_panel(self, value: int) -> str:
        """
        Simulate lamp panel display
        [X] = on (1), [ ] = off (0)
        """
        bits = []
        for i in range(4, -1, -1):
            bit = (value >> i) & 1
            bits.append('[X]' if bit else '[ ]')
        return ' '.join(bits)
    
    def get_status(self) -> dict:
        """Get simulator status"""
        return {
            'tube_count': self.tube_count,
            'active_tubes': sum(1 for t in self.tubes if t.active),
            'clock_speed_hz': self.clock_speed,
            'cycle_count': self.cycle_count,
            'registers': len(self.registers),
            'memory_bits': len(self.memory)
        }


def demo():
    """Demo Colossus simulator"""
    print("=" * 60)
    print("  COLOSSUS COMPUTER SIMULATOR (1943)")
    print("  World's First Electronic Digital Computer")
    print("=" * 60)
    print()
    
    # Create simulator
    colossus = ColossusSimulator(tube_count=1500)
    
    # Display specs
    status = colossus.get_status()
    print("Hardware Specs:")
    print(f"   Vacuum Tubes: {status['tube_count']}")
    print(f"   Clock Speed: {status['clock_speed_hz']} Hz")
    print(f"   Parallel Registers: {status['registers']} (5-bit)")
    print(f"   Flip-flop Memory: {status['memory_bits']} bits")
    print()
    
    # Demo 5-bit parallel processing
    print("5-bit Parallel Processing Demo:")
    test_inputs = [
        [1, 0, 1, 1, 0],  # A=1, B=0, C=1, D=1, E=0
        [0, 1, 1, 0, 1],
        [1, 1, 0, 0, 1],
    ]
    
    for inputs in test_inputs:
        result = colossus.process_parallel(inputs)
        display = colossus.display_lamp_panel(result)
        print(f"   Input: {inputs} -> Output: {display} ({result})")
    print()
    
    # Demo hash function
    print("Colossus Hash Function:")
    test_data = [
        b"BLOCK1",
        b"BLOCK2",
        b"RUSTCHAIN",
    ]
    
    for data in test_data:
        hash_val = colossus.compute_hash(data)
        display = colossus.display_lamp_panel(hash_val)
        print(f"   hash('{data.decode()}') = {display} ({hash_val:02d})")
    print()
    
    # Demo mining
    print("Mining Demo (difficulty=2):")
    header = b"RUSTCHAIN_BLOCK_HEADER"
    nonce, attempts = colossus.mine(header, difficulty=2)
    print(f"   Header: {header.decode()}")
    print(f"   Found Nonce: {nonce}")
    print(f"   Attempts: {attempts}")
    
    # Verify
    data = header + bytes([nonce])
    final_hash = colossus.compute_hash(data)
    display = colossus.display_lamp_panel(final_hash)
    print(f"   Final Hash: {display} ({final_hash})")
    print()
    
    # Lamp panel examples
    print("Lamp Panel Examples:")
    for i in range(8):
        display = colossus.display_lamp_panel(i)
        print(f"   {i:02d}: {display}")
    print()
    
    print("=" * 60)
    print(f"Simulation Complete - Total Cycles: {colossus.cycle_count}")
    print("=" * 60)


if __name__ == "__main__":
    demo()
