/**
 * Hardware Fingerprinting
 * 
 * Collects unique hardware identifiers from:
 * - CIA timer jitter
 * - VIC-II raster timing
 * - SID chip behavior
 * - Kernal ROM checksum
 */

#ifndef FINGERPRINT_H
#define FINGERPRINT_H

#include <stdint.h>

typedef struct {
    char device_arch[16];     // "c64_6510"
    char device_family[16];   // "commodore_64"
    uint32_t cpu_speed;       // 1023000 (1.023 MHz)
    uint16_t total_ram_kb;    // 64
    uint32_t cia_timer_fp;    // CIA timer fingerprint
    uint32_t vic_raster_fp;   // VIC-II raster fingerprint
    uint32_t sid_fp;          // SID chip fingerprint
    uint16_t rom_checksum;    // Kernal ROM checksum
} C64Fingerprint;

// Build complete fingerprint
void build_fingerprint(C64Fingerprint* fp);

// Detect if running in emulator
int detect_emulator(void);

#endif
