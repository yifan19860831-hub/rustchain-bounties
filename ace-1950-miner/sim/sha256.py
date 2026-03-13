#!/usr/bin/env python3
"""
SHA-256 Implementation for ACE (1950)

This module provides:
1. Reference SHA-256 implementation in Python
2. ACE assembly code generation for SHA-256 core
3. Test vectors for verification

Note: Full SHA-256 on ACE is challenging due to:
- 32-bit word size (matches SHA-256 perfectly!)
- No hardware multiplication (must use software)
- Limited memory (128-352 words)
- Serial delay line access

The implementation focuses on the core compression function.
"""

import struct

# SHA-256 constants (first 32 bits of fractional parts of cube roots of primes)
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
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
]

# Initial hash values (first 32 bits of fractional parts of square roots of first 8 primes)
H_INIT = [
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19,
]


def rotr(x, n):
    """Right rotate 32-bit value"""
    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF


def sha256_compress(state, block):
    """
    SHA-256 compression function.
    
    Args:
        state: 8 × 32-bit hash state
        block: 16 × 32-bit message schedule
    
    Returns:
        New 8 × 32-bit hash state
    """
    # Extend message schedule from 16 to 64 words
    w = list(block)
    for i in range(16, 64):
        s0 = rotr(w[i-15], 7) ^ rotr(w[i-15], 18) ^ (w[i-15] >> 3)
        s1 = rotr(w[i-2], 17) ^ rotr(w[i-2], 19) ^ (w[i-2] >> 10)
        w.append((w[i-16] + s0 + w[i-7] + s1) & 0xFFFFFFFF)
    
    # Initialize working variables
    a, b, c, d, e, f, g, h = state
    
    # 64 rounds
    for i in range(64):
        S1 = rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25)
        ch = (e & f) ^ ((~e) & g)
        temp1 = (h + S1 + ch + K[i] + w[i]) & 0xFFFFFFFF
        S0 = rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22)
        maj = (a & b) ^ (a & c) ^ (b & c)
        temp2 = (S0 + maj) & 0xFFFFFFFF
        
        h = g
        g = f
        f = e
        e = (d + temp1) & 0xFFFFFFFF
        d = c
        c = b
        b = a
        a = (temp1 + temp2) & 0xFFFFFFFF
    
    # Add compressed chunk to current hash value
    return [
        (state[0] + a) & 0xFFFFFFFF,
        (state[1] + b) & 0xFFFFFFFF,
        (state[2] + c) & 0xFFFFFFFF,
        (state[3] + d) & 0xFFFFFFFF,
        (state[4] + e) & 0xFFFFFFFF,
        (state[5] + f) & 0xFFFFFFFF,
        (state[6] + g) & 0xFFFFFFFF,
        (state[7] + h) & 0xFFFFFFFF,
    ]


def sha256(message):
    """
    Compute SHA-256 hash of a message.
    
    Args:
        message: bytes or string
    
    Returns:
        32-byte hash digest
    """
    if isinstance(message, str):
        message = message.encode('utf-8')
    
    # Pre-processing: add padding
    msg_len = len(message)
    message += b'\x80'
    message += b'\x00' * ((55 - msg_len) % 64)
    message += struct.pack('>Q', msg_len * 8)
    
    # Process each 512-bit block
    state = list(H_INIT)
    for i in range(0, len(message), 64):
        block = struct.unpack('>16I', message[i:i+64])
        state = sha256_compress(state, block)
    
    # Produce final hash value
    return struct.pack('>8I', *state)


def sha256_hex(message):
    """Compute SHA-256 and return as hex string"""
    return sha256(message).hex()


# Test vectors
TEST_VECTORS = [
    ("", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    ("abc", "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"),
    ("hello world", "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"),
    ("The quick brown fox jumps over the lazy dog", 
     "d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592"),
]


def test_sha256():
    """Test SHA-256 implementation against known vectors"""
    print("=" * 60)
    print("SHA-256 Test Vectors")
    print("=" * 60)
    
    all_pass = True
    for message, expected in TEST_VECTORS:
        result = sha256_hex(message)
        status = "PASS" if result == expected else "FAIL"
        if result != expected:
            all_pass = False
        print(f"\nInput: '{message}'")
        print(f"Expected: {expected}")
        print(f"Got:      {result}")
        print(f"Status:   {status}")
    
    print("\n" + "=" * 60)
    print(f"Overall: {'ALL TESTS PASSED' if all_pass else 'SOME TESTS FAILED'}")
    print("=" * 60)
    
    return all_pass


def generate_ace_assembly():
    """
    Generate ACE assembly code for SHA-256 round function.
    
    This is a simplified version that demonstrates the approach.
    Full implementation would need optimization for delay line timing.
    """
    assembly = """
; ACE SHA-256 Round Function
; Simplified implementation for demonstration
; 
; Memory layout:
;   0x00-0x1F: System
;   0x20-0x3F: Hash state (H0-H7)
;   0x40-0x7F: Message schedule (W0-W15)
;   0x80-0xFF: Working variables

; Constants (stored in delay line)
K_VALUES:
    DC 0x428a2f98  ; K[0]
    DC 0x71374491  ; K[1]
    DC 0xb5c0fbcf  ; K[2]
    ; ... more constants

; SHA-256 Round Macro (one round)
; Input: a,b,c,d,e,f,g,h in accumulators
;        K[i] and W[i] in memory
SHA256_ROUND:
    ; S1 = rotr(e,6) ^ rotr(e,11) ^ rotr(e,25)
    LD  E_REG          ; Load e
    RSH 6              ; Rotate right 6
    ST  TEMP1
    LD  E_REG
    RSH 11
    XOR TEMP1
    LD  E_REG
    RSH 25
    XOR TEMP1
    ST  S1
    
    ; ch = (e & f) ^ ((~e) & g)
    LD  E_REG
    AND F_REG
    ST  TEMP2
    LD  E_REG
    NOT
    AND G_REG
    XOR TEMP2
    ST  CH
    
    ; temp1 = h + S1 + ch + K[i] + W[i]
    LD  H_REG
    ADD S1
    ADD CH
    ADD K_I
    ADD W_I
    ST  TEMP1
    
    ; S0 = rotr(a,2) ^ rotr(a,13) ^ rotr(a,22)
    LD  A_REG
    RSH 2
    ST  TEMP3
    LD  A_REG
    RSH 13
    XOR TEMP3
    LD  A_REG
    RSH 22
    XOR TEMP3
    ST  S0
    
    ; maj = (a & b) ^ (a & c) ^ (b & c)
    LD  A_REG
    AND B_REG
    ST  TEMP4
    LD  A_REG
    AND C_REG
    XOR TEMP4
    LD  B_REG
    AND C_REG
    XOR TEMP4
    ST  MAJ
    
    ; temp2 = S0 + maj
    LD  S0
    ADD MAJ
    ST  TEMP2
    
    ; Update working variables
    ; h = g, g = f, f = e, e = d + temp1
    LD  G_REG
    ST  H_REG
    LD  F_REG
    ST  G_REG
    LD  E_REG
    ST  F_REG
    LD  D_REG
    ADD TEMP1
    ST  E_REG
    
    ; d = c, c = b, b = a, a = temp1 + temp2
    LD  C_REG
    ST  D_REG
    LD  B_REG
    ST  C_REG
    LD  A_REG
    ST  B_REG
    LD  TEMP1
    ADD TEMP2
    ST  A_REG
    
    JMP NEXT_ROUND
"""
    return assembly


def estimate_ace_resources():
    """Estimate ACE resources needed for SHA-256"""
    print("\n" + "=" * 60)
    print("ACE Resource Estimation for SHA-256")
    print("=" * 60)
    
    resources = {
        "Memory for constants (K)": "64 words",
        "Memory for hash state (H)": "8 words",
        "Memory for message schedule (W)": "64 words",
        "Memory for working variables": "8 words",
        "Total memory required": "~144 words",
        "ACE memory (original)": "128 words",
        "ACE memory (expanded)": "352 words",
        "Feasible?": "Yes (with expanded memory)",
    }
    
    for item, value in resources.items():
        print(f"  {item:35} {value}")
    
    print("\nNote: ACE originally had 128 words, expanded to 352.")
    print("SHA-256 requires careful memory management on ACE.")
    print("=" * 60)


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("   SHA-256 for ACE (1950)")
    print("   Alan Turing's Computer")
    print("=" * 60)
    
    # Run tests
    test_sha256()
    
    # Show resource estimation
    estimate_ace_resources()
    
    # Generate assembly example
    print("\n" + "=" * 60)
    print("ACE Assembly Code Example (SHA-256 Round)")
    print("=" * 60)
    print(generate_ace_assembly())
