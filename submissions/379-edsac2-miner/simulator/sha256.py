#!/usr/bin/env python3
"""
EDSAC 2 SHA256 Implementation
=============================
Reference implementation of SHA256 for the EDSAC 2 miner.

This implementation is designed to be portable to EDSAC 2 assembly,
with 40-bit word operations and minimal memory footprint.

Author: RustChain EDSAC 2 Miner Project
License: MIT
"""

import struct
from typing import List, Tuple


class SHA256_EDSAC2:
    """
    SHA256 implementation optimized for EDSAC 2 architecture.
    
    Uses 40-bit words internally (like EDSAC 2), but operates
    on 32-bit SHA256 values by masking.
    """
    
    # 40-bit mask
    MASK_40 = 0xFFFFFFFFFF
    # 32-bit mask (for SHA256 operations)
    MASK_32 = 0xFFFFFFFF
    
    # SHA256 constants (first 32 bits of fractional parts of cube roots of first 64 primes)
    K = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
        0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
        0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
        0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
        0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
        0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
        0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
        0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
        0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ]
    
    # Initial hash values (first 32 bits of fractional parts of square roots of first 8 primes)
    H_INIT = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    ]
    
    def __init__(self):
        """Initialize SHA256 context"""
        self.H = list(self.H_INIT)  # Hash state
        self.buffer = bytearray()    # Message buffer
        self.bit_count = 0           # Total bits processed
    
    def rotr(self, x: int, n: int) -> int:
        """32-bit right rotation"""
        x = x & self.MASK_32
        return ((x >> n) | (x << (32 - n))) & self.MASK_32
    
    def shr(self, x: int, n: int) -> int:
        """32-bit right shift"""
        return (x >> n) & self.MASK_32
    
    def ch(self, x: int, y: int, z: int) -> int:
        """Choice function: (x AND y) XOR (NOT x AND z)"""
        return ((x & y) ^ (~x & z)) & self.MASK_32
    
    def maj(self, x: int, y: int, z: int) -> int:
        """Majority function: (x AND y) XOR (x AND z) XOR (y AND z)"""
        return ((x & y) ^ (x & z) ^ (y & z)) & self.MASK_32
    
    def sigma0(self, x: int) -> int:
        """Σ0(x) = ROTR²(x) ⊕ ROTR¹³(x) ⊕ ROTR²²(x)"""
        return self.rotr(x, 2) ^ self.rotr(x, 13) ^ self.rotr(x, 22)
    
    def sigma1(self, x: int) -> int:
        """Σ1(x) = ROTR⁶(x) ⊕ ROTR¹¹(x) ⊕ ROTR²⁵(x)"""
        return self.rotr(x, 6) ^ self.rotr(x, 11) ^ self.rotr(x, 25)
    
    def gamma0(self, x: int) -> int:
        """σ0(x) = ROTR⁷(x) ⊕ ROTR¹⁸(x) ⊕ SHR³(x)"""
        return self.rotr(x, 7) ^ self.rotr(x, 18) ^ self.shr(x, 3)
    
    def gamma1(self, x: int) -> int:
        """σ1(x) = ROTR¹⁷(x) ⊕ ROTR¹⁹(x) ⊕ SHR¹⁰(x)"""
        return self.rotr(x, 17) ^ self.rotr(x, 19) ^ self.shr(x, 10)
    
    def pad_message(self, message: bytes) -> bytes:
        """
        Pad message according to SHA256 specification.
        
        Message is padded to a multiple of 512 bits (64 bytes):
        - Append bit '1'
        - Append zeros until length ≡ 448 (mod 512)
        - Append original length in bits as 64-bit big-endian
        """
        msg_len = len(message)
        bit_len = msg_len * 8
        
        # Append bit '1' (as 0x80 byte)
        message += b'\x80'
        
        # Append zeros until length ≡ 448 (mod 512)
        # 448 bits = 56 bytes
        pad_len = (56 - (msg_len + 1) % 64) % 64
        message += b'\x00' * pad_len
        
        # Append original length in bits as 64-bit big-endian
        message += struct.pack('>Q', bit_len)
        
        return message
    
    def process_block(self, block: bytes):
        """
        Process a single 512-bit (64-byte) block.
        
        This is the core compression function.
        """
        assert len(block) == 64, "Block must be 64 bytes"
        
        # Parse block into 16 32-bit big-endian words
        W = list(struct.unpack('>16I', block))
        
        # Extend to 64 words (message schedule)
        for i in range(16, 64):
            s0 = self.gamma0(W[i-15])
            s1 = self.gamma1(W[i-2])
            W.append((W[i-16] + s0 + W[i-7] + s1) & self.MASK_32)
        
        # Initialize working variables
        a, b, c, d, e, f, g, h = self.H
        
        # 64 rounds
        for i in range(64):
            S1 = self.sigma1(e)
            ch = self.ch(e, f, g)
            temp1 = (h + S1 + ch + self.K[i] + W[i]) & self.MASK_32
            S0 = self.sigma0(a)
            maj = self.maj(a, b, c)
            temp2 = (S0 + maj) & self.MASK_32
            
            h = g
            g = f
            f = e
            e = (d + temp1) & self.MASK_32
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & self.MASK_32
        
        # Update hash state
        self.H[0] = (self.H[0] + a) & self.MASK_32
        self.H[1] = (self.H[1] + b) & self.MASK_32
        self.H[2] = (self.H[2] + c) & self.MASK_32
        self.H[3] = (self.H[3] + d) & self.MASK_32
        self.H[4] = (self.H[4] + e) & self.MASK_32
        self.H[5] = (self.H[5] + f) & self.MASK_32
        self.H[6] = (self.H[6] + g) & self.MASK_32
        self.H[7] = (self.H[7] + h) & self.MASK_32
    
    def update(self, data: bytes):
        """
        Update hash with new data.
        
        Data is buffered until we have a complete 512-bit block.
        """
        self.buffer.extend(data)
        self.bit_count += len(data) * 8
        
        # Process complete blocks
        while len(self.buffer) >= 64:
            self.process_block(bytes(self.buffer[:64]))
            self.buffer = self.buffer[64:]
    
    def digest(self) -> bytes:
        """
        Finalize hash and return digest.
        
        Returns:
            32-byte SHA256 digest
        """
        # Save current state
        H_save = list(self.H)
        buffer_save = bytearray(self.buffer)
        bit_count_save = self.bit_count
        
        # Pad and process final block(s)
        padded = self.pad_message(bytes(self.buffer))
        for i in range(0, len(padded), 64):
            self.process_block(padded[i:i+64])
        
        # Get final hash
        result = struct.pack('>8I', *self.H)
        
        # Restore state (for potential reuse)
        self.H = H_save
        self.buffer = buffer_save
        self.bit_count = bit_count_save
        
        return result
    
    def hexdigest(self) -> str:
        """Return hexadecimal digest"""
        return self.digest().hex()
    
    def reset(self):
        """Reset hash state"""
        self.H = list(self.H_INIT)
        self.buffer = bytearray()
        self.bit_count = 0


def sha256(data: bytes) -> bytes:
    """Convenience function: compute SHA256 of data"""
    hasher = SHA256_EDSAC2()
    hasher.update(data)
    return hasher.digest()


def sha256_hex(data: bytes) -> str:
    """Convenience function: compute SHA256 hex digest of data"""
    return sha256(data).hex()


def sha256_double(data: bytes) -> bytes:
    """Double SHA256 (used in Bitcoin/RustChain mining)"""
    return sha256(sha256(data))


# Test vectors from NIST FIPS 180-4
TEST_VECTORS = [
    (b"", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    (b"abc", "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"),
    (b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq",
     "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1"),
]


def test_sha256():
    """Test SHA256 implementation against NIST vectors"""
    print("Testing SHA256 implementation...")
    print("=" * 60)
    
    all_passed = True
    for i, (message, expected) in enumerate(TEST_VECTORS):
        result = sha256_hex(message)
        passed = result == expected
        all_passed = all_passed and passed
        
        status = "PASS" if passed else "FAIL"
        print(f"Test {i+1}: {status}")
        print(f"  Input:    {message!r}")
        print(f"  Expected: {expected}")
        print(f"  Got:      {result}")
        print()
    
    if all_passed:
        print("All tests PASSED!")
    else:
        print("Some tests FAILED!")
    
    return all_passed


class EDSAC2Miner:
    """
    RustChain miner simulation for EDSAC 2.
    
    This class simulates the mining process that would run on EDSAC 2 hardware.
    """
    
    def __init__(self, wallet_address: str):
        self.wallet = wallet_address
        self.sha256 = SHA256_EDSAC2()
        self.nonce = 0
        self.hashes_computed = 0
    
    def build_block_header(self, prev_hash: bytes, merkle_root: bytes, 
                          timestamp: int, difficulty: int) -> bytes:
        """
        Build block header for mining.
        
        Header format (80 bytes):
        - prev_hash: 32 bytes
        - merkle_root: 32 bytes
        - timestamp: 8 bytes (64-bit)
        - difficulty: 8 bytes (64-bit)
        """
        header = bytearray()
        header.extend(prev_hash)
        header.extend(merkle_root)
        header.extend(struct.pack('>Q', timestamp))
        header.extend(struct.pack('>Q', difficulty))
        return bytes(header)
    
    def mine(self, prev_hash: bytes, merkle_root: bytes, 
             timestamp: int, difficulty: int, max_nonces: int = 1000) -> Tuple[bool, int, bytes]:
        """
        Attempt to mine a block.
        
        Args:
            prev_hash: Previous block hash (32 bytes)
            merkle_root: Merkle root of transactions (32 bytes)
            timestamp: Block timestamp
            difficulty: Mining difficulty target
            max_nonces: Maximum nonce attempts
        
        Returns:
            (success, nonce, block_hash)
        """
        target = (1 << 256) // difficulty  # Simplified difficulty target
        
        for nonce in range(max_nonces):
            # Build header with nonce
            header = self.build_block_header(prev_hash, merkle_root, timestamp, difficulty)
            header_with_nonce = header + struct.pack('>Q', nonce)
            
            # Double SHA256
            block_hash = sha256_double(header_with_nonce)
            block_hash_int = int.from_bytes(block_hash, 'big')
            
            self.hashes_computed += 2  # Double SHA256 counts as 2 hashes
            
            # Check if we found a valid block
            if block_hash_int < target:
                return (True, nonce, block_hash)
        
        return (False, max_nonces, None)
    
    def get_stats(self) -> dict:
        """Get mining statistics"""
        return {
            'wallet': self.wallet,
            'hashes_computed': self.hashes_computed,
            'current_nonce': self.nonce,
        }


def demo_mining():
    """Demonstrate mining on simulated EDSAC 2"""
    print("EDSAC 2 RustChain Miner Demo")
    print("=" * 60)
    
    wallet = "RTC4325af95d26d59c3ef025963656d22af638bb96b"
    miner = EDSAC2Miner(wallet)
    
    # Sample block data
    prev_hash = bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000000")
    merkle_root = bytes.fromhex("4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b")
    timestamp = 1231006505  # Bitcoin genesis block timestamp
    difficulty = 1  # Minimum difficulty
    
    print(f"Wallet: {wallet}")
    print(f"Previous hash: {prev_hash.hex()}")
    print(f"Merkle root: {merkle_root.hex()}")
    print(f"Timestamp: {timestamp}")
    print(f"Difficulty: {difficulty}")
    print()
    print("Mining... (simulated EDSAC 2)")
    print()
    
    # Mine with limited nonces (EDSAC 2 is slow!)
    success, nonce, block_hash = miner.mine(
        prev_hash, merkle_root, timestamp, difficulty, max_nonces=100
    )
    
    stats = miner.get_stats()
    print(f"Hashes computed: {stats['hashes_computed']}")
    print(f"Nonces tried: {nonce}")
    
    if success:
        print(f"BLOCK FOUND!")
        print(f"  Nonce: {nonce}")
        print(f"  Block hash: {block_hash.hex()}")
    else:
        print(f"No block found in {nonce} attempts")
        print(f"  (EDSAC 2 would continue mining...)")
    
    print()
    print("Note: Real EDSAC 2 hardware would be much slower (~0.1-1 H/s)")
    print("      due to paper tape I/O and vacuum tube limitations.")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        # Run test vectors
        success = test_sha256()
        sys.exit(0 if success else 1)
    elif len(sys.argv) > 1 and sys.argv[1] == '--mine':
        # Run mining demo
        demo_mining()
    else:
        # Default: run tests
        test_sha256()
        print()
        demo_mining()
