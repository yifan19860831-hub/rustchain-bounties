# Williams-Kilburn Tube Memory

## Overview

The IBM 701 used **Williams-Kilburn tubes** for main memory - the first fully electronic random-access memory system. This document details the technology and our simulation approach.

## Physical Technology

### What is a Williams Tube?

A Williams-Kilburn tube is a **cathode ray tube (CRT)** modified to store binary data as charged spots on the phosphor-coated screen.

```
┌─────────────────────────────────────────────────────────┐
│              WILLIAMS TUBE STRUCTURE                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Electron Gun ────▶ Phosphor Screen                   │
│        │                  │                             │
│        │                  ▼                             │
│        │         Charged Spots (Data)                  │
│        │         ┌───┬───┬───┬───┐                    │
│        │         │ 1 │ 0 │ 1 │ 1 │  ← Binary data     │
│        │         └───┴───┴───┴───┘                    │
│        │                  │                             │
│        ▼                  ▼                             │
│   Beam Control     Pickup Plate                        │
│   (Write/Read)     (Sense charge)                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### How It Works

1. **Writing**: Electron beam charges spots on phosphor
   - Charged spot = binary 1
   - No charge = binary 0

2. **Reading**: Beam scans spots, pickup plate senses charge
   - **Destructive read**: Reading erases the data!
   - Must rewrite after every read

3. **Refresh**: Charge dissipates over time (~20ms)
   - Must continuously refresh to maintain data
   - Similar to DRAM refresh in modern computers

## IBM 701 Memory Configuration

### Physical Layout

```
┌─────────────────────────────────────────────────────────┐
│          IBM 701 WILLIAMS TUBE MEMORY BANK              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Total tubes: 72                                        │
│  Capacity per tube: 1024 bits                          │
│  Total capacity: 73,728 bits                           │
│                                                         │
│  Organized as: 2048 words × 36 bits                    │
│  (72 tubes × 1024 bits = 2048 × 36 bits)              │
│                                                         │
│  Tube 0-35:   Data bits (36 bits per word)            │
│  Tube 36-71:  Parity/spare (not used in 701)          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Word Organization

Each 36-bit word is distributed across 36 Williams tubes:

```
Word N (36 bits):
┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
│S  │D35│D34│D33│D32│D31│D30│D29│D28│D27│D26│D25│
└───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
 │   │   │   │   │   │   │   │   │   │   │   │
 ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼
T0  T1  T2  T3  T4  T5  T6  T7  T8  T9  T10 T11

┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
│D24│D23│D22│D21│D20│D19│D18│D17│D16│D15│D14│D13│
└───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
 │   │   │   │   │   │   │   │   │   │   │   │
 ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼
T12 T13 T14 T15 T16 T17 T18 T19 T20 T21 T22 T23

┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
│D12│D11│D10│D9 │D8 │D7 │D6 │D5 │D4 │D3 │D2 │D1 │
└───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
 │   │   │   │   │   │   │   │   │   │   │   │
 ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼
T24 T25 T26 T27 T28 T29 T30 T31 T32 T33 T34 T35

S = Sign bit
D = Data bit
T = Williams Tube number
```

## Timing Characteristics

### Access Times

| Operation | Time | Notes |
|-----------|------|-------|
| Read | 12 μs | Destructive - must rewrite |
| Write | 12 μs | Electron beam positioning |
| Refresh | 10-20 ms | Full memory refresh cycle |
| Cycle time | 12 μs | Minimum between operations |

### Refresh Requirements

Williams tubes require continuous refreshing:

```python
# Refresh cycle timing
REFRESH_INTERVAL_MS = 20  # Must refresh every 20ms
REFRESH_FREQUENCY_HZ = 50  # 50 Hz refresh rate

def refresh_memory(memory):
    """
    Refresh all 2048 words in Williams tube memory
    Must complete within 20ms to prevent data loss
    """
    for address in range(2048):
        # Read restores charge (but destroys data)
        data = memory.read_word(address)
        # Immediately rewrite to restore pattern
        memory.write_word(address, data)
```

## Decay Simulation

### Charge Dissipation Model

Williams tube charge decays exponentially:

```python
class WilliamsTubeDecay:
    """Models charge decay on Williams tube phosphor"""
    
    def __init__(self):
        self.initial_charge = 1.0
        self.decay_constant = 0.05  # 5% per ms
        self.current_charge = 1.0
    
    def decay(self, time_ms):
        """Simulate charge decay over time"""
        # Exponential decay: Q(t) = Q₀ * e^(-λt)
        import math
        self.current_charge = self.initial_charge * math.exp(
            -self.decay_constant * time_ms
        )
        return self.current_charge
    
    def is_valid(self):
        """Check if charge is above readable threshold"""
        return self.current_charge > 0.3  # 30% threshold
```

### Temperature Effects

Williams tubes are temperature sensitive:

```python
class TemperatureEffect:
    """Models temperature effects on Williams tube operation"""
    
    def __init__(self):
        self.optimal_temp_celsius = 25
        self.current_temp_celsius = 25
        self.temp_coefficient = 0.02  # 2% per degree
    
    def get_decay_modifier(self):
        """Temperature affects decay rate"""
        delta_t = abs(self.current_temp_celsius - self.optimal_temp_celsius)
        # Higher temp = faster decay
        return 1.0 + (delta_t * self.temp_coefficient)
```

## Simulation Implementation

### Python Model

```python
@dataclass
class WilliamsTube:
    """Simulates a Williams tube memory cell"""
    bits: int = 0
    refresh_count: int = 0
    decay_timer: float = 0.0
    
    def read(self) -> int:
        """Read value - simulates destructive read"""
        self.refresh_count += 1
        
        # Check for decay-induced data loss
        if self.decay_timer > 0.02:  # 20ms threshold
            self.bits = 0  # Data lost!
        
        return self.bits
    
    def write(self, value: int):
        """Write value to tube"""
        mask = (1 << 36) - 1  # 36-bit mask
        self.bits = value & mask
        self.decay_timer = 0.0  # Reset decay timer
    
    def tick(self, delta: float):
        """Simulate time passage"""
        self.decay_timer += delta
```

### Memory Bank

```python
@dataclass
class WilliamsTubeMemory:
    """2048-word Williams tube memory (72 tubes)"""
    tubes: List[WilliamsTube] = field(default_factory=lambda: 
        [WilliamsTube() for _ in range(2048)])
    
    def read_word(self, addr: int) -> int:
        """Read 36-bit word from address"""
        if 0 <= addr < 2048:
            return self.tubes[addr].read()
        return 0
    
    def write_word(self, addr: int, value: int):
        """Write 36-bit word to address"""
        if 0 <= addr < 2048:
            self.tubes[addr].write(value)
    
    def refresh(self):
        """Refresh all tubes to prevent data loss"""
        for addr in range(2048):
            data = self.read_word(addr)
            self.write_word(addr, data)
```

## Historical Context

### Invention

- **Inventors**: Freddie Williams and Tom Kilburn
- **Year**: 1947
- **Location**: University of Manchester, England
- **First use**: Manchester Baby (1948) - first stored-program computer

### Advantages (for the era)

✅ Fully electronic (no moving parts)
✅ Random access (not sequential like drums)
✅ Faster than relay or vacuum tube latch memory
✅ Proved viability of stored-program concept

### Disadvantages

❌ Required constant refresh
❌ Temperature sensitive
❌ Unreliable (tube failures common)
❌ Limited capacity
❌ Destructive read (must rewrite)

### Successor Technology

Williams tubes were replaced by **magnetic core memory** in the late 1950s:

| Feature | Williams Tube | Magnetic Core |
|---------|---------------|---------------|
| **Technology** | CRT | Magnetic cores |
| **Refresh** | Required | Not required |
| **Volatility** | Volatile | Non-volatile |
| **Reliability** | Low | High |
| **Capacity** | Low (~1KB) | Medium (~4KB) |
| **Speed** | Fast | Fast |
| **Era** | 1947-1957 | 1955-1975 |

## IBM 701 Specifics

### Memory Configuration Options

IBM 701 shipped with different memory configurations:

| Configuration | Words | Tubes | Price Impact |
|---------------|-------|-------|--------------|
| Minimum | 256 | 9 | Base |
| Standard | 1024 | 36 | +$5,000/month |
| Maximum | 2048 | 72 | +$10,000/month |

### Maintenance Requirements

Williams tubes required constant maintenance:

```
Daily:
- Warm-up period: 30 minutes
- Focus adjustment
- Deflection calibration

Weekly:
- Tube replacement (failed tubes)
- Phosphor cleaning
- High voltage adjustment

Monthly:
- Complete realignment
- Pickup plate adjustment
- Timing calibration
```

### Failure Modes

Common Williams tube failures:

1. **Phosphor burnout**: Spots become permanent
2. **Gas buildup**: Tube loses vacuum
3. **Cathode depletion**: Electron gun weakens
4. **Pickup plate drift**: Signal weakens
5. **High voltage failure**: CRT won't operate

## References

- Williams, F.C. & Kilburn, T. (1948). "Electronic Digital Computer"
- IBM 701 Reference Manual (A24-1403-0, 1953)
- "Williams Tube Memory Systems" - IEEE Annals of History
- Computer History Museum: Williams Tube Collection

---

*Williams-Kilburn tubes made the IBM 701 possible - the first commercial computer with fully electronic random-access memory.*
