/**
 * Hardware Fingerprint Implementation
 */

#include "fingerprint.h"
#include <string.h>
#include <c64.h>

// CIA #1 registers
#define CIA1_TALO   (*(volatile unsigned char*)0xDC04)
#define CIA1_TAHI   (*(volatile unsigned char*)0xDC05)

// VIC-II registers
#define VIC_RASTER  (*(volatile unsigned char*)0xD012)

// SID registers
#define SID_POTX    (*(volatile unsigned char*)0xD419)
#define SID_POTY    (*(volatile unsigned char*)0xD41A)

// Memory configuration register
#define MEM_CONFIG  (*(volatile unsigned char*)0xDD00)

/**
 * Measure CIA timer jitter
 * Real hardware has crystal variance; emulators often have perfect timing
 */
static uint32_t fingerprint_cia_timer(void) {
    unsigned char lo, hi, lo2, hi2;
    
    // Disable interrupts for precise timing
    asm("sei");
    
    lo = CIA1_TALO;
    hi = CIA1_TAHI;
    
    // Small delay (~100 cycles)
    for (volatile int i = 0; i < 100; i++) {
        asm("nop");
    }
    
    lo2 = CIA1_TALO;
    hi2 = CIA1_TAHI;
    
    asm("cli");
    
    // Calculate timer delta
    uint16_t delta1 = (hi << 8) | lo;
    uint16_t delta2 = (hi2 << 8) | lo2;
    
    return (uint32_t)(delta2 - delta1);
}

/**
 * Measure VIC-II raster timing jitter
 */
static uint32_t fingerprint_vic_raster(void) {
    unsigned char raster1, raster2, raster3;
    
    // Wait for specific raster line
    while (VIC_RASTER != 100);
    raster1 = VIC_RASTER;
    
    // Small delay
    for (volatile int i = 0; i < 50; i++) {
        asm("nop");
    }
    
    raster2 = VIC_RASTER;
    raster3 = VIC_RASTER;
    
    // Combine raster values
    return ((uint32_t)raster1 << 16) | ((uint32_t)raster2 << 8) | raster3;
}

/**
 * Read SID chip behavior
 * Some registers return different values on real hardware vs emulators
 */
static uint32_t fingerprint_sid(void) {
    unsigned char potx = SID_POTX;
    unsigned char poty = SID_POTY;
    
    return ((uint32_t)potx << 8) | poty;
}

/**
 * Calculate Kernal ROM checksum
 */
static uint16_t fingerprint_rom_checksum(void) {
    uint16_t sum = 0;
    unsigned char old_config;
    
    // Save current memory configuration
    old_config = MEM_CONFIG;
    
    // Enable ROMs (bits 0-1 = 11)
    MEM_CONFIG = old_config | 0x03;
    
    // Calculate checksum of Kernal ROM (0xE000-0xFFFF)
    for (unsigned int addr = 0xE000; addr <= 0xFFFF; addr++) {
        sum += *(volatile unsigned char*)addr;
    }
    
    // Restore previous configuration
    MEM_CONFIG = old_config;
    
    return sum;
}

/**
 * Build complete hardware fingerprint
 */
void build_fingerprint(C64Fingerprint* fp) {
    memset(fp, 0, sizeof(C64Fingerprint));
    
    // Set static fields
    strcpy(fp->device_arch, "c64_6510");
    strcpy(fp->device_family, "commodore_64");
    fp->cpu_speed = 1023000;  // 1.023 MHz (NTSC)
    fp->total_ram_kb = 64;
    
    // Collect hardware-specific fingerprints
    fp->cia_timer_fp = fingerprint_cia_timer();
    fp->vic_raster_fp = fingerprint_vic_raster();
    fp->sid_fp = fingerprint_sid();
    fp->rom_checksum = fingerprint_rom_checksum();
}

/**
 * Detect if running in an emulator
 * Returns 1 if emulator detected, 0 if real hardware
 */
int detect_emulator(void) {
    uint32_t cia_fp = fingerprint_cia_timer();
    uint32_t vic_fp = fingerprint_vic_raster();
    
    // Emulators often have:
    // - Perfect CIA timing (no jitter)
    // - Fixed raster values
    // - Zero or fixed SID register values
    
    if (cia_fp == 0 || cia_fp > 1000) {
        // CIA timer should have small, consistent delta on real hardware
        return 1;
    }
    
    if (vic_fp == 0) {
        // VIC raster should never be all zeros
        return 1;
    }
    
    // Additional checks could be added:
    // - SID register behavior
    // - DRAM refresh timing
    // - Color burst phase detection
    
    return 0;  // Likely real hardware
}
