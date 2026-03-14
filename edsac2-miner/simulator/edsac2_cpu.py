#!/usr/bin/env python3
"""
EDSAC 2 CPU Simulator
=====================
A Python simulator for the EDSAC 2 computer (1958).

EDSAC 2 was the first microprogrammed computer, featuring:
- 40-bit word length
- Magnetic core memory (1024 words RAM, 768 words ROM)
- 20-bit instructions with 11-bit addresses
- 2 index registers (B1, B2)
- Microprogrammed control unit

Author: RustChain EDSAC 2 Miner Project
License: MIT
"""

import sys
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import IntEnum
import struct


class InstructionSet(IntEnum):
    """EDSAC 2 Instruction Set"""
    STOP = 0x00
    ADD = 0x01
    SUB = 0x02
    MUL = 0x03
    DIV = 0x04
    AND = 0x05
    OR = 0x06
    XOR = 0x07
    SHL = 0x08
    SHR = 0x09
    JMP = 0x0A
    JZ = 0x0B
    JN = 0x0C
    LD = 0x0D
    ST = 0x0E
    IN = 0x0F
    OUT = 0x10
    IDX1 = 0x11  # Use index register B1
    IDX2 = 0x12  # Use index register B2


@dataclass
class Instruction:
    """Represents a single EDSAC 2 instruction"""
    opcode: int       # 5 bits (0-31)
    index: int        # 2 bits (0-3): 0=none, 1=B1, 2=B2, 3=reserved
    address: int      # 11 bits (0-2047)
    length: int       # 2 bits: 01=single word (40-bit), 10=double word (80-bit)
    
    @classmethod
    def from_word(cls, word: int) -> 'Instruction':
        """Decode a 40-bit word into an instruction"""
        # Instruction format: [opcode:5][index:2][address:11][length:2][unused:20]
        opcode = (word >> 35) & 0x1F
        index = (word >> 33) & 0x03
        address = (word >> 22) & 0x7FF
        length = (word >> 20) & 0x03
        return cls(opcode=opcode, index=index, address=address, length=length)
    
    def to_word(self) -> int:
        """Encode instruction into a 40-bit word"""
        word = 0
        word |= (self.opcode & 0x1F) << 35
        word |= (self.index & 0x03) << 33
        word |= (self.address & 0x7FF) << 22
        word |= (self.length & 0x03) << 20
        return word
    
    def __str__(self) -> str:
        opname = InstructionSet(self.opcode).name if self.opcode <= 0x12 else f"UNKNOWN({self.opcode})"
        idx_str = ["", "B1", "B2", "RES"][self.index]
        len_str = ["WORD", "DOUBLE", "RES", "RES"][self.length]
        return f"{opname:6s} {idx_str:3s} {self.address:04X}h {len_str}"


@dataclass
class MagneticCoreMemory:
    """
    Magnetic Core Memory Model for EDSAC 2
    
    Features:
    - 1024 words RAM (40 bits each)
    - 768 words ROM (microcode)
    - Destructive read (requires rewrite)
    - Non-volatile (retains data without power)
    """
    ram_size: int = 1024
    rom_size: int = 768
    
    # Main memory (RAM)
    ram: List[int] = field(default_factory=lambda: [0] * 1024)
    
    # Read-only memory (ROM) for microcode
    rom: List[int] = field(default_factory=lambda: [0] * 768)
    
    # Memory access statistics
    read_count: int = 0
    write_count: int = 0
    
    # Destructive read flag
    destructive_read: bool = True
    
    # Last read value (for rewrite)
    last_read_addr: Optional[int] = None
    last_read_value: Optional[int] = None
    
    def read(self, address: int, rewrite: bool = True) -> int:
        """
        Read a word from memory.
        
        Magnetic core memory has destructive read:
        reading a word destroys its contents, so it
        must be rewritten immediately.
        """
        if address < 0 or address >= self.ram_size:
            raise ValueError(f"Memory access violation: address {address} out of range")
        
        value = self.ram[address]
        self.read_count += 1
        
        # Store for potential rewrite
        self.last_read_addr = address
        self.last_read_value = value
        
        return value
    
    def write(self, address: int, value: int):
        """Write a word to memory"""
        if address < 0 or address >= self.ram_size:
            raise ValueError(f"Memory access violation: address {address} out of range")
        
        # Mask to 40 bits
        value = value & 0xFFFFFFFFFF
        self.ram[address] = value
        self.write_count += 1
        
        # If we're rewriting the last read address, clear the destructive read flag
        if self.last_read_addr == address:
            self.last_read_addr = None
            self.last_read_value = None
    
    def read_rom(self, address: int) -> int:
        """Read from ROM (microcode storage)"""
        if address < 0 or address >= self.rom_size:
            raise ValueError(f"ROM access violation: address {address} out of range")
        return self.rom[address]
    
    def load_program(self, program: List[int], start_addr: int = 0):
        """Load a program into memory"""
        for i, word in enumerate(program):
            if start_addr + i < self.ram_size:
                self.ram[start_addr + i] = word & 0xFFFFFFFFFF
    
    def dump(self, start: int = 0, count: int = 32) -> str:
        """Dump memory contents as hex"""
        lines = []
        for i in range(count):
            addr = start + i
            if addr < self.ram_size:
                value = self.ram[addr]
                lines.append(f"{addr:04X}: {value:010X}")
        return "\n".join(lines)


@dataclass
class EDSAC2CPU:
    """
    EDSAC 2 CPU Simulator
    
    Registers:
    - ACC: 40-bit accumulator
    - PC: 11-bit program counter
    - B1: 40-bit index register 1
    - B2: 40-bit index register 2
    - IR: 40-bit instruction register
    - STATUS: Status flags (zero, negative, overflow)
    """
    
    # 40-bit registers
    acc: int = 0          # Accumulator
    b1: int = 0           # Index register 1
    b2: int = 0           # Index register 2
    ir: int = 0           # Instruction register
    
    # Program counter (11 bits)
    pc: int = 0
    
    # Status flags
    zero: bool = False
    negative: bool = False
    overflow: bool = False
    
    # Control
    running: bool = False
    halted: bool = False
    
    # Memory
    memory: MagneticCoreMemory = field(default_factory=MagneticCoreMemory)
    
    # Statistics
    instructions_executed: int = 0
    cycles: int = 0
    
    # I/O
    input_buffer: List[int] = field(default_factory=list)
    output_buffer: List[int] = field(default_factory=list)
    
    # Callbacks
    on_halt: Optional[callable] = None
    on_output: Optional[callable] = None
    
    MASK_40 = 0xFFFFFFFFFF  # 40-bit mask
    MASK_11 = 0x7FF         # 11-bit mask (for PC)
    SIGN_BIT = 1 << 39      # Sign bit position
    
    def reset(self):
        """Reset CPU to initial state"""
        self.acc = 0
        self.b1 = 0
        self.b2 = 0
        self.ir = 0
        self.pc = 0
        self.zero = False
        self.negative = False
        self.overflow = False
        self.running = False
        self.halted = False
        self.instructions_executed = 0
        self.cycles = 0
        self.input_buffer = []
        self.output_buffer = []
    
    def sign_extend(self, value: int, bits: int = 40) -> int:
        """Sign-extend a value to 40 bits"""
        sign_bit = 1 << (bits - 1)
        mask = (1 << bits) - 1
        value = value & mask
        if value & sign_bit:
            return value | ~mask
        return value
    
    def is_negative(self, value: int) -> bool:
        """Check if a 40-bit value is negative"""
        return bool(value & self.SIGN_BIT)
    
    def update_flags(self, value: int):
        """Update status flags based on result"""
        value = value & self.MASK_40
        self.zero = (value == 0)
        self.negative = self.is_negative(value)
    
    def effective_address(self, instr: Instruction) -> int:
        """Calculate effective address using index registers"""
        base_addr = instr.address
        
        if instr.index == 1:  # B1
            base_addr = (base_addr + self.b1) & self.MASK_11
        elif instr.index == 2:  # B2
            base_addr = (base_addr + self.b2) & self.MASK_11
        
        return base_addr
    
    def fetch(self) -> Instruction:
        """Fetch instruction from memory"""
        word = self.memory.read(self.pc)
        self.ir = word
        instr = Instruction.from_word(word)
        
        # Increment PC
        self.pc = (self.pc + 1) & self.MASK_11
        
        return instr
    
    def execute(self, instr: Instruction) -> int:
        """
        Execute a single instruction.
        Returns number of cycles used.
        """
        cycles = 17  # Base cycle time (μs)
        eff_addr = self.effective_address(instr)
        
        op = instr.opcode
        
        if op == InstructionSet.STOP:
            self.halted = True
            self.running = False
            if self.on_halt:
                self.on_halt()
            return cycles
        
        elif op == InstructionSet.ADD:
            value = self.memory.read(eff_addr)
            self.acc = (self.acc + value) & self.MASK_40
            self.update_flags(self.acc)
            cycles = 42  # Addition takes 17-42 μs
        
        elif op == InstructionSet.SUB:
            value = self.memory.read(eff_addr)
            self.acc = (self.acc - value) & self.MASK_40
            self.update_flags(self.acc)
            cycles = 42
        
        elif op == InstructionSet.MUL:
            # Microprogrammed multiplication
            value = self.memory.read(eff_addr)
            # Simplified: actual implementation would use microcode
            self.acc = (self.acc * value) & self.MASK_40
            self.update_flags(self.acc)
            cycles = 200  # Multiplication is slower
        
        elif op == InstructionSet.DIV:
            # Microprogrammed division
            value = self.memory.read(eff_addr)
            if value != 0:
                self.acc = (self.acc // value) & self.MASK_40
            self.update_flags(self.acc)
            cycles = 300  # Division is even slower
        
        elif op == InstructionSet.AND:
            value = self.memory.read(eff_addr)
            self.acc = (self.acc & value) & self.MASK_40
            self.update_flags(self.acc)
        
        elif op == InstructionSet.OR:
            value = self.memory.read(eff_addr)
            self.acc = (self.acc | value) & self.MASK_40
            self.update_flags(self.acc)
        
        elif op == InstructionSet.XOR:
            value = self.memory.read(eff_addr)
            self.acc = (self.acc ^ value) & self.MASK_40
            self.update_flags(self.acc)
        
        elif op == InstructionSet.SHL:
            # Shift left by amount in address field
            shift = eff_addr & 0x3F  # Max 63 bits
            self.acc = (self.acc << shift) & self.MASK_40
            self.update_flags(self.acc)
        
        elif op == InstructionSet.SHR:
            # Arithmetic shift right
            shift = eff_addr & 0x3F
            sign = self.acc & self.SIGN_BIT
            self.acc = (self.acc >> shift) | sign
            self.update_flags(self.acc)
        
        elif op == InstructionSet.JMP:
            self.pc = eff_addr
            cycles = 25  # Jump takes extra cycles
        
        elif op == InstructionSet.JZ:
            if self.zero:
                self.pc = eff_addr
                cycles = 25
        
        elif op == InstructionSet.JN:
            if self.negative:
                self.pc = eff_addr
                cycles = 25
        
        elif op == InstructionSet.LD:
            value = self.memory.read(eff_addr)
            self.acc = value
            self.update_flags(self.acc)
        
        elif op == InstructionSet.ST:
            self.memory.write(eff_addr, self.acc)
        
        elif op == InstructionSet.IN:
            # Input from paper tape
            if self.input_buffer:
                self.acc = self.input_buffer.pop(0)
                self.update_flags(self.acc)
        
        elif op == InstructionSet.OUT:
            # Output to paper tape
            self.output_buffer.append(self.acc & 0xFF)
            if self.on_output:
                self.on_output(self.acc & 0xFF)
        
        elif op == InstructionSet.IDX1:
            # Load index register B1
            self.b1 = self.memory.read(eff_addr)
        
        elif op == InstructionSet.IDX2:
            # Load index register B2
            self.b2 = self.memory.read(eff_addr)
        
        else:
            # Unknown instruction
            print(f"WARNING: Unknown opcode {op:02X} at PC={self.pc:04X}")
        
        self.instructions_executed += 1
        self.cycles += cycles
        return cycles
    
    def step(self) -> int:
        """Execute a single instruction cycle"""
        if self.halted:
            return 0
        
        instr = self.fetch()
        cycles = self.execute(instr)
        return cycles
    
    def run(self, max_instructions: int = 0) -> int:
        """
        Run the CPU until halted or max_instructions reached.
        
        Args:
            max_instructions: Maximum instructions to execute (0 = unlimited)
        
        Returns:
            Total instructions executed
        """
        self.running = True
        self.halted = False
        
        count = 0
        while self.running and not self.halted:
            if max_instructions > 0 and count >= max_instructions:
                break
            
            self.step()
            count += 1
        
        return count
    
    def load_program(self, program: List[int], start_addr: int = 0):
        """Load a program into memory"""
        self.memory.load_program(program, start_addr)
    
    def get_state(self) -> Dict:
        """Get CPU state as dictionary"""
        return {
            'PC': self.pc,
            'ACC': self.acc,
            'B1': self.b1,
            'B2': self.b2,
            'IR': self.ir,
            'ZERO': self.zero,
            'NEGATIVE': self.negative,
            'OVERFLOW': self.overflow,
            'RUNNING': self.running,
            'HALTED': self.halted,
            'INSTRUCTIONS': self.instructions_executed,
            'CYCLES': self.cycles,
        }
    
    def __str__(self) -> str:
        state = self.get_state()
        return (
            f"EDSAC 2 CPU State:\n"
            f"  PC:   {state['PC']:04X}\n"
            f"  ACC:  {state['ACC']:010X}\n"
            f"  B1:   {state['B1']:010X}\n"
            f"  B2:   {state['B2']:010X}\n"
            f"  IR:   {state['IR']:010X}\n"
            f"  Flags: Z={state['ZERO']} N={state['NEGATIVE']} V={state['OVERFLOW']}\n"
            f"  Status: {'HALTED' if state['HALTED'] else 'RUNNING' if state['RUNNING'] else 'STOPPED'}\n"
            f"  Instructions: {state['INSTRUCTIONS']}\n"
            f"  Cycles: {state['CYCLES']}"
        )


def assemble(source: str) -> List[int]:
    """
    Simple assembler for EDSAC 2.
    
    Supports:
    - Labels (name:)
    - Instructions (ADD, SUB, etc.)
    - Comments (# or //)
    - Numeric literals (decimal or 0x hex)
    - Index register specification (,B1 or ,B2)
    
    Example:
        START:  LD  DATA      # Load data
                ADD CONST,B1  # Add with index
                ST  RESULT
                STOP
        DATA:   100
        CONST:  5
        RESULT: 0
    """
    
    # Instruction mnemonics
    mnemonics = {
        'STOP': 0x00, 'ADD': 0x01, 'SUB': 0x02, 'MUL': 0x03, 'DIV': 0x04,
        'AND': 0x05, 'OR': 0x06, 'XOR': 0x07, 'SHL': 0x08, 'SHR': 0x09,
        'JMP': 0x0A, 'JZ': 0x0B, 'JN': 0x0C, 'LD': 0x0D, 'ST': 0x0E,
        'IN': 0x0F, 'OUT': 0x10, 'IDX1': 0x11, 'IDX2': 0x12,
    }
    
    lines = source.split('\n')
    symbols: Dict[str, int] = {}
    
    # First pass: collect labels and count addresses
    addr = 0
    for line in lines:
        # Remove comments
        line = line.split('#')[0].split('//')[0].strip()
        if not line:
            continue
        
        # Check for label
        if ':' in line:
            parts = line.split(':', 1)
            label = parts[0].strip()
            symbols[label] = addr
            line = parts[1].strip() if len(parts) > 1 else ''
            if not line:
                continue
        
        # Count this as taking an address
        addr += 1
    
    # Second pass: generate code
    program = []
    for line in lines:
        line = line.split('#')[0].split('//')[0].strip()
        if not line:
            continue
        
        # Handle label
        if ':' in line:
            parts = line.split(':', 1)
            line = parts[1].strip() if len(parts) > 1 else ''
            if not line:
                continue
        
        # Handle data (numeric literal)
        try:
            if line.startswith('0x'):
                value = int(line, 16)
            else:
                value = int(line)
            program.append(value & 0xFFFFFFFFFF)
            continue
        except ValueError:
            pass
        
        # Parse instruction
        parts = line.replace(',', ' ').split()
        if not parts:
            continue
        
        mnemonic = parts[0].upper()
        if mnemonic not in mnemonics:
            print(f"WARNING: Unknown mnemonic '{mnemonic}' at line {line}")
            continue
        
        opcode = mnemonics[mnemonic]
        index = 0
        operand = 0
        
        # Parse operand and index register
        if len(parts) > 1:
            operand_str = parts[1]
            if operand_str.upper() in ['B1', 'B2']:
                index = 1 if operand_str.upper() == 'B1' else 2
            else:
                # Check for indexed operand
                if len(parts) > 2 and parts[2].upper() in ['B1', 'B2']:
                    index = 1 if parts[2].upper() == 'B1' else 2
                
                # Resolve symbol or number
                if operand_str in symbols:
                    operand = symbols[operand_str]
                else:
                    try:
                        operand = int(operand_str, 0)  # Auto-detect hex/decimal
                    except ValueError:
                        print(f"WARNING: Unknown operand '{operand_str}'")
        
        # Encode instruction
        word = 0
        word |= (opcode & 0x1F) << 35
        word |= (index & 0x03) << 33
        word |= (operand & 0x7FF) << 22
        word |= 0x01 << 20  # Single word length
        
        program.append(word)
    
    return program


def main():
    """Main entry point for EDSAC 2 simulator"""
    import argparse
    
    parser = argparse.ArgumentParser(description='EDSAC 2 CPU Simulator')
    parser.add_argument('--program', '-p', type=str, help='Assembly program file')
    parser.add_argument('--load', '-l', type=str, help='Load binary program file')
    parser.add_argument('--run', '-r', action='store_true', help='Run program after loading')
    parser.add_argument('--max-instr', '-m', type=int, default=0, help='Max instructions to execute')
    parser.add_argument('--demo', '-d', action='store_true', help='Run demo program')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    cpu = EDSAC2CPU()
    
    # Demo program
    if args.demo:
        print("Running EDSAC 2 Demo Program")
        print("=" * 50)
        
        demo_source = """
        # EDSAC 2 Demo: Sum numbers 1 to 10
        START:  LD   COUNT      # Load counter
                JZ   DONE       # If zero, done
                LD   SUM        # Load sum
                ADD  COUNT      # Add counter
                ST   SUM        # Store sum
                LD   COUNT      # Load counter
                SUB  ONE        # Decrement
                ST   COUNT      # Store counter
                JMP  START      # Loop
        DONE:   LD   SUM        # Load final sum
                OUT             # Output result
                STOP
        COUNT:  10
        SUM:    0
        ONE:    1
        """
        
        program = assemble(demo_source)
        cpu.load_program(program)
        
        if args.verbose:
            print("Program loaded:")
            print(cpu.memory.dump(0, len(program)))
            print()
        
        cpu.run(max_instructions=args.max_instr or 1000)
        
        print()
        print(cpu)
        print()
        print(f"Output: {cpu.output_buffer}")
        print(f"Sum of 1 to 10 = {cpu.output_buffer[0] if cpu.output_buffer else 'N/A'}")
        return
    
    # Load assembly program
    if args.program:
        print(f"Loading assembly program: {args.program}")
        with open(args.program, 'r') as f:
            source = f.read()
        program = assemble(source)
        cpu.load_program(program)
        print(f"Loaded {len(program)} words")
    
    # Load binary program
    if args.load:
        print(f"Loading binary program: {args.load}")
        with open(args.load, 'rb') as f:
            data = f.read()
        program = []
        for i in range(0, len(data), 5):
            if i + 5 <= len(data):
                word = int.from_bytes(data[i:i+5], 'big')
                program.append(word)
        cpu.load_program(program)
        print(f"Loaded {len(program)} words")
    
    # Run program
    if args.run:
        print("Running program...")
        cpu.run(max_instructions=args.max_instr or 10000)
        print()
        print(cpu)
        if cpu.output_buffer:
            print(f"Output: {cpu.output_buffer}")
    
    # Interactive mode if nothing specified
    if not (args.program or args.load or args.demo or args.run):
        print("EDSAC 2 Simulator - Interactive Mode")
        print("Commands: step, run, dump, regs, load, quit")
        print()
        
        while True:
            try:
                cmd = input("edsac2> ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            
            if cmd == 'quit' or cmd == 'q':
                break
            elif cmd == 'step' or cmd == 's':
                cycles = cpu.step()
                print(f"Executed instruction at PC={cpu.pc-1:04X}, cycles={cycles}")
            elif cmd == 'run' or cmd == 'r':
                count = cpu.run(max_instructions=1000)
                print(f"Executed {count} instructions")
            elif cmd == 'dump' or cmd == 'd':
                print(cpu.memory.dump(0, 32))
            elif cmd == 'regs' or cmd == 'r':
                print(cpu)
            elif cmd.startswith('load '):
                addr = int(cmd.split()[1], 0)
                value = int(cmd.split()[2], 0)
                cpu.memory.write(addr, value)
                print(f"Memory[{addr:04X}] = {value:010X}")
            else:
                print(f"Unknown command: {cmd}")


if __name__ == '__main__':
    main()
