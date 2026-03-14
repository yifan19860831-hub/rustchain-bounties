#!/usr/bin/env python3
"""
Altair 8800 Emulator - Intel 8080 CPU Simulator
=================================================================
Emulates the first personal computer (1975) for educational purposes.
This simulator demonstrates the conceptual mining implementation.

Hardware Specs:
- CPU: Intel 8080 @ 2 MHz
- Memory: 64 KB max
- I/O: Front panel switches and LEDs
- Bus: S-100

Author: RustChain Community
Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b
"""

import time
import struct
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class Intel8080:
    """Intel 8080 CPU Emulator"""
    
    # Registers
    A: int = 0x00      # Accumulator
    B: int = 0x00
    C: int = 0x00
    D: int = 0x00
    E: int = 0x00
    H: int = 0x00
    L: int = 0x00
    
    # Program Counter and Stack Pointer
    PC: int = 0x0000
    SP: int = 0xFFFF
    
    # Flags (Z, S, P, CY, AC)
    flag_Z: bool = False  # Zero
    flag_S: bool = False  # Sign
    flag_P: bool = False  # Parity
    flag_CY: bool = False # Carry
    flag_AC: bool = False # Auxiliary Carry
    
    # Status
    halted: bool = False
    cycles: int = 0
    
    def get_HL(self) -> int:
        """Get HL register pair"""
        return (self.H << 8) | self.L
    
    def set_HL(self, value: int):
        """Set HL register pair"""
        self.H = (value >> 8) & 0xFF
        self.L = value & 0xFF
    
    def get_BC(self) -> int:
        """Get BC register pair"""
        return (self.B << 8) | self.C
    
    def get_DE(self) -> int:
        """Get DE register pair"""
        return (self.D << 8) | self.E
    
    def update_flags(self, value: int, include_carry: bool = False):
        """Update flags based on value"""
        value &= 0xFF
        self.flag_Z = (value == 0)
        self.flag_S = (value & 0x80) != 0
        self.flag_P = bin(value).count('1') % 2 == 0
    
    def push(self, value: int, memory: bytearray):
        """Push value to stack"""
        self.SP = (self.SP - 1) & 0xFFFF
        memory[self.SP] = (value >> 8) & 0xFF
        self.SP = (self.SP - 1) & 0xFFFF
        memory[self.SP] = value & 0xFF
    
    def pop(self, memory: bytearray) -> int:
        """Pop value from stack"""
        low = memory[self.SP]
        self.SP = (self.SP + 1) & 0xFFFF
        high = memory[self.SP]
        self.SP = (self.SP + 1) & 0xFFFF
        return (high << 8) | low


@dataclass
class Altair8800:
    """Altair 8800 System Emulator"""
    
    cpu: Intel8080 = field(default_factory=Intel8080)
    memory: bytearray = field(default_factory=lambda: bytearray(65536))
    
    # I/O Ports
    switches: int = 0x00  # Front panel switches
    leds: int = 0x00      # LED display
    status: int = 0x00    # Status register
    
    # Mining state
    mining: bool = False
    nonce: int = 0
    hashes_computed: int = 0
    target_difficulty: int = 0x10
    
    # Performance
    instructions_executed: int = 0
    start_time: float = 0.0
    
    def load_program(self, program: List[int], address: int = 0x0000):
        """Load program into memory"""
        for i, byte in enumerate(program):
            self.memory[address + i] = byte & 0xFF
    
    def load_asm_file(self, filepath: str, address: int = 0x0000):
        """Load assembled binary from file"""
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
                for i, byte in enumerate(data):
                    self.memory[address + i] = byte
            print(f"[OK] Loaded {len(data)} bytes from {filepath}")
        except FileNotFoundError:
            print(f"鉁?File not found: {filepath}")
    
    def read_byte(self, address: int) -> int:
        """Read byte from memory"""
        return self.memory[address & 0xFFFF]
    
    def write_byte(self, address: int, value: int):
        """Write byte to memory"""
        self.memory[address & 0xFFFF] = value & 0xFF
    
    def read_word(self, address: int) -> int:
        """Read 16-bit word from memory"""
        low = self.memory[address & 0xFFFF]
        high = self.memory[(address + 1) & 0xFFFF]
        return (high << 8) | low
    
    def write_word(self, address: int, value: int):
        """Write 16-bit word to memory"""
        self.memory[address & 0xFFFF] = value & 0xFF
        self.memory[(address + 1) & 0xFFFF] = (value >> 8) & 0xFF
    
    def out_port(self, port: int, value: int):
        """Output to I/O port"""
        if port == 0x01:  # LED port
            self.leds = value & 0xFF
            print(f"  [LEDs] {value:02X} = {value:08b}")
        elif port == 0x02:  # Status port
            self.status = value & 0xFF
            if value & 0x01:
                print(f"[SUCCESS] Mining success! Nonce: {self.nonce}")
    
    def in_port(self, port: int) -> int:
        """Input from I/O port"""
        if port == 0x00:  # Switches
            return self.switches
        return 0x00
    
    def execute_instruction(self) -> int:
        """Execute single instruction (simplified)"""
        cpu = self.cpu
        if cpu.halted:
            return 0
        
        opcode = self.read_byte(cpu.PC)
        cpu.PC = (cpu.PC + 1) & 0xFFFF
        cycles = 4  # Default cycles
        
        # Simplified instruction decoder
        if opcode == 0x76:  # HLT
            cpu.halted = True
            cycles = 7
        elif opcode == 0xC3:  # JMP addr
            addr = self.read_word(cpu.PC)
            cpu.PC = addr
            cycles = 10
        elif opcode == 0xCD:  # CALL addr
            addr = self.read_word(cpu.PC)
            cpu.PC = (cpu.PC + 2) & 0xFFFF
            cpu.push(cpu.PC, self.memory)
            cpu.PC = addr
            cycles = 17
        elif opcode == 0xC9:  # RET
            cpu.PC = cpu.pop(self.memory)
            cycles = 10
        elif opcode == 0x00:  # NOP
            cycles = 4
        elif opcode == 0x3E:  # MVI A, data
            cpu.A = self.read_byte(cpu.PC)
            cpu.PC = (cpu.PC + 1) & 0xFFFF
            cpu.update_flags(cpu.A)
            cycles = 7
        elif opcode == 0x06:  # MVI B, data
            cpu.B = self.read_byte(cpu.PC)
            cpu.PC = (cpu.PC + 1) & 0xFFFF
            cycles = 7
        elif opcode == 0x0E:  # MVI C, data
            cpu.C = self.read_byte(cpu.PC)
            cpu.PC = (cpu.PC + 1) & 0xFFFF
            cycles = 7
        elif opcode == 0x16:  # MVI D, data
            cpu.D = self.read_byte(cpu.PC)
            cpu.PC = (cpu.PC + 1) & 0xFFFF
            cycles = 7
        elif opcode == 0x1E:  # MVI E, data
            cpu.E = self.read_byte(cpu.PC)
            cpu.PC = (cpu.PC + 1) & 0xFFFF
            cycles = 7
        elif opcode == 0x26:  # MVI H, data
            cpu.H = self.read_byte(cpu.PC)
            cpu.PC = (cpu.PC + 1) & 0xFFFF
            cycles = 7
        elif opcode == 0x2E:  # MVI L, data
            cpu.L = self.read_byte(cpu.PC)
            cpu.PC = (cpu.PC + 1) & 0xFFFF
            cycles = 7
        elif opcode == 0x3A:  # LDA addr
            addr = self.read_word(cpu.PC)
            cpu.PC = (cpu.PC + 2) & 0xFFFF
            cpu.A = self.read_byte(addr)
            cpu.update_flags(cpu.A)
            cycles = 13
        elif opcode == 0x32:  # STA addr
            addr = self.read_word(cpu.PC)
            cpu.PC = (cpu.PC + 2) & 0xFFFF
            self.write_byte(addr, cpu.A)
            cycles = 13
        elif opcode == 0x21:  # LXI H, data
            cpu.L = self.read_byte(cpu.PC)
            cpu.H = self.read_byte((cpu.PC + 1) & 0xFFFF)
            cpu.PC = (cpu.PC + 2) & 0xFFFF
            cycles = 10
        elif opcode == 0x11:  # LXI D, data
            cpu.E = self.read_byte(cpu.PC)
            cpu.D = self.read_byte((cpu.PC + 1) & 0xFFFF)
            cpu.PC = (cpu.PC + 2) & 0xFFFF
            cycles = 10
        elif opcode == 0x31:  # LXI SP, data
            low = self.read_byte(cpu.PC)
            high = self.read_byte((cpu.PC + 1) & 0xFFFF)
            cpu.SP = (high << 8) | low
            cpu.PC = (cpu.PC + 2) & 0xFFFF
            cycles = 10
        elif opcode == 0x23:  # INX H
            hl = cpu.get_HL()
            hl = (hl + 1) & 0xFFFF
            cpu.set_HL(hl)
            cycles = 5
        elif opcode == 0x13:  # INX D
            de = cpu.get_DE()
            de = (de + 1) & 0xFFFF
            cpu.D = (de >> 8) & 0xFF
            cpu.E = de & 0xFF
            cycles = 5
        elif opcode == 0x04:  # INR B
            cpu.B = (cpu.B + 1) & 0xFF
            cpu.update_flags(cpu.B)
            cycles = 5
        elif opcode == 0x0C:  # INR C
            cpu.C = (cpu.C + 1) & 0xFF
            cpu.update_flags(cpu.C)
            cycles = 5
        elif opcode == 0x3C:  # INR A
            cpu.A = (cpu.A + 1) & 0xFF
            cpu.update_flags(cpu.A)
            cycles = 5
        elif opcode == 0x78:  # MOV A, B
            cpu.A = cpu.B
            cpu.update_flags(cpu.A)
            cycles = 4
        elif opcode == 0x79:  # MOV A, C
            cpu.A = cpu.C
            cpu.update_flags(cpu.A)
            cycles = 4
        elif opcode == 0x7A:  # MOV A, D
            cpu.A = cpu.D
            cpu.update_flags(cpu.A)
            cycles = 4
        elif opcode == 0x7B:  # MOV A, E
            cpu.A = cpu.E
            cpu.update_flags(cpu.A)
            cycles = 4
        elif opcode == 0x7C:  # MOV A, H
            cpu.A = cpu.H
            cpu.update_flags(cpu.A)
            cycles = 4
        elif opcode == 0x7D:  # MOV A, L
            cpu.A = cpu.L
            cpu.update_flags(cpu.A)
            cycles = 4
        elif opcode == 0x7E:  # MOV A, M
            addr = cpu.get_HL()
            cpu.A = self.read_byte(addr)
            cpu.update_flags(cpu.A)
            cycles = 7
        elif opcode == 0x77:  # MOV M, A
            addr = cpu.get_HL()
            self.write_byte(addr, cpu.A)
            cycles = 7
        elif opcode == 0x0A:  # LDAX B
            addr = cpu.get_BC()
            cpu.A = self.read_byte(addr)
            cpu.update_flags(cpu.A)
            cycles = 7
        elif opcode == 0x1A:  # LDAX D
            addr = cpu.get_DE()
            cpu.A = self.read_byte(addr)
            cpu.update_flags(cpu.A)
            cycles = 7
        elif opcode == 0x02:  # STAX B
            addr = cpu.get_BC()
            self.write_byte(addr, cpu.A)
            cycles = 7
        elif opcode == 0x12:  # STAX D
            addr = cpu.get_DE()
            self.write_byte(addr, cpu.A)
            cycles = 7
        elif opcode == 0xA8:  # XRA B
            cpu.A ^= cpu.B
            cpu.update_flags(cpu.A)
            cycles = 4
        elif opcode == 0xA9:  # XRA C
            cpu.A ^= cpu.C
            cpu.update_flags(cpu.A)
            cycles = 4
        elif opcode == 0xAA:  # XRA D
            cpu.A ^= cpu.D
            cpu.update_flags(cpu.A)
            cycles = 4
        elif opcode == 0xAB:  # XRA E
            cpu.A ^= cpu.E
            cpu.update_flags(cpu.A)
            cycles = 4
        elif opcode == 0xAC:  # XRA H
            cpu.A ^= cpu.H
            cpu.update_flags(cpu.A)
            cycles = 4
        elif opcode == 0xAD:  # XRA L
            cpu.A ^= cpu.L
            cpu.update_flags(cpu.A)
            cycles = 4
        elif opcode == 0xAE:  # XRA M
            addr = cpu.get_HL()
            cpu.A ^= self.read_byte(addr)
            cpu.update_flags(cpu.A)
            cycles = 7
        elif opcode == 0xBF:  # CMP A
            result = cpu.A - cpu.A
            cpu.update_flags(result & 0xFF, include_carry=True)
            cycles = 4
        elif opcode == 0xB8:  # CMP B
            result = cpu.A - cpu.B
            cpu.update_flags(result & 0xFF, include_carry=True)
            cycles = 4
        elif opcode == 0xB9:  # CMP C
            result = cpu.A - cpu.C
            cpu.update_flags(result & 0xFF, include_carry=True)
            cycles = 4
        elif opcode == 0xBA:  # CMP D
            result = cpu.A - cpu.D
            cpu.update_flags(result & 0xFF, include_carry=True)
            cycles = 4
        elif opcode == 0xBB:  # CMP E
            result = cpu.A - cpu.E
            cpu.update_flags(result & 0xFF, include_carry=True)
            cycles = 4
        elif opcode == 0xBC:  # CMP H
            result = cpu.A - cpu.H
            cpu.update_flags(result & 0xFF, include_carry=True)
            cycles = 4
        elif opcode == 0xBD:  # CMP L
            result = cpu.A - cpu.L
            cpu.update_flags(result & 0xFF, include_carry=True)
            cycles = 4
        elif opcode == 0xBE:  # CMP M
            addr = cpu.get_HL()
            result = cpu.A - self.read_byte(addr)
            cpu.update_flags(result & 0xFF, include_carry=True)
            cycles = 7
        elif opcode == 0xD3:  # OUT port
            port = self.read_byte(cpu.PC)
            cpu.PC = (cpu.PC + 1) & 0xFFFF
            self.out_port(port, cpu.A)
            cycles = 10
        elif opcode == 0xDB:  # IN port
            port = self.read_byte(cpu.PC)
            cpu.PC = (cpu.PC + 1) & 0xFFFF
            cpu.A = self.in_port(port)
            cpu.update_flags(cpu.A)
            cycles = 10
        elif opcode == 0xC2:  # JNZ addr
            addr = self.read_word(cpu.PC)
            cpu.PC = (cpu.PC + 2) & 0xFFFF
            if not cpu.flag_Z:
                cpu.PC = addr
            cycles = 10 if not cpu.flag_Z else 7
        elif opcode == 0xCA:  # JZ addr
            addr = self.read_word(cpu.PC)
            cpu.PC = (cpu.PC + 2) & 0xFFFF
            if cpu.flag_Z:
                cpu.PC = addr
            cycles = 10 if cpu.flag_Z else 7
        elif opcode == 0xDA:  # JC addr
            addr = self.read_word(cpu.PC)
            cpu.PC = (cpu.PC + 2) & 0xFFFF
            if cpu.flag_CY:
                cpu.PC = addr
            cycles = 10 if cpu.flag_CY else 7
        elif opcode == 0xD2:  # JNC addr
            addr = self.read_word(cpu.PC)
            cpu.PC = (cpu.PC + 2) & 0xFFFF
            if not cpu.flag_CY:
                cpu.PC = addr
            cycles = 10 if not cpu.flag_CY else 7
        elif opcode == 0xF5:  # PUSH PSW
            psw = (cpu.A << 4) | (0x02 if cpu.flag_S else 0) | \
                  (0x04 if cpu.flag_Z else 0) | (0x08 if cpu.flag_AC else 0) | \
                  (0x10 if cpu.flag_P else 0) | (0x20 if cpu.flag_CY else 0)
            cpu.push(psw, self.memory)
            cycles = 12
        elif opcode == 0xC5:  # PUSH B
            cpu.push(cpu.get_BC(), self.memory)
            cycles = 12
        elif opcode == 0xD5:  # PUSH D
            cpu.push(cpu.get_DE(), self.memory)
            cycles = 12
        elif opcode == 0xE5:  # PUSH H
            cpu.push(cpu.get_HL(), self.memory)
            cycles = 12
        elif opcode == 0xF1:  # POP PSW
            psw = cpu.pop(self.memory)
            cpu.A = (psw >> 4) & 0xFF
            cpu.flag_S = (psw & 0x02) != 0
            cpu.flag_Z = (psw & 0x04) != 0
            cpu.flag_AC = (psw & 0x08) != 0
            cpu.flag_P = (psw & 0x10) != 0
            cpu.flag_CY = (psw & 0x20) != 0
            cycles = 10
        elif opcode == 0xC1:  # POP B
            bc = cpu.pop(self.memory)
            cpu.B = (bc >> 8) & 0xFF
            cpu.C = bc & 0xFF
            cycles = 10
        elif opcode == 0xD1:  # POP D
            de = cpu.pop(self.memory)
            cpu.D = (de >> 8) & 0xFF
            cpu.E = de & 0xFF
            cycles = 10
        elif opcode == 0xE1:  # POP H
            hl = cpu.pop(self.memory)
            cpu.set_HL(hl)
            cycles = 10
        else:
            print(f"  [CPU] Unknown opcode: {opcode:02X} at PC={cpu.PC-1:04X}")
            cycles = 4
        
        cpu.cycles += cycles
        self.instructions_executed += 1
        return cycles
    
    def run(self, max_instructions: int = 1000000, verbose: bool = False):
        """Run the emulator"""
        self.start_time = time.time()
        self.mining = True
        
        print(f"\n{'='*60}")
        print(f"Altair 8800 Emulator - Intel 8080 @ 2 MHz")
        print(f"{'='*60}")
        print(f"Starting mining simulation...")
        print(f"Target difficulty: 0x{self.target_difficulty:02X}")
        print(f"{'='*60}\n")
        
        while self.mining and self.instructions_executed < max_instructions:
            if verbose and self.instructions_executed % 1000 == 0:
                print(f"  [Progress] Nonce: {self.nonce:5d}, " +
                      f"Instructions: {self.instructions_executed:8d}")
            
            self.execute_instruction()
            
            # Check for mining success (simplified)
            if self.status & 0x01:
                print(f"\n{'='*60}")
                print(f"馃帀 MINING SUCCESS!")
                print(f"{'='*60}")
                print(f"Nonce found: {self.nonce}")
                print(f"Hashes computed: {self.hashes_computed}")
                print(f"Instructions executed: {self.instructions_executed}")
                elapsed = time.time() - self.start_time
                print(f"Time elapsed: {elapsed:.3f} seconds")
                print(f"Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b")
                print(f"{'='*60}\n")
                self.mining = False
        
        if not self.mining:
            return True
        
        print(f"\n[Timeout] Reached max instructions ({max_instructions})")
        return False


class MiningSimulator:
    """High-level mining simulation for Altair 8800"""
    
    def __init__(self, target_difficulty: int = 0x10):
        self.altair = Altair8800()
        self.target_difficulty = target_difficulty
        self.nonce = 0
        self.hashes_computed = 0
        
        # Initialize mining data structures in memory
        self._init_mining_data()
    
    def _init_mining_data(self):
        """Initialize mining data in Altair memory"""
        # Nonce storage (0x8000)
        self.altair.write_word(0x8000, 0x0000)
        
        # Target difficulty (0x8020)
        self.altair.write_byte(0x8020, self.target_difficulty)
        
        # Block header (0x8030) - dummy data
        for i in range(32):
            self.altair.write_byte(0x8030 + i, 0xAA)
        
        print(f"[OK] Mining data initialized at 0x8000")
    
    def compute_hash(self, nonce: int) -> int:
        """Compute simplified hash (XOR-based for 8080)"""
        # Simplified hash: XOR nonce with block header pattern
        header_hash = 0xAA ^ ((nonce >> 8) & 0xFF) ^ (nonce & 0xFF)
        return header_hash & 0xFF
    
    def check_target(self, hash_value: int) -> bool:
        """Check if hash meets target difficulty"""
        return hash_value < self.target_difficulty
    
    def mine(self, max_nonces: int = 10000) -> Optional[int]:
        """Run mining simulation"""
        print(f"\n{'='*60}")
        print(f"Altair 8800 Mining Simulator")
        print(f"{'='*60}")
        print(f"Target difficulty: 0x{self.target_difficulty:02X}")
        print(f"Max nonces to try: {max_nonces}")
        print(f"{'='*60}\n")
        
        start_time = time.time()
        
        for self.nonce in range(max_nonces):
            # Update nonce in memory
            self.altair.write_word(0x8000, self.nonce)
            
            # Compute hash
            hash_value = self.compute_hash(self.nonce)
            self.hashes_computed += 1
            
            # Check target
            if self.check_target(hash_value):
                elapsed = time.time() - start_time
                print(f"馃帀 MINING SUCCESS!")
                print(f"{'='*60}")
                print(f"Nonce found: {self.nonce}")
                print(f"Hash value: 0x{hash_value:02X}")
                print(f"Target: 0x{self.target_difficulty:02X}")
                print(f"Hashes computed: {self.hashes_computed}")
                print(f"Time elapsed: {elapsed:.6f} seconds")
                print(f"\nSimulated Altair 8800 @ 2 MHz:")
                print(f"  - Intel 8080 8-bit CPU")
                print(f"  - 64 KB RAM")
                print(f"  - S-100 Bus")
                print(f"  - Front panel switches & LEDs")
                print(f"\nWallet: RTC4325af95d26d59c3ef025963656d22af638bb96b")
                print(f"{'='*60}\n")
                return self.nonce
            
            # Display progress every 1000 nonces
            if self.nonce % 1000 == 0 and self.nonce > 0:
                print(f"  [Mining] Nonce: {self.nonce:5d}, " +
                      f"Best hash: 0x{hash_value:02X}")
        
        elapsed = time.time() - start_time
        print(f"\n[Timeout] No valid nonce found in {max_nonces} attempts")
        print(f"Time elapsed: {elapsed:.6f} seconds")
        return None
    
    def run_cpu_emulator(self):
        """Run the full CPU emulator with mining program"""
        # Load a simple mining program (assembled opcodes)
        # This is a minimal program that demonstrates the concept
        mining_program = [
            # Initialize stack
            0x31, 0xFF, 0xFF,  # LXI SP, 0xFFFF
            
            # Main mining loop
            0x21, 0x00, 0x80,  # LXI H, 0x8000 (nonce location)
            
            # Increment nonce
            0x04,              # INR B (nonce low)
            0xC2, 0x0B, 0x00,  # JNZ check_target (if no carry)
            0x0C,              # INR C (nonce high)
            
            # Check target (simplified)
            0x3A, 0x00, 0x80,  # LDA nonce
            0xE6, 0x0F,        # ANI 0x0F (mask to check difficulty)
            0xC2, 0x03, 0x00,  # JNZ continue_mining
            
            # Found valid nonce - output to LEDs
            0xD3, 0x01,        # OUT 0x01 (LED port)
            0x3E, 0x01,        # MVI A, 0x01
            0xD3, 0x02,        # OUT 0x02 (status port)
            0x76,              # HLT
            
            # Continue mining
            0xC3, 0x03, 0x00,  # JMP mining_loop
        ]
        
        self.altair.load_program(mining_program, 0x0000)
        self.altair.run(max_instructions=100000, verbose=True)


def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("ALT AIR 8800 MINER - RUSTCHAIN PORT")
    print("="*60)
    print("The First Personal Computer (1975)")
    print("Intel 8080 @ 2 MHz | 64 KB RAM | S-100 Bus")
    print("="*60)
    
    # Create and run mining simulator
    simulator = MiningSimulator(target_difficulty=0x10)
    result = simulator.mine(max_nonces=10000)
    
    if result is not None:
        print(f"\n鉁?Mining completed successfully!")
        print(f"   Nonce: {result}")
        print(f"   Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b")
    else:
        print(f"\n鉂?Mining did not find a valid nonce")
    
    # Optionally run CPU emulator
    print("\n" + "="*60)
    print("Running CPU Emulator Demo...")
    print("="*60)
    simulator.run_cpu_emulator()


if __name__ == "__main__":
    main()

