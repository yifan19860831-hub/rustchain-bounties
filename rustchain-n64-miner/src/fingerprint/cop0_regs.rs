//! COP0 Register Fingerprint
//! 
//! Reads processor-specific control registers.

/// Read COP0 registers
pub fn read() -> u64 {
    #[cfg(feature = "n64-homebrew")]
    {
        let mut regs: u64 = 0;
        
        unsafe {
            // Read Config register (CP0 Register 16)
            let config: u32;
            core::arch::asm!("mfc0 {0}, $16", out(reg) config);
            regs = regs.wrapping_add(config as u64);
            
            // Read Config1 register (CP0 Register 16, Select 1)
            let config1: u32;
            core::arch::asm!("mfc0 {0}, $16, 1", out(reg) config1);
            regs = regs.wrapping_add((config1 as u64) << 32);
            
            // Read PRId (Processor ID, CP0 Register 15)
            let prid: u32;
            core::arch::asm!("mfc0 {0}, $15", out(reg) prid);
            regs = regs.wrapping_xor(prid as u64);
        }
        
        regs
    }
    #[cfg(not(feature = "n64-homebrew"))]
    {
        0x123456789ABCDEF0
    }
}

/// Read Processor ID
pub fn read_prid() -> u32 {
    #[cfg(feature = "n64-homebrew")]
    {
        unsafe {
            let prid: u32;
            core::arch::asm!("mfc0 {0}, $15", out(reg) prid);
            prid
        }
    }
    #[cfg(not(feature = "n64-homebrew"))]
    {
        0
    }
}

/// Read Config register
pub fn read_config() -> u32 {
    #[cfg(feature = "n64-homebrew")]
    {
        unsafe {
            let config: u32;
            core::arch::asm!("mfc0 {0}, $16", out(reg) config);
            config
        }
    }
    #[cfg(not(feature = "n64-homebrew"))]
    {
        0
    }
}
