#!/usr/bin/env python3
"""
Test Suite for MANIAC I Miner
Validates simulator and mining functionality
"""

import unittest
import time
from maniac_simulator import MANIACSimulator, Opcode, WilliamsTube
from maniac_miner import MANIACMiner, BlockHeader, MiningResult


class TestWilliamsTube(unittest.TestCase):
    """Test Williams-Kilburn tube memory"""
    
    def test_write_read(self):
        """Test basic memory operations"""
        tube = WilliamsTube(capacity=1024)
        
        # Write value
        tube.write(0, 0x123456789)
        
        # Read back
        value = tube.read(0)
        self.assertEqual(value, 0x123456789)
    
    def test_40_bit_mask(self):
        """Test 40-bit word masking"""
        tube = WilliamsTube(capacity=1024)
        
        # Write value larger than 40 bits
        tube.write(0, 0xFFFFFFFFFFFF)  # 48 bits
        
        # Should be masked to 40 bits
        value = tube.read(0)
        self.assertEqual(value, 0xFFFFFFFFFF)  # 40 bits max
    
    def test_address_bounds(self):
        """Test memory bounds checking"""
        tube = WilliamsTube(capacity=1024)
        
        with self.assertRaises(MemoryError):
            tube.write(1024, 0x123)  # Out of bounds
        
        with self.assertRaises(MemoryError):
            tube.read(-1)  # Negative address
    
    def test_refresh_counter(self):
        """Test memory refresh counting"""
        tube = WilliamsTube(capacity=1024)
        initial_refreshes = tube.refresh_count
        
        tube.read(0)
        self.assertEqual(tube.refresh_count, initial_refreshes + 1)
        
        tube.write(0, 0x123)
        self.assertEqual(tube.refresh_count, initial_refreshes + 2)


class TestMANIACSimulator(unittest.TestCase):
    """Test MANIAC I CPU simulator"""
    
    def setUp(self):
        self.sim = MANIACSimulator()
    
    def test_load_store(self):
        """Test LOAD and STORE instructions"""
        program = [
            0x0000000010,  # LOAD from addr 16
            0x0100000011,  # STORE to addr 17
            0x0B00000000,  # HALT
        ]
        
        self.sim.load_program(program)
        self.sim.load_data([0xDEADBEEF], start_address=16)
        
        self.sim.run()
        
        # Check value was copied
        value = self.sim.memory.read(17)
        self.assertEqual(value, 0xDEADBEEF)
    
    def test_arithmetic(self):
        """Test ADD and SUB instructions"""
        program = [
            0x0000000010,  # LOAD a (16)
            0x0200000011,  # ADD b (17)
            0x0100000012,  # STORE result (18)
            0x0B00000000,  # HALT
        ]
        
        self.sim.load_program(program)
        self.sim.load_data([10, 20], start_address=16)  # a=10, b=20
        
        self.sim.run()
        
        result = self.sim.memory.read(18)
        self.assertEqual(result, 30)
    
    def test_jump_zero(self):
        """Test conditional jump on zero"""
        program = [
            0x0000000010,  # LOAD value (16)
            0x0700000005,  # JZ to addr 5 if zero
            0x0B00000000,  # HALT (addr 2)
            0x0000000000,  # NOP (addr 3)
            0x0000000000,  # NOP (addr 4)
            0x0B00000000,  # HALT (addr 5)
        ]
        
        # Test with zero - should jump
        self.sim.load_program(program)
        self.sim.load_data([0], start_address=16)
        self.sim.run()
        self.assertTrue(self.sim.state.halt)
        
        # Test with non-zero - should not jump
        self.sim = MANIACSimulator()
        self.sim.load_program(program)
        self.sim.load_data([1], start_address=16)
        self.sim.run()
        # Should halt at addr 2, not addr 5
    
    def test_sum_program(self):
        """Test summing numbers 1-10"""
        program = [
            0x0000000010,  # LOAD counter
            0x0200000011,  # ADD one
            0x0100000010,  # STORE counter
            0x0000000012,  # LOAD sum
            0x0200000010,  # ADD counter
            0x0100000012,  # STORE sum
            0x0000000010,  # LOAD counter
            0x0300000013,  # SUB ten
            0x0800000000,  # JN start (loop)
            0x0B00000000,  # HALT
        ]
        
        data = [0, 1, 0, 10]  # counter, one, sum, ten
        
        self.sim.load_program(program)
        self.sim.load_data(data, start_address=16)
        
        cycles = self.sim.run(max_cycles=1000)
        
        sum_result = self.sim.memory.read(18)
        self.assertEqual(sum_result, 55)  # 1+2+...+10 = 55
        self.assertLess(cycles, 1000)


class TestMANIACMiner(unittest.TestCase):
    """Test MANIAC I miner"""
    
    def test_miner_initialization(self):
        """Test miner creates with correct parameters"""
        wallet = "RTC4325af95d26d59c3ef025963656d22af638bb96b"
        miner = MANIACMiner(wallet_address=wallet)
        
        self.assertEqual(miner.wallet, wallet)
        self.assertEqual(miner.antiquity_multiplier, 10.0)
        self.assertIsNotNone(miner.hardware_id)
    
    def test_hardware_fingerprint(self):
        """Test hardware fingerprint is unique"""
        miner1 = MANIACMiner(wallet_address="RTC1")
        miner2 = MANIACMiner(wallet_address="RTC2")
        
        # Fingerprints should be different (random components)
        self.assertNotEqual(miner1.hardware_id, miner2.hardware_id)
    
    def test_hash_computation(self):
        """Test hash computation"""
        miner = MANIACMiner(wallet_address="RTC1")
        
        header = BlockHeader(
            version=1,
            previous_hash="0" * 64,
            merkle_root="test" + "0" * 60,
            timestamp=int(time.time()),
            difficulty=4,
            nonce=12345
        )
        
        hash_result = miner._compute_hash(header)
        
        # Should produce valid SHA-256 hash
        self.assertEqual(len(hash_result), 64)
        self.assertTrue(all(c in '0123456789abcdef' for c in hash_result))
    
    def test_difficulty_check(self):
        """Test difficulty validation"""
        miner = MANIACMiner(wallet_address="RTC1")
        
        # Easy difficulty (1 leading zero)
        self.assertTrue(miner._check_difficulty("0abc123", 1))
        self.assertFalse(miner._check_difficulty("1abc123", 1))
        
        # Harder difficulty (4 leading zeros)
        self.assertTrue(miner._check_difficulty("0000abcd", 4))
        self.assertFalse(miner._check_difficulty("000abcd", 4))
    
    def test_mining_result(self):
        """Test mining produces valid result"""
        miner = MANIACMiner(wallet_address="RTC1")
        
        # Mine with easy difficulty
        result = miner.mine_block(difficulty=2, max_nonces=10000)
        
        # Should complete (may or may not find block)
        self.assertIsInstance(result, MiningResult)
        self.assertGreater(result.cycles, 0)
        self.assertGreater(result.time_elapsed, 0)
    
    def test_hardware_stats(self):
        """Test hardware statistics collection"""
        miner = MANIACMiner(wallet_address="RTC1")
        
        # Mine a bit to generate stats
        miner.mine_block(difficulty=1, max_nonces=100)
        
        stats = miner.get_hardware_stats()
        
        self.assertEqual(stats['architecture'], 'MANIAC I (1952)')
        self.assertEqual(stats['word_size'], 40)
        self.assertEqual(stats['memory_size'], 1024)
        self.assertEqual(stats['clock_speed_hz'], 200000)
        self.assertEqual(stats['antiquity_multiplier'], 10.0)
        self.assertGreater(stats['cpu_cycles'], 0)


class TestBlockHeader(unittest.TestCase):
    """Test block header serialization"""
    
    def test_serialize(self):
        """Test header serialization"""
        header = BlockHeader(
            version=1,
            previous_hash="abc123",
            merkle_root="def456",
            timestamp=1234567890,
            difficulty=4,
            nonce=999
        )
        
        serialized = header.serialize()
        self.assertIsInstance(serialized, bytes)
        self.assertGreater(len(serialized), 0)


if __name__ == '__main__':
    print("=" * 60)
    print("🧪 MANIAC I Miner Test Suite")
    print("=" * 60)
    
    unittest.main(verbosity=2)
