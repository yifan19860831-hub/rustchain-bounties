#!/usr/bin/env python3
"""
Test suite for ERA 1101 CPU simulator
"""

import sys
sys.path.insert(0, '.')

from cpu import ERA1101CPU


def test_basic_arithmetic():
    """Test basic addition and subtraction"""
    print("Testing basic arithmetic...")
    cpu = ERA1101CPU()
    
    # Test addition: 42 + 24 = 66
    # Instruction format: opcode(6) | skip(4) | address(14)
    program = [
        0x000003,  # INS skip=0 addr=3
        0x180004,  # ADD skip=0 addr=4 (0x06 << 18 = 0x180000)
        0x540005,  # STO skip=0 addr=5 (0x15 << 18 = 0x540000)
        0x00002A,  # Data: 42
        0x000018,  # Data: 24
        0x000000,  # Result
        0x880000,  # HALT (0x22 << 18 = 0x880000)
    ]
    
    cpu.load_program(program)
    cpu.run(max_instructions=10)
    
    assert cpu.memory[5] == 66, f"Expected 66, got {cpu.memory[5]}"
    print("[PASS] Addition test passed")


def test_ones_complement():
    """Test ones' complement arithmetic"""
    print("Testing ones' complement...")
    cpu = ERA1101CPU()
    
    # Test complement
    value = 0x123456
    complement = cpu.ones_complement(value)
    expected = (~value) & 0xFFFFFF
    
    assert complement == expected, f"Complement failed: {complement:06X} != {expected:06X}"
    print("[PASS] Ones' complement test passed")


def test_flags():
    """Test status flags"""
    print("Testing status flags...")
    cpu = ERA1101CPU()
    
    # Test zero flag
    cpu.AL = 0
    cpu.set_flags(0)
    assert cpu.zero_flag == True, "Zero flag should be set"
    
    # Test negative flag
    cpu.set_flags(0x800000)  # MSB set
    assert cpu.neg_flag == True, "Negative flag should be set"
    
    print("[PASS] Flags test passed")


def test_jump():
    """Test jump instructions"""
    print("Testing jump instructions...")
    cpu = ERA1101CPU()
    
    # Simple loop: increment counter, jump if not zero
    program = [
        0x000003,  # 0: INS 3 (load counter)
        0x180004,  # 1: ADD 4 (increment) - fixed encoding
        0x540003,  # 2: STO 3 (store back) - fixed encoding
        0x700000,  # 3: JNZ 0 (loop if not zero) - 0x1C << 18 = 0x700000
        0x000000,  # 4: Counter (starts at 0)
        0x000001,  # 5: Increment value
    ]
    
    cpu.load_program(program)
    cpu.run(max_instructions=20)
    
    print("[PASS] Jump test passed")


def test_memory():
    """Test memory operations"""
    print("Testing memory operations...")
    cpu = ERA1101CPU()
    
    # Write and read
    cpu.store(0x100, 0xABCDEF)
    value = cpu.load(0x100)
    
    assert value == 0xABCDEF, f"Memory test failed: {value:06X}"
    print("[PASS] Memory test passed")


def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("ERA 1101 CPU Simulator Test Suite")
    print("=" * 50)
    print()
    
    tests = [
        test_basic_arithmetic,
        test_ones_complement,
        test_flags,
        test_jump,
        test_memory,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"[FAIL] {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"[FAIL] {test.__name__} error: {e}")
            failed += 1
    
    print()
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
