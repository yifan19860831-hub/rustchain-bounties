/*
 * RUSTCHAIN 386 MINER - Wallet Management
 * 
 * Wallet generation from hardware entropy
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "wallet.h"
#include "entropy.h"

/* Load wallet from file */
int wallet_load(Wallet386 *wallet, const char *path) {
    FILE *fp = fopen(path, "r");
    if (!fp) {
        return 0;
    }

    char line[256];
    int line_num = 0;
    
    while (fgets(line, sizeof(line), fp)) {
        /* Skip comments */
        if (line[0] == '#') continue;
        
        /* Remove newline */
        line[strcspn(line, "\n")] = 0;
        
        if (line_num == 0) {
            /* Wallet ID */
            strncpy(wallet->wallet_id, line, sizeof(wallet->wallet_id) - 1);
            wallet->wallet_id[sizeof(wallet->wallet_id) - 1] = '\0';
        } else if (line_num == 1) {
            /* Miner ID */
            strncpy(wallet->miner_id, line, sizeof(wallet->miner_id) - 1);
            wallet->miner_id[sizeof(wallet->miner_id) - 1] = '\0';
        } else if (line_num == 2) {
            /* Created timestamp */
            sscanf(line, "%lu", &wallet->created);
        }
        
        line_num++;
        if (line_num >= 3) break;
    }
    
    fclose(fp);
    
    if (wallet->wallet_id[0] != '\0' && wallet->miner_id[0] != '\0') {
        wallet->initialized = 1;
        return 1;
    }
    
    return 0;
}

/* Save wallet to file */
int wallet_save(const Wallet386 *wallet, const char *path) {
    FILE *fp = fopen(path, "w");
    if (!fp) {
        perror("Cannot save wallet");
        return 0;
    }

    fprintf(fp, "%s\n", wallet->wallet_id);
    fprintf(fp, "%s\n", wallet->miner_id);
    fprintf(fp, "%lu\n", wallet->created);
    fprintf(fp, "# RustChain 386 Miner Wallet\n");
    fprintf(fp, "# DO NOT DELETE THIS FILE!\n");
    fprintf(fp, "# Backup to floppy disk!\n");
    
    fclose(fp);
    
    printf("Wallet saved to %s\n", path);
    return 1;
}

/* Generate wallet from entropy */
int wallet_generate(Wallet386 *wallet, const void *entropy_ptr) {
    const Entropy386 *entropy = (const Entropy386 *)entropy_ptr;
    int i;
    static const char hex[] = "0123456789abcdef";

    /* Wallet format: RTC + 40 hex chars from entropy hash */
    strcpy(wallet->wallet_id, "RTC");
    for (i = 0; i < 20; i++) {
        wallet->wallet_id[3 + i*2] = hex[(entropy->hash[i] >> 4) & 0x0F];
        wallet->wallet_id[3 + i*2 + 1] = hex[entropy->hash[i] & 0x0F];
    }
    wallet->wallet_id[43] = '\0';

    /* Miner ID: 386-XXXXXXXX */
    sprintf(wallet->miner_id, "386-%02X%02X%02X%02X",
            entropy->hash[0], entropy->hash[1],
            entropy->hash[2], entropy->hash[3]);

    wallet->created = (unsigned long)time(NULL);
    wallet->initialized = 1;
    
    return 1;
}
