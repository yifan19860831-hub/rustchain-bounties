# Palm OS Technical Reference

## Motorola DragonBall EZ Architecture

### CPU Specifications
```
Processor:    Motorola MC68328 (DragonBall EZ)
Architecture: Motorola 68000 (32-bit internal, 16-bit external bus)
Clock Speed:  16 MHz (some models 33 MHz)
Instructions: 68000 compatible + DragonBall extensions
Power:        ~0.1W typical (ultra low power!)
```

### Memory Map
```
0x00000000 - 0x000FFFFF: RAM (2 MB on Palm III)
0x00100000 - 0x001FFFFF: Expansion slot
0xFFF00000 - 0xFFFFFFFF: ROM (2 MB Flash)
```

### DragonBall Peripherals

#### RTC (Real-Time Clock)
```
Base: 0xFFFFF000
Registers:
  0x00 - Seconds
  0x01 - Minutes
  0x02 - Hours
  0x03 - Days
  0x04 - Months
  0x05 - Years
  0x06 - Control
  0x07 - Status
```

#### Timers
```
Timer 1: System tick (1 ms resolution)
Timer 2: User programmable
```

#### UART (Serial)
```
Used for HotSync cradle communication
Baud: 9600 - 115200
```

## Palm OS 3.5 API

### Application Structure
```c
UInt32 PilotMain(Int16 cmd, MemPtr cmdPBP, UInt16 launchFlags)
{
    // 1. Handle launch codes
    // 2. Initialize
    // 3. Event loop
    // 4. Cleanup
}
```

### Launch Codes
```
sysAppLaunchCmdNormalLaunch    = 0x0000
sysAppLaunchCmdFind            = 0x0004
sysAppLaunchCmdGoTo            = 0x0005
sysAppLaunchCmdSyncNotify      = 0x000B
sysAppLaunchCmdExgReceiveData  = 0x000D
```

### Event Loop
```c
EventType event;
Boolean done = false;

while (!done) {
    EvtGetEvent(&event, evtWaitForever);
    
    if (!AppHandleEvent(&event)) {
        SysHandleEvent(&event);
        MenuHandleEvent(NULL, &event, NULL);
    }
    
    if (event.eType == appStopEvent)
        done = true;
}
```

### Forms and UI
```c
// Create form
FormPtr form = FrmInitForm(MainFormID);
FrmSetActiveForm(form);
FrmDrawForm(form);

// Handle events
switch (event.eType) {
    case frmLoadEvent:
        // Load form
        break;
    case ctlSelectEvent:
        // Button pressed
        break;
}
```

### Memory Management
```c
// Allocate
MemPtr ptr = MemPtrNew(size);

// Free
MemPtrFree(ptr);

// Lock handle
MemPtr locked = MemHandleLock(handle);

// Unlock
MemHandleUnlock(handle);
```

### Database Storage
```c
// Open database
DmOpenRef db = DmOpenDatabase(dbNum, mode);

// Create record
UInt16 index = DmNumRecords(db);
MemHandle record = DmNewRecord(db, &index, size);

// Write data
void* data = MemHandleLock(record);
// ... write ...
MemHandleUnlock(record);
DmReleaseRecord(db, index, true);

// Close
DmCloseDatabase(db);
```

### Entropy Sources on Palm III

#### 1. RTC Jitter
```c
TimeType now = TimGetSeconds();
UInt8 entropy = now & 0xFF;
```

#### 2. Touchscreen Timing
```c
// User tap timing varies based on human factors
EventType event;
EvtGetEvent(&event, evtWaitForever);
// event.timestamp provides entropy
```

#### 3. RAM Power-On State
```c
// Uninitialized RAM contains random patterns
// (Only available on cold boot)
```

#### 4. Timer Tick Jitter
```c
UInt32 ticks = SysTicksPerSecond();
// Low bits vary due to interrupt timing
```

### Power Management
```c
// Set auto-off timer
SysSetAutoOffTime(300);  // 5 minutes

// Sleep
SysTaskSleep(ticks);

// Wake on event (automatic)
```

### Display Specifications
```
Resolution:  160 × 160 pixels
Colors:      4-level grayscale
Backlight:   Electroluminescent
Touch:       Resistive touchscreen
```

### Storage Limits
```
Application: 64 KB max (single segment)
Resources:   64 KB max
Database:    Limited by available RAM (~1.5 MB free)
Heap:        Dynamic (shared with other apps)
```

## Building for Palm OS

### Resource Compiler (PilRC)
```
resource 'tAIB' 1000 {
    "RtMn",              // Creator ID
    "RC Miner",          // App name
    0x00000001,          // Version
    0x00003000,          // Palm OS 3.0+
    0x0000,              // Flags
    0                    // Features
};
```

### PRC File Format
```
Header (78 bytes)
  - Name (32 bytes)
  - Attributes
  - Version
  - Creation date
  - Modification date
  - Backup date
  - Modification number
  - App info ID
  - Sort info ID
  - Type (4 bytes)
  - Creator (4 bytes)
  - Unique ID seed
  - Next record list ID

Records
  - Record 0: Code
  - Record 1+: Resources
```

## Debugging

### POSE Emulator
```
1. Download POSE from PalmSource archives
2. Load Palm III ROM image
3. Enable memory debugging
4. Install PRC via drag-drop
5. Use breakpoints and watchpoints
```

### Gremlins (Automated Testing)
```
// Record user actions
// Replay for testing
// Catch crashes and memory leaks
```

### Logging
```c
#ifdef DEBUG
    Char buffer[64];
    StrPrintF(buffer, "Value: %ld", value);
    FrmAlert(AlertCustomBase);  // Show in dialog
#endif
```

## Optimization Tips

### Size Optimization
```
- Use -Os flag
- Avoid printf (use StrPrintF)
- Share common strings
- Use overlays for large features
```

### Speed Optimization
```
- Cache frequently accessed data
- Use assembly for hot loops
- Minimize memory allocations
- Batch database operations
```

### Power Optimization
```
- Sleep between operations
- Reduce display updates
- Use hardware timers (not busy-wait)
- Disable backlight when not needed
```

## References

- Palm OS SDK Documentation
- Motorola DragonBall EZ Data Sheet
- "Palm OS Programming" by Dan Parks Sydow
- PalmSource Developer Archives

---

**For RustChain Miner Implementation**

Key considerations:
1. Minimal memory footprint (< 500 KB)
2. Event-driven (no busy loops)
3. Power-efficient (battery powered!)
4. Robust storage (Palm DB format)
5. Simple UI (160×160 display)

Wallet: `RTC4325af95d26d59c3ef025963656d22af638bb96b`
