//! N64 Controller Module
//! 
//! Handles controller input.

/// Controller button: A
pub const BUTTON_A: u16 = 0x8000;

/// Controller button: B
pub const BUTTON_B: u16 = 0x4000;

/// Controller button: Z
pub const BUTTON_Z: u16 = 0x2000;

/// Controller button: Start
pub const BUTTON_START: u16 = 0x1000;

/// Controller button: D-Pad Up
pub const BUTTON_UP: u16 = 0x0800;

/// Controller button: D-Pad Down
pub const BUTTON_DOWN: u16 = 0x0400;

/// Controller button: D-Pad Left
pub const BUTTON_LEFT: u16 = 0x0200;

/// Controller button: D-Pad Right
pub const BUTTON_RIGHT: u16 = 0x0100;

/// Initialize controller
pub fn init() {
    #[cfg(feature = "n64-homebrew")]
    {
        // Initialize PIF (Peripheral Interface)
        unsafe {
            let pif_ram = 0xA4600000 as *mut u8;
            // Reset controller
            pif_ram.write_volatile(0xFF);
        }
    }
}

/// Read controller buttons
pub fn read_buttons() -> u16 {
    #[cfg(feature = "n64-homebrew")]
    {
        unsafe {
            // Read from PIF RAM
            let pif_ram = 0xA4600024 as *const u16;
            pif_ram.read_volatile()
        }
    }
    #[cfg(not(feature = "n64-homebrew"))]
    {
        0
    }
}

/// Check if button is pressed
pub fn is_pressed(button: u16) -> bool {
    read_buttons() & button != 0
}

/// Wait for button press
pub fn wait_for_button(button: u16) {
    loop {
        if is_pressed(button) {
            break;
        }
        crate::n64::delay_ms(16);
    }
}
