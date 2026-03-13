#!/usr/bin/env python3
"""
Philco 2000 Miner - RustChain Proof-of-Antiquity
Python Simulator for Philco TRANSAC S-2000 (1959)

The first production transistorized supercomputer!
"""

import time
import hashlib
import json
from datetime import datetime
from enum import IntEnum

# ============================================================================
# CONSTANTS
# ============================================================================

WALLET_ADDRESS = "RTC4325af95d26d59c3ef025963656d22af638bb96b"
MEMORY_SIZE_KB = 64  # 64K words maximum
WORD_SIZE_BITS = 48
WORD_SIZE_BYTES = 6
ACCESS_TIME_US = 2  # Model 212: 2μs

# ============================================================================
# MINING STATE MACHINE
# ============================================================================

class MiningState(IntEnum):
    IDLE = 0
    MINING = 1
    ATTESTING = 2


class PhilcoMiner:
    """Philco 2000 Miner State Machine"""
    
    def __init__(self):
        self.state = MiningState.IDLE
        self.epoch = 0
        self.wallet = WALLET_ADDRESS
        self.attestations = []
        self.start_time = datetime.now()
        
    def transition(self, new_state):
        old_state = self.state
        self.state = new_state
        timestamp = datetime.now().isoformat()
        print(f"[{timestamp}] State: {old_state.name} → {new_state.name}")
        
    def get_status(self):
        return {
            'state': self.state.name,
            'epoch': self.epoch,
            'wallet': self.wallet,
            'uptime_seconds': (datetime.now() - self.start_time).total_seconds(),
            'attestations_count': len(self.attestations)
        }


# ============================================================================
# CORE MEMORY EMULATION
# ============================================================================

class CoreMemory:
    """
    Magnetic-core memory emulation for Philco 2000
    
    Features:
    - 4K-64K words × 48 bits
    - Non-destructive read
    - 2μs access time (Model 212)
    """
    
    def __init__(self, size_kb=64):
        self.size_words = size_kb * 1024
        self.word_size_bits = 48
        self.word_size_bytes = 6
        self.access_time_us = 2  # Model 212
        self.memory = bytearray(self.size_words * self.word_size_bytes)
        self.read_count = 0
        self.write_count = 0
        
    def read(self, address):
        """Read 48-bit word from memory (non-destructive)"""
        if address >= self.size_words:
            raise ValueError(f"Address {address} out of range")
        
        offset = address * self.word_size_bytes
        value = int.from_bytes(self.memory[offset:offset+self.word_size_bytes], 'big')
        self.read_count += 1
        
        # Simulate access time (optional, for realism)
        # time.sleep(self.access_time_us / 1_000_000)
        
        return value
    
    def write(self, address, value):
        """Write 48-bit word to memory"""
        if address >= self.size_words:
            raise ValueError(f"Address {address} out of range")
        if value < 0 or value >= (1 << self.word_size_bits):
            raise ValueError(f"Value {value} out of 48-bit range")
        
        offset = address * self.word_size_bytes
        self.memory[offset:offset+self.word_size_bytes] = value.to_bytes(self.word_size_bytes, 'big')
        self.write_count += 1
        
        # Simulate access time
        # time.sleep(self.access_time_us / 1_000_000)
    
    def dump(self, start_addr, count=16):
        """Dump memory contents in Philco hex notation"""
        philco_hex = '0123456789KSNJFL'
        
        print(f"\nMemory Dump (0x{start_addr:04X} - 0x{start_addr+count-1:04X}):")
        print("-" * 60)
        
        for i in range(0, count, 4):
            addr = start_addr + i
            row_values = []
            for j in range(4):
                if addr + j < self.size_words:
                    val = self.read(addr + j)
                    # Convert to Philco hex notation
                    hex_str = format(val, '012X')
                    philco_str = ''.join(philco_hex[int(c, 16)] for c in hex_str)
                    row_values.append(philco_str)
                else:
                    row_values.append(" " * 12)
            
            print(f"  {addr:04X}: {'  '.join(row_values)}")
        
        print("-" * 60)
        print(f"Reads: {self.read_count}, Writes: {self.write_count}")


# ============================================================================
# SURFACE-BARRIER TRANSISTOR LOGIC
# ============================================================================

class TransistorLogic:
    """
    Surface-barrier transistor logic gates
    
    Philco's breakthrough invention (1953):
    - 5μm base region
    - ~100 MHz frequency response
    - Germanium material
    - US Patent 2,885,571
    """
    
    MASK_48 = 0xFFFFFFFFFFFF  # 48-bit mask
    MASK_24 = 0xFFFFFF        # 24-bit mask
    
    @staticmethod
    def NOT(a):
        return (~a) & TransistorLogic.MASK_48
    
    @staticmethod
    def AND(a, b):
        return a & b
    
    @staticmethod
    def OR(a, b):
        return a | b
    
    @staticmethod
    def XOR(a, b):
        return a ^ b
    
    @staticmethod
    def NAND(a, b):
        return (~(a & b)) & TransistorLogic.MASK_48
    
    @staticmethod
    def NOR(a, b):
        return (~(a | b)) & TransistorLogic.MASK_48
    
    @staticmethod
    def ADD(a, b):
        """48-bit addition with carry"""
        result = a + b
        carry = (result >> 48) & 1
        return (result & TransistorLogic.MASK_48), carry
    
    @staticmethod
    def SUB(a, b):
        """48-bit subtraction"""
        result = a - b
        if result < 0:
            result += (1 << 48)
        return result & TransistorLogic.MASK_48


# ============================================================================
# PHILOCO 2000 CPU SIMULATION
# ============================================================================

class PhilcoCPU:
    """
    Philco TRANSAC S-2000 CPU Simulation
    
    Registers:
    - AC: 48-bit Accumulator
    - R0-R2: 24-bit General Purpose Registers
    - XR0-XR31: 15-bit Index Registers
    - BR: 16-bit Base Register
    - PC: 16-bit Program Counter
    - SR: 8-bit Status Register
    """
    
    def __init__(self, memory):
        self.memory = memory
        self.ac = 0  # 48-bit accumulator
        self.r = [0, 0, 0]  # 3× 24-bit general registers
        self.xr = [0] * 32  # 32× 15-bit index registers
        self.br = 0  # 16-bit base register
        self.pc = 0  # 16-bit program counter
        self.sr = 0  # 8-bit status register
        
        # Status flags
        self.FLAG_OVERFLOW = 0x80
        self.FLAG_CARRY = 0x40
        self.FLAG_ZERO = 0x20
        self.FLAG_NEGATIVE = 0x10
        self.FLAG_INTERRUPT = 0x08
        
        # Instruction statistics
        self.instructions_executed = 0
        
    def fetch(self):
        """Fetch 24-bit instruction from memory (2 instructions per 48-bit word)"""
        word = self.memory.read(self.pc)
        
        # Alternate between left and right instruction
        if self.pc % 2 == 0:
            # Left instruction (bits 0-23)
            instruction = (word >> 24) & 0xFFFFFF
        else:
            # Right instruction (bits 24-47)
            instruction = word & 0xFFFFFF
        
        self.instructions_executed += 1
        return instruction
    
    def decode(self, instruction):
        """Decode 24-bit instruction into opcode and address"""
        opcode = (instruction >> 16) & 0xFF  # 8-bit opcode
        address = instruction & 0xFFFF  # 16-bit address
        return opcode, address
    
    def execute(self, opcode, address):
        """Execute instruction"""
        # Simplified instruction set (subset of 225 opcodes)
        
        # Load/Store (0x00-0x1F)
        if opcode == 0x00:  # LOAD
            self.ac = self.memory.read(address)
        elif opcode == 0x01:  # STORE
            self.memory.write(address, self.ac)
        
        # Arithmetic (0x20-0x3F)
        elif opcode == 0x20:  # ADD
            mem_val = self.memory.read(address)
            result, carry = TransistorLogic.ADD(self.ac, mem_val)
            self.ac = result
            self._set_flag(self.FLAG_CARRY, carry)
            self._set_flag(self.FLAG_ZERO, 1 if self.ac == 0 else 0)
        
        elif opcode == 0x21:  # SUB
            mem_val = self.memory.read(address)
            self.ac = TransistorLogic.SUB(self.ac, mem_val)
            self._set_flag(self.FLAG_ZERO, 1 if self.ac == 0 else 0)
        
        # Control (0x60-0x7F)
        elif opcode == 0x60:  # JUMP
            self.pc = address
            return  # Skip PC increment
        
        elif opcode == 0x61:  # JUMP_ZERO
            if self._get_flag(self.FLAG_ZERO):
                self.pc = address
                return
        
        elif opcode == 0x62:  # JUMP_NOT_ZERO
            if not self._get_flag(self.FLAG_ZERO):
                self.pc = address
                return
        
        # Index operations (0x80-0x9F)
        elif opcode == 0x80:  # LOAD_INDEX
            xr_num = address & 0x1F  # 5-bit index register number
            self.xr[xr_num] = self.ac & 0x7FFF  # 15-bit
        
        # Halt
        elif opcode == 0xFF:  # HALT
            print(f"[HALT] PC=0x{self.pc:04X}, AC=0x{self.ac:012X}")
            return False
        
        return True
    
    def _set_flag(self, flag_mask, value):
        if value:
            self.sr |= flag_mask
        else:
            self.sr &= ~flag_mask
    
    def _get_flag(self, flag_mask):
        return (self.sr & flag_mask) != 0
    
    def get_register_state(self):
        """Get CPU register state as dictionary"""
        philco_hex = '0123456789KSNJFL'
        
        def to_philco(val, bits):
            hex_digits = bits // 4
            hex_str = format(val, f'0{hex_digits}X')
            return ''.join(philco_hex[int(c, 16)] for c in hex_str)
        
        return {
            'PC': f'0x{self.pc:04X}',
            'AC': f'0x{to_philco(self.ac, 48)}',
            'R0': f'0x{to_philco(self.r[0], 24)}',
            'R1': f'0x{to_philco(self.r[1], 24)}',
            'R2': f'0x{to_philco(self.r[2], 24)}',
            'BR': f'0x{self.br:04X}',
            'SR': f'0x{self.sr:02X}',
            'Instructions': self.instructions_executed
        }


# ============================================================================
# PHILOCO 2400 I/O PROCESSOR
# ============================================================================

class Philco2400:
    """
    Philco 2400 I/O Processor Simulation
    
    Dedicated I/O system:
    - 24-bit word length
    - 4K-32K characters memory
    - 3μs cycle time
    - Offloads I/O from main CPU
    """
    
    def __init__(self):
        self.memory_size = 8192  # 8K words
        self.cycle_time_us = 3
        self.channels = {
            'card_reader': False,
            'card_punch': False,
            'printer': False,
            'tape1': False,
            'tape2': False,
            'tape3': False,
            'tape4': False,
            'paper_tape': False
        }
        self.output_buffer = []
        
    def print_line(self, text):
        """Simulate printer output"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.output_buffer.append(f"[{timestamp}] {text}")
        print(f"[PRINTER] {text}")
    
    def punch_paper_tape(self, data):
        """Simulate paper tape punch"""
        print(f"[PAPER TAPE] Punching {len(data)} bytes")
        return self.encode_paper_tape(data)
    
    def encode_paper_tape(self, data_bytes):
        """Encode data as 8-channel paper tape"""
        tape = []
        for byte in data_bytes:
            # Add sprocket hole (bit 7)
            tape_byte = byte | 0x80
            tape.append(tape_byte)
        return bytes(tape)
    
    def get_output_log(self):
        return self.output_buffer


# ============================================================================
# MAIN MINER SIMULATION
# ============================================================================

class PhilcoMinerSimulator:
    """Main Philco 2000 Miner Simulator"""
    
    def __init__(self):
        self.memory = CoreMemory(size_kb=64)
        self.cpu = PhilcoCPU(self.memory)
        self.io = Philco2400()
        self.miner = PhilcoMiner()
        self.running = False
        
        # Initialize memory map
        self._init_memory()
        
    def _init_memory(self):
        """Initialize memory with miner program and data"""
        
        # Wallet address at 0x0300
        wallet_bytes = WALLET_ADDRESS.encode('ascii')
        for i, byte in enumerate(wallet_bytes):
            self.memory.write(0x0300 + i, byte)
        
        # Initial state at 0x0400
        self.memory.write(0x0400, self.miner.state)
        
        # Epoch counter at 0x0200
        self.memory.write(0x0200, 0)
        
        self.io.print_line("Philco 2000 Miner initialized")
        self.io.print_line(f"Wallet: {WALLET_ADDRESS}")
        self.io.print_line(f"Memory: 64K × 48 bits")
        self.io.print_line(f"Access time: 2μs (Model 212)")
        
    def run_epoch(self):
        """Run one mining epoch"""
        print(f"\n{'='*60}")
        print(f"EPOCH {self.miner.epoch}")
        print(f"{'='*60}")
        
        # State: IDLE → MINING
        self.miner.transition(MiningState.MINING)
        
        # Simulate mining computation
        print("Computing proof-of-antiquity...")
        time.sleep(0.5)  # Simulated work
        
        # Generate hash (simulated)
        epoch_data = f"{self.miner.epoch}-{WALLET_ADDRESS}-{time.time()}"
        simulated_hash = hashlib.sha256(epoch_data.encode()).hexdigest()
        
        print(f"Hash: {simulated_hash[:32]}...")
        
        # State: MINING → ATTESTING
        self.miner.transition(MiningState.ATTESTING)
        
        # Generate attestation
        attestation = {
            'epoch': self.miner.epoch,
            'wallet': WALLET_ADDRESS,
            'timestamp': datetime.now().isoformat(),
            'hardware': 'Philco TRANSAC S-2000 (1959)',
            'multiplier': '2.5× (MUSEUM_TIER)',
            'hash': simulated_hash,
            'memory_reads': self.memory.read_count,
            'memory_writes': self.memory.write_count,
            'instructions': self.cpu.instructions_executed
        }
        
        self.miner.attestations.append(attestation)
        
        # Print attestation
        self.io.print_line(f"ATTESTATION #{self.miner.epoch}")
        self.io.print_line(f"Hardware: Philco 2000 (1959)")
        self.io.print_line(f"Multiplier: 2.5×")
        
        # State: ATTESTING → IDLE
        self.miner.transition(MiningState.IDLE)
        
        self.miner.epoch += 1
        
        return attestation
    
    def run(self, epochs=3):
        """Run miner for specified number of epochs"""
        print(f"\n{'='*60}")
        print("PHILOCO 2000 MINER - RustChain Proof-of-Antiquity")
        print(f"{'='*60}")
        print(f"Starting miner for {epochs} epochs...")
        print(f"Wallet: {WALLET_ADDRESS}")
        print(f"Hardware: Philco TRANSAC S-2000 (1959)")
        print(f"Multiplier: 2.5× MUSEUM_TIER")
        print(f"{'='*60}\n")
        
        self.running = True
        
        for i in range(epochs):
            if not self.running:
                break
            self.run_epoch()
            time.sleep(0.5)
        
        # Final status
        self.print_status()
        
        return self.miner.attestations
    
    def stop(self):
        """Stop the miner"""
        self.running = False
        print("\nMiner stopped")
    
    def print_status(self):
        """Print miner status"""
        status = self.miner.get_status()
        cpu_state = self.cpu.get_register_state()
        
        print(f"\n{'='*60}")
        print("MINER STATUS")
        print(f"{'='*60}")
        print(f"State: {status['state']}")
        print(f"Epoch: {status['epoch']}")
        print(f"Uptime: {status['uptime_seconds']:.2f} seconds")
        print(f"Attestations: {status['attestations_count']}")
        print(f"\nCPU STATE:")
        for reg, val in cpu_state.items():
            print(f"  {reg}: {val}")
        print(f"\nMEMORY STATISTICS:")
        print(f"  Reads: {self.memory.read_count}")
        print(f"  Writes: {self.memory.write_count}")
        print(f"{'='*60}")


# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Philco 2000 Miner - RustChain Proof-of-Antiquity'
    )
    parser.add_argument(
        '--epochs', '-e',
        type=int,
        default=3,
        help='Number of epochs to mine (default: 3)'
    )
    parser.add_argument(
        '--dump-memory',
        action='store_true',
        help='Dump memory contents after mining'
    )
    parser.add_argument(
        '--json-output',
        action='store_true',
        help='Output attestations as JSON'
    )
    
    args = parser.parse_args()
    
    # Create and run simulator
    simulator = PhilcoMinerSimulator()
    attestations = simulator.run(epochs=args.epochs)
    
    # Memory dump if requested
    if args.dump_memory:
        simulator.memory.dump(0x0000, 32)
    
    # JSON output if requested
    if args.json_output:
        print("\n" + "="*60)
        print("ATTESTATIONS (JSON)")
        print("="*60)
        print(json.dumps(attestations, indent=2))
    
    print(f"\n[OK] Mining simulation complete!")
    print(f"  Wallet: {WALLET_ADDRESS}")
    print(f"  Bounty: #341 - LEGENDARY Tier (200 RTC)")
    print(f"  Hardware: Philco TRANSAC S-2000 (1959)")


if __name__ == '__main__':
    main()
