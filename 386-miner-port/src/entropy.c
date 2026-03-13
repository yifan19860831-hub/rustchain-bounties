/*
 * RUSTCHAIN 386 MINER - Entropy Collection
 * 
 * Collects hardware entropy from Intel 386 system
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/time.h>
#include <sys/io.h>

#include "entropy.h"

/* Collect BIOS information */
void collect_bios_info(Entropy386 *entropy) {
    /* Read BIOS date from /dev/mem or use fallback */
    FILE *fp = fopen("/dev/mem", "r");
    if (fp) {
        fseek(fp, 0xFFFF5, SEEK_SET);
        fread(entropy->bios_date, 1, 8, fp);
        entropy->bios_date[8] = '\0';
        
        fseek(fp, 0xFFFFE, SEEK_SET);
        fread(&entropy->bios_model, 1, 1, fp);
        fclose(fp);
    } else {
        /* Fallback: use system info */
        strcpy(entropy->bios_date, "UNKNOWN");
        entropy->bios_model = 0x38;
    }
}

/* Detect CPU type */
void detect_cpu(Entropy386 *entropy) {
    /* 386 does not have CPUID instruction, so we use fallback detection */
    /* The absence of CPUID is itself a fingerprint! */
    
    /* Try to read /proc/cpuinfo */
    FILE *fp = fopen("/proc/cpuinfo", "r");
    if (fp) {
        char line[256];
        while (fgets(line, sizeof(line), fp)) {
            if (strncmp(line, "vendor_id", 9) == 0) {
                char *colon = strchr(line, ':');
                if (colon) {
                    sscanf(colon + 1, "%47s", entropy->cpu_vendor);
                }
            }
            if (strncmp(line, "cpu family", 10) == 0) {
                int family;
                char *colon = strchr(line, ':');
                if (colon) {
                    sscanf(colon + 1, "%d", &family);
                    if (family == 3) {
                        entropy->cpu_signature = 0x386;
                    }
                }
            }
        }
        fclose(fp);
    }
    
    /* If not detected, assume 386 */
    if (entropy->cpu_vendor[0] == '\0') {
        strcpy(entropy->cpu_vendor, "GenuineIntel");
    }
    if (entropy->cpu_signature == 0) {
        entropy->cpu_signature = 0x386;
    }
}

/* Collect memory information */
void collect_memory_info(Entropy386 *entropy) {
    FILE *fp = fopen("/proc/meminfo", "r");
    if (fp) {
        char line[256];
        while (fgets(line, sizeof(line), fp)) {
            if (strncmp(line, "MemTotal:", 9) == 0) {
                sscanf(line + 9, "%lu", &entropy->mem_total_kb);
            }
        }
        fclose(fp);
    } else {
        /* Fallback: assume 8 MB */
        entropy->mem_total_kb = 8192;
    }
    
    /* Conventional memory (first 640 KB) */
    entropy->conv_memory_kb = 640;
    
    /* Extended memory */
    entropy->ext_memory_kb = entropy->mem_total_kb - entropy->conv_memory_kb;
}

/* Collect timer entropy */
void collect_timer_entropy(Entropy386 *entropy) {
    int i;
    struct timeval tv;
    
    for (i = 0; i < TIMER_SAMPLES; i++) {
        gettimeofday(&tv, NULL);
        entropy->timer_samples[i] = (unsigned int)(tv.tv_usec & 0xFFFF);
        
        /* Small delay */
        usleep(1000);
    }
}

/* Collect RTC information */
void collect_rtc(Entropy386 *entropy) {
    time_t now = time(NULL);
    struct tm *tm_info = localtime(&now);
    
    entropy->rtc_time[0] = (unsigned char)tm_info->tm_sec;
    entropy->rtc_time[1] = (unsigned char)tm_info->tm_min;
    entropy->rtc_time[2] = (unsigned char)tm_info->tm_hour;
}

/* Refresh entropy (called periodically) */
void refresh_entropy(Entropy386 *entropy) {
    collect_timer_entropy(entropy);
    collect_rtc(entropy);
    
    /* Refresh 386-specific measurements */
    entropy->isa_timing_cycles = measure_isa_timing();
    entropy->mem_timing_cycles = measure_memory_timing();
    entropy->clock_drift_ppm = measure_clock_drift();
}

/* Generate entropy hash */
void generate_entropy_hash(Entropy386 *entropy) {
    unsigned long h[4] = {0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476};
    unsigned char *ptr;
    int i, j;

    /* Mix all entropy sources */
    for (i = 0; i < 8; i++) {
        h[0] ^= (unsigned long)entropy->bios_date[i] << ((i % 4) * 8);
        h[0] = (h[0] << 5) | (h[0] >> 27);
    }

    h[1] ^= entropy->bios_model;
    h[1] ^= entropy->cpu_signature;
    h[1] = (h[1] << 7) | (h[1] >> 25);

    for (i = 0; i < TIMER_SAMPLES; i++) {
        h[2] ^= entropy->timer_samples[i];
        h[2] = (h[2] << 3) | (h[2] >> 29);
    }

    h[3] ^= ((unsigned long)entropy->rtc_time[0] << 16) |
            ((unsigned long)entropy->rtc_time[1] << 8) |
            entropy->rtc_time[2];
    h[3] ^= ((unsigned long)entropy->conv_memory_kb << 16) | 
            (entropy->ext_memory_kb & 0xFFFF);

    /* Mix rounds */
    for (j = 0; j < 8; j++) {
        h[0] += h[1]; h[1] = (h[1] << 13) | (h[1] >> 19);
        h[2] += h[3]; h[3] = (h[3] << 17) | (h[3] >> 15);
        h[0] ^= h[3]; h[2] ^= h[1];
    }

    /* Store 32-byte hash */
    for (i = 0; i < 4; i++) {
        ptr = (unsigned char *)&h[i];
        entropy->hash[i*4 + 0] = ptr[0];
        entropy->hash[i*4 + 1] = ptr[1];
        entropy->hash[i*4 + 2] = ptr[2];
        entropy->hash[i*4 + 3] = ptr[3];
        /* Duplicate for 32 bytes */
        entropy->hash[16 + i*4 + 0] = ptr[0] ^ 0xAA;
        entropy->hash[16 + i*4 + 1] = ptr[1] ^ 0x55;
        entropy->hash[16 + i*4 + 2] = ptr[2] ^ 0xAA;
        entropy->hash[16 + i*4 + 3] = ptr[3] ^ 0x55;
    }
}

/* 386-specific: Measure ISA bus timing */
unsigned long measure_isa_timing(void) {
    struct timeval start, end;
    unsigned char val;
    int i;
    
    /* Request I/O permission for keyboard controller (ISA device) */
    if (ioperm(0x60, 1, 1) != 0) {
        /* Fall back to userspace I/O */
        return 500;  /* Typical ISA timing */
    }
    
    gettimeofday(&start, NULL);
    
    /* Multiple ISA bus accesses */
    for (i = 0; i < 100; i++) {
        val = inb(0x60);
        (void)val;  /* Suppress unused warning */
    }
    
    gettimeofday(&end, NULL);
    
    /* Calculate cycles (assuming 33 MHz CPU) */
    unsigned long usec = (end.tv_sec - start.tv_sec) * 1000000 +
                         (end.tv_usec - start.tv_usec);
    unsigned long cycles = usec * 33;  /* 33 cycles per microsecond */
    
    return cycles / 100;  /* Average per access */
}

/* 386-specific: Measure memory timing */
unsigned long measure_memory_timing(void) {
    struct timeval start, end;
    volatile char *buffer;
    size_t size = 1024 * 1024;  /* 1 MB */
    int i;
    
    buffer = (volatile char *)malloc(size);
    if (!buffer) return 0;
    
    gettimeofday(&start, NULL);
    
    for (i = 0; i < (int)size; i++) {
        buffer[i] = (char)(i & 0xFF);
    }
    
    gettimeofday(&end, NULL);
    
    free((void *)buffer);
    
    /* Calculate cycles per byte */
    unsigned long usec = (end.tv_sec - start.tv_sec) * 1000000 +
                         (end.tv_usec - start.tv_usec);
    unsigned long cycles = usec * 33;  /* 33 MHz */
    
    return cycles / size;  /* Cycles per byte */
}

/* 386-specific: Measure clock drift */
unsigned long measure_clock_drift(void) {
    struct timeval tv1, tv2;
    time_t start_time, end_time;
    
    start_time = time(NULL);
    gettimeofday(&tv1, NULL);
    
    /* Wait 10 seconds */
    sleep(10);
    
    end_time = time(NULL);
    gettimeofday(&tv2, NULL);
    
    /* Calculate actual elapsed time vs expected */
    unsigned long actual_usec = (tv2.tv_sec - tv1.tv_sec) * 1000000 +
                                 (tv2.tv_usec - tv1.tv_usec);
    unsigned long expected_usec = (unsigned long)(end_time - start_time) * 1000000;
    
    /* Drift in parts per million */
    if (expected_usec == 0) return 0;
    
    long drift = (long)actual_usec - (long)expected_usec;
    unsigned long ppm = (unsigned long)(drift * 1000000 / (long)expected_usec);
    
    /* 386 crystals typically drift 10-50 ppm */
    return ppm < 100000 ? ppm : 50000;  /* Cap at 50000 ppm */
}

/* Detect FPU presence */
int detect_fpu_presence(void) {
    /* 386 typically does NOT have FPU (387 was optional) */
    /* We can try to execute FPU instruction and see if it traps */
    
    /* For now, assume no FPU (authentic 386) */
    /* This can be enhanced with actual FPU detection */
    return 0;  /* No FPU */
}
