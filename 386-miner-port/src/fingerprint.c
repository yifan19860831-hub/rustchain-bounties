/*
 * RUSTCHAIN 386 MINER - Fingerprint Generation
 * 
 * Generates 386-specific hardware fingerprint for attestation
 */

#include <stdio.h>
#include <string.h>

#include "fingerprint.h"

/* Generate fingerprint from entropy */
void generate_fingerprint(Fingerprint386 *fp, const Entropy386 *entropy) {
    /* Architecture identification */
    strcpy(fp->arch, "i386");
    strcpy(fp->family, "x86_32");
    strcpy(fp->model, "Intel 386");
    
    /* CPU info */
    strncpy(fp->cpu_vendor, entropy->cpu_vendor, sizeof(fp->cpu_vendor) - 1);
    fp->cpu_vendor[sizeof(fp->cpu_vendor) - 1] = '\0';
    fp->cpu_signature = entropy->cpu_signature;
    
    /* BIOS info */
    strncpy(fp->bios_date, entropy->bios_date, sizeof(fp->bios_date) - 1);
    fp->bios_date[sizeof(fp->bios_date) - 1] = '\0';
    
    /* 386-specific fingerprints */
    fp->has_fpu = entropy->has_fpu;
    fp->isa_timing_cycles = entropy->isa_timing_cycles;
    fp->mem_timing_cycles = entropy->mem_timing_cycles;
    fp->clock_drift_ppm = entropy->clock_drift_ppm;
    
    /* If entropy doesn't have these measurements yet, use defaults */
    if (fp->isa_timing_cycles == 0) {
        fp->isa_timing_cycles = measure_isa_timing();
    }
    if (fp->mem_timing_cycles == 0) {
        fp->mem_timing_cycles = measure_memory_timing();
    }
    if (fp->clock_drift_ppm == 0) {
        fp->clock_drift_ppm = measure_clock_drift();
    }
    if (fp->has_fpu == 0 && entropy->has_fpu == 0) {
        fp->has_fpu = detect_fpu_presence();
    }
}

/* Validate fingerprint (check for authenticity) */
int validate_fingerprint(const Fingerprint386 *fp) {
    /* Check architecture */
    if (strcmp(fp->arch, "i386") != 0) {
        return 0;
    }
    
    /* Check for no FPU (authentic 386 characteristic) */
    if (fp->has_fpu != 0) {
        /* Has FPU - might be 386 with 387, or emulator */
        /* Still valid, but less authentic */
    }
    
    /* Check ISA timing (should be slow for real ISA bus) */
    if (fp->isa_timing_cycles < 100) {
        /* Too fast - might be emulated */
        return 0;
    }
    
    /* Check clock drift (386 crystals drift significantly) */
    if (fp->clock_drift_ppm < 1000 || fp->clock_drift_ppm > 100000) {
        /* Unusual drift - might be emulated */
        return 0;
    }
    
    return 1;  /* Fingerprint appears authentic */
}

/* Print fingerprint for debugging */
void print_fingerprint(const Fingerprint386 *fp) {
    printf("\n--- 386 FINGERPRINT ---\n");
    printf("Architecture:    %s\n", fp->arch);
    printf("Family:          %s\n", fp->family);
    printf("Model:           %s\n", fp->model);
    printf("CPU Vendor:      %s\n", fp->cpu_vendor);
    printf("CPU Signature:   0x%08lX\n", fp->cpu_signature);
    printf("BIOS Date:       %s\n", fp->bios_date);
    printf("Has FPU:         %s\n", fp->has_fpu ? "Yes" : "No (authentic!)");
    printf("ISA Timing:      %lu cycles\n", fp->isa_timing_cycles);
    printf("Memory Timing:   %lu cycles/byte\n", fp->mem_timing_cycles);
    printf("Clock Drift:     %lu ppm\n", fp->clock_drift_ppm);
    printf("-----------------------\n\n");
}
