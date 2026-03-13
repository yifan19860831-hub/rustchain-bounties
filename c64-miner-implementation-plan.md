# Commodore 64 RustChain Miner - Implementation Plan

## Project Overview

**Goal:** Port RustChain miner to Commodore 64 (1982)
**Target Hardware:** MOS 6510 @ 1.023 MHz, 64 KB RAM
**Bounty:** 150 RTC (4.0x multiplier)
**Wallet:** RTC4325af95d26d59c3ef025963656d22af638bb96b

---

## Phase 1: Development Environment Setup (Week 1-2)

### 1.1 Install Toolchain

```powershell
# Windows (Chocolatey)
choco install cc65
choco install vice

# Or download manually:
# cc65: https://cc65.github.io
# VICE: https://vice-emu.sourceforge.io
```

### 1.2 Project Structure

```
c64-miner/
├── src/
│   ├── main.c              # Entry point
│   ├── miner.c             # Core miner logic
│   ├── miner.h
│   ├── network.c           # Network stack interface
│   ├── network.h
│   ├── fingerprint.c       # Hardware fingerprinting
│   ├── fingerprint.h
│   ├── ui.c                # User interface
│   ├── ui.h
│   └── json.c              # Minimal JSON builder/parser
├── asm/
│   ├── startup.s           # 6502 startup code
│   ├── fingerprint.s       # Performance-critical fingerprint routines
│   └── sha256.s            # Optional: SHA-256 in assembly
├── include/
│   └── c64.h               # C64 hardware definitions
├── Makefile
├── README.md
└── miner.prg               # Output binary
```

### 1.3 Hello World Test

```c
// src/main.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <conio.h>
#include <c64.h>

void main(void) {
    clrscr();
    screensize(40, 25);
    
    printf("+----------------------------------------+\n");
    printf("|  RUSTCHAIN MINER v0.1 - C64           |\n");
    printf("+----------------------------------------+\n");
    printf("|  Development Test OK                  |\n");
    printf("|  Press any key to exit...             |\n");
    printf("+----------------------------------------+\n");
    
    cgetc();  // Wait for keypress
}
```

**Build:**
```bash
cl65 -t c64 -o miner.prg src/main.c
```

**Test in VICE:**
```bash
x64 miner.prg
```

---

## Phase 2: Network Stack Implementation (Week 3-10)

### 2.1 Network Hardware Selection

**Recommended:** RR-Net Ethernet Cartridge
- Cost: ~$80-150
- Documentation: https://www.c64-wiki.com/wiki/RR-Net
- Library: tcpip.lib (included with cc65)

**Alternative:** Userport + ESP32 Bridge
- Cost: ~$20 (ESP32 dev board)
- More work but cheaper
- Requires ESP32 firmware development

### 2.2 RR-Net Integration

```c
// src/network.c
#include <tcpip.h>
#include <string.h>
#include <stdio.h>

#define SERVER_IP "rustchain.org"
#define SERVER_PORT 80

static unsigned char ip_buffer[256];
static int sockfd = -1;

int network_init(void) {
    // Initialize network stack
    if (tcpip_init() != 0) {
        return -1;
    }
    return 0;
}

int network_connect(void) {
    struct sockaddr_in server;
    
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        return -1;
    }
    
    server.sin_family = AF_INET;
    server.sin_port = htons(SERVER_PORT);
    // Resolve hostname or use hardcoded IP
    
    if (connect(sockfd, (struct sockaddr*)&server, sizeof(server)) < 0) {
        return -1;
    }
    
    return 0;
}

int network_send(const char* data, int len) {
    return send(sockfd, data, len, 0);
}

int network_recv(char* buffer, int max_len) {
    return recv(sockfd, buffer, max_len, 0);
}

void network_close(void) {
    if (sockfd >= 0) {
        close(sockfd);
        sockfd = -1;
    }
}
```

### 2.3 HTTP Client

```c
// Minimal HTTP POST client
int http_post(const char* path, const char* json_body, char* response, int max_response_len) {
    char request[512];
    
    sprintf(request,
        "POST %s HTTP/1.0\r\n"
        "Host: rustchain.org\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: %d\r\n"
        "\r\n"
        "%s",
        path, strlen(json_body), json_body);
    
    network_send(request, strlen(request));
    
    // Read response
    int bytes = network_recv(response, max_response_len);
    if (bytes < 0) {
        return -1;
    }
    
    // Find body (skip headers)
    char* body = strstr(response, "\r\n\r\n");
    if (body) {
        memmove(response, body + 4, strlen(body + 4) + 1);
    }
    
    return 0;
}
```

---

## Phase 3: Hardware Fingerprinting (Week 11-16)

### 3.1 CIA Timer Fingerprint

```c
// src/fingerprint.c
#include <c64.h>

// CIA #1 registers
#define CIA1_PRA    (*(volatile unsigned char*)0xDC00)
#define CIA1_PRA    (*(volatile unsigned char*)0xDC01)
#define CIA1_TALO   (*(volatile unsigned char*)0xDC04)
#define CIA1_TAHI   (*(volatile unsigned char*)0xDC05)
#define CIA1_TODLO  (*(volatile unsigned char*)0xDC08)
#define CIA1_TODMID (*(volatile unsigned char*)0xDC09)
#define CIA1_TODHI  (*(volatile unsigned char*)0xDC0A)

uint32_t fingerprint_cia_timer(void) {
    // Read CIA timer at precise moment
    // Timing jitter varies per hardware due to crystal variance
    unsigned char lo, hi;
    
    // Disable interrupts for precise timing
    asm("sei");
    
    lo = CIA1_TALO;
    hi = CIA1_TAHI;
    
    // Small delay
    for (volatile int i = 0; i < 100; i++);
    
    unsigned char lo2 = CIA1_TALO;
    unsigned char hi2 = CIA1_TAHI;
    
    asm("cli");
    
    // Calculate timer delta (varies per hardware)
    uint16_t delta1 = (hi << 8) | lo;
    uint16_t delta2 = (hi2 << 8) | lo2;
    
    return (uint32_t)(delta2 - delta1);
}
```

### 3.2 VIC-II Raster Timing

```c
// Measure raster interrupt jitter
#define VIC_CTRL1   (*(volatile unsigned char*)0xD011)
#define VIC_RASTER  (*(volatile unsigned char*)0xD012)

uint32_t fingerprint_vic_raster(void) {
    unsigned char raster1, raster2, raster3;
    
    // Wait for specific raster line
    while (VIC_RASTER != 100);
    raster1 = VIC_RASTER;
    
    // Small delay
    for (volatile int i = 0; i < 50; i++);
    
    raster2 = VIC_RASTER;
    raster3 = VIC_RASTER;
    
    // Jitter in raster timing is hardware-specific
    return ((uint32_t)raster1 << 16) | ((uint32_t)raster2 << 8) | raster3;
}
```

### 3.3 SID Chip Fingerprint

```c
// SID registers
#define SID_POTX    (*(volatile unsigned char*)0xD419)
#define SID_POTY    (*(volatile unsigned char*)0xD41A)

uint32_t fingerprint_sid(void) {
    // SID register readback behavior varies
    // Some registers return different values on real hardware vs emulators
    unsigned char potx = SID_POTX;
    unsigned char poty = SID_POTY;
    
    return ((uint32_t)potx << 8) | poty;
}
```

### 3.4 ROM Checksum

```c
uint16_t fingerprint_rom_checksum(void) {
    // Calculate Kernal ROM checksum
    uint16_t sum = 0;
    
    // Kernal ROM is at 0xE000-0xFFFF
    // Temporarily swap in ROM if banked out
    unsigned char old_dd00 = (*(volatile unsigned char*)0xDD00);
    (*(volatile unsigned char*)0xDD00) = old_dd00 | 0x03;  // Enable ROM
    
    for (unsigned int addr = 0xE000; addr <= 0xFFFF; addr++) {
        sum += *(volatile unsigned char*)addr;
    }
    
    // Restore previous state
    (*(volatile unsigned char*)0xDD00) = old_dd00;
    
    return sum;
}
```

### 3.5 Combined Fingerprint

```c
typedef struct {
    char device_arch[16];
    char device_family[16];
    uint32_t cpu_speed;
    uint16_t total_ram_kb;
    uint32_t cia_timer_fp;
    uint32_t vic_raster_fp;
    uint32_t sid_fp;
    uint16_t rom_checksum;
} C64Fingerprint;

void build_fingerprint(C64Fingerprint* fp) {
    memset(fp, 0, sizeof(C64Fingerprint));
    
    strcpy(fp->device_arch, "c64_6510");
    strcpy(fp->device_family, "commodore_64");
    fp->cpu_speed = 1023000;  // 1.023 MHz
    fp->total_ram_kb = 64;
    
    fp->cia_timer_fp = fingerprint_cia_timer();
    fp->vic_raster_fp = fingerprint_vic_raster();
    fp->sid_fp = fingerprint_sid();
    fp->rom_checksum = fingerprint_rom_checksum();
}
```

---

## Phase 4: Miner Integration (Week 17-24)

### 4.1 JSON Builder

```c
// src/json.c - Minimal JSON builder
void json_build_attestation(char* buffer, int max_len, C64Fingerprint* fp, const char* wallet) {
    sprintf(buffer,
        "{"
        "\"device_arch\":\"%s\","
        "\"device_family\":\"%s\","
        "\"cpu_speed\":%lu,"
        "\"total_ram_kb\":%u,"
        "\"cia_timer_fp\":%lu,"
        "\"vic_raster_fp\":%lu,"
        "\"sid_fp\":%lu,"
        "\"rom_checksum\":%u,"
        "\"wallet\":\"%s\""
        "}",
        fp->device_arch,
        fp->device_family,
        fp->cpu_speed,
        fp->total_ram_kb,
        fp->cia_timer_fp,
        fp->vic_raster_fp,
        fp->sid_fp,
        fp->rom_checksum,
        wallet
    );
}
```

### 4.2 Attestation Flow

```c
// src/miner.c
#define ATTEST_ENDPOINT "/api/attest"
#define EPOCH_SECONDS 600  // 10 minutes

int perform_attestation(const char* wallet) {
    C64Fingerprint fp;
    char json_payload[512];
    char response[1024];
    
    // Build fingerprint
    build_fingerprint(&fp);
    
    // Build JSON payload
    json_build_attestation(json_payload, sizeof(json_payload), &fp, wallet);
    
    // Connect to server
    if (network_init() != 0) {
        return -1;
    }
    
    if (network_connect() != 0) {
        return -1;
    }
    
    // Send attestation
    if (http_post(ATTEST_ENDPOINT, json_payload, response, sizeof(response)) != 0) {
        network_close();
        return -1;
    }
    
    // Parse response (simplified)
    // Expected: {"success":true,"reward":0.0042,"epoch":123}
    
    network_close();
    return 0;
}

void miner_loop(const char* wallet) {
    while (1) {
        // Display status
        ui_show_status("ATTESTING...");
        
        // Perform attestation
        int result = perform_attestation(wallet);
        
        if (result == 0) {
            ui_show_status("SUCCESS");
        } else {
            ui_show_status("FAILED - RETRYING");
        }
        
        // Wait for next epoch (10 minutes)
        ui_countdown(EPOCH_SECONDS);
    }
}
```

---

## Phase 5: User Interface (Week 25-30)

### 5.1 Screen Layout

```c
// src/ui.c
void ui_init(void) {
    clrscr();
    bordercolor(COLOR_BLUE);
    bgcolor(COLOR_BLACK);
    textcolor(COLOR_WHITE);
}

void ui_show_status(const char* status) {
    gotoxy(2, 5);
    cprintf("STATUS: %s", status);
}

void ui_show_epoch_timer(unsigned int seconds) {
    unsigned int mins = seconds / 60;
    unsigned int secs = seconds % 60;
    
    gotoxy(2, 6);
    cprintf("EPOCH:  %02u:%02u REMAINING", mins, secs);
}

void ui_show_earned(float rtc) {
    gotoxy(2, 7);
    cprintf("EARNED: %.4f RTC", rtc);
}

void ui_show_hardware(void) {
    gotoxy(2, 9);
    cprintf("HARDWARE:");
    gotoxy(2, 10);
    cprintf("CPU: MOS 6510 @ 1.023 MHZ");
    gotoxy(2, 11);
    cprintf("RAM: 64 KB");
    gotoxy(2, 12);
    cprintf("NET: RR-NET CONNECTED");
}

void ui_show_menu(void) {
    gotoxy(2, 20);
    cprintf("[F1] PAUSE  [F3] MENU  [F5] QUIT");
}
```

### 5.2 Keyboard Input

```c
void ui_handle_input(void) {
    if (kbhit()) {
        char key = cgetc();
        
        switch (key) {
            case CH_F1:
                // Pause mining
                miner_paused = 1;
                break;
            case CH_F3:
                // Show menu
                ui_show_menu_screen();
                break;
            case CH_F5:
                // Quit
                exit(0);
                break;
        }
    }
}
```

---

## Phase 6: Testing & Documentation (Week 31-34)

### 6.1 Testing Checklist

- [ ] Build succeeds with cc65
- [ ] Runs in VICE emulator
- [ ] Network connection works (test server)
- [ ] Fingerprint collection works
- [ ] Attestation POST succeeds
- [ ] Response parsing works
- [ ] UI displays correctly
- [ ] Keyboard input responsive
- [ ] **Test on real C64 hardware** (CRITICAL)
- [ ] Anti-emulation detects VICE
- [ ] Photo/video proof captured
- [ ] Attestation visible on rustchain.org

### 6.2 Documentation

Create README.md with:
- Build instructions
- Hardware requirements
- Network setup guide
- Usage instructions
- Troubleshooting

### 6.3 Proof Collection

1. **Photo:** C64 running miner with timestamp
2. **Video:** 30+ second attestation cycle
3. **Screenshot:** rustchain.org/api/miners showing C64
4. **Hardware info:** CIA/VIC/SID fingerprint values
5. **Wallet address:** RTC4325af95d26d59c3ef025963656d22af638bb96b

---

## Memory Optimization

### Zero Page Usage (Critical!)

```asm
; asm/zeropage.s
.zeropage
    ptr1:       .word   ; General purpose pointer
    ptr2:       .word   ; Secondary pointer
    temp1:      .byte   ; Temporary storage
    temp2:      .byte   ; Temporary storage
    json_len:   .word   ; JSON buffer length
    sock_fd:    .byte   ; Socket file descriptor
.endzp
```

### ROM Banking

```c
// Enable RAM at ROM addresses
void bank_out_rom(void) {
    // DD00: Data Direction Register A for CIA2
    // Bits 0-1 control ROM banking
    // 0 = ROM visible, 1 = RAM visible
    
    (*(volatile unsigned char*)0xDD00) |= 0x03;  // Bank out ROMs
}

void bank_in_rom(void) {
    (*(volatile unsigned char*)0xDD00) &= ~0x03;  // Bank in ROMs
}
```

---

## Anti-Emulation

```c
int detect_emulator(void) {
    uint32_t cia_fp = fingerprint_cia_timer();
    uint32_t vic_fp = fingerprint_vic_raster();
    
    // Emulators often have perfect timing (no jitter)
    // Real hardware has analog variance
    
    // Check for VICE-specific behavior
    // VICE returns fixed values for some registers
    
    if (cia_fp == 0 || vic_fp == 0) {
        return 1;  // Likely emulator
    }
    
    // Additional checks can be added
    // e.g., SID register behavior, DRAM refresh timing
    
    return 0;  // Real hardware
}
```

---

## Build System

### Makefile

```makefile
CC = cl65
AS = ca65
LD = ld65

CFLAGS = -t c64 -O -Or -Oi
ASFLAGS = -t c64

SRCS_C = src/main.c src/miner.c src/network.c src/fingerprint.c src/ui.c src/json.c
SRCS_ASM = asm/startup.s asm/fingerprint.s

OBJS = $(SRCS_C:.c=.o) $(SRCS_ASM:.s=.o)

TARGET = miner.prg

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $<

%.o: %.s
	$(AS) $(ASFLAGS) $<

clean:
	del *.o
	del $(TARGET)

.PHONY: all clean
```

---

## Timeline Summary

| Phase | Duration | RTC Value |
|-------|----------|-----------|
| 1. Dev Environment | Week 1-2 | 20 RTC |
| 2. Network Stack | Week 3-10 | 50 RTC |
| 3. Fingerprinting | Week 11-16 | 50 RTC |
| 4. Miner Integration | Week 17-24 | 50 RTC |
| 5. UI | Week 25-30 | 20 RTC |
| 6. Testing/Docs | Week 31-34 | 10 RTC |
| **Total** | **34 weeks** | **150 RTC** |

---

## Budget

| Item | Cost (USD) |
|------|------------|
| RR-Net Ethernet | $80-150 |
| Commodore 64 | $50-200 (if not owned) |
| SD2IEC (optional) | $80-100 |
| **Total** | **$210-450** |

**Alternative (cheaper):**
| Item | Cost (USD) |
|------|------------|
| ESP32 dev board | $20 |
| Userport cable | $10-20 (or build) |
| Commodore 64 | $50-200 |
| **Total** | **$80-240** |

---

## Risk Mitigation

1. **SHA-256 too slow:** Server-side hashing, C64 provides fingerprint only
2. **RR-Net unavailable:** Use Userport + ESP32 bridge (cheaper, more work)
3. **C64 hardware unavailable:** Borrow from retro computing groups
4. **Memory too constrained:** Optimize with assembly, bank out ROMs
5. **Timing issues:** Use cycle-exact code, disable interrupts during critical sections

---

## Success Criteria

- [ ] Real C64 hardware successfully attests to RustChain
- [ ] Attestation visible on rustchain.org/api/miners
- [ ] Source code published on GitHub (MIT license)
- [ ] Build instructions documented
- [ ] Video proof submitted
- [ ] Bounty claimed to wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b

---

*Let's make the C64 mine cryptocurrency again!*
