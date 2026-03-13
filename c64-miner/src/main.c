/**
 * RustChain Miner for Commodore 64
 * 
 * Target: MOS 6510 @ 1.023 MHz, 64 KB RAM
 * Bounty: 150 RTC (4.0x multiplier)
 * Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <conio.h>
#include <c64.h>
#include "miner.h"
#include "network.h"
#include "fingerprint.h"
#include "ui.h"

// Wallet address for bounty claims
#define WALLET_ADDRESS "RTC4325af95d26d59c3ef025963656d22af638bb96b"

// Epoch duration in seconds (10 minutes)
#define EPOCH_SECONDS 600

// Global state
static int miner_running = 1;
static int miner_paused = 0;
static float total_earned = 0.0f;
static unsigned int epoch_count = 0;

/**
 * Main entry point
 */
void main(void) {
    C64Fingerprint fp;
    char json_payload[512];
    char response[1024];
    int result;
    
    // Initialize
    ui_init();
    
    // Show splash screen
    ui_show_splash();
    cgetc();  // Wait for keypress
    
    // Clear screen and show main UI
    clrscr();
    ui_show_main_screen();
    
    // Initialize network
    ui_show_status("INITIALIZING NETWORK...");
    if (network_init() != 0) {
        ui_show_status("NETWORK INIT FAILED!");
        goto error;
    }
    ui_show_status("NETWORK READY");
    
    // Build hardware fingerprint
    ui_show_status("COLLECTING FINGERPRINT...");
    build_fingerprint(&fp);
    
    // Display fingerprint info
    ui_show_fingerprint(&fp);
    
    // Main mining loop
    while (miner_running) {
        // Handle user input
        ui_handle_input(&miner_running, &miner_paused);
        
        if (miner_paused) {
            ui_show_status("PAUSED");
            continue;
        }
        
        // Perform attestation
        ui_show_status("ATTESTING...");
        
        // Build JSON payload
        build_attestation_json(&fp, WALLET_ADDRESS, json_payload, sizeof(json_payload));
        
        // Connect to server
        if (network_connect() != 0) {
            ui_show_status("CONNECT FAILED");
            sleep(5);
            continue;
        }
        
        // Send attestation
        result = http_post("/api/attest", json_payload, response, sizeof(response));
        
        network_close();
        
        if (result == 0) {
            // Parse response (simplified)
            float reward = parse_reward(response);
            total_earned += reward;
            epoch_count++;
            
            ui_show_status("SUCCESS");
            ui_show_earned(total_earned);
            ui_show_epoch(epoch_count);
        } else {
            ui_show_status("FAILED - RETRYING");
        }
        
        // Wait for next epoch
        ui_show_status("WAITING FOR NEXT EPOCH...");
        ui_countdown(EPOCH_SECONDS);
    }
    
    // Cleanup
    ui_show_status("SHUTTING DOWN...");
    network_close();
    
    return;
    
error:
    ui_show_status("FATAL ERROR - PRESS KEY");
    cgetc();
    exit(1);
}
