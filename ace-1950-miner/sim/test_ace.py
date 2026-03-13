#!/usr/bin/env python3
"""
ACE (1950) Simulator Test Suite

Tests for:
- CPU instruction execution
- Memory operations
- SHA-256 integration
- Assembler output validation
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sim.ace_cpu import ACECPU, encode_instr
from sim.sha256 import sha256_hex, TEST_VECTORS


def test_cpu_basic():
    """Test basic CPU operations"""
    print("\n" + "=" * 60)
    print("Test 1: CPU Basic Operations")
    print("=" * 60)
    
    cpu = ACECPU(memory_size=128)
    
    # Test program: Simple addition (opcodes match ace_cpu.py)
    # LD=0x0C, ACL=0x02, ST=0x0D, STOP=0x11
    program = [
        encode_instr(0x0C, 10, 0),  # LD from 10
        encode_instr(0x02, 11, 0),  # ACL from 11
        encode_instr(0x0D, 0, 20),  # ST to 20
        encode_instr(0x11, 0, 0),   # STOP
    ]
    program.extend([0] * 6)
    program.extend([100, 50, 0])  # Data at 10,11
    program.extend([0] * 7)
    program.append(0)  # Result at 20
    
    cpu.load_program(program)
    cpu.run(max_instructions=10)
    
    result = cpu.memory.read(20)
    expected = 150
    
    print(f"Result: {result}")
    print(f"Expected: {expected}")
    
    if result == expected:
        print("Status: PASS")
        return True
    else:
        print("Status: FAIL")
        return False


def test_cpu_multiply():
    """Test software multiplication"""
    print("\n" + "=" * 60)
    print("Test 2: CPU Multiplication")
    print("=" * 60)
    
    cpu = ACECPU(memory_size=128)
    
    # Test: 8 × 9 = 72 (LD=0x0C, MLA=0x14, ST=0x0D, STOP=0x11)
    program = [
        encode_instr(0x0C, 10, 0),  # LD from 10
        encode_instr(0x14, 11, 0),  # MLA from 11
        encode_instr(0x0D, 0, 20),  # ST to 20
        encode_instr(0x11, 0, 0),   # STOP
    ]
    program.extend([0] * 6)
    program.extend([8, 9, 0])
    program.extend([0] * 7)
    program.append(0)
    
    cpu.load_program(program)
    cpu.run(max_instructions=10)
    
    result = cpu.memory.read(20)
    expected = 72
    
    print(f"Result: {result}")
    print(f"Expected: {expected}")
    
    if result == expected:
        print("Status: PASS")
        return True
    else:
        print("Status: FAIL")
        return False


def test_cpu_jump():
    """Test jump instructions"""
    print("\n" + "=" * 60)
    print("Test 3: CPU Jump Instructions")
    print("=" * 60)
    
    cpu = ACECPU(memory_size=128)
    
    # Test: Loop that counts down (LD=0x0C, SUB=0x05, ST=0x0D, JZ=0x0F, JMP=0x0E, STOP=0x11)
    program = [
        encode_instr(0x0C, 10, 0),  # 0: LD counter
        encode_instr(0x05, 11, 0),  # 1: SUB 1
        encode_instr(0x0D, 0, 10),  # 2: ST back to counter
        encode_instr(0x0F, 5, 0),   # 3: JZ to 5 (if zero, exit)
        encode_instr(0x0E, 0, 0),   # 4: JMP to 0
        encode_instr(0x11, 0, 0),   # 5: STOP
    ]
    program.extend([0] * 4)
    program.extend([3, 1])  # Counter=3, decrement=1
    
    cpu.load_program(program)
    cpu.run(max_instructions=20)
    
    result = cpu.memory.read(10)
    expected = 0  # Should count down to 0
    
    print(f"Final counter: {result}")
    print(f"Expected: {expected}")
    
    if result == expected:
        print("Status: PASS")
        return True
    else:
        print("Status: FAIL")
        return False


def test_sha256_vectors():
    """Test SHA-256 implementation"""
    print("\n" + "=" * 60)
    print("Test 4: SHA-256 Test Vectors")
    print("=" * 60)
    
    all_pass = True
    for message, expected in TEST_VECTORS:
        result = sha256_hex(message)
        if result != expected:
            all_pass = False
            print(f"FAIL: '{message}'")
            print(f"  Expected: {expected}")
            print(f"  Got: {result}")
        else:
            print(f"PASS: '{message}'")
    
    if all_pass:
        print("Status: ALL PASS")
    else:
        print("Status: SOME FAILED")
    
    return all_pass


def test_memory_expansion():
    """Test memory expansion (128 -> 352 words)"""
    print("\n" + "=" * 60)
    print("Test 5: Memory Expansion")
    print("=" * 60)
    
    cpu = ACECPU(memory_size=128)
    
    # Write to original memory
    cpu.memory.write(100, 0x12345678)
    
    # Expand memory
    cpu.memory.expand(352)
    
    # Verify original data
    original = cpu.memory.read(100)
    
    # Write to expanded memory
    cpu.memory.write(300, 0xABCDEF01)
    expanded = cpu.memory.read(300)
    
    print(f"Original memory[100]: 0x{original:08X}")
    print(f"Expanded memory[300]: 0x{expanded:08X}")
    
    if original == 0x12345678 and expanded == 0xABCDEF01:
        print("Status: PASS")
        return True
    else:
        print("Status: FAIL")
        return False


def run_all_tests():
    """Run all tests and report results"""
    print("\n" + "=" * 60)
    print("   ACE (1950) Simulator - Test Suite")
    print("   Alan Turing's Computer")
    print("=" * 60)
    
    tests = [
        ("CPU Basic", test_cpu_basic),
        ("CPU Multiply", test_cpu_multiply),
        ("CPU Jump", test_cpu_jump),
        ("SHA-256", test_sha256_vectors),
        ("Memory Expansion", test_memory_expansion),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\nERROR in {name}: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {name:20} {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\nALL TESTS PASSED!")
        return 0
    else:
        print(f"\n{total - passed} TEST(S) FAILED!")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
