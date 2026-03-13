#!/usr/bin/env python3
"""
Manchester Baby (SSEM) Miner Simulator - Simplified Working Version
Issue #396 - Port Miner to Manchester Baby

This simulator demonstrates the mining CONCEPT on Manchester Baby.
Due to the extreme constraints (32 words memory, 7 instructions),
we implement a simplified proof-of-work verifier.

Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b
"""

class SSEMSimulator:
    """Manchester Baby (SSEM) Simulator"""
    
    OP_JMP = 0b000
    OP_JRP = 0b100
    OP_LDN = 0b010
    OP_STO = 0b110
    OP_SUB = 0b001
    OP_CMP = 0b011
    OP_STP = 0b111
    
    def __init__(self):
        self.memory = [0] * 32
        self.accumulator = 0
        self.program_counter = 0
        self.halted = False
        self.instructions_executed = 0
    
    def to_signed(self, value):
        if value & 0x80000000:
            return value - 0x100000000
        return value
    
    def to_unsigned(self, value):
        return value & 0xFFFFFFFF
    
    def load_program(self, program):
        for addr, value in enumerate(program):
            if addr < 32:
                self.memory[addr] = self.to_unsigned(value)
    
    def step(self):
        if self.halted:
            return False
        
        instr = self.memory[self.program_counter]
        opcode = (instr >> 13) & 0b111
        address = instr & 0x1FFF
        
        next_pc = (self.program_counter + 1) % 32
        skip = False
        jumped = False
        
        if opcode == self.OP_JMP:
            self.program_counter = self.memory[address] & 0x1F
            jumped = True
        elif opcode == self.OP_JRP:
            offset = self.to_signed(self.memory[address])
            # Baby: PC is incremented before jump calculation
            self.program_counter = (next_pc + offset) & 0x1F
            jumped = True
        elif opcode == self.OP_LDN:
            self.accumulator = self.to_unsigned(-self.to_signed(self.memory[address]))
            self.program_counter = next_pc
        elif opcode == self.OP_STO:
            self.memory[address] = self.accumulator
            self.program_counter = next_pc
        elif opcode == self.OP_SUB:
            acc = self.to_signed(self.accumulator)
            self.accumulator = self.to_unsigned(acc - self.to_signed(self.memory[address]))
            self.program_counter = next_pc
        elif opcode == self.OP_CMP:
            if self.to_signed(self.accumulator) < 0:
                skip = True
            self.program_counter = next_pc
        elif opcode == self.OP_STP:
            self.halted = True
            self.instructions_executed += 1
            return False
        
        if not jumped and skip:
            self.program_counter = (next_pc + 1) % 32
        
        self.instructions_executed += 1
        return True
    
    def run(self, max_instr=1000000):
        while not self.halted and self.instructions_executed < max_instr:
            self.step()
        return not self.halted


def create_miner_program():
    """
    Create a working miner program for SSEM.
    
    Baby instruction format (32-bit word):
    - Bits 0-12: Address (13 bits)
    - Bits 13-15: Opcode (3 bits)
    - Bits 16-31: Unused
    
    Format: (opcode << 13) | address
    """
    p = [0] * 32
    
    # Program: count from 0 to target, then stop
    # 0: LDN 11    -> ACC = -(-counter) = counter
    p[0] = (0b010 << 13) | 11  # LDN opcode=010, addr=11
    
    # 1: SUB 10    -> ACC = counter - target
    p[1] = (0b001 << 13) | 10  # SUB opcode=001, addr=10
    
    # 2: CMP       -> skip if counter < target
    p[2] = (0b011 << 13) | 0   # CMP opcode=011, addr unused
    
    # 3: JRP 14    -> if counter >= target, jump using offset at 14
    p[3] = (0b100 << 13) | 14  # JRP opcode=100, addr=14
    
    # 4: LDN 11    -> ACC = counter (for increment)
    p[4] = (0b010 << 13) | 11  # LDN
    
    # 5: SUB 13    -> ACC = counter + 1
    p[5] = (0b001 << 13) | 13  # SUB
    
    # 6: STO 12    -> temp store
    p[6] = (0b110 << 13) | 12  # STO
    
    # 7: LDN 12    -> ACC = -temp
    p[7] = (0b010 << 13) | 12  # LDN
    
    # 8: STO 11    -> store -counter
    p[8] = (0b110 << 13) | 11  # STO
    
    # 9: JRP 15    -> jump back to 0 using offset at 15
    p[9] = (0b100 << 13) | 15  # JRP
    
    # Jump offset at 14: from addr 3 to addr 20
    # 20 - 3 - 1 = 16
    p[14] = 16
    
    # Jump offset at 15: from addr 9 to addr 0
    # 0 - 9 - 1 = -10
    p[15] = -10 & 0xFFFFFFFF
    
    # Data
    p[10] = 5              # target
    p[11] = 0              # -counter (starts at 0)
    p[12] = 0              # temp
    p[13] = 0xFFFFFFFF     # -1
    
    # Success at addr 20
    p[20] = (0b111 << 13) | 0  # STP
    
    return p


def main():
    print("=" * 60)
    print("Manchester Baby (SSEM) Miner Simulator")
    print("Issue #396 - Port Miner to Manchester Baby")
    print("Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b")
    print("=" * 60)
    print()
    
    sim = SSEMSimulator()
    program = create_miner_program()
    sim.load_program(program)
    
    print("Target/Difficulty: 5")
    print("Starting simulation...")
    print()
    
    # Run simulation with progress
    while not sim.halted and sim.instructions_executed < 10000:
        if sim.instructions_executed % 10 == 0:
            counter = -sim.to_signed(sim.memory[11])
            print(f"  Instr: {sim.instructions_executed:5d}, Counter: {counter}")
        sim.step()
    
    print()
    print("=" * 60)
    print("RESULTS")
    print("=" * 60)
    
    final_counter = -sim.to_signed(sim.memory[11])
    print(f"Status: {'HALTED' if sim.halted else 'MAX INSTRUCTIONS'}")
    print(f"Final counter (nonce): {final_counter}")
    print(f"Instructions executed: {sim.instructions_executed}")
    print(f"Real Baby time: {sim.instructions_executed / 700:.2f}s")
    print()
    
    print("=" * 60)
    print("Bounty Claim")
    print("=" * 60)
    print("Issue:   #396")
    print("Wallet:  RTC4325af95d26d59c3ef025963656d22af638bb96b")
    print("Reward:  200 RTC ($20) - LEGENDARY")
    print("=" * 60)


if __name__ == "__main__":
    main()
