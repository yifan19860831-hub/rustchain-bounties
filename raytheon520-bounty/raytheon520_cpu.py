#!/usr/bin/env python3
"""
Raytheon 520 CPU Simulator
===========================
Simulates the first fully transistorized computer (1960).

Architecture:
- 18-bit word size
- 6 μs memory cycle time
- ~3,000 discrete transistors
- Magnetic core memory (4K-32K words)
- Single-address instruction format

Author: RustChain Bounty Hunter
Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b
License: MIT
"""

from typing import Optional, List, Dict
from dataclasses import dataclass
import time


class StatusFlags:
    """Raytheon 520 status flags"""
    def __init__(self):
        self.overflow = False
        self.carry = False
        self.zero = False
        self.sign = False
    
    def reset(self):
        self.overflow = False
        self.carry = False
        self.zero = False
        self.sign = False
    
    def __repr__(self):
        flags = []
        if self.overflow: flags.append('O')
        if self.carry: flags.append('C')
        if self.zero: flags.append('Z')
        if self.sign: flags.append('S')
        return ''.join(flags) if flags else '-'


@dataclass
class Instruction:
    """Raytheon 520 instruction (18 bits)"""
    opcode: int = 0
    indirect: bool = False
    indexed: bool = False
    address: int = 0
    
    def encode(self) -> int:
        return ((self.opcode & 0x3F) << 12) | \
               ((1 if self.indirect else 0) << 11) | \
               ((1 if self.indexed else 0) << 10) | \
               (self.address & 0x3FF)
    
    @classmethod
    def decode(cls, word: int) -> 'Instruction':
        return cls(
            opcode=(word >> 12) & 0x3F,
            indirect=bool((word >> 11) & 0x01),
            indexed=bool((word >> 10) & 0x01),
            address=word & 0x3FF
        )


class Raytheon520CPU:
    """Raytheon 520 CPU Simulator (1960)"""
    
    OP_CLA, OP_ADD, OP_SUB, OP_MUL, OP_DIV = 0x00, 0x01, 0x02, 0x03, 0x04
    OP_STO, OP_STQ, OP_LDI, OP_STI, OP_JMP = 0x05, 0x06, 0x07, 0x08, 0x09
    OP_JZ, OP_JN, OP_JO, OP_AND, OP_OR = 0x0A, 0x0B, 0x0C, 0x0D, 0x0E
    OP_XOR, OP_SHL, OP_SHR, OP_RCL, OP_RCR = 0x0F, 0x10, 0x11, 0x12, 0x13
    OP_IN, OP_OUT, OP_HLT, OP_NOP = 0x14, 0x15, 0x16, 0x17
    
    WORD_MASK = 0x3FFFF
    SIGN_BIT = 0x20000
    
    def __init__(self, memory_size: int = 4096):
        self.AC = self.MQ = self.XR = self.PC = 0
        self.flags = StatusFlags()
        self.memory_size = min(memory_size, 32768)
        self.memory = [0] * self.memory_size
        self.cycle_time_us = 6.0
        self.clock_cycles = self.instructions_executed = 0
        self.io_registers: Dict[int, int] = {}
        self.running = self.halted = False
    
    def reset(self):
        self.AC = self.MQ = self.XR = self.PC = 0
        self.flags.reset()
        self.clock_cycles = self.instructions_executed = 0
        self.running = self.halted = False
    
    def fetch(self, address: int) -> int:
        if address >= self.memory_size:
            raise MemoryError(f"Address {address} out of range")
        self.clock_cycles += 1
        return self.memory[address] & self.WORD_MASK
    
    def store(self, address: int, value: int):
        if address >= self.memory_size:
            raise MemoryError(f"Address {address} out of range")
        self.memory[address] = value & self.WORD_MASK
        self.clock_cycles += 1
    
    def _set_flags(self, value: int):
        masked = value & self.WORD_MASK
        self.flags.zero = (masked == 0)
        self.flags.sign = (masked & self.SIGN_BIT) != 0
        self.flags.overflow = (value > self.WORD_MASK or value < -0x20000)
        self.flags.carry = (value > self.WORD_MASK)
    
    def _effective_address(self, instr: Instruction) -> int:
        addr = instr.address
        if instr.indexed:
            addr = (addr + self.XR) & 0x7FFF
        if instr.indirect:
            addr = self.fetch(addr) & 0x7FFF
        return addr
    
    def execute_instruction(self, instr: Instruction):
        op = instr.opcode
        
        if op == self.OP_NOP:
            pass
        elif op == self.OP_CLA:
            self.AC = self.fetch(self._effective_address(instr))
            self._set_flags(self.AC)
        elif op == self.OP_ADD:
            result = self.AC + self.fetch(self._effective_address(instr))
            self._set_flags(result)
            self.AC = result & self.WORD_MASK
        elif op == self.OP_SUB:
            result = self.AC - self.fetch(self._effective_address(instr))
            self._set_flags(result)
            self.AC = result & self.WORD_MASK
        elif op == self.OP_MUL:
            operand = self.fetch(self._effective_address(instr))
            result = (self.AC & 0xFFFF) * (operand & 0xFFFF)
            self.MQ = result & self.WORD_MASK
            self.AC = (result >> 18) & self.WORD_MASK
        elif op == self.OP_DIV:
            operand = self.fetch(self._effective_address(instr))
            if operand == 0:
                raise ZeroDivisionError("Division by zero")
            dividend = ((self.AC & 0xFFFF) << 18) | (self.MQ & 0xFFFF)
            self.AC = dividend // operand
            self.MQ = dividend % operand
        elif op == self.OP_STO:
            self.store(self._effective_address(instr), self.AC)
        elif op == self.OP_STQ:
            self.store(self._effective_address(instr), self.MQ)
        elif op == self.OP_LDI:
            self.XR = self.fetch(self._effective_address(instr)) & 0x7FFF
        elif op == self.OP_STI:
            self.store(self._effective_address(instr), self.XR)
        elif op == self.OP_JMP:
            self.PC = instr.address
            return
        elif op == self.OP_JZ and self.flags.zero:
            self.PC = instr.address
            return
        elif op == self.OP_JN and self.flags.sign:
            self.PC = instr.address
            return
        elif op == self.OP_JO and self.flags.overflow:
            self.PC = instr.address
            return
        elif op == self.OP_AND:
            self.AC &= self.fetch(self._effective_address(instr))
            self._set_flags(self.AC)
        elif op == self.OP_OR:
            self.AC |= self.fetch(self._effective_address(instr))
            self._set_flags(self.AC)
        elif op == self.OP_XOR:
            self.AC ^= self.fetch(self._effective_address(instr))
            self._set_flags(self.AC)
        elif op == self.OP_SHL:
            self.AC = (self.AC << (instr.address & 0x1F)) & self.WORD_MASK
            self._set_flags(self.AC)
        elif op == self.OP_SHR:
            self.AC = (self.AC >> (instr.address & 0x1F)) & self.WORD_MASK
            self._set_flags(self.AC)
        elif op == self.OP_RCL:
            shift = instr.address & 0x1F
            self.AC = ((self.AC << shift) | (self.AC >> (18 - shift))) & self.WORD_MASK
            self._set_flags(self.AC)
        elif op == self.OP_RCR:
            shift = instr.address & 0x1F
            self.AC = ((self.AC >> shift) | (self.AC << (18 - shift))) & self.WORD_MASK
            self._set_flags(self.AC)
        elif op == self.OP_IN:
            self.AC = self.io_registers.get(instr.address & 0xFF, 0)
        elif op == self.OP_OUT:
            self.io_registers[instr.address & 0xFF] = self.AC
        elif op == self.OP_HLT:
            self.halted = True
            self.running = False
            return
        else:
            raise NotImplementedError(f"Opcode {op:02X} not implemented")
        
        self.instructions_executed += 1
        self.clock_cycles += 1
    
    def step(self) -> bool:
        if self.halted:
            return False
        instr = Instruction.decode(self.fetch(self.PC))
        self.PC = (self.PC + 1) & 0x7FFF
        self.execute_instruction(instr)
        return not self.halted
    
    def run(self, start_address: int = 0, max_instructions: Optional[int] = None):
        self.PC = start_address
        self.running = True
        self.halted = False
        count = 0
        while self.running and not self.halted:
            if max_instructions and count >= max_instructions:
                break
            self.step()
            count += 1
        self.running = False
    
    def load_program(self, program: List[int], start_address: int = 0):
        for i, word in enumerate(program):
            self.store(start_address + i, word)
    
    def dump_registers(self) -> str:
        return f"AC={self.AC:05X} MQ={self.MQ:05X} XR={self.XR:04X} PC={self.PC:04X} Flags=[{self.flags}]"
    
    def dump_memory(self, start: int = 0, length: int = 16) -> str:
        lines = []
        for i in range(0, length, 8):
            addr = start + i
            words = [f"{self.fetch(addr + j):05X}" for j in range(min(8, length - i))]
            lines.append(f"{addr:04X}: {' '.join(words)}")
        return '\n'.join(lines)


def make_instruction(opcode: int, address: int = 0, indirect: bool = False, indexed: bool = False) -> int:
    return Instruction(opcode=opcode, indirect=indirect, indexed=indexed, address=address).encode()


if __name__ == '__main__':
    print("Raytheon 520 CPU Simulator")
    print("=" * 50)
    
    cpu = Raytheon520CPU()
    
    # Test program: Add two numbers
    program = [
        make_instruction(Raytheon520CPU.OP_CLA, 0x100),
        make_instruction(Raytheon520CPU.OP_ADD, 0x101),
        make_instruction(Raytheon520CPU.OP_STO, 0x102),
        make_instruction(Raytheon520CPU.OP_HLT),
    ]
    
    cpu.load_program(program, 0)
    cpu.store(0x100, 0x12345)
    cpu.store(0x101, 0x05000)
    
    print(f"Initial: {cpu.dump_registers()}")
    print(f"Data: [0x100]={cpu.fetch(0x100):05X} [0x101]={cpu.fetch(0x101):05X}")
    
    cpu.run()
    
    print(f"Final:   {cpu.dump_registers()}")
    print(f"Result:  [0x102]={cpu.fetch(0x102):05X}")
    print(f"Instructions: {cpu.instructions_executed}, Cycles: {cpu.clock_cycles}")
    print(f"Simulated time: {cpu.clock_cycles * cpu.cycle_time_us / 1000:.3f} ms")
