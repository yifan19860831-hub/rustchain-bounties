#!/usr/bin/env python3
"""
ACE (Automatic Computing Engine) CPU Simulator

Simulates Alan Turing's ACE computer design from 1945-1950,
as built at the National Physical Laboratory (NPL).

Architecture:
- 32-bit word size
- Mercury delay line memory: 128 words (expandable to 352)
- 1 MHz clock speed
- Two-address instruction format
- Fixed-point arithmetic (floating-point added later)

Based on:
- Turing's ACE Report (1946)
- Pilot ACE operational specifications (1950)
"""

class DelayLine:
    """
    Simulates mercury delay line memory.
    
    Mercury delay lines store data as acoustic waves in tubes of mercury.
    Data circulates continuously and must be refreshed.
    Access is serial - must wait for the correct bit to emerge.
    """
    
    def __init__(self, word_size=32, capacity=128):
        self.word_size = word_size
        self.capacity = capacity
        self.words = [0] * capacity
        self.access_time_cycles = 32  # One word = 32 bit cycles
        
    def read(self, address):
        """Read word from delay line (simulates waiting for serial access)"""
        if 0 <= address < self.capacity:
            return self.words[address] & 0xFFFFFFFF
        raise ValueError(f"Address {address} out of range")
    
    def write(self, address, value):
        """Write word to delay line"""
        if 0 <= address < self.capacity:
            self.words[address] = value & 0xFFFFFFFF
        else:
            raise ValueError(f"Address {address} out of range")
    
    def expand(self, new_capacity):
        """Expand delay line capacity (historical: 128 -> 352 words)"""
        if new_capacity > self.capacity:
            self.words.extend([0] * (new_capacity - self.capacity))
            self.capacity = new_capacity


class ACECPU:
    """
    ACE CPU Simulator
    
    Registers:
    - A (Accumulator): 64 bits (split into AH:AL, each 32 bits)
    - Q (Multiplier/Quotient): 32 bits
    - CI (Control Instruction): Current instruction register
    - P (Program Counter): Address of next instruction
    
    The ACE used a minimalist design with delay lines for most storage.
    """
    
    def __init__(self, memory_size=352):
        # 64-bit accumulator (split into two 32-bit halves)
        self.AH = 0  # Accumulator high
        self.AL = 0  # Accumulator low
        
        # Q register for multiplication/division
        self.Q = 0
        
        # Program counter
        self.P = 0
        
        # Current instruction
        self.CI = 0
        
        # Status flags
        self.zero_flag = False
        self.neg_flag = False
        self.overflow_flag = False
        
        # Mercury delay line memory
        self.memory = DelayLine(word_size=32, capacity=memory_size)
        
        # Execution statistics
        self.instructions_executed = 0
        self.cycle_count = 0
        self.halted = False
        
        # Timing simulation (1 MHz clock)
        self.clock_hz = 1_000_000
        self.cycles_per_instruction = 32  # Average
        
    def mask32(self, value):
        """Mask to 32 bits"""
        return value & 0xFFFFFFFF
    
    def mask64(self, value):
        """Mask to 64 bits"""
        return value & 0xFFFFFFFFFFFFFFFF
    
    def is_negative(self, value):
        """Check if 32-bit value is negative (MSB set)"""
        return (value & 0x80000000) != 0
    
    def sign_extend(self, value):
        """Sign-extend 32-bit to 64-bit"""
        if self.is_negative(value):
            return value | 0xFFFFFFFF00000000
        return value
    
    def set_flags(self, value):
        """Set status flags based on 32-bit value"""
        value = self.mask32(value)
        self.zero_flag = (value == 0)
        self.neg_flag = self.is_negative(value)
    
    def fetch(self):
        """Fetch instruction from memory"""
        self.CI = self.memory.read(self.P)
        self.cycle_count += 1
        
    def decode(self, instruction):
        """
        Decode ACE instruction.
        
        ACE instruction format (simplified for simulation):
        - Bits 31-26: Opcode (6 bits)
        - Bits 25-20: Source address (6 bits)  
        - Bits 19-14: Destination address (6 bits)
        - Bits 13-0: Unused/reserved
        
        Some instructions use different formats.
        """
        opcode = (instruction >> 26) & 0x3F
        source = (instruction >> 20) & 0x3F
        dest = (instruction >> 14) & 0x3F
        return opcode, source, dest
    
    def execute(self, opcode, source, dest):
        """Execute decoded instruction"""
        self.instructions_executed += 1
        self.cycle_count += self.cycles_per_instruction
        
        # Opcodes based on ACE instruction set
        try:
            # Load/Store (0x00-0x0F)
            if opcode == 0x00:  # NOP
                pass
                
            elif opcode == 0x01:  # ACH: Add source to AH
                value = self.memory.read(source)
                self.AH = self.mask32(self.AH + value)
                self.set_flags(self.AH)
                
            elif opcode == 0x02:  # ACL: Add source to AL
                value = self.memory.read(source)
                self.AL = self.mask32(self.AL + value)
                # Handle carry to AH
                if self.AL < value:
                    self.AH = self.mask32(self.AH + 1)
                self.set_flags(self.AL)
                
            elif opcode == 0x03:  # ADH: Add delay line to H
                value = self.memory.read(source)
                self.AH = self.mask32(self.AH + value)
                self.set_flags(self.AH)
                
            elif opcode == 0x04:  # ADL: Add delay line to L
                value = self.memory.read(source)
                old_al = self.AL
                self.AL = self.mask32(self.AL + value)
                if self.AL < old_al:
                    self.AH = self.mask32(self.AH + 1)
                self.set_flags(self.AL)
                
            elif opcode == 0x05:  # SUB: Subtract source from AL
                value = self.memory.read(source)
                self.AL = self.mask32(self.AL - value)
                self.set_flags(self.AL)
                
            elif opcode == 0x06:  # RND: Round (simplified)
                if self.AL & 0x80000000:
                    self.AH = self.mask32(self.AH + 1)
                    
            elif opcode == 0x07:  # LSH: Left shift accumulator
                self.AH = self.mask32((self.AH << 1) | (self.AL >> 31))
                self.AL = self.mask32(self.AL << 1)
                self.set_flags(self.AH)
                
            elif opcode == 0x08:  # RSH: Right shift accumulator
                self.AL = self.mask32((self.AL >> 1) | (self.AH << 31))
                self.AH = self.mask32(self.AH >> 1)
                self.set_flags(self.AH)
                
            elif opcode == 0x09:  # AND: Logical AND
                value = self.memory.read(source)
                self.AL = self.mask32(self.AL & value)
                self.set_flags(self.AL)
                
            elif opcode == 0x0A:  # OR: Logical OR
                value = self.memory.read(source)
                self.AL = self.mask32(self.AL | value)
                self.set_flags(self.AL)
                
            elif opcode == 0x0B:  # NOT: Logical NOT
                self.AL = self.mask32(~self.AL)
                self.set_flags(self.AL)
                
            elif opcode == 0x0C:  # LD: Load from delay line to AL
                self.AL = self.memory.read(source)
                self.set_flags(self.AL)
                
            elif opcode == 0x0D:  # ST: Store AL to delay line
                self.memory.write(dest, self.AL)
                
            elif opcode == 0x0E:  # JMP: Unconditional jump
                self.P = source
                return  # Skip normal PC increment
                
            elif opcode == 0x0F:  # JZ: Jump if zero
                if self.zero_flag:
                    self.P = source
                    return
                    
            elif opcode == 0x10:  # JN: Jump if negative
                if self.neg_flag:
                    self.P = source
                    return
                    
            elif opcode == 0x11:  # STOP: Halt
                self.halted = True
                return False
                
            elif opcode == 0x12:  # LDQ: Load Q from delay line
                self.Q = self.memory.read(source)
                
            elif opcode == 0x13:  # STQ: Store Q to delay line
                self.memory.write(dest, self.Q)
                
            elif opcode == 0x14:  # MLA: Multiply AL by source (software)
                # Software multiplication (ACE initially had no hardware multiply)
                multiplicand = self.memory.read(source)
                result = 0
                temp_al = self.AL
                temp_mc = multiplicand
                for i in range(32):
                    if temp_al & 1:
                        result = self.mask64(result + temp_mc)
                    temp_al >>= 1
                    temp_mc <<= 1
                self.AL = self.mask32(result)
                self.AH = self.mask32(result >> 32)
                self.set_flags(self.AL)
                
            elif opcode == 0x15:  # DIV: Divide AH:AL by source (software)
                # Software division
                divisor = self.memory.read(source)
                if divisor != 0:
                    dividend = (self.AH << 32) | self.AL
                    quotient = dividend // divisor
                    remainder = dividend % divisor
                    self.AL = self.mask32(quotient)
                    self.AH = self.mask32(remainder)
                    self.set_flags(self.AL)
                    
            elif opcode == 0x16:  # IN: Input (simulated)
                # Simulated input from "paper tape"
                self.AL = self.memory.read(source)
                
            elif opcode == 0x17:  # OUT: Output (simulated)
                # Simulated output to "teleprinter"
                value = self.memory.read(source)
                print(f"OUT: {value:08X} ({value})")
                
            else:
                print(f"WARNING: Unimplemented opcode 0x{opcode:02X} at P=0x{self.P:02X}")
                
        except Exception as e:
            print(f"ERROR executing instruction: {e}")
            self.halted = True
            return False
            
        # Increment program counter
        self.P = (self.P + 1) % self.memory.capacity
        return True
    
    def run(self, start_address=0, max_instructions=10000):
        """Run program from start address"""
        self.P = start_address
        self.instructions_executed = 0
        self.cycle_count = 0
        self.halted = False
        
        print(f"ACE starting execution at P=0x{start_address:02X}")
        print(f"Memory size: {self.memory.capacity} words")
        print(f"Clock: {self.clock_hz / 1_000_000:.0f} MHz")
        print()
        
        for i in range(max_instructions):
            if self.halted:
                print(f"\nHalted after {i} instructions")
                break
                
            self.fetch()
            opcode, source, dest = self.decode(self.CI)
            result = self.execute(opcode, source, dest)
            
            if result is False:
                break
        
        elapsed_time = self.cycle_count / self.clock_hz
        print(f"\nExecution complete:")
        print(f"  Instructions: {self.instructions_executed}")
        print(f"  Cycles: {self.cycle_count}")
        print(f"  Estimated time: {elapsed_time * 1000:.3f} ms")
        
    def load_program(self, program, start_address=0):
        """Load program into memory"""
        for i, word in enumerate(program):
            self.memory.write(start_address + i, word)
        print(f"Loaded {len(program)} words at address 0x{start_address:02X}")
    
    def dump_memory(self, start=0, length=32):
        """Dump memory contents"""
        print(f"\nMemory dump (0x{start:02X}-0x{start+length:02X}):")
        for i in range(length):
            addr = start + i
            if addr >= self.memory.capacity:
                break
            if addr % 8 == 0:
                print(f"\n0x{addr:02X}: ", end="")
            print(f"{self.memory.read(addr):08X} ", end="")
        print()
    
    def dump_registers(self):
        """Dump register contents"""
        print(f"\nRegisters:")
        print(f"  A = 0x{self.AH:08X}:{self.AL:08X} (64-bit)")
        print(f"  Q = 0x{self.Q:08X}")
        print(f"  P = 0x{self.P:02X}")
        print(f"  CI = 0x{self.CI:08X}")
        print(f"Flags:")
        print(f"  Zero = {self.zero_flag}, Negative = {self.neg_flag}, Overflow = {self.overflow_flag}")


def encode_instr(opcode, source=0, dest=0):
    """Helper to encode ACE instructions"""
    return ((opcode & 0x3F) << 26) | ((source & 0x3F) << 20) | ((dest & 0x3F) << 14)


# Test program: Add two numbers
def test_basic():
    """Test basic arithmetic"""
    print("=" * 60)
    print("ACE 1950 Simulator - Basic Arithmetic Test")
    print("=" * 60)
    
    cpu = ACECPU(memory_size=128)
    
    # Program: Load 42, add 24, store result
    # Instructions at 0-3, data at 10-12, result at 20
    program = [
        encode_instr(0x0C, 10, 0),  # 0x00: LD from addr 10 (42)
        encode_instr(0x02, 11, 0),  # 0x01: ACL from addr 11 (24)
        encode_instr(0x0D, 0, 20),  # 0x02: ST to addr 20
        encode_instr(0x11, 0, 0),   # 0x03: STOP
    ]
    # Fill rest with zeros, then add data
    program.extend([0] * 6)  # addresses 4-9
    program.extend([42, 24, 0])  # addresses 10-12: data
    program.extend([0] * 7)  # addresses 13-19
    program.append(0)  # address 20: result
    
    cpu.load_program(program)
    cpu.run()
    cpu.dump_registers()
    result = cpu.memory.read(20)
    print(f"\nResult at memory[20]: 0x{result:08X} = {result}")
    print(f"Expected: 66 (0x42)")
    
    return result == 66


# Test multiplication
def test_multiply():
    """Test software multiplication"""
    print("\n" + "=" * 60)
    print("ACE 1950 Simulator - Multiplication Test")
    print("=" * 60)
    
    cpu = ACECPU(memory_size=128)
    
    # Program: Multiply 6 × 7 = 42
    program = [
        encode_instr(0x0C, 10, 0),  # 0x00: LD from addr 10 (6)
        encode_instr(0x14, 11, 0),  # 0x01: MLA from addr 11 (7)
        encode_instr(0x0D, 0, 20),  # 0x02: ST to addr 20
        encode_instr(0x11, 0, 0),   # 0x03: STOP
    ]
    program.extend([0] * 6)  # addresses 4-9
    program.extend([6, 7, 0])  # addresses 10-12: data
    program.extend([0] * 7)  # addresses 13-19
    program.append(0)  # address 20: result
    
    cpu.load_program(program)
    cpu.run()
    cpu.dump_registers()
    result = cpu.memory.read(20)
    print(f"\nResult: {result}")
    print(f"Expected: 42")
    
    return result == 42


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("   ACE (Automatic Computing Engine) Simulator")
    print("   Alan Turing's Design - 1950")
    print("=" * 60 + "\n")
    
    test1 = test_basic()
    test2 = test_multiply()
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print(f"  Basic Arithmetic: {'PASS' if test1 else 'FAIL'}")
    print(f"  Multiplication:   {'PASS' if test2 else 'FAIL'}")
    print("=" * 60)
