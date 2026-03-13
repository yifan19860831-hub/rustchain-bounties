/*
 * RUSTCHAIN 386 MINER - Network Header
 */

#ifndef NETWORK_H
#define NETWORK_H

/* Initialize network */
int network_init(void);

/* Submit attestation via HTTP POST */
int submit_attestation(const char *host, int port, const char *json);

/* Build attestation JSON */
void build_attestation_json(const void *wallet, 
                           const void *fingerprint,
                           const void *entropy,
                           char *buffer,
                           size_t buffer_size);

#endif /* NETWORK_H */
