/**
 * Miner Core Implementation
 */

#include "miner.h"
#include <stdio.h>
#include <string.h>

void build_attestation_json(C64Fingerprint* fp, const char* wallet, char* buffer, int max_len) {
    snprintf(buffer, max_len,
        "{"
        "\"device_arch\":\"%s\","
        "\"device_family\":\"%s\","
        "\"cpu_speed\":%lu,"
        "\"total_ram_kb\":%u,"
        "\"cia_timer_fp\":%lu,"
        "\"vic_raster_fp\":%lu,"
        "\"sid_fp\":%lu,"
        "\"rom_checksum\":%u,"
        "\"wallet\":\"%s\""
        "}",
        fp->device_arch,
        fp->device_family,
        fp->cpu_speed,
        fp->total_ram_kb,
        fp->cia_timer_fp,
        fp->vic_raster_fp,
        fp->sid_fp,
        fp->rom_checksum,
        wallet
    );
}

float parse_reward(const char* response) {
    // Simplified JSON parsing
    // Look for "reward":X.XXXX pattern
    const char* reward_str = strstr(response, "\"reward\":");
    if (reward_str) {
        reward_str += 9;  // Skip "\"reward\":"
        return (float)atof(reward_str);
    }
    return 0.0f;
}
