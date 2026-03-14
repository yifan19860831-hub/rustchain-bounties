#!/usr/bin/env python3
"""
IBM 701 Assembler (1952)
Assembly language support for IBM 701

Converts IBM 701 assembly code to machine code (36-bit words, 2 instructions per word)
"""

import re
from typing import List, Dict, Tuple

# IBM 701 opcodes
OPCODES = {
    'STOP': 0x00,
    'ADD': 0x01,
    'SUB': 0x02,
    'MUL': 0x03,
    'DIV': 0x04,
    'AND': 0x05,
    'OR': 0x06,
    'JMP': 0x07,
    'JZ': 0x08,
    'JN': 0x09,
    'LD': 0x0A,
    'ST': 0x0B,
    'IN': 0x0C,
    'OUT': 0x0D,
    'RSH': 0x0E,
    'LSH': 0x0F,
}

# Pseudo-ops
PSEUDO_OPS = ['DC', 'DS', 'ORG', 'EQU', 'END']


class IBM701Assembler:
    """IBM 701 Assembly Language Assembler"""
    
    def __init__(self):
        self.symbols: Dict[str, int] = {}
        self.memory: List[int] = [0] * 2048
        self.location_counter = 0
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def parse_line(self, line: str) -> Tuple[str, str, str]:
        """Parse assembly line into label, opcode, operand"""
        # Remove comments
        if ';' in line:
            line = line[:line.index(';')]
        
        line = line.strip()
        if not line:
            return None, None, None
        
        # Parse label
        label = None
        if ':' in line:
            parts = line.split(':', 1)
            label = parts[0].strip()
            line = parts[1].strip()
        
        # Parse opcode and operand
        parts = line.split(None, 1)
        if not parts:
            return label, None, None
        
        opcode = parts[0].upper()
        operand = parts[1].strip() if len(parts) > 1 else None
        
        return label, opcode, operand
    
    def assemble(self, source: str) -> List[int]:
        """Assemble source code into machine code"""
        lines = source.split('\n')
        
        # First pass: collect symbols
        for line in lines:
            label, opcode, operand = self.parse_line(line)
            
            if label:
                self.symbols[label] = self.location_counter
            
            if opcode in OPCODES:
                self.location_counter += 1
            elif opcode == 'DC':
                self.location_counter += 1
            elif opcode == 'DS':
                if operand:
                    try:
                        count = int(operand)
                        self.location_counter += count
                    except ValueError:
                        self.errors.append(f"Invalid DS operand: {operand}")
            elif opcode == 'ORG':
                if operand:
                    try:
                        self.location_counter = int(operand, 0)
                    except ValueError:
                        self.errors.append(f"Invalid ORG address: {operand}")
            elif opcode == 'END':
                break
        
        # Second pass: generate code
        self.location_counter = 0
        for line in lines:
            label, opcode, operand = self.parse_line(line)
            
            if opcode in OPCODES:
                self.assemble_instruction(opcode, operand)
            elif opcode == 'DC':
                self.assemble_data(operand)
            elif opcode == 'DS':
                pass  # Already allocated
            elif opcode == 'ORG':
                if operand:
                    self.location_counter = int(operand, 0)
            elif opcode == 'END':
                break
            elif opcode and opcode not in PSEUDO_OPS and not label:
                self.warnings.append(f"Unknown opcode: {opcode}")
        
        return self.memory[:self.location_counter]
    
    def assemble_instruction(self, opcode: str, operand: str):
        """Assemble single instruction"""
        op = OPCODES.get(opcode, 0)
        
        # Parse address
        addr = 0
        if operand:
            if operand in self.symbols:
                addr = self.symbols[operand]
            else:
                try:
                    addr = int(operand, 0)
                except ValueError:
                    self.errors.append(f"Invalid operand: {operand}")
        
        # Create 18-bit instruction
        instruction = ((op & 0xFF) << 10) | (addr & 0x3FF)
        
        # Store in memory (2 instructions per 36-bit word)
        if self.location_counter % 2 == 0:
            # First instruction in word (bits 0-17)
            self.memory[self.location_counter // 2] = instruction << 18
        else:
            # Second instruction in word (bits 18-35)
            self.memory[self.location_counter // 2] |= instruction
        
        self.location_counter += 1
    
    def assemble_data(self, operand: str):
        """Assemble data constant"""
        if not operand:
            return
        
        # String constant
        if operand.startswith("'") and operand.endswith("'"):
            value = 0
            for char in operand[1:-1]:
                value = (value << 8) | ord(char)
            self.memory[self.location_counter // 2] = value
        else:
            # Numeric constant
            try:
                value = int(operand, 0)
                self.memory[self.location_counter // 2] = value & 0xFFFFFFFFF
            except ValueError:
                self.errors.append(f"Invalid data constant: {operand}")
        
        self.location_counter += 1
    
    def get_errors(self) -> List[str]:
        return self.errors
    
    def get_warnings(self) -> List[str]:
        return self.warnings


def assemble_file(input_file: str, output_file: str = None):
    """Assemble file and optionally save binary output"""
    with open(input_file, 'r') as f:
        source = f.read()
    
    assembler = IBM701Assembler()
    memory = assembler.assemble(source)
    
    if assembler.get_errors():
        print("Errors:")
        for error in assembler.get_errors():
            print(f"  ERROR: {error}")
        return None
    
    if assembler.get_warnings():
        print("Warnings:")
        for warning in assembler.get_warnings():
            print(f"  WARNING: {warning}")
    
    print(f"Assembled {len(memory)} words")
    
    if output_file:
        with open(output_file, 'w') as f:
            for i, word in enumerate(memory):
                f.write(f"{i:04X}: {word:010X}\n")
        print(f"Output saved to {output_file}")
    
    return memory


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='IBM 701 Assembler')
    parser.add_argument('input', help='Input assembly file')
    parser.add_argument('-o', '--output', help='Output binary file')
    
    args = parser.parse_args()
    
    assemble_file(args.input, args.output)


if __name__ == '__main__':
    main()
