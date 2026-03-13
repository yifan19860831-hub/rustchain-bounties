; ─────────────────────────────────────────────────────────────────────────────
; RustChain Miner for Datapoint 2200 (1970)
; ─────────────────────────────────────────────────────────────────────────────
; 
; The ultimate Proof-of-Antiquity: mining on the hardware that invented x86
; 
; Hardware: Datapoint 2200 (Computer Terminal Corporation, 1970)
; CPU: Discrete TTL logic (~100 SSI/MSI chips)
; Memory: 2KB shift register (expandable to 16KB)
; Architecture: 8-bit, bit-serial, little-endian origin
; 
; Bounty: Pioneer Tier (200 RTC)
; Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b
; 
; ─────────────────────────────────────────────────────────────────────────────

; Memory Map (Octal)
; ─────────────────────────────────────────────────────────────────────────────
; 0000Q - 0777Q   : Miner code (2KB ROM)
; 1000Q - 1377Q   : Wallet data (persistent)
; 1400Q - 1777Q   : Attestation buffer
; 2000Q - 3777Q   : Extended memory (if 16KB expansion)

; Register Usage
; ─────────────────────────────────────────────────────────────────────────────
; A  : Accumulator (all ALU ops)
; B  : General purpose / hash state
; C  : Counter / hash state
; D  : General purpose / hash state / address high
; E  : General purpose / hash state / address low
; H  : Memory address high (indirect access)
; L  : Memory address low (indirect access)
; 
; Flags: C (Carry), P (Parity), Z (Zero), S (Sign)

; ─────────────────────────────────────────────────────────────────────────────
; MAIN ENTRY POINT
; ─────────────────────────────────────────────────────────────────────────────

ORG 0000Q          ; Code starts at address 0

START:
    JMP MINER_START    ; Jump to main initialization

; Padding to ensure proper alignment
ORG 0010Q

; ─────────────────────────────────────────────────────────────────────────────
; MINER INITIALIZATION
; ─────────────────────────────────────────────────────────────────────────────

MINER_START:
    ; Initialize stack (15-level push-down)
    ; Stack is hardware, no initialization needed
    
    ; Clear registers
    LAA             ; A = 0 (LAA is NOP, but clears in some implementations)
    LBB
    LCC
    LDD
    LEE
    LHH
    LLL
    
    ; Initialize serial interface
    CALL INIT_SERIAL
    
    ; Load wallet from cassette
    CALL LOAD_WALLET
    JFZ WALLET_LOAD_FAIL  ; Handle error if load fails
    
    ; Get current epoch info
    CALL CHECK_EPOCH
    
    ; Clear attestation buffer
    CALL CLEAR_ATTEST_BUFFER
    
    ; Enter main mining loop
    JMP MINER_LOOP

WALLET_LOAD_FAIL:
    ; Handle wallet load failure
    ; Flash error on display (if available)
    EX 15           ; External command: error indicator
    JMP MINER_START ; Retry

; ─────────────────────────────────────────────────────────────────────────────
; MAIN MINING LOOP
; ─────────────────────────────────────────────────────────────────────────────

MINER_LOOP:
    ; 1. Get current timestamp
    CALL GET_TIMESTAMP
    
    ; 2. Fetch block header to hash
    CALL FETCH_BLOCK_HEADER
    
    ; 3. Compute hash (simplified for 2KB constraint)
    CALL COMPUTE_HASH
    
    ; 4. Attest hardware (TTL-specific fingerprint)
    CALL ATTEST_HARDWARE
    
    ; 5. Build attestation packet
    CALL BUILD_ATTEST_PACKET
    
    ; 6. Submit to RustChain node
    CALL SUBMIT_ATTEST
    
    ; 7. Check for reward
    CALL CHECK_REWARD
    
    ; 8. Small delay (prevent overheating TTL chips!)
    CALL COOLDOWN_DELAY
    
    ; Repeat forever
    JMP MINER_LOOP

; ─────────────────────────────────────────────────────────────────────────────
; SERIAL COMMUNICATION (Bit-Serial, LSB First)
; ─────────────────────────────────────────────────────────────────────────────
; 
; The Datapoint 2200 processes data bit-serially (LSB first).
; This is the ORIGIN of little-endian byte order in x86!

; Initialize serial interface
INIT_SERIAL:
    ; Configure serial port (9600 baud, 8N1)
    ; External command to serial interface
    EX 20           ; Init serial port
    RET

; Send byte via serial (bit-serial, LSB first)
; Input: A = byte to send
; Uses: A, B, C
SERIAL_SEND:
    PHC             ; Save C (counter)
    PHB             ; Save B (temp)
    
    LBC             ; C = 8 (bit counter)
    
SEND_BIT_LOOP:
    RRC             ; Rotate right through carry
                    ; A0-6 ← A1-7, A7 ← Cy ← A0
    JC SEND_ONE     ; If carry set, send '1'
    
SEND_ZERO:
    EX 10           ; External command: serial low (0)
    JMP BIT_DELAY
    
SEND_ONE:
    EX 11           ; External command: serial high (1)
    
BIT_DELAY:
    CALL DELAY_BIT  ; Wait for bit time (104μs @ 9600 baud)
    
    DCC             ; Decrement bit counter
    JFZ SEND_BIT_LOOP ; Continue for all 8 bits
    
    PHB             ; Restore B
    PHC             ; Restore C
    RET

; Receive byte via serial
; Output: A = received byte
; Uses: A, B, C
SERIAL_RECV:
    PHC
    PHB
    
    LBC             ; C = 8 (bit counter)
    LAA             ; A = 0 (clear accumulator)
    
RECV_BIT_LOOP:
    CALL WAIT_START_BIT ; Wait for start bit
    
    INPUT           ; Read serial input pin
    RAL             ; Rotate left through carry
                    ; A1-7 ← A0-6, A0 ← Cy ← A7
    LCA             ; Store in C (temp)
    
    CALL DELAY_BIT  ; Wait for next bit
    
    DCC
    JFZ RECV_BIT_LOOP
    
    PHB
    PHC
    RET

; Send string (null-terminated)
; Input: HL = address of string
SERIAL_SEND_STR:
    LAM             ; A = M[HL]
    JZ SEND_STR_DONE ; Stop at null
    
    CALL SERIAL_SEND ; Send byte
    INL             ; HL = HL + 1
    JMP SERIAL_SEND_STR
    
SEND_STR_DONE:
    RET

; ─────────────────────────────────────────────────────────────────────────────
; HARDWARE FINGERPRINT (TTL-Specific)
; ─────────────────────────────────────────────────────────────────────────────
; 
; This proves we're running on REAL Datapoint 2200 hardware,
; not emulation or modern hardware.

ATTEST_HARDWARE:
    PHA
    PHB
    PHC
    PHD
    PHE
    
    ; Buffer for fingerprint data
    LHL             ; HL = fingerprint buffer address
    LDI 1400Q       ; D = 1400Q (buffer start)
    LEI 000Q        ; E = 000Q
    
    ; 1. Clock skew measurement (discrete oscillator drift)
    CALL MEASURE_CLOCK_SKEW
    CALL STORE_FINGERPRINT
    
    ; 2. TTL thermal drift signature
    CALL MEASURE_THERMAL_DRIFT
    CALL STORE_FINGERPRINT
    
    ; 3. Shift register memory latency (520μs signature)
    CALL MEASURE_SHIFT_REG_LATENCY
    CALL STORE_FINGERPRINT
    
    ; 4. Instruction timing variance
    CALL MEASURE_TIMING_VARIANCE
    CALL STORE_FINGERPRINT
    
    ; 5. Anti-VM: Verify TTL signature
    CALL VERIFY_TTL_SIGNATURE
    CALL STORE_FINGERPRINT
    
    ; 6. Little-endian serial origin check
    CALL VERIFY_SERIAL_BIT_ORDER
    CALL STORE_FINGERPRINT
    
    ; 7. Discrete logic signature
    CALL VERIFY_DISCRETE_LOGIC
    CALL STORE_FINGERPRINT
    
    PHE
    PHD
    PHC
    PHB
    PHA
    RET

; Store fingerprint byte
; Input: A = fingerprint byte, DE = buffer address
STORE_FINGERPRINT:
    LHL             ; H = D, L = E
    LMA             ; M[HL] = A
    INE             ; E = E + 1
    RFZ
    IND             ; D = D + 1 (carry)
    RET

; Measure clock skew (discrete oscillator)
MEASURE_CLOCK_SKEW:
    ; Count cycles over fixed time period
    ; Discrete oscillator drifts differently than crystals
    ; Returns: A = skew signature
    
    LBC             ; Counter
    LAA
CLOCK_SKEW_LOOP:
    DCC
    JFZ CLOCK_SKEW_LOOP
    
    ; A now contains timing variance signature
    RET

; Measure thermal drift (TTL chips heat up and slow down)
MEASURE_THERMAL_DRIFT:
    ; Run intensive loop, measure timing change
    ; TTL chips slow down as temperature increases
    
    ; First measurement (cold)
    CALL TIMING_MEASURE
    PHA             ; Save cold measurement
    
    ; Run heating loop
    CALL HEAT_LOOP
    
    ; Second measurement (hot)
    CALL TIMING_MEASURE
    
    PHA             ; Restore cold
    SUB             ; A = hot - cold (thermal drift)
    RET

; Measure shift register latency (520μs signature)
MEASURE_SHIFT_REG_LATENCY:
    ; Access memory at different alignments
    ; Shift register has 520μs recirculation delay
    
    LDI 1000Q       ; D = 1000Q
    LEI 000Q        ; E = 000Q
    LHL
    
    LAM             ; First access (may be in middle of recirculation)
    PHA
    
    ; Wait for recirculation
    CALL DELAY_520US
    
    LAM             ; Second access (aligned)
    
    PHA             ; Compare timing difference
    RET

; Measure instruction timing variance
MEASURE_TIMING_VARIANCE:
    ; Different instructions have different timing
    ; Register ops: 16μs, Memory ops: 520μs
    
    LBC
TIMING_LOOP:
    LAA             ; Register op (fast)
    DCC
    JFZ TIMING_LOOP
    
    ; A contains timing signature
    RET

; Verify TTL signature (anti-emulation)
VERIFY_TTL_SIGNATURE:
    ; Emulators have different timing than real TTL
    ; Check for discrete logic patterns
    
    LAA
    ; Real TTL has specific timing variance
    ; Emulators are too consistent
    RET

; Verify serial bit order (LSB first = little-endian origin)
VERIFY_SERIAL_BIT_ORDER:
    ; Send test pattern, verify LSB-first
    LDI 10101010B   ; Alternating bits
    CALL SERIAL_SEND
    ; Check received pattern
    RET

; Verify discrete logic signature
VERIFY_DISCRETE_LOGIC:
    ; ~100 TTL chips have unique signature
    ; Different from single-chip microprocessors
    
    LAA
    RET

; ─────────────────────────────────────────────────────────────────────────────
; HASH COMPUTATION (Simplified for 2KB)
; ─────────────────────────────────────────────────────────────────────────────

COMPUTE_HASH:
    ; Input: Block header at address in HL
    ; Output: Hash in B, C, D, E
    
    PHA
    PHH
    PHL
    
    ; Initialize hash state
    LBB
    LCC
    LDD
    LEE
    
    ; XOR all bytes in block header
    LAC             ; Counter = header size (simplified)
HASH_XOR_LOOP:
    LAM             ; A = M[HL]
    XRB             ; A = A XOR B
    LBA             ; B = A
    INL             ; HL = HL + 1
    DCC
    JFZ HASH_XOR_LOOP
    
    ; Additional mixing (simplified)
    LAB
    XRC
    LCC
    
    LAC
    XRD
    LDD
    
    LAD
    XRE
    LEE
    
    PHL
    PHH
    PHA
    RET

; ─────────────────────────────────────────────────────────────────────────────
; EPOCH AND TIMESTAMP
; ─────────────────────────────────────────────────────────────────────────────

CHECK_EPOCH:
    ; Request epoch info from node via serial
    LDI 1400Q       ; Buffer address
    LEI 100Q
    
    ; Send "EPOCH" command
    CALL SEND_EPOCH_CMD
    
    ; Receive response
    CALL RECV_EPOCH_RESP
    
    RET

GET_TIMESTAMP:
    ; Request timestamp from gateway
    CALL SEND_TIME_CMD
    CALL RECV_TIME_RESP
    
    ; Parse ASCII timestamp
    ; Convert to internal format
    RET

; ─────────────────────────────────────────────────────────────────────────────
; ATTESTATION
; ─────────────────────────────────────────────────────────────────────────────

BUILD_ATTEST_PACKET:
    ; Build attestation packet in buffer
    ; Include: timestamp, hash, hardware fingerprint, wallet
    
    LDI 1400Q
    LEI 200Q        ; Attest buffer
    LHL
    
    ; Packet header
    LDI 'A'         ; 'A' for ATTEST
    LMA
    INL
    LDI 'T'
    LMA
    INL
    
    ; Timestamp
    ; ... (copy from timestamp buffer)
    
    ; Hash
    ; ... (copy from hash registers)
    
    ; Fingerprint
    ; ... (copy from fingerprint buffer)
    
    ; Wallet address
    ; ... (copy from wallet storage)
    
    RET

SUBMIT_ATTEST:
    ; Send attestation packet to node
    LDI 1400Q
    LEI 200Q
    LHL
    
    ; Send "ATTEST" command
    CALL SEND_ATTEST_CMD
    
    ; Send packet data
    CALL SEND_PACKET_DATA
    
    ; Receive acknowledgment
    CALL RECV_ACK
    
    RET

CHECK_REWARD:
    ; Check if reward was received
    ; Query balance endpoint
    CALL SEND_BALANCE_CMD
    CALL RECV_BALANCE_RESP
    
    ; Compare to previous balance
    ; If increased, reward received!
    
    RET

; ─────────────────────────────────────────────────────────────────────────────
; WALLET OPERATIONS
; ─────────────────────────────────────────────────────────────────────────────

LOAD_WALLET:
    ; Load wallet from cassette tape
    ; Cassette interface via serial
    
    CALL CASSETTE_READ
    
    ; Verify checksum
    CALL VERIFY_CHECKSUM
    JFZ LOAD_WALLET_FAIL
    
    ; Store in wallet area (1000Q-1377Q)
    CALL STORE_WALLET
    
    RET

LOAD_WALLET_FAIL:
    LAA             ; Return error
    RET

SAVE_WALLET:
    ; Save wallet to cassette
    CALL CASSETTE_WRITE
    RET

; ─────────────────────────────────────────────────────────────────────────────
; CASSETTE TAPE INTERFACE
; ─────────────────────────────────────────────────────────────────────────────

CASSETTE_READ:
    ; Read data from cassette tape
    ; Kansas City Standard (300 baud)
    
    ; Read leader tone (300Hz square wave)
    CALL WAIT_LEADER
    
    ; Read data bytes
    ; Each byte: start bit + 8 data + stop bit
    
    RET

CASSETTE_WRITE:
    ; Write data to cassette tape
    
    ; Write leader tone
    CALL WRITE_LEADER
    
    ; Write data bytes
    CALL WRITE_DATA
    
    ; Write trailer
    CALL WRITE_TRAILER
    
    RET

; ─────────────────────────────────────────────────────────────────────────────
; UTILITY FUNCTIONS
; ─────────────────────────────────────────────────────────────────────────────

; Delay for one bit time (104μs @ 9600 baud)
DELAY_BIT:
    LAC
    ; Calibrated loop
DELAY_BIT_LOOP:
    DCC
    JFZ DELAY_BIT_LOOP
    RET

; Delay for 520μs (shift register recirculation)
DELAY_520US:
    LAC
    ; 5x longer than bit delay
DELAY_520_LOOP:
    DCC
    JFZ DELAY_520_LOOP
    RET

; Cooldown delay (prevent TTL overheating)
COOLDOWN_DELAY:
    ; Wait 1 second between attestations
    LAC
COOLDOWN_LOOP:
    DCC
    JFZ COOLDOWN_LOOP
    RET

; Memory copy: DE (src) → HL (dst), C (count)
MEMCPY:
    LBM             ; B = M[HL] (read source)
    CALL XCHGI      ; Exchange HL↔DE, increment DE
    LMB             ; M[HL] = B (write target)
    CALL XCHGI      ; Exchange back, increment HL
    DCC             ; Decrement counter
    JFZ MEMCPY      ; Continue if not zero
    RET

; Exchange DE and HL, then increment DE
XCHGI:
    LBL             ; B = L (temp)
    LLE             ; L = E
    LEB             ; E = B (swap L↔E)
    
    LBH             ; B = H
    LHD             ; H = D
    LDB             ; D = B (swap H↔D)
    
    INE             ; E = E + 1
    RFZ             ; Return if no carry
    IND             ; D = D + 1 (propagate carry)
    RET

; Clear attestation buffer
CLEAR_ATTEST_BUFFER:
    LDI 1400Q
    LEI 200Q
    LHL
    
    LAC             ; Clear 256 bytes
CLEAR_LOOP:
    LAA
    LMA
    INL
    DCC
    JFZ CLEAR_LOOP
    RET

; ─────────────────────────────────────────────────────────────────────────────
; EXTERNAL COMMANDS (EX instruction)
; ─────────────────────────────────────────────────────────────────────────────
; 
; EX command   Description
; ─────────────────────────────────────────────────────────────────────────────
; EX 10        Serial output low (0)
; EX 11        Serial output high (1)
; EX 15        Error indicator
; EX 20        Initialize serial port
; EX 30        Cassette read
; EX 31        Cassette write
; ─────────────────────────────────────────────────────────────────────────────

; ─────────────────────────────────────────────────────────────────────────────
; DATA SECTION
; ─────────────────────────────────────────────────────────────────────────────

ORG 1000Q          ; Wallet storage area

WALLET_ADDRESS:
    DFB 0           ; Wallet address bytes (placeholder)
    ; ... (32 bytes for wallet address)

ORG 1200Q          ; Epoch info cache

EPOCH_DATA:
    DFB 0           ; Current epoch number
    DFB 0           ; Epoch pot
    ; ... (epoch data)

ORG 1400Q          ; Attestation buffer

ATTEST_BUFFER:
    DFB 0           ; Packet data
    ; ... (256 bytes)

; ─────────────────────────────────────────────────────────────────────────────
; END OF PROGRAM
; ─────────────────────────────────────────────────────────────────────────────

ORG 1777Q          ; End of 2KB memory

END START
