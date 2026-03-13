//! N64 Display Module
//! 
//! Handles video output and text rendering.

/// Display width
pub const WIDTH: u32 = 320;

/// Display height
pub const HEIGHT: u32 = 240;

/// Display buffer
static mut FRAMEBUFFER: [u32; WIDTH as usize * HEIGHT as usize] = [0; WIDTH as usize * HEIGHT as usize];

/// Initialize display
pub fn init() {
    // Clear framebuffer
    clear(0x000000FF);
}

/// Clear display with color
pub fn clear(color: u32) {
    unsafe {
        for pixel in FRAMEBUFFER.iter_mut() {
            *pixel = color;
        }
    }
}

/// Print text at position
pub fn print(x: u32, y: u32, text: &str) {
    // Simplified text rendering
    // In production, use proper font rendering
    let mut cursor_x = x;
    for ch in text.chars() {
        if ch == '\n' {
            cursor_x = x;
            continue;
        }
        
        // Draw character (placeholder)
        draw_char(cursor_x, y, ch);
        cursor_x += 8; // Character width
    }
}

/// Print text centered horizontally
pub fn print_centered(y: u32, text: &str) {
    let text_width = text.len() as u32 * 8;
    let x = (WIDTH - text_width) / 2;
    print(x, y, text);
}

/// Draw a single character
fn draw_char(x: u32, y: u32, ch: char) {
    // Placeholder character rendering
    // In production, use bitmap font
    unsafe {
        for dy in 0..8 {
            for dx in 0..8 {
                let px = x + dx;
                let py = y + dy;
                if px < WIDTH && py < HEIGHT {
                    let idx = (py * WIDTH + px) as usize;
                    FRAMEBUFFER[idx] = 0xFFFFFFFF; // White
                }
            }
        }
    }
}

/// Swap buffers (display new frame)
pub fn swap_buffers() {
    #[cfg(feature = "n64-homebrew")]
    {
        unsafe {
            // Copy framebuffer to VI
            let vi_ptr = 0xA4000000 as *mut u32;
            for (i, &pixel) in FRAMEBUFFER.iter().enumerate() {
                vi_ptr.add(i).write_volatile(pixel);
            }
        }
    }
}

/// Print debug text
pub fn print_debug(text: &str) {
    // Print to IS-Viewer or similar debug output
    #[cfg(feature = "n64-homebrew")]
    {
        // Simplified debug output
        print(10, 200, text);
        swap_buffers();
    }
}
