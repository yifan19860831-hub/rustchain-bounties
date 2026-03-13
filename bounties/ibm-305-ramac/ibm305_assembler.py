#!/usr/bin/env python3
"""
IBM 305 RAMAC Cross-Assembler
=============================
Assembles IBM 305 assembly language into drum memory format.

Instruction Format (10 characters):
T1 A1 B1 T2 A2 B2 M N P Q

Where:
- T1/A1/B1: Source track and address (0-99)
- T2/A2/B2: Destination track and address (0-99)
- M: Length of operand (1-9 characters)
- N: Control code (jump/condition)
- P: Reserved
- Q: Operation code
"""

import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class AssemblyInstruction:
    """Parsed assembly instruction"""
    label: Optional[str] = None
    t1: str = ' '
    a1: str = ' '
    b1: str = ' '
    t2: str = ' '
    a2: str = ' '
    b2: str = ' '
    m: str = ' '
    n: str = ' '
    p: str = ' '
    q: str = ' '
    comment: str = ''
    
    def to_machine_code(self) -> str:
        """Convert to 10-character machine code"""
        return f"{self.t1}{self.a1}{self.b1}{self.t2}{self.a2}{self.b2}{self.m}{self.n}{self.p}{self.q}"


class IBM305Assembler:
    """IBM 305 Cross-Assembler"""
    
    # Operation codes
    OPCODES = {
        'COPY': ' ',
        'NOP': ' ',
        'CMP': '1',
        'COMPARE': '1',
        'FCMP': '2',
        'FIELD_COMPARE': '2',
        'CMPFC': '3',
        'CLEAR_ACC': '5',
        'LOAD': 'L',
        'LOAD_ADD': 'L',
        'LOAD_CLEAR': 'M',
        'SUB': 'M',
        'SUBTRACT': 'M',
        'MULT': 'N',
        'MULTIPLY': 'N',
        'DIV': 'P',
        'DIVIDE': 'P',
        'CARD_IN': 'K',
        'CARD_OUT': 'S',
        'PRINT': 'T',
        'INQUIRY': 'Q',
        'DISK_ADDR': 'J',
        'DISK_IO': 'R',
        'CORE': '-',
        'TAPE': '$',
    }
    
    # Track aliases
    TRACKS = {
        'W': 'W', 'X': 'X', 'Y': 'Y', 'Z': 'Z',
        'I': 'I', 'H': 'H', 'G': 'G', 'F': 'F',
        'E': 'E', 'D': 'D', 'C': 'C', 'B': 'B',
        'A': 'A', '9': '9', '8': '8', '7': '7',
        '6': '6', '5': '5', '4': '4', '3': '3',
        '2': '2', '1': '1', '0': '0',
        'ACC': 'L', 'ACCUMULATOR': 'L',
        'BUFFER': '-', 'CORE': '-',
        'DISK': 'J', 'FILE': 'J',
        'CARD': 'K', 'PUNCH': 'S',
        'PRINTER': 'T', 'PRINT': 'T',
    }
    
    # Control codes
    CONTROL_CODES = {
        'JUMP': 'P',
        'EXIT': 'P',
        'HALT': 'P',
        'COND1': '1',
        'COND2': '2',
        'COND3': '3',
        'COND5': '5',
        'COND6': '6',
        'COND7': '7',
        'COND8': '8',
        'COND9': '9',
        'N': 'N',  # No jump
        ' ': ' ',  # Blank
    }
    
    def __init__(self):
        self.symbols: Dict[str, int] = {}
        self.instructions: List[AssemblyInstruction] = []
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.current_address = 0
    
    def reset(self):
        """Reset assembler state"""
        self.symbols = {}
        self.instructions = []
        self.errors = []
        self.warnings = []
        self.current_address = 0
    
    def parse_line(self, line: str) -> Optional[AssemblyInstruction]:
        """Parse a single assembly line"""
        # Remove comments
        comment = ''
        if '//' in line:
            line, comment = line.split('//', 1)
            comment = comment.strip()
        elif ';' in line:
            line, comment = line.split(';', 1)
            comment = comment.strip()
        
        line = line.strip()
        if not line:
            return None
        
        # Check for label
        label = None
        if ':' in line:
            parts = line.split(':', 1)
            label = parts[0].strip()
            line = parts[1].strip()
        
        # Parse instruction
        instr = AssemblyInstruction(comment=comment)
        
        # Try to parse mnemonic format: OPCODE T1 A1 B1 T2 A2 B2 M N P Q
        # Or simplified format
        tokens = line.split()
        
        if not tokens:
            return None
        
        # First token is opcode
        opcode = tokens[0].upper()
        if opcode in self.OPCODES:
            instr.q = self.OPCODES[opcode]
        else:
            # Try to parse as raw machine code
            if len(line) >= 10:
                instr.t1 = line[0] if len(line) > 0 else ' '
                instr.a1 = line[1] if len(line) > 1 else ' '
                instr.b1 = line[2] if len(line) > 2 else ' '
                instr.t2 = line[3] if len(line) > 3 else ' '
                instr.a2 = line[4] if len(line) > 4 else ' '
                instr.b2 = line[5] if len(line) > 5 else ' '
                instr.m = line[6] if len(line) > 6 else ' '
                instr.n = line[7] if len(line) > 7 else ' '
                instr.p = line[8] if len(line) > 8 else ' '
                instr.q = line[9] if len(line) > 9 else ' '
                instr.label = label
                return instr
        
        # Parse operands if mnemonic (simplified format: OPCODE TRACK,ADDR,...)
        if len(tokens) > 1:
            # Parse source: TRACK,ADDR format
            src = tokens[1].upper().replace(',', '')
            instr.t1 = self.TRACKS.get(src[0], src[0]) if src else ' '
            if len(src) > 2:
                try:
                    addr = int(src[1:])
                    instr.a1 = str(addr // 10)
                    instr.b1 = str(addr % 10)
                except ValueError:
                    pass
            
            # Parse destination
            if len(tokens) > 2:
                dst = tokens[2].upper().replace(',', '')
                instr.t2 = self.TRACKS.get(dst[0], dst[0]) if dst else ' '
                if len(dst) > 2:
                    try:
                        addr = int(dst[1:])
                        instr.a2 = str(addr // 10)
                        instr.b2 = str(addr % 10)
                    except ValueError:
                        pass
                
                # Length
                if len(tokens) > 3:
                    try:
                        instr.m = str(int(tokens[3]))
                    except ValueError:
                        pass
        
        instr.label = label
        return instr
    
    def first_pass(self, source: str):
        """First pass: collect symbols and labels"""
        lines = source.split('\n')
        address = 0
        
        for line in lines:
            instr = self.parse_line(line)
            if instr:
                if instr.label:
                    if instr.label in self.symbols:
                        self.errors.append(f"Duplicate label: {instr.label} at address {address}")
                    else:
                        self.symbols[instr.label] = address
                address += 1
        
        self.current_address = address
    
    def second_pass(self, source: str) -> List[str]:
        """Second pass: generate machine code"""
        lines = source.split('\n')
        machine_code = []
        
        for line in lines:
            instr = self.parse_line(line)
            if instr:
                # Resolve symbols in addresses
                # (simplified - full implementation would resolve symbol references)
                machine_code.append(instr.to_machine_code())
        
        return machine_code
    
    def assemble(self, source: str) -> Tuple[List[str], List[str], List[str]]:
        """
        Assemble source code into machine code.
        Returns: (machine_code, errors, warnings)
        """
        self.reset()
        
        # First pass: collect symbols
        self.first_pass(source)
        
        # Second pass: generate code
        machine_code = self.second_pass(source)
        
        return machine_code, self.errors, self.warnings
    
    def assemble_file(self, filename: str) -> Tuple[List[str], List[str], List[str]]:
        """Assemble a file"""
        try:
            with open(filename, 'r') as f:
                source = f.read()
            return self.assemble(source)
        except FileNotFoundError:
            return [], [f"File not found: {filename}"], []
        except Exception as e:
            return [], [f"Error reading file: {str(e)}"], []


# Example assembly programs
EXAMPLE_PROGRAMS = {
    'hello_world': """
// IBM 305 RAMAC Hello World Program
// Stores "HELLO WORLD" in track 1, then prints it

        CLEAR_ACC       // Clear accumulator
        LOAD    0,10,5  // Load message length
        STORE   1,0,11  // Store at track 1 addr 0
        HALT            // Exit

// Data section
// Track 1, address 10: "HELLO WORLD"
""",
    
    'simple_copy': """
// Simple copy operation
// Copy 5 characters from track 0 addr 0 to track 1 addr 0

START:  COPY    0,0,1,0,5   // Copy 5 chars
        HALT                // Exit
""",
    
    'mining_init': """
// IBM 305 RAMAC Miner Initialization
// Initialize mining data structures

        CLEAR_ACC           // Clear accumulator
        LOAD    0,0,10      // Load nonce initial value
        STORE   W,0,10      // Store in work area
        LOAD    0,10,64     // Load block header
        STORE   X,0,64      // Store in hash buffer
        DISK_ADDR 0,1       // Select disk 0, track 1
        DISK_IO   X,0,R     // Read disk data
        HALT                // Ready for mining
""",
}


def test_assembler():
    """Test the assembler with example programs"""
    print("=" * 60)
    print("IBM 305 RAMAC Cross-Assembler Test")
    print("=" * 60)
    
    assembler = IBM305Assembler()
    
    # Test simple copy program
    test_program = """
// Simple test program
START:  COPY    0,0,1,0,5   // Copy 5 chars
        CLEAR_ACC           // Clear accumulator
        HALT                // Exit
"""
    
    print("\nInput Assembly:")
    print(test_program)
    
    machine_code, errors, warnings = assembler.assemble(test_program)
    
    print("\nMachine Code Output:")
    for i, code in enumerate(machine_code):
        print(f"  {i:02d}: {code}")
    
    if errors:
        print("\nErrors:")
        for err in errors:
            print(f"  - {err}")
    
    if warnings:
        print("\nWarnings:")
        for warn in warnings:
            print(f"  - {warn}")
    
    print("\nSymbols:")
    for label, addr in assembler.symbols.items():
        print(f"  {label}: {addr}")
    
    print("\n" + "=" * 60)
    print("Assembler test complete")
    print("=" * 60)


if __name__ == '__main__':
    test_assembler()
