#!/usr/bin/env python3
"""
Test suite for RustChain IBM System/360 Model 30 Miner
======================================================

Tests the S/360 miner functionality including:
- Hardware fingerprint collection
- Entropy generation
- Proof calculation
- Attestation submission
"""

import unittest
import sys
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from s360_miner import S360Miner


class TestS360Miner(unittest.TestCase):
    """Test cases for S/360 miner"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.miner = S360Miner(
            wallet="RTC4325af95d26d59c3ef025963656d22af638bb96b",
            miner_id="S360-TEST-001"
        )
    
    def test_miner_initialization(self):
        """Test miner initializes correctly"""
        self.assertEqual(self.miner.wallet, "RTC4325af95d26d59c3ef025963656d22af638bb96b")
        self.assertEqual(self.miner.architecture["year"], 1965)
        self.assertEqual(self.miner.architecture["antiquity_multiplier"], 5.0)
        self.assertEqual(self.miner.architecture["technology"], "SLT (Solid Logic Technology)")
    
    def test_fingerprint_collection(self):
        """Test hardware fingerprint collection"""
        result = self.miner.collect_fingerprint()
        
        self.assertTrue(result)
        self.assertIn("fingerprint_hash", self.miner.fingerprint_data)
        self.assertIn("slt_timing_samples", self.miner.fingerprint_data)
        self.assertEqual(self.miner.fingerprint_data["technology"], "SLT")
        self.assertEqual(self.miner.fingerprint_data["year"], 1965)
        
        # Verify hash format
        fingerprint = self.miner.fingerprint_data["fingerprint_hash"]
        self.assertEqual(len(fingerprint), 16)  # 16 hex characters
    
    def test_entropy_collection(self):
        """Test entropy collection"""
        result = self.miner.collect_entropy()
        
        self.assertTrue(result)
        self.assertIn("samples", self.miner.entropy_data)
        self.assertIn("variance", self.miner.entropy_data)
        self.assertIn("quality", self.miner.entropy_data)
        
        # Verify entropy quality
        self.assertIn(self.miner.entropy_data["quality"], ["HIGH", "MEDIUM", "LOW"])
    
    def test_proof_calculation(self):
        """Test proof of work calculation"""
        # Must collect fingerprint and entropy first
        self.miner.collect_fingerprint()
        self.miner.collect_entropy()
        
        slot = int(time.time()) // 600  # Current epoch slot
        success, proof_hash = self.miner.calculate_proof(slot)
        
        self.assertIsInstance(success, bool)
        self.assertIsInstance(proof_hash, str)
        self.assertEqual(len(proof_hash), 8)  # 8 hex characters
        
        # Verify proof hash is valid hex
        try:
            int(proof_hash, 16)
        except ValueError:
            self.fail("Proof hash is not valid hexadecimal")
    
    def test_miner_id_generation(self):
        """Test miner ID generation"""
        miner_id = self.miner._generate_miner_id()
        
        self.assertTrue(miner_id.startswith("S360-"))
        self.assertEqual(len(miner_id), 13)  # S360- + 8 hex chars
    
    def test_antiquity_multiplier(self):
        """Test that S/360 gets maximum antiquity multiplier"""
        multiplier = self.miner.architecture["antiquity_multiplier"]
        
        # 1965 hardware should get maximum multiplier
        self.assertEqual(multiplier, 5.0)
        self.assertGreater(multiplier, 2.5)  # Greater than PowerPC G4
    
    def test_architecture_details(self):
        """Test architecture details are correct"""
        arch = self.miner.architecture
        
        self.assertEqual(arch["name"], "IBM System/360 Model 30")
        self.assertEqual(arch["year"], 1965)
        self.assertEqual(arch["word_size"], 32)
        self.assertEqual(arch["byte_size"], 8)
        self.assertEqual(arch["technology"], "SLT (Solid Logic Technology)")
        self.assertEqual(arch["memory_kb"], 32)
        self.assertEqual(arch["clock_mhz"], 1.0)
    
    def test_eligibility_check(self):
        """Test eligibility check (simulated mode)"""
        eligibility = self.miner.check_eligibility()
        
        self.assertIn("eligible", eligibility)
        self.assertIn("slot", eligibility)
        
        # In simulated mode, should be eligible
        self.assertTrue(eligibility.get("simulated", False) or eligibility.get("eligible"))


class TestS360HistoricalAccuracy(unittest.TestCase):
    """Test historical accuracy of S/360 emulation"""
    
    def test_slt_technology(self):
        """Test SLT technology description"""
        miner = S360Miner()
        
        # SLT was introduced with System/360 in 1965
        self.assertEqual(miner.architecture["year"], 1965)
        self.assertIn("SLT", miner.architecture["technology"])
    
    def test_byte_standard(self):
        """Test 8-bit byte standard (S/360 introduced this)"""
        miner = S360Miner()
        
        # S/360 established the 8-bit byte standard
        self.assertEqual(miner.architecture["byte_size"], 8)
    
    def test_word_size(self):
        """Test 32-bit word size"""
        miner = S360Miner()
        
        # S/360 had 32-bit words
        self.assertEqual(miner.architecture["word_size"], 32)


def run_tests():
    """Run all tests"""
    print("=" * 70)
    print("RustChain S/360 Miner Test Suite")
    print("=" * 70)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add tests
    suite.addTests(loader.loadTestsFromTestCase(TestS360Miner))
    suite.addTests(loader.loadTestsFromTestCase(TestS360HistoricalAccuracy))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print()
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
