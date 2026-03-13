/**
 * User Interface
 */

#ifndef UI_H
#define UI_H

#include "fingerprint.h"

// Initialize UI
void ui_init(void);

// Show splash screen
void ui_show_splash(void);

// Show main screen
void ui_show_main_screen(void);

// Show status message
void ui_show_status(const char* status);

// Show earned amount
void ui_show_earned(float rtc);

// Show epoch count
void ui_show_epoch(unsigned int count);

// Show fingerprint info
void ui_show_fingerprint(C64Fingerprint* fp);

// Show countdown timer
void ui_countdown(unsigned int seconds);

// Handle keyboard input
void ui_handle_input(int* running, int* paused);

#endif
