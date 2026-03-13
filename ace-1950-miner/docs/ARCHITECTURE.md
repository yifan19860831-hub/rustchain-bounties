# ACE Architecture Documentation

## Overview

The **ACE (Automatic Computing Engine)** was designed by **Alan Turing** in 1945-1946 and built at the National Physical Laboratory (NPL) in the UK. The Pilot ACE ran its first program on **May 10, 1950**.

## Technical Specifications

| Feature | Specification |
|---------|--------------|
| **Designer** | Alan Turing |
| **First Program** | May 10, 1950 |
| **Word Size** | 32 bits |
| **Memory Type** | Mercury delay lines |
| **Memory Capacity** | 128 words (original), 352 words (expanded) |
| **Clock Speed** | 1 MHz |
| **Vacuum Tubes** | ~800 |
| **Instruction Format** | 32-bit, two-address |
| **Arithmetic** | Fixed-point (floating-point added later) |

## Memory Architecture

### Mercury Delay Lines

ACE used **mercury delay line memory**, which stored data as acoustic waves in tubes filled with mercury. Key characteristics:

- **Serial Access**: Data circulates continuously; must wait for correct bit to emerge
- **Refresh Required**: Data must be constantly recirculated
- **Access Time**: ~32 bit cycles per word (1 MHz = 1μs per bit)
- **Temperature Sensitive**: Mercury properties vary with temperature

### Memory Map (Expanded Configuration)

```
Address Range    Size      Usage
0x00-0x1F        32 words  System & Boot
0x20-0x3F        32 words  Hash State (H0-H7) + Working
0x40-0x7F        64 words  Message Schedule (W0-W15) + K Constants
0x80-0xFF        128 words Program & Data
0x100-0x15F      96 words  Extended Data (if available)
```

## Instruction Set

### Format

```
Bits 31-26: Opcode (6 bits)
Bits 25-20: Source address (6 bits)
Bits 19-14: Destination address (6 bits)
Bits 13-0:  Reserved (14 bits)
```

### Core Instructions

| Opcode | Mnemonic | Description | Cycles |
|--------|----------|-------------|--------|
| 0x00 | NOP | No operation | 1 |
| 0x01 | ACH | Add to accumulator high | 3 |
| 0x02 | ACL | Add to accumulator low | 3 |
| 0x05 | SUB | Subtract from AL | 3 |
| 0x07 | LSH | Left shift accumulator | 2 |
| 0x08 | RSH | Right shift accumulator | 2 |
| 0x09 | AND | Logical AND | 2 |
| 0x0A | OR | Logical OR | 2 |
| 0x0B | NOT | Logical NOT | 2 |
| 0x0D | LD | Load from delay line | 3 |
| 0x0E | ST | Store to delay line | 3 |
| 0x0F | JMP | Unconditional jump | 2 |
| 0x10 | JZ | Jump if zero | 2 |
| 0x11 | JN | Jump if negative | 2 |
| 0x12 | STOP | Halt | 1 |
| 0x13 | LDQ | Load Q register | 3 |
| 0x14 | STQ | Store Q register | 3 |
| 0x15 | MLA | Multiply AL by source | 32+ |
| 0x16 | DIV | Divide AH:AL by source | 64+ |

### Instruction Timing

- **Simple instructions**: 1-3 cycles
- **Shift operations**: 2 cycles
- **Memory access**: 3 cycles (delay line latency)
- **Multiplication**: 32+ cycles (software implementation)
- **Division**: 64+ cycles (software implementation)

## Registers

### Accumulator (A)

64-bit register split into two 32-bit halves:
- **AH**: Accumulator high (bits 63-32)
- **AL**: Accumulator low (bits 31-0)

### Q Register

32-bit register used for:
- Multiplication (holds multiplier)
- Division (holds quotient)
- Temporary storage

### Program Counter (P)

Address of next instruction (6 bits, 0-63 for original memory).

### Status Flags

- **Zero (Z)**: Set when result is zero
- **Negative (N)**: Set when MSB is 1
- **Overflow (V)**: Set on arithmetic overflow

## SHA-256 Implementation Notes

### Advantages

1. **32-bit word size**: Perfect match for SHA-256's 32-bit operations
2. **Native rotations**: LSH/RSH instructions support bit rotation
3. **Logical operations**: AND, OR, NOT directly available

### Challenges

1. **Memory constraints**: 128 words insufficient; need expanded 352-word configuration
2. **No hardware multiply**: Software multiplication is slow (~32 cycles)
3. **Serial memory access**: Delay line timing requires careful instruction scheduling
4. **Limited registers**: Must frequently spill to memory

### Memory Requirements

| Component | Words | Description |
|-----------|-------|-------------|
| K constants | 64 | Round constants |
| Hash state (H) | 8 | Current hash value |
| Message schedule (W) | 64 | Extended message block |
| Working variables | 8 | a,b,c,d,e,f,g,h |
| **Total** | **144** | Minimum required |

### Optimization Strategies

1. **Delay line scheduling**: Place frequently accessed data in same delay line
2. **Instruction packing**: Minimize memory accesses
3. **Loop unrolling**: Reduce branch overhead
4. **Constant folding**: Pre-compute where possible

## Mining Protocol Integration

### Attestation Flow

1. **Receive challenge** from RustChain node (via network bridge)
2. **Compute hardware fingerprint**:
   - Vacuum tube timing characteristics
   - Thermal drift patterns
   - Delay line access patterns
3. **Generate SHA-256 proof**:
   - Hash challenge + fingerprint
   - Submit to node
4. **Earn RTC** based on authenticity score

### Network Bridge

Since ACE has no native networking, a bridge is required:
- **Input**: Paper tape or punch cards
- **Output**: Teleprinter or paper tape punch
- **Modern interface**: ESP32/Arduino bridge via GPIO

## Performance Estimates

### SHA-256 Compression Function

| Operation | Cycles | Time (1 MHz) |
|-----------|--------|--------------|
| Single round | ~200 | 200 μs |
| 64 rounds | ~12,800 | 12.8 ms |
| Full hash (1 block) | ~13,000 | 13 ms |
| Hashes per second | ~77 | |

### Mining Performance

- **Hash rate**: ~77 H/s (theoretical maximum)
- **Power consumption**: ~3 kW (vacuum tubes)
- **Efficiency**: 0.026 H/W

Note: This is purely educational/historical. Modern miners achieve TH/s rates.

## References

1. Turing, A.M. (1946). "ACE Report". National Physical Laboratory.
2. Wilkinson, J.H. (1951). "The Pilot ACE Computer". NPL.
3. Science Museum London. "Pilot ACE Exhibition".
4. Copeland, B.J. (2006). "Colossus: The Secrets of Bletchley Park".

---

**Document Version**: 1.0  
**Last Updated**: 2026-03-14  
**Author**: ACE Miner Project
