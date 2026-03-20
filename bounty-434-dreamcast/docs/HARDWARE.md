# Hardware Requirements

This document describes the hardware requirements and recommendations for running the RustChain miner on Sega Dreamcast.

## Minimum Requirements

| Component | Specification | Notes |
|-----------|--------------|-------|
| **Console** | Sega Dreamcast (any revision) | VA0, VA1, VA2 all supported |
| **Network** | Broadband Adapter (BBA) | **Required** - modem too slow |
| **Storage** | VMU (128 KB) | Minimum for configuration |
| **Display** | Any Dreamcast-compatible display | TV, VGA, or capture card |
| **Controller** | Standard Dreamcast controller | For menu navigation |

## Recommended Setup

| Component | Specification | Notes |
|-----------|--------------|-------|
| **Console** | Sega Dreamcast (VA0 preferred) | Better video output |
| **Network** | Broadband Adapter + Ethernet | Stable connection |
| **Storage** | GDEMU SD Card Adapter | For persistent storage |
| **Display** | VGA Box + CRT/LCD | 640x480 progressive scan |
| **Controller** | Original Sega controller | Best compatibility |

## Broadband Adapter (BBA)

### Why Required?

The built-in 56k modem is **not practical** for mining:

| Connection | Speed | Latency | Viability |
|------------|-------|---------|-----------|
| 56k Modem | ~7 KB/s | High | ❌ Too slow |
| BBA (10 Mbps) | ~1 MB/s | Low | ✅ Viable |
| BBA (100 Mbps) | ~10 MB/s | Low | ✅ Best |

### BBA Models

| Model | Compatibility | Notes |
|-------|--------------|-------|
| **Sega BBA (HGD-001U)** | All Dreamcasts | Original, best compatibility |
| **Planetweb BBA** | All Dreamcasts | Third-party, rare |
| **PSU BBA** | Modified consoles | Requires mod |

### BBA Installation

1. Turn off Dreamcast
2. Open serial port cover
3. Insert BBA firmly
4. Connect Ethernet cable
5. Power on Dreamcast

## Storage Options

### VMU (Visual Memory Unit)

| Spec | Value |
|------|-------|
| Capacity | 128 KB (200 blocks) |
| Speed | Slow |
| Use | Configuration only |

**Pros:**
- Official Sega peripheral
- No modification required
- Portable saves

**Cons:**
- Very limited storage
- Slow read/write
- Battery-dependent

### SD Card Adapter (GDEMU/MODE)

| Spec | Value |
|------|-------|
| Capacity | Up to 32 GB |
| Speed | Medium |
| Use | Full storage solution |

**Pros:**
- Large storage capacity
- Fast loading
- Persistent storage

**Cons:**
- Requires purchase ($20-40)
- Installation may require mod

**Recommended Models:**
- GDEMU (official)
- MODE (modern alternative)
- Terraonion DC-SD

## Network Configuration

### Static IP (Recommended)

Configure your router to assign a static IP to the Dreamcast's MAC address.

### DHCP

The miner supports DHCP, but static IP is more reliable.

### Firewall Rules

Allow outbound connections to:
- TCP port 3333 (mining pool)
- TCP port 80/443 (if using HTTP pool)

## Power Considerations

| Component | Power Draw |
|-----------|-----------|
| Dreamcast | ~15W |
| BBA | ~2W |
| GDEMU | ~1W |
| **Total** | **~18W** |

**24-hour power consumption:** ~0.43 kWh

## Expected Performance

| Metric | Value |
|--------|-------|
| Hash Rate | ~100 H/s |
| Shares/day | ~8,640 (if difficulty = 1) |
| Power efficiency | ~5.5 H/W |

**Note:** This is **not profitable** - novelty/educational only!

## Troubleshooting

### BBA Not Detected

1. Check BBA is firmly seated
2. Try different Dreamcast (some revisions have issues)
3. Check BBA LED (should light when connected)

### Network Connection Fails

1. Verify Ethernet cable is working
2. Check router DHCP settings
3. Try static IP configuration
4. Test with another device on same cable

### Storage Issues

1. Format SD card as FAT32
2. Check GDEMU firmware is updated
3. Try different SD card brand

## Where to Buy

| Item | Source | Price |
|------|--------|-------|
| Dreamcast | eBay, local | $50-100 |
| BBA | eBay | $80-150 |
| GDEMU | dreamcast-mod.com | $25 |
| VMU | eBay, retail | $15-30 |

## Alternative: Emulator Testing

For development without hardware:

**Flycast Emulator**
- Supports BBA emulation
- Supports SD card emulation
- Free and fast iteration

**Download:** https://github.com/flyinghead/flycast

---

**Last Updated:** 2026-03-13
