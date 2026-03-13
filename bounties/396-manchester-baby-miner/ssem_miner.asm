; Manchester Baby (SSEM) Miner - Assembly Source
; Issue #396 - Port Miner to Manchester Baby
; Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b
;
; Architecture Constraints:
;   - 32 words × 32-bit memory (1 kilobit total)
;   - 7 instructions: JMP, JRP, LDN, STO, SUB, CMP, STP
;   - Only subtraction and negation in hardware
;   - ~700 instructions/second
;   - Programs entered via 32 toggle switches
;
; Memory Layout:
;   Addr 0-18:   Program code (19 words)
;   Addr 19:     Block data (input)
;   Addr 20:     Difficulty threshold
;   Addr 21:     Nonce counter
;   Addr 22:     Working hash storage
;   Addr 23:     Result storage
;   Addr 24:     Constant -1 (for incrementing)
;   Addr 25-31:  Spare working memory

; ============================================================
; PROGRAM CODE (Addresses 0-18)
; ============================================================

; Address 0: Initialize nonce to 0
; LDN 24 - Load negative of address 24 (which is 0 at start)
00000000000110001000000000000000  ; LDN 24

; Address 1: Store initial nonce
; STO 21 - Store accumulator at nonce location
00000000000101011100000000000000  ; STO 21

; Address 2: MAIN LOOP - Load block data
; LDN 19 - Load negative block data
00000000000100111000000000000000  ; LDN 19

; Address 3: Subtract nonce (simulating hash operation)
; SUB 21 - Subtract nonce from accumulator
00000000000101010010000000000000  ; SUB 21

; Address 4: Store intermediate hash
; STO 22 - Store at working hash location
00000000000101101100000000000000  ; STO 22

; Address 5: Load hash for difficulty check
; LDN 22 - Load negative hash
00000000000101101000000000000000  ; LDN 22

; Address 6: Subtract difficulty threshold
; SUB 20 - Subtract difficulty
00000000000101000010000000000000  ; SUB 20

; Address 7: Compare result
; CMP - Skip next instruction if accumulator < 0
00000000000000000000001100000000  ; CMP

; Address 8: Jump to increment if hash >= difficulty
; JRP 12 - Jump relative to address (8 + value at 12)
; Value at 12 should be: target_addr - current_addr - 1 = 11 - 8 - 1 = 2
00000000000000010100000000000000  ; JRP (relative +2 → addr 11)

; Address 9: SUCCESS - Store winning nonce
; STO 23 - Store result
00000000000101111100000000000000  ; STO 23

; Address 10: Stop - mining complete!
; STP - Halt execution
00000000000000000000011100000000  ; STP

; Address 11: (Skipped on success, used for jump target)
; This is where we land if hash >= difficulty

; Address 12: Relative jump offset for JRP at addr 8
; Target: addr 14 (increment section)
; Offset: 14 - 8 - 1 = 5
00000000000000000000000000000101  ; Constant: 5

; Address 13: Increment nonce section
; LDN 21 - Load negative nonce
00000000000101011000000000000000  ; LDN 21

; Address 14: Subtract -1 (effectively add 1)
; SUB 24 - Subtract constant -1
00000000000110000010000000000000  ; SUB 24

; Address 15: Store incremented nonce
; STO 21 - Store back to nonce location
00000000000101011100000000000000  ; STO 21

; Address 16: Jump back to main loop
; JRP - Jump relative to addr 2
; Offset: 2 - 16 - 1 = -15 (in two's complement: -15)
11111111111100010100000000000000  ; JRP (relative -15 → addr 2)

; Address 17: Overflow protection (simplified)
; In practice, Baby would wrap around naturally
; STP - Stop if we ever reach here
00000000000000000000011100000000  ; STP

; Address 18: Padding / unused
00000000000000000000000000000000  ; NOP (unused)

; ============================================================
; DATA STORAGE (Addresses 19-31)
; ============================================================

; Address 19: Block data (INPUT - set via toggle switches)
; Example: 0xDEADBEEF = 11011110101011011011111011101111
; In Baby format (LSB first): 11110111011110110101011110110110
11110111011110110101011110110110  ; Block data: 0xDEADBEEF

; Address 20: Difficulty threshold (INPUT)
; Example: 0x0000FFFF = easier difficulty for demo
; LSB first: 11111111111111110000000000000000
11111111111111110000000000000000  ; Difficulty: 0x0000FFFF

; Address 21: Nonce counter (initialized to 0)
00000000000000000000000000000000  ; Nonce: 0 (runtime variable)

; Address 22: Working hash storage
00000000000000000000000000000000  ; Hash: 0 (runtime variable)

; Address 23: Result storage
00000000000000000000000000000000  ; Result: 0 (output)

; Address 24: Constant -1 (for incrementing nonce)
; -1 in 32-bit two's complement: all 1s
11111111111111111111111111111111  ; Constant: -1

; Address 25: Spare working memory
00000000000000000000000000000000  ; Spare

; Address 26: Spare working memory
00000000000000000000000000000000  ; Spare

; Address 27: Spare working memory
00000000000000000000000000000000  ; Spare

; Address 28: Spare working memory
00000000000000000000000000000000  ; Spare

; Address 29: Spare working memory
00000000000000000000000000000000  ; Spare

; Address 30: Spare working memory
00000000000000000000000000000000  ; Spare

; Address 31: Spare working memory
00000000000000000000000000000000  ; Spare

; ============================================================
; END OF PROGRAM
; ============================================================

; To run on real Manchester Baby:
; 1. Set toggle switches for each address (0-31)
; 2. Press "Load" to store each word
; 3. Set program counter to 0
; 4. Press "Start"
; 5. Wait ~1-2 hours for result (depending on difficulty)
; 6. Read result from address 23 on CRT display

; Estimated execution:
; - Instructions per hash attempt: ~15
; - Hash attempts per second: ~45
; - Time for 1M attempts: ~6 hours
; - Time for 1B attempts: ~257 days

; This demonstrates the EXTREME nature of Proof-of-Antiquity!
