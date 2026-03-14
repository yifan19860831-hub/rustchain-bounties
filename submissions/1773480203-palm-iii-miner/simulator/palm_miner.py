#!/usr/bin/env python3
"""
RustChain Palm III Miner Simulator
"DragonBall Edition" - Python simulation of Palm III mining

This simulator emulates:
- Motorola DragonBall EZ @ 16 MHz behavior
- Palm OS 3.5 event loop
- 160x160 text display
- Entropy collection from virtual hardware
- Attestation storage

Bounty Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b
"""

import os
import sys
import time
import random
import hashlib
import json
from datetime import datetime
from typing import Optional, Dict, List

# Constants
DRAGONBALL_FREQ = 16_000_000  # 16 MHz
DISPLAY_WIDTH = 160
DISPLAY_HEIGHT = 160
WALLET_SIZE = 48
ENTROPY_SIZE = 64
ATTEST_INTERVAL = 600  # 10 minutes
DEV_FEE = "0.001"
DEV_WALLET = "founder_dev_fund"

class DragonBallEmulator:
    """Emulates Motorola DragonBall EZ hardware registers"""
    
    def __init__(self):
        self.rtc_seconds = 0
        self.rtc_minutes = 0
        self.rtc_hours = 0
        self.timer_ticks = 0
        self.ram_pattern = bytes([random.randint(0, 255) for _ in range(256)])
        
    def get_rtc_time(self) -> tuple:
        """Get current RTC time"""
        now = datetime.now()
        return (now.second, now.minute, now.hour)
    
    def get_timer_tick(self) -> int:
        """Get current timer tick (simulated jitter)"""
        return int(time.time() * 1000) & 0xFFFFFFFF
    
    def get_ram_pattern(self, offset: int = 0, length: int = 16) -> bytes:
        """Get RAM power-on pattern (simulated entropy)"""
        return self.ram_pattern[offset:offset+length]
    
    def collect_entropy(self) -> bytes:
        """Collect entropy from DragonBall hardware"""
        entropy = bytearray(ENTROPY_SIZE)
        
        # 1. RTC registers
        sec, min, hour = self.get_rtc_time()
        entropy[0] = sec & 0xFF
        entropy[1] = min & 0xFF
        entropy[2] = hour & 0xFF
        
        # 2. Timer tick jitter (multiple samples)
        for i in range(16):
            tick = self.get_timer_tick()
            entropy[3 + i] = (tick >> (i % 4) * 8) & 0xFF
            time.sleep(0.001)  # Small delay for jitter
        
        # 3. RAM pattern
        ram = self.get_ram_pattern()
        entropy[19:35] = ram
        
        # 4. System info simulation
        entropy[35] = 0x03  # Palm OS 3.x
        entropy[36] = 0x50  # 'P'
        entropy[37] = 0x61  # 'a'
        
        # 5. Fill rest with hash-based expansion
        seed = hashlib.sha256(entropy[:38]).digest()
        for i in range(38, ENTROPY_SIZE):
            entropy[i] = seed[i % 32] ^ (i * 7) & 0xFF
        
        return bytes(entropy)


class PalmOSDisplay:
    """Emulates Palm III 160x160 grayscale display"""
    
    GRAY_LEVELS = [' ', '░', '▒', '▓', '█']
    
    def __init__(self):
        self.width = DISPLAY_WIDTH
        self.height = DISPLAY_HEIGHT
        self.buffer = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        self.contrast = 2  # 0-4
        
    def clear(self):
        """Clear display"""
        self.buffer = [[' ' for _ in range(self.width)] for _ in range(self.height)]
    
    def draw_text(self, x: int, y: int, text: str, invert: bool = False):
        """Draw text at position"""
        if y >= self.height:
            return
        for i, char in enumerate(text[:self.width - x]):
            if x + i < self.width:
                self.buffer[y][x + i] = char
    
    def draw_box(self, x1: int, y1: int, x2: int, y2: int):
        """Draw rectangular box"""
        for x in range(x1, x2 + 1):
            self.buffer[y1][x] = '─'
            self.buffer[y2][x] = '─'
        for y in range(y1, y2 + 1):
            self.buffer[y][x1] = '│'
            self.buffer[y][x2] = '│'
        self.buffer[y1][x1] = '┌'
        self.buffer[y1][x2] = '┐'
        self.buffer[y2][x1] = '└'
        self.buffer[y2][x2] = '┘'
    
    def render(self) -> str:
        """Render display to text (8 rows visible)"""
        lines = []
        for y in range(0, min(64, self.height), 8):  # Show 8 text rows
            line = ''.join(self.buffer[y])
            lines.append(line.rstrip())
        return '\n'.join(lines)


class AttestationDB:
    """Palm OS Database for storing attestations"""
    
    def __init__(self, db_path: str = "palm_attestations.db"):
        self.db_path = db_path
        self.attestations: List[Dict] = []
        self.load()
    
    def load(self):
        """Load attestations from file"""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r') as f:
                    self.attestations = json.load(f)
            except:
                self.attestations = []
    
    def save(self):
        """Save attestations to file"""
        with open(self.db_path, 'w') as f:
            json.dump(self.attestations, f, indent=2)
    
    def add_attestation(self, entropy: bytes, timestamp: float) -> Dict:
        """Add new attestation"""
        attest = {
            'timestamp': timestamp,
            'datetime': datetime.now().isoformat(),
            'entropy_hash': hashlib.sha256(entropy).hexdigest()[:16],
            'device': 'Palm III',
            'cpu': 'DragonBall EZ 16MHz',
            'os': 'Palm OS 3.5'
        }
        self.attestations.append(attest)
        self.save()
        return attest


class PalmMiner:
    """Main Palm III Miner Application"""
    
    def __init__(self):
        self.dragonball = DragonBallEmulator()
        self.display = PalmOSDisplay()
        self.db = AttestationDB()
        
        self.wallet_id: Optional[str] = None
        self.mining = False
        self.last_attest = 0
        self.attest_count = 0
        
        self.load_wallet()
    
    def load_wallet(self):
        """Load or generate wallet"""
        wallet_file = "palm_wallet.json"
        if os.path.exists(wallet_file):
            with open(wallet_file, 'r') as f:
                data = json.load(f)
                self.wallet_id = data.get('wallet_id')
                print(f"[OK] Loaded wallet: {self.wallet_id}")
        else:
            self.generate_wallet()
    
    def generate_wallet(self):
        """Generate new wallet from entropy"""
        print("Generating wallet from DragonBall entropy...")
        entropy = self.dragonball.collect_entropy()
        
        # Generate wallet ID (RTC prefix + hash)
        hash_bytes = hashlib.sha256(entropy).digest()
        hex_chars = "0123456789ABCDEF"
        wallet = "RTC"
        for byte in hash_bytes[:20]:
            wallet += hex_chars[byte & 0x0F]
            wallet += hex_chars[(byte >> 4) & 0x0F]
        
        self.wallet_id = wallet
        
        # Save wallet
        with open("palm_wallet.json", 'w') as f:
            json.dump({
                'wallet_id': self.wallet_id,
                'created': datetime.now().isoformat(),
                'device': 'Palm III Simulator',
                'entropy_hash': hashlib.sha256(entropy).hexdigest()
            }, f, indent=2)
        
        print(f"[OK] Wallet generated: {self.wallet_id}")
        print("[WARN] BACKUP THIS WALLET!")
    
    def draw_main_screen(self):
        """Draw main mining screen"""
        self.display.clear()
        
        # Box
        self.display.draw_box(0, 0, 159, 63)
        
        # Title
        self.display.draw_text(20, 2, "RustChain Miner")
        self.display.draw_text(18, 4, "Palm III Edition")
        
        # Info
        if self.wallet_id:
            wallet_short = self.wallet_id[:12] + "..."
            self.display.draw_text(2, 10, f"Wallet: {wallet_short}")
        
        self.display.draw_text(2, 14, f"Attestations: {self.attest_count}")
        
        status = "Mining..." if self.mining else "Stopped"
        self.display.draw_text(2, 18, f"Status: {status}")
        
        # Buttons (text representation)
        btn_text = "[Stop]" if self.mining else "[Mine]"
        self.display.draw_text(2, 24, f"{btn_text} [Status] [Wallet] [Exit]")
    
    def mine_step(self):
        """One step of mining loop"""
        now = time.time()
        
        if self.mining and (now - self.last_attest) >= ATTEST_INTERVAL:
            print(f"\n[ALARM] Creating attestation #{self.attest_count + 1}")
            entropy = self.dragonball.collect_entropy()
            attest = self.db.add_attestation(entropy, now)
            self.attest_count += 1
            self.last_attest = now
            print(f"   Hash: {attest['entropy_hash']}")
            print(f"   Time: {attest['datetime']}")
    
    def run_ui_loop(self):
        """Run text-based UI loop"""
        print("\n" + "="*60)
        print("RustChain Palm III Miner Simulator")
        print("DragonBall EZ @ 16 MHz Emulation")
        print("="*60)
        print("\nControls:")
        print("  m - Toggle mining")
        print("  s - Show status")
        print("  w - Show wallet")
        print("  d - Show display")
        print("  q - Quit")
        print("="*60)
        
        try:
            while True:
                self.draw_main_screen()
                
                cmd = input("\nCommand> ").strip().lower()
                
                if cmd == 'q':
                    print("Exiting...")
                    break
                elif cmd == 'm':
                    self.mining = not self.mining
                    print(f"Mining: {'ON' if self.mining else 'OFF'}")
                    self.mine_step()
                elif cmd == 's':
                    print(f"\n=== Status ===")
                    print(f"Wallet: {self.wallet_id}")
                    print(f"Attestations: {self.attest_count}")
                    print(f"Mining: {self.mining}")
                    print(f"Last attest: {datetime.fromtimestamp(self.last_attest) if self.last_attest else 'Never'}")
                elif cmd == 'w':
                    print(f"\n=== Wallet ===")
                    print(f"ID: {self.wallet_id}")
                    print(f"Device: Palm III (DragonBall EZ)")
                    print(f"Antiquity Multiplier: 3.5x")
                elif cmd == 'd':
                    print("\n=== Display ===")
                    print(self.display.render())
                else:
                    print("Unknown command. Try: m, s, w, d, q")
                
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\nInterrupted")
    
    def run_background(self, duration: int = 3600):
        """Run mining in background for specified duration"""
        print(f"Starting background mining for {duration} seconds...")
        self.mining = True
        start = time.time()
        
        try:
            while (time.time() - start) < duration:
                self.mine_step()
                time.sleep(10)  # Check every 10 seconds
                print(f".", end='', flush=True)
        except KeyboardInterrupt:
            pass
        
        self.mining = False
        print(f"\n[STOP] Mining stopped. Total attestations: {self.attest_count}")


def main():
    """Main entry point"""
    miner = PalmMiner()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == '--background':
            duration = int(sys.argv[2]) if len(sys.argv) > 2 else 3600
            miner.run_background(duration)
        elif cmd == '--generate':
            miner.generate_wallet()
        elif cmd == '--status':
            print(f"Wallet: {miner.wallet_id}")
            print(f"Attestations: {miner.attest_count}")
        else:
            print(f"Unknown command: {cmd}")
    else:
        miner.run_ui_loop()


if __name__ == "__main__":
    main()
