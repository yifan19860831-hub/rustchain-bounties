/*
 * RUSTCHAIN 386 MINER - Wallet Header
 */

#ifndef WALLET_H
#define WALLET_H

/* Wallet structure */
typedef struct {
    char wallet_id[48];     /* RTC + 40 hex chars */
    char miner_id[32];      /* 386-XXXXXXXX */
    unsigned long created;  /* Unix timestamp */
    int initialized;
} Wallet386;

/* Function prototypes */
int wallet_load(Wallet386 *wallet, const char *path);
int wallet_save(const Wallet386 *wallet, const char *path);
int wallet_generate(Wallet386 *wallet, const void *entropy);

#endif /* WALLET_H */
