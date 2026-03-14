; ============================================================================
; RustChain Miner for ColecoVision - Memory Definitions
; ============================================================================

; ============================================================================
; COLECOVISION MEMORY MAP
; ============================================================================

; System ROM (BIOS)
ROM_START       EQU $0000
ROM_END         EQU $0FFF

; Cartridge ROM (Our Code)
CARTRIDGE_START EQU $1000
CARTRIDGE_END   EQU $1FFF

; System RAM (Our Workspace - Only 1 KB!)
RAM_START       EQU $2000
RAM_END         EQU $23FF

; Video RAM (TMS9918)
VRAM_START      EQU $2400
VRAM_END        EQU $3FFF

; ============================================================================
; RAM ALLOCATION (1024 bytes total)
; ============================================================================

; Stack (256 bytes)
STACK_START     EQU $2000
STACK_END       EQU $20FF

; Mining State (256 bytes)
MINER_STATE     EQU $2100
NONCE_COUNTER   EQU $2100     ; 4 bytes
CURRENT_HASH    EQU $2104     ; 4 bytes
BEST_HASH       EQU $2108     ; 4 bytes
HASH_COUNT      EQU $210C     ; 1 byte
HASH_RATE       EQU $210D     ; 1 byte

; Hash Working Buffer (128 bytes)
HASH_BUFFER     EQU $2200     ; 64 bytes
HASH_STATE      EQU $2240     ; 8 bytes
HASH_CONSTANTS  EQU $2248     ; 8 bytes

; Display Buffer (64 bytes)
DISPLAY_BUFFER  EQU $2280
NONCE_DISPLAY   EQU $2280     ; 9 bytes
RATE_DISPLAY    EQU $2289     ; 4 bytes
STATUS_DISPLAY  EQU $228D     ; 16 bytes

; Temporary / Free Space (64 bytes)
TEMP_SPACE      EQU $22C0

; Block Header Template
BLOCK_HEADER    EQU $22D0     ; 64 bytes

; Difficulty Target
DIFFICULTY      EQU $2310     ; 4 bytes

; ============================================================================
; TMS9918 VDP REGISTERS
; ============================================================================

VDP_DATA        EQU $98       ; VDP Data Port
VDP_CONTROL     EQU $99       ; VDP Control Port

; VDP Register Numbers
VDP_REG_0       EQU $80       ; Mode Register 0
VDP_REG_1       EQU $81       ; Mode Register 1
VDP_REG_2       EQU $82       ; Name Table Base
VDP_REG_3       EQU $83       ; Color Table Base
VDP_REG_4       EQU $84       ; Pattern Table Base
VDP_REG_5       EQU $85       ; Sprite Attribute Table
VDP_REG_6       EQU $86       ; Sprite Pattern Table
VDP_REG_7       EQU $87       ; Text Color / Border

; ============================================================================
; INPUT/OUTPUT PORTS
; ============================================================================

INPUT_PORT_1    EQU $DC       ; Controller 1
INPUT_PORT_2    EQU $DD       ; Controller 2

; ============================================================================
; INTERRUPT VECTORS
; ============================================================================

NMI_VECTOR      EQU $0066     ; Non-Maskable Interrupt
RESET_VECTOR    EQU $1000     ; Our Reset Handler

; ============================================================================
; CONSTANTS
; ============================================================================

; Screen Dimensions (TMS9918 Graphics II)
SCREEN_WIDTH    EQU 32        ; Characters
SCREEN_HEIGHT   EQU 24        ; Characters
SCREEN_SIZE     EQU 768       ; Name table bytes

; Colors
COLOR_BLACK     EQU $00
COLOR_GREEN     EQU $02
COLOR_YELLOW    EQU $06
COLOR_WHITE     EQU $0F

; Mining Constants
NONCE_MAX       EQU $FFFFFFFF ; 32-bit nonce range
HASH_SIZE       EQU 32        ; Full SHA-256 output (we use 4)
BLOCK_SIZE      EQU 64        ; SHA-256 block size

; ============================================================================
; MACROS
; ============================================================================

; Wait for VDP to be ready
MACRO WAIT_VDP
    IN A, (VDP_CONTROL)
    AND $80
    JR Z, $-4
ENDM

; Write to VDP Register
MACRO VDP_WRITE_REG reg, value
    LD A, value
    OUT (VDP_DATA), A
    LD A, reg
    OUT (VDP_CONTROL), A
ENDM

; Set VDP Address for Write
MACRO VDP_SET_ADDR addr
    LD A, addr & $FF
    OUT (VDP_DATA), A
    LD A, (addr >> 8) | $40
    OUT (VDP_CONTROL), A
ENDM

; ============================================================================
; END OF HEADER
; ============================================================================
