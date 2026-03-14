"""
Mining Badge Logic

Implements the "Badge Only" mining solution for Game & Watch.
Since a real miner cannot fit in 260 bytes RAM, this provides
a symbolic representation of mining activity.
"""

from dataclasses import dataclass, field
from typing import Set, Optional
from enum import Enum
import time
import random


class BadgeState(Enum):
    """States for the mining badge display"""
    IDLE = 0
    MINING = 1
    FOUND_SHARE = 2
    ERROR = 3
    LOW_BATTERY = 4


@dataclass
class GameWatchMemory:
    """
    Emulates the 260 bytes of RAM in the Game & Watch.
    
    Memory layout (260 bytes total):
    - 0x00-0x0F: Display state (16 bytes)
    - 0x10-0x1F: Mining state (16 bytes)
    - 0x20-0x2F: Wallet address cache (16 bytes, abbreviated)
    - 0x30-0x3F: Nonce counter (16 bytes)
    - 0x40-0x4F: RTC balance (16 bytes)
    - 0x50-0x5F: Temporary calculation space (16 bytes)
    - 0x60-0xFF: General purpose (160 bytes)
    - 0x100-0x103: Stack (4 bytes for 4-bit CPU)
    
    Total: 260 bytes (0x000-0x103)
    """
    
    RAM_SIZE: int = 260  # bytes - HARD LIMIT!
    ROM_SIZE: int = 1792  # bytes
    
    # Memory arrays
    ram: bytearray = field(default_factory=lambda: bytearray(260))
    rom: bytearray = field(default_factory=lambda: bytearray(1792))
    
    # Display state (which LCD segments are active)
    lcd_segments: Set[int] = field(default_factory=set)
    
    # Mining state variables
    mining_active: bool = False
    rtc_balance: int = 0
    nonce_counter: int = 0
    badge_state: BadgeState = BadgeState.IDLE
    
    # Wallet address (stored in ROM, not RAM)
    wallet_address: str = "RTC4325af95d26d59c3ef025963656d22af638bb96b"
    
    # Statistics
    shares_found: int = 0
    mining_time_seconds: float = 0.0
    
    def __post_init__(self):
        """Initialize memory after dataclass creation"""
        self.boot()
    
    def boot(self):
        """
        Execute boot sequence.
        
        On real hardware, this would:
        1. Initialize RAM (clear to 0)
        2. Set up LCD driver
        3. Display startup animation
        4. Jump to main loop
        """
        # Clear RAM
        for i in range(self.RAM_SIZE):
            self.ram[i] = 0
        
        # Initialize display
        self.lcd_segments.clear()
        
        # Load boot program into ROM (simulated)
        self._load_boot_rom()
        
        # Set initial state
        self.badge_state = BadgeState.IDLE
    
    def _load_boot_rom(self):
        """Load boot sequence into ROM"""
        # Simplified boot sequence (opcodes)
        boot_code = [
            0x0B,  # LCD_ON
            0x01,  # LOAD
            0x00,  # (operand)
            0x0D,  # SEG_SET (display startup)
            0x00,  # NOP
            0x0F,  # HALT (end of boot, jump to main in real code)
        ]
        
        for i, opcode in enumerate(boot_code):
            if i < self.ROM_SIZE:
                self.rom[i] = opcode
    
    def get_memory_usage(self) -> dict:
        """
        Report current memory usage.
        
        Returns:
            dict with RAM/ROM usage statistics
        """
        ram_used = sum(1 for byte in self.ram if byte != 0)
        rom_used = sum(1 for byte in self.rom if byte != 0)
        
        return {
            'ram_used': ram_used,
            'ram_total': self.RAM_SIZE,
            'ram_percent': (ram_used / self.RAM_SIZE) * 100,
            'rom_used': rom_used,
            'rom_total': self.ROM_SIZE,
            'rom_percent': (rom_used / self.ROM_SIZE) * 100,
        }
    
    def write_ram(self, address: int, value: int):
        """Write a byte to RAM with bounds checking"""
        if 0 <= address < self.RAM_SIZE:
            self.ram[address] = value & 0xFF
    
    def read_ram(self, address: int) -> int:
        """Read a byte from RAM with bounds checking"""
        if 0 <= address < self.RAM_SIZE:
            return self.ram[address]
        return 0
    
    def update_display(self, segments: Set[int]):
        """Update LCD segment display"""
        self.lcd_segments = segments.copy()
    
    def increment_nonce(self) -> int:
        """Increment nonce counter and return new value"""
        self.nonce_counter = (self.nonce_counter + 1) & 0xFFFFFFFF
        return self.nonce_counter
    
    def add_rtc(self, amount: int = 1):
        """Add RTC to balance"""
        self.rtc_balance += amount
        self.shares_found += 1
    
    def set_badge_state(self, state: BadgeState):
        """Update badge display state"""
        self.badge_state = state
        
        # Update LCD segments based on state
        self.lcd_segments.clear()
        
        if state == BadgeState.MINING:
            # Add mining icon segments
            self.lcd_segments.update(range(100, 110))
        elif state == BadgeState.FOUND_SHARE:
            # Flash all segments briefly
            self.lcd_segments.update(range(0, 50))
        elif state == BadgeState.LOW_BATTERY:
            # Battery warning segments
            self.lcd_segments.update(range(200, 210))
    
    def get_status_report(self) -> str:
        """Generate human-readable status report"""
        mem_usage = self.get_memory_usage()
        
        report = [
            "[GAME & WATCH] Miner Status",
            "=" * 40,
            f"Wallet: {self.wallet_address}",
            f"Badge State: {self.badge_state.name}",
            f"RTC Balance: {self.rtc_balance} RTC",
            f"Shares Found: {self.shares_found}",
            f"Nonce: {self.nonce_counter}",
            f"Mining Time: {self.mining_time_seconds:.1f}s",
            "",
            "Memory Usage:",
            f"  RAM: {mem_usage['ram_used']}/{mem_usage['ram_total']} bytes ({mem_usage['ram_percent']:.1f}%)",
            f"  ROM: {mem_usage['rom_used']}/{mem_usage['rom_total']} bytes ({mem_usage['rom_percent']:.1f}%)",
            "",
            "[WARNING] EXTREME CONSTRAINTS:",
            f"  - Only {self.RAM_SIZE} bytes RAM (vs 512MB+ on modern systems)",
            f"  - 4-bit CPU @ 500kHz (vs 64-bit @ 3GHz+)",
            f"  - Segmented LCD (vs full graphics)",
            "",
            "This demonstrates why 'Badge Only' approach is necessary!",
        ]
        
        return "\n".join(report)


@dataclass
class MiningBadge:
    """
    Manages the mining badge display and logic.
    
    The badge is a symbolic representation of mining activity
    that fits within the Game & Watch's extreme constraints.
    """
    
    memory: GameWatchMemory
    animation_frame: int = 0
    last_update: float = 0.0
    
    def start_mining(self):
        """Start the mining badge animation"""
        self.memory.mining_active = True
        self.memory.set_badge_state(BadgeState.MINING)
    
    def stop_mining(self):
        """Stop mining and return to idle"""
        self.memory.mining_active = False
        self.memory.set_badge_state(BadgeState.IDLE)
    
    def update(self, current_time: float):
        """
        Update badge animation.
        
        Args:
            current_time: Current timestamp in seconds
        """
        # Limit update rate to save CPU cycles
        if current_time - self.last_update < 0.1:  # 10 FPS max
            return
        
        self.last_update = current_time
        self.animation_frame = (self.animation_frame + 1) % 4
        
        # Animate mining icon
        if self.memory.mining_active:
            # Simulate "mining" animation by toggling segments
            if self.animation_frame % 2 == 0:
                self.memory.lcd_segments.add(100)
            else:
                self.memory.lcd_segments.discard(100)
            
            # Update mining time
            self.memory.mining_time_seconds += 0.1
            
            # Simulate finding a share (1% chance per update)
            if random.random() < 0.01:
                self.found_share()
    
    def found_share(self):
        """Handle finding a mining share"""
        self.memory.add_rtc(1)
        self.memory.set_badge_state(BadgeState.FOUND_SHARE)
        
        # Brief celebration animation
        time.sleep(0.1)
        
        # Return to mining state
        self.memory.set_badge_state(BadgeState.MINING)
    
    def render_text(self) -> str:
        """Render badge as text for terminal display"""
        status_icon = {
            BadgeState.IDLE: "⏸",
            BadgeState.MINING: "⛏️",
            BadgeState.FOUND_SHARE: "✨",
            BadgeState.ERROR: "❌",
            BadgeState.LOW_BATTERY: "🪫",
        }.get(self.memory.badge_state, "?")
        
        lines = [
            f"{status_icon} Game & Watch Miner",
            f"   Balance: {self.memory.rtc_balance} RTC",
            f"   Nonce: {self.memory.nonce_counter}",
            f"   RAM: {self.memory.get_memory_usage()['ram_used']}/{self.memory.RAM_SIZE} bytes",
        ]
        
        return "\n".join(lines)
    
    def get_wallet_address(self) -> str:
        """Get the wallet address for this badge"""
        return self.memory.wallet_address
