//! TLB Timing Fingerprint
//! 
//! Measures Translation Lookaside Buffer characteristics.

/// N64 TLB entries
const TLB_ENTRIES: usize = 48;

/// Measure TLB timing pattern
pub fn measure() -> u32 {
    #[cfg(feature = "n64-homebrew")]
    {
        let mut timing_sum = 0u32;
        
        // Probe TLB entries
        for i in 0..TLB_ENTRIES {
            let start = get_cycle_count();
            
            // Access page that may cause TLB miss
            access_page(i);
            
            let end = get_cycle_count();
            timing_sum = timing_sum.wrapping_add(end.wrapping_sub(start));
        }
        
        // Create pattern
        timing_sum ^ (timing_sum >> 8)
    }
    #[cfg(not(feature = "n64-homebrew"))]
    {
        0xABCD1234
    }
}

/// Access a page to probe TLB
fn access_page(page_num: usize) {
    #[cfg(feature = "n64-homebrew")]
    {
        unsafe {
            // Access memory at different pages
            let addr = 0x80100000 + (page_num * 4096);
            let ptr = addr as *mut u8;
            ptr.write_volatile(1);
        }
    }
}

/// Get CPU cycle count
fn get_cycle_count() -> u32 {
    #[cfg(feature = "n64-homebrew")]
    {
        unsafe {
            let count: u32;
            core::arch::asm!("mfc0 {0}, $9", out(reg) count);
            count
        }
    }
    #[cfg(not(feature = "n64-homebrew"))]
    {
        0
    }
}
