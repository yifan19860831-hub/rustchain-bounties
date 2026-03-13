#!/usr/bin/env python3
"""
IBM 305 RAMAC Miner Test Suite
===============================
Comprehensive tests for IBM 305 RAMAC mining implementation.
"""

import sys
import os
import time
import hashlib

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_bcd_codec():
    """Test BCD character encoding/decoding"""
    print("\n" + "=" * 60)
    print("TEST 1: BCD Codec")
    print("=" * 60)
    
    from ibm305_miner import BCDCodec
    
    # Test encoding
    test_text = "HELLO WORLD"
    encoded = BCDCodec.encode(test_text)
    print(f"Input:  {test_text}")
    print(f"Encoded: {[f'{b:07b}' for b in encoded]}")
    
    # Test decoding
    decoded = BCDCodec.decode(encoded)
    print(f"Decoded: {decoded}")
    
    # Verify
    assert decoded == test_text, f"Expected {test_text}, got {decoded}"
    print("[PASS] BCD Codec test PASSED")
    
    return True


def test_sha256_bcd():
    """Test SHA256 BCD implementation"""
    print("\n" + "=" * 60)
    print("TEST 2: SHA256 BCD")
    print("=" * 60)
    
    from ibm305_miner import SHA256BCD
    
    # Test cases
    test_cases = [
        ("IBM305", "SHA256 of 'IBM305'"),
        ("RAMAC1956", "SHA256 of 'RAMAC1956'"),
        ("HELLO WORLD", "SHA256 of 'HELLO WORLD'"),
    ]
    
    for message, description in test_cases:
        hash_result = SHA256BCD.hash_bcd(message)
        print(f"\n{description}:")
        print(f"  Input:  {message}")
        print(f"  Hash:   {hash_result}")
        
        # Verify against standard SHA256
        expected = hashlib.sha256(message.encode()).hexdigest().upper()
        assert hash_result == expected, f"Hash mismatch: {hash_result} != {expected}"
    
    print("\n[PASS] SHA256 BCD test PASSED")
    return True


def test_hardware_fingerprint():
    """Test hardware fingerprinting"""
    print("\n" + "=" * 60)
    print("TEST 3: Hardware Fingerprint")
    print("=" * 60)
    
    from ibm305_miner import HardwareFingerprint
    
    # Create fingerprint
    fp = HardwareFingerprint(serial_number="IBM305_TEST_001")
    fingerprint_hash = fp.generate()
    
    print(f"Serial Number: {fp.serial_number}")
    print(f"Fingerprint:   {fingerprint_hash}")
    print(f"Length:        {len(fingerprint_hash)} chars")
    
    # Verify uniqueness
    fp2 = HardwareFingerprint(serial_number="IBM305_TEST_002")
    fingerprint_hash2 = fp2.generate()
    
    assert fingerprint_hash != fingerprint_hash2, "Fingerprints should be unique"
    print(f"Fingerprint 2: {fingerprint_hash2}")
    
    print("\n[PASS] Hardware Fingerprint test PASSED")
    return True


def test_simulator():
    """Test IBM 305 simulator"""
    print("\n" + "=" * 60)
    print("TEST 4: IBM 305 Simulator")
    print("=" * 60)
    
    from ibm305_simulator import IBM305Simulator
    
    # Create simulator
    sim = IBM305Simulator()
    
    # Load test program
    test_program = [
        "000000001   ",  # Clear accumulator
        "001002005   ",  # Copy 5 chars
        "00000000P   ",  # Halt
    ]
    
    # Initialize data
    sim.drum.write_field('0', 1, "HELLO")
    
    # Run
    print("Loading test program...")
    sim.load_program(test_program)
    
    print("Running simulation...")
    stats = sim.run(max_instructions=100)
    
    print(f"\nStatistics:")
    print(f"  Instructions: {stats['instructions_executed']}")
    print(f"  Drum reads:   {stats['drum_reads']}")
    print(f"  Drum writes:  {stats['drum_writes']}")
    print(f"  Halted:       {stats['halted']}")
    
    # Verify execution
    assert stats['instructions_executed'] > 0, "No instructions executed"
    assert stats['halted'], "Program did not halt"
    
    print("\n[PASS] IBM 305 Simulator test PASSED")
    return True


def test_assembler():
    """Test IBM 305 assembler"""
    print("\n" + "=" * 60)
    print("TEST 5: IBM 305 Assembler")
    print("=" * 60)
    
    from ibm305_assembler import IBM305Assembler
    
    # Test program
    test_program = """
// Test assembly program
START:  COPY    0,0,1,0,5   // Copy 5 chars
        CLEAR_ACC           // Clear accumulator
        HALT                // Exit
"""
    
    # Assemble
    assembler = IBM305Assembler()
    machine_code, errors, warnings = assembler.assemble(test_program)
    
    print("Input assembly:")
    print(test_program)
    
    print("\nMachine code output:")
    for i, code in enumerate(machine_code):
        print(f"  {i:02d}: {code}")
    
    if errors:
        print(f"\nErrors: {errors}")
        return False
    
    if warnings:
        print(f"\nWarnings: {warnings}")
    
    # Verify output
    assert len(machine_code) == 3, f"Expected 3 instructions, got {len(machine_code)}"
    assert 'START' in assembler.symbols, "Label not found"
    
    print("\n[PASS] IBM 305 Assembler test PASSED")
    return True


def test_miner():
    """Test IBM 305 miner"""
    print("\n" + "=" * 60)
    print("TEST 6: IBM 305 Miner")
    print("=" * 60)
    
    from ibm305_miner import IBM305Miner
    
    # Create miner
    miner = IBM305Miner(
        miner_name="test_miner",
        wallet="RTC4325af95d26d59c3ef025963656d22af638bb96b"
    )
    
    # Get work
    work = miner.get_work(
        challenge="TEST_CHALLENGE_123",
        difficulty=3  # Low difficulty for testing
    )
    
    print(f"Work received:")
    print(f"  Challenge: {work.challenge}")
    print(f"  Difficulty: {work.difficulty}")
    print(f"  Target: {work.target}")
    
    # Mine (small range for testing)
    print("\nMining (100 nonces)...")
    start_time = time.time()
    solution = miner.mine(max_nonces=100)
    elapsed = time.time() - start_time
    
    if solution:
        print(f"\n[SUCCESS] Solution found!")
        print(f"  Nonce: {solution.nonce}")
        print(f"  Hash: {solution.hash_result[:32]}...")
    else:
        print(f"\nNo solution in 100 nonces (expected for low sample)")
    
    # Get statistics
    stats = miner.get_statistics()
    print(f"\nStatistics:")
    print(f"  Miner ID: {stats['miner_id']}")
    print(f"  Total hashes: {stats['total_hashes']}")
    print(f"  Hash rate: {stats['hash_rate']:.2f} H/s")
    print(f"  Uptime: {elapsed:.2f}s")
    
    # Verify
    assert stats['total_hashes'] > 0, "No hashes computed"
    
    print("\n[PASS] IBM 305 Miner test PASSED")
    return True


def test_network_bridge():
    """Test network bridge"""
    print("\n" + "=" * 60)
    print("TEST 7: Network Bridge")
    print("=" * 60)
    
    from ibm305_network_bridge import NetworkBridge, InterfaceType
    
    # Create bridge (simulated mode)
    bridge = NetworkBridge(InterfaceType.SIMULATED)
    
    # Initialize
    print("Initializing network bridge...")
    success = bridge.initialize("test_miner", "RTC4325af95d26d59c3ef025963656d22af638bb96b")
    
    if not success:
        print("Running in offline mode (no network)...")
    
    # Test card operations
    print("\nTesting card operations...")
    bridge.write_disk("0-0-0", "TEST_DATA_123")
    data = bridge.read_disk("0-0-0")
    print(f"Disk write/read: {data}")
    
    assert data == "TEST_DATA_123", "Disk I/O failed"
    
    # Get statistics
    stats = bridge.get_statistics()
    print(f"\nBridge statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n[PASS] Network Bridge test PASSED")
    return True


def test_drum_optimization():
    """Test drum memory optimization"""
    print("\n" + "=" * 60)
    print("TEST 8: Drum Memory Optimization")
    print("=" * 60)
    
    from ibm305_miner import IBM305Miner
    
    miner = IBM305Miner("test", "wallet")
    
    print("Current drum layout:")
    for section, (track, addr) in miner.drum_layout.items():
        print(f"  {section:15s}: Track {track}, Address {addr}")
    
    # Optimize
    print("\nOptimizing...")
    miner.optimize_drum_layout()
    
    print("\n[PASS] Drum Memory Optimization test PASSED")
    return True


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("IBM 305 RAMAC MINER - TEST SUITE")
    print("=" * 70)
    print(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    tests = [
        ("BCD Codec", test_bcd_codec),
        ("SHA256 BCD", test_sha256_bcd),
        ("Hardware Fingerprint", test_hardware_fingerprint),
        ("IBM 305 Simulator", test_simulator),
        ("IBM 305 Assembler", test_assembler),
        ("IBM 305 Miner", test_miner),
        ("Network Bridge", test_network_bridge),
        ("Drum Optimization", test_drum_optimization),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result, None))
        except Exception as e:
            results.append((name, False, str(e)))
            print(f"\n[FAIL] {name} test FAILED: {e}")
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result, _ in results if result)
    total = len(results)
    
    for name, result, error in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"  {name:30s}: {status}")
        if error:
            print(f"    Error: {error}")
    
    print("\n" + "-" * 70)
    print(f"Total: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("=" * 70)
    
    return passed == total


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
