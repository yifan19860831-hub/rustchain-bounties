# RustChain Bridge Documentation

> **Complete guide to the RustChain cross-chain bridge ecosystem**

---

## Overview

RustChain implements a cross-chain bridge system enabling seamless token transfers between RustChain and other blockchain ecosystems. The primary bridge connects RustChain (RTC) with Solana (wRTC).

### Key Features

- **1:1 Peg**: wRTC maintains 1:1 value ratio with native RTC
- **Trust-Minimized**: Bridge operations verifiable on-chain
- **Fast Settlement**: Solana transactions finalize in ~400ms
- **Low Fees**: Bridge fees typically 0.1-0.5%
- **Bi-Directional**: Bridge both directions (RTC ↔ wRTC)

---

## What is wRTC?

**wRTC (Wrapped RustChain Token)** is the Solana-native representation of RTC.

| Feature | RTC (Native) | wRTC (Wrapped) |
|---------|--------------|----------------|
| **Network** | RustChain | Solana |
| **Use** | Mining, governance | Trading, DeFi |
| **Speed** | ~10 min epochs | ~400ms finality |
| **DEX** | Bridge only | Raydium, Jupiter |

---

## Bridge Architecture

```
┌─────────────────┐         Lock & Mint        ┌─────────────────┐
│   RustChain     │───────────────────────────▶│     Solana      │
│     RTC         │                            │     wRTC        │
│                 │◀───────────────────────────│                 │
│  ┌───────────┐  │         Burn & Unlock      │  ┌───────────┐  │
│  │  Escrow   │  │                            │  │   Vault   │  │
│  └───────────┘  │                            │  └───────────┘  │
└─────────────────┘                            └─────────────────┘
         │                                              │
         └─────────────── BoTTube Bridge ───────────────┘
                   https://bottube.ai/bridge/wrtc
```

---

## Technical Mechanism

### RTC → wRTC (Wrapping)

1. **User initiates** bridge via UI
2. **Lock RTC** in RustChain escrow via `POST /agent/jobs`
3. **Verify** transaction confirmations
4. **Mint wRTC** on Solana to destination wallet
5. **Complete** - user receives wRTC (~5-30 min total)

**API Example:**
```json
POST /agent/jobs
{
  "type": "bridge_escrow",
  "amount": 100,
  "destination_chain": "solana",
  "destination_address": "7nx8QmzxD1wKX7QJ1FVqT5hX9YvJxKqZb8yPoR3dL8mN"
}
```

### wRTC → RTC (Unwrapping)

1. **User initiates** bridge via UI
2. **Burn wRTC** on Solana
3. **Verify** burn transaction
4. **Release RTC** from escrow to RustChain wallet
5. **Complete** - user receives RTC (~5-30 min total)

---

## User Guide

### Prerequisites

- RustChain wallet (for RTC → wRTC)
- Solana wallet (Phantom, Solflare)
- SOL for fees (~0.001 SOL)

### Bridge RTC to wRTC

1. Navigate to https://bottube.ai/bridge/wrtc
2. Select "RTC → wRTC"
3. Connect RustChain wallet
4. Enter Solana destination address
5. Enter amount and review fees
6. Confirm bridge transaction
7. Wait for confirmation (5-30 min)
8. Verify wRTC in Solana wallet

### Bridge wRTC to RTC

1. Navigate to https://bottube.ai/bridge/wrtc
2. Select "wRTC → RTC"
3. Connect Solana wallet
4. Enter RustChain destination address
5. Enter amount and approve burn
6. Wait for confirmation (5-30 min)
7. Verify RTC in RustChain wallet

---

## API Reference

### Bridge Endpoints

**Create Bridge Job:**
```http
POST /agent/jobs
Content-Type: application/json

{
  "type": "bridge_escrow",
  "amount": 100,
  "destination_chain": "solana",
  "destination_address": "SOLANA_ADDRESS"
}
```

**Response:**
```json
{
  "job_id": "bridge_abc123",
  "status": "pending_lock",
  "estimated_time": "5-30 minutes",
  "fee_percentage": 0.1
}
```

**Check Status:**
```http
GET /bridge/status/{job_id}
```

**Get Quote:**
```http
GET /bridge/quote?amount=100&direction=rtc_to_wrtc
```

---

## Security

### Verify Before Every Transaction

| Check | Value |
|-------|-------|
| **Token Mint** | `12TAdKXxcGf6oCv4rqDz2NkgxjyHq6HQKoxKZYGf5i4X` |
| **Decimals** | 6 |
| **Bridge URL** | `https://bottube.ai/bridge/wrtc` |

### 🚨 Red Flags

- Token mint doesn't match exactly
- Website URL slightly different (typosquatting)
- DM'd "better" bridge links
- Different decimal places
- Price too good to be true

### Best Practices

1. Never share seed phrases
2. Verify mint addresses character-by-character
3. Bookmark official URLs
4. Start with small amounts
5. Verify transactions on explorers

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Insufficient SOL | Ensure wallet has 0.001+ SOL |
| Token not found | Verify mint: `12TAdKXxcGf6oCv4rqDz2NkgxjyHq6HQKoxKZYGf5i4X` |
| Transaction pending | Wait up to 1 hour, check Solscan |
| Slippage exceeded | Increase to 1-2% on Raydium |
| Bridge failed | Verify addresses, clear cache, retry |
| wRTC not showing | Manually add token in wallet |

---

## FAQ

**Q: How long does bridging take?**
A: 5-30 minutes depending on network conditions.

**Q: What are the fees?**
A: Typically 0.1-0.5%, displayed before confirmation.

**Q: Where can I trade wRTC?**
A: Raydium, Jupiter, and other Solana DEXs.

**Q: How is the 1:1 peg maintained?**
A: Every wRTC is backed 1:1 by RTC in bridge escrow.

---

## Quick Reference

### Token Details

| Property | Value |
|----------|-------|
| **Mint** | `12TAdKXxcGf6oCv4rqDz2NkgxjyHq6HQKoxKZYGf5i4X` |
| **Decimals** | 6 |
| **Network** | Solana |

### Links

| Resource | URL |
|----------|-----|
| Bridge | https://bottube.ai/bridge/wrtc |
| Raydium | https://raydium.io/swap/?inputMint=sol&outputMint=12TAdKXxcGf6oCv4rqDz2NkgxjyHq6HQKoxKZYGf5i4X |
| DexScreener | https://dexscreener.com/solana/8CF2Q8nSCxRacDShbtF86XTSrYjueBMKmfdR3MLdnYzb |
| Explorer | https://rustchain.org/explorer |

---

<div align="center">

**Version:** 1.0.0 | **Updated:** 2026-03-12

Questions? Open an issue on GitHub or reach out in community channels.

*Always verify, never rush. Your security is worth the extra 30 seconds.*

</div>
