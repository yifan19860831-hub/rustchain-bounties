#!/usr/bin/env python3
"""
Unit tests for Joust Miner Simulator
"""

import unittest
import time
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from joust_simulator import Motorola6809, JoustMiner
from joust_hardware import JoustHardwareFingerprint


class TestMotorola6809(unittest.TestCase):
    """Test 6809 CPU emulator"""
    
    def test_register_initialization(self):
        """Test registers initialize to zero"""
        cpu = Motorola6809()
        self.assertEqual(cpu.A, 0)
        self.assertEqual(cpu.B, 0)
        self.assertEqual(cpu.X, 0)
        self.assertEqual(cpu.Y, 0)
        self.assertEqual(cpu.PC, 0)
    
    def test_memory_read_write(self):
        """Test memory read/write operations"""
        cpu = Motorola6809()
        
        # Write byte
        cpu.write_byte(0x100, 0xAB)
        self.assertEqual(cpu.read_byte(0x100), 0xAB)
        
        # Write word
        cpu.write_word(0x200, 0x1234)
        self.assertEqual(cpu.read_word(0x200), 0x1234)
    
    def test_vblank_interrupt(self):
        """Test VBLANK interrupt counter"""
        cpu = Motorola6809()
        
        initial = cpu.vblank_count
        cpu.vblank_interrupt()
        self.assertEqual(cpu.vblank_count, initial + 1)
    
    def test_hash_computation(self):
        """Test hash computation is deterministic"""
        cpu = Motorola6809()
        cpu.epoch_num = 1
        cpu.nonce = 100
        cpu.hardware_id = 0xDEAD
        
        hash1 = cpu.compute_hash()
        hash2 = cpu.compute_hash()
        
        self.assertEqual(hash1, hash2)
    
    def test_mining_step(self):
        """Test mining step increments nonce"""
        cpu = Motorola6809()
        initial_nonce = cpu.nonce
        
        cpu.mine_step()
        
        self.assertEqual(cpu.nonce, initial_nonce + 1)


class TestJoustHardwareFingerprint(unittest.TestCase):
    """Test hardware fingerprinting"""
    
    def test_fingerprint_generation(self):
        """Test fingerprint generation"""
        hw = JoustHardwareFingerprint()
        fingerprint = hw.get_full_fingerprint()
        
        self.assertIn('platform', fingerprint)
        self.assertIn('hardware_signature', fingerprint)
        self.assertIn('checks', fingerprint)
        self.assertEqual(len(fingerprint['checks']), 6)
    
    def test_clock_skew_check(self):
        """Test clock skew measurement"""
        hw = JoustHardwareFingerprint()
        result = hw.measure_clock_skew()
        
        self.assertEqual(result['check'], 'clock_skew')
        self.assertIn('drift_ppm', result)
        self.assertIn('passed', result)
    
    def test_anti_emulation_check(self):
        """Test anti-emulation check"""
        hw = JoustHardwareFingerprint()
        result = hw.check_anti_emulation()
        
        self.assertEqual(result['check'], 'anti_emulation')
        self.assertIn('belly_flop_bug_detected', result)
    
    def test_attestation_generation(self):
        """Test attestation generation"""
        hw = JoustHardwareFingerprint()
        attestation = hw.generate_attestation(
            wallet='RTC4325af95d26d59c3ef025963656d22af638bb96b',
            epoch=1,
            nonce=100
        )
        
        self.assertEqual(attestation['wallet'], 'RTC4325af95d26d59c3ef025963656d22af638bb96b')
        self.assertEqual(attestation['epoch'], 1)
        self.assertEqual(attestation['nonce'], 100)
        self.assertEqual(attestation['antiquity_multiplier'], 3.0)


class TestJoustMiner(unittest.TestCase):
    """Test Joust Miner integration"""
    
    def test_miner_initialization(self):
        """Test miner initializes correctly"""
        miner = JoustMiner(
            wallet='RTC4325af95d26d59c3ef025963656d22af638bb96b',
            dry_run=True
        )
        
        self.assertEqual(miner.wallet, 'RTC4325af95d26d59c3ef025963656d22af638bb96b')
        self.assertTrue(miner.bridge.dry_run)
        self.assertEqual(miner.proofs_found, 0)
    
    def test_miner_dry_run(self):
        """Test miner dry run mode"""
        miner = JoustMiner(
            wallet='RTC4325af95d26d59c3ef025963656d22af638bb96b',
            dry_run=True
        )
        
        # Run for very short duration
        miner.run(duration=0.1)
        
        # Should have computed some hashes
        self.assertGreater(miner.hashes_computed, 0)


if __name__ == '__main__':
    unittest.main()
