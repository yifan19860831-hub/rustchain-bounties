//! RustChain Miner for Sega Dreamcast
//!
//! Entry point for KallistiOS

#![no_std]
#![no_main]

use rustchain_dc::Miner;

/// KallistiOS entry point
#[no_mangle]
pub extern "C" fn _kallistios_main() -> i32 {
    // Initialize KOS subsystems (handled by runtime)
    
    // Create miner instance with bounty wallet
    let mut miner = Miner::new("RTC4325af95d26d59c3ef025963656d22af638bb96b");
    
    // Initialize subsystems
    if miner.init().is_err() {
        return -1;
    }
    
    // Connect to pool (configured in storage or default)
    if miner.connect("pool.rustchain.org", 3333).is_err() {
        return -2;
    }
    
    // Start mining loop (runs forever)
    miner.start();
    
    0
}
