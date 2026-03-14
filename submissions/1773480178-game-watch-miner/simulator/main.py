"""
Game & Watch (1980) RustChain Miner - Python Simulator

This simulator emulates the extreme constraints of the original Game & Watch:
- 260 bytes RAM
- 1,792 bytes ROM
- 4-bit CPU @ ~500kHz
- Segmented LCD display

Since a real miner cannot fit in these constraints, this implements
the "Badge Only" solution - a symbolic mining display.

Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b
"""

import time
import random
import sys
import os

# Handle Windows console encoding
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')  # Set UTF-8 code page
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class LCDSegment(Enum):
    """Represents segments on the Game & Watch LCD"""
    DIGIT_0 = 0
    DIGIT_1 = 1
    DIGIT_2 = 2
    DIGIT_3 = 3
    DIGIT_4 = 4
    DIGIT_5 = 5
    MINING_ICON = 6
    BATTERY_ICON = 7
    CLOCK_ICON = 8
    SCORE_LABEL = 9
    TIME_LABEL = 10


@dataclass
class GameWatchMemory:
    """
    Emulates the 260 bytes of RAM in the Game & Watch.
    This is an EXTREMELY constrained environment.
    """
    RAM_SIZE: int = 260  # bytes
    ROM_SIZE: int = 1792  # bytes
    
    # Memory layout
    ram: bytearray = field(default_factory=lambda: bytearray(260))
    
    # Register emulation (4-bit CPU)
    registers: dict = field(default_factory=lambda: {
        'A': 0,   # Accumulator (4-bit)
        'B': 0,   # B register (4-bit)
        'C': 0,   # C register (4-bit)
        'D': 0,   # D register (4-bit)
        'PC': 0,  # Program counter (11-bit for 2KB ROM)
        'SP': 0,  # Stack pointer
    })
    
    # Display state (which segments are active)
    lcd_segments: set = field(default_factory=set)
    
    # Mining state
    mining_active: bool = False
    rtc_balance: int = 0
    nonce_counter: int = 0
    
    def __post_init__(self):
        # Initialize with boot sequence
        self.boot()
    
    def boot(self):
        """Simulate boot sequence"""
        self.registers['PC'] = 0
        self.registers['A'] = 0
        # Display startup animation
        for i in range(5):
            self.lcd_segments.add(LCDSegment.DIGIT_0)
            self._clear_display()
    
    def _clear_display(self):
        """Clear all LCD segments"""
        self.lcd_segments.clear()
    
    def get_memory_usage(self) -> dict:
        """Report current memory usage"""
        used_ram = sum(1 for byte in self.ram if byte != 0)
        return {
            'ram_used': used_ram,
            'ram_total': self.RAM_SIZE,
            'ram_percent': (used_ram / self.RAM_SIZE) * 100,
            'registers': len([v for v in self.registers.values() if v != 0]),
        }


@dataclass
class SegmentedDisplay:
    """
    Emulates the segmented LCD display of the Game & Watch.
    Each "digit" is a 7-segment display.
    """
    
    # 7-segment patterns for digits 0-9
    SEGMENT_PATTERNS = {
        0: [1, 1, 1, 0, 1, 1, 1],  # _
        1: [0, 0, 1, 0, 0, 1, 0],  # |  right side
        2: [1, 0, 1, 1, 1, 0, 1],
        3: [1, 0, 1, 1, 0, 1, 1],
        4: [0, 1, 1, 1, 0, 1, 0],
        5: [1, 1, 0, 1, 0, 1, 1],
        6: [1, 1, 0, 1, 1, 1, 1],
        7: [1, 0, 1, 0, 0, 1, 0],
        8: [1, 1, 1, 1, 1, 1, 1],
        9: [1, 1, 1, 1, 0, 1, 1],
    }
    
    def render_digit(self, digit: int) -> str:
        """Render a single digit as ASCII art"""
        if digit < 0 or digit > 9:
            return "[?]"
        
        pattern = self.SEGMENT_PATTERNS[digit]
        # Simplified ASCII representation
        return f" {digit} "
    
    def render_display(self, memory: GameWatchMemory) -> str:
        """Render the full LCD display as ASCII art"""
        lines = []
        
        # Top bar
        lines.append("┌─────────────────────────────────┐")
        
        # Time display
        now = datetime.now()
        time_str = f"{now.hour:02d}:{now.minute:02d}"
        lines.append(f"│  TIME: {time_str}                    │")
        
        # Mining status
        status = "⛏️ MINING" if memory.mining_active else "⏸ PAUSED"
        lines.append(f"│  STATUS: {status:22} │")
        
        # RTC Balance (simulated)
        balance = memory.rtc_balance
        lines.append(f"│  BALANCE: {balance} RTC                  │")
        
        # Wallet badge (abbreviated)
        wallet = "RTC4325...bb96b"
        lines.append(f"│  WALLET: {wallet:22} │")
        
        # Nonce counter
        nonce = memory.nonce_counter
        lines.append(f"│  NONCE: {nonce:23} │")
        
        # Memory usage
        mem_usage = memory.get_memory_usage()
        lines.append(f"│  RAM: {mem_usage['ram_used']}/{mem_usage['ram_total']} bytes ({mem_usage['ram_percent']:.1f}%)       │")
        
        # Bottom bar with icons
        battery = "🔋" if True else "🪫"
        lines.append(f"│  {battery}  🎮 GAME & WATCH (1980)           │")
        
        lines.append("└─────────────────────────────────┘")
        
        return "\n".join(lines)


class SharpSM5xxEmulator:
    """
    Emulates the Sharp SM5xx 4-bit microcontroller.
    This is a simplified emulation - real SM5xx has complex instruction set.
    """
    
    def __init__(self, memory: GameWatchMemory):
        self.memory = memory
        self.clock_speed = 500000  # 500 kHz
        self.instructions_executed = 0
    
    def execute_instruction(self, opcode: int):
        """Execute a single instruction (simplified)"""
        # In reality, this would decode and execute SM5xx opcodes
        # For simulation, we just increment counters
        self.instructions_executed += 1
        self.memory.registers['PC'] = (self.memory.registers['PC'] + 1) % self.memory.ROM_SIZE
    
    def run_miner_loop(self, iterations: int = 10):
        """Simulate running the miner main loop"""
        for i in range(iterations):
            # Simulate "mining" work
            self.memory.nonce_counter += 1
            
            # Random chance to "find" a share (simulated)
            if random.random() < 0.1:
                self.memory.rtc_balance += 1
            
            # Execute some "instructions"
            for _ in range(100):
                self.execute_instruction(random.randint(0, 255))
            
            # Yield to allow display update
            time.sleep(0.1)


class GameWatchMiner:
    """Main miner class that ties everything together"""
    
    def __init__(self, wallet_address: str = "RTC4325af95d26d59c3ef025963656d22af638bb96b"):
        self.wallet = wallet_address
        self.memory = GameWatchMemory()
        self.display = SegmentedDisplay()
        self.cpu = SharpSM5xxEmulator(self.memory)
        self.running = False
    
    def start_mining(self):
        """Start the mining simulation"""
        print("🎮 Game & Watch RustChain Miner Starting...")
        print(f"💼 Wallet: {self.wallet}")
        print(f"💾 RAM: {self.memory.RAM_SIZE} bytes")
        print(f"📦 ROM: {self.memory.ROM_SIZE} bytes")
        print(f"⚡ CPU: Sharp SM5xx @ {self.cpu.clock_speed / 1000:.0f}kHz")
        print()
        
        self.memory.mining_active = True
        self.running = True
        
        # Display initial state
        self._render_screen()
        
        print("\n⛏️ Starting mining simulation...\n")
        print("Press Ctrl+C to stop\n")
        
        try:
            iteration = 0
            while self.running:
                # Run miner loop
                self.cpu.run_miner_loop(iterations=5)
                
                # Update display every 10 iterations
                if iteration % 10 == 0:
                    self._render_screen()
                
                iteration += 1
                
        except KeyboardInterrupt:
            print("\n\n⏹ Mining stopped by user")
            self.running = False
            self.memory.mining_active = False
        
        # Final stats
        self._print_stats()
    
    def _render_screen(self):
        """Render the LCD display"""
        # Clear screen (ANSI codes)
        print("\033[2J\033[H", end="")
        print(self.display.render_display(self.memory))
    
    def _print_stats(self):
        """Print final mining statistics"""
        print("\n" + "="*50)
        print("📊 MINING STATISTICS")
        print("="*50)
        print(f"Wallet: {self.wallet}")
        print(f"Total RTC Earned: {self.memory.rtc_balance}")
        print(f"Nonces Attempted: {self.memory.nonce_counter}")
        print(f"Instructions Executed: {self.cpu.instructions_executed:,}")
        print(f"Memory Usage: {self.memory.get_memory_usage()}")
        print("="*50)


def main():
    """Main entry point"""
    print("="*50)
    print("🎮 GAME & WATCH RUSTCHAIN MINER (1980)")
    print("   Badge Only Edition - Proof of Concept")
    print("="*50)
    print()
    
    # Create and start miner
    miner = GameWatchMiner()
    miner.start_mining()


if __name__ == "__main__":
    main()
