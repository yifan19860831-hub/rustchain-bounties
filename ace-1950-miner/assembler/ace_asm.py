#!/usr/bin/env python3
"""
ACE (1950) Cross-Assembler

Assembles ACE assembly language into machine code.

Usage:
    python ace_asm.py input.asm [-o output.bin]

Assembly syntax:
    LABEL:  MNEMONIC  OPERANDS  ; COMMENT
    
Example:
    START:  LD        0x10      ; Load from address 0x10
            ADD       0x11      ; Add from address 0x11
            ST        0x12      ; Store to address 0x12
            STOP                ; Halt
"""

import sys
import re
import argparse

# ACE Instruction Set (matches ace_cpu.py)
OPCODES = {
    'NOP':   0x00,
    'ACH':   0x01,  # Add to AH
    'ACL':   0x02,  # Add to AL
    'ADH':   0x03,  # Add delay line to H
    'ADL':   0x04,  # Add delay line to L
    'SUB':   0x05,  # Subtract
    'RND':   0x06,  # Round
    'LSH':   0x07,  # Left shift
    'RSH':   0x08,  # Right shift
    'AND':   0x09,  # Logical AND
    'OR':    0x0A,  # Logical OR
    'NOT':   0x0B,  # Logical NOT
    'LD':    0x0C,  # Load from delay line
    'ST':    0x0D,  # Store to delay line
    'JMP':   0x0E,  # Unconditional jump
    'JZ':    0x0F,  # Jump if zero
    'JN':    0x10,  # Jump if negative
    'STOP':  0x11,  # Halt
    'LDQ':   0x12,  # Load Q
    'STQ':   0x13,  # Store Q
    'MLA':   0x14,  # Multiply AL by source
    'DIV':   0x15,  # Divide AH:AL by source
    'IN':    0x16,  # Input
    'OUT':   0x17,  # Output
}


class ACEAssembler:
    """ACE Cross-Assembler"""
    
    def __init__(self):
        self.labels = {}
        self.instructions = []
        self.current_address = 0
        self.errors = []
        self.warnings = []
        
    def parse_operand(self, operand):
        """Parse operand and return numeric value"""
        if operand is None:
            return 0
            
        operand = operand.strip()
        
        # Hex literal
        if operand.startswith('0x') or operand.startswith('0X'):
            return int(operand, 16)
        
        # Decimal literal
        if operand.isdigit():
            return int(operand)
        
        # Label reference
        if operand in self.labels:
            return self.labels[operand]
        
        # Try to parse as integer anyway
        try:
            return int(operand)
        except ValueError:
            raise ValueError(f"Unknown operand: {operand}")
    
    def encode_instruction(self, mnemonic, operands):
        """Encode instruction to 32-bit word"""
        mnemonic = mnemonic.upper()
        
        if mnemonic not in OPCODES:
            raise ValueError(f"Unknown instruction: {mnemonic}")
        
        opcode = OPCODES[mnemonic]
        
        # Parse operands
        if len(operands) == 0:
            source = 0
            dest = 0
        elif len(operands) == 1:
            source = self.parse_operand(operands[0])
            dest = 0
        elif len(operands) == 2:
            source = self.parse_operand(operands[0])
            dest = self.parse_operand(operands[1])
        else:
            raise ValueError(f"Too many operands for {mnemonic}: {len(operands)}")
        
        # Encode: opcode(6) | source(6) | dest(6) | reserved(14)
        instruction = ((opcode & 0x3F) << 26) | ((source & 0x3F) << 20) | ((dest & 0x3F) << 14)
        return instruction & 0xFFFFFFFF
    
    def first_pass(self, lines):
        """First pass: collect labels and calculate addresses"""
        self.current_address = 0
        
        for line_num, line in enumerate(lines, 1):
            # Remove comments
            if ';' in line:
                line = line[:line.index(';')]
            
            line = line.strip()
            if not line:
                continue
            
            # Check for label
            if ':' in line:
                label_part, rest = line.split(':', 1)
                label = label_part.strip()
                self.labels[label] = self.current_address
                line = rest.strip()
            
            # Count instruction/data word
            if line:
                self.current_address += 1
    
    def second_pass(self, lines):
        """Second pass: generate machine code"""
        self.instructions = []
        self.current_address = 0
        
        for line_num, line in enumerate(lines, 1):
            original_line = line
            
            # Remove comments
            if ';' in line:
                line = line[:line.index(';')]
            
            line = line.strip()
            if not line:
                continue
            
            # Skip label (already processed)
            if ':' in line:
                label_part, line = line.split(':', 1)
                line = line.strip()
            
            if not line:
                continue
            
            # Parse instruction
            parts = line.split()
            if not parts:
                continue
            
            mnemonic = parts[0].upper()
            operands = parts[1:] if len(parts) > 1 else []
            
            # Handle pseudo-instructions
            if mnemonic in ['ORG']:
                # Set origin address
                self.current_address = self.parse_operand(operands[0])
                continue
            elif mnemonic in ['END']:
                # End of program
                break
            elif mnemonic in ['DC', 'DW', 'DD']:
                # Define constant/word/data
                for op in operands:
                    value = self.parse_operand(op)
                    self.instructions.append(value)
                    self.current_address += 1
            elif mnemonic in ['NOP', 'STOP']:
                # No operands
                instruction = self.encode_instruction(mnemonic, [])
                self.instructions.append(instruction)
                self.current_address += 1
            elif mnemonic == 'ADD':
                # ADD is alias for ACL (add to AL)
                instruction = self.encode_instruction('ACL', operands)
                self.instructions.append(instruction)
                self.current_address += 1
            else:
                # Regular instruction
                try:
                    instruction = self.encode_instruction(mnemonic, operands)
                    self.instructions.append(instruction)
                    self.current_address += 1
                except ValueError as e:
                    self.errors.append(f"Line {line_num}: {e}")
        
        return self.instructions
    
    def assemble(self, source):
        """Assemble source code"""
        lines = source.split('\n')
        
        # First pass
        self.first_pass(lines)
        
        # Second pass
        self.second_pass(lines)
        
        return self.instructions
    
    def assemble_file(self, filename):
        """Assemble from file"""
        with open(filename, 'r') as f:
            source = f.read()
        return self.assemble(source)
    
    def output_binary(self, filename):
        """Write binary output"""
        with open(filename, 'wb') as f:
            for instr in self.instructions:
                f.write(instr.to_bytes(4, byteorder='big'))
    
    def output_hex(self, filename):
        """Write hex output"""
        with open(filename, 'w') as f:
            for i, instr in enumerate(self.instructions):
                f.write(f"{i:04X}: {instr:08X}\n")
    
    def report(self):
        """Print assembly report"""
        print(f"\nAssembly Report:")
        print(f"  Labels defined: {len(self.labels)}")
        print(f"  Instructions: {len(self.instructions)}")
        print(f"  Errors: {len(self.errors)}")
        print(f"  Warnings: {len(self.warnings)}")
        
        if self.errors:
            print("\nErrors:")
            for error in self.errors:
                print(f"  ERROR: {error}")
        
        if self.warnings:
            print("\nWarnings:")
            for warning in self.warnings:
                print(f"  WARNING: {warning}")
        
        if self.labels:
            print("\nSymbol Table:")
            for label, addr in sorted(self.labels.items()):
                print(f"  {label:20} = 0x{addr:04X}")


def main():
    parser = argparse.ArgumentParser(description='ACE (1950) Cross-Assembler')
    parser.add_argument('input', help='Input assembly file')
    parser.add_argument('-o', '--output', help='Output file (default: input.bin)')
    parser.add_argument('--hex', action='store_true', help='Output hex format')
    parser.add_argument('--list', action='store_true', help='Show listing')
    
    args = parser.parse_args()
    
    # Assemble
    assembler = ACEAssembler()
    
    try:
        assembler.assemble_file(args.input)
    except FileNotFoundError:
        print(f"Error: File not found: {args.input}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    # Report
    assembler.report()
    
    if assembler.errors:
        print("\nAssembly failed.")
        sys.exit(1)
    
    # Output
    output_file = args.output
    if not output_file:
        base = args.input.rsplit('.', 1)[0]
        output_file = base + '.hex' if args.hex else base + '.bin'
    
    if args.hex:
        assembler.output_hex(output_file)
        print(f"\nHex output written to: {output_file}")
    else:
        assembler.output_binary(output_file)
        print(f"\nBinary output written to: {output_file}")
    
    # Show listing if requested
    if args.list:
        print("\nProgram Listing:")
        for i, instr in enumerate(assembler.instructions):
            print(f"  {i:04X}: {instr:08X}")


if __name__ == "__main__":
    main()
