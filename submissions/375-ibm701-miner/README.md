# RustChain IBM 701 Miner (1952) 🖥️

[![IBM 701](https://img.shields.io/badge/hardware-IBM%20701%20(1952)-blue?style=flat)](https://en.wikipedia.org/wiki/IBM_701)
[![Era](https://img.shields.io/badge/era-Vacuum%20Tube%20(1950s)-red?style=flat)](https://en.wikipedia.org/wiki/Vacuum_tube)
[![Antiquity Multiplier](https://img.shields.io/badge/multiplier-5.0x%20LEGENDARY-gold?style=flat)](https://github.com/Scottcjn/rustchain-bounties)
[![BCOS Certified](https://img.shields.io/badge/BCOS-Certified-brightgreen?style=flat)](https://github.com/nicholaelaw/awesome-bcos)

**RustChain Proof-of-Antiquity miner for the IBM 701 - IBM's first commercial scientific computer**

## 🏆 Bounty Information

- **Issue**: [#375](https://github.com/Scottcjn/rustchain-bounties/issues/375)
- **Tier**: LEGENDARY
- **Reward**: 200 RTC ($20 USD)
- **Multiplier**: 5.0× (MAXIMUM - Museum Tier)
- **Wallet**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`

---

## 📋 Overview

This is a **Python simulator and miner** for the **IBM 701 Electronic Data Processing Machine**, announced on May 21, 1952. The IBM 701 was IBM's **first commercial scientific computer** and its **first series production mainframe computer**.

### ⚠️ Important Disclaimer

This implementation demonstrates the RustChain Proof-of-Antiquity protocol on one of history's most significant early computers. **Real mining is impractical** due to IBM 701's hardware constraints:

- Vacuum tubes (4,000+ tubes)
- Williams tube memory (2048 words × 36 bits, CRT storage)
- 36-bit word length
- 18-bit instructions (2 per word)
- No network capabilities (predates Ethernet by ~20 years)
- No SHA-256 support (cryptographic hash functions didn't exist in 1952)

---

## 🏛️ IBM 701 Architecture

| Feature | Specification |
|---------|---------------|
| **Announced** | May 21, 1952 |
| **Developer** | Jerrier Haddad, Nathaniel Rochester |
| **Based On** | IAS Machine (Princeton) |
| **Memory** | 2048 words × 36 bits (Williams tubes) |
| **Williams Tubes** | 72 tubes × 1024 bits each |
| **Word Size** | 36 bits |
| **Instruction Size** | 18 bits (2 per word) |
| **Technology** | Vacuum tubes (4,000+) |
| **Add Time** | ~60 microseconds |
| **Multiply Time** | ~300 microseconds |
| **Memory Access** | ~12 microseconds |
| **Rental Price** | $12,000-15,000/month (~$144k-180k in 2025) |
| **Units Shipped** | 19 |

### Historical Context

The IBM 701 competed with Remington Rand's **UNIVAC 1103** in the scientific computation market. It was used for:
- Nuclear weapons calculations (Lawrence Livermore National Laboratory)
- Aircraft design (8 went to aircraft companies)
- Weather prediction
- Scientific research

**Fun Fact**: The famous quote "I think there is a world market for maybe five computers" (often misattributed to Thomas Watson Sr.) actually came from Thomas Watson Jr. at the 1953 IBM stockholders' meeting, referring to the IBM 701: *"as a result of our trip, on which we expected to get orders for five machines, we came home with orders for 18"*.

---

## 🏗️ Technical Architecture

### Memory System

```
┌─────────────────────────────────────────────────────────┐
│           WILLIAMS TUBE MEMORY BANK                     │
├─────────────────────────────────────────────────────────┤
│  72 CRT tubes × 1024 bits each = 73,728 bits total     │
│  Organized as: 2048 words × 36 bits                    │
│  Each word: 36 bits (sign + magnitude)                 │
│  Access time: ~12 μs                                    │
│  Refresh required: continuous (~100 Hz)                 │
│  Temperature sensitive: requires frequent calibration   │
└─────────────────────────────────────────────────────────┘
```

### Memory Map

```
Address Range    Usage
─────────────────────────────────────────────────────
0x000-0x03F      System reserved / Bootstrap
0x040-0x0FF      Miner program
0x100-0x1FF      Epoch counters
0x200-0x2FF      Wallet address storage
0x300-0x3FF      Working registers / Hash state
0x400-0x4FF      Nonce counter
0x500-0x5FF      Attestation buffer
...
0x7FF            Final word (2048 total)
```

### CPU Registers

| Register | Size | Description |
|----------|------|-------------|
| **AC** (Accumulator) | 36 bits | Primary arithmetic register |
| **MQ** (Multiplier/Quotient) | 36 bits | Multiplication/division auxiliary |
| **IBR** (Instruction Buffer) | 18 bits | Holds second instruction from word |
| **PC** (Program Counter) | 11 bits | Address of next instruction (0-2047) |
| **IR** (Instruction Register) | 18 bits | Current instruction |

---

## 📜 Instruction Set

IBM 701 used 18-bit instructions with the following format:

```
┌─────┬───┬───────────┐
│ OP  │ I │  Address  │
│ 8b  │1b │   10b     │
└─────┴───┴───────────┘
OP = Opcode (8 bits)
I  = Immediate flag (1 bit)
Address = Memory address (10 bits, 0-1023)
```

| Opcode | Mnemonic | Description | Cycles |
|--------|----------|-------------|--------|
| `0x00` | STOP | Halt execution | 1 |
| `0x01` | ADD | Add memory to AC | 3 |
| `0x02` | SUB | Subtract from AC | 3 |
| `0x03` | MUL | Multiply MQ by memory | 15 |
| `0x04` | DIV | Divide AC by memory | 25 |
| `0x05` | AND | Bitwise AND | 2 |
| `0x06` | OR | Bitwise OR | 2 |
| `0x07` | JMP | Unconditional jump | 2 |
| `0x08` | JZ | Jump if zero | 2 |
| `0x09` | JN | Jump if negative | 2 |
| `0x0A` | LD | Load from memory | 2 |
| `0x0B` | ST | Store to memory | 2 |
| `0x0C` | IN | Input from card/tape | 100+ |
| `0x0D` | OUT | Output to printer/tape | 100+ |
| `0x0E` | RSH | Right shift | 2 |
| `0x0F` | LSH | Left shift | 2 |

---

## 🔄 Mining State Machine

```
┌─────────────────────────────────────────────────────────┐
│                  IBM 701 MINER STATES                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌──────┐      ┌─────────┐      ┌──────────┐         │
│   │ IDLE │─────▶│ MINING  │─────▶│ATTESTING │         │
│   │ (0)  │      │   (1)   │      │   (2)    │         │
│   └──────┘      └─────────┘      └──────────┘         │
│      ▲                                │                │
│      └────────────────────────────────┘                │
│           [attestation complete]                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

| State | Code | Description | Williams Pattern |
|-------|------|-------------|------------------|
| **IDLE** | 0 | Waiting for epoch trigger | `0000...0000` |
| **MINING** | 1 | Computing proof-of-antiquity | `0000...0001` |
| **ATTESTING** | 2 | Generating attestation | `0000...0010` |

---

## 📁 Project Structure

```
ibm701-miner/
├── README.md                    # This file
├── ARCHITECTURE.md              # Technical specification
├── WILLIAMS_TUBE.md             # Williams tube memory details
├── IBM701_INSTRUCTIONS.md       # IBM 701 instruction set reference
├── ibm701_simulator.py          # Main Python simulator
├── ibm701_miner.py              # RustChain miner implementation
├── ibm701_assembler.py          # Assembly language support
├── mining_routine.asm           # IBM 701 assembly mining routine
├── test_ibm701.py               # Test suite
├── wallet.txt                   # Generated wallet address
└── LICENSE
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- No external dependencies (pure Python implementation)

### Run the Miner

```bash
# Clone and navigate to directory
cd ibm701-miner

# Run the IBM 701 miner simulator
python ibm701_miner.py

# First run will generate wallet
# Wallet saved to: wallet.txt
# BACKUP THIS FILE!
```

### Configuration

Create `ibm701_config.ini`:

```ini
[rustchain]
node_url = https://node.rustchain.org
epoch_duration = 300
dev_fee = 0.001

[ibm701_emulation]
memory_size = 2048
word_bits = 36
instruction_bits = 18
williams_tube_count = 72
clock_hz = 16666  ; ~60μs add time
vacuum_tube_warmup = true
```

---

## 💰 RustChain Antiquity Multiplier

The IBM 701 represents **museum-tier antiquity** - the highest possible tier:

| Era | Multiplier | Example |
|-----|------------|---------|
| Modern (2020+) | 1.0× | Apple Silicon |
| Vintage (2000-2010) | 1.5× | Core 2 Duo |
| Ancient (1980-1999) | 2.0× | PowerPC G3 |
| Classic (1960-1979) | 3.0× | IBM 360 |
| Pioneer (1950-1959) | 4.0× | IBM 701 |
| **Museum (pre-1960, operational)** | **5.0×** | **IBM 701** |

**IBM 701 Multiplier: 5.0× (MAXIMUM)**

### Expected Earnings (Theoretical)

| Metric | Value |
|--------|-------|
| Base reward | 0.12 RTC/epoch |
| With 5.0× multiplier | 0.60 RTC/epoch |
| Per day (144 epochs) | 86.4 RTC |
| Per month | ~2,592 RTC |
| Per year | ~31,104 RTC |

At $0.10/RTC: **~$3,110/year** in mining rewards.

---

## ⚡ Performance Comparison

| Operation | IBM 701 | Modern CPU | Ratio |
|-----------|---------|------------|-------|
| Addition | 60 μs | ~1 ns | 60,000:1 |
| Multiplication | 300 μs | ~3 ns | 100,000:1 |
| Memory Access | 12 μs | ~100 ns | 120:1 |
| SHA-256 Hash | ∞ (not possible) | ~10 ns | ∞ |

**Conclusion**: Real mining is impractical. This is a **conceptual demonstration** honoring IBM 701's legacy.

---

## 🔧 Technical Implementation Details

### 36-Bit Word Format

IBM 701 used 36-bit words in sign-magnitude format:

```
┌───┬───────────────────────────────────┐
│ S │ 35-bit magnitude                  │
└───┴───────────────────────────────────┘
S = Sign bit (0=positive, 1=negative)
```

### Williams Tube Refresh

Williams tube memory required constant refreshing:

```python
def refresh_williams_tubes():
    """
    Williams tubes store data as charged spots on CRT phosphor.
    Charge dissipates over time (~20ms), requiring refresh.
    """
    for word_address in range(2048):
        word = read_word(word_address)
        # Read operation restores charge
        write_word(word_address, word)
```

### Vacuum Tube Characteristics

The IBM 701 used over 4,000 vacuum tubes, which created unique timing characteristics:

```python
class VacuumTubeTiming:
    """Simulates vacuum tube timing variance for entropy"""
    
    def __init__(self):
        self.warmup_time = 300  # 5 minutes warmup
        self.thermal_drift = random.gauss(0, 0.03)  # 3% variance
        
    def get_operation_time(self, base_time: float) -> float:
        """Add authentic vacuum tube timing variance"""
        return base_time * (1.0 + self.thermal_drift)
```

---

## 📺 I/O Systems

IBM 701 used punched cards and magnetic tape for I/O. The network interface would work like this:

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   IBM 701   │────▶│ Punched Card │────▶│ Microcontroller│
│  Computer   │◀────│ Punch/Reader │◀────│ (Network Bridge)│
└─────────────┘     └──────────────┘     └─────────────┘
                                              │
                                              ▼
                                       ┌─────────────┐
                                       │  Internet   │
                                       │  (HTTPS)    │
                                       └─────────────┘
```

### Punched Card Format

IBM 701 used standard 80-column punched cards:

```
┌─────────────────────────────────────────────────────────┐
│  IBM 701 PUNCHED CARD FORMAT                            │
├─────────────────────────────────────────────────────────┤
│  80 columns × 12 rows (Hollerith code)                 │
│  Each card: 80 characters or numeric data              │
│  Program cards: Binary encoded instructions            │
│  Data cards: Numeric values in columns                 │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Sample IBM 701 Assembly Code

```assembly
; IBM 701 Miner - Main Loop
; Stored at memory address 0x040

START,  LD  EPOCH       ; Load epoch counter
        ADD ONE         ; Increment epoch
        ST  EPOCH       ; Store back
        LD  STATE       ; Load current state
        CMP MINING      ; Compare to MINING state
        JMP CHECK_MINING
        
        ; IDLE state - print status
        OUT IDLE_MSG    ; Output "IDLE"
        JMP START

CHECK_MINING,
        JZ  DO_MINING   ; If zero, start mining
        JMP START

DO_MINING,
        ; Mining computation (simplified)
        LD  NONCE       ; Load nonce
        ADD INCREMENT   ; Add increment
        ST  NONCE       ; Store nonce
        ; ... hash computation would go here
        
        ; Transition to ATTESTING
        LD  STATE       ; Load state
        LD  ATTESTING   ; Load ATTESTING value
        ST  STATE       ; Store new state
        
ATTEST, OUT ATTEST_MSG  ; Output "ATTEST"
        OUT EPOCH       ; Output epoch number
        OUT WALLET      ; Output wallet address
        LD  ZERO        ; Load 0
        ST  STATE       ; Reset to IDLE
        JMP START

; Data Section
EPOCH:      0           ; Epoch counter
STATE:      0           ; Current state (0=IDLE, 1=MINING, 2=ATTESTING)
NONCE:      0           ; Nonce counter
ZERO:       0           ; Constant zero
ONE:        1           ; Constant one
INCREMENT:  1           ; Nonce increment
IDLE_MSG:   "IDLE"      ; Status message
ATTEST_MSG: "ATTEST"    ; Attestation message
WALLET:     RTC4325af95d26d59c3ef025963656d22af638bb96b
```

---

## 🏛️ Historical Context

### Development Team

- **Jerrier Haddad**: Chief engineer, led the IBM 701 development
- **Nathaniel Rochester**: IBM's first chief architect, designed the architecture
- **Based on**: IAS machine from Princeton (von Neumann architecture)

### Historical Achievements

- **1952**: Announced May 21, first commercial scientific computer
- **1953**: First delivery to IBM world headquarters, New York
- **1953-1956**: 19 units shipped total
- **Applications**: Nuclear weapons, aircraft design, weather prediction
- **Legacy**: First of the IBM 700/7000 series, predecessor to System/360

### The "Five Computers" Quote

At the 1953 IBM annual stockholders' meeting, Thomas Watson Jr. said:
*"as a result of our trip, on which we expected to get orders for five machines, we came home with orders for 18"*

This was about the IBM 701, and became misquoted as "I think there is a world market for maybe five computers" - attributed to his father Thomas Watson Sr.

---

## ✅ Implementation Checklist

- [x] **Williams tube memory emulation** (2048×36 bits)
- [x] **IBM 701 CPU simulation** (IAS-derived instruction set)
- [x] **18-bit instruction encoding** (2 per 36-bit word)
- [x] **Vacuum tube timing characteristics**
- [x] **Mining state machine**
- [x] **Attestation generation**
- [x] **Historical documentation**
- [x] **Wallet address included**
- [x] **Assembly language support**

---

## 📚 References

- [IBM 701 - Wikipedia](https://en.wikipedia.org/wiki/IBM_701)
- [Williams-Kilburn Tube - Wikipedia](https://en.wikipedia.org/wiki/Williams%E2%80%93Kilburn_tube)
- [IAS Machine - Wikipedia](https://en.wikipedia.org/wiki/IAS_machine)
- [IBM 700/7000 Series - Wikipedia](https://en.wikipedia.org/wiki/IBM_700/7000_series)
- [BITSavers IBM 701 Documentation](http://bitsavers.org/pdf/ibm/701/)
- [Computer History Museum](https://computerhistory.org/)
- [RustChain Documentation](https://github.com/Scottcjn/Rustchain)

---

## 🙏 Acknowledgments

- **Jerrier Haddad and Nathaniel Rochester** for IBM 701 design
- **IBM** for pioneering commercial computing
- **BITSavers** for preserving historical documentation
- **Computer History Museum** for preserving IBM 701 heritage
- **RustChain Foundation** for the LEGENDARY tier bounty

---

## 📄 License

MIT License - See LICENSE file for details.

---

## 💬 Contact

**Wallet Address**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`

**Bounty**: #375 - Port RustChain Miner to IBM 701 (1952)

**Tier**: LEGENDARY (200 RTC / $20)

---

*The IBM 701 (1952) represents a pivotal moment in computing history - IBM's entry into the commercial electronic computer age. While it cannot mine cryptocurrency practically, this implementation honors its legacy by demonstrating that Proof-of-Antiquity applies to the earliest commercial computers.*

**Built with ❤️ and 4,000+ vacuum tubes**

*Your vintage hardware earns rewards. Make mining meaningful again.*

🖥️ **IBM forever!** 🖥️
