"""
Sharp SM5xx CPU Emulator

Emulates the 4-bit microcontroller used in the original Game & Watch.
The SM5xx series was a mask-programmed ROM microcontroller with
integrated LCD drive circuitry.

Key specs:
- 4-bit CPU
- ~500 kHz clock speed
- 260 bytes RAM
- 1-2 KB ROM (mask programmed)
- Integrated LCD driver
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import time
import random


class SM5xxRegister(Enum):
    """SM5xx CPU registers"""
    A = 0    # Accumulator (4-bit)
    B = 1    # B register (4-bit)
    C = 2    # C register (4-bit)
    D = 3    # D register (4-bit)
    PC = 4   # Program counter (11-bit)
    SP = 5   # Stack pointer (8-bit)


@dataclass
class SM5xxInstruction:
    """Represents a single SM5xx instruction"""
    opcode: int
    name: str
    operands: List[int] = field(default_factory=list)
    cycles: int = 1


class SharpSM5xxEmulator:
    """
    Emulates the Sharp SM5xx 4-bit microcontroller.
    
    This is a simplified emulation for the mining badge simulation.
    A full SM5xx emulator would implement the complete instruction set.
    """
    
    # Instruction set (simplified subset)
    INSTRUCTIONS = {
        0x00: "NOP",    # No operation
        0x01: "LOAD",   # Load accumulator
        0x02: "STORE",  # Store accumulator
        0x03: "ADD",    # Add to accumulator
        0x04: "SUB",    # Subtract from accumulator
        0x05: "INC",    # Increment
        0x06: "DEC",    # Decrement
        0x07: "JMP",    # Jump
        0x08: "JZ",     # Jump if zero
        0x09: "CALL",   # Call subroutine
        0x0A: "RET",    # Return
        0x0B: "LCD_ON", # Turn on LCD driver
        0x0C: "LCD_OFF",# Turn off LCD driver
        0x0D: "SEG_SET",# Set segment
        0x0E: "SEG_CLR",# Clear segment
        0x0F: "HALT",   # Halt CPU
    }
    
    def __init__(self, memory: 'GameWatchMemory'):
        """
        Initialize the SM5xx emulator.
        
        Args:
            memory: GameWatchMemory instance to operate on
        """
        self.memory = memory
        self.clock_speed = 500000  # 500 kHz
        self.instructions_executed = 0
        self.halted = False
        self.lcd_enabled = False
        
        # Initialize registers
        self.registers: Dict[SM5xxRegister, int] = {
            SM5xxRegister.A: 0,   # 4-bit accumulator
            SM5xxRegister.B: 0,   # 4-bit B register
            SM5xxRegister.C: 0,   # 4-bit C register
            SM5xxRegister.D: 0,   # 4-bit D register
            SM5xxRegister.PC: 0,  # 11-bit program counter
            SM5xxRegister.SP: 0,  # 8-bit stack pointer
        }
        
        # Stack (for subroutine calls)
        self.stack: List[int] = []
    
    def fetch(self) -> int:
        """Fetch instruction from ROM at PC"""
        # In real hardware, this reads from mask ROM
        # For simulation, we read from memory.ROM area
        if self.registers[SM5xxRegister.PC] < len(self.memory.rom):
            opcode = self.memory.rom[self.registers[SM5xxRegister.PC]]
        else:
            opcode = 0x00  # NOP if past ROM end
        
        # Increment PC (wrap at ROM size)
        self.registers[SM5xxRegister.PC] = (self.registers[SM5xxRegister.PC] + 1) % self.memory.ROM_SIZE
        
        return opcode
    
    def decode(self, opcode: int) -> SM5xxInstruction:
        """Decode opcode into instruction"""
        name = self.INSTRUCTIONS.get(opcode, "UNKNOWN")
        return SM5xxInstruction(opcode=opcode, name=name)
    
    def execute(self, instruction: SM5xxInstruction):
        """Execute a decoded instruction"""
        self.instructions_executed += 1
        
        op = instruction.opcode
        
        if op == 0x00:  # NOP
            pass
        elif op == 0x01:  # LOAD
            self.registers[SM5xxRegister.A] = random.randint(0, 15)
        elif op == 0x05:  # INC
            self.registers[SM5xxRegister.A] = (self.registers[SM5xxRegister.A] + 1) & 0x0F
        elif op == 0x06:  # DEC
            self.registers[SM5xxRegister.A] = (self.registers[SM5xxRegister.A] - 1) & 0x0F
        elif op == 0x0B:  # LCD_ON
            self.lcd_enabled = True
        elif op == 0x0C:  # LCD_OFF
            self.lcd_enabled = False
        elif op == 0x0F:  # HALT
            self.halted = True
        # Other instructions simplified for simulation
    
    def step(self) -> bool:
        """
        Execute one instruction cycle.
        
        Returns:
            True if CPU is still running, False if halted
        """
        if self.halted:
            return False
        
        opcode = self.fetch()
        instruction = self.decode(opcode)
        self.execute(instruction)
        
        return not self.halted
    
    def run_cycles(self, cycles: int):
        """Run specified number of instruction cycles"""
        for _ in range(cycles):
            if not self.step():
                break
    
    def run_miner_loop(self, iterations: int = 10):
        """
        Simulate running the miner main loop.
        
        This emulates what a mining loop would look like on the SM5xx:
        1. Increment nonce counter
        2. Update display
        3. Check for "share found" (simulated)
        4. Repeat
        """
        for i in range(iterations):
            if self.halted:
                break
            
            # Simulate mining work
            # Increment nonce (stored in RAM)
            self.memory.nonce_counter = (self.memory.nonce_counter + 1) & 0xFFFF
            
            # Execute some instructions to simulate work
            self.run_cycles(100)
            
            # Random chance to "find" a share (simulated mining reward)
            if random.random() < 0.1:
                self.memory.rtc_balance += 1
                # Flash display to indicate success
                self.memory.lcd_enabled = not self.memory.lcd_enabled
            
            # Small delay to simulate real clock speed
            # At 500kHz, 100 cycles = 0.2ms
            time.sleep(0.0002)
    
    def get_status(self) -> dict:
        """Get current CPU status"""
        return {
            'pc': self.registers[SM5xxRegister.PC],
            'accumulator': self.registers[SM5xxRegister.A],
            'instructions_executed': self.instructions_executed,
            'halted': self.halted,
            'lcd_enabled': self.lcd_enabled,
            'clock_speed_hz': self.clock_speed,
        }
    
    def reset(self):
        """Reset CPU to initial state"""
        self.registers[SM5xxRegister.PC] = 0
        self.registers[SM5xxRegister.A] = 0
        self.registers[SM5xxRegister.B] = 0
        self.registers[SM5xxRegister.C] = 0
        self.registers[SM5xxRegister.D] = 0
        self.registers[SM5xxRegister.SP] = 0
        self.instructions_executed = 0
        self.halted = False
        self.lcd_enabled = False
        self.stack.clear()
