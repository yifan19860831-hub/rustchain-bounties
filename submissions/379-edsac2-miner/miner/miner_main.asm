; EDSAC 2 RustChain Miner - Main Program
; =======================================
; 
; This is the main miner program for EDSAC 2 (1958).
; It implements SHA256 double-hash mining for RustChain.
;
; Memory Layout:
;   0x000-0x01F: Boot and initialization
;   0x020-0x05F: SHA256 constants K[0..63]
;   0x060-0x06F: Hash state H[0..7]
;   0x070-0x0AF: Message schedule W[0..63]
;   0x0B0-0x0BF: Working variables a-h
;   0x0C0-0x0DF: Input buffer
;   0x0E0-0x0FF: Temporary storage
;   0x100-0x3FF: Code and stack
;
; Author: RustChain EDSAC 2 Miner Project
; License: MIT

; ============================================================
; BOOT SECTION
; ============================================================

        ORG 0x000
        
START:  JMP     INIT            ; Jump to initialization

; Interrupt vectors
        ORG 0x008
        STOP                    ; HALT vector

        ORG 0x010
        JMP     TAPE_INTERRUPT  ; Paper tape interrupt

; ============================================================
; SHA256 CONSTANTS (K table)
; ============================================================

        ORG 0x020

K_TABLE:
        DW 0x428a2f98   ; K[0]
        DW 0x71374491   ; K[1]
        DW 0xb5c0fbcf   ; K[2]
        DW 0xe9b5dba5   ; K[3]
        DW 0x3956c25b   ; K[4]
        DW 0x59f111f1   ; K[5]
        DW 0x923f82a4   ; K[6]
        DW 0xab1c5ed5   ; K[7]
        DW 0xd807aa98   ; K[8]
        DW 0x12835b01   ; K[9]
        DW 0x243185be   ; K[10]
        DW 0x550c7dc3   ; K[11]
        DW 0x72be5d74   ; K[12]
        DW 0x80deb1fe   ; K[13]
        DW 0x9bdc06a7   ; K[14]
        DW 0xc19bf174   ; K[15]
        DW 0xe49b69c1   ; K[16]
        DW 0xefbe4786   ; K[17]
        DW 0x0fc19dc6   ; K[18]
        DW 0x240ca1cc   ; K[19]
        DW 0x2de92c6f   ; K[20]
        DW 0x4a7484aa   ; K[21]
        DW 0x5cb0a9dc   ; K[22]
        DW 0x76f988da   ; K[23]
        DW 0x983e5152   ; K[24]
        DW 0xa831c66d   ; K[25]
        DW 0xb00327c8   ; K[26]
        DW 0xbf597fc7   ; K[27]
        DW 0xc6e00bf3   ; K[28]
        DW 0xd5a79147   ; K[29]
        DW 0x06ca6351   ; K[30]
        DW 0x14292967   ; K[31]
        DW 0x27b70a85   ; K[32]
        DW 0x2e1b2138   ; K[33]
        DW 0x4d2c6dfc   ; K[34]
        DW 0x53380d13   ; K[35]
        DW 0x650a7354   ; K[36]
        DW 0x766a0abb   ; K[37]
        DW 0x81c2c92e   ; K[38]
        DW 0x92722c85   ; K[39]
        DW 0xa2bfe8a1   ; K[40]
        DW 0xa81a664b   ; K[41]
        DW 0xc24b8b70   ; K[42]
        DW 0xc76c51a3   ; K[43]
        DW 0xd192e819   ; K[44]
        DW 0xd6990624   ; K[45]
        DW 0xf40e3585   ; K[46]
        DW 0x106aa070   ; K[47]
        DW 0x19a4c116   ; K[48]
        DW 0x1e376c08   ; K[49]
        DW 0x2748774c   ; K[50]
        DW 0x34b0bcb5   ; K[51]
        DW 0x391c0cb3   ; K[52]
        DW 0x4ed8aa4a   ; K[53]
        DW 0x5b9cca4f   ; K[54]
        DW 0x682e6ff3   ; K[55]
        DW 0x748f82ee   ; K[56]
        DW 0x78a5636f   ; K[57]
        DW 0x84c87814   ; K[58]
        DW 0x8cc70208   ; K[59]
        DW 0x90befffa   ; K[60]
        DW 0xa4506ceb   ; K[61]
        DW 0xbef9a3f7   ; K[62]
        DW 0xc67178f2   ; K[63]

; ============================================================
; INITIALIZATION
; ============================================================

        ORG 0x100

INIT:   ; Initialize hash state H
        LD      H_INIT_0
        ST      H0
        LD      H_INIT_1
        ST      H1
        LD      H_INIT_2
        ST      H2
        LD      H_INIT_3
        ST      H3
        LD      H_INIT_4
        ST      H4
        LD      H_INIT_5
        ST      H5
        LD      H_INIT_6
        ST      H6
        LD      H_INIT_7
        ST      H7
        
        ; Initialize nonce counter
        LD      ZERO
        ST      NONCE
        
        ; Clear statistics
        ST      HASH_COUNT
        ST      BLOCKS_FOUND
        
        ; Print startup message
        LD      MSG_INIT
        CALL    PRINT_STRING
        
        JMP     MINER_LOOP

; ============================================================
; MAIN MINER LOOP
; ============================================================

MINER_LOOP:
        ; Get new work from pool (via paper tape)
        CALL    GET_WORK_FROM_POOL
        
        ; Check if we got valid work
        LD      WORK_STATUS
        JZ      GOT_WORK
        JMP     MINER_LOOP              ; Retry if no work
        
GOT_WORK:
        ; Initialize nonce for this work
        LD      ZERO
        ST      NONCE
        
NONCE_LOOP:
        ; Build block header with current nonce
        CALL    BUILD_BLOCK_HEADER
        
        ; Compute SHA256(SHA256(header))
        CALL    SHA256_HASH
        CALL    SHA256_HASH             ; Double hash
        
        ; Increment hash counter
        LD      HASH_COUNT
        ADD     ONE
        ST      HASH_COUNT
        
        ; Check if hash meets difficulty target
        CALL    CHECK_DIFFICULTY
        JZ      FOUND_BLOCK             ; If zero, we found a block!
        
        ; Increment nonce
        LD      NONCE
        ADD     ONE
        ST      NONCE
        
        ; Check if nonce overflowed
        JZ      GET_NEW_WORK            ; If zero, try new work
        
        ; Check if we've tried enough nonces
        LD      NONCE
        SUB     MAX_NONCE_PER_WORK
        JN      NONCE_LOOP              ; Continue if not exhausted
        
GET_NEW_WORK:
        JMP     MINER_LOOP

; ============================================================
; BLOCK FOUND!
; ============================================================

FOUND_BLOCK:
        ; Print success message
        LD      MSG_BLOCK_FOUND
        CALL    PRINT_STRING
        
        ; Output nonce
        LD      NONCE
        CALL    PRINT_NUMBER
        
        ; Output block hash
        LD      HASH_RESULT
        CALL    PRINT_HASH
        
        ; Submit block to pool
        CALL    SUBMIT_BLOCK
        
        ; Increment blocks found counter
        LD      BLOCKS_FOUND
        ADD     ONE
        ST      BLOCKS_FOUND
        
        ; Continue mining
        JMP     MINER_LOOP

; ============================================================
; SHA256 HASH FUNCTION
; ============================================================

; Input: Block header in INPUT_BUFFER (64 bytes)
; Output: Hash in HASH_RESULT (32 bytes)
; Clobbers: All registers

SHA256_HASH:
        ; Save registers
        ST      SAVE_ACC
        
        ; Initialize working variables from hash state
        LD      H0
        ST      WORK_A
        LD      H1
        ST      WORK_B
        LD      H2
        ST      WORK_C
        LD      H3
        ST      WORK_D
        LD      H4
        ST      WORK_E
        LD      H5
        ST      WORK_F
        LD      H6
        ST      WORK_G
        LD      H7
        ST      WORK_H
        
        ; Prepare message schedule W[0..63]
        CALL    PREPARE_MESSAGE_SCHEDULE
        
        ; 64 rounds of SHA256
        LD      ZERO
        ST      ROUND_COUNTER
        
SHA256_ROUNDS:
        LD      ROUND_COUNTER
        SUB     SIXTYFOUR
        JZ      SHA256_ROUNDS_DONE
        
        ; Compute T1 = h + Σ1(e) + Ch(e,f,g) + K[i] + W[i]
        LD      WORK_H
        CALL    SIGMA1
        ST      TEMP_T1
        
        LD      WORK_E
        ST      REG_X
        LD      WORK_F
        ST      REG_Y
        LD      WORK_G
        ST      REG_Z
        CALL    CH_FUNCTION
        ADD     TEMP_T1
        
        ; Add K[i]
        LD      ROUND_COUNTER
        CALL    GET_K_CONSTANT
        ADD     ACC
        
        ; Add W[i]
        LD      ROUND_COUNTER
        CALL    GET_W_WORD
        ADD     ACC
        ST      TEMP_T1
        
        ; Compute T2 = Σ0(a) + Maj(a,b,c)
        LD      WORK_A
        CALL    SIGMA0
        ST      TEMP_T2
        
        LD      WORK_A
        ST      REG_X
        LD      WORK_B
        ST      REG_Y
        LD      WORK_C
        ST      REG_Z
        CALL    MAJ_FUNCTION
        ADD     TEMP_T2
        
        ; Update working variables
        ; h = g, g = f, f = e, e = d + T1, d = c, c = b, b = a, a = T1 + T2
        LD      WORK_G
        ST      WORK_H
        LD      WORK_F
        ST      WORK_G
        LD      WORK_E
        ST      WORK_F
        LD      WORK_D
        ADD     TEMP_T1
        ST      WORK_E
        LD      WORK_C
        ST      WORK_D
        LD      WORK_B
        ST      WORK_C
        LD      WORK_A
        ST      WORK_B
        LD      TEMP_T1
        ADD     TEMP_T2
        ST      WORK_A
        
        ; Increment round counter
        LD      ROUND_COUNTER
        ADD     ONE
        ST      ROUND_COUNTER
        JMP     SHA256_ROUNDS

SHA256_ROUNDS_DONE:
        ; Update hash state
        LD      H0
        ADD     WORK_A
        ST      H0
        LD      H1
        ADD     WORK_B
        ST      H1
        LD      H2
        ADD     WORK_C
        ST      H2
        LD      H3
        ADD     WORK_D
        ST      H3
        LD      H4
        ADD     WORK_E
        ST      H4
        LD      H5
        ADD     WORK_F
        ST      H5
        LD      H6
        ADD     WORK_G
        ST      H6
        LD      H7
        ADD     WORK_H
        ST      H7
        
        ; Restore registers
        LD      SAVE_ACC
        
        RETURN

; ============================================================
; HELPER FUNCTIONS
; ============================================================

; ROTR32 - 32-bit right rotation
; Input: ACC = value, B1 = rotation amount
; Output: ACC = rotated value
ROTR32:
        ST      TEMP_VAL
        LD      THIRTYTWO
        SUB     B1              ; 32 - n
        ST      TEMP_SHIFT
        LD      TEMP_VAL
        SHR     TEMP_SHIFT      ; x >> (32-n)
        ST      TEMP_PART1
        LD      TEMP_VAL
        SHL     B1              ; x << n
        OR      TEMP_PART1      ; (x >> (32-n)) | (x << n)
        AND     MASK32          ; Keep lower 32 bits
        RETURN

; CH - Choice function: (x AND y) XOR (NOT x AND z)
CH_FUNCTION:
        LD      REG_X
        AND     REG_Y
        ST      TEMP_CH1
        LD      REG_X
        XOR     ALL_ONES        ; NOT x
        AND     REG_Z           ; NOT x AND z
        XOR     TEMP_CH1        ; (x AND y) XOR (NOT x AND z)
        RETURN

; MAJ - Majority function: (x AND y) XOR (x AND z) XOR (y AND z)
MAJ_FUNCTION:
        LD      REG_X
        AND     REG_Y
        ST      TEMP_MAJ1
        LD      REG_X
        AND     REG_Z
        ST      TEMP_MAJ2
        LD      REG_Y
        AND     REG_Z
        XOR     TEMP_MAJ1
        XOR     TEMP_MAJ2
        RETURN

; SIGMA0 - Σ0(x) = ROTR²(x) ⊕ ROTR¹³(x) ⊕ ROTR²²(x)
SIGMA0:
        ST      TEMP_SIG
        LD      TWO
        ST      B1
        LD      TEMP_SIG
        CALL    ROTR32
        ST      TEMP_SIG0
        LD      THIRTEEN
        ST      B1
        LD      TEMP_SIG
        CALL    ROTR32
        XOR     TEMP_SIG0
        ST      TEMP_SIG0
        LD      TWENTYTWO
        ST      B1
        LD      TEMP_SIG
        CALL    ROTR32
        XOR     TEMP_SIG0
        RETURN

; SIGMA1 - Σ1(x) = ROTR⁶(x) ⊕ ROTR¹¹(x) ⊕ ROTR²⁵(x)
SIGMA1:
        ST      TEMP_SIG
        LD      SIX
        ST      B1
        LD      TEMP_SIG
        CALL    ROTR32
        ST      TEMP_SIG1
        LD      ELEVEN
        ST      B1
        LD      TEMP_SIG
        CALL    ROTR32
        XOR     TEMP_SIG1
        ST      TEMP_SIG1
        LD      TWENTYFIVE
        ST      B1
        LD      TEMP_SIG
        CALL    ROTR32
        XOR     TEMP_SIG1
        RETURN

; ============================================================
; I/O FUNCTIONS
; ============================================================

; GET_WORK_FROM_POOL - Get mining work from pool via paper tape
GET_WORK_FROM_POOL:
        ; Request work from pool (punch tape)
        LD      CMD_GET_WORK
        OUT
        
        ; Wait for response (read tape)
        IN
        ST      WORK_STATUS
        RETURN

; SUBMIT_BLOCK - Submit found block to pool
SUBMIT_BLOCK:
        ; Send block data to pool
        LD      CMD_SUBMIT
        OUT
        
        ; Send nonce
        LD      NONCE
        OUT
        
        ; Send hash
        LD      HASH_RESULT
        OUT
        
        ; Wait for acknowledgment
        IN
        RETURN

; PRINT_STRING - Print null-terminated string
; Input: ACC = address of string
PRINT_STRING:
        ST      TEMP_PTR
PRINT_LOOP:
        LD      TEMP_PTR
        CALL    READ_CHAR
        JZ      PRINT_DONE
        OUT
        LD      TEMP_PTR
        ADD     ONE
        ST      TEMP_PTR
        JMP     PRINT_LOOP
PRINT_DONE:
        RETURN

; ============================================================
; DATA SECTION
; ============================================================

        ORG 0x300

; Hash state
H0:             DW 0
H1:             DW 0
H2:             DW 0
H3:             DW 0
H4:             DW 0
H5:             DW 0
H6:             DW 0
H7:             DW 0

; Working variables
WORK_A:         DW 0
WORK_B:         DW 0
WORK_C:         DW 0
WORK_D:         DW 0
WORK_E:         DW 0
WORK_F:         DW 0
WORK_G:         DW 0
WORK_H:         DW 0

; Message schedule
W_TABLE:        DS 64             ; W[0..63]

; Temporary storage
TEMP_VAL:       DW 0
TEMP_SHIFT:     DW 0
TEMP_PART1:     DW 0
TEMP_CH1:       DW 0
TEMP_MAJ1:      DW 0
TEMP_MAJ2:      DW 0
TEMP_SIG:       DW 0
TEMP_SIG0:      DW 0
TEMP_SIG1:      DW 0
TEMP_T1:        DW 0
TEMP_T2:        DW 0
SAVE_ACC:       DW 0

; Mining state
NONCE:          DW 0
HASH_COUNT:     DW 0
BLOCKS_FOUND:   DW 0
WORK_STATUS:    DW 0
HASH_RESULT:    DS 32

; Round counter
ROUND_COUNTER:  DW 0

; Registers for functions
REG_X:          DW 0
REG_Y:          DW 0
REG_Z:          DW 0

; Constants
ZERO:           DW 0
ONE:            DW 1
TWO:            DW 2
SIX:            DW 6
ELEVEN:         DW 11
THIRTEEN:       DW 13
TWENTYTWO:      DW 22
TWENTYFIVE:     DW 25
THIRTYTWO:      DW 32
SIXTYFOUR:      DW 64
MASK32:         DW 0xFFFFFFFF
ALL_ONES:       DW 0xFFFFFFFF

; Command codes
CMD_GET_WORK:   DW 0x01
CMD_SUBMIT:     DW 0x02

; Messages
MSG_INIT:       DW "EDSAC2 MINER", 0
MSG_BLOCK_FOUND: DW "BLOCK FOUND!", 0

; Initial hash values
H_INIT_0:       DW 0x6a09e667
H_INIT_1:       DW 0xbb67ae85
H_INIT_2:       DW 0x3c6ef372
H_INIT_3:       DW 0xa54ff53a
H_INIT_4:       DW 0x510e527f
H_INIT_5:       DW 0x9b05688c
H_INIT_6:       DW 0x1f83d9ab
H_INIT_7:       DW 0x5be0cd19

; Mining configuration
MAX_NONCE_PER_WORK: DW 1000000

; ============================================================
; END OF PROGRAM
; ============================================================

        END START
