//! N64 Platform Layer
//! 
//! Provides hardware abstraction for Nintendo 64.

pub mod display;
pub mod controller;
pub mod storage;

/// Initialize N64 hardware
pub fn init() {
    // Initialize video interface
    display::init();
    
    // Initialize controller interface
    controller::init();
    
    // Initialize storage (Controller Pak)
    storage::init();
}

/// Shutdown N64 hardware
pub fn shutdown() {
    // Clean shutdown
    display::clear(0x000000FF);
    display::swap_buffers();
}

/// Get current time in milliseconds
pub fn get_time_ms() -> u64 {
    #[cfg(feature = "n64-homebrew")]
    {
        // Use VI counter for timing
        unsafe {
            let vi_count = *(0xA4400000 as *const u32);
            (vi_count as u64) * 16 // VI runs at ~60 Hz
        }
    }
    #[cfg(not(feature = "n64-homebrew"))]
    {
        0
    }
}

/// Delay for specified milliseconds
pub fn delay_ms(ms: u32) {
    #[cfg(feature = "n64-homebrew")]
    {
        let start = get_time_ms();
        while get_time_ms() - start < ms as u64 {
            core::hint::black_box(());
        }
    }
}

/// Print to debug output
pub fn debug_print(text: &str) {
    #[cfg(feature = "n64-homebrew")]
    {
        // Use IS-Viewer debug output if available
        // Or print to screen
        display::print_debug(text);
    }
}

/// COP0 register access
pub mod cop0 {
    /// Read Count register
    pub unsafe fn read_count() -> u32 {
        let count: u32;
        core::arch::asm!("mfc0 {0}, $9", out(reg) count);
        count
    }
    
    /// Read PRId (Processor ID)
    pub fn read_prid() -> u32 {
        unsafe {
            let prid: u32;
            core::arch::asm!("mfc0 {0}, $15", out(reg) prid);
            prid
        }
    }
}

/// Random number generation
pub mod rng {
    /// Generate next random byte
    pub fn next_byte() -> u8 {
        #[cfg(feature = "n64-homebrew")]
        {
            // Use RCP noise source
            unsafe {
                let noise = *(0xA4600000 as *const u32);
                (noise & 0xFF) as u8
            }
        }
        #[cfg(not(feature = "n64-homebrew"))]
        {
            0x42
        }
    }
}
