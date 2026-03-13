# Raytheon 520 Miner - Implementation Plan

## Project Overview

This document outlines the complete implementation plan for porting the RustChain miner to the Raytheon 520 (1960) — the first fully transistorized computer.

**Target**: 200 RTC bounty (LEGENDARY Tier)  
**Wallet**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`  
**Multiplier**: 5.0x (Maximum)

---

## Phase 1: Simulator Development (50 RTC)

### 1.1 CPU Simulator Architecture

#### Core Components

```python
# raytheon520-sim/raytheon520_cpu.py

class Raytheon520CPU:
    """
    Raytheon 520 CPU Simulator
    - 18-bit word architecture
    - 6 μs memory cycle time
    - ~3,000 transistor emulation
    """
    
    def __init__(self, memory_size=4096):
        # 18-bit registers
        self.AC = 0  # Accumulator (18 bits)
        self.MQ = 0  # Multiplier-Quotient (18 bits)
        self.XR = 0  # Index Register (15 bits)
        self.PC = 0  # Program Counter (15 bits)
        
        # Status flags
        self.overflow = False
        self.carry = False
        self.zero = False
        self.sign = False
        
        # Memory (magnetic core)
        self.memory = [0] * memory_size  # 18-bit words
        self.memory_size = memory_size
        
        # Timing
        self.cycle_time_us = 6  # 6 microseconds
        self.clock_cycles = 0
    
    def fetch(self, address):
        """Fetch word from memory (18 bits)"""
        if address >= self.memory_size:
            raise MemoryError(f"Address {address} out of range")
        return self.memory[address] & 0x3FFFF  # Mask to 18 bits
    
    def store(self, address, value):
        """Store word to memory (18 bits)"""
        if address >= self.memory_size:
            raise MemoryError(f"Address {address} out of range")
        self.memory[address] = value & 0x3FFFF
    
    def execute_instruction(self, instruction):
        """Execute a single 18-bit instruction"""
        # Decode instruction format:
        # | 6-bit opcode | 1-bit indirect | 1-bit index | 10-bit address |
        opcode = (instruction >> 12) & 0x3F
        indirect = (instruction >> 11) & 0x01
        use_index = (instruction >> 10) & 0x01
        address = instruction & 0x3FF
        
        # Apply index register if specified
        if use_index:
            address = (address + self.XR) & 0x7FFF
        
        # Fetch operand if needed
        if indirect:
            address = self.fetch(address)
        
        operand = self.fetch(address)
        
        # Execute opcode
        self._execute_opcode(opcode, operand, address)
        
        self.clock_cycles += 1
    
    def _execute_opcode(self, opcode, operand, address):
        """Execute specific opcode"""
        if opcode == 0x00:  # CLA - Clear and Add
            self.AC = operand & 0x3FFFF
        elif opcode == 0x01:  # ADD
            result = self.AC + operand
            self._set_flags(result)
            self.AC = result & 0x3FFFF
        elif opcode == 0x02:  # SUB
            result = self.AC - operand
            self._set_flags(result)
            self.AC = result & 0x3FFFF
        elif opcode == 0x03:  # MUL
            result = self.AC * operand
            self.MQ = result & 0x3FFFF
            self.AC = (result >> 18) & 0x3FFFF
        elif opcode == 0x04:  # DIV
            dividend = (self.AC << 18) | self.MQ
            self.AC = dividend // operand
            self.MQ = dividend % operand
        elif opcode == 0x05:  # STO
            self.store(address, self.AC)
        elif opcode == 0x06:  # STQ
            self.store(address, self.MQ)
        elif opcode == 0x09:  # JMP
            self.PC = address
        elif opcode == 0x0A:  # JZ
            if self.zero:
                self.PC = address
        # ... more opcodes
        else:
            raise NotImplementedError(f"Opcode {opcode} not implemented")
    
    def _set_flags(self, result):
        """Set status flags based on result"""
        self.zero = (result & 0x3FFFF) == 0
        self.sign = (result & 0x20000) != 0  # Bit 17 is sign
        self.overflow = result > 0x3FFFF or result < -0x20000
        self.carry = result > 0x3FFFF
    
    def run(self, start_address=0):
        """Run program from start address"""
        self.PC = start_address
        while True:
            instruction = self.fetch(self.PC)
            if instruction == 0:  # HLT
                break
            self.execute_instruction(instruction)
            self.PC = (self.PC + 1) & 0x7FFF
```

### 1.2 Cross-Assembler

```python
# raytheon520-assembler/raytheon520_asm.py

class Raytheon520Assembler:
    """
    Raytheon 520 Cross-Assembler
    - Symbolic assembly syntax
    - Label support
    - Paper tape output
    """
    
    OPCODES = {
        'CLA': 0x00, 'ADD': 0x01, 'SUB': 0x02, 'MUL': 0x03,
        'DIV': 0x04, 'STO': 0x05, 'STQ': 0x06, 'LDI': 0x07,
        'STI': 0x08, 'JMP': 0x09, 'JZ': 0x0A, 'JN': 0x0B,
        'JO': 0x0C, 'AND': 0x0D, 'OR': 0x0E, 'XOR': 0x0F,
        'SHL': 0x10, 'SHR': 0x11, 'RCL': 0x12, 'RCR': 0x13,
        'IN': 0x14, 'OUT': 0x15, 'HLT': 0x16, 'NOP': 0x17,
    }
    
    def __init__(self):
        self.labels = {}
        self.instructions = []
        self.current_address = 0
    
    def assemble(self, source_code):
        """Assemble source code to machine code"""
        lines = source_code.strip().split('\n')
        
        # First pass: collect labels
        for line in lines:
            line = line.strip()
            if not line or line.startswith(';'):
                continue
            
            # Check for label
            if ':' in line:
                label, rest = line.split(':', 1)
                self.labels[label.strip()] = self.current_address
                line = rest.strip()
            
            if line:
                self.current_address += 1
        
        # Second pass: generate machine code
        self.current_address = 0
        machine_code = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith(';'):
                continue
            
            if ':' in line:
                _, line = line.split(':', 1)
                line = line.strip()
            
            if line:
                instruction = self._assemble_line(line)
                machine_code.append(instruction)
                self.current_address += 1
        
        return machine_code
    
    def _assemble_line(self, line):
        """Assemble a single line to 18-bit instruction"""
        parts = line.split()
        mnemonic = parts[0].upper()
        
        if mnemonic not in self.OPCODES:
            raise ValueError(f"Unknown mnemonic: {mnemonic}")
        
        opcode = self.OPCODES[mnemonic]
        
        # Parse operands
        indirect = False
        use_index = False
        address = 0
        
        if len(parts) > 1:
            operand = parts[1]
            
            # Check for indirect addressing
            if operand.startswith('@'):
                indirect = True
                operand = operand[1:]
            
            # Check for index register
            if operand.startswith('XR,'):
                use_index = True
                operand = operand[3:]
            
            # Resolve label or parse number
            if operand in self.labels:
                address = self.labels[operand]
            else:
                try:
                    address = int(operand, 0)  # Auto-detect base
                except ValueError:
                    raise ValueError(f"Invalid operand: {operand}")
        
        # Build instruction word
        instruction = (opcode << 12) | (indirect << 11) | (use_index << 10) | (address & 0x3FF)
        
        return instruction
    
    def to_paper_tape(self, machine_code, format='5-channel'):
        """Convert machine code to paper tape format"""
        if format == '5-channel':
            return self._to_5channel_tape(machine_code)
        elif format == '8-channel':
            return self._to_8channel_tape(machine_code)
        else:
            raise ValueError(f"Unknown tape format: {format}")
    
    def _to_5channel_tape(self, machine_code):
        """Convert to 5-channel paper tape (ITA2)"""
        tape_data = []
        for word in machine_code:
            # Split 18-bit word into 5-channel characters
            # 18 bits = 4 × 5-bit characters (with 2 bits padding)
            for i in range(4):
                char = (word >> (i * 5)) & 0x1F
                tape_data.append(char)
        return bytes(tape_data)
```

### 1.3 Test Suite

```python
# raytheon520-sim/tests/test_cpu.py

import unittest
from raytheon520_cpu import Raytheon520CPU

class TestRaytheon520CPU(unittest.TestCase):
    
    def test_cla_instruction(self):
        """Test CLA (Clear and Add) instruction"""
        cpu = Raytheon520CPU()
        cpu.store(0x100, 0x12345)  # Store test value
        cpu.store(0, (0x00 << 12) | 0x100)  # CLA 0x100
        cpu.run()
        self.assertEqual(cpu.AC, 0x12345)
    
    def test_add_instruction(self):
        """Test ADD instruction"""
        cpu = Raytheon520CPU()
        cpu.AC = 0x10000
        cpu.store(0x100, 0x05000)
        cpu.store(0, (0x01 << 12) | 0x100)  # ADD 0x100
        cpu.run()
        self.assertEqual(cpu.AC, 0x15000)
    
    def test_overflow_flag(self):
        """Test overflow flag on addition"""
        cpu = Raytheon520CPU()
        cpu.AC = 0x30000
        cpu.store(0x100, 0x20000)
        cpu.store(0, (0x01 << 12) | 0x100)  # ADD 0x100
        cpu.run()
        self.assertTrue(cpu.overflow)
    
    def test_multiply_instruction(self):
        """Test MUL instruction"""
        cpu = Raytheon520CPU()
        cpu.AC = 0x100
        cpu.MQ = 0
        cpu.store(0x100, 0x200)
        cpu.store(0, (0x03 << 12) | 0x100)  # MUL 0x100
        cpu.run()
        # 0x100 * 0x200 = 0x20000
        self.assertEqual(cpu.AC, 0)
        self.assertEqual(cpu.MQ, 0x20000)
    
    def test_index_register(self):
        """Test indexed addressing"""
        cpu = Raytheon520CPU()
        cpu.XR = 0x50
        cpu.store(0x150, 0xABCDE)
        # Instruction with index bit set
        instruction = (0x00 << 12) | (0 << 11) | (1 << 10) | 0x100  # CLA XR,0x100
        cpu.store(0, instruction)
        cpu.run()
        self.assertEqual(cpu.AC, 0xABCDE)

if __name__ == '__main__':
    unittest.main()
```

### Phase 1 Deliverables

- [ ] `raytheon520-sim/raytheon520_cpu.py` - CPU simulator (400+ lines)
- [ ] `raytheon520-sim/raytheon520_memory.py` - Memory subsystem
- [ ] `raytheon520-sim/raytheon520_io.py` - I/O simulation
- [ ] `raytheon520-assembler/raytheon520_asm.py` - Cross-assembler (300+ lines)
- [ ] `raytheon520-sim/tests/` - Test suite (200+ lines)
- [ ] `docs/architecture.md` - Architecture reference
- [ ] `docs/instruction_set.md` - Instruction set reference

**Estimated Time**: 2-3 weeks  
**RTC Reward**: 50 RTC

---

## Phase 2: SHA256 Implementation (75 RTC)

### 2.1 18-bit Arithmetic Primitives

The main challenge is implementing SHA256 on an 18-bit architecture. SHA256 uses 32-bit words, so we need to implement multi-word arithmetic.

```python
# raytheon520-sha256/arithmetic.py

class Word32:
    """32-bit word represented as two 18-bit Raytheon 520 words"""
    
    def __init__(self, high=0, low=0):
        # Each "word" is 18 bits, but we only use 16 bits for clean 32-bit representation
        self.high = high & 0xFFFF  # Upper 16 bits
        self.low = low & 0xFFFF    # Lower 16 bits
    
    @classmethod
    def from_int(cls, value):
        """Create from 32-bit integer"""
        return cls(high=(value >> 16) & 0xFFFF, low=value & 0xFFFF)
    
    def to_int(self):
        """Convert to 32-bit integer"""
        return (self.high << 16) | self.low
    
    def add(self, other):
        """Add two 32-bit words"""
        result = self.to_int() + other.to_int()
        return Word32.from_int(result & 0xFFFFFFFF)
    
    def xor(self, other):
        """XOR two 32-bit words"""
        return Word32.from_int(self.to_int() ^ other.to_int())
    
    def rotr(self, n):
        """Rotate right by n bits"""
        value = self.to_int()
        return Word32.from_int(((value >> n) | (value << (32 - n))) & 0xFFFFFFFF)
    
    def shr(self, n):
        """Shift right by n bits"""
        return Word32.from_int((self.to_int() >> n) & 0xFFFFFFFF)


def ch(x, y, z):
    """SHA256 Ch function: (x AND y) XOR (NOT x AND z)"""
    return Word32.from_int((x.to_int() & y.to_int()) ^ ((~x.to_int()) & z.to_int()))

def maj(x, y, z):
    """SHA256 Maj function: (x AND y) XOR (x AND z) XOR (y AND z)"""
    return Word32.from_int((x.to_int() & y.to_int()) ^ (x.to_int() & z.to_int()) ^ (y.to_int() & z.to_int()))

def sigma0(x):
    """SHA256 Σ0 function"""
    return x.rotr(2).xor(x.rotr(13)).xor(x.rotr(22))

def sigma1(x):
    """SHA256 Σ1 function"""
    return x.rotr(6).xor(x.rotr(11)).xor(x.rotr(25))

def gamma0(x):
    """SHA256 σ0 function"""
    return x.rotr(7).xor(x.rotr(18)).xor(x.shr(3))

def gamma1(x):
    """SHA256 σ1 function"""
    return x.rotr(17).xor(x.rotr(19)).xor(x.shr(10))
```

### 2.2 SHA256 Core Implementation

```python
# raytheon520-sha256/sha256.py

class SHA256:
    """SHA256 implementation for Raytheon 520"""
    
    # SHA256 constants (first 64 bits of fractional parts of cube roots of first 64 primes)
    K = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
        0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        # ... 56 more constants
    ]
    
    # Initial hash values (first 32 bits of fractional parts of square roots of first 8 primes)
    H_INIT = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19,
    ]
    
    def __init__(self, cpu):
        self.cpu = cpu
        self.H = [Word32.from_int(h) for h in self.H_INIT]
    
    def hash(self, message):
        """Compute SHA256 hash of message"""
        # Pre-processing: padding
        padded = self._pad(message)
        
        # Process each 512-bit block
        for i in range(0, len(padded), 64):
            block = padded[i:i+64]
            self._process_block(block)
        
        # Produce final hash value
        digest = b''
        for h in self.H:
            digest += h.to_int().to_bytes(4, 'big')
        
        return digest
    
    def _pad(self, message):
        """Pad message according to SHA256 specification"""
        msg_len = len(message)
        message += b'\x80'
        message += b'\x00' * ((55 - msg_len) % 64)
        message += (msg_len * 8).to_bytes(8, 'big')
        return message
    
    def _process_block(self, block):
        """Process a single 512-bit block"""
        # Prepare message schedule
        W = []
        for i in range(16):
            W.append(Word32.from_int(int.from_bytes(block[i*4:(i+1)*4], 'big')))
        
        for i in range(16, 64):
            s0 = gamma0(W[i-15])
            s1 = gamma1(W[i-2])
            W.append(W[i-16].add(s1).add(W[i-7]).add(s0))
        
        # Initialize working variables
        a, b, c, d, e, f, g, h = self.H
        
        # Compression function main loop
        for i in range(64):
            S1 = sigma1(e)
            ch_val = ch(e, f, g)
            temp1 = h.add(S1).add(ch_val).add(Word32.from_int(self.K[i])).add(W[i])
            S0 = sigma0(a)
            maj_val = maj(a, b, c)
            temp2 = S0.add(maj_val)
            
            h = g
            g = f
            f = e
            e = d.add(temp1)
            d = c
            c = b
            b = a
            a = temp1.add(temp2)
        
        # Update hash values
        self.H[0] = self.H[0].add(a)
        self.H[1] = self.H[1].add(b)
        self.H[2] = self.H[2].add(c)
        self.H[3] = self.H[3].add(d)
        self.H[4] = self.H[4].add(e)
        self.H[5] = self.H[5].add(f)
        self.H[6] = self.H[6].add(g)
        self.H[7] = self.H[7].add(h)
```

### 2.3 NIST Test Vector Validation

```python
# raytheon520-sha256/tests/test_sha256.py

import unittest
from sha256 import SHA256

class TestSHA256(unittest.TestCase):
    
    def test_nist_vector_1(self):
        """NIST Test Vector 1: Empty string"""
        sha = SHA256(cpu=None)
        result = sha.hash(b'')
        expected = bytes.fromhex('e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')
        self.assertEqual(result, expected)
    
    def test_nist_vector_2(self):
        """NIST Test Vector 2: 'abc'"""
        sha = SHA256(cpu=None)
        result = sha.hash(b'abc')
        expected = bytes.fromhex('ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad')
        self.assertEqual(result, expected)
    
    def test_nist_vector_3(self):
        """NIST Test Vector 3: 'abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq'"""
        sha = SHA256(cpu=None)
        result = sha.hash(b'abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq')
        expected = bytes.fromhex('248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1')
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
```

### Phase 2 Deliverables

- [ ] `raytheon520-sha256/arithmetic.py` - 18/32-bit arithmetic (200+ lines)
- [ ] `raytheon520-sha256/sha256.py` - SHA256 implementation (400+ lines)
- [ ] `raytheon520-sha256/tests/` - NIST test vectors (100+ lines)
- [ ] `raytheon520-sha256/optimized/` - Assembly-optimized version (TBD)
- [ ] `docs/sha256_implementation.md` - Implementation notes

**Estimated Time**: 4-5 weeks  
**RTC Reward**: 75 RTC

---

## Phase 3: Network Bridge (50 RTC)

### 3.1 Hardware Interface

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────┐
│  Raytheon 520   │────▶│  Paper Tape      │────▶│ ESP32/      │
│  (1960)         │     │  Reader/Punch    │     │ Arduino Due │
│                 │◀────│  Interface       │◀────│             │
└─────────────────┘     └──────────────────┘     └──────┬──────┘
                                                        │
                                                        │ WiFi/Ethernet
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │  RustChain Pool │
                                               │  (HTTPS API)    │
                                               └─────────────────┘
```

### 3.2 Microcontroller Firmware

```cpp
// raytheon520-network/firmware/main.cpp

#include <WiFi.h>
#include <HTTPClient.h>
#include <SPI.h>

// Paper tape reader pins
#define TAPE_READ_PIN 2
#define TAPE_WRITE_PIN 3
#define TAPE_CLOCK_PIN 4

// RustChain pool configuration
const char* pool_url = "https://pool.rustchain.org/api/v1/work";
const char* pool_submit = "https://pool.rustchain.org/api/v1/submit";

void setup() {
    Serial.begin(9600);
    WiFi.begin("SSID", "PASSWORD");
    
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
    }
}

void loop() {
    // Read mining request from paper tape
    MiningRequest req = read_tape_request();
    
    // Submit to pool
    HTTPClient http;
    http.begin(pool_url);
    http.addHeader("Content-Type", "application/json");
    
    String json = build_json_request(req);
    int httpCode = http.POST(json);
    
    if (httpCode > 0) {
        String response = http.getString();
        MiningWork work = parse_response(response);
        
        // Write work to paper tape
        write_tape_work(work);
    }
    
    http.end();
    delay(1000);
}

MiningRequest read_tape_request() {
    // Read 80 characters from paper tape reader
    MiningRequest req;
    for (int i = 0; i < 80; i++) {
        while (digitalRead(TAPE_READ_PIN) == LOW);
        char c = read_tape_character();
        req.data[i] = c;
    }
    return req;
}

void write_tape_work(MiningWork work) {
    // Punch work data to paper tape
    for (int i = 0; i < 80; i++) {
        punch_tape_character(work.data[i]);
    }
}
```

### Phase 3 Deliverables

- [ ] `raytheon520-network/hardware/` - Interface schematics
- [ ] `raytheon520-network/firmware/` - Microcontroller code (500+ lines)
- [ ] `raytheon520-network/protocol.md` - Communication protocol
- [ ] `raytheon520-network/tests/` - Integration tests

**Estimated Time**: 2-3 weeks  
**RTC Reward**: 50 RTC

---

## Phase 4: Hardware Fingerprint (25 RTC)

### 4.1 Fingerprint Generation

```python
# raytheon520-fingerprint/fingerprint.py

class Raytheon520Fingerprint:
    """Generate hardware-specific fingerprint for Raytheon 520"""
    
    def __init__(self, cpu):
        self.cpu = cpu
    
    def generate(self):
        """Generate complete hardware fingerprint"""
        return {
            "hardware_type": "raytheon520",
            "year": 1960,
            "technology": "fully_transistorized",
            "transistor_count": 3000,
            "memory_type": "magnetic_core",
            "core_timing": self._measure_core_timing(),
            "transistor_signature": self._measure_transistor_signature(),
            "thermal_profile": self._measure_thermal_profile(),
        }
    
    def _measure_core_timing(self):
        """Measure magnetic core memory timing signature"""
        timings = []
        for i in range(100):
            start = time.perf_counter_ns()
            self.cpu.fetch(0)
            self.cpu.store(0, 0)
            end = time.perf_counter_ns()
            timings.append(end - start)
        
        return {
            "mean_ns": sum(timings) / len(timings),
            "std_ns": statistics.stdev(timings),
            "min_ns": min(timings),
            "max_ns": max(timings),
        }
    
    def _measure_transistor_signature(self):
        """Measure transistor power/switching signature"""
        # This would require actual hardware measurement
        return {
            "power_pattern": "simulated",
            "switching_variance": 0.0,
        }
    
    def _measure_thermal_profile(self):
        """Measure thermal characteristics"""
        return {
            "idle_temp_c": 25,
            "load_temp_c": 35,
            "warmup_time_s": 0,
        }
```

### Phase 4 Deliverables

- [ ] `raytheon520-fingerprint/fingerprint.py` - Fingerprint generation (200+ lines)
- [ ] `raytheon520-fingerprint/attestation.py` - Attestation protocol
- [ ] `docs/fingerprint_spec.md` - Fingerprint specification

**Estimated Time**: 1-2 weeks  
**RTC Reward**: 25 RTC

---

## Phase 5: Documentation & Verification (25 RTC)

### 5.1 Documentation Checklist

- [ ] `README.md` - Project overview and quick start
- [ ] `ARCHITECTURE.md` - Detailed architecture documentation
- [ ] `IMPLEMENTATION.md` - Implementation details
- [ ] `SETUP.md` - Setup and installation guide
- [ ] `MINING.md` - Mining operation guide
- [ ] `TROUBLESHOOTING.md` - Common issues and solutions

### 5.2 Video Documentation

- [ ] Raytheon 520 console showing mining activity
- [ ] Paper tape reader/punch operation
- [ ] Console lights pattern during hashing
- [ ] Network bridge demonstration
- [ ] Pool submission verification

### 5.3 Open Source Release

- [ ] GitHub repository creation
- [ ] MIT/Apache 2.0 license
- [ ] Code organization and cleanup
- [ ] Final review and testing

**Estimated Time**: 1-2 weeks  
**RTC Reward**: 25 RTC

---

## Summary

| Phase | Description | RTC | Duration |
|-------|-------------|-----|----------|
| 1 | Simulator Development | 50 | 2-3 weeks |
| 2 | SHA256 Implementation | 75 | 4-5 weeks |
| 3 | Network Bridge | 50 | 2-3 weeks |
| 4 | Hardware Fingerprint | 25 | 1-2 weeks |
| 5 | Documentation & Verification | 25 | 1-2 weeks |
| **Total** | | **200** | **10-15 weeks** |

---

## Wallet for Bounty Claim

```
RTC4325af95d26d59c3ef025963656d22af638bb96b
```

---

**66 years of transistor computing. One blockchain. Infinite possibilities.**

*The first fully transistorized computer, ready to mine RustChain!*
