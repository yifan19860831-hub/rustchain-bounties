# Philco 2000 Miner - Architecture Specification

## Overview

This document provides the technical specification for the Philco TRANSAC S-2000 miner implementation.

## CPU Architecture

### Register Set

```
┌─────────────────────────────────────────────────────────┐
│              PHILOCO 2000 REGISTER FILE                 │
├─────────────────────────────────────────────────────────┤
│  AC  (Accumulator)     : 48 bits                       │
│  R0-R2 (General)       : 24 bits each                  │
│  XR0-XR31 (Index)      : 15 bits each                  │
│  BR  (Base Register)   : 16 bits                       │
│  PC  (Program Counter) : 16 bits                       │
│  IR  (Instruction Reg) : 24 bits                       │
│  SR  (Status Register) : 8 bits                        │
└─────────────────────────────────────────────────────────┘
```

### Status Register (SR)

```
Bit 7: Overflow flag (OV)
Bit 6: Carry flag (CY)
Bit 5: Zero flag (Z)
Bit 4: Negative flag (N)
Bit 3: Interrupt enable (IE)
Bit 2: Index valid (XV)
Bit 1-0: Reserved
```

## Instruction Format

Each 48-bit word contains two 24-bit instructions:

```
┌─────────────────────────────────────────┐
│  Bits 0-7   : Opcode (8 bits)           │
│  Bits 8-23  : Address (16 bits)         │
└─────────────────────────────────────────┘
```

### Instruction Classes

| Class | Opcode Range | Description |
|-------|--------------|-------------|
| Load/Store | 0x00-0x1F | Memory transfers |
| Arithmetic | 0x20-0x3F | Math operations |
| Logic | 0x40-0x5F | Bitwise operations |
| Control | 0x60-0x7F | Jumps and branches |
| Index | 0x80-0x9F | Index register ops |
| I/O | 0xA0-0xBF | Input/output |
| BCD | 0xC0-0xDF | Decimal operations |
| Special | 0xE0-0xFF | System operations |

## Core Memory Emulation

### Memory Configuration

```python
class CoreMemory:
    def __init__(self, size_kb=64):
        self.size_words = size_kb * 1024  # 4K-64K words
        self.word_size = 48  # bits
        self.access_time_us = 2  # Model 212: 2μs
        self.memory = bytearray(self.size_words * 6)  # 6 bytes per word
    
    def read(self, address):
        # Non-destructive read
        offset = address * 6
        return int.from_bytes(self.memory[offset:offset+6], 'big')
    
    def write(self, address, value):
        # Core memory write
        offset = address * 6
        self.memory[offset:offset+6] = value.to_bytes(6, 'big')
```

### Memory Timing

| Model | Cycle Time | Access Time |
|-------|------------|-------------|
| 210 (original) | 6μs | 6μs |
| 211 (MADT) | 4μs | 4μs |
| 212 (upgraded) | 2μs | 2μs |

## Surface-Barrier Transistor Model

### Transistor Characteristics

```python
class SurfaceBarrierTransistor:
    def __init__(self):
        self.base_width_um = 5  # 5 micrometers
        self.max_frequency_mhz = 100  # ~100 MHz
        self.max_power_mw = 50  # 50 milliwatts
        self.material = 'germanium'
        self.patent = 'US2885571'  # 1959
    
    def switch_time_ns(self):
        # Approximate switching time
        return 10  # ~10 nanoseconds
```

### Logic Gate Implementation

```python
class TransistorLogic:
    @staticmethod
    def NOT(input):
        return ~input & 0xFFFFFFFFFFFF  # 48-bit
    
    @staticmethod
    def AND(a, b):
        return a & b
    
    @staticmethod
    def OR(a, b):
        return a | b
    
    @staticmethod
    def NAND(a, b):
        return ~(a & b) & 0xFFFFFFFFFFFF
    
    @staticmethod
    def NOR(a, b):
        return ~(a | b) & 0xFFFFFFFFFFFF
```

## Mining State Machine

### State Transitions

```python
class MiningState:
    IDLE = 0
    MINING = 1
    ATTESTING = 2
    
    def __init__(self):
        self.state = self.IDLE
        self.epoch = 0
        self.wallet = "RTC4325af95d26d59c3ef025963656d22af638bb96b"
    
    def transition(self, new_state):
        old_state = self.state
        self.state = new_state
        print(f"State: {old_state} -> {new_state}")
```

### State Memory Layout

```
Address 0x0200-0x0205: Epoch counter (48 bits)
Address 0x0300-0x0329: Wallet address (42 ASCII chars)
Address 0x0400-0x0405: State variable (48 bits)
Address 0x0800-0x083F: SHA-256 state (simulated, 64 words)
```

## Philco 2400 I/O Processor

### I/O Architecture

```python
class Philco2400:
    def __init__(self):
        self.memory_size = 8192  # 8K words × 24 bits
        self.cycle_time_us = 3
        self.channels = {
            'card_reader': False,
            'card_punch': False,
            'printer': False,
            'tape1': False,
            'tape2': False,
            'tape3': False,
            'tape4': False,
            'paper_tape': False
        }
    
    def transfer(self, channel, data):
        # DMA-style transfer
        pass
```

## Paper Tape Format

### 8-Channel Format

```
Channel 8: Sprocket hole (always punched)
Channel 7: Data bit 6 (MSB)
Channel 6: Data bit 5
Channel 5: Data bit 4
Channel 4: Data bit 3
Channel 3: Data bit 2
Channel 2: Data bit 1
Channel 1: Data bit 0 (LSB)
```

### Encoding

```python
def encode_paper_tape(data_bytes):
    tape = []
    for byte in data_bytes:
        # Add sprocket hole (bit 7)
        tape_byte = byte | 0x80
        tape.append(tape_byte)
    return bytes(tape)
```

## KSNJFL Hexadecimal

### Philco Hex Notation

```
Decimal:  0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
Philco:   0  1  2  3  4  5  6  7  8  9  K  S  N  J  F  L
```

### Conversion

```python
PHILCO_HEX = '0123456789KSNJFL'

def to_philco_hex(value):
    result = ''
    hex_str = format(value, 'X')
    for c in hex_str:
        if c.isdigit():
            result += c
        else:
            idx = ord(c) - ord('A') + 10
            result += PHILCO_HEX[idx]
    return result
```

## Performance Model

### Instruction Timing

| Instruction Type | Cycles | Time (2μs memory) |
|------------------|--------|-------------------|
| Load/Store | 2-3 | 4-6μs |
| Add/Subtract | 2-4 | 4-8μs |
| Multiply (FP) | 11 | 22μs |
| Divide (FP) | 15 | 30μs |
| Jump | 2 | 4μs |
| Jump Conditional | 2-3 | 4-6μs |

### Mining Performance (Theoretical)

```
SHA-256 requires ~64 operations per hash
Philco 212: ~10μs per operation (average)
Time per hash: 640μs = 0.64ms
Hashes per second: ~1,562 H/s (theoretical maximum)

Reality: SHA-256 impossible without cryptographic hardware
Actual: Conceptual demonstration only
```

## Testing

### Test Vectors

```python
def test_core_memory():
    mem = CoreMemory(size_kb=64)
    mem.write(0x100, 0x123456789ABC)
    assert mem.read(0x100) == 0x123456789ABC
    print("✓ Core memory test passed")

def test_transistor_logic():
    assert TransistorLogic.NOT(0) == 0xFFFFFFFFFFFF
    assert TransistorLogic.AND(0xFF, 0x0F) == 0x0F
    assert TransistorLogic.OR(0xF0, 0x0F) == 0xFF
    print("✓ Transistor logic test passed")

def test_mining_state():
    miner = MiningState()
    assert miner.state == MiningState.IDLE
    miner.transition(MiningState.MINING)
    assert miner.state == MiningState.MINING
    print("✓ Mining state test passed")
```

## Implementation Phases

### Phase 1: Core Memory (Week 1)
- [x] Memory specification
- [ ] CoreMemory class implementation
- [ ] Read/write timing simulation
- [ ] Memory map definition

### Phase 2: CPU Simulation (Week 2)
- [ ] PhilcoCPU class
- [ ] 225 opcodes implementation
- [ ] Register file emulation
- [ ] Index register support

### Phase 3: I/O System (Week 3)
- [ ] Philco2400 I/O processor
- [ ] Paper tape encoder/decoder
- [ ] Magnetic tape simulation
- [ ] Printer output

### Phase 4: Mining Logic (Week 4)
- [ ] State machine implementation
- [ ] SHA-256 simulation (software)
- [ ] Attestation generation
- [ ] Network bridge (simulated)

### Phase 5: Documentation (Week 5)
- [ ] Historical research
- [ ] Technical documentation
- [ ] User guide
- [ ] Bounty claim submission

## Conclusion

This architecture specification provides the foundation for implementing a Philco 2000 miner that honors the historical significance of this pioneering transistorized supercomputer while demonstrating the RustChain Proof-of-Antiquity protocol conceptually.

---

*Specification Version: 1.0*
*Date: 2026-03-13*
*Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b*
