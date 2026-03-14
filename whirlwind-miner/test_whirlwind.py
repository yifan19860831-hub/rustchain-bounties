#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Suite for Whirlwind I Miner
=================================

Verifies the Whirlwind simulator implementation for RustChain.
"""

import sys
import os
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from whirlwind_miner import (
    MagneticCoreMemory,
    WhirlwindCPU,
    WhirlwindMiner,
    WORD_SIZE,
    MEMORY_WORDS,
    OPCODES
)


def test_memory_basic():
    """Test basic memory operations"""
    print("[TEST] Memory Basic Operations...")
    
    memory = MagneticCoreMemory(size=2048)
    
    # Test write/read
    memory.write(0x100, 0xABCD)
    assert memory.read(0x100) == 0xABCD, "Basic write/read failed"
    
    # Test 16-bit masking
    memory.write(0x101, 0x12345)  # Exceeds 16 bits
    assert memory.read(0x101) == 0x2345, "16-bit masking failed"
    
    # Test boundary
    memory.write(0x7FF, 0xFFFF)
    assert memory.read(0x7FF) == 0xFFFF, "Boundary test failed"
    
    print("  [PASS] Memory basic operations")
    return True


def test_memory_bounds():
    """Test memory boundary checking"""
    print("[TEST] Memory Boundary Checking...")
    
    memory = MagneticCoreMemory(size=2048)
    
    try:
        memory.read(2048)  # Out of bounds
        print("  [FAIL] Should have raised ValueError")
        return False
    except ValueError:
        pass
    
    try:
        memory.write(-1, 0x1234)  # Negative address
        print("  [FAIL] Should have raised ValueError")
        return False
    except ValueError:
        pass
    
    print("  [PASS] Memory boundary checking")
    return True


def test_cpu_cla():
    """Test CLA (Clear Accumulator) instruction"""
    print("[TEST] CPU CLA Instruction...")
    
    memory = MagneticCoreMemory()
    cpu = WhirlwindCPU(memory)
    
    cpu.accumulator = 0xFFFF
    cpu.execute(0b0000, 0)  # CLA
    
    assert cpu.accumulator == 0, f"CLA failed: {cpu.accumulator}"
    print("  [PASS] CLA instruction")
    return True


def test_cpu_add():
    """Test ADD instruction"""
    print("[TEST] CPU ADD Instruction...")
    
    memory = MagneticCoreMemory()
    cpu = WhirlwindCPU(memory)
    
    memory.write(0x100, 0x0042)
    cpu.accumulator = 0x0010
    cpu.execute(0b0001, 0x100)  # ADD
    
    assert cpu.accumulator == 0x0052, f"ADD failed: {cpu.accumulator:04X}"
    print("  [PASS] ADD instruction")
    return True


def test_cpu_sub():
    """Test SUB instruction"""
    print("[TEST] CPU SUB Instruction...")
    
    memory = MagneticCoreMemory()
    cpu = WhirlwindCPU(memory)
    
    memory.write(0x100, 0x0020)
    cpu.accumulator = 0x0050
    cpu.execute(0b0010, 0x100)  # SUB
    
    assert cpu.accumulator == 0x0030, f"SUB failed: {cpu.accumulator:04X}"
    print("  [PASS] SUB instruction")
    return True


def test_cpu_sto():
    """Test STO (Store) instruction"""
    print("[TEST] CPU STO Instruction...")
    
    memory = MagneticCoreMemory()
    cpu = WhirlwindCPU(memory)
    
    cpu.accumulator = 0xDEAD
    cpu.execute(0b0101, 0x200)  # STO
    
    assert memory.read(0x200) == 0xDEAD, f"STO failed: {memory.read(0x200):04X}"
    print("  [PASS] STO instruction")
    return True


def test_cpu_jumps():
    """Test jump instructions"""
    print("[TEST] CPU Jump Instructions...")
    
    memory = MagneticCoreMemory()
    cpu = WhirlwindCPU(memory)
    
    # Test JUP (unconditional jump)
    cpu.program_counter = 0x100
    cpu.execute(0b1000, 0x200)  # JUP
    assert cpu.program_counter == 0x200, "JUP failed"
    
    # Test JIZ (jump if zero)
    cpu.accumulator = 0
    cpu.program_counter = 0x100
    cpu.execute(0b1011, 0x300)  # JIZ
    assert cpu.program_counter == 0x300, "JIZ (zero) failed"
    
    # Test JIZ (not zero - should not jump, but PC already incremented by fetch)
    # Note: In real CPU, fetch increments PC, so execute doesn't change it if no jump
    cpu.accumulator = 1
    cpu.program_counter = 0x100
    # Simulate fetch incrementing PC
    cpu.program_counter = 0x101
    cpu.execute(0b1011, 0x300)  # JIZ - should NOT change PC
    assert cpu.program_counter == 0x101, f"JIZ (non-zero) failed: {cpu.program_counter}"
    
    # Test JIM (jump if minus)
    cpu.accumulator = 0x8000  # Sign bit set
    cpu.program_counter = 0x100
    cpu.execute(0b1001, 0x400)  # JIM
    assert cpu.program_counter == 0x400, "JIM failed"
    
    print("  [PASS] Jump instructions")
    return True


def test_cpu_logic():
    """Test logic instructions"""
    print("[TEST] CPU Logic Instructions...")
    
    memory = MagneticCoreMemory()
    cpu = WhirlwindCPU(memory)
    
    # Test ANI (AND)
    memory.write(0x100, 0x0F0F)
    cpu.accumulator = 0xF0F0
    cpu.execute(0b1101, 0x100)  # ANI
    assert cpu.accumulator == 0x0000, f"ANI failed: {cpu.accumulator:04X}"
    
    # Test ORI (OR)
    memory.write(0x101, 0x00FF)
    cpu.accumulator = 0xF000
    cpu.execute(0b1110, 0x101)  # ORI
    assert cpu.accumulator == 0xF0FF, f"ORI failed: {cpu.accumulator:04X}"
    
    # Test XOR
    memory.write(0x102, 0xFFFF)
    cpu.accumulator = 0x5555
    cpu.execute(0b1111, 0x102)  # XOR
    assert cpu.accumulator == 0xAAAA, f"XOR failed: {cpu.accumulator:04X}"
    
    print("  [PASS] Logic instructions")
    return True


def test_cpu_run_program():
    """Test running a complete program"""
    print("[TEST] CPU Program Execution...")
    
    memory = MagneticCoreMemory()
    cpu = WhirlwindCPU(memory)
    
    # Load simple program: CLA, ADD, STO, HTR
    program = [
        0b0000_000000000000,  # 0x0: CLA (clear accumulator)
        0b0001_000000000100,  # 0x1: ADD 4 (add value at addr 4)
        0b0101_000000000010,  # 0x2: STO 2 (store to addr 2)
        0b0111_000000000000,  # 0x3: HTR (halt)
        0x002A,  # 0x4: value 42
    ]
    
    for addr, value in enumerate(program):
        memory.write(addr, value)
    
    # Run program
    cpu.run(max_instructions=100)
    
    # Check result: accumulator should be 42 (0x2A)
    assert cpu.accumulator == 0x2A, f"Program failed: {cpu.accumulator:04X}"
    assert cpu.halted == True, "Program should have halted"
    assert memory.read(2) == 0x2A, "Store failed"
    
    print("  [PASS] Program execution")
    return True


def test_miner_initialization():
    """Test miner initialization"""
    print("[TEST] Miner Initialization...")
    
    miner = WhirlwindMiner(
        wallet="RTC4325af95d26d59c3ef025963656d22af638bb96b",
        miner_id="whirlwind-test-1951"
    )
    
    assert miner.wallet == "RTC4325af95d26d59c3ef025963656d22af638bb96b"
    assert "whirlwind" in miner.miner_id.lower()
    assert miner.memory.size == 2048
    assert miner.cpu is not None
    
    print("  [PASS] Miner initialization")
    return True


def test_miner_fingerprint():
    """Test hardware fingerprint generation"""
    print("[TEST] Miner Hardware Fingerprint...")
    
    miner = WhirlwindMiner()
    fingerprint = miner.get_hardware_fingerprint()
    
    # Check basic structure
    assert "checks" in fingerprint, "Missing 'checks' key"
    assert "all_passed" in fingerprint, "Missing 'all_passed' key"
    
    # Check all 6 required checks
    checks = fingerprint["checks"]
    required_checks = [
        "clock_skew",
        "cache_timing",
        "simd_identity",
        "thermal_drift",
        "instruction_jitter",
        "anti_emulation"
    ]
    
    for check_name in required_checks:
        assert check_name in checks, f"Missing check: {check_name}"
        check_data = checks[check_name]
        assert isinstance(check_data, dict), f"Check {check_name} is not a dict"
        assert "passed" in check_data, f"Check {check_name} missing 'passed' field"
        assert "data" in check_data, f"Check {check_name} missing 'data' field"
    
    print("  [PASS] Hardware fingerprint")
    return True


def test_miner_epoch_mining():
    """Test epoch mining simulation"""
    print("[TEST] Miner Epoch Mining...")
    
    miner = WhirlwindMiner()
    result = miner.mine_epoch(epoch=1)
    
    assert "epoch" in result
    assert "instructions_executed" in result
    assert "commitment" in result
    assert "accepted" in result
    assert "reward_rtc" in result
    assert "multiplier" in result
    
    assert result["epoch"] == 1
    assert result["multiplier"] == 3.0  # LEGENDARY tier
    assert result["instructions_executed"] > 0
    assert len(result["commitment"]) == 64  # SHA256 hex
    
    print("  [PASS] Epoch mining")
    return True


def test_opcode_table():
    """Test opcode table completeness"""
    print("[TEST] Opcode Table...")
    
    assert len(OPCODES) == 16, "Should have 16 opcodes"
    
    # Verify all expected opcodes
    expected = {
        0b0000: 'CLA',
        0b0001: 'ADD',
        0b0010: 'SUB',
        0b0011: 'MPY',
        0b0100: 'DIV',
        0b0101: 'STO',
        0b0110: 'SLW',
        0b0111: 'HTR',
        0b1000: 'JUP',
        0b1001: 'JIM',
        0b1010: 'JIP',
        0b1011: 'JIZ',
        0b1100: 'TMI',
        0b1101: 'ANI',
        0b1110: 'ORI',
        0b1111: 'XOR',
    }
    
    for opcode, mnemonic in expected.items():
        assert opcode in OPCODES, f"Missing opcode {opcode:04b}"
        assert OPCODES[opcode] == mnemonic, f"Opcode {opcode:04b} mismatch"
    
    print("  [PASS] Opcode table")
    return True


def run_all_tests():
    """Run all tests"""
    print("=" * 70)
    print("WHIRLWIND I MINER - TEST SUITE")
    print("=" * 70)
    print()
    
    tests = [
        test_memory_basic,
        test_memory_bounds,
        test_cpu_cla,
        test_cpu_add,
        test_cpu_sub,
        test_cpu_sto,
        test_cpu_jumps,
        test_cpu_logic,
        test_cpu_run_program,
        test_miner_initialization,
        test_miner_fingerprint,
        test_miner_epoch_mining,
        test_opcode_table,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  [FAIL] {test.__name__} raised exception: {e}")
            failed += 1
        print()
    
    print("=" * 70)
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(tests)} tests")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
