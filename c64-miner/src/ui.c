/**
 * User Interface Implementation
 */

#include "ui.h"
#include <stdio.h>
#include <conio.h>
#include <c64.h>
#include <time.h>

/**
 * Initialize UI
 */
void ui_init(void) {
    clrscr();
    bordercolor(COLOR_BLUE);
    bgcolor(COLOR_BLACK);
    textcolor(COLOR_WHITE);
}

/**
 * Show splash screen
 */
void ui_show_splash(void) {
    clrscr();
    textcolor(COLOR_YELLOW);
    
    gotoxy(5, 3);
    cprintf("################################");
    gotoxy(5, 4);
    cprintf("#                              #");
    gotoxy(5, 5);
    cprintf("#   RUSTCHAIN MINER v0.1      #");
    gotoxy(5, 6);
    cprintf("#   Commodore 64 Edition       #");
    gotoxy(5, 7);
    cprintf("#                              #");
    gotoxy(5, 8);
    cprintf("#   150 RTC Bounty             #");
    gotoxy(5, 9);
    cprintf("#   4.0x Multiplier            #");
    gotoxy(5, 10);
    cprintf("#                              #");
    gotoxy(5, 11);
    cprintf("#   Wallet:                    #");
    gotoxy(5, 12);
    cprintf("#   RTC4325af95d26d59c3ef...  #");
    gotoxy(5, 13);
    cprintf("#                              #");
    gotoxy(5, 14);
    cprintf("################################");
    
    textcolor(COLOR_WHITE);
    gotoxy(5, 16);
    cprintf("Press any key to start...");
}

/**
 * Show main screen layout
 */
void ui_show_main_screen(void) {
    textcolor(COLOR_WHITE);
    
    // Header
    gotoxy(1, 1);
    cprintf("+----------------------------------------+");
    gotoxy(1, 2);
    cprintf("|  RUSTCHAIN MINER v0.1 - C64           |");
    gotoxy(1, 3);
    cprintf("+----------------------------------------+");
    
    // Status area
    gotoxy(2, 5);
    cprintf("STATUS: INITIALIZING...");
    gotoxy(2, 6);
    cprintf("EPOCH:  --:-- REMAINING");
    gotoxy(2, 7);
    cprintf("EARNED: 0.0000 RTC");
    
    // Hardware info
    gotoxy(2, 9);
    cprintf("HARDWARE:");
    gotoxy(2, 10);
    cprintf("CPU: MOS 6510 @ 1.023 MHZ");
    gotoxy(2, 11);
    cprintf("RAM: 64 KB");
    gotoxy(2, 12);
    cprintf("NET: WAITING...");
    
    // Menu
    gotoxy(1, 22);
    cprintf("+----------------------------------------+");
    gotoxy(1, 23);
    cprintf("| [F1] PAUSE  [F3] MENU  [F5] QUIT      |");
    gotoxy(1, 24);
    cprintf("+----------------------------------------+");
}

/**
 * Show status message
 */
void ui_show_status(const char* status) {
    gotoxy(2, 5);
    cprintf("STATUS: %-20s", status);
}

/**
 * Show earned amount
 */
void ui_show_earned(float rtc) {
    gotoxy(2, 7);
    cprintf("EARNED: %.4f RTC       ", rtc);
}

/**
 * Show epoch count
 */
void ui_show_epoch(unsigned int count) {
    gotoxy(20, 6);
    cprintf("EPOCH #%u", count);
}

/**
 * Show fingerprint info
 */
void ui_show_fingerprint(C64Fingerprint* fp) {
    gotoxy(2, 14);
    cprintf("FINGERPRINT:");
    gotoxy(2, 15);
    cprintf("CIA:  %08lX", fp->cia_timer_fp);
    gotoxy(2, 16);
    cprintf("VIC:  %08lX", fp->vic_raster_fp);
    gotoxy(2, 17);
    cprintf("SID:  %04X", (unsigned int)fp->sid_fp);
    gotoxy(2, 18);
    cprintf("ROM:  %04X", fp->rom_checksum);
}

/**
 * Show countdown timer
 */
void ui_countdown(unsigned int seconds) {
    unsigned int mins, secs;
    clock_t start, current;
    
    start = clock();
    
    while (seconds > 0) {
        mins = seconds / 60;
        secs = seconds % 60;
        
        gotoxy(2, 6);
        cprintf("EPOCH:  %02u:%02u REMAINING     ", mins, secs);
        
        // Wait approximately 1 second
        current = clock();
        while ((current - start) < CLOCKS_PER_SEC) {
            // Check for user input
            if (kbhit()) {
                char key = cgetc();
                if (key == CH_F1) {
                    // Pause
                    cprintf("\nPAUSED - PRESS F1 TO RESUME");
                    while (cgetc() != CH_F1);
                } else if (key == CH_F5) {
                    // Quit
                    return;
                }
            }
            current = clock();
        }
        start = current;
        seconds--;
    }
}

/**
 * Handle keyboard input
 */
void ui_handle_input(int* running, int* paused) {
    if (kbhit()) {
        char key = cgetc();
        
        switch (key) {
            case CH_F1:
                // Toggle pause
                *paused = !*paused;
                break;
            case CH_F3:
                // Show menu (placeholder)
                gotoxy(1, 20);
                cprintf("MENU: [M] NETWORK  [I] INFO  [X] EXIT");
                break;
            case CH_F5:
                // Quit
                *running = 0;
                break;
            case 'm':
            case 'M':
                // Network info
                gotoxy(2, 12);
                cprintf("NET: RR-NET CONNECTED   ");
                break;
            case 'i':
            case 'I':
                // Show info
                gotoxy(1, 20);
                cprintf("INFO: C64 Miner v0.1 - 150 RTC Bounty");
                break;
            case 'x':
            case 'X':
                // Exit
                *running = 0;
                break;
        }
    }
}
