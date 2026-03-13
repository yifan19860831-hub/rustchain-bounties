; ============================================================================
; RustChain Amiga 500 - Hardware Fingerprint Routines
; ============================================================================
; Optimized 68000 assembly for Amiga hardware detection
; Assembles with: vasmm68k_mot -Fbin -o fingerprint.o fingerprint.asm
;                 OR devpac fingerprint.asm
;
; These routines provide fast, low-level access to Amiga hardware
; for Proof-of-Antiquity attestation.
; ============================================================================

        SECTION code,CODE
        XDEF _rom_checksum_asm
        XDEF _vblank_wait
        XDEF _copper_timing_test
        XDEF _chipram_test_asm

; ============================================================================
; rom_checksum_asm
; ============================================================================
; Calculate ROM checksum using optimized assembly loop
; Input:  A0 = ROM base address (default: $F80000)
;         D0 = length in bytes (default: 262144 = 256KB)
; Output: D0 = 32-bit checksum
; ============================================================================

_rom_checksum_asm:
        MOVEM.L D2-D7,-(SP)     ; Save registers
        
        LEA     $F80000,A0      ; ROM base address
        MOVE.L  #262144,D7      ; 256KB to sum
        CLR.L   D0              ; Clear checksum accumulator

.rom_loop:
        MOVE.B  (A0),D1         ; Get byte from ROM
        ADD.L   D1,D0           ; Add to checksum
        ADDQ.L  #2,A0           ; Skip every other byte (word alignment)
        SUBQ.L  #1,D7           ; Decrement counter
        BNE.S   .rom_loop       ; Continue until done
        
        MOVEM.L (SP)+,D2-D7     ; Restore registers
        RTS

; ============================================================================
; vblank_wait
; ============================================================================
; Wait for specified number of VBlank interrupts
; Input:  D0 = number of VBlanks to wait
; Output: D0 = actual VBlanks waited
; Uses:   VPOSR register at $DFF004
; ============================================================================

_vblank_wait:
        MOVEM.L D2-D3,-(SP)
        
        MOVE.L  D0,D3           ; Store target count
        CLR.L   D0              ; Clear counter
        
        LEA     $DFF004,A0      ; VPOSR register

.vblank_loop:
        MOVE.W  (A0),D1         ; Read VPOSR
        AND.W   #$8000,D1       ; Check VBlank bit
        BEQ.S   .vblank_loop    ; Wait for VBlank
        
        ADDQ.L  #1,D0           ; Increment counter
        CMP.L   D3,D0           ; Check if done
        BLT.S   .vblank_loop    ; Continue if not done
        
        MOVE.L  D0,D0           ; Return count
        MOVEM.L (SP)+,D2-D3
        RTS

; ============================================================================
; copper_timing_test
; ============================================================================
; Measure Copper coprocessor access timing
; Output: D0 = timing value (unique to real Amiga hardware)
; ============================================================================

_copper_timing_test:
        MOVEM.L D2-D7,-(SP)
        
        CLR.L   D0              ; Clear accumulator
        LEA     $DFF044,A0      ; DSKDATR register
        MOVEQ   #1000,D7        ; 1000 iterations

.copper_loop:
        MOVE.W  (A0),D1         ; Read chipset register
        ADD.L   D1,D0           ; Accumulate
        DBRA    D7,.copper_loop ; Decrement and branch
        
        MOVE.L  D0,D0           ; Return result
        MOVEM.L (SP)+,D2-D7
        RTS

; ============================================================================
; chipram_test_asm
; ============================================================================
; Test for Chip RAM availability using Exec AllocMem
; Input:  D0 = size to allocate (bytes)
; Output: D0 = 1 if Chip RAM available, 0 if not
; ============================================================================

_chipram_test_asm:
        MOVEM.L D2-D3/A2,-(SP)
        
        MOVE.L  4,A6            ; ExecBase
        MOVE.L  D0,D3           ; Save size
        
        ; Try to allocate Chip RAM
        MOVE.L  D3,D0           ; Size
        MOVE.L  #$00000002,D1   ; MEMF_CHIP flag
        JSR     -198(A6)        ; AllocMem
        
        TST.L   D0              ; Check if allocation succeeded
        BEQ.S   .no_chipram     ; Branch if NULL
        
        ; Free the memory
        MOVE.L  D3,D0           ; Size
        MOVE.L  D0,-(SP)        ; Save size
        MOVE.L  D1,-(SP)        ; Save pointer
        JSR     -210(A6)        ; FreeMem
        ADDQ.L  #8,SP
        
        MOVEQ   #1,D0           ; Return success
        BRA.S   .done

.no_chipram:
        MOVEQ   #0,D0           ; Return failure

.done:
        MOVEM.L (SP)+,D2-D3/A2
        RTS

        END
