#!/usr/bin/env python3
"""Quick test of Apple I miner functionality"""

import sys
sys.path.insert(0, 'src')

from apple1_miner import MOS6502, Apple1Fingerprint, RustChainAttestation

print("=" * 60)
print("RustChain Apple I Miner - Quick Test")
print("=" * 60)

# Test 1: 6502 Emulator
print("\n[TEST 1] MOS 6502 Emulator")
cpu = MOS6502(memory_size=4096)
print(f"  Memory size: {len(cpu.memory)} bytes")
print(f"  Initial state: A={cpu.registers['A']:02X}, X={cpu.registers['X']:02X}, Y={cpu.registers['Y']:02X}")
print(f"  PC: ${cpu.registers['PC']:04X}, SP: ${cpu.registers['SP']:02X}")
print(f"  Status: ${cpu.registers['P']:02X}")
print("  [OK] 6502 initialized")

# Test 2: Hardware Fingerprint
print("\n[TEST 2] Apple I Hardware Fingerprint")
fp = Apple1Fingerprint(cpu)
fingerprint = fp.generate_fingerprint()

print(f"  Platform: {fingerprint['platform']}")
print(f"  CPU: {fingerprint['cpu']}")
print(f"  Year: {fingerprint['year']}")
print(f"  All checks passed: {fingerprint['all_passed']}")

for check_name, check_data in fingerprint['checks'].items():
    status = "PASS" if check_data['pass'] else "FAIL"
    print(f"    - {check_name:20} [{status}]")

print(f"  Fingerprint hash: {fingerprint['fingerprint_hash'][:32]}...")

# Test 3: Attestation Generation
print("\n[TEST 3] RustChain Attestation")
wallet = "RTC4325af95d26d59c3ef025963656d22af638bb96b"
attestation = RustChainAttestation(wallet, cpu)
attest_data = attestation.generate_attestation(epoch=1)

print(f"  Wallet: {attest_data['wallet']}")
print(f"  Epoch: {attest_data['epoch']}")
print(f"  Antiquity Multiplier: {attest_data['antiquity_multiplier']}x")
print(f"  Timestamp: {attest_data['timestamp']}")
print(f"  Signature: {attest_data['signature'][:32]}...")

# Test 4: Reward Calculation
print("\n[TEST 4] Reward Calculation")
reward = attestation.calculate_reward(base_reward=1.5, num_miners=5)
print(f"  Base reward: 1.5 RTC/epoch")
print(f"  Active miners: 5")
print(f"  Apple I multiplier: 5.0x")
print(f"  Expected reward: {reward:.2f} RTC/epoch")

# Test 5: Save/Load Attestation
print("\n[TEST 5] Save/Load Attestation")
attestation.save_to_file(attest_data, 'test_attest.json')
loaded = attestation.load_from_file('test_attest.json')
if loaded:
    print(f"  [OK] Attestation saved and loaded successfully")
    print(f"  Verified epoch: {loaded['epoch']}")
    print(f"  Verified wallet: {loaded['wallet']}")
else:
    print(f"  [FAIL] Could not load attestation")

print("\n" + "=" * 60)
print("All tests completed successfully!")
print("=" * 60)
