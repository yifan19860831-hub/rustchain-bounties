#!/usr/bin/env python3
"""
ORDVAC Assembler
Assembles ORDVAC assembly language to machine code

ORDVAC Instruction Format (20-bit):
  Bits 0-6:   Opcode (7 bits)
  Bits 7-19:  Address (13 bits)

Two instructions per 40-bit word
"""

import sys
import re

# ORDVAC opcodes
OPCODES = {
    'ADD':      0b000001,
    'SUB':      0b000010,
    'MPY':      0b000011,
    'DIV':      0b000100,
    'LOAD':     0b000101,
    'STORE':    0b000110,
    'JUMP':     0b000111,
    'JUMP+':    0b001000,
    'JUMP-':    0b001001,
    'HALT':     0b001010,
    'INPUT':    0b001011,
    'OUTPUT':   0b001100,
    'STMQ':     0b001101,
    'LOADMQ':   0b001110,
    'ALSHIFT':  0b001111,
    'ARSHIFT':  0b010000,
    'LSHIFT':   0b010001,
    'RSHIFT':   0b010010,
    'NOP':      0b000000,
}

# Pseudo-instructions
PSEUDO_OPS = {
    'DW': 'define_word',
    'DD': 'define_data',
    'ORG': 'origin',
    'EQU': 'equate',
}


class ORDVACAssembler:
    def __init__(self):
        self.symbols = {}
        self.origin = 0
        self.words = []
        self.current_word = 0
        self.instruction_in_word = 0
        
    def assemble(self, source: str) -> list:
        """Assemble source code to machine code"""
        lines = source.split('\n')
        
        # First pass: collect symbols
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Check for label
            if ':' in line and not line.startswith(' '):
                parts = line.split(':')
                label = parts[0].strip()
                self.symbols[label] = self.origin + len(self.words)
        
        # Second pass: generate code
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Skip labels
            if ':' in line and not line.startswith(' '):
                line = line.split(':', 1)[1].strip()
            
            if not line:
                continue
            
            # Handle pseudo-ops
            if line.startswith('DW '):
                value = int(line[3:].strip())
                self.words.append(value & 0xFFFFFFFFFF)  # 40-bit mask
                continue
            
            if line.startswith('ORG '):
                self.origin = int(line[4:].strip())
                continue
            
            # Parse instruction
            self.assemble_instruction(line)
        
        return self.words
    
    def assemble_instruction(self, line: str):
        """Assemble single instruction"""
        # Parse instruction
        match = re.match(r'(\w+)\s*(\d+)?', line)
        if not match:
            print(f"Warning: Cannot parse: {line}")
            return
        
        mnemonic = match.group(1).upper()
        address_str = match.group(2)
        address = int(address_str) if address_str else 0
        
        if mnemonic not in OPCODES:
            print(f"Warning: Unknown instruction: {mnemonic}")
            return
        
        opcode = OPCODES[mnemonic]
        
        # Create 20-bit instruction
        instruction = ((opcode & 0x7F) << 13) | (address & 0x1FFF)
        
        # Pack into 40-bit words (2 instructions per word)
        if self.instruction_in_word == 0:
            self.current_word = instruction & 0xFFFFF
            self.instruction_in_word = 1
        else:
            self.current_word |= (instruction & 0xFFFFF) << 20
            self.words.append(self.current_word)
            self.current_word = 0
            self.instruction_in_word = 0
    
    def finalize(self):
        """Finalize assembly, add last word if needed"""
        if self.instruction_in_word == 1:
            self.words.append(self.current_word)
        return self.words
    
    def to_hex(self, words: list = None) -> str:
        """Convert words to ORDVAC hex notation (KSNJFL)"""
        if words is None:
            words = self.words
        
        hex_chars = '0123456789KSNJFL'  # ORDVAC hex notation
        result = []
        
        for word in words:
            hex_str = f"{word:010X}"  # 40 bits = 10 hex digits
            ordvac_hex = ''
            for c in hex_str:
                if c in '0123456789':
                    ordvac_hex += c
                else:
                    # Convert standard hex to ORDVAC notation
                    mapping = {'A': 'K', 'B': 'S', 'C': 'N', 'D': 'J', 'E': 'F', 'F': 'L'}
                    ordvac_hex += mapping.get(c, c)
            result.append(ordvac_hex)
        
        return ' '.join(result)
    
    def print_listing(self, source: str):
        """Print assembly listing"""
        print("=" * 70)
        print("ORDVAC Assembly Listing")
        print("=" * 70)
        
        words = self.assemble(source)
        self.finalize()
        
        print(f"\nOrigin: {self.origin}")
        print(f"Symbols: {self.symbols}")
        print(f"Words: {len(words)}")
        print(f"\nMachine Code (ORDVAC Hex):")
        print(self.to_hex(words))
        print(f"\nMachine Code (Standard Hex):")
        for i, word in enumerate(words):
            print(f"  {self.origin + i:04X}: {word:010X}")
        
        print("\n" + "=" * 70)
        
        return words


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='ORDVAC Assembler')
    parser.add_argument('input', help='Input assembly file')
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('-l', '--listing', action='store_true', help='Print listing')
    
    args = parser.parse_args()
    
    # Read source
    with open(args.input, 'r') as f:
        source = f.read()
    
    # Assemble
    assembler = ORDVACAssembler()
    
    if args.listing:
        words = assembler.print_listing(source)
    else:
        words = assembler.assemble(source)
        assembler.finalize()
    
    # Write output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(f"# ORDVAC Machine Code\n")
            f.write(f"# Generated from: {args.input}\n")
            f.write(f"# Words: {len(words)}\n\n")
            for i, word in enumerate(words):
                f.write(f"{word:010X}\n")
        print(f"Output written to: {args.output}")
    else:
        # Print machine code
        print("\nMachine Code:")
        for i, word in enumerate(words):
            print(f"  {i:04X}: {word:010X}")


if __name__ == "__main__":
    main()
