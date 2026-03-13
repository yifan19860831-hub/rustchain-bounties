#!/usr/bin/env python3
"""
IBM 305 RAMAC Simulator
=======================
Simulates the IBM 305 RAMAC computer (1956) with:
- Drum memory (3,200 characters = 32 tracks × 100 characters)
- Core buffer (100 characters)
- IBM 350 disk storage (5 MB)
- BCD character architecture (6-bit data + 1-bit parity)

This simulator is used for testing and developing the IBM 305 RAMAC miner.
"""

import hashlib
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class TrackCode(Enum):
    """IBM 305 track/source codes"""
    W = 'W'  # General storage
    X = 'X'  # General storage
    Y = 'Y'  # General storage
    Z = 'Z'  # General storage
    ZERO = '0'  # Instruction/General storage
    ONE = '1'  # Instruction/General storage
    TWO = '2'  # Instruction/General storage
    THREE = '3'  # Instruction/General storage
    FOUR = '4'  # Instruction/General storage
    FIVE = '5'  # Instruction/General storage
    SIX = '6'  # Instruction/General storage
    SEVEN = '7'  # Instruction/General storage
    EIGHT = '8'  # Instruction/General storage
    NINE = '9'  # Instruction/General storage
    A = 'A'  # Instruction/General storage
    B = 'B'  # Instruction/General storage
    C = 'C'  # Instruction/General storage
    D = 'D'  # Instruction/General storage
    E = 'E'  # Instruction/General storage
    F = 'F'  # Instruction/General storage
    G = 'G'  # Instruction/General storage
    H = 'H'  # Instruction/General storage
    I = 'I'  # Instruction/General storage
    L = 'L'  # Accumulator (arithmetic)
    M = 'M'  # Accumulator (arithmetic, clear)
    V = 'V'  # Multiplier/Divisor
    N = 'N'  # Multiply result
    P = 'P'  # Divide result
    K = 'K'  # Card input
    S = 'S'  # Card output
    T = 'T'  # Printer output
    Q = 'Q'  # Inquiry I/O
    J = 'J'  # Disk file address
    R = 'R'  # Disk file data
    DASH = '-'  # Core buffer
    DOLLAR = '$'  # Paper tape I/O


@dataclass
class BCDCharacter:
    """IBM 305 BCD Character (7-bit: 6 data + 1 parity)"""
    x_zone: bool = False  # X zone bit
    o_zone: bool = False  # O zone bit
    value: int = 0  # 4-bit numeric value (0-9)
    parity: bool = False  # Odd parity
    
    def to_bits(self) -> int:
        """Convert to 7-bit integer"""
        return (
            (int(self.x_zone) << 6) |
            (int(self.o_zone) << 5) |
            (self.value << 1) |
            int(self.parity)
        )
    
    @classmethod
    def from_bits(cls, bits: int) -> 'BCDCharacter':
        """Create from 7-bit integer"""
        return cls(
            x_zone=bool(bits & 0x40),
            o_zone=bool(bits & 0x20),
            value=(bits & 0x1E) >> 1,
            parity=bool(bits & 0x01)
        )
    
    def __str__(self) -> str:
        """Convert to readable character"""
        if self.x_zone and self.o_zone:
            # Special characters
            return chr(ord('A') + self.value - 1) if self.value > 0 else '&'
        elif self.x_zone:
            # Letters J-Z
            return chr(ord('J') + self.value - 1) if self.value > 0 else '/'
        elif self.o_zone:
            # Letters A-I
            return chr(ord('A') + self.value - 1) if self.value > 0 else '-'
        else:
            # Digits 0-9
            return str(self.value)
    
    @classmethod
    def from_char(cls, char: str) -> 'BCDCharacter':
        """Create from ASCII character"""
        char = char.upper()
        if char.isdigit():
            return cls(value=int(char))
        elif 'A' <= char <= 'I':
            return cls(o_zone=True, value=ord(char) - ord('A') + 1)
        elif 'J' <= char <= 'Z':
            return cls(x_zone=True, value=ord(char) - ord('J') + 1)
        elif char == '&':
            return cls(x_zone=True, o_zone=True)
        elif char == '/':
            return cls(x_zone=True, o_zone=True, value=10)
        elif char == '-':
            return cls(x_zone=True, o_zone=True, value=10)
        else:
            return cls()  # Default to 0
    
    def check_parity(self) -> bool:
        """Verify odd parity"""
        bits = self.to_bits()
        parity_bit = bin(bits >> 1).count('1') % 2
        return self.parity != (parity_bit == 0)


@dataclass
class Instruction:
    """IBM 305 Instruction (10 characters)"""
    t1: str = ' '  # Source track
    a1: str = ' '  # Source track address (tens)
    b1: str = ' '  # Source track address (units)
    t2: str = ' '  # Destination track
    a2: str = ' '  # Destination track address (tens)
    b2: str = ' '  # Destination track address (units)
    m: str = ' '   # Length of operand
    n: str = ' '   # Control (jump/condition)
    p: str = ' '   # Reserved
    q: str = ' '   # Operation code
    
    @classmethod
    def parse(cls, text: str) -> 'Instruction':
        """Parse 10-character instruction"""
        if len(text) < 10:
            text = text.ljust(10)
        return cls(
            t1=text[0], a1=text[1], b1=text[2],
            t2=text[3], a2=text[4], b2=text[5],
            m=text[6], n=text[7], p=text[8], q=text[9]
        )
    
    def __str__(self) -> str:
        return f"{self.t1}{self.a1}{self.b1}{self.t2}{self.a2}{self.b2}{self.m}{self.n}{self.p}{self.q}"
    
    def get_source_address(self) -> int:
        """Get source address (0-99)"""
        try:
            return int(self.a1) * 10 + int(self.b1)
        except ValueError:
            return 0
    
    def get_dest_address(self) -> int:
        """Get destination address (0-99)"""
        try:
            return int(self.a2) * 10 + int(self.b2)
        except ValueError:
            return 0
    
    def get_length(self) -> int:
        """Get operand length"""
        try:
            return int(self.m) if self.m.isdigit() else 1
        except ValueError:
            return 1


@dataclass
class DrumMemory:
    """IBM 305 Drum Memory (3,200 characters = 32 tracks × 100 characters)"""
    tracks: Dict[str, List[BCDCharacter]] = field(default_factory=dict)
    current_rotation: int = 0  # Current drum rotation position (0-99)
    
    def __post_init__(self):
        # Initialize 32 tracks (W, X, Y, Z, 0-9, A-I)
        track_names = ['W', 'X', 'Y', 'Z'] + [str(i) for i in range(10)] + list('ABCDEFGHI')
        for track in track_names:
            self.tracks[track] = [BCDCharacter() for _ in range(100)]
    
    def read_character(self, track: str, address: int) -> BCDCharacter:
        """Read character from drum memory"""
        if track in self.tracks and 0 <= address < 100:
            return self.tracks[track][address]
        return BCDCharacter()
    
    def write_character(self, track: str, address: int, char: BCDCharacter):
        """Write character to drum memory"""
        if track in self.tracks and 0 <= address < 100:
            self.tracks[track][address] = char
    
    def read_field(self, track: str, start: int, length: int) -> str:
        """Read field of characters"""
        result = []
        for i in range(length):
            addr = (start + i) % 100
            result.append(str(self.read_character(track, addr)))
        return ''.join(result)
    
    def write_field(self, track: str, start: int, data: str):
        """Write field of characters"""
        for i, char in enumerate(data):
            addr = (start + i) % 100
            self.write_character(track, addr, BCDCharacter.from_char(char))


@dataclass
class CoreBuffer:
    """IBM 305 Core Buffer (100 characters)"""
    memory: List[BCDCharacter] = field(default_factory=lambda: [BCDCharacter() for _ in range(100)])
    
    def read(self, address: int) -> BCDCharacter:
        if 0 <= address < 100:
            return self.memory[address]
        return BCDCharacter()
    
    def write(self, address: int, char: BCDCharacter):
        if 0 <= address < 100:
            self.memory[address] = char


@dataclass
class Accumulator:
    """IBM 305 Accumulator (arithmetic operations)"""
    value: str = ""
    cleared: bool = False
    
    def clear(self):
        self.value = ""
        self.cleared = True
    
    def add(self, value: str):
        if self.cleared:
            self.value = value
            self.cleared = False
        else:
            # Simple string concatenation for BCD arithmetic
            try:
                result = int(self.value or '0') + int(value or '0')
                self.value = str(result)
            except ValueError:
                self.value = value
    
    def subtract(self, value: str):
        try:
            result = int(self.value or '0') - int(value or '0')
            self.value = str(max(0, result))
        except ValueError:
            self.value = ""


@dataclass
class DiskStorage:
    """IBM 350 Disk Storage (5 MB simulation)"""
    disks: Dict[int, Dict[int, str]] = field(default_factory=dict)  # disk_id -> track -> data
    current_disk: int = 0
    current_track: int = 0
    
    def write(self, address: str, data: str):
        """Write data to disk address"""
        # Parse address format: disk-track-sector
        parts = address.split('-')
        if len(parts) >= 3:
            disk_id = int(parts[0])
            track = int(parts[1])
            if disk_id not in self.disks:
                self.disks[disk_id] = {}
            self.disks[disk_id][track] = data
    
    def read(self, address: str) -> str:
        """Read data from disk address"""
        parts = address.split('-')
        if len(parts) >= 3:
            disk_id = int(parts[0])
            track = int(parts[1])
            if disk_id in self.disks and track in self.disks[disk_id]:
                return self.disks[disk_id][track]
        return ""


class IBM305Simulator:
    """Main IBM 305 RAMAC Simulator"""
    
    def __init__(self):
        self.drum = DrumMemory()
        self.core = CoreBuffer()
        self.accumulator = Accumulator()
        self.disk = DiskStorage()
        self.program_counter = 0
        self.halted = False
        self.instruction_count = 0
        self.start_time = time.time()
        
        # Statistics
        self.stats = {
            'instructions_executed': 0,
            'drum_reads': 0,
            'drum_writes': 0,
            'disk_reads': 0,
            'disk_writes': 0,
            'arithmetic_ops': 0,
            'io_ops': 0
        }
    
    def load_program(self, program: List[str], start_address: int = 0):
        """Load program into drum memory track 0"""
        for i, instruction in enumerate(program):
            addr = start_address + i
            if addr < 100:
                # Store as BCD characters
                for j, char in enumerate(instruction[:10].ljust(10)):
                    self.drum.write_character('0', addr, BCDCharacter.from_char(char))
    
    def fetch_instruction(self, address: int) -> Instruction:
        """Fetch instruction from drum memory"""
        # Read 10 characters from track 0
        chars = []
        for i in range(10):
            char = self.drum.read_character('0', address)
            chars.append(str(char))
        return Instruction.parse(''.join(chars))
    
    def execute_instruction(self, instr: Instruction) -> bool:
        """Execute a single instruction. Returns True if program should continue."""
        self.stats['instructions_executed'] += 1
        
        # Parse operation code (Q field)
        op_code = instr.q.upper() if instr.q.strip() else ' '
        
        # Get source and destination
        src_track = instr.t1.upper()
        src_addr = instr.get_source_address()
        dst_track = instr.t2.upper()
        dst_addr = instr.get_dest_address()
        length = instr.get_length()
        
        # Execute based on operation
        if op_code == ' ' or op_code == '0':
            # Copy operation
            self._copy(src_track, src_addr, dst_track, dst_addr, length)
        elif op_code == '1':
            # Compare
            self._compare(src_track, src_addr, dst_track, dst_addr, length)
        elif op_code == '5':
            # Clear accumulator
            self.accumulator.clear()
            self.stats['arithmetic_ops'] += 1
        elif op_code == 'L':
            # Load to accumulator / Add
            data = self.drum.read_field(src_track, src_addr, length)
            self.accumulator.add(data)
            self.stats['arithmetic_ops'] += 1
        elif op_code == 'M':
            # Load and clear / Subtract
            data = self.drum.read_field(src_track, src_addr, length)
            self.accumulator.subtract(data)
            self.stats['arithmetic_ops'] += 1
        elif op_code == 'K':
            # Card input (simulated)
            self.stats['io_ops'] += 1
        elif op_code == 'S' or op_code == 'T':
            # Card/Printer output (simulated)
            self.stats['io_ops'] += 1
        elif op_code == 'J':
            # Disk address
            self.disk.current_disk = src_addr
            self.disk.current_track = dst_addr
            self.stats['io_ops'] += 1
        elif op_code == 'R':
            # Disk data I/O
            if instr.n.strip():  # Read
                data = self.disk.read(f"{self.disk.current_disk}-{self.disk.current_track}-0")
                self.drum.write_field(dst_track, dst_addr, data)
                self.stats['disk_reads'] += 1
            else:  # Write
                data = self.drum.read_field(src_track, src_addr, length)
                self.disk.write(f"{self.disk.current_disk}-{self.disk.current_track}-0", data)
                self.stats['disk_writes'] += 1
        
        # Handle program flow (N field)
        if instr.n.upper() == 'P':
            # Program exit - halt
            self.halted = True
            return False
        elif instr.n.isdigit() and int(instr.n) > 0:
            # Conditional jump (simplified)
            pass
        
        return True
    
    def _copy(self, src_track: str, src_addr: int, dst_track: str, dst_addr: int, length: int):
        """Copy data from source to destination"""
        for i in range(length):
            char = self.drum.read_character(src_track, (src_addr + i) % 100)
            self.drum.write_character(dst_track, (dst_addr + i) % 100, char)
            self.stats['drum_reads'] += 1
            self.stats['drum_writes'] += 1
    
    def _compare(self, src_track: str, src_addr: int, dst_track: str, dst_addr: int, length: int):
        """Compare two fields"""
        for i in range(length):
            c1 = self.drum.read_character(src_track, (src_addr + i) % 100)
            c2 = self.drum.read_character(dst_track, (dst_addr + i) % 100)
            if c1.to_bits() != c2.to_bits():
                return False  # Mismatch
        return True  # Match
    
    def run(self, max_instructions: int = 10000, start_address: int = 0):
        """Run the program"""
        self.program_counter = start_address
        self.halted = False
        
        while not self.halted and self.instruction_count < max_instructions:
            instr = self.fetch_instruction(self.program_counter)
            if not self.execute_instruction(instr):
                break
            
            self.instruction_count += 1
            self.program_counter += 1
            
            # Wrap around drum track
            if self.program_counter >= 100:
                self.program_counter = 0
        
        return self.get_statistics()
    
    def get_statistics(self) -> dict:
        """Get execution statistics"""
        elapsed = time.time() - self.start_time
        return {
            **self.stats,
            'elapsed_time': elapsed,
            'instructions_per_second': self.stats['instructions_executed'] / elapsed if elapsed > 0 else 0,
            'final_pc': self.program_counter,
            'halted': self.halted
        }
    
    def dump_memory(self, track: str = '0', start: int = 0, length: int = 20):
        """Dump memory contents"""
        result = []
        for i in range(length):
            addr = (start + i) % 100
            char = self.drum.read_character(track, addr)
            result.append(f"{addr:02d}: {char}")
        return '\n'.join(result)


# SHA256 Subset Implementation for IBM 305
class SHA256Subset:
    """
    Simplified SHA256 implementation adapted for IBM 305's character architecture.
    This is a subset that works with BCD characters.
    """
    
    # SHA256 constants (first 8)
    K = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
        0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5
    ]
    
    # Initial hash values
    H0 = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    ]
    
    @staticmethod
    def bcd_to_binary(bcd_string: str) -> bytes:
        """Convert BCD string to binary"""
        # Simple conversion - in real implementation would use BCD arithmetic
        return bcd_string.encode('ascii')
    
    @staticmethod
    def binary_to_bcd(data: bytes) -> str:
        """Convert binary to BCD string"""
        # Simple conversion
        return data.hex().upper()
    
    @classmethod
    def hash(cls, message: str) -> str:
        """
        Compute simplified SHA256 hash of BCD message.
        Returns hash as BCD-compatible hex string.
        """
        # Convert BCD message to binary
        binary_msg = cls.bcd_to_binary(message)
        
        # Use standard SHA256 (in real implementation, would use BCD operations)
        hash_obj = hashlib.sha256(binary_msg)
        hash_bytes = hash_obj.digest()
        
        # Convert back to BCD-compatible format
        return cls.binary_to_bcd(hash_bytes)


# Example usage and testing
if __name__ == '__main__':
    print("=" * 60)
    print("IBM 305 RAMAC Simulator")
    print("=" * 60)
    
    # Create simulator
    sim = IBM305Simulator()
    
    # Load a simple test program
    test_program = [
        "000000001   ",  # Clear accumulator
        "001L00205   ",  # Load 5 chars from track 0 addr 1 to accumulator
        "000000005   ",  # Copy operation
        "00000000P   ",  # Halt
    ]
    
    # Initialize some data
    sim.drum.write_field('0', 1, "HELLO")
    
    # Load and run program
    sim.load_program(test_program)
    print("\nLoaded test program")
    print("Initial memory at track 0, addr 1-5:")
    print(sim.dump_memory('0', 1, 5))
    
    print("\nRunning program...")
    stats = sim.run(max_instructions=100)
    
    print("\nExecution Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n" + "=" * 60)
    print("SHA256 Subset Test")
    print("=" * 60)
    
    # Test SHA256 subset
    test_message = "IBM305RAMAC1956"
    hash_result = SHA256Subset.hash(test_message)
    print(f"Message: {test_message}")
    print(f"SHA256:  {hash_result}")
    
    print("\n" + "=" * 60)
    print("Simulator ready for IBM 305 RAMAC miner development")
    print("=" * 60)
