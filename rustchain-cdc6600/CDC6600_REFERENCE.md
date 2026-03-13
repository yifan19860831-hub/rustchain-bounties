# CDC 6600 Architecture Quick Reference

## Core Specifications
| Property | Value |
|----------|-------|
| Word Size | 60 bits |
| Clock | 10 MHz (100ns) |
| Memory | 131K words (982 KB) |
| Performance | 3 MFLOPS |
| Release | 1964 |
| Designer | Seymour Cray |

## Registers

### X Registers (60-bit operands)
- X0: Always zero
- X1-X5: Read operands
- X6-X7: Write results

### A Registers (18-bit addresses)
- A0: No side effect
- A1-A5: Read addresses
- A6-A7: Write addresses

### B Registers (18-bit increments)
- B0: Always zero
- B1-B7: General purpose

## Key Instructions

| Mnemonic | Operation | Cycles |
|----------|-----------|--------|
| LXK i,K | X[i] = K (immediate) | 1 |
| LD i,d(j) | X[i] = mem[A[j]+d] | 8 |
| SD i,d(j) | mem[A[j]+d] = X[i] | 8 |
| ADD i,j,k | X[k] = X[i] + X[j] | 4 |
| FMP i,j,k | FP multiply | 10 |
| J label | Jump | 2 |
| BP label | Branch if positive | 2 |
| ANA i,j,k | X[k] = X[i] AND X[j] | 2 |
| ORA i,j,k | X[k] = X[i] OR X[j] | 2 |

## Number Formats

### 60-bit Integer (Ones' Complement)
- Bit 59: Sign
- Bits 58-0: Magnitude
- Range: ±(2^59 - 1)

### 60-bit Floating Point
- Bit 59: Sign
- Bits 58-48: Exponent (11 bits, excess-1024)
- Bits 47-0: Mantissa (48 bits)

## Peripheral Processors
- 10 PPs (PP0-PP9)
- 12-bit, 4KB each
- PP0: Control
- PP9: Console

## Memory Organization
```
0x000-0x0FF:   Bootstrap
0x100-0xFFF:   Code
0x1000-0x1FFF: Data
0x2000-0xFFFF: Extended (ECS)
```

## Functional Units (10 parallel)
- FP Multiply ×2
- FP Divide ×1
- FP Add ×1
- Long Add ×1
- Incrementer ×2
- Shift ×1
- Boolean ×1
- Branch ×1

---

*For RustChain CDC 6600 Miner Port*  
*Bounty: 200 RTC - LEGENDARY Tier*
