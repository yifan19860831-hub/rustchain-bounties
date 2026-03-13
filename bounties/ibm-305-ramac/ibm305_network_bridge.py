#!/usr/bin/env python3
"""
IBM 305 RAMAC Network Bridge
============================
Provides network interface for IBM 305 RAMAC miner via:
- Card reader/punch simulation
- Disk controller interface
- Serial console interface

This bridge allows the IBM 305 to communicate with RustChain network.
"""

import socket
import json
import hashlib
import time
import requests
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum


class InterfaceType(Enum):
    """Supported interface types"""
    CARD_READER = "card_reader"
    DISK_CONTROLLER = "disk_controller"
    SERIAL_CONSOLE = "serial_console"
    SIMULATED = "simulated"


@dataclass
class NetworkRequest:
    """Network request to RustChain API"""
    method: str
    endpoint: str
    params: Dict[str, Any] = None
    body: Dict[str, Any] = None


@dataclass
class NetworkResponse:
    """Network response from RustChain API"""
    status_code: int
    data: Any
    headers: Dict[str, str] = None
    error: str = None


class RustChainAPI:
    """RustChain Network API Client"""
    
    def __init__(self, base_url: str = "https://rustchain.org/api"):
        self.base_url = base_url
        self.session = requests.Session()
        self.miner_id = None
        self.wallet = None
    
    def register_miner(self, miner_name: str, wallet: str, hardware_type: str) -> bool:
        """Register miner with RustChain network"""
        endpoint = f"{self.base_url}/miners"
        payload = {
            "miner_id": f"ibm305ramac_{miner_name}",
            "wallet": wallet,
            "hardware": {
                "type": hardware_type,
                "year": 1956,
                "architecture": "vacuum_tube_bcd",
                "memory": "3200_chars_drum",
                "storage": "5mb_disk"
            }
        }
        
        try:
            response = self.session.post(endpoint, json=payload, timeout=30)
            if response.status_code == 200 or response.status_code == 201:
                self.miner_id = payload["miner_id"]
                self.wallet = wallet
                return True
            else:
                print(f"Registration failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"Registration error: {e}")
            return False
    
    def get_mining_work(self) -> Optional[Dict[str, Any]]:
        """Get mining work from network"""
        if not self.miner_id:
            return None
        
        endpoint = f"{self.base_url}/miners/{self.miner_id}/work"
        
        try:
            response = self.session.get(endpoint, timeout=30)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Get work failed: {response.status_code}")
                return None
        except Exception as e:
            print(f"Get work error: {e}")
            return None
    
    def submit_solution(self, nonce: str, hash_result: str) -> bool:
        """Submit mining solution"""
        if not self.miner_id:
            return False
        
        endpoint = f"{self.base_url}/miners/{self.miner_id}/submit"
        payload = {
            "nonce": nonce,
            "hash": hash_result,
            "timestamp": int(time.time())
        }
        
        try:
            response = self.session.post(endpoint, json=payload, timeout=30)
            if response.status_code == 200:
                print(f"Solution accepted! Hash: {hash_result}")
                return True
            else:
                print(f"Solution rejected: {response.status_code}")
                return False
        except Exception as e:
            print(f"Submit error: {e}")
            return False
    
    def get_miner_status(self) -> Optional[Dict[str, Any]]:
        """Get miner status and earnings"""
        if not self.miner_id:
            return None
        
        endpoint = f"{self.base_url}/miners/{self.miner_id}/status"
        
        try:
            response = self.session.get(endpoint, timeout=30)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception:
            return None


class NetworkBridge:
    """
    Network Bridge for IBM 305 RAMAC
    
    Simulates network interface via card reader/punch or disk controller.
    """
    
    def __init__(self, interface_type: InterfaceType = InterfaceType.SIMULATED):
        self.interface_type = interface_type
        self.api = RustChainAPI()
        self.buffer = []
        self.card_punch_output = []
        self.disk_buffer = {}
        
        # Statistics
        self.stats = {
            'requests_sent': 0,
            'responses_received': 0,
            'cards_punched': 0,
            'cards_read': 0,
            'disk_reads': 0,
            'disk_writes': 0,
            'errors': 0
        }
    
    def initialize(self, miner_name: str, wallet: str) -> bool:
        """Initialize network bridge and register miner"""
        print(f"Initializing IBM 305 Network Bridge...")
        print(f"  Interface: {self.interface_type.value}")
        print(f"  Miner: ibm305ramac_{miner_name}")
        print(f"  Wallet: {wallet}")
        
        success = self.api.register_miner(miner_name, wallet, "IBM_305_RAMAC")
        if success:
            print("  ✓ Miner registered successfully")
        else:
            print("  ✗ Registration failed")
        
        return success
    
    def request_work(self) -> Optional[Dict[str, Any]]:
        """Request mining work from network"""
        print("\nRequesting mining work...")
        work = self.api.get_mining_work()
        
        if work:
            self.stats['requests_sent'] += 1
            self.stats['responses_received'] += 1
            print(f"  ✓ Work received: {work.get('challenge', 'N/A')}")
            
            # Convert work to BCD-compatible format for IBM 305
            bcd_work = self._convert_to_bcd_format(work)
            self.buffer = bcd_work
            
            return work
        else:
            self.stats['errors'] += 1
            print("  ✗ Failed to get work")
            return None
    
    def _convert_to_bcd_format(self, data: Dict[str, Any]) -> list:
        """Convert network data to BCD character format"""
        # Simplified conversion - real implementation would use proper BCD encoding
        json_str = json.dumps(data)
        return [char.upper() for char in json_str if char.isalnum() or char in ' -']
    
    def punch_card(self, data: str):
        """Simulate punching card with data"""
        self.card_punch_output.append(data)
        self.stats['cards_punched'] += 1
        print(f"  [PUNCH] Card: {data[:40]}...")
    
    def read_card(self) -> Optional[str]:
        """Simulate reading a card"""
        if self.buffer:
            card_data = self.buffer.pop(0)
            self.stats['cards_read'] += 1
            print(f"  [READ] Card: {card_data[:40]}...")
            return card_data
        return None
    
    def write_disk(self, address: str, data: str):
        """Write data to disk buffer"""
        self.disk_buffer[address] = data
        self.stats['disk_writes'] += 1
        print(f"  [DISK WRITE] {address}: {data[:40]}...")
    
    def read_disk(self, address: str) -> Optional[str]:
        """Read data from disk buffer"""
        data = self.disk_buffer.get(address)
        if data:
            self.stats['disk_reads'] += 1
            print(f"  [DISK READ] {address}: {data[:40]}...")
        return data
    
    def submit_work(self, nonce: str, hash_result: str) -> bool:
        """Submit mining solution"""
        print(f"\nSubmitting solution...")
        print(f"  Nonce: {nonce}")
        print(f"  Hash: {hash_result}")
        
        success = self.api.submit_solution(nonce, hash_result)
        if success:
            print("  ✓ Solution accepted!")
        else:
            print("  ✗ Solution rejected")
            self.stats['errors'] += 1
        
        return success
    
    def get_statistics(self) -> dict:
        """Get bridge statistics"""
        return {
            **self.stats,
            'interface': self.interface_type.value,
            'miner_id': self.api.miner_id,
            'buffer_size': len(self.buffer),
            'cards_in_buffer': len(self.card_punch_output),
            'disk_entries': len(self.disk_buffer)
        }
    
    def print_card_output(self):
        """Print all punched cards"""
        print("\n" + "=" * 60)
        print("PUNCHED CARD OUTPUT")
        print("=" * 60)
        for i, card in enumerate(self.card_punch_output):
            print(f"Card {i+1:03d}: {card}")
        print("=" * 60)


class CardReaderInterface:
    """
    Arduino/Raspberry Pi Card Reader Interface
    
    This class would interface with physical hardware to read/punch cards.
    For simulation, it uses the NetworkBridge above.
    """
    
    def __init__(self, port: str = "/dev/ttyUSB0", baud: int = 9600):
        self.port = port
        self.baud = baud
        self.serial = None
        self.bridge = NetworkBridge()
    
    def connect(self) -> bool:
        """Connect to card reader hardware"""
        try:
            # In real implementation:
            # import serial
            # self.serial = serial.Serial(self.port, self.baud, timeout=1)
            print(f"Connected to card reader on {self.port} at {self.baud} baud")
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
    
    def read_card(self) -> Optional[str]:
        """Read a physical card"""
        if self.serial:
            # Read from serial
            line = self.serial.readline().decode('ascii').strip()
            return line if line else None
        return None
    
    def punch_card(self, data: str):
        """Punch a physical card"""
        if self.serial:
            # Send to serial
            self.serial.write(f"{data}\n".encode('ascii'))
            print(f"Punched: {data}")


class DiskControllerInterface:
    """
    IBM 350 Disk Controller Interface
    
    Interfaces with IBM 350 disk storage unit via custom controller.
    """
    
    def __init__(self, controller_port: str = "0x378"):
        self.controller_port = controller_port
        self.bridge = NetworkBridge()
        self.current_disk = 0
        self.current_track = 0
        self.current_sector = 0
    
    def select_disk(self, disk_id: int) -> bool:
        """Select disk (0-49)"""
        if 0 <= disk_id < 50:
            self.current_disk = disk_id
            print(f"Selected disk {disk_id}")
            return True
        return False
    
    def seek_track(self, track: int) -> bool:
        """Seek to track"""
        if 0 <= track < 100:  # IBM 350 had ~100 tracks per surface
            self.current_track = track
            print(f"Seek to track {track}")
            # Simulate seek time (~600ms average for IBM 350)
            time.sleep(0.6)
            return True
        return False
    
    def read_sector(self) -> Optional[str]:
        """Read current sector"""
        address = f"{self.current_disk}-{self.current_track}-{self.current_sector}"
        return self.bridge.read_disk(address)
    
    def write_sector(self, data: str):
        """Write current sector"""
        address = f"{self.current_disk}-{self.current_track}-{self.current_sector}"
        self.bridge.write_disk(address, data)


def test_network_bridge():
    """Test network bridge functionality"""
    print("=" * 60)
    print("IBM 305 RAMAC Network Bridge Test")
    print("=" * 60)
    
    # Create bridge
    bridge = NetworkBridge(InterfaceType.SIMULATED)
    
    # Initialize with test wallet
    test_wallet = "RTC4325af95d26d59c3ef025963656d22af638bb96b"
    success = bridge.initialize("test_miner_001", test_wallet)
    
    if not success:
        print("\nRunning in offline mode...")
    
    # Simulate mining cycle
    print("\n" + "=" * 60)
    print("Simulating Mining Cycle")
    print("=" * 60)
    
    # Request work
    work = bridge.request_work()
    
    if work:
        # Simulate IBM 305 processing
        print("\nIBM 305 processing work...")
        time.sleep(1)  # Simulate computation
        
        # Simulate result
        nonce = "12345678"
        hash_result = hashlib.sha256(f"{work.get('challenge', '')}{nonce}".encode()).hexdigest()
        
        # Submit solution
        bridge.submit_work(nonce, hash_result)
    else:
        # Offline mode - simulate work
        print("\nOffline mode - simulating work")
        simulated_work = {
            "challenge": "IBM305_CHALLENGE_1956",
            "difficulty": 5,
            "block_height": 1000000
        }
        bridge.buffer = bridge._convert_to_bcd_format(simulated_work)
        
        # Simulate mining
        nonce = "87654321"
        hash_result = hashlib.sha256(f"{simulated_work['challenge']}{nonce}".encode()).hexdigest()
        bridge.submit_work(nonce, hash_result)
    
    # Print statistics
    print("\n" + "=" * 60)
    print("Bridge Statistics")
    print("=" * 60)
    stats = bridge.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    bridge.print_card_output()
    
    print("\n" + "=" * 60)
    print("Network bridge test complete")
    print("=" * 60)


if __name__ == '__main__':
    test_network_bridge()
