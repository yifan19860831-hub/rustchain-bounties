/*
 * RUSTCHAIN 386 MINER - "Fossil Edition"
 * For Intel 386 architecture running Linux (Slackware 3.0+)
 *
 * Copyright (c) 2026 RustChain Project
 * SPDX-License-Identifier: Apache-2.0
 *
 * Compile: gcc -m386 -O2 -o rustchain-386-miner miner.c entropy.c \
 *          fingerprint.c network.c wallet.c -lm
 *
 * Dev Fee: 0.001 RTC/epoch -> founder_dev_fund
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include <signal.h>
#include <sys/time.h>
#include <sys/types.h>

#include "miner.h"
#include "entropy.h"
#include "fingerprint.h"
#include "network.h"
#include "wallet.h"

/* Configuration */
#define NODE_HOST "rustchain.org"
#define NODE_PORT 8088
#define BLOCK_TIME 600
#define DEV_FEE "0.001"
#define DEV_WALLET "founder_dev_fund"
#define WALLET_FILE "wallet.dat"
#define CONFIG_FILE "miner.cfg"

/* Global state */
static Entropy386 g_entropy;
static Wallet386 g_wallet;
static Fingerprint386 g_fingerprint;
static int g_network_ok = 0;
static volatile int g_running = 1;

/* Signal handler */
void signal_handler(int sig) {
    (void)sig;
    printf("\nReceived interrupt, shutting down...\n");
    g_running = 0;
}

/* Print banner */
void print_banner(void) {
    printf("\n");
    printf("======================================================\n");
    printf("  RUSTCHAIN 386 MINER - Fossil Edition\n");
    printf("  Intel 386 Architecture (1985)\n");
    printf("  \"Every vintage computer has historical potential\"\n");
    printf("======================================================\n");
    printf("  Dev Fee: %s RTC/epoch -> %s\n", DEV_FEE, DEV_WALLET);
    printf("======================================================\n\n");
}

/* Print status */
void print_status(void) {
    printf("\n--- MINER STATUS ---\n");
    printf("Wallet:    %s\n", g_wallet.wallet_id);
    printf("Miner ID:  %s\n", g_wallet.miner_id);
    printf("CPU:       %s (0x%08lX)\n", 
           g_fingerprint.cpu_vendor, g_fingerprint.cpu_signature);
    printf("BIOS:      %s\n", g_fingerprint.bios_date);
    printf("Memory:    %lu KB total\n", g_entropy.mem_total_kb);
    printf("FPU:       %s\n", g_fingerprint.has_fpu ? "Present" : "Not detected (authentic 386!)");
    printf("ISA Timing: %lu cycles\n", g_fingerprint.isa_timing_cycles);
    printf("Clock Drift: %lu ppm\n", g_fingerprint.clock_drift_ppm);
    printf("Network:   %s\n", g_network_ok ? "Online" : "Offline");
    printf("Node:      %s:%d\n", NODE_HOST, NODE_PORT);
    printf("Architecture: %s (4.0x multiplier!)\n", g_fingerprint.arch);
    printf("--------------------\n\n");
}

/* Load configuration */
int load_config(void) {
    FILE *fp = fopen(CONFIG_FILE, "r");
    if (!fp) {
        printf("Config file not found, using defaults\n");
        return 0;
    }

    char line[256];
    while (fgets(line, sizeof(line), fp)) {
        if (line[0] == '#' || line[0] == '\n') continue;
        
        char key[64], value[128];
        if (sscanf(line, "%63[^=]=%127s", key, value) == 2) {
            if (strcmp(key, "node_host") == 0) {
                /* Could override NODE_HOST */
            } else if (strcmp(key, "node_port") == 0) {
                /* Could override NODE_PORT */
            } else if (strcmp(key, "wallet_file") == 0) {
                /* Could override WALLET_FILE */
            }
        }
    }
    
    fclose(fp);
    return 1;
}

/* Main mining loop */
void mining_loop(void) {
    unsigned long next_attest = 0;
    unsigned long now;
    int cycle = 0;

    printf("Starting mining loop (Ctrl+C to exit)...\n\n");

    while (g_running) {
        now = (unsigned long)time(NULL);

        if (now >= next_attest) {
            cycle++;
            printf("[%lu] Cycle %d: Collecting entropy...\n", now, cycle);

            /* Refresh entropy */
            refresh_entropy(&g_entropy);
            
            /* Regenerate hash */
            generate_entropy_hash(&g_entropy);

            if (g_network_ok) {
                printf("[%lu] Sending attestation to node...\n", now);
                
                /* Build attestation JSON */
                char json[2048];
                build_attestation_json(&g_wallet, &g_fingerprint, 
                                      &g_entropy, json, sizeof(json));
                
                if (submit_attestation(NODE_HOST, NODE_PORT, json)) {
                    printf("[%lu] SUCCESS! Attestation accepted.\n", now);
                } else {
                    printf("[%lu] WARN: Attestation failed, will retry.\n", now);
                    
                    /* Save to file for later submission */
                    FILE *fp = fopen("attestation_pending.json", "w");
                    if (fp) {
                        fprintf(fp, "%s\n", json);
                        fclose(fp);
                        printf("[%lu] Saved to attestation_pending.json\n", now);
                    }
                }
            } else {
                printf("[%lu] Offline mode - saving entropy locally.\n", now);
                
                /* Save to file for later submission */
                FILE *fp = fopen("attestation.txt", "a");
                if (fp) {
                    fprintf(fp, "[%lu] Cycle %d\n", now, cycle);
                    fprintf(fp, "Hash: ");
                    for (int i = 0; i < 32; i++) {
                        fprintf(fp, "%02x", g_entropy.hash[i]);
                    }
                    fprintf(fp, "\n\n");
                    fclose(fp);
                }
            }

            next_attest = now + BLOCK_TIME;
            printf("[%lu] Next attestation in %d seconds.\n\n", now, BLOCK_TIME);
        }

        /* Check for keypress (non-blocking) */
        /* Note: This requires termios setup for non-blocking input */
        /* For now, just sleep */
        sleep(1);
    }
}

/* Initialize miner */
int init_miner(void) {
    printf("Initializing...\n\n");

    /* Collect initial entropy */
    printf("[1/5] Collecting BIOS info...\n");
    collect_bios_info(&g_entropy);

    printf("[2/5] Detecting CPU...\n");
    detect_cpu(&g_entropy);

    printf("[3/5] Reading memory config...\n");
    collect_memory_info(&g_entropy);

    printf("[4/5] Collecting timer entropy...\n");
    collect_timer_entropy(&g_entropy);
    collect_rtc(&g_entropy);

    printf("[5/5] Generating entropy hash...\n");
    generate_entropy_hash(&g_entropy);

    /* Generate fingerprint */
    printf("\nGenerating 386 fingerprint...\n");
    generate_fingerprint(&g_fingerprint, &g_entropy);

    /* Load or generate wallet */
    printf("\nChecking for existing wallet...\n");
    if (wallet_load(&g_wallet, WALLET_FILE)) {
        printf("Loaded wallet: %s\n", g_wallet.wallet_id);
    } else {
        printf("No wallet found, generating new wallet...\n");
        wallet_generate(&g_wallet, &g_entropy);
        wallet_save(&g_wallet, WALLET_FILE);
        printf("\n");
        printf("========================================\n");
        printf("  NEW WALLET GENERATED!\n");
        printf("  %s\n", g_wallet.wallet_id);
        printf("========================================\n");
        printf("  SAVE THIS! Backup %s to floppy!\n", WALLET_FILE);
        printf("========================================\n\n");
    }

    /* Initialize network */
    printf("Initializing network...\n");
    if (network_init()) {
        printf("Network: Online\n");
        g_network_ok = 1;
    } else {
        printf("Network: Offline mode\n");
        g_network_ok = 0;
    }

    return 1;
}

/* Main entry point */
int main(int argc, char *argv[]) {
    (void)argc;
    (void)argv;

    print_banner();

    /* Load configuration */
    load_config();

    /* Set up signal handlers */
    signal(SIGINT, signal_handler);
    signal(SIGTERM, signal_handler);

    /* Initialize miner */
    if (!init_miner()) {
        fprintf(stderr, "Failed to initialize miner\n");
        return 1;
    }

    /* Show status */
    print_status();

    /* Start mining */
    printf("Press Ctrl+C to quit.\n\n");
    mining_loop();

    printf("\nMiner stopped. Wallet: %s\n", g_wallet.wallet_id);
    return 0;
}
