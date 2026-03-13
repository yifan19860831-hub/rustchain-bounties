//! Cache Timing Fingerprint
//! 
//! Measures N64's 16 KB L1 cache characteristics.

/// N64 L1 cache size (data cache)
const CACHE_SIZE: usize = 8192;

/// Cache line size
const CACHE_LINE: usize = 16;

/// Measure cache timing pattern
pub fn measure() -> u32 {
    #[cfg(feature = "n64-homebrew")]
    {
        let mut buffer: [u8; CACHE_SIZE] = [0; CACHE_SIZE];
        let mut total_time = 0u32;
        
        // Test different access patterns
        for stride in [1, 2, 4, 8, 16, 32, 64, 128] {
            let start = get_cycle_count();
            
            for i in (0..CACHE_SIZE).step_by(stride * CACHE_LINE) {
                unsafe {
                    let ptr = buffer.as_mut_ptr().add(i);
                    ptr.write_volatile(1);
                }
            }
            
            let end = get_cycle_count();
            total_time = total_time.wrapping_add(end.wrapping_sub(start));
        }
        
        // Create pattern from timing
        total_time ^ (total_time >> 16)
    }
    #[cfg(not(feature = "n64-homebrew"))]
    {
        0x87654321
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
