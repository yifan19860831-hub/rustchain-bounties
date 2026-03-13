/*
 * RUSTCHAIN 386 MINER - Fingerprint Header
 */

#ifndef FINGERPRINT_H
#define FINGERPRINT_H

#include "entropy.h"

/* Fingerprint structure for 386 */
typedef struct {
    char arch[16];           /* "i386" */
    char family[16];         /* "x86_32" */
    char cpu_vendor[48];     /* CPU vendor string */
    char model[48];          /* "Intel 386" */
    unsigned long cpu_signature;
    char bios_date[16];
    int has_fpu;             /* 0 = no FPU (authentic 386) */
    unsigned long isa_timing_cycles;
    unsigned long mem_timing_cycles;
    unsigned long clock_drift_ppm;
} Fingerprint386;

/* Function prototypes */
void generate_fingerprint(Fingerprint386 *fp, const Entropy386 *entropy);
int validate_fingerprint(const Fingerprint386 *fp);
void print_fingerprint(const Fingerprint386 *fp);

#endif /* FINGERPRINT_H */
