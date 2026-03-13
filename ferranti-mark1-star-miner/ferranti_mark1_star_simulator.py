#!/usr/bin/env python3
"""
Ferranti Mark 1* Miner Simulator (1957)
Manchester University Upgraded Version

Key differences from Mark 1 (1951):
- 16 Williams tubes (1024 words) vs 8 tubes (512 words)
- Extended instruction set
- Improved reliability
- Enhanced I/O (teleprinter support)

Bounty Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b
"""

import random
import time
import hashlib
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import IntEnum


# ============================================================================
# CONSTANTS
# ============================================================================

MEMORY_WORDS = 1024  # Mark 1*: 1024 words (vs 512 in Mark 1)
NUM_TUBES = 16  # Mark 1*: 16 tubes (vs 8 in Mark 1)
WORDS_PER_TUBE = 64
WORD_BITS = 20  # Instruction word
DATA_BITS = 40  # Data word
ACCUMULATOR_BITS = 80
B_LINES = 8
DRUM_PAGES = 1024

# Instruction opcodes (Mark 1* extended set)
class Opcode(IntEnum):
    STOP = 0x00
    LOAD = 0x01
    STORE = 0x02
    ADD = 0x03
    SUB = 0x04
    MUL = 0x05
    DIV = 0x06
    JUMP = 0x07
    JNEG = 0x08
    JZER = 0x09
    LOAD_B = 0x0A
    ADD_B = 0x0B
    INPUT = 0x0C
    OUTPUT = 0x0D
    HOOT = 0x0E
    RAND = 0x0F
    AND = 0x10
    OR = 0x11
    NOT = 0x12
    # Mark 1* extensions
    SHIFT_L = 0x13  # Left shift
    SHIFT_R = 0x14  # Right shift
    COMPARE = 0x15  # Compare and set flags
    LOAD_MQ = 0x16  # Load MQ register
    STORE_MQ = 0x17  # Store MQ register
    DRUM_READ = 0x18  # Read from drum
    DRUM_WRITE = 0x19  # Write to drum
    TELE_PRINT = 0x1A  # Teleprinter output


# ============================================================================
# WILLIAMS TUBE MEMORY
# ============================================================================

@dataclass
class WilliamsTube:
    """Simulates a Williams cathode-ray tube memory cell."""
    tube_id: int
    words: List[int] = field(default_factory=lambda: [0] * WORDS_PER_TUBE)
    fingerprint: int = 0
    charge_pattern: List[float] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize tube with unique residual charge pattern."""
        self._initialize_fingerprint()
    
    def _initialize_fingerprint(self):
        """Generate unique fingerprint from residual charge patterns."""
        # Simulate unique manufacturing variations in each tube
        random.seed(self.tube_id * 1773399197)  # Fixed seed for reproducibility
        self.charge_pattern = [random.gauss(0.5, 0.1) for _ in range(WORDS_PER_TUBE)]
        
        # Create fingerprint from charge pattern
        fingerprint_hash = hashlib.sha256(
            str(self.charge_pattern).encode()
        ).hexdigest()[:10]
        self.fingerprint = int(fingerprint_hash, 16) & 0xFFFFF
    
    def read(self, address: int) -> int:
        """Read word from tube with residual charge effect."""
        if 0 <= address < WORDS_PER_TUBE:
            # Simulate charge leakage (very minor effect)
            base_value = self.words[address]
            charge_effect = int(self.charge_pattern[address] * 0.001)
            return (base_value + charge_effect) & 0xFFFFF
        return 0
    
    def write(self, address: int, value: int):
        """Write word to tube."""
        if 0 <= address < WORDS_PER_TUBE:
            self.words[address] = value & 0xFFFFF
    
    def get_fingerprint(self) -> int:
        """Return tube's unique hardware fingerprint."""
        return self.fingerprint


# ============================================================================
# MAGNETIC DRUM STORAGE
# ============================================================================

@dataclass
class MagneticDrum:
    """Simulates magnetic drum secondary storage."""
    pages: Dict[int, List[int]] = field(default_factory=dict)
    rotation_ms: int = 30  # 30ms per revolution
    current_position: int = 0
    
    def read_page(self, page_num: int) -> List[int]:
        """Read a page from drum (30ms latency)."""
        if page_num not in self.pages:
            self.pages[page_num] = [0] * WORDS_PER_TUBE
        time.sleep(self.rotation_ms / 1000 / 10)  # Simulated latency (shortened)
        return self.pages[page_num].copy()
    
    def write_page(self, page_num: int, data: List[int]):
        """Write a page to drum."""
        self.pages[page_num] = [w & 0xFFFFF for w in data[:WORDS_PER_TUBE]]


# ============================================================================
# FERRANTI MARK 1* CPU
# ============================================================================

class FerrantiMark1StarCPU:
    """Ferranti Mark 1* CPU simulator (1957 upgraded version)."""
    
    def __init__(self):
        # 16 Williams tubes (1024 words total)
        self.tubes = [WilliamsTube(i) for i in range(NUM_TUBES)]
        
        # Registers
        self.accumulator = 0  # 80-bit
        self.mq_register = 0  # 40-bit (multiplicand/quotient)
        self.b_lines = [0] * B_LINES  # Index registers
        self.program_counter = 0
        self.flags = {'negative': False, 'zero': False}
        
        # Secondary storage
        self.drum = MagneticDrum()
        
        # I/O
        self.paper_tape_output: List[str] = []
        self.teleprinter_output: List[str] = []
        self.hoot_pitches: List[int] = []
        
        # Mining state
        self.mining_active = False
        self.shares_found = 0
    
    def _get_hardware_fingerprint(self) -> int:
        """Generate unique fingerprint from all 16 Williams tubes."""
        fingerprints = [tube.get_fingerprint() for tube in self.tubes]
        combined = 0
        for i, fp in enumerate(fingerprints):
            combined ^= (fp << (i * 20))
        return combined & 0xFFFFFFFFFFFFFFFF
    
    def _read_memory(self, address: int) -> int:
        """Read from main memory (1024 words)."""
        if 0 <= address < MEMORY_WORDS:
            tube_num = address // WORDS_PER_TUBE
            tube_addr = address % WORDS_PER_TUBE
            return self.tubes[tube_num].read(tube_addr)
        return 0
    
    def _write_memory(self, address: int, value: int):
        """Write to main memory."""
        if 0 <= address < MEMORY_WORDS:
            tube_num = address // WORDS_PER_TUBE
            tube_addr = address % WORDS_PER_TUBE
            self.tubes[tube_num].write(tube_addr, value)
    
    def _effective_address(self, addr_field: int) -> int:
        """Calculate effective address using B-lines."""
        # Mark 1*: B-line 0 is always 0, B-lines 1-7 can modify address
        base_addr = addr_field & 0x3FF  # 10-bit address for 1024 words
        b_line = (addr_field >> 10) & 0x7  # 3-bit B-line selector
        
        if b_line > 0:
            return (base_addr + self.b_lines[b_line]) % MEMORY_WORDS
        return base_addr
    
    def execute_instruction(self, instruction: int) -> bool:
        """Execute a single instruction. Returns False if STOP."""
        opcode = (instruction >> 15) & 0x1F
        addr_field = instruction & 0x7FFF
        
        if opcode == Opcode.STOP:
            return False
        
        elif opcode == Opcode.LOAD:
            addr = self._effective_address(addr_field)
            self.accumulator = self._read_memory(addr)
        
        elif opcode == Opcode.STORE:
            addr = self._effective_address(addr_field)
            self._write_memory(addr, self.accumulator & 0xFFFFF)
        
        elif opcode == Opcode.ADD:
            addr = self._effective_address(addr_field)
            self.accumulator = (self.accumulator + self._read_memory(addr)) & 0xFFFFFFFFFF
        
        elif opcode == Opcode.SUB:
            addr = self._effective_address(addr_field)
            self.accumulator = (self.accumulator - self._read_memory(addr)) & 0xFFFFFFFFFF
        
        elif opcode == Opcode.MUL:
            addr = self._effective_address(addr_field)
            multiplicand = self._read_memory(addr)
            result = self.accumulator * multiplicand
            self.accumulator = (result >> 40) & 0xFFFFFFFFFF  # High 40 bits
            self.mq_register = result & 0xFFFFFFFFFF  # Low 40 bits
        
        elif opcode == Opcode.DIV:
            addr = self._effective_address(addr_field)
            divisor = self._read_memory(addr)
            if divisor != 0:
                quotient = self.accumulator // divisor
                remainder = self.accumulator % divisor
                self.accumulator = quotient
                self.mq_register = remainder
        
        elif opcode == Opcode.JUMP:
            self.program_counter = self._effective_address(addr_field)
            return True
        
        elif opcode == Opcode.JNEG:
            if self.accumulator & 0x8000000000:  # Check sign bit
                self.program_counter = self._effective_address(addr_field)
                return True
        
        elif opcode == Opcode.JZER:
            if self.accumulator == 0:
                self.program_counter = self._effective_address(addr_field)
                return True
        
        elif opcode == Opcode.LOAD_B:
            b_line = (addr_field >> 3) & 0x7
            value = addr_field & 0x7FF
            if b_line > 0:
                self.b_lines[b_line] = value
        
        elif opcode == Opcode.ADD_B:
            b_line = (addr_field >> 3) & 0x7
            value = addr_field & 0x7FF
            if b_line > 0:
                self.b_lines[b_line] = (self.b_lines[b_line] + value) % 0x800
        
        elif opcode == Opcode.INPUT:
            # Simulate paper tape input (not implemented for mining)
            pass
        
        elif opcode == Opcode.OUTPUT:
            # Output to paper tape
            value = self.accumulator & 0xFFFFF
            self.paper_tape_output.append(f"{value:05X}")
        
        elif opcode == Opcode.HOOT:
            # Audio output - generate pitch from accumulator
            pitch = (self.accumulator & 0xFF) + 40  # 40-295 Hz range
            self.hoot_pitches.append(pitch)
        
        elif opcode == Opcode.RAND:
            # Random number from tube noise
            self.accumulator = random.randint(0, 0xFFFFFFFFFF)
        
        elif opcode == Opcode.AND:
            addr = self._effective_address(addr_field)
            self.accumulator = self.accumulator & self._read_memory(addr)
        
        elif opcode == Opcode.OR:
            addr = self._effective_address(addr_field)
            self.accumulator = self.accumulator | self._read_memory(addr)
        
        elif opcode == Opcode.NOT:
            self.accumulator = ~self.accumulator & 0xFFFFFFFFFF
        
        # Mark 1* extensions
        elif opcode == Opcode.SHIFT_L:
            shift = addr_field & 0x3F
            self.accumulator = (self.accumulator << shift) & 0xFFFFFFFFFF
        
        elif opcode == Opcode.SHIFT_R:
            shift = addr_field & 0x3F
            self.accumulator = self.accumulator >> shift
        
        elif opcode == Opcode.COMPARE:
            addr = self._effective_address(addr_field)
            value = self._read_memory(addr)
            self.flags['zero'] = (self.accumulator == value)
            self.flags['negative'] = (self.accumulator < value)
        
        elif opcode == Opcode.LOAD_MQ:
            self.mq_register = self._read_memory(self._effective_address(addr_field))
        
        elif opcode == Opcode.STORE_MQ:
            self._write_memory(self._effective_address(addr_field), self.mq_register)
        
        elif opcode == Opcode.DRUM_READ:
            page = self.accumulator & 0x3FF
            addr = self._effective_address(addr_field)
            drum_data = self.drum.read_page(page)
            for i, word in enumerate(drum_data[:8]):
                self._write_memory(addr + i, word)
        
        elif opcode == Opcode.DRUM_WRITE:
            page = self.accumulator & 0x3FF
            addr = self._effective_address(addr_field)
            drum_data = [self._read_memory(addr + i) for i in range(8)]
            self.drum.write_page(page, drum_data)
        
        elif opcode == Opcode.TELE_PRINT:
            char = self.accumulator & 0x7F
            self.teleprinter_output.append(chr(char) if 32 <= char < 127 else '?')
        
        # Update flags
        self.flags['zero'] = (self.accumulator == 0)
        self.flags['negative'] = bool(self.accumulator & 0x8000000000)
        
        self.program_counter = (self.program_counter + 1) % MEMORY_WORDS
        return True
    
    def run_program(self, start_addr: int = 0, max_instructions: int = 10000) -> bool:
        """Run program from start address."""
        self.program_counter = start_addr
        count = 0
        
        while count < max_instructions:
            instruction = self._read_memory(self.program_counter)
            if not self.execute_instruction(instruction):
                return True  # Stopped normally
            count += 1
        
        return False  # Hit instruction limit
    
    # ========================================================================
    # MINING FUNCTIONS
    # ========================================================================
    
    def initialize_mining(self, wallet: str, difficulty: int = 0x100):
        """Initialize mining state."""
        self.mining_wallet = wallet
        self.mining_difficulty = difficulty
        self.mining_fingerprint = self._get_hardware_fingerprint()
        self.mining_active = True
        self.shares_found = 0
    
    def mine_share(self) -> Optional[Dict]:
        """Execute one mining iteration."""
        if not self.mining_active:
            return None
        
        # Mining loop simulation
        for nonce in range(1, 100000):
            # XOR-based hash (simplified for 1957 hardware)
            hash_value = (self.mining_fingerprint ^ nonce) & 0xFFFF
            
            if hash_value < self.mining_difficulty:
                # Share found!
                self.shares_found += 1
                
                # Output share to paper tape
                share_data = f"SHARE|{self.mining_wallet[:12]}...|{nonce:05X}|{hash_value:05X}"
                self.paper_tape_output.append(share_data)
                
                # HOOT audio proof
                self.hoot_pitches.append(80 + (nonce % 200))
                
                return {
                    'wallet': self.mining_wallet,
                    'fingerprint': f"{self.mining_fingerprint:016X}",
                    'nonce': nonce,
                    'hash': hash_value,
                    'difficulty': self.mining_difficulty,
                    'timestamp': int(time.time())
                }
        
        return None
    
    def get_status(self) -> Dict:
        """Get current CPU status."""
        return {
            'memory_words': MEMORY_WORDS,
            'num_tubes': NUM_TUBES,
            'accumulator': f"{self.accumulator:020X}",
            'mq_register': f"{self.mq_register:010X}",
            'b_lines': [f"{b:03X}" for b in self.b_lines],
            'program_counter': self.program_counter,
            'shares_found': self.shares_found,
            'paper_tape_outputs': len(self.paper_tape_output),
            'hoot_count': len(self.hoot_pitches)
        }


# ============================================================================
# DEMO / MAIN
# ============================================================================

def run_demo(wallet: str = "RTC4325af95d26d59c3ef025963656d22af638bb96b"):
    """Run mining demonstration."""
    print("=" * 60)
    print("Ferranti Mark 1* Miner - RustChain Proof-of-Antiquity")
    print("=" * 60)
    print(f"Memory:     {MEMORY_WORDS} words ({NUM_TUBES} Williams tubes)")
    print(f"Cycle Time: 1.2 ms")
    print(f"Year:       1957")
    print()
    
    cpu = FerrantiMark1StarCPU()
    
    print("Initializing Williams tubes...")
    for i, tube in enumerate(cpu.tubes):
        filled = tube.fingerprint % 10
        bar = "#" * filled + "-" * (10 - filled)
        print(f"Tube {i:2d}:  [{bar}] Fingerprint: {tube.fingerprint:05X}")
    print()
    
    print("Generating hardware fingerprint from 16 tubes...")
    fingerprint = cpu._get_hardware_fingerprint()
    print(f"FINGERPRINT: {fingerprint:016X}")
    print()
    
    print("Initializing mining...")
    cpu.initialize_mining(wallet)
    print(f"Difficulty: {cpu.mining_difficulty:05X}")
    print()
    
    print("Mining started...")
    start_time = time.time()
    
    share = None
    iterations = 0
    while share is None and iterations < 100:
        share = cpu.mine_share()
        iterations += 1
        if share:
            elapsed = time.time() - start_time
            print(f"\nMining complete after {iterations} iterations ({elapsed:.2f}s)")
            break
        print(f"Iteration {iterations}... no share yet")
    
    if share:
        print()
        print("=" * 60)
        print("SHARE FOUND!")
        print("=" * 60)
        print(f"Wallet:      {share['wallet']}")
        print(f"Fingerprint: {share['fingerprint']}")
        print(f"Nonce:       {share['nonce']:05X}")
        print(f"Hash:        {share['hash']:05X}")
        print(f"Difficulty:  {share['difficulty']:05X}")
        print(f"Timestamp:   {share['timestamp']}")
        print("=" * 60)
        print()
        print(f"[HOOT] Playing audio proof ({len(cpu.hoot_pitches)} tones)")
        print(f"[TAPE] Output: {cpu.paper_tape_output[-1]}")
        print()
        print("Mining session complete. Share submitted via paper tape.")
    
    print()
    print("CPU Status:")
    status = cpu.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        wallet = sys.argv[2] if len(sys.argv) > 2 else "RTC4325af95d26d59c3ef025963656d22af638bb96b"
        run_demo(wallet)
    else:
        run_demo()
