# Motorola 6809 Quick Reference

## Register Summary

| Register | Size | Description |
|----------|------|-------------|
| A | 8-bit | Accumulator A |
| B | 8-bit | Accumulator B |
| D | 16-bit | Double accumulator (A:B) |
| X | 16-bit | Index register X |
| Y | 16-bit | Index register Y |
| S | 16-bit | System stack pointer |
| U | 16-bit | User stack pointer |
| PC | 16-bit | Program counter |
| DP | 8-bit | Direct page register |

## Condition Code Register (CCR)

| Bit | Name | Description |
|-----|------|-------------|
| 7 | F | Entire flag (disable interrupts) |
| 6 | H | Half carry |
| 5 | I | IRQ mask |
| 4 | N | Negative |
| 3 | Z | Zero |
| 2 | V | Overflow |
| 1 | - | Unused |
| 0 | C | Carry |

## Key Instructions for Mining

### Load/Store

```
LDA  <addr>    ; Load A from memory
STA  <addr>    ; Store A to memory
LDD  <addr>    ; Load D (16-bit)
STD  <addr>    ; Store D (16-bit)
LDX  <addr>    ; Load X
STX  <addr>    ; Store X
```

### Arithmetic

```
ADDA <addr>    ; Add to A
ADDB <addr>    ; Add to B
ADDD <addr>    ; Add to D
SUBA <addr>    ; Subtract from A
SUBB <addr>    ; Subtract from B
SUBD <addr>    ; Subtract from D
MUL            ; Multiply A × B → D (10-11 cycles!)
```

### Logic

```
EORA <addr>    ; XOR with A
EORB <addr>    ; XOR with B
EORD <addr>    ; XOR with D
COMA           ; Complement A
COMB           ; Complement B
```

### Shift/Rotate

```
LSRA           ; Logical shift right A
LSRB           ; Logical shift right B
LSRD           ; Logical shift right D
ASLA           ; Arithmetic shift left A
ASLB           ; Arithmetic shift left B
ROLA           ; Rotate left A
RORA           ; Rotate right A
```

### Branch

```
BEQ  <label>   ; Branch if equal (Z=1)
BNE  <label>   ; Branch if not equal (Z=0)
BGT  <label>   ; Branch if greater than
BLT  <label>   ; Branch if less than
BRA  <label>   ; Branch always
BSR  <label>   ; Branch to subroutine
```

### Stack Operations

```
PSHS <regs>    ; Push registers to stack
PULS <regs>    ; Pull registers from stack
PSHU <regs>    ; Push registers to U stack
PULU <regs>    ; Pull registers from U stack
```

### Interrupt Control

```
CLI            ; Clear I flag (enable IRQ)
SEI            ; Set I flag (disable IRQ)
RTI            ; Return from interrupt
SWI            ; Software interrupt
```

## Addressing Modes

| Mode | Syntax | Example | Description |
|------|--------|---------|-------------|
| Immediate | #value | LDA #$FF | Load immediate value |
| Direct | <addr | LDA $80 | Direct page (8-bit addr) |
| Extended | <addr | LDA $1234 | Full 16-bit address |
| Indexed | ,X | LDA ,X | Indexed by X |
| Post-inc | ,X+ | LDA ,X+ | Indexed, then increment X |
| Pre-dec | ,-X | LDA ,-X | Decrement X, then indexed |
| PC-relative | <label | LDA label | Relative to PC |

## Timing Reference

| Instruction | Cycles |
|-------------|--------|
| LDA (imm) | 2 |
| LDA (dir) | 3 |
| LDA (ext) | 4 |
| STA (dir) | 4 |
| ADDA (imm) | 2 |
| MUL | 10-11 |
| BRA | 3 |
| BEQ (taken) | 3 |
| BEQ (not taken) | 3 |
| BSR | 7 |
| JSR (ext) | 7 |
| RTS | 5 |
| RTI | 9-13 |

## Example: Simple Hash Loop

```assembly
; Hash computation loop
HASH_LOOP:
    LDD     EPOCH       ; Load epoch
    EORA    HW_ID       ; XOR with hardware ID
    EORB    HW_ID+1     
    LDX     NONCE       ; Load nonce
    EORA    XL          ; XOR with nonce low
    EORB    XH          ; XOR with nonce high
    MUL                 ; A × B → D
    EORA    B           ; Mix result
    STD     HASH        ; Store hash
    
    ; Check target
    CMPX    TARGET      
    BGT     NO_PROOF    ; Not valid
    
    ; Valid proof!
    JSR     SUBMIT      
    
NO_PROOF:
    INC     NONCE       ; Next nonce
    BRA     HASH_LOOP   ; Continue
```

## Interrupt Vectors

| Address | Vector | Purpose |
|---------|--------|---------|
| $FFF6 | RESET | Power-on reset |
| $FFF4 | NMI | Non-maskable interrupt |
| $FFF2 | SWI3 | Software interrupt 3 |
| $FFF0 | SWI2 | Software interrupt 2 |
| $FFEE | FIRQ | Fast interrupt request |
| $FFEC | IRQ | Interrupt request |
| $FFEA | SWI | Software interrupt |

## Joust-Specific Notes

- **VBLANK**: ~60Hz (NTSC) or ~50Hz (PAL)
- **ROM Base**: Typically $C000 or $E000
- **RAM Base**: Typically $0000-$0FFF
- **Video Register**: Hypothetical $FF00 for status

## Resources

- [Motorola 6809 Datasheet](https://archive.org/details/bitsavers_motorolada_3224333)
- [6809 Programming Manual](https://archive.org/details/bitsavers_motorola68_13419254)
- [6809 Emulation Page](http://atjs.great-site.net/mc6809/)

---

*Quick reference for Joust Miner development*
