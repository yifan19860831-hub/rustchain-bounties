# Altair 8800 Architecture

## Historical Significance

The **Altair 8800**, introduced in January 1975 by MITS (Micro Instrumentation and Telemetry Systems), is widely recognized as the first personal computer. It sparked the microcomputer revolution and led directly to the founding of Microsoft (Bill Gates and Paul Allen wrote a BASIC interpreter for it).

## Technical Specifications

### CPU: Intel 8080

| Parameter | Value |
|-----------|-------|
| **Clock Speed** | 2 MHz |
| **Architecture** | 8-bit |
| **Data Bus** | 8 bits |
| **Address Bus** | 16 bits |
| **Addressable Memory** | 64 KB |
| **Registers** | A, B, C, D, E, H, L (8-bit each) |
| **Register Pairs** | BC, DE, HL, SP, PC (16-bit each) |
| **Flags** | Sign, Zero, Auxiliary Carry, Parity, Carry |

### Memory Architecture

```
Address Range    Usage
0x0000-0x00FF    Reset Vector & Interrupts
0x0100-0x7FFF    User RAM (typically 256B - 4KB base)
0x8000-0xEFFF    Expansion RAM (up to 64KB total)
0xF000-0xFFFF    ROM (monitor, BASIC)
```

### S-100 Bus

The Altair 8800 used the **S-100 bus** (also called Altair bus), a 100-pin connection that became the first industry-standard bus for microcomputers.

**Bus Signals:**
- 16 address lines (A0-A15)
- 8 data lines (D0-D7)
- Power: +8V, +16V, -16V
- Control: Clock, Interrupt, DMA, etc.

### I/O System

The Altair 8800 had no traditional keyboard or display. Instead:

**Input:**
- Front panel toggle switches (binary input)
- Paper tape reader (optional)
- Cassette interface (optional)

**Output:**
- Front panel LEDs (binary display)
- Paper tape punch (optional)
- Cassette interface (optional)
- Teletype (optional, via serial)

### Programming Model

**Intel 8080 Instruction Set:**
- 243 instructions total
- Data transfer (MOV, MVI, LXI, LDA, STA)
- Arithmetic (ADD, SUB, INR, DCR)
- Logical (ANA, ORA, XRA, CMP)
- Branching (JMP, CALL, RET, conditional jumps)
- Stack operations (PUSH, POP)
- I/O (IN, OUT)

**Example Program:**
```assembly
        LXI H, 0x8000    ; Load HL with address
        MVI A, 0x55      ; Load accumulator
        MOV M, A         ; Store at HL
        HLT              ; Halt
```

## Limitations for Modern Computing

### Why Cryptocurrency Mining is Impossible

1. **No 32-bit Arithmetic**
   - SHA-256 requires 32-bit operations
   - 8080 is purely 8-bit
   - Would need ~4x instructions per 32-bit op

2. **Memory Constraints**
   - SHA-256 needs working space for hash state
   - 64KB max vs modern GB requirements
   - No cache hierarchy

3. **No Hardware Multiplication**
   - Must implement in software
   - Extremely slow (hundreds of cycles)

4. **Clock Speed**
   - 2 MHz vs modern GHz processors
   - ~500-1000x slower

5. **No Network Connectivity**
   - No Ethernet, WiFi, or TCP/IP
   - Would need external modem (300 baud!)

### Theoretical Performance

If we could run SHA-256 on an 8080:

- **Estimated hashes/second**: ~0.001 H/s (1 hash per 1000 seconds)
- **Modern ASIC**: ~100 TH/s (100,000,000,000,000 H/s)
- **Performance ratio**: 1 : 100,000,000,000,000,000

## Educational Value

Despite its limitations, the Altair 8800 teaches:

1. **Computer Fundamentals**
   - How CPUs execute instructions
   - Memory addressing
   - I/O operations

2. **Assembly Programming**
   - Direct hardware control
   - Efficient coding (every byte counts)
   - Understanding the machine

3. **Historical Context**
   - Where personal computing began
   - Evolution of technology
   - Appreciation for modern capabilities

## Emulation Approach

This project uses a **Python-based emulator** that:

1. Simulates the Intel 8080 CPU
2. Models 64KB of RAM
3. Implements front panel I/O
4. Demonstrates mining conceptually

The emulator runs the 8080 assembly code and shows how mining *would* work if the hardware could support it.

---

*"The Altair 8800 didn't just start a company—it started an industry."*
