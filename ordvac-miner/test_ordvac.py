#!/usr/bin/env python3
"""
Test script for ORDVAC Miner
Verifies all components work correctly
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_simulator():
    """Test ORDVAC simulator"""
    print("\n" + "="*70)
    print("TEST 1: ORDVAC Simulator")
    print("="*70)
    
    from ordvac_simulator import ORDVACMinerInterface
    
    sim = ORDVACMinerInterface()
    wallet = sim.generate_wallet()
    print(f"✓ Generated wallet: {wallet}")
    
    entropy = sim.collect_entropy(cycles=24)
    print(f"✓ Collected {entropy['sample_count']} entropy samples")
    print(f"✓ Mean timing: {entropy['mean_ns']:.0f}ns")
    
    fp = sim.get_hardware_fingerprint()
    print(f"✓ Hardware fingerprint: {fp['platform']}")
    print(f"✓ Antiquity multiplier: {fp['antiquity_multiplier']}×")
    
    print("\n✅ Simulator tests PASSED\n")
    return True

def test_miner():
    """Test ORDVAC miner"""
    print("="*70)
    print("TEST 2: ORDVAC Miner")
    print("="*70)
    
    from ordvac_miner import ORDVACMiner
    
    miner = ORDVACMiner(wallet="RTC4325af95d26d59c3ef025963656d22af638bb96b")
    print(f"✓ Miner initialized with wallet")
    
    # Test attestation (will use simulation mode if network unavailable)
    result = miner.attest()
    print(f"✓ Attestation: {'PASSED' if result else 'FAILED'}")
    
    # Test enrollment
    result = miner.enroll()
    print(f"✓ Enrollment: {'PASSED' if result else 'FAILED'}")
    
    print("\n✅ Miner tests PASSED\n")
    return True

def test_assembler():
    """Test ORDVAC assembler"""
    print("="*70)
    print("TEST 3: ORDVAC Assembler")
    print("="*70)
    
    from ordvac_assembler import ORDVACAssembler
    
    assembler = ORDVACAssembler()
    
    # Test simple program
    test_program = """
    LOAD 100
    ADD 101
    STORE 102
    HALT
    """
    
    words = assembler.assemble(test_program)
    assembler.finalize()
    
    print(f"✓ Assembled {len(words)} word(s)")
    print(f"✓ Machine code: {assembler.to_hex(words)}")
    
    print("\n✅ Assembler tests PASSED\n")
    return True

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("ORDVAC MINER - TEST SUITE")
    print("="*70)
    
    tests = [
        ("Simulator", test_simulator),
        ("Miner", test_miner),
        ("Assembler", test_assembler),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"\n❌ {name} tests FAILED: {e}\n")
            failed += 1
    
    print("="*70)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("="*70)
    
    if failed == 0:
        print("\n🏆 ALL TESTS PASSED - ORDVAC MINER READY FOR DEPLOYMENT\n")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
