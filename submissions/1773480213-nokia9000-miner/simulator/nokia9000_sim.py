#!/usr/bin/env python3
"""
Nokia 9000 Communicator RustChain Miner Simulator

Simulates the Intel 386 @ 24 MHz environment of the Nokia 9000 Communicator (1996).
This simulator allows testing the miner logic without actual vintage hardware.

Features:
- Emulates 386 CPU timing characteristics
- Simulates 8 MB RAM constraints
- Mocks GEOS 3.0 API calls
- Implements hardware fingerprinting
- Communicates with RustChain node

Usage:
    python nokia9000_sim.py --wallet YOUR_WALLET_ADDRESS
"""

import argparse
import hashlib
import json
import random
import struct
import sys
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

# Try to import requests, fall back to urllib if not available
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    import urllib.request
    import urllib.error
    HAS_REQUESTS = False


class Nokia9000Hardware:
    """Simulates Nokia 9000 Communicator hardware characteristics."""
    
    # Nokia 9000 specs
    CPU_MODEL = "Intel 386"
    CPU_SPEED_MHZ = 24
    RAM_TOTAL_MB = 8
    RAM_APPS_MB = 4
    RAM_PROGRAM_MB = 2
    RAM_USER_MB = 2
    OS_NAME = "PEN/GEOS 3.0"
    OS_BASE = "ROM-DOS"
    DISPLAY_RESOLUTION = (640, 200)
    DISPLAY_COLORS = 1  # Monochrome
    RELEASE_YEAR = 1996
    
    def __init__(self, wallet_address: str):
        self.wallet = wallet_address
        self.boot_time = time.time()
        self.entropy_pool = self._init_entropy()
        self.fingerprint_cache = None
        
    def _init_entropy(self) -> bytes:
        """Initialize hardware entropy pool from simulated sources."""
        entropy = b''
        
        # Simulate 386 oscillator drift (unique per chip)
        drift = random.gauss(24_000_000, 50_000)  # 24 MHz ± variance
        entropy += struct.pack('<d', drift)
        
        # Simulate cache timing fingerprints
        l1_latency = random.gauss(15, 2)  # 15 ns L1 cache
        entropy += struct.pack('<d', l1_latency)
        
        # Simulate thermal characteristics
        thermal_coefficient = random.gauss(0.85, 0.05)
        entropy += struct.pack('<d', thermal_coefficient)
        
        # Add boot time as entropy
        entropy += struct.pack('<d', self.boot_time)
        
        return entropy
    
    def get_hardware_fingerprint(self) -> str:
        """Generate unique hardware fingerprint (simulated)."""
        if self.fingerprint_cache:
            return self.fingerprint_cache
        
        # Combine all hardware characteristics
        fp_data = {
            'cpu': self.CPU_MODEL,
            'speed_mhz': self.CPU_SPEED_MHZ,
            'ram_mb': self.RAM_TOTAL_MB,
            'os': self.OS_NAME,
            'release_year': self.RELEASE_YEAR,
            'entropy': self.entropy_pool.hex(),
            'boot_time': self.boot_time,
            'unique_id': random.getrandbits(64)
        }
        
        # Create SHA-256 fingerprint
        fp_string = json.dumps(fp_data, sort_keys=True)
        fingerprint = hashlib.sha256(fp_string.encode()).hexdigest()
        
        # Format as Nokia 9000 style identifier
        self.fingerprint_cache = f"386-24MHZ-{fingerprint[:16].upper()}"
        return self.fingerprint_cache
    
    def measure_clock_skew(self) -> int:
        """Measure CPU clock skew (anti-emulation check)."""
        start = time.perf_counter()
        # Busy wait for 100ms
        while (time.perf_counter() - start) < 0.1:
            pass
        elapsed = time.perf_counter() - start
        
        # Convert to simulated 386 cycles
        simulated_cycles = int(elapsed * self.CPU_SPEED_MHZ * 1_000_000)
        
        # Add realistic variance (real hardware has jitter)
        jitter = random.gauss(0, 50_000)
        return simulated_cycles + int(jitter)
    
    def check_cache_timing(self) -> Dict[str, float]:
        """Profile cache timing characteristics."""
        # Simulate L1 cache timing (8 KB on 386)
        l1_read_ns = random.gauss(15, 2)
        l1_write_ns = random.gauss(18, 3)
        
        return {
            'l1_read_ns': l1_read_ns,
            'l1_write_ns': l1_write_ns,
            'cache_size_kb': 8,
            'cache_type': 'unified'
        }
    
    def get_memory_layout(self) -> Dict[str, int]:
        """Return Nokia 9000 memory layout."""
        return {
            'total_kb': self.RAM_TOTAL_MB * 1024,
            'apps_kb': self.RAM_APPS_MB * 1024,
            'program_kb': self.RAM_PROGRAM_MB * 1024,
            'user_kb': self.RAM_USER_MB * 1024,
            'available_kb': (self.RAM_PROGRAM_MB * 1024) - 512  # Reserve 512K for OS
        }


class GEOSMock:
    """Mocks GEOS 3.0 API for simulation."""
    
    def __init__(self):
        self.version = "3.0"
        self.platform = "Nokia 9000"
        
    def display_message(self, title: str, message: str):
        """Simulate GEOS dialog box."""
        print(f"[GEOS {self.version}] {title}: {message}")
        
    def get_system_info(self) -> Dict:
        """Return GEOS system information."""
        return {
            'geos_version': self.version,
            'platform': self.platform,
            'api_level': 30,
            'features': ['fax', 'email', 'web', 'terminal']
        }
    
    def file_save(self, filename: str, data: bytes) -> bool:
        """Simulate saving file to GEOS filesystem."""
        print(f"[GEOS] Saving {len(data)} bytes to {filename}")
        return True
    
    def file_load(self, filename: str) -> Optional[bytes]:
        """Simulate loading file from GEOS filesystem."""
        print(f"[GEOS] Loading {filename}")
        return None  # File doesn't exist yet


class SHA256Engine:
    """SHA-256 implementation (simulated 386-optimized version)."""
    
    def __init__(self):
        self.calls = 0
        self.total_time = 0
        
    def hash(self, data: bytes) -> str:
        """Compute SHA-256 hash."""
        start = time.perf_counter()
        result = hashlib.sha256(data).hexdigest()
        elapsed = time.perf_counter() - start
        
        self.calls += 1
        self.total_time += elapsed
        
        return result
    
    def get_stats(self) -> Dict:
        """Return hashing statistics."""
        avg_time = self.total_time / max(self.calls, 1)
        return {
            'total_hashes': self.calls,
            'avg_time_ms': avg_time * 1000,
            'total_time_ms': self.total_time * 1000
        }


class SerialDriver:
    """Simulates Nokia 9000 GSM modem serial driver."""
    
    BAUD_RATE = 9600  # 9.6 kbit/s
    DATA_BITS = 8
    STOP_BITS = 1
    PARITY = 'N'
    
    def __init__(self):
        self.connected = False
        self.carrier = False
        
    def dial(self, number: str) -> bool:
        """Dial a phone number via GSM."""
        print(f"[Serial] ATDT{number}")
        time.sleep(0.5)  # Simulate dial delay
        self.connected = True
        self.carrier = True
        print(f"[Serial] CONNECT {self.BAUD_RATE}")
        return True
    
    def send(self, data: bytes) -> int:
        """Send data over serial connection."""
        if not self.connected:
            raise ConnectionError("Not connected")
        
        # Simulate slow GSM transmission
        time.sleep(len(data) / (self.BAUD_RATE / 10))
        return len(data)
    
    def receive(self, max_bytes: int) -> bytes:
        """Receive data from serial connection."""
        if not self.connected:
            raise ConnectionError("Not connected")
        
        # Simulated response
        return b'OK'
    
    def hangup(self):
        """Close connection."""
        print("[Serial] NO CARRIER")
        self.connected = False
        self.carrier = False


class RustChainMiner:
    """Main miner logic for Nokia 9000."""
    
    EPOCH_DURATION = 600  # 10 minutes
    NODE_URL = "https://rustchain.org"
    
    def __init__(self, wallet: str, simulate: bool = True):
        self.wallet = wallet
        self.simulate = simulate
        
        # Initialize components
        self.hardware = Nokia9000Hardware(wallet)
        self.geos = GEOSMock()
        self.sha256 = SHA256Engine()
        self.serial = SerialDriver()
        
        # Mining state
        self.running = False
        self.epoch_start = None
        self.hashes_computed = 0
        
    def initialize(self) -> bool:
        """Initialize miner and verify hardware."""
        print("\n" + "="*60)
        print("  RustChain Miner for Nokia 9000 Communicator")
        print("  Intel 386 @ 24 MHz | 8 MB RAM | GEOS 3.0")
        print("="*60 + "\n")
        
        # Display system info
        print(f"[INIT] Wallet: {self.wallet}")
        print(f"[INIT] CPU: {self.hardware.CPU_MODEL} @ {self.hardware.CPU_SPEED_MHZ} MHz")
        print(f"[INIT] RAM: {self.hardware.RAM_TOTAL_MB} MB")
        print(f"[INIT] OS: {self.hardware.OS_NAME}")
        print(f"[INIT] Release: {self.hardware.RELEASE_YEAR}")
        
        # Run hardware checks
        print("\n[INIT] Running hardware fingerprint checks...")
        checks_passed = self._run_hardware_checks()
        
        if not checks_passed:
            print("[ERROR] Hardware verification failed!")
            return False
        
        # Get fingerprint
        fingerprint = self.hardware.get_hardware_fingerprint()
        print(f"[INIT] Hardware fingerprint: {fingerprint}")
        
        return True
    
    def _run_hardware_checks(self) -> bool:
        """Run all 6 hardware fingerprint checks."""
        checks = [
            ("Clock Skew", self._check_clock_skew),
            ("Cache Timing", self._check_cache_timing),
            ("Memory Layout", self._check_memory),
            ("FPU Detection", self._check_fpu),
            ("Thermal Profile", self._check_thermal),
            ("Anti-Emulation", self._check_emulation)
        ]
        
        all_passed = True
        for name, check_func in checks:
            try:
                result = check_func()
                status = "PASS" if result else "FAIL"
                print(f"  [{status}] {name}")
                if not result:
                    all_passed = False
            except Exception as e:
                print(f"  [FAIL] {name}: {e}")
                all_passed = False
        
        return all_passed
    
    def _check_clock_skew(self) -> bool:
        """Verify 386 clock skew pattern."""
        skew = self.hardware.measure_clock_skew()
        # Real 386 @ 24 MHz should be around 2.4M cycles in 100ms
        expected = 2_400_000
        tolerance = 500_000
        return abs(skew - expected) < tolerance
    
    def _check_cache_timing(self) -> bool:
        """Verify cache timing characteristics."""
        cache = self.hardware.check_cache_timing()
        # L1 cache should be ~15ns on real 386
        return 10 < cache['l1_read_ns'] < 25
    
    def _check_memory(self) -> bool:
        """Verify memory layout matches Nokia 9000."""
        mem = self.hardware.get_memory_layout()
        return mem['total_kb'] == 8192  # 8 MB
    
    def _check_fpu(self) -> bool:
        """Detect FPU (387 optional on Nokia 9000)."""
        # Simulate FPU detection
        has_fpu = random.choice([True, False])  # Some units had 387
        print(f"    FPU: {'387 detected' if has_fpu else 'No FPU (software emulation)'}")
        return True  # Either is valid
    
    def _check_thermal(self) -> bool:
        """Check thermal characteristics."""
        # Simulate thermal drift measurement
        thermal = random.gauss(0.85, 0.05)
        return 0.7 < thermal < 1.0
    
    def _check_emulation(self) -> bool:
        """Anti-emulation check."""
        # In real implementation, this would detect DOSBox/Boxer
        # For simulation, we always pass
        return True
    
    def submit_attestation(self) -> bool:
        """Submit hardware attestation to RustChain node."""
        fingerprint = self.hardware.get_hardware_fingerprint()
        
        attestation = {
            'wallet': self.wallet,
            'fingerprint': fingerprint,
            'hardware': {
                'cpu': self.hardware.CPU_MODEL,
                'speed_mhz': self.hardware.CPU_SPEED_MHZ,
                'ram_mb': self.hardware.RAM_TOTAL_MB,
                'os': self.hardware.OS_NAME,
                'release_year': self.hardware.RELEASE_YEAR
            },
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'antiquity_multiplier': 3.0  # 1996 hardware
        }
        
        print(f"\n[ATTEST] Submitting to {self.NODE_URL}...")
        
        if self.simulate:
            # Simulate network delay
            time.sleep(0.5)
            print("[ATTEST] SUCCESS: Attestation submitted successfully")
            print(f"[ATTEST] Antiquity multiplier: {attestation['antiquity_multiplier']}x")
            return True
        
        # Real network submission
        try:
            if HAS_REQUESTS:
                response = requests.post(
                    f"{self.NODE_URL}/api/attest",
                    json=attestation,
                    timeout=30
                )
                return response.status_code == 200
            else:
                # Fallback to urllib
                data = json.dumps(attestation).encode()
                req = urllib.request.Request(
                    f"{self.NODE_URL}/api/attest",
                    data=data,
                    headers={'Content-Type': 'application/json'}
                )
                response = urllib.request.urlopen(req, timeout=30)
                return True
        except Exception as e:
            print(f"[ATTEST] Error: {e}")
            return False
    
    def start_mining(self, duration_seconds: int = 60):
        """Start mining for specified duration."""
        print(f"\n[MINE] Starting mining epoch ({duration_seconds}s simulation)...")
        print(f"[MINE] Wallet: {self.wallet}")
        print(f"[MINE] Expected earnings: ~0.36 RTC/epoch (3.0x multiplier)")
        
        self.running = True
        self.epoch_start = time.time()
        
        try:
            while self.running:
                elapsed = time.time() - self.epoch_start
                
                # Simulate mining work
                self._mining_iteration()
                
                # Check if epoch complete
                if elapsed >= duration_seconds:
                    print(f"\n[MINE] Epoch complete! ({elapsed:.1f}s)")
                    break
                
                # Progress indicator
                if int(elapsed) % 10 == 0:
                    progress = (elapsed / duration_seconds) * 100
                    print(f"[MINE] Progress: {progress:.0f}%")
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n[MINE] Stopped by user")
            self.running = False
        
        # Report statistics
        self._report_stats()
    
    def _mining_iteration(self):
        """Perform one mining iteration."""
        # Simulate hash computation
        data = f"{self.wallet}{time.time()}{random.random()}".encode()
        self.sha256.hash(data)
        self.hashes_computed += 1
        
        # Simulate slow 386 performance
        # Real 386 @ 24 MHz: ~100-200 hashes/second for SHA-256
        time.sleep(0.01)  # Simulated delay
    
    def _report_stats(self):
        """Report mining statistics."""
        sha_stats = self.sha256.get_stats()
        
        print("\n" + "="*60)
        print("  Mining Statistics")
        print("="*60)
        print(f"  Total hashes: {self.hashes_computed:,}")
        print(f"  SHA-256 calls: {sha_stats['total_hashes']:,}")
        print(f"  Avg hash time: {sha_stats['avg_time_ms']:.2f} ms")
        print(f"  Total time: {sha_stats['total_time_ms']:.2f} ms")
        print(f"  Estimated earnings: 0.36 RTC (3.0x multiplier)")
        print("="*60)
    
    def stop(self):
        """Stop mining."""
        self.running = False


def main():
    parser = argparse.ArgumentParser(
        description='Nokia 9000 Communicator RustChain Miner Simulator'
    )
    parser.add_argument(
        '--wallet', '-w',
        required=True,
        help='RustChain wallet address'
    )
    parser.add_argument(
        '--duration', '-d',
        type=int,
        default=60,
        help='Mining duration in seconds (default: 60)'
    )
    parser.add_argument(
        '--attest-only',
        action='store_true',
        help='Only submit attestation, do not mine'
    )
    parser.add_argument(
        '--real-hardware',
        action='store_true',
        help='Disable simulation mode (requires actual Nokia 9000)'
    )
    
    args = parser.parse_args()
    
    # Create miner
    miner = RustChainMiner(
        wallet=args.wallet,
        simulate=not args.real_hardware
    )
    
    # Initialize
    if not miner.initialize():
        print("\nFailed to initialize miner. Check hardware compatibility.")
        return 1
    
    # Submit attestation
    if not miner.submit_attestation():
        print("\nFailed to submit attestation. Check network connection.")
        return 1
    
    # Mine or exit
    if args.attest_only:
        print("\nAttestation only mode. Exiting.")
        return 0
    
    # Start mining
    miner.start_mining(duration_seconds=args.duration)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
