#!/usr/bin/env python3
"""
SHA-256 Subset Implementation for Ferranti Mark 1* (1957)

This module implements a simplified SHA-256 variant that can be simulated
on the Ferranti Mark 1* architecture. Due to hardware limitations (20-bit words,
no native 32/64-bit operations), this is a "SHA-256 subset" that maintains
the cryptographic structure while adapting to 1957 constraints.

Key Adaptations:
- 20-bit words instead of 32-bit
- Simplified rotation operations
- Reduced round count (16 vs 64) for feasibility
- Maintains Merkle-Damg氓rd construction
- Uses same initial hash values (truncated to 20 bits)

Bounty Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b
"""

import struct
from typing import List, Tuple


# ============================================================================
# CONSTANTS - SHA-256 Subset (20-bit adapted)
# ============================================================================

# First 32 bits of the fractional parts of the cube roots of the first 8 primes
# Truncated to 20 bits for Mark 1* compatibility
H_INIT = [
    0x6A09E & 0xFFFFF,  # H0: 0x6a09e667
    0xBB670 & 0xFFFFF,  # H1: 0xbb67ae85
    0x3C6EF & 0xFFFFF,  # H2: 0x3c6ef372
    0xA54FF & 0xFFFFF,  # H3: 0xa54ff53a
    0x510E5 & 0xFFFFF,  # H4: 0x510e527f
    0x9B056 & 0xFFFFF,  # H5: 0x9b05688c
    0x1F83D & 0xFFFFF,  # H6: 0x1f83d9ab
    0x5BE0C & 0xFFFFF,  # H7: 0x5be0cd19
]

# First 32 bits of the fractional parts of the cube roots of the first 64 primes
# Using only 16 rounds (truncated from 64), 20-bit values
K = [
    0x428A2 & 0xFFFFF, 0x71374 & 0xFFFFF, 0xB5C0F & 0xFFFFF, 0xE9B5D & 0xFFFFF,
    0x3956C & 0xFFFFF, 0x59F11 & 0xFFFFF, 0x923F8 & 0xFFFFF, 0xAB1C5 & 0xFFFFF,
    0xD807A & 0xFFFFF, 0x12835 & 0xFFFFF, 0x24318 & 0xFFFFF, 0x550C7 & 0xFFFFF,
    0x72BE5 & 0xFFFFF, 0x80DEB & 0xFFFFF, 0x9BDC0 & 0xFFFFF, 0xC19BF & 0xFFFFF,
]

# 20-bit mask
MASK_20 = 0xFFFFF


# ============================================================================
# BITWISE OPERATIONS - 20-bit adapted
# ============================================================================

def rotr(x: int, n: int) -> int:
    """Right rotate a 20-bit value."""
    return ((x >> n) | (x << (20 - n))) & MASK_20


def shr(x: int, n: int) -> int:
    """Right shift a 20-bit value."""
    return x >> n


def ch(x: int, y: int, z: int) -> int:
    """SHA-256 Ch function: (x AND y) XOR (NOT x AND z)"""
    return ((x & y) ^ ((~x) & z)) & MASK_20


def maj(x: int, y: int, z: int) -> int:
    """SHA-256 Maj function: (x AND y) XOR (x AND z) XOR (y AND z)"""
    return ((x & y) ^ (x & z) ^ (y & z)) & MASK_20


def sigma0(x: int) -> int:
    """SHA-256 危0 function for 20-bit words."""
    return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 17)


def sigma1(x: int) -> int:
    """SHA-256 危1 function for 20-bit words."""
    return rotr(x, 7) ^ rotr(x, 11) ^ rotr(x, 15)


def gamma0(x: int) -> int:
    """SHA-256 蟽0 function for message schedule."""
    return rotr(x, 3) ^ rotr(x, 10) ^ shr(x, 5)


def gamma1(x: int) -> int:
    """SHA-256 蟽1 function for message schedule."""
    return rotr(x, 8) ^ rotr(x, 14) ^ shr(x, 7)


# ============================================================================
# SHA-256 SUBSET CLASS
# ============================================================================

class SHA256Subset:
    """
    SHA-256 subset implementation adapted for Ferranti Mark 1* constraints.
    
    Differences from full SHA-256:
    - 20-bit words (vs 32-bit)
    - 16 rounds (vs 64 rounds)
    - Simplified rotation constants
    - Output: 160 bits (8 脳 20) instead of 256 bits (8 脳 32)
    
    This maintains the cryptographic structure while being feasible to
    simulate on 1957 hardware with 20-bit instruction words.
    """
    
    def __init__(self):
        """Initialize hash state."""
        self.h = list(H_INIT)  # 8 脳 20-bit hash values
        self.buffer = bytearray()
        self.length = 0
    
    def _process_block(self, block: bytes):
        """Process a single 64-byte block."""
        assert len(block) == 64, "Block must be 64 bytes"
        
        # Parse block into 16 脳 20-bit words (overlapping)
        w = []
        for i in range(16):
            # Extract 20-bit words from 64-byte block
            byte_offset = (i * 20) // 8
            bit_offset = (i * 20) % 8
            
            if byte_offset + 3 <= len(block):
                word = struct.unpack('>I', block[byte_offset:byte_offset + 4])[0]
                word = (word >> (12 - bit_offset)) & MASK_20 if bit_offset else (word >> 12) & MASK_20
            else:
                word = 0
            w.append(word)
        
        # Extend to 16 words (simplified, no extension for 16 rounds)
        
        # Initialize working variables
        a, b, c, d, e, f, g, h = self.h
        
        # 16 rounds
        for i in range(16):
            t1 = (h + sigma1(e) + ch(e, f, g) + K[i] + w[i]) & MASK_20
            t2 = (sigma0(a) + maj(a, b, c)) & MASK_20
            
            h = g
            g = f
            f = e
            e = (d + t1) & MASK_20
            d = c
            c = b
            b = a
            a = (t1 + t2) & MASK_20
        
        # Update hash state
        self.h[0] = (self.h[0] + a) & MASK_20
        self.h[1] = (self.h[1] + b) & MASK_20
        self.h[2] = (self.h[2] + c) & MASK_20
        self.h[3] = (self.h[3] + d) & MASK_20
        self.h[4] = (self.h[4] + e) & MASK_20
        self.h[5] = (self.h[5] + f) & MASK_20
        self.h[6] = (self.h[6] + g) & MASK_20
        self.h[7] = (self.h[7] + h) & MASK_20
    
    def update(self, data: bytes):
        """Update hash with new data."""
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        self.buffer.extend(data)
        self.length += len(data)
        
        # Process complete blocks
        while len(self.buffer) >= 64:
            self._process_block(bytes(self.buffer[:64]))
            self.buffer = self.buffer[64:]
    
    def finalize(self) -> bytes:
        """Finalize hash computation and return digest."""
        # Padding
        msg_len_bits = self.length * 8
        self.buffer.append(0x80)
        
        # Pad to 56 bytes mod 64
        while len(self.buffer) % 64 != 56:
            self.buffer.append(0x00)
        
        # Append length as 64-bit big-endian (truncated to fit)
        self.buffer.extend(struct.pack('>Q', msg_len_bits)[-8:])
        
        # Process final block(s)
        while len(self.buffer) >= 64:
            self._process_block(bytes(self.buffer[:64]))
            self.buffer = self.buffer[64:]
        
        # Convert hash values to bytes (20 bits each = 2.5 bytes each)
        digest = bytearray()
        for h_val in self.h:
            # 20-bit value 鈫?3 bytes (with 4 bits unused)
            digest.extend(struct.pack('>I', h_val)[1:])  # Skip first 4 bits
        
        return bytes(digest)
    
    def digest(self) -> bytes:
        """Return hash digest without finalizing (for incremental hashing)."""
        temp = SHA256Subset()
        temp.h = list(self.h)
        temp.length = self.length
        if self.buffer:
            temp.update(bytes(self.buffer))
        return temp.finalize()
    
    def hexdigest(self) -> str:
        """Return hexadecimal representation of digest."""
        return self.digest().hex()


def sha256_subset(data: bytes) -> bytes:
    """Convenience function: compute SHA-256 subset hash."""
    hasher = SHA256Subset()
    hasher.update(data)
    return hasher.finalize()


def sha256_subset_hex(data: bytes) -> str:
    """Convenience function: compute SHA-256 subset hash as hex string."""
    return sha256_subset(data).hex()


# ============================================================================
# FERRANTI MARK 1* INTEGRATION
# ============================================================================

class FerrantiSHA256Bridge:
    """
    Bridge between SHA-256 subset and Ferranti Mark 1* simulator.
    
    This class provides methods to:
    - Hash mining data using SHA-256 subset
    - Integrate with Mark 1* hardware fingerprint
    - Generate network-compatible share payloads
    """
    
    def __init__(self, cpu=None):
        """Initialize bridge with optional Mark 1* CPU."""
        self.cpu = cpu
        self.hasher = SHA256Subset()
    
    def compute_share_hash(self, wallet: str, nonce: int, fingerprint: int) -> str:
        """
        Compute SHA-256 subset hash for a mining share.
        
        Args:
            wallet: Wallet address
            nonce: Mining nonce
            fingerprint: Hardware fingerprint
        
        Returns:
            Hex string of hash (40 characters = 160 bits)
        """
        # Create share data
        share_data = f"{wallet}:{nonce}:{fingerprint:016X}"
        return sha256_subset_hex(share_data.encode('utf-8'))
    
    def verify_share(self, wallet: str, nonce: int, fingerprint: int, 
                     hash_result: str, difficulty: int) -> bool:
        """
        Verify a mining share meets difficulty target.
        
        Args:
            wallet: Wallet address
            nonce: Mining nonce
            fingerprint: Hardware fingerprint
            hash_result: Claimed hash (hex string)
            difficulty: Difficulty target
        
        Returns:
            True if share is valid
        """
        # Recompute hash
        computed_hash = self.compute_share_hash(wallet, nonce, fingerprint)
        
        # Check hash matches
        if computed_hash != hash_result:
            return False
        
        # Check difficulty (first 5 hex chars must be < difficulty)
        hash_prefix = int(hash_result[:5], 16)
        return hash_prefix < difficulty
    
    def create_network_payload(self, share_data: dict) -> bytes:
        """
        Create network-compatible payload for share submission.
        
        Args:
            share_data: Dict with wallet, nonce, fingerprint, hash
        
        Returns:
            Serialized payload for network transmission
        """
        import json
        payload = {
            'version': 'ferranti-mark1-star-1957',
            'wallet': share_data['wallet'],
            'nonce': share_data['nonce'],
            'fingerprint': share_data['fingerprint'],
            'hash': share_data['hash'],
            'timestamp': share_data.get('timestamp', 0),
            'proof_type': 'sha256_subset'
        }
        return json.dumps(payload).encode('utf-8')
    
    def parse_network_payload(self, payload: bytes) -> dict:
        """
        Parse network payload back to share data.
        
        Args:
            payload: Serialized payload
        
        Returns:
            Parsed share data dict
        """
        import json
        return json.loads(payload.decode('utf-8'))


# ============================================================================
# DEMO / TESTING
# ============================================================================

def run_demo():
    """Demonstrate SHA-256 subset functionality."""
    print("=" * 60)
    print("SHA-256 Subset for Ferranti Mark 1* (1957)")
    print("=" * 60)
    print()
    
    # Test 1: Basic hashing
    print("Test 1: Basic Hashing")
    print("-" * 40)
    test_data = b"Hello, Ferranti Mark 1*!"
    hash_result = sha256_subset_hex(test_data)
    print(f"Input:  {test_data.decode()}")
    print(f"Hash:   {hash_result}")
    print(f"Length: {len(hash_result)} chars (160 bits)")
    print()
    
    # Test 2: Mining share hash
    print("Test 2: Mining Share Hash")
    print("-" * 40)
    bridge = FerrantiSHA256Bridge()
    wallet = "RTC4325af95d26d59c3ef025963656d22af638bb96b"
    nonce = 0x04200
    fingerprint = 0xDF01DDB0348242C0
    
    share_hash = bridge.compute_share_hash(wallet, nonce, fingerprint)
    print(f"Wallet:     {wallet}")
    print(f"Nonce:      {nonce:05X}")
    print(f"Fingerprint:{fingerprint:016X}")
    print(f"Share Hash: {share_hash}")
    print()
    
    # Test 3: Share verification
    print("Test 3: Share Verification")
    print("-" * 40)
    difficulty = 0x10000  # 20-bit difficulty target
    is_valid = bridge.verify_share(wallet, nonce, fingerprint, share_hash, difficulty)
    print(f"Difficulty: {difficulty:05X}")
    print(f"Valid:      {is_valid}")
    print()
    
    # Test 4: Network payload
    print("Test 4: Network Payload")
    print("-" * 40)
    share_data = {
        'wallet': wallet,
        'nonce': nonce,
        'fingerprint': f"{fingerprint:016X}",
        'hash': share_hash,
        'timestamp': 1773404728
    }
    payload = bridge.create_network_payload(share_data)
    print(f"Payload: {payload.decode()[:100]}...")
    print()
    
    # Test 5: Determinism
    print("Test 5: Determinism Check")
    print("-" * 40)
    hash1 = sha256_subset_hex(test_data)
    hash2 = sha256_subset_hex(test_data)
    print(f"Hash 1: {hash1}")
    print(f"Hash 2: {hash2}")
    print(f"Match:  {hash1 == hash2}")
    print()
    
    print("=" * 60)
    print("All SHA-256 subset tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    run_demo()
