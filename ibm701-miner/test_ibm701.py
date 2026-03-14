#!/usr/bin/env python3
"""
Test suite for IBM 701 Simulator and Miner
"""

import unittest
import sys
import os
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import simulator components
from ibm701_simulator import (
    WilliamsTube, WilliamsTubeMemory, IBM701CPU, 
    IBM701Miner, WORD_BITS, MEMORY_SIZE, VacuumTubeTiming
)


class TestWilliamsTube(unittest.TestCase):
    """Test Williams tube memory simulation"""
    
    def test_write_read(self):
        """Test basic write and read operations"""
        tube = WilliamsTube()
        test_value = 0x12345678
        tube.write(test_value)
        self.assertEqual(tube.read(), test_value)
    
    def test_36bit_mask(self):
        """Test 36-bit word masking"""
        tube = WilliamsTube()
        large_value = 0xFFFFFFFFF  # 36 bits
        tube.write(large_value)
        self.assertEqual(tube.read(), large_value)
        
        # Test overflow
        overflow_value = 0x1000000000  # 37 bits
        tube.write(overflow_value)
        self.assertEqual(tube.read(), large_value)
    
    def test_decay(self):
        """Test Williams tube decay simulation"""
        tube = WilliamsTube()
        tube.write(0x12345)
        
        # Simulate time passing without refresh
        tube.tick(0.025)  # 25ms (> 20ms decay threshold)
        
        # Data should be lost
        self.assertEqual(tube.read(), 0)


class TestWilliamsTubeMemory(unittest.TestCase):
    """Test Williams tube memory array"""
    
    def test_memory_size(self):
        """Test memory has correct size"""
        mem = WilliamsTubeMemory()
        self.assertEqual(len(mem.tubes), MEMORY_SIZE)
    
    def test_memory_read_write(self):
        """Test memory read/write operations"""
        mem = WilliamsTubeMemory()
        test_value = 0xABCDEF123
        address = 100
        
        mem.write_word(address, test_value)
        self.assertEqual(mem.read_word(address), test_value)
    
    def test_memory_bounds(self):
        """Test memory bounds checking"""
        mem = WilliamsTubeMemory()
        
        # Should return 0 for out of bounds
        self.assertEqual(mem.read_word(-1), 0)
        self.assertEqual(mem.read_word(MEMORY_SIZE), 0)


class TestIBM701CPU(unittest.TestCase):
    """Test IBM 701 CPU simulation"""
    
    def setUp(self):
        """Set up test CPU"""
        self.cpu = IBM701CPU()
    
    def test_initial_state(self):
        """Test CPU initial state"""
        self.assertEqual(self.cpu.ac, 0)
        self.assertEqual(self.cpu.mq, 0)
        self.assertEqual(self.cpu.pc, 0)
        self.assertFalse(self.cpu.running)
    
    def test_load_store(self):
        """Test LD and ST instructions"""
        # Store value at address 0x100
        self.cpu.ac = 0x12345
        self.cpu.memory.write_word(0x100, self.cpu.ac)
        
        # Load it back
        loaded = self.cpu.memory.read_word(0x100)
        self.assertEqual(loaded, 0x12345)
    
    def test_add_instruction(self):
        """Test ADD instruction"""
        self.cpu.ac = 10
        self.cpu.memory.write_word(0x100, 5)
        
        # Manually execute ADD
        value = self.cpu.memory.read_word(0x100)
        self.cpu.ac = self.cpu.to_36bit(self.cpu.ac + value)
        
        self.assertEqual(self.cpu.ac, 15)
    
    def test_vacuum_tube_timing(self):
        """Test vacuum tube timing variance"""
        times = []
        for _ in range(100):
            # Reinitialize timing to get fresh random values
            self.cpu.timing = VacuumTubeTiming()
            time_us = self.cpu.timing.get_operation_time(60)
            times.append(time_us)
        
        # Average should be close to base time (variance averages out)
        avg_time = sum(times) / len(times)
        self.assertAlmostEqual(avg_time, 60, delta=5)


class TestIBM701Miner(unittest.TestCase):
    """Test IBM 701 Miner"""
    
    def setUp(self):
        """Set up test miner"""
        self.miner = IBM701Miner(wallet_address='RTCtest123456789')
    
    def test_wallet_initialization(self):
        """Test wallet is set correctly"""
        self.assertEqual(self.miner.wallet, 'RTCtest123456789')
    
    def test_generate_wallet(self):
        """Test wallet generation"""
        miner = IBM701Miner()
        self.assertTrue(miner.wallet.startswith('RTC'))
        self.assertEqual(len(miner.wallet), 43)  # RTC + 40 hex chars
    
    def test_fingerprint_generation(self):
        """Test fingerprint generation"""
        fingerprint = self.miner.generate_fingerprint()
        self.assertTrue(fingerprint.startswith('IBM701-'))
        self.assertTrue(len(fingerprint) >= 23)  # IBM701- + hex chars
    
    def test_attestation_creation(self):
        """Test attestation creation"""
        attestation = self.miner.create_attestation()
        
        self.assertEqual(attestation['hardware'], 'IBM 701')
        self.assertEqual(attestation['year'], 1952)
        self.assertEqual(attestation['multiplier'], 5.0)
        self.assertEqual(attestation['tier'], 'LEGENDARY')
        self.assertIn('signature', attestation)
    
    def test_mine_epoch(self):
        """Test mining a single epoch"""
        attestation = self.miner.mine_epoch()
        
        self.assertIn('fingerprint', attestation)
        self.assertIn('signature', attestation)
        self.assertEqual(self.miner.epoch, 1)


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_full_mining_cycle(self):
        """Test complete mining cycle"""
        miner = IBM701Miner(wallet_address='RTCintegration123')
        
        # Mine 3 epochs
        attestations = miner.run(epochs=3)
        
        self.assertEqual(len(attestations), 3)
        self.assertEqual(miner.epoch, 3)
        
        # Verify all attestations have required fields
        for att in attestations:
            self.assertIn('hardware', att)
            self.assertIn('fingerprint', att)
            self.assertIn('signature', att)
            self.assertEqual(att['multiplier'], 5.0)


def run_tests():
    """Run all tests"""
    print("=" * 60)
    print("IBM 701 Miner Test Suite")
    print("=" * 60)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestWilliamsTube))
    suite.addTests(loader.loadTestsFromTestCase(TestWilliamsTubeMemory))
    suite.addTests(loader.loadTestsFromTestCase(TestIBM701CPU))
    suite.addTests(loader.loadTestsFromTestCase(TestIBM701Miner))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print()
    print("=" * 60)
    if result.wasSuccessful():
        print("[OK] All tests passed!")
    else:
        print(f"[FAIL] {len(result.failures)} failures, {len(result.errors)} errors")
    print("=" * 60)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
