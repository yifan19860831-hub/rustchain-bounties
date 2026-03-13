/*
 * RUSTCHAIN 386 MINER - Main Header
 */

#ifndef MINER_H
#define MINER_H

/* Configuration structure */
typedef struct {
    char node_host[64];
    int node_port;
    char wallet_file[128];
    int use_network;
    int dev_fee_enabled;
    char dev_fee_wallet[48];
    char dev_fee_amount[16];
} MinerConfig;

/* Function prototypes */
void print_banner(void);
void print_status(void);
int load_config(void);
void mining_loop(void);
int init_miner(void);

#endif /* MINER_H */
