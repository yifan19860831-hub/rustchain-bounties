# RustChain 386 Miner - Hardware Setup Guide

## Overview

This guide covers the hardware requirements and setup process for running the RustChain miner on Intel 386 architecture.

## Required Components

### Minimum Configuration

| Component | Specification | Notes |
|-----------|---------------|-------|
| CPU | Intel 386SX-16 or better | Any 386 variant works |
| RAM | 4 MB | Minimum for Slackware 3.0 |
| Storage | 64 MB | Floppy or CF-to-IDE |
| Network | NE2000 ISA Ethernet | Required for online mining |
| Video | VGA or better | For console display |

### Recommended Configuration

| Component | Specification | Notes |
|-----------|---------------|-------|
| CPU | Intel 386DX-40 | Best performance |
| RAM | 16 MB | Comfortable headroom |
| Storage | 128+ MB CF-to-IDE | Reliable, modern storage |
| Network | NE2000 ISA Ethernet | Widely compatible |
| Video | SVGA | Better display |

## Component Sourcing

### Where to Buy

1. **eBay**: Search "386 computer", "386 motherboard", "vintage PC"
   - Complete systems: $100-200
   - Motherboards only: $50-100
   
2. **Local Sources**:
   - Computer swap meets
   - Ham radio flea markets
   - Estate sales
   - Recycling centers (sometimes!)

3. **Online Forums**:
   - [VOGONS](https://www.vogons.org/)
   - [VCFed](https://www.vcfed.org/)
   - Reddit r/vintagecomputing

### Specific Parts to Look For

#### Motherboards

Good 386 motherboards:
- **Intel 386DX**: Reliable, well-documented
- **Acer 386**: Common, good support
- **Compaq 386**: Proprietary but robust
- **Any AT-form factor 386**: Standard, expandable

Avoid:
- Proprietary laptop motherboards (hard to expand)
- Damaged boards (capacitor leakage common)

#### RAM (30-pin SIMM)

- **Type**: 30-pin SIMM (not 72-pin!)
- **Speed**: 80ns or faster
- **Size**: 1MB, 2MB, 4MB modules
- **Parity**: Non-parity preferred (simpler)

Typical configuration:
- 4x 1MB = 4 MB (minimum)
- 4x 4MB = 16 MB (recommended)

#### Network Card

**NE2000 compatible** is the gold standard:
- Widely supported in Linux 2.0.x
- Cheap and common
- ISA bus (required for 386)

Part numbers to look for:
- Realtek RTL8019AS
- Winbond W89C940F
- Any "NE2000 compatible"

#### Storage: CF-to-IDE Adapter

Modern solution for reliable storage:
- **Adapter**: CF-to-IDE, 44-pin or 40-pin
- **CF Card**: 128MB or larger (industrial grade preferred)
- **Cost**: ~$15-20 total

Benefits:
- No moving parts (unlike old HDDs)
- Reliable
- Easy to transfer files from modern PC

#### Power Supply

- **Type**: AT power supply (not ATX!)
- **Wattage**: 200W minimum
- **Connectors**: AT motherboard connector (2x6 pins)

Note: ATX supplies require an adapter or modification.

## Assembly Instructions

### Step 1: Prepare Workspace

- Anti-static mat or bare concrete floor
- Phillips screwdriver
- Jumpers (for motherboard configuration)
- Thermal paste (if CPU has heatsink)

### Step 2: Install CPU

1. **Identify pin 1** on CPU and socket
2. **Insert CPU** gently (ZIF socket: lift lever, insert, lower lever)
3. **Apply thermal paste** if using heatsink
4. **Install heatsink/fan** if present (386s often passive)

### Step 3: Install RAM

1. **Match SIMM orientation** (notches align)
2. **Insert at 45° angle**, then push upright
3. **Repeat** for all modules
4. **Check jumper settings** for RAM size (some boards require)

### Step 4: Install Video Card

1. **Choose ISA slot** (any available)
2. **Insert firmly**
3. **Secure with screw**

### Step 5: Install Network Card

1. **Choose ISA slot** (avoid slot next to video if possible)
2. **Set IRQ and I/O** (usually IRQ 3, I/O 0x300)
3. **Insert and secure**

### Step 6: Install Storage

**For CF-to-IDE:**
1. **Connect IDE cable** to motherboard
2. **Connect CF adapter** (match pin 1!)
3. **Secure adapter** (standoffs or tape)
4. **Insert CF card**

**For floppy:**
1. **Mount drive** in bay
2. **Connect floppy cable** (twist in middle!)
3. **Connect power**

### Step 7: Connect Power

1. **AT connector**: Two 6-pin connectors (black wires together in middle)
2. **Drive power**: 4-pin Molex or floppy power
3. **Check polarity** before powering on!

### Step 8: Initial Boot

1. **Connect monitor** (VGA)
2. **Connect keyboard** (AT or PS/2 with adapter)
3. **Power on**
4. **Watch for POST** (Power-On Self Test)
5. **Enter BIOS setup** (usually Del or F2)

### Step 9: BIOS Configuration

Critical settings:
- **RAM size**: Auto-detect or manual
- **Hard disk**: Set geometry or "Auto"
- **Boot order**: C: first, then A:
- **Cache**: Enable if present
- **Wait states**: Auto or conservative

Save and exit.

## Troubleshooting

### No Power

- Check power supply switch (110V vs 220V!)
- Verify AT connectors (black wires together)
- Test PSU with paperclip method

### No Display

- Reseat video card
- Try different slot
- Check monitor connection
- Listen for beep codes

### RAM Not Detected

- Reseat SIMMs (ensure fully seated)
- Try one module at a time
- Check motherboard jumpers
- Clean SIMM contacts with eraser

### Boot Failures

- "Missing operating system": Install OS
- "Invalid boot disk": Check boot order
- Beep codes: Refer to motherboard manual

### Network Card Not Detected

- Check IRQ conflicts (video, NIC, sound)
- Verify I/O address (0x300 standard)
- Try different slot
- Update kernel drivers

## Performance Optimization

### CPU Speed

- **386DX-40**: Best performance (~40 MIPS)
- **386DX-33**: Good balance (~33 MIPS)
- **386SX-25**: Acceptable (~15 MIPS)

Higher clock = faster attestations, but also more power/heat.

### RAM Configuration

- **4 MB**: Minimum, tight
- **8 MB**: Comfortable
- **16 MB**: Plenty of headroom

More RAM = better caching, smoother operation.

### Storage Speed

- **CF card**: Fast, reliable
- **Old HDD**: Slow, unreliable, noisy
- **Floppy**: Very slow, use only for boot

CF card recommended for reliability.

## Power Consumption

Typical 386 system:
- **Motherboard + CPU**: 15-25W
- **RAM**: 2-5W
- **Video**: 5-10W
- **CF adapter**: <1W
- **Total**: ~30-50W

Much lower than modern systems!

## Environmental Considerations

### Temperature

- **Operating**: 10-35°C (50-95°F)
- **Storage**: -20-60°C (-4-140°F)

Older components tolerate heat poorly. Ensure ventilation.

### Humidity

- **Operating**: 20-80% non-condensing
- Avoid basements, attics

### Capacitor Leakage

Old electrolytic capacitors may leak:
- Look for bulging tops
- Brown crust around leads
- Replace if leaking (can damage board)

## Safety

### Electrical Safety

- **Unplug** before working inside
- **Discharge** static electricity
- **Don't work** on live circuits
- **Use proper** power cables

### Component Safety

- **Handle by edges** (don't touch chips)
- **Store in** anti-static bags
- **Don't force** connectors
- **Match pin 1** orientation

## Cost Summary

| Item | Low End | High End |
|------|---------|----------|
| 386 system (complete) | $100 | $200 |
| RAM upgrade (to 16MB) | $20 | $40 |
| NE2000 NIC | $15 | $25 |
| CF-to-IDE + 128MB CF | $15 | $20 |
| **Total** | **$150** | **$285** |

**Bounty**: 150 RTC (may cover entire cost!)
**Ongoing**: 4.0x multiplier provides passive income

## Next Steps

1. ✅ Acquire hardware
2. ✅ Assemble and test
3. ✅ Install Slackware 3.0
4. ✅ Configure network
5. ✅ Build and run miner

See [README.md](../README.md) for software setup.

---

**Questions?** Check [Troubleshooting](troubleshooting.md) or open an issue.
