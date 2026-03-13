/**
 * @file n64.h
 * @brief N64 Hardware Definitions for FFI
 * 
 * C header file for interfacing with N64 hardware
 * from Rust code via FFI.
 */

#ifndef N64_H
#define N64_H

#include <stdint.h>
#include <stdbool.h>

/* N64 Memory Addresses */
#define N64_RAM_BASE        0x80000000
#define N64_RAM_SIZE        0x400000      /* 4 MB */
#define N64_RDRAM_BASE      0xA0000000
#define N64_RDRAM_SIZE      0x800000      /* 8 MB (aliased) */
#define N64_ROM_BASE        0xB0000000
#define N64_PIF_RAM_BASE    0xA4600000

/* Video Interface (VI) */
#define VI_BASE             0xA4400000
#define VI_CONTROL          (VI_BASE + 0x000)
#define VI_DRAM_ADDR        (VI_BASE + 0x004)
#define VI_H_START          (VI_BASE + 0x00C)
#define VI_V_START          (VI_BASE + 0x010)
#define VI_V_CURRENT        (VI_BASE + 0x044)

/* Display Configuration */
#define VI_NTSC_WIDTH       320
#define VI_NTSC_HEIGHT      240
#define VI_PAL_WIDTH        320
#define VI_PAL_HEIGHT      240

/* Controller Buttons */
#define CONTROLLER_A        0x8000
#define CONTROLLER_B        0x4000
#define CONTROLLER_Z        0x2000
#define CONTROLLER_START    0x1000
#define CONTROLLER_UP       0x0800
#define CONTROLLER_DOWN     0x0400
#define CONTROLLER_LEFT     0x0200
#define CONTROLLER_RIGHT    0x0100

/* COP0 Registers */
#define COP0_INDEX          0
#define COP0_RANDOM         1
#define COP0_ENTRYLO0       2
#define COP0_ENTRYLO1       3
#define COP0_CONTEXT        4
#define COP0_PAGEMASK       5
#define COP0_WIRED          6
#define COP0_BADVADDR       8
#define COP0_COUNT          9
#define COP0_ENTRYHI        10
#define COP0_COMPARE        11
#define COP0_STATUS         12
#define COP0_CAUSE          13
#define COP0_EPC            14
#define COP0_PRID           15
#define COP0_CONFIG         16
#define COP0_CONFIG1        17

/* RCP (Reality Coprocessor) */
#define RCP_BASE            0xA4000000
#define SP_BASE             (RCP + 0x04000000)
#define DPC_BASE            (RCP + 0x04100000)
#define DPS_BASE            (RCP + 0x04200000)
#define MI_BASE             (RCP + 0x04300000)
#define VI_BASE_RCP         (RCP + 0x04400000)
#define AI_BASE             (RCP + 0x04500000)
#define PI_BASE             (RCP + 0x04600000)
#define RI_BASE             (RCP + 0x04700000)
#define SI_BASE             (RCP + 0x04800000)

/* MIPS Instructions */
#define MIPS_NOP            0x00000000
#define MIPS_CACHE          0xBC1A0000

/* Cache Operations */
#define CACHE_INDEX_INVALIDATE_I  0x00
#define CACHE_INDEX_INVALIDATE_D  0x01
#define CACHE_INDEX_STORE_TAG_D   0x05
#define CACHE_HIT_INVALIDATE_I    0x10
#define CACHE_HIT_INVALIDATE_D    0x11
#define CACHE_HIT_WRITEBACK_D     0x15

/* Status Register Bits */
#define SR_IE               0x0001
#define SR_EXL              0x0002
#define SR_ERL              0x0004
#define SR_KSU_USER         0x0018
#define SR_KSU_SUPER        0x0008
#define SR_KSU_KERNEL       0x0000
#define SR_CU0              0x10000
#define SR_CU1              0x20000

/* Cause Register Bits */
#define CAUSE_EXC_CODE      0x0000007C
#define CAUSE_EXC_CODE_SHIFT 2

/* Exception Codes */
#define EXC_CODE_INT        0
#define EXC_CODE_MOD        1
#define EXC_CODE_TLBL       2
#define EXC_CODE_TLBS       3
#define EXC_CODE_ADEL       4
#define EXC_CODE_ADES       5
#define EXC_CODE_IBE        6
#define EXC_CODE_IBD        7
#define EXC_CODE_SYS        8
#define EXC_CODE_BP         9
#define EXC_CODE_RI         10
#define EXC_CODE_CPU        11
#define EXC_CODE_OV         12
#define EXC_CODE_TR         13
#define EXC_CODE_FPE        15

/* FPU Control/Status Register */
#define FPU_CSR_RM          0x00000003
#define FPU_CSR_RM_RN       0x00
#define FPU_CSR_RM_RZ       0x01
#define FPU_CSR_RM_RP       0x02
#define FPU_CSR_RM_RM       0x03
#define FPU_CSR_FLAGS       0x0000007C
#define FPU_CSR_ENABLES     0x00000F80
#define FPU_CSR_CONDITION   0x00800000

/* Data Types */
typedef uint32_t n64_addr_t;
typedef uint32_t n64_color_t;

typedef struct {
    uint8_t r;
    uint8_t g;
    uint8_t b;
    uint8_t a;
} n64_rgba_t;

typedef struct {
    float x;
    float y;
    float z;
} n64_vec3_t;

typedef struct {
    n64_addr_t dram_addr;
    uint32_t width;
    uint32_t height;
    uint32_t format;
} n64_framebuffer_t;

typedef struct {
    uint16_t buttons;
    int8_t stick_x;
    int8_t stick_y;
} n64_controller_state_t;

/* Function Prototypes */

/**
 * Initialize N64 hardware
 */
void n64_init(void);

/**
 * Shutdown N64 hardware
 */
void n64_shutdown(void);

/**
 * Initialize video interface
 * @param width Screen width
 * @param height Screen height
 */
void n64_vi_init(uint32_t width, uint32_t height);

/**
 * Set framebuffer address
 * @param addr Physical address of framebuffer
 */
void n64_vi_set_framebuffer(n64_addr_t addr);

/**
 * Clear framebuffer with color
 * @param fb Framebuffer pointer
 * @param color Clear color (RGBA)
 */
void n64_fb_clear(n64_color_t *fb, n64_color_t color);

/**
 * Initialize controller interface
 */
void n64_controller_init(void);

/**
 * Read controller state
 * @param port Controller port (0-3)
 * @param state Output state structure
 * @return true if successful
 */
bool n64_controller_read(uint8_t port, n64_controller_state_t *state);

/**
 * Get current time in milliseconds
 * @return Time in ms
 */
uint64_t n64_get_time_ms(void);

/**
 * Get CPU cycle count
 * @return Cycle count
 */
uint32_t n64_get_cycle_count(void);

/**
 * Read COP0 register
 * @param reg Register number
 * @return Register value
 */
uint32_t n64_cop0_read(uint8_t reg);

/**
 * Write COP0 register
 * @param reg Register number
 * @param value Value to write
 */
void n64_cop0_write(uint8_t reg, uint32_t value);

/**
 * Invalidate instruction cache
 * @param addr Address to invalidate
 * @param size Size in bytes
 */
void n64_cache_invalidate_i(n64_addr_t addr, uint32_t size);

/**
 * Invalidate data cache
 * @param addr Address to invalidate
 * @param size Size in bytes
 */
void n64_cache_invalidate_d(n64_addr_t addr, uint32_t size);

/**
 * Writeback data cache
 * @param addr Address to writeback
 * @param size Size in bytes
 */
void n64_cache_writeback_d(n64_addr_t addr, uint32_t size);

/**
 * Generate random byte
 * @return Random byte
 */
uint8_t n64_random_byte(void);

/**
 * Print debug message
 * @param msg Message string
 */
void n64_debug_print(const char *msg);

#endif /* N64_H */
