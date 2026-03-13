/**
 * Miner Core Logic
 */

#ifndef MINER_H
#define MINER_H

#include "fingerprint.h"

// Build JSON attestation payload
void build_attestation_json(C64Fingerprint* fp, const char* wallet, char* buffer, int max_len);

// Parse reward from response
float parse_reward(const char* response);

#endif
