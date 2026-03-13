#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IBM 7094 Miner - RustChain Proof-of-Antiquity
Main simulator entry point

Simulates mining on the legendary IBM 7094 (1962) mainframe
that guided NASA's Mercury and Gemini missions and sang "Daisy Bell"

Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b
Bounty: #331 - LEGENDARY Tier (200 RTC / $20)
"""

import sys
import time
import random
from datetime import datetime
from enum import IntEnum

# Import simulation modules
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core_memory import CoreMemory
from index_registers import IndexRegisters
from data_channels import DataChannels
from punched_card import PunchedCard
from magnetic_tape import MagneticTape


class MiningState(IntEnum):
    """Mining state machine states"""
    IDLE = 0
    MINING = 1
    ATTESTING = 2
    OUTPUT = 3


class IBM7094Miner:
    """
    IBM 7094 Miner Simulator
    
    Emulates the IBM 7094 mainframe computer from 1962
    for RustChain Proof-of-Antiquity demonstration
    """
    
    def __init__(self, verbose=True):
        """Initialize the IBM 7094 miner simulation"""
        self.verbose = verbose
        
        # Core memory: 32,768 words  36 bits
        self.memory = CoreMemory(size=32768, word_size=36)
        
        # Index registers: XR1-XR7
        self.index_registers = IndexRegisters(count=7, word_size=36)
        
        # Data channels: 8 channels for I/O
        self.data_channels = DataChannels(channels=8)
        
        # Punched card I/O
        self.card_reader = PunchedCard()
        self.card_punch = PunchedCard()
        
        # Magnetic tape storage
        self.tape_drive = MagneticTape(drive_number=0)
        
        # CPU registers
        self.ac = 0  # Accumulator (36 bits)
        self.mq = 0  # Multiplier-Quotient (36 bits)
        self.ic = 0  # Instruction Counter (15 bits)
        self.sense_indicators = 0  # 36 sense bits
        
        # Mining state
        self.state = MiningState.IDLE
        self.epoch = 0
        self.wallet_address = "RTC4325af95d26d59c3ef025963656d22af638bb96b"
        
        # Statistics
        self.instructions_executed = 0
        self.attestations_generated = 0
        self.start_time = datetime.now()
        
        if self.verbose:
            self._print_banner()
    
    def _print_banner(self):
        """Print startup banner"""
        print("=" * 70)
        print("  IBM 7094 MINER - RustChain Proof-of-Antiquity")
        print("  Simulating legendary 1962 mainframe computer")
        print("=" * 70)
        print()
        print("  [CPU] CPU: 36-bit transistorized mainframe")
        print("  [MEM] Memory: 32,768 words x 36 bits (magnetic-core)")
        print("  [I/O] I/O: Punched cards + Magnetic tape")
        print("  [MUS] Famous for: First computer to sing 'Daisy Bell' (1961)")
        print("  [NASA] NASA: Mercury & Gemini flight control")
        print()
        print(f"  Wallet: {self.wallet_address}")
        print(f"  Bounty: #331 - LEGENDARY Tier (200 RTC / $20)")
        print("=" * 70)
        print()
    
    def initialize(self):
        """Initialize the miner state"""
        if self.verbose:
            print("[INIT] Initializing IBM 7094 miner...")
            print()
        
        # Clear core memory
        self.memory.clear()
        
        # Clear index registers
        self.index_registers.clear()
        
        # Reset CPU registers
        self.ac = 0
        self.mq = 0
        self.ic = 0
        self.sense_indicators = 0
        
        # Initialize mining state
        self.state = MiningState.IDLE
        self.epoch = 0
        
        # Load miner program into memory
        self._load_miner_program()
        
        # Initialize data channels
        self.data_channels.initialize()
        
        # Prepare tape drive
        self.tape_drive.initialize()
        
        if self.verbose:
            print("?Initialization complete")
            print(f"   - Core memory: {self.memory.size} words  {self.memory.word_size} bits")
            print(f"   - Index registers: {self.index_registers.count} registers")
            print(f"   - Data channels: {self.data_channels.channels} channels")
            print(f"   - Initial state: {self.state.name}")
            print()
    
    def _load_miner_program(self):
        """Load the miner program into core memory"""
        if self.verbose:
            print(" Loading miner program into core memory...")
        
        # Memory map:
        # 0x0000-0x007F: System reserved
        # 0x0080-0x00FF: Miner entry point
        # 0x0100-0x03FF: Miner program code
        # 0x0400-0x04FF: Epoch counters
        # 0x0500-0x05FF: Wallet address storage
        # 0x0600-0x07FF: Working registers
        
        # Store epoch counter at 0x0400
        self.memory.write(0x0400, self.epoch)
        
        # Store mining state at 0x0401
        self.memory.write(0x0401, int(self.state))
        
        # Store wallet address (packed into multiple words)
        wallet_words = self._pack_wallet_address(self.wallet_address)
        for i, word in enumerate(wallet_words):
            self.memory.write(0x0500 + i, word)
        
        # Store program entry point
        self.ic = 0x0080
        
        if self.verbose:
            print(f"   - Program loaded at 0x0100-0x03FF")
            print(f"   - Epoch counter at 0x0400")
            print(f"   - Wallet address at 0x0500-0x050F")
            print(f"   - Entry point: 0x{self.ic:04X}")
            print()
    
    def _pack_wallet_address(self, address):
        """Pack wallet address string into 36-bit words"""
        # Each 36-bit word can hold 6 characters (6-bit BCD)
        words = []
        for i in range(0, len(address), 6):
            chunk = address[i:i+6]
            word = 0
            for j, char in enumerate(chunk):
                # Simple ASCII to 6-bit encoding (simplified)
                char_code = ord(char) & 0x3F
                word |= (char_code << (30 - j * 6))
            words.append(word)
        return words
    
    def run(self, max_epochs=10):
        """
        Run the miner simulation
        
        Args:
            max_epochs: Maximum number of epochs to mine
        """
        if self.verbose:
            print(" Starting IBM 7094 miner simulation...")
            print(f"   - Target epochs: {max_epochs}")
            print()
        
        try:
            for epoch in range(max_epochs):
                self.epoch = epoch
                self._run_epoch()
                
                # Small delay for realism
                time.sleep(0.5)
            
            self._print_summary()
            
        except KeyboardInterrupt:
            print("\n  Miner interrupted by user")
            self._print_summary()
    
    def _run_epoch(self):
        """Run a single mining epoch"""
        if self.verbose:
            print(f"  Epoch {self.epoch + 1}:")
        
        # State transition: IDLE ?MINING
        self.state = MiningState.MINING
        self.memory.write(0x0401, int(self.state))
        
        if self.verbose:
            print(f"   - State: {self.state.name}")
        
        # Simulate mining computation
        self._simulate_mining()
        
        # State transition: MINING ?ATTESTING
        self.state = MiningState.ATTESTING
        self.memory.write(0x0401, int(self.state))
        
        if self.verbose:
            print(f"   - State: {self.state.name}")
        
        # Generate attestation
        attestation = self._generate_attestation()
        
        # State transition: ATTESTING ?OUTPUT
        self.state = MiningState.OUTPUT
        self.memory.write(0x0401, int(self.state))
        
        if self.verbose:
            print(f"   - State: {self.state.name}")
        
        # Output attestation
        self._output_attestation(attestation)
        
        # State transition: OUTPUT ?IDLE
        self.state = MiningState.IDLE
        self.memory.write(0x0401, int(self.state))
        
        self.attestations_generated += 1
        
        if self.verbose:
            print(f"   ?Attestation generated")
            print()
    
    def _simulate_mining(self):
        """Simulate the mining computation"""
        if self.verbose:
            print("     Mining (simulating proof-of-antiquity)...")
        
        # Simulate instruction execution
        instructions = random.randint(1000, 5000)
        self.instructions_executed += instructions
        
        # Simulate timing (2.18 s per memory cycle)
        # For demonstration, we'll speed this up significantly
        time.sleep(0.1)
        
        # Compute "proof" (simulated hash)
        proof = self._compute_proof()
        
        # Store proof in memory
        self.memory.write(0x0600, proof)
        
        if self.verbose:
            print(f"   - Instructions executed: {instructions}")
            print(f"   - Proof stored at 0x0600")
    
    def _compute_proof(self):
        """
        Compute proof-of-antiquity
        
        Returns:
            36-bit proof value
        """
        # Simple deterministic "hash" based on epoch and wallet
        epoch_data = self.epoch
        wallet_hash = sum(ord(c) for c in self.wallet_address)
        
        # Combine and mask to 36 bits
        proof = (epoch_data * 12345 + wallet_hash) & 0xFFFFFFFFF
        
        return proof
    
    def _generate_attestation(self):
        """
        Generate attestation record
        
        Returns:
            Dictionary with attestation data
        """
        proof = self.memory.read(0x0600)
        
        attestation = {
            'epoch': self.epoch,
            'state': int(self.state),
            'proof': proof,
            'timestamp': datetime.now().isoformat(),
            'wallet': self.wallet_address,
            'antiquity_multiplier': 2.5,  # Museum tier (pre-1980)
            'computer': 'IBM 7094',
            'year': 1962,
            'technology': 'Germanium transistors',
            'memory': '32K  36-bit magnetic-core',
        }
        
        return attestation
    
    def _output_attestation(self, attestation):
        """Output attestation to punched cards and magnetic tape"""
        if self.verbose:
            print("    Outputting attestation...")
        
        # Punch onto card
        card_data = self._format_attestation_card(attestation)
        self.card_punch.punch(card_data)
        
        # Write to tape
        tape_data = self._format_attestation_tape(attestation)
        self.tape_drive.write_record(tape_data)
        
        if self.verbose:
            print(f"   - Punched card: {len(card_data)} columns")
            print(f"   - Tape record: {len(tape_data)} bytes")
    
    def _format_attestation_card(self, attestation):
        """Format attestation as punched card data"""
        # 80-column card format
        card = f"EPOCH:{attestation['epoch']:06d} PROOF:{attestation['proof']:010o} IBM7094"
        return card.ljust(80)[:80]
    
    def _format_attestation_tape(self, attestation):
        """Format attestation as magnetic tape record"""
        # Binary tape record format
        import struct
        record = struct.pack('>I', attestation['epoch'])
        record += struct.pack('>I', attestation['proof'])
        record += struct.pack('>I', int(attestation['state']))
        return record
    
    def _print_summary(self):
        """Print mining summary"""
        elapsed = datetime.now() - self.start_time
        
        print()
        print("=" * 70)
        print("  IBM 7094 MINER - SUMMARY")
        print("=" * 70)
        print()
        print(f"  Runtime: {elapsed}")
        print(f"  Epochs completed: {self.epoch + 1}")
        print(f"  Attestations generated: {self.attestations_generated}")
        print(f"  Instructions executed: {self.instructions_executed:,}")
        print()
        print(f"  Wallet: {self.wallet_address}")
        print(f"  Bounty: #331 - LEGENDARY Tier (200 RTC / $20)")
        print()
        print("   Antiquity Multiplier: 2.5 (Museum tier)")
        print("  ? Computer: IBM 7094 (1962)")
        print("   Technology: Germanium transistors")
        print("   Memory: 32K  36-bit magnetic-core")
        print()
        print("=" * 70)
        print()
        print("  Thank you for running the IBM 7094 Miner!")
        print("  This is a conceptual demonstration honoring computing history.")
        print()
    
    def dump_memory(self, start=0, length=32):
        """Dump a section of core memory"""
        print(f"\n Core Memory Dump (0x{start:04X} - 0x{start+length-1:04X}):")
        print("-" * 50)
        
        for i in range(0, length, 4):
            addr = start + i
            words = [self.memory.read(addr + j) for j in range(4)]
            print(f"  {addr:04X}: {words[0]:010o} {words[1]:010o} {words[2]:010o} {words[3]:010o}")
        
        print()
    
    def dump_registers(self):
        """Dump CPU and index register state"""
        print("\n Register State:")
        print("-" * 50)
        print(f"  AC:  {self.ac:010o} (octal)")
        print(f"  MQ:  {self.mq:010o} (octal)")
        print(f"  IC:  {self.ic:04X} (hex)")
        print()
        print("  Index Registers:")
        for i in range(7):
            value = self.index_registers.read(i)
            print(f"    XR{i+1}: {value:010o}")
        print()


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='IBM 7094 Miner - RustChain Proof-of-Antiquity',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ibm7094_miner.py              # Run with defaults
  python ibm7094_miner.py -e 5         # Run 5 epochs
  python ibm7094_miner.py --quiet      # Run without verbose output
  python ibm7094_miner.py --dump       # Dump memory after run

Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b
Bounty: #331 - LEGENDARY Tier (200 RTC / $20)
        """
    )
    
    parser.add_argument('-e', '--epochs', type=int, default=10,
                        help='Number of epochs to mine (default: 10)')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Suppress verbose output')
    parser.add_argument('--dump', action='store_true',
                        help='Dump memory and registers after run')
    
    args = parser.parse_args()
    
    # Create miner
    miner = IBM7094Miner(verbose=not args.quiet)
    
    # Initialize
    miner.initialize()
    
    # Run mining simulation
    miner.run(max_epochs=args.epochs)
    
    # Dump state if requested
    if args.dump:
        miner.dump_memory()
        miner.dump_registers()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

