; ============================================================================
; Atari 2600 Memory-Mapped I/O Constants
; ============================================================================
; For use with RustChain Miner project
; ============================================================================

; TIA - Television Interface Adaptor
VSYNC       = $00       ; Vertical sync set/clear
VBLANK      = $01       ; Vertical blank set/clear
WSYNC       = $02       ; Wait for horizontal blank
RSYNC       = $03       ; Reset horizontal sync counter
NUSIZ0      = $04       ; Number-size player-missile 0
NUSIZ1      = $05       ; Number-size player-missile 1
COLUP0      = $06       ; Color-luminance player 0
COLUP1      = $07       ; Color-luminance player 1
COLUPF      = $08       ; Color-luminance playfield
COLUBK      = $09       ; Color-luminance background
CTRLPF      = $0A       ; Control playfield ball collision
REFP0       = $0B       ; Reflect player 0
REFP1       = $0C       ; Reflect player 1
PF0         = $0D       ; Playfield register byte 0
PF1         = $0E       ; Playfield register byte 1
PF2         = $0F       ; Playfield register byte 2
RESP0       = $10       ; Reset player 0
RESP1       = $11       ; Reset player 1
RESM0       = $12       ; Reset missile 0
RESM1       = $13       ; Reset missile 1
HMOVE       = $14       ; Apply horizontal motion
HMCLR       = $15       ; Clear horizontal move registers
CXCLR       = $16       ; Clear collision latches

; TIA Write (Read addresses are +$10)
VSYNC_W     = $00
VBLANK_W    = $01
WSYNC_W     = $02

; RAM - 128 bytes at $80-$FF
RAM_START   = $80
RAM_END     = $FF
RAM_SIZE    = 128

; PIA - Peripheral Interface Adapter
SWCHA       = $0280     ; Port A input (joysticks)
SWACNT      = $0281     ; Port A data direction
SWCHB       = $0282     ; Port B input (console switches)
SWBCNT      = $0283     ; Port B data direction
INTIM       = $0284     ; Timer output (read)
TIM1T       = $0294     ; Timer set 1 clock interval
TIM8T       = $0295     ; Timer set 8 clock intervals
TIM64T      = $0296     ; Timer set 64 clock intervals
T1024T      = $0297     ; Timer set 1024 clock intervals

; ROM - Cartridge space
ROM_START   = $F000
ROM_END     = $FFFF
ROM_SIZE    = 4096      ; 4 KB

; ============================================================================
; Mining-Specific Memory Layout (within 128 byte RAM)
; ============================================================================

; $00-$01: Nonce counter (16-bit)
MINER_NONCE_LOW   = $00
MINER_NONCE_HIGH  = $01

; $02-$05: Hash result buffer (32-bit simplified)
MINER_HASH_0      = $02
MINER_HASH_1      = $03
MINER_HASH_2      = $04
MINER_HASH_3      = $05

; $06: Difficulty threshold
MINER_DIFFICULTY  = $06

; $07: Status flag
MINER_STATUS      = $07
STATUS_MINING     = $00
STATUS_FOUND      = $01

; $08-$0F: Display buffer
MINER_DISPLAY     = $08

; $10-$1F: Kernel stack
MINER_STACK       = $10

; $20-$7F: General workspace (96 bytes)
MINER_WORKSPACE   = $20

; ============================================================================
; Color Constants (NTSC)
; ============================================================================

COLOR_BLACK       = $00
COLOR_WHITE       = $0E
COLOR_RED         = $24
COLOR_GREEN       = $44
COLOR_BLUE        = $84
COLOR_YELLOW      = $0A
COLOR_CYAN        = $A4
COLOR_MAGENTA     = $64
COLOR_ORANGE      = $16
COLOR_BROWN       = $38

; ============================================================================
; Timing Constants (NTSC)
; ============================================================================

SCANLINES_VISIBLE  = 192
SCANLINES_VBLANK   = 30
SCANLINES_OVERSCAN = 30
SCANLINES_TOTAL    = 262

FRAME_RATE         = 60       ; 60 Hz NTSC
CYCLES_PER_FRAME   = 14318    ; ~14k CPU cycles per frame
CYCLES_PER_SCANLINE = 76      ; 76 CPU cycles per scanline

; ============================================================================
