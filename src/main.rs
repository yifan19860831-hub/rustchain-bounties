mod pdp8_cpu;
mod arithmetic;
mod sha256;
mod miner;

use sha256::{SHA256, digest_to_hex};
use miner::Miner;

fn main() {
    println!("RustChain PDP-8 Miner - LEGENDARY Tier Bounty\n");
    
    println!("Testing SHA256...");
    let h1 = SHA256::hash(b"");
    println!("SHA256(\"\") = {}", digest_to_hex(&h1));
    
    let h2 = SHA256::hash(b"abc");
    println!("SHA256(\"abc\") = {}", digest_to_hex(&h2));
    
    println!("\nTesting Mining...");
    let mut miner = Miner::new();
    miner.set_header(b"test block", 0);
    miner.set_target(0xFFFFFFFF);
    let result = miner.mine(0, 100);
    println!("Mining: {} attempts", result.attempts);
    
    println!("\nBounty Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b");
    println!("Issue: #1848 - Port Miner to DEC PDP-8 (1965)");
}
