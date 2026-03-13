/*
 * RUSTCHAIN 386 MINER - Entropy Collection Header
 */

#ifndef ENTROPY_H
#define ENTROPY_H

#define TIMER_SAMPLES 32
#define HASH_SIZE 32

/* Entropy structure for 386 */
typedef struct {
    /* BIOS info */
    char bios_date[16];
    unsigned char bios_model;
    
    /* CPU info */
    char cpu_vendor[48];
    unsigned long cpu_signature;
    
    /* Memory info */
    unsigned int conv_memory_kb;
    unsigned long ext_memory_kb;
    unsigned long mem_total_kb;
    
    /* Timer entropy */
    unsigned int timer_samples[TIMER_SAMPLES];
    
    /* RTC */
    unsigned char rtc_time[3];
    
    /* Video */
    unsigned char video_mode;
    unsigned char has_vga;
    
    /* 386-specific */
    unsigned long isa_timing_cycles;
    unsigned long mem_timing_cycles;
    unsigned long clock_drift_ppm;
    int has_fpu;
    
    /* Hash */
    unsigned char hash[HASH_SIZE];
} Entropy386;

/* Function prototypes */
void collect_bios_info(Entropy386 *entropy);
void detect_cpu(Entropy386 *entropy);
void collect_memory_info(Entropy386 *entropy);
void collect_timer_entropy(Entropy386 *entropy);
void collect_rtc(Entropy386 *entropy);
void refresh_entropy(Entropy386 *entropy);
void generate_entropy_hash(Entropy386 *entropy);

#endif /* ENTROPY_H */
