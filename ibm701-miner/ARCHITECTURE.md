# IBM 701 Architecture Specification

## Technical Overview

The IBM 701 Electronic Data Processing Machine (1952) was IBM's first commercial scientific computer. This document details the architecture for the RustChain Proof-of-Antiquity miner implementation.

## System Architecture

### Core Specifications

| Component | Specification |
|-----------|---------------|
| **Word Length** | 36 bits |
| **Memory Capacity** | 2048 words (73,728 bits) |
| **Memory Technology** | Williams-Kilburn tubes (72 CRTs) |
| **Instruction Size** | 18 bits |
| **Instructions per Word** | 2 |
| **Address Space** | 11 bits (0-2047) |
| **Technology** | Vacuum tubes (4,000+) |

### CPU Registers

```
┌─────────────────────────────────────────────────────────┐
│                  IBM 701 CPU REGISTERS                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  AC (Accumulator)     - 36 bits - Primary arithmetic   │
│  MQ (Multiplier/Quot) - 36 bits - Multiply/divide aux  │
│  IBR (Instr Buffer)   - 18 bits - Second instruction  │
│  PC (Program Counter) - 11 bits - Address 0-2047       │
│  IR (Instruction Reg) - 18 bits - Current instruction  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Memory Organization

```
┌─────────────────────────────────────────────────────────┐
│           WILLIAMS TUBE MEMORY (2048 words)             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  72 Williams tubes × 1024 bits each = 73,728 bits      │
│  Organized as: 2048 words × 36 bits                    │
│                                                         │
│  Address Range: 0x000 - 0x7FF                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Memory Map for Miner

```
Address    Size    Usage
─────────────────────────────────────────────────────────
0x000-0x03F  64     System reserved / Bootstrap
0x040-0x0FF  192    Miner program code
0x100-0x1FF  256    Epoch counters and state
0x200-0x2FF  256    Wallet address storage
0x300-0x3FF  256    Working registers / Hash state
0x400-0x4FF  256    Nonce counter
0x500-0x5FF  256    Attestation buffer
0x600-0x7FF  512    Available for program use
```

## Instruction Set

### Instruction Format

```
┌──────────────────────────────────────┐
│     18-BIT INSTRUCTION FORMAT        │
├──────────┬────┬──────────────────────┤
│   OP     │ I  │     Address          │
│  8 bits  │1bit│     10 bits          │
└──────────┴────┴──────────────────────┘

OP  = Opcode (operation to perform)
I   = Immediate flag (not used in 701)
Address = Memory address (0-1023)
```

### Complete Instruction Set

| Opcode | Mnemonic | Description | Execution Time |
|--------|----------|-------------|----------------|
| 0x00 | STOP | Halt execution | 1 μs |
| 0x01 | ADD | Add memory to AC | 60 μs |
| 0x02 | SUB | Subtract memory from AC | 60 μs |
| 0x03 | MUL | Multiply MQ by memory | 300 μs |
| 0x04 | DIV | Divide AC by memory | 300 μs |
| 0x05 | AND | Bitwise AND | 12 μs |
| 0x06 | OR | Bitwise OR | 12 μs |
| 0x07 | JMP | Unconditional jump | 12 μs |
| 0x08 | JZ | Jump if AC = 0 | 12 μs |
| 0x09 | JN | Jump if AC < 0 | 12 μs |
| 0x0A | LD | Load memory to AC | 12 μs |
| 0x0B | ST | Store AC to memory | 12 μs |
| 0x0C | IN | Input from card/tape | 100+ ms |
| 0x0D | OUT | Output to printer/tape | 100+ ms |
| 0x0E | RSH | Right shift AC | 12 μs |
| 0x0F | LSH | Left shift AC | 12 μs |

## Williams Tube Memory

### Physical Characteristics

```
┌─────────────────────────────────────────────────────────┐
│            WILLIAMS TUBE PHYSICAL LAYOUT                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Each tube: Cathode Ray Tube (CRT)                     │
│  Storage: Charged spots on phosphor coating            │
│  Capacity: 1024 bits per tube                          │
│  Total tubes: 72                                       │
│  Total capacity: 73,728 bits (2048 × 36-bit words)     │
│                                                         │
│  Refresh requirement: ~100 Hz (every 10ms)             │
│  Access time: ~12 microseconds                         │
│  Temperature sensitive: Yes                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Refresh Mechanism

Williams tubes require continuous refreshing to maintain data:

```python
def refresh_cycle(memory):
    """
    Williams tube refresh cycle
    Must be performed every 10-20ms
    """
    for address in range(2048):
        # Read restores charge on phosphor
        data = memory.read_word(address)
        # Rewrite to restore pattern
        memory.write_word(address, data)
```

### Decay Simulation

```python
class WilliamsTubeDecay:
    """Simulates charge decay on Williams tube phosphor"""
    
    def __init__(self):
        self.decay_time_ms = 20  # 20ms until data loss
        self.charge_level = 1.0
    
    def tick(self, delta_ms):
        """Simulate time passage"""
        self.charge_level -= delta_ms / self.decay_time_ms
        if self.charge_level <= 0:
            self.charge_level = 0
            return True  # Data lost
        return False
```

## Vacuum Tube Characteristics

### Timing Variance

Vacuum tubes introduce timing variance due to:
- Thermal drift
- Power supply ripple
- Component aging
- Warm-up characteristics

```python
class VacuumTubeTiming:
    """Simulates vacuum tube timing characteristics"""
    
    def __init__(self):
        self.thermal_drift = gauss(0, 0.03)  # 3% variance
        self.power_ripple = gauss(0, 0.01)   # 1% ripple
        self.warmup_factor = 1.0  # Increases during warmup
    
    def get_operation_time(self, base_time):
        """Calculate actual operation time with variance"""
        variance = self.thermal_drift + self.power_ripple
        return base_time * (1.0 + variance) * self.warmup_factor
```

## Mining State Machine

### States

```
┌─────────────────────────────────────────────────────────┐
│              IBM 701 MINER STATE MACHINE                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│                    ┌─────────┐                         │
│         ┌─────────▶│  IDLE   │◀──────────┐             │
│         │          │  (0x0)  │           │             │
│         │          └────┬────┘           │             │
│         │               │                 │             │
│         │ epoch_start   │                 │ complete    │
│         │               ▼                 │             │
│         │          ┌─────────┐           │             │
│         │          │ MINING  │───────────┘             │
│         │          │  (0x1)  │                         │
│         │          └────┬────┘                         │
│         │               │                              │
│         │ solution_found│                              │
│         │               ▼                              │
│         │          ┌─────────┐                        │
│         └──────────│ATTESTING│                        │
│                    │  (0x2)  │                        │
│                    └─────────┘                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### State Transitions

| From State | Trigger | To State | Action |
|------------|---------|----------|--------|
| IDLE | Epoch start | MINING | Initialize nonce |
| MINING | Solution found | ATTESTING | Generate fingerprint |
| ATTESTING | Complete | IDLE | Submit attestation |

## Hardware Fingerprinting

### Entropy Sources

The IBM 701 miner generates unique fingerprints from:

1. **Williams Tube Decay Patterns**
   - Each tube has unique decay characteristics
   - Phosphor aging creates distinctive signatures
   - Temperature gradients affect decay rates

2. **Vacuum Tube Timing**
   - Thermal drift varies by tube
   - Power supply ripple unique to system
   - Component aging signatures

3. **Memory Access Patterns**
   - Williams tube refresh timing
   - Address decoding delays
   - Signal propagation variance

### Fingerprint Generation

```python
def generate_fingerprint(cpu, epoch, nonce):
    """Generate unique IBM 701 hardware fingerprint"""
    
    # Sample vacuum tube timing
    timing_samples = []
    for _ in range(100):
        time_us = cpu.timing.get_operation_time(60)
        timing_samples.append(time_us)
    
    # Sample Williams tube decay
    decay_pattern = sum([
        tube.decay_timer 
        for tube in cpu.memory.tubes[:72]
    ])
    
    # Create hash
    data = {
        'timing_avg': mean(timing_samples),
        'timing_variance': variance(timing_samples),
        'decay_pattern': decay_pattern,
        'epoch': epoch,
        'nonce': nonce,
        'timestamp': time.time()
    }
    
    return sha256(str(data).encode()).hexdigest()[:16]
```

## Attestation Format

### RustChain Attestation

```json
{
  "hardware": "IBM 701",
  "year": 1952,
  "architecture": "36-bit IAS-derived",
  "memory_type": "Williams tube",
  "memory_size": "2048 words",
  "multiplier": 5.0,
  "tier": "LEGENDARY",
  "wallet": "RTC...",
  "epoch": 0,
  "nonce": 1,
  "fingerprint": "IBM701-xxxxxxxxxxxxxxxx",
  "timestamp": 1234567890.123,
  "instructions_executed": 1000,
  "total_time_us": 60000,
  "signature": "..."
}
```

## Performance Characteristics

### Theoretical Performance

| Metric | IBM 701 | Modern CPU | Ratio |
|--------|---------|------------|-------|
| Addition | 60 μs | 1 ns | 60,000:1 |
| Multiplication | 300 μs | 3 ns | 100,000:1 |
| Memory Access | 12 μs | 100 ns | 120:1 |
| Instructions/sec | ~16,667 | ~4,000,000,000 | 240,000:1 |

### Mining Performance (Simulated)

| Metric | Value |
|--------|-------|
| Instructions per epoch | ~1,000 |
| Simulated time per epoch | ~60 ms |
| Real time per epoch | ~1 ms |
| Attestations per minute | ~60 |

## I/O Systems

### Punched Cards

IBM 701 used 80-column punched cards:

```
┌────────────────────────────────────────┐
│ 80 columns × 12 rows (Hollerith code) │
│ Each card: 80 characters               │
│ Binary mode: 36 bits per card          │
└────────────────────────────────────────┘
```

### Magnetic Tape

Optional 7-track magnetic tape:

```
┌────────────────────────────────────────┐
│ 7 tracks (6 data + 1 parity)          │
│ Density: 100 bits per inch            │
│ Speed: 75 inches per second           │
│ Capacity: ~1.5 MB per reel            │
└────────────────────────────────────────┘
```

## References

- IBM 701 Reference Manual (1953)
- BITSavers IBM 701 Documentation
- Williams-Kilburn Tube Technical Manual
- IEEE History of Computing: IBM 700 Series

---

*This architecture specification supports the RustChain Proof-of-Antiquity protocol for the IBM 701 (1952).*
