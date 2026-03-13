#!/usr/bin/env python3
"""
Palm Pilot Bridge - Serial to HTTP proxy for RustChain Palm Miner

This bridge forwards attestations from the Palm Pilot (via serial) to the RustChain network.

Usage:
    python palm_bridge.py --port COM3 --wallet RTC4325af95d26d59c3ef025963656d22af638bb96b

Requirements:
    pip install pyserial requests
"""

import serial
import requests
import json
import time
import argparse
import sys

RUSTCHAIN_ATTEST_URL = "https://rustchain.org/api/attest"
BAUD_RATE = 9600

def setup_serial(port, baud=BAUD_RATE):
    """Open serial connection to Palm Pilot."""
    try:
        ser = serial.Serial(port, baud, timeout=1)
        print(f"✓ Connected to {port} at {baud} baud")
        return ser
    except serial.SerialException as e:
        print(f"✗ Failed to open {port}: {e}")
        sys.exit(1)

def forward_attestation(ser, wallet):
    """Read attestation from Palm and forward to RustChain."""
    try:
        # Read attestation data from Palm (JSON format)
        print("⏳ Waiting for attestation from Palm...")
        line = ser.readline().decode('utf-8').strip()
        
        if not line:
            print("⚠ No data received from Palm")
            return False
        
        print(f"📥 Received: {line[:80]}...")
        
        # Parse JSON
        try:
            attestation = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"✗ Invalid JSON from Palm: {e}")
            return False
        
        # Add wallet if not present
        if 'wallet' not in attestation:
            attestation['wallet'] = wallet
        
        # Forward to RustChain
        print(f"📤 Sending to RustChain...")
        response = requests.post(
            RUSTCHAIN_ATTEST_URL,
            json=attestation,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"📊 Response status: {response.status_code}")
        
        # Send response back to Palm
        response_data = {
            'status': response.status_code,
            'body': response.text
        }
        ser.write(json.dumps(response_data).encode() + b'\n')
        
        if response.status_code == 200:
            print("✓ Attestation successful!")
            try:
                result = response.json()
                print(f"  Epoch: {result.get('epoch', 'N/A')}")
                print(f"  Reward: {result.get('reward', 'N/A')} RTC")
            except:
                pass
            return True
        else:
            print(f"✗ Attestation failed: {response.text}")
            return False
            
    except serial.SerialException as e:
        print(f"✗ Serial error: {e}")
        return False
    except requests.RequestException as e:
        print(f"✗ Network error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Palm Pilot RustChain Bridge')
    parser.add_argument('--port', required=True, help='Serial port (e.g., COM3, /dev/ttyUSB0)')
    parser.add_argument('--wallet', required=True, help='RTC wallet address')
    parser.add_argument('--baud', type=int, default=BAUD_RATE, help='Baud rate (default: 9600)')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("RustChain Palm Pilot Bridge")
    print("=" * 60)
    print(f"Serial Port: {args.port}")
    print(f"Baud Rate: {args.baud}")
    print(f"Wallet: {args.wallet}")
    print(f"RustChain URL: {RUSTCHAIN_ATTEST_URL}")
    print("=" * 60)
    
    # Open serial connection
    ser = setup_serial(args.port, args.baud)
    
    # Main loop
    successful_attestations = 0
    total_attempts = 0
    
    try:
        while True:
            total_attempts += 1
            print(f"\n[Attempt {total_attempts}]")
            
            if forward_attestation(ser, args.wallet):
                successful_attestations += 1
            
            # Wait for next epoch (10 minutes)
            # Palm will wake up and send next attestation
            print(f"\n⏱ Waiting for next epoch (10 minutes)...")
            print(f"Stats: {successful_attestations}/{total_attempts} successful")
            time.sleep(600)  # 10 minutes
            
    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user")
        print(f"Final stats: {successful_attestations}/{total_attempts} successful")
    finally:
        ser.close()
        print("✓ Serial port closed")

if __name__ == '__main__':
    main()
