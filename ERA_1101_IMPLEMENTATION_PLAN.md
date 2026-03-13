# ERA 1101 Miner Implementation Plan

## Executive Summary

This document provides a detailed technical implementation plan for porting the RustChain miner to the ERA 1101 (1950), the first commercially available stored-program computer. The implementation requires:

1. **Simulator development** for testing and validation
2. **SHA256 implementation** adapted to 24-bit ones' complement architecture
3. **Drum memory optimization** for minimal rotational latency
4. **Network bridge** via paper tape interface
5. **Hardware fingerprinting** unique to ERA 1101

**Target**: 200 RTC bounty (LEGENDARY Tier, 5.0× multiplier)

---

## Phase 1: Simulator Development

### 1.1 CPU Simulator Architecture

```python
# era1101_sim/cpu.py
class ERA1101CPU:
    def __init__(self):
        # 24-bit registers (ones' complement)
        self.A = 0  # 48-bit accumulator (high + low)
        self.AH = 0  # Accumulator high 24 bits
        self.AL = 0  # Accumulator low 24 bits
        self.Q = 0  # 24-bit Q-register (multiplier/quotient)
        self.X = 0  # 24-bit X-register (index)
        
        # Program counter
        self.PC = 0
        self.IR = 0  # Instruction register
        
        # Status flags
        self.zero_flag = False
        self.neg_flag = False
        
    def ones_complement(self, value):
        """Compute ones' complement (bitwise NOT for 24 bits)"""
        return (~value) & 0xFFFFFF
        
    def add_with_complement(self, a, b):
        """Addition via complement subtraction (ERA 1101 style)"""
        # A + B = A - (~B) in ones' complement
        complement_b = self.ones_complement(b)
        result = (a + complement_b + 1) & 0xFFFFFF
        # End-around carry for ones' complement
        if result > 0xFFFFFF:
            result = (result + 1) & 0xFFFFFF
        return result
```

### 1.2 Drum Memory Model

```python
# era1101_sim/drum.py
class MagneticDrum:
    def __init__(self):
        self.capacity = 16384  # 16K words
        self.word_size = 24  # bits
        self.rpm = 3500
        self.heads = 200
        self.memory = [0] * self.capacity
        
        # Timing characteristics
        self.rotation_period_us = 60_000_000 / self.rpm  # ~17,143 μs per rotation
        self.words_per_track = self.capacity // self.heads  # ~82 words per track
        self.word_time_us = self.rotation_period_us / self.words_per_track  # ~209 μs per word
        
    def access_time(self, current_pos, target_pos):
        """Calculate access time based on rotational position"""
        if current_pos == target_pos:
            return 32  # Minimum access time (head already positioned)
        
        # Calculate rotational latency
        distance = (target_pos - current_pos) % self.capacity
        latency_us = (distance * self.word_time_us)
        
        return min(latency_us, self.rotation_period_us)  # Max 17ms
```

### 1.3 Instruction Set Implementation

```python
# era1101_sim/instructions.py
INSTRUCTION_SET = {
    # Arithmetic (00-0F)
    0x00: ('INS',   'Insert (y) in A'),
    0x01: ('INSC',  'Insert complement of (y) in A'),
    0x02: ('INSM',  'Insert (y) in A [multiple precision]'),
    0x03: ('INSCM', 'Insert complement of (y) in A [multiple precision]'),
    0x04: ('INSA',  'Insert absolute value (y) in A'),
    0x05: ('INSCA', 'Insert complement of absolute value (y) in A'),
    0x06: ('ADD',   'Add (y) to (A)'),
    0x07: ('SUB',   'Subtract (y) from (A)'),
    0x08: ('ADDM',  'Add (y) to (A) [multiple precision]'),
    0x09: ('SUBM',  'Subtract (y) from (A) [multiple precision]'),
    0x0A: ('ADDA',  'Add absolute value of (y) to (A)'),
    0x0B: ('SUBA',  'Subtract absolute value of (y) from (A)'),
    0x0C: ('INSQ',  'Insert (Q) in A'),
    0x0D: ('CLR',   'Clear right half of A'),
    0x0E: ('ADDQ',  'Add (Q) to (A)'),
    0x0F: ('TRA',   'Transmit (A) to Q'),
    
    # Multiply/Divide (10-14)
    0x10: ('MPY',   'Form product (Q) * (y) in A'),
    0x11: ('LGR',   'Add logical product (Q) * (y) to A'),
    0x12: ('AND',   'Form logical product (Q) * (y) in A'),
    0x13: ('DIV',   'Divide (A) by (y)'),
    0x14: ('MLA',   'Add product (Q) * (y) to (A)'),
    
    # Logical/Control (15-1F)
    0x15: ('STO',   'Store right half of (A) at y'),
    0x16: ('SHL',   'Shift (A) left'),
    0x17: ('STQ',   'Store (Q) at y'),
    0x18: ('SHQ',   'Shift (Q) left'),
    0x19: ('RPL',   'Replace (y) with (A) using (Q) as operator'),
    0x1A: ('JMP',   'Take (y) as next order'),
    0x1B: ('STA',   'Replace (y) with (A) [address portion only]'),
    0x1C: ('JNZ',   'Take (y) as next order if (A) is not zero'),
    0x1D: ('INSX',  'Insert (y) in Q'),
    0x1E: ('JN',    'Take (y) as next order if (A) is negative'),
    0x1F: ('JQ',    'Take (y) as next order if (Q) is negative'),
}

def decode_instruction(word):
    """Decode 24-bit instruction word"""
    opcode = (word >> 18) & 0x3F  # 6-bit opcode
    skip = (word >> 14) & 0x0F   # 4-bit skip
    address = word & 0x3FFF       # 14-bit address
    return opcode, skip, address
```

### 1.4 Assembler with Drum Optimization

```python
# era1101_sim/assembler.py
class DrumOptimizingAssembler:
    def __init__(self):
        self.instructions = []
        self.labels = {}
        self.optimized = False
        
    def optimize_placement(self):
        """
        Optimize instruction placement for minimal drum rotational latency.
        
        Strategy:
        1. Calculate execution time for each instruction
        2. Place next instruction at optimal drum position
        3. Use skip field to account for execution time
        """
        optimized_program = []
        current_pos = 0
        
        for instr in self.instructions:
            exec_time = instr.execution_time_us
            
            # Calculate optimal next position
            words_to_skip = exec_time / drum.word_time_us
            optimal_next = (current_pos + int(words_to_skip)) % drum.capacity
            
            # Update skip field
            instr.skip = (optimal_next - current_pos) % drum.capacity
            
            optimized_program.append(instr)
            current_pos = optimal_next
            
        return optimized_program
```

---

## Phase 2: SHA256 Implementation

### 2.1 Adapting SHA256 to 24-bit Architecture

SHA256 is designed for 32-bit words. ERA 1101 has 24-bit words. We need to adapt:

**Strategy**: Use multi-word arithmetic for 32-bit operations
- 32-bit value = 24-bit word + 8-bit partial word
- Or: 32-bit value = 2 × 24-bit words (with padding)

```assembly
; SHA256 constant K0 (first 32 bits of sqrt(2))
; Original: 0x428A2F98
; ERA 1101 representation (2 × 24-bit):
K0_HIGH:  0x428A2F  ; Upper 24 bits
K0_LOW:   0x980000  ; Lower 8 bits, padded to 24 bits
```

### 2.2 SHA256 Core Operations

```assembly
; SHA256 Σ0 function: ROTR(2) XOR ROTR(13) XOR ROTR(22)
; Implemented for 24-bit words

SHA256_SIGMA0:
    ; Input: Q-register contains value
    ; Output: A-register contains result
    
    ; ROTR(2)
    INSQ        ; Q -> A
    SHL         ; Shift left (with wraparound for rotation)
    SHL         ; 2 positions
    
    ; Store temp1
    STO     TEMP1
    
    ; ROTR(13)
    INSQ
    ; ... (13 shifts)
    
    ; XOR with temp1
    ; ... (bitwise operations)
    
    ; Continue for ROTR(22)
    ; ...
    
    JMP     NEXT_INSTR
```

### 2.3 Memory Layout for SHA256

```
Drum Memory Map (16,384 words total):

Zone 1: Boot & System (0x0000-0x0FFF, 4K words)
├── 0x0000-0x00FF: Boot loader (256 words)
├── 0x0100-0x01FF: Interrupt vectors (256 words)
├── 0x0200-0x03FF: I/O routines (512 words)
└── 0x0400-0x0FFF: System utilities (3K words)

Zone 2: SHA256 Constants (0x1000-0x2FFF, 8K words)
├── 0x1000-0x107F: K constants (64 words × 2 for 32-bit = 128 words)
├── 0x1080-0x10FF: H initial values (8 words × 2 = 16 words)
├── 0x1100-0x1FFF: Lookup tables (optimized for drum access)
└── 0x2000-0x2FFF: Reserved constants

Zone 3: Working Memory (0x3000-0x3FFF, 4K words)
├── 0x3000-0x3007: Hash state H0-H7 (8 words)
├── 0x3008-0x3017: Message schedule W[0..15] (16 words)
├── 0x3018-0x30FF: Temporary variables (232 words)
├── 0x3100-0x31FF: Network I/O buffer (256 words)
├── 0x3200-0x33FF: Stack (512 words)
└── 0x3400-0x3FFF: General purpose (3K words)

Zone 4: Unassigned (0x4000-0x3FFF, remaining)
```

### 2.4 Drum-Optimized SHA256 Loop

```assembly
; Optimized SHA256 compression function main loop
; Key insight: Schedule instructions to minimize drum rotational latency

MAIN_LOOP:
    ; Load W[t] (optimized position)
    LD      W_TABLE+0(t)    ; Position: track 48, word 12
    
    ; Execute SHA256 operations (96 μs each)
    ; Next instruction placed at optimal drum position
    
    ADD     TEMP1           ; Position: track 48, word 15 (3 words ahead)
    ADD     TEMP2           ; Position: track 48, word 18
    STO     TEMP3           ; Position: track 48, word 21
    
    ; Rotate to next track for next operation
    JMP     NEXT_OP         ; Position: track 48, word 24
    
NEXT_OP:
    ; Continue with T1 computation
    ; ... (drum-optimized throughout)
```

---

## Phase 3: Network Bridge

### 3.1 Paper Tape Interface Hardware

```
ERA 1101 ←→ Microcontroller ←→ Internet

Paper Tape Reader (Input):
├── Optical sensor array (8-bit parallel)
├── Sprocket hole detector (timing)
├── Level shifter (ERA 1101 logic → 3.3V)
└── Microcontroller GPIO

Paper Tape Punch (Output):
├── Microcontroller GPIO
├── Level shifter (3.3V → ERA 1101 logic)
├── Punch solenoid driver
└── Paper tape mechanism
```

### 3.2 Communication Protocol

```
Mining Request (ERA 1101 → Microcontroller):
╔════════════════════════════════════════╗
║ START (1) | CMD (1) | NONCE (8)        ║
║ DIFFICULTY (1) | CHECKSUM (1) | END (1)║
╚════════════════════════════════════════╝
Total: 13 characters @ 100 chars/s = 130ms

Mining Response (Microcontroller → ERA 1101):
╔═══════════════════════════════════════════════════╗
║ START (1) | NONCE (8) | HASH (32) | CHECKSUM (1) ║
║ END (1)                                           ║
╚═══════════════════════════════════════════════════╝
Total: 43 characters @ 100 chars/s = 430ms
```

### 3.3 Microcontroller Firmware

```cpp
// era1101_bridge/firmware.cpp
#include <WiFi.h>
#include <HTTPClient.h>

#define TAPE_READ_PIN   2
#define TAPE_PUNCH_PIN  3
#define TAPE_CLOCK_PIN  4

void handleMiningRequest() {
    // Read paper tape input
    uint8_t nonce[8];
    readPaperTape(nonce, 8);
    
    // Build HTTP request to mining pool
    HTTPClient http;
    http.begin("https://pool.rustchain.org/api/job");
    http.addHeader("Content-Type", "application/json");
    
    String payload = "{\"nonce\":\"" + bytesToHex(nonce, 8) + "\"}";
    int httpCode = http.POST(payload);
    
    if (httpCode > 0) {
        String response = http.getString();
        
        // Parse response and punch to paper tape
        uint8_t hash[32];
        parseResponse(response, hash);
        punchPaperTape(hash, 32);
    }
    
    http.end();
}
```

---

## Phase 4: Hardware Fingerprinting

### 4.1 Drum Timing Signature

```python
# era1101_fingerprint/drum_timing.py
def extract_drum_signature():
    """
    Extract unique magnetic drum timing signature.
    
    Factors:
    - Rotational variance (RPM fluctuation)
    - Head positioning delay
    - Track-to-track seek time
    - Temperature-dependent expansion
    """
    samples = []
    for i in range(1000):
        start_time = time.time()
        access_word(random_address)
        end_time = time.time()
        samples.append(end_time - start_time)
    
    # Statistical analysis
    mean_access = np.mean(samples)
    std_access = np.std(samples)
    min_access = np.min(samples)
    max_access = np.max(samples)
    
    # Create signature
    signature = {
        'mean_us': mean_access * 1e6,
        'std_us': std_access * 1e6,
        'min_us': min_access * 1e6,
        'max_us': max_access * 1e6,
        'histogram': np.histogram(samples, bins=100)
    }
    
    return signature
```

### 4.2 Vacuum Tube Power Signature

```python
# era1101_fingerprint/tube_signature.py
def extract_tube_signature():
    """
    Extract vacuum tube power consumption signature.
    
    2700 tubes create a unique power draw pattern.
    """
    # Measure current draw at high frequency
    current_samples = []
    for i in range(10000):
        current = read_current_sensor()
        current_samples.append(current)
        time.sleep(0.001)  # 1kHz sampling
    
    # FFT analysis for frequency signature
    fft = np.fft.fft(current_samples)
    frequency_signature = np.abs(fft[:1000])  # First 1000 Hz
    
    return {
        'mean_current': np.mean(current_samples),
        'std_current': np.std(current_samples),
        'frequency_signature': frequency_signature.tolist()
    }
```

### 4.3 Attestation Payload

```json
{
  "hardware_type": "era_1101",
  "year": 1950,
  "technology": "vacuum_tube",
  "memory_type": "magnetic_drum",
  "fingerprint": {
    "drum_timing": {
      "mean_us": 2847.3,
      "std_us": 1523.8,
      "min_us": 32.1,
      "max_us": 17142.9,
      "signature_hash": "0x7a8b9c..."
    },
    "tube_power": {
      "mean_amps": 47.3,
      "std_amps": 2.1,
      "frequency_hash": "0x3d4e5f..."
    },
    "thermal_profile": {
      "idle_temp_c": 42.5,
      "load_temp_c": 68.3,
      "warmup_time_s": 180
    }
  },
  "timestamp": "2026-03-13T11:33:15Z",
  "wallet": "RTC4325af95d26d59c3ef025963656d22af638bb96b"
}
```

---

## Phase 5: Testing & Validation

### 5.1 SHA256 Test Vectors

```python
# era1101_sim/tests/sha256_tests.py
import unittest

class TestSHA256(unittest.TestCase):
    def test_empty_string(self):
        # SHA256("") = e3b0c44298fc1c149afbf4c8996fb924...
        result = sha256_era1101(b"")
        expected = bytes.fromhex("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
        self.assertEqual(result, expected)
    
    def test_abc(self):
        # SHA256("abc") = ba7816bf8f01cfea414140de5dae2223...
        result = sha256_era1101(b"abc")
        expected = bytes.fromhex("ba7816bf8f01cfea414140de5dae2223b097fe4934da6243a5a1f8e7e9c1f1e7")
        self.assertEqual(result, expected)
    
    def test_performance(self):
        # Measure hash time
        start = time.time()
        for i in range(10):
            sha256_era1101(b"test")
        elapsed = time.time() - start
        print(f"Average hash time: {elapsed/10:.2f}s")
        # Target: < 20s per hash
```

### 5.2 Drum Optimization Validation

```python
# era1101_sim/tests/drum_optimization.py
def test_drum_scheduling():
    """Verify drum optimization reduces average access time"""
    
    # Unoptimized program
    unoptimized = load_program("sha256_naive.asm")
    unoptimized_time = simulate_with_timing(unoptimized)
    
    # Optimized program
    optimized = load_program("sha256_optimized.asm")
    optimized_time = simulate_with_timing(optimized)
    
    improvement = (unoptimized_time - optimized_time) / unoptimized_time
    print(f"Drum optimization improvement: {improvement*100:.1f}%")
    
    # Target: > 50% improvement
    assert improvement > 0.5, "Drum optimization should improve performance by >50%"
```

---

## Directory Structure

```
era-1101-miner/
├── README.md
├── LICENSE
├── docs/
│   ├── architecture.md
│   ├── instruction_set.md
│   ├── drum_optimization.md
│   └── fingerprint.md
├── sim/
│   ├── cpu.py
│   ├── drum.py
│   ├── instructions.py
│   ├── assembler.py
│   └── tests/
│       ├── test_cpu.py
│       ├── test_sha256.py
│       └── test_drum.py
├── assembler/
│   ├── era1101_asm.py
│   ├── optimizer.py
│   └── examples/
│       ├── hello_world.asm
│       └── sha256_core.asm
├── firmware/
│   ├── bridge/
│   │   ├── firmware.cpp
│   │   └── protocol.h
│   └── hardware/
│       ├── schematic.pdf
│       └── pcb/
├── sha256/
│   ├── sha256_core.asm
│   ├── constants.asm
│   └── test_vectors.asm
├── fingerprint/
│   ├── drum_timing.py
│   ├── tube_signature.py
│   └── attestation.py
└── examples/
    ├── mining_loop.asm
    └── network_io.asm
```

---

## Milestones & Timeline

| Milestone | Deliverable | Timeline | RTC |
|-----------|-------------|----------|-----|
| M1 | Simulator passes SHA256 test vectors | Week 3 | 25 |
| M2 | Assembler with drum optimization | Week 4 | 25 |
| M3 | SHA256 implementation complete | Week 7 | 50 |
| M4 | Network bridge hardware + firmware | Week 9 | 50 |
| M5 | Hardware fingerprint implementation | Week 10 | 25 |
| M6 | Full system integration test | Week 11 | 25 |
| M7 | Documentation + video | Week 12 | 25 |
| **Total** | **Complete bounty** | **12 weeks** | **200** |

---

## Risk Mitigation

### Technical Risks

1. **SHA256 too slow for practical mining**
   - Mitigation: Accept low hash rate (0.05-0.2 H/s is acceptable for bounty)
   - Focus on correctness over speed

2. **Drum optimization insufficient**
   - Mitigation: Multiple optimization passes, profile-guided optimization
   - Use simulator to test different strategies

3. **Paper tape interface unreliable**
   - Mitigation: Error detection + retry logic
   - Offline batch mode as fallback

### Hardware Risks

1. **ERA 1101 unavailable**
   - Mitigation: Partner with Computer History Museum or similar
   - Use simulator for development, hardware for final validation

2. **Drum memory failure**
   - Mitigation: Spare drum unit, regular maintenance
   - Non-critical data on paper tape backup

---

## Success Criteria

✅ **Simulator**: Passes all NIST SHA256 test vectors  
✅ **Performance**: < 20s per SHA256 hash (drum-optimized)  
✅ **Network**: Successful round-trip to mining pool via paper tape  
✅ **Fingerprint**: Unique hardware signature registered with RustChain  
✅ **Verification**: Miner appears in rustchain.org/api/miners  
✅ **Documentation**: Complete technical docs + video demonstration  
✅ **Open Source**: All code released under MIT/Apache 2.0  

---

## Conclusion

The ERA 1101 miner implementation is a challenging but achievable project that combines:

- **Historical preservation**: Bringing the first commercial computer back to life
- **Technical innovation**: Adapting modern cryptography to 1950s architecture
- **Engineering optimization**: Drum scheduling for minimal rotational latency
- **Hardware interfacing**: Bridging 76-year-old technology to modern internet

**The reward**: 200 RTC + 5.0× multiplier + a place in computing history.

Let's make the ERA 1101 earn its keep in 2026.

---

**Wallet**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`  
**Created**: 2026-03-13  
**Status**: Ready for implementation
