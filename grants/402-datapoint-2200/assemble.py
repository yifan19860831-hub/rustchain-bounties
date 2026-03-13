#!/usr/bin/env python3
"""
Datapoint 2200 Cross-Assembler

Assembles Datapoint 2200 assembly code to binary format.

Usage:
    python assemble.py input.asm -o output.bin

Datapoint 2200 Architecture:
- 8-bit CPU, 48 instructions
- Memory: 2KB-16KB (octal addressing)
- All addresses in octal notation
"""

import sys
import argparse
import re

# Datapoint 2200 Instruction Set
# Format: (mnemonic, opcode_mask, operand_type, cycles)
INSTRUCTIONS = {
    # HALT
    'HALT':     (0o000, 'none', 0),
    
    # Shift operations
    'SLC':      (0o002, 'none', 1),  # Shift left through carry
    'SRC':      (0o012, 'none', 1),  # Shift right through carry
    'RAL':      (0o042, 'none', 1),  # Rotate left through carry
    'RAR':      (0o052, 'none', 1),  # Rotate right through carry
    'RLC':      (0o002, 'none', 1),  # Alias for SLC
    'RRC':      (0o012, 'none', 1),  # Alias for SRC
    
    # Return operations
    'RET':      (0o007, 'none', 1),
    'RETURN':   (0o007, 'none', 1),
    
    # Conditional returns (Rcc)
    'RFC':      (0o013, 'none', 1),  # Return if carry false
    'RFZ':      (0o023, 'none', 1),  # Return if zero false
    'RFS':      (0o033, 'none', 1),  # Return if sign false
    'RFP':      (0o043, 'none', 1),  # Return if parity odd
    'RTC':      (0o053, 'none', 1),  # Return if carry true
    'RTZ':      (0o063, 'none', 1),  # Return if zero true
    'RTS':      (0o073, 'none', 1),  # Return if sign true
    'RTP':      (0o103, 'none', 1),  # Return if parity even
    
    # Load immediate (LrI)
    'LAI':      (0o136, 'imm8', 1),
    'LBI':      (0o116, 'imm8', 1),
    'LCI':      (0o126, 'imm8', 1),
    'LDI':      (0o156, 'imm8', 1),
    'LEI':      (0o166, 'imm8', 1),
    'LHI':      (0o176, 'imm8', 1),
    'LLI':      (0o206, 'imm8', 1),
    
    # Load register from register (Lds)
    'LAA':      (0o300, 'none', 1),  # NOP
    'LAB':      (0o301, 'none', 1),
    'LAC':      (0o302, 'none', 1),
    'LAD':      (0o303, 'none', 1),
    'LAE':      (0o304, 'none', 1),
    'LAH':      (0o305, 'none', 1),
    'LAL':      (0o306, 'none', 1),
    'LBA':      (0o310, 'none', 1),
    'LBB':      (0o311, 'none', 1),
    'LBC':      (0o312, 'none', 1),
    'LBD':      (0o313, 'none', 1),
    'LBE':      (0o314, 'none', 1),
    'LBH':      (0o315, 'none', 1),
    'LBL':      (0o316, 'none', 1),
    'LCA':      (0o320, 'none', 1),
    'LCB':      (0o321, 'none', 1),
    'LCC':      (0o322, 'none', 1),
    'LCD':      (0o323, 'none', 1),
    'LCE':      (0o324, 'none', 1),
    'LCH':      (0o325, 'none', 1),
    'LCL':      (0o326, 'none', 1),
    'LDA':      (0o330, 'none', 1),
    'LDB':      (0o331, 'none', 1),
    'LDC':      (0o332, 'none', 1),
    'LDD':      (0o333, 'none', 1),
    'LDE':      (0o334, 'none', 1),
    'LDH':      (0o335, 'none', 1),
    'LDL':      (0o336, 'none', 1),
    'LEA':      (0o340, 'none', 1),
    'LEB':      (0o341, 'none', 1),
    'LEC':      (0o342, 'none', 1),
    'LED':      (0o343, 'none', 1),
    'LEE':      (0o344, 'none', 1),
    'LEH':      (0o345, 'none', 1),
    'LEL':      (0o346, 'none', 1),
    'LHA':      (0o350, 'none', 1),
    'LHB':      (0o351, 'none', 1),
    'LHC':      (0o352, 'none', 1),
    'LHD':      (0o353, 'none', 1),
    'LHE':      (0o354, 'none', 1),
    'LHH':      (0o355, 'none', 1),
    'LHL':      (0o356, 'none', 1),
    'LLA':      (0o360, 'none', 1),
    'LLB':      (0o361, 'none', 1),
    'LLC':      (0o362, 'none', 1),
    'LLD':      (0o363, 'none', 1),
    'LLE':      (0o364, 'none', 1),
    'LLH':      (0o365, 'none', 1),
    'LLL':      (0o366, 'none', 1),
    
    # Memory operations (through HL)
    'LAM':      (0o100, 'none', 2),  # A = M[HL]
    'LMA':      (0o140, 'none', 2),  # M[HL] = A
    'LBM':      (0o101, 'none', 2),  # B = M[HL]
    'LMB':      (0o141, 'none', 2),  # M[HL] = B
    'LCM':      (0o102, 'none', 2),  # C = M[HL]
    'LMC':      (0o142, 'none', 2),  # M[HL] = C
    'LDM':      (0o103, 'none', 2),  # D = M[HL]
    'LMD':      (0o143, 'none', 2),  # M[HL] = D
    'LEM':      (0o104, 'none', 2),  # E = M[HL]
    'LME':      (0o144, 'none', 2),  # M[HL] = E
    'LHM':      (0o105, 'none', 2),  # H = M[HL]
    'LMH':      (0o145, 'none', 2),  # M[HL] = H
    'LLM':      (0o106, 'none', 2),  # L = M[HL]
    'LML':      (0o146, 'none', 2),  # M[HL] = L
    
    # ALU operations with register (ALUr)
    'ADA':      (0o200, 'none', 1),  # A = A + A
    'ADB':      (0o201, 'none', 1),  # A = A + B
    'ADC':      (0o202, 'none', 1),  # A = A + C
    'ADD':      (0o203, 'none', 1),  # A = A + D
    'ADE':      (0o204, 'none', 1),  # A = A + E
    'ADH':      (0o205, 'none', 1),  # A = A + H
    'ADL':      (0o206, 'none', 1),  # A = A + L
    'ADM':      (0o207, 'none', 2),  # A = A + M[HL]
    'ACA':      (0o210, 'none', 1),  # A = A + A + Cy
    'ACB':      (0o211, 'none', 1),
    'ACC':      (0o212, 'none', 1),
    'ACD':      (0o213, 'none', 1),
    'ACE':      (0o214, 'none', 1),
    'ACH':      (0o215, 'none', 1),
    'ACL':      (0o216, 'none', 1),
    'ACM':      (0o217, 'none', 2),
    'SUA':      (0o220, 'none', 1),  # A = A - A
    'SUB':      (0o221, 'none', 1),  # A = A - B
    'SUC':      (0o222, 'none', 1),  # A = A - C
    'SUD':      (0o223, 'none', 1),  # A = A - D
    'SUE':      (0o224, 'none', 1),  # A = A - E
    'SUH':      (0o225, 'none', 1),  # A = A - H
    'SUL':      (0o226, 'none', 1),  # A = A - L
    'SUM':      (0o227, 'none', 2),  # A = A - M[HL]
    'SBA':      (0o230, 'none', 1),  # A = A - A - Cy
    'SBB':      (0o231, 'none', 1),
    'SBC':      (0o232, 'none', 1),
    'SBD':      (0o233, 'none', 1),
    'SBE':      (0o234, 'none', 1),
    'SBH':      (0o235, 'none', 1),
    'SBL':      (0o236, 'none', 1),
    'SBM':      (0o237, 'none', 2),
    'NDA':      (0o240, 'none', 1),  # A = A AND A
    'NDB':      (0o241, 'none', 1),  # A = A AND B
    'NDC':      (0o242, 'none', 1),  # A = A AND C
    'NDD':      (0o243, 'none', 1),  # A = A AND D
    'NDE':      (0o244, 'none', 1),  # A = A AND E
    'NDH':      (0o245, 'none', 1),  # A = A AND H
    'NDL':      (0o246, 'none', 1),  # A = A AND L
    'NDM':      (0o247, 'none', 2),  # A = A AND M[HL]
    'XRA':      (0o250, 'none', 1),  # A = A XOR A
    'XRB':      (0o251, 'none', 1),  # A = A XOR B
    'XRC':      (0o252, 'none', 1),  # A = A XOR C
    'XRD':      (0o253, 'none', 1),  # A = A XOR D
    'XRE':      (0o254, 'none', 1),  # A = A XOR E
    'XRH':      (0o255, 'none', 1),  # A = A XOR H
    'XRL':      (0o256, 'none', 1),  # A = A XOR L
    'XRM':      (0o257, 'none', 2),  # A = A XOR M[HL]
    'ORA':      (0o260, 'none', 1),  # A = A OR A
    'ORB':      (0o261, 'none', 1),  # A = A OR B
    'ORC':      (0o262, 'none', 1),  # A = A OR C
    'ORD':      (0o263, 'none', 1),  # A = A OR D
    'ORE':      (0o264, 'none', 1),  # A = A OR E
    'ORH':      (0o265, 'none', 1),  # A = A OR H
    'ORL':      (0o266, 'none', 1),  # A = A OR L
    'ORM':      (0o267, 'none', 2),  # A = A OR M[HL]
    'CPA':      (0o270, 'none', 1),  # Compare A - A
    'CPB':      (0o271, 'none', 1),  # Compare A - B
    'CPC':      (0o272, 'none', 1),  # Compare A - C
    'CPD':      (0o273, 'none', 1),  # Compare A - D
    'CPE':      (0o274, 'none', 1),  # Compare A - E
    'CPH':      (0o275, 'none', 1),  # Compare A - H
    'CPL':      (0o276, 'none', 1),  # Compare A - L
    'CPM':      (0o277, 'none', 2),  # Compare A - M[HL]
    
    # ALU immediate (ALU data)
    'ADI':      (0o110, 'imm8', 1),  # A = A + data
    'ACI':      (0o111, 'imm8', 1),  # A = A + data + Cy
    'SUI':      (0o112, 'imm8', 1),  # A = A - data
    'SBI':      (0o113, 'imm8', 1),  # A = A - data - Cy
    'NDI':      (0o114, 'imm8', 1),  # A = A AND data
    'XRI':      (0o115, 'imm8', 1),  # A = A XOR data
    'ORI':      (0o116, 'imm8', 1),  # A = A OR data
    'CPI':      (0o117, 'imm8', 1),  # Compare A - data
    
    # Increment/Decrement
    'INA':      (0o020, 'none', 1),  # A = A + 1 (not available on 8008)
    'INB':      (0o021, 'none', 1),
    'INC':      (0o022, 'none', 1),
    'IND':      (0o023, 'none', 1),
    'INE':      (0o024, 'none', 1),
    'INH':      (0o025, 'none', 1),
    'INL':      (0o026, 'none', 1),
    'DCA':      (0o030, 'none', 1),  # A = A - 1 (not available on 8008)
    'DCB':      (0o031, 'none', 1),
    'DCC':      (0o032, 'none', 1),
    'DCD':      (0o033, 'none', 1),
    'DCE':      (0o034, 'none', 1),
    'DCH':      (0o035, 'none', 1),
    'DCL':      (0o036, 'none', 1),
    
    # Jumps (Jcc add)
    'JMP':      (0o124, 'addr13', 2),
    'JFC':      (0o100, 'addr13', 2),  # Jump if carry false
    'JFZ':      (0o104, 'addr13', 2),  # Jump if zero false
    'JFS':      (0o110, 'addr13', 2),  # Jump if sign false
    'JFP':      (0o114, 'addr13', 2),  # Jump if parity odd
    'JTC':      (0o120, 'addr13', 2),  # Jump if carry true
    'JTZ':      (0o124, 'addr13', 2),  # Jump if zero true (alias for JMP)
    'JTS':      (0o130, 'addr13', 2),  # Jump if sign true
    'JTP':      (0o134, 'addr13', 2),  # Jump if parity even
    
    # Calls (Ccc add)
    'CALL':     (0o136, 'addr13', 2),
    'CFC':      (0o101, 'addr13', 2),
    'CFZ':      (0o105, 'addr13', 2),
    'CFS':      (0o111, 'addr13', 2),
    'CFP':      (0o115, 'addr13', 2),
    'CTC':      (0o121, 'addr13', 2),
    'CTZ':      (0o125, 'addr13', 2),
    'CTS':      (0o131, 'addr13', 2),
    'CTP':      (0o135, 'addr13', 2),
    
    # Input/Output
    'INPUT':    (0o101, 'none', 1),
    'INP':      (0o101, 'port3', 1),  # Input from port 0-7
    'OUT':      (0o122, 'port5', 1),  # Output to port 8-31
    'EX':       (0o122, 'imm8', 1),   # External command (Datapoint extension)
    
    # RST (Restart)
    'RST0':     (0o037, 'none', 1),
    'RST1':     (0o047, 'none', 1),
    'RST2':     (0o057, 'none', 1),
    'RST3':     (0o067, 'none', 1),
    'RST4':     (0o077, 'none', 1),
    'RST5':     (0o107, 'none', 1),
    'RST6':     (0o117, 'none', 1),
    'RST7':     (0o127, 'none', 1),
    
    # NOP
    'NOP':      (0o300, 'none', 1),
}

# Register codes
REG_CODES = {
    'A': 0o000, 'B': 0o001, 'C': 0o010, 'D': 0o011,
    'E': 0o100, 'H': 0o101, 'L': 0o110, 'M': 0o111
}


def parse_octal(s):
    """Parse octal number (with or without Q suffix)"""
    s = s.strip().upper()
    if s.endswith('Q'):
        s = s[:-1]
    if s.startswith('0') and len(s) > 1 and s[1] != 'x':
        # Octal literal
        return int(s, 8)
    try:
        return int(s, 8)
    except ValueError:
        return int(s, 10)


def parse_binary(s):
    """Parse binary number (with B suffix)"""
    s = s.strip().upper()
    if s.endswith('B'):
        s = s[:-1]
    return int(s, 2)


def parse_operand(operand, op_type):
    """Parse operand based on type"""
    if op_type == 'none':
        return None
    elif op_type == 'imm8':
        # Immediate 8-bit value
        operand = operand.strip()
        if operand.startswith('0') and len(operand) > 1:
            return int(operand, 8) & 0xFF
        elif operand.endswith('B'):
            return parse_binary(operand) & 0xFF
        elif operand.startswith("'") and operand.endswith("'"):
            # Character literal
            return ord(operand[1]) & 0xFF
        else:
            return int(operand) & 0xFF
    elif op_type == 'addr13':
        # 13-bit address
        return parse_octal(operand) & 0x1FFF
    elif op_type == 'port3':
        # 3-bit port (0-7)
        return int(operand) & 0o7
    elif op_type == 'port5':
        # 5-bit port (0-31)
        return int(operand) & 0o37
    else:
        raise ValueError(f"Unknown operand type: {op_type}")


def assemble_line(line, line_num, symbols, pc):
    """Assemble a single line of assembly"""
    # Remove comments
    if ';' in line:
        line = line[:line.index(';')]
    
    line = line.strip()
    if not line:
        return [], pc
    
    # Check for label
    if ':' in line:
        parts = line.split(':', 1)
        label = parts[0].strip()
        symbols[label] = pc
        line = parts[1].strip() if len(parts) > 1 else ''
        if not line:
            return [], pc
    
    # Parse instruction
    parts = line.split(None, 1)
    mnemonic = parts[0].upper()
    operand = parts[1].strip() if len(parts) > 1 else None
    
    if mnemonic not in INSTRUCTIONS:
        print(f"Line {line_num}: Unknown instruction: {mnemonic}")
        return [], pc
    
    opcode_mask, op_type, cycles = INSTRUCTIONS[mnemonic]
    
    if op_type == 'none':
        return [opcode_mask], pc + 1
    elif operand is None:
        print(f"Line {line_num}: Missing operand for {mnemonic}")
        return [], pc
    else:
        op_value = parse_operand(operand, op_type)
        if op_type == 'imm8':
            return [opcode_mask, op_value], pc + 2
        elif op_type == 'addr13':
            # 13-bit address in two bytes (low, high)
            low = op_value & 0xFF
            high = (op_value >> 8) & 0x1F
            return [opcode_mask, low, high], pc + 3
        elif op_type in ('port3', 'port5', 'imm8'):
            return [opcode_mask, op_value], pc + 2
        else:
            return [opcode_mask, op_value], pc + 2


def assemble(source_file, output_file):
    """Assemble source file to binary"""
    with open(source_file, 'r') as f:
        lines = f.readlines()
    
    symbols = {}
    binary = []
    pc = 0
    
    # First pass: collect symbols
    for line_num, line in enumerate(lines, 1):
        # Handle ORG directive
        stripped = line.strip().upper()
        if stripped.startswith('ORG'):
            addr_part = stripped[3:].strip()
            pc = parse_octal(addr_part)
            continue
        
        # Handle END directive
        if stripped.startswith('END'):
            break
        
        # Handle DFB (Define Byte) directive
        if stripped.startswith('DFB'):
            values_part = stripped[3:].strip()
            # Count bytes
            values = [v.strip() for v in values_part.split(',')]
            pc += len(values)
            continue
        
        # Parse line for labels
        if ':' in line:
            label = line.split(':')[0].strip()
            symbols[label] = pc
    
    # Second pass: generate code
    pc = 0
    for line_num, line in enumerate(lines, 1):
        stripped = line.strip().upper()
        
        # Handle ORG directive
        if stripped.startswith('ORG'):
            addr_part = stripped[3:].strip()
            pc = parse_octal(addr_part)
            continue
        
        # Handle END directive
        if stripped.startswith('END'):
            break
        
        # Handle DFB directive
        if stripped.startswith('DFB'):
            values_part = stripped[3:].strip()
            values = [v.strip() for v in values_part.split(',')]
            for v in values:
                if v.startswith("'") and v.endswith("'"):
                    binary.append(ord(v[1]) & 0xFF)
                else:
                    binary.append(parse_octal(v) & 0xFF)
            pc += len(values)
            continue
        
        # Assemble instruction
        code, pc = assemble_line(line, line_num, symbols, pc)
        binary.extend(code)
    
    # Write binary output
    with open(output_file, 'wb') as f:
        f.write(bytes(binary))
    
    print(f"Assembled {len(binary)} bytes to {output_file}")
    print(f"Symbols: {len(symbols)}")


def main():
    parser = argparse.ArgumentParser(description='Datapoint 2200 Cross-Assembler')
    parser.add_argument('input', help='Input assembly file')
    parser.add_argument('-o', '--output', required=True, help='Output binary file')
    args = parser.parse_args()
    
    assemble(args.input, args.output)


if __name__ == '__main__':
    main()
