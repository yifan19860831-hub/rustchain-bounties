#!/usr/bin/env python3
"""
Unit tests for Atari 2600 Miner Simulator
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulator.atari_miner import (
    Atari2600State,
    AtariDisplay,
    MiningStats,
    SimplifiedSHA256,
    AtariMinerSimulator
)


class TestAtari2600State(unittest.TestCase):
    """Test the Atari 2600 state emulation"""
    
    def test_initial_state(self):
        """Test initial state values"""
        state = Atari2600State()
        self.assertEqual(state.nonce, 0)
        self.assertEqual(state.nonce_low, 0)
        self.assertEqual(state.nonce_high, 0)
        self.assertEqual(state.difficulty, 15)
        self.assertEqual(state.status, 0)
    
    def test_nonce_increment(self):
        """Test 16-bit nonce increment"""
        state = Atari2600State()
        
        # Increment from 0 to 1
        state.increment_nonce()
        self.assertEqual(state.nonce, 1)
        self.assertEqual(state.nonce_low, 1)
        self.assertEqual(state.nonce_high, 0)
        
        # Increment to 255
        state.nonce = 254
        state.increment_nonce()
        self.assertEqual(state.nonce, 255)
        self.assertEqual(state.nonce_low, 255)
        self.assertEqual(state.nonce_high, 0)
        
        # Increment to 256 (should carry)
        state.increment_nonce()
        self.assertEqual(state.nonce, 256)
        self.assertEqual(state.nonce_low, 0)
        self.assertEqual(state.nonce_high, 1)
        
        # Increment to 65535
        state.nonce = 65534
        state.increment_nonce()
        self.assertEqual(state.nonce, 65535)
        self.assertEqual(state.nonce_low, 255)
        self.assertEqual(state.nonce_high, 255)
        
        # Increment to 0 (wrap around)
        state.increment_nonce()
        self.assertEqual(state.nonce, 0)
        self.assertEqual(state.nonce_low, 0)
        self.assertEqual(state.nonce_high, 0)
    
    def test_nonce_setter(self):
        """Test nonce setter"""
        state = Atari2600State()
        
        state.nonce = 0x1234
        self.assertEqual(state.nonce_low, 0x34)
        self.assertEqual(state.nonce_high, 0x12)
        
        state.nonce = 0xFFFF
        self.assertEqual(state.nonce_low, 0xFF)
        self.assertEqual(state.nonce_high, 0xFF)
    
    def test_reset(self):
        """Test state reset"""
        state = Atari2600State()
        state.nonce = 12345
        state.status = 1
        
        state.reset()
        
        self.assertEqual(state.nonce, 0)
        self.assertEqual(state.status, 0)


class TestSimplifiedSHA256(unittest.TestCase):
    """Test the simplified SHA-256 implementation"""
    
    def test_mine_returns_tuple(self):
        """Test that mine returns (hash, found) tuple"""
        hash_result, found = SimplifiedSHA256.mine(0, 15)
        
        self.assertIsInstance(hash_result, bytes)
        self.assertEqual(len(hash_result), 4)
        self.assertIsInstance(found, bool)
    
    def test_mine_deterministic(self):
        """Test that same nonce produces same hash"""
        hash1, _ = SimplifiedSHA256.mine(42, 15)
        hash2, _ = SimplifiedSHA256.mine(42, 15)
        
        self.assertEqual(hash1, hash2)
    
    def test_mine_different_nonces(self):
        """Test that different nonces produce different hashes"""
        hash1, _ = SimplifiedSHA256.mine(1, 15)
        hash2, _ = SimplifiedSHA256.mine(2, 15)
        
        self.assertNotEqual(hash1, hash2)
    
    def test_difficulty_check(self):
        """Test difficulty threshold checking"""
        # Very easy difficulty (255) should find blocks frequently
        found_count = 0
        for nonce in range(1000):
            _, found = SimplifiedSHA256.mine(nonce, 255)
            if found:
                found_count += 1
        
        # With difficulty 255, almost all hashes should be "found"
        self.assertGreater(found_count, 900)
        
        # Very hard difficulty (1) should rarely find blocks
        found_count = 0
        for nonce in range(1000):
            _, found = SimplifiedSHA256.mine(nonce, 1)
            if found:
                found_count += 1
        
        # With difficulty 1, very few hashes should be "found"
        self.assertLess(found_count, 10)


class TestMiningStats(unittest.TestCase):
    """Test mining statistics tracking"""
    
    def test_initial_stats(self):
        """Test initial statistics values"""
        stats = MiningStats()
        
        self.assertEqual(stats.total_hashes, 0)
        self.assertEqual(stats.blocks_found, 0)
        self.assertEqual(stats.hash_rate, 0.0)
    
    def test_reset(self):
        """Test stats reset"""
        stats = MiningStats()
        stats.total_hashes = 1000
        stats.blocks_found = 5
        
        stats.reset()
        
        self.assertEqual(stats.total_hashes, 0)
        self.assertEqual(stats.blocks_found, 0)
        self.assertGreater(stats.elapsed, 0)


class TestAtariDisplay(unittest.TestCase):
    """Test Atari display rendering"""
    
    def test_render_frame(self):
        """Test frame rendering"""
        display = AtariDisplay()
        state = Atari2600State()
        stats = MiningStats()
        
        frame = display.render_frame(state, stats)
        
        self.assertIn("RUSTCHAIN MINER", frame)
        self.assertIn("NONCE:", frame)
        self.assertIn("HASH:", frame)
        self.assertIn("STATUS:", frame)


class TestAtariMinerSimulator(unittest.TestCase):
    """Test the main simulator"""
    
    def test_simulator_initialization(self):
        """Test simulator initialization"""
        sim = AtariMinerSimulator(difficulty=20)
        
        self.assertEqual(sim.state.difficulty, 20)
        self.assertFalse(sim.running)
    
    def test_mine_step(self):
        """Test single mining step"""
        sim = AtariMinerSimulator(difficulty=255)  # Very easy
        
        # Should find blocks frequently with easy difficulty
        found = False
        for _ in range(100):
            if sim.mine_step():
                found = True
                break
        
        self.assertTrue(found)
    
    def test_mine_step_increments_nonce(self):
        """Test that mining increments nonce"""
        sim = AtariMinerSimulator()
        
        initial_nonce = sim.state.nonce
        sim.mine_step()
        
        self.assertEqual(sim.state.nonce, initial_nonce + 1)


if __name__ == '__main__':
    unittest.main()
