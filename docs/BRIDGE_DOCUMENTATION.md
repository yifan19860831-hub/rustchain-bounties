# RustChain Bridge Documentation

> **Complete guide to the RustChain cross-chain bridge ecosystem**
> 
> This documentation covers the wRTC bridge mechanism, technical architecture, and usage instructions for bridging between RustChain and other blockchain networks.

---

## 📋 Table of Contents

- [Overview](#overview)
- [What is wRTC?](#what-is-wrtc)
- [Bridge Architecture](#bridge-architecture)
- [Technical Mechanism](#technical-mechanism)
- [Supported Bridges](#supported-bridges)
- [User Guide](#user-guide)
- [API Reference](#api-reference)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)

---

## Overview

RustChain implements a cross-chain bridge system that enables seamless token transfers between the RustChain network and other blockchain ecosystems. The primary bridge connects RustChain (RTC) with Solana (wRTC), with additional bridges planned for Base, Ethereum, and Ergo.

### Key Features

- **1:1 Peg**: wRTC maintains a 1:1 value ratio with native RTC
- **Trust-Minimized**: Bridge operations are verifiable on-chain
- **Fast Settlement**: Solana transactions finalize in ~400ms
- **Low Fees**: Bridge fees typically 0.1-0.5%
- **Bi-Directional**: Bridge in both directions (RTC ↔ wRTC)

### Bridge Statistics

| Metric | Value |
|--------|-------|
| Token Mint (Solana) | `12TAdKXxcGf6oCv4rqDz2NkgxjyHq6HQKoxKZYGf5i4X` |
| Decimals | 6 |
| Total Bridged (circulating) | Variable |
| Bridge UI | https://bottube.ai/bridge/wrtc |
| Average Bridge Time | 5-30 minutes |

---

## What is wRTC?

**wRTC (Wrapped RustChain Token)** is the Solana-native representation of RustChain Token (RTC).

### RTC vs wRTC Comparison

| Feature | RTC (Native) | wRTC (Wrapped) |
|---------|--------------|----------------|
| **Network** | RustChain | Solana |
| **Primary Use** | Mining rewards, governance | Trading, DeFi |
| **Wallet Type** | RustChain wallet | Solana wallet (Phantom, Solflare) |
| **Transaction Speed** | ~10 min epochs | ~400ms finality |
| **Transaction Cost** | Network fees | ~0.000005 SOL |
| **DEX Availability** | Bridge only | Raydium, Jupiter, etc. |
| **Token Standard** | RustChain native | SPL Token |

### Why Use wRTC?

1. **Trade on DEXs**: Swap wRTC for SOL, USDC, or other Solana tokens
2. **Liquidity Provision**: Provide liquidity on Raydium to earn fees
3. **Fast Transfers**: Near-instant transfers on Solana network
4. **DeFi Integration**: Use with any Solana DeFi protocol
5. **Price Discovery**: Market-driven price discovery on open markets

---

## Bridge Architecture

### High-Level Architecture

```
┌─────────────────┐                    ┌─────────────────┐
│   RustChain     │                    │     Solana      │
│     Network     │                    │     Network     │
│                 │                    │                 │
│  ┌───────────┐  │                    │  ┌───────────┐  │
│  │   RTC     │  │                    │  │   wRTC    │  │
│  │  Token    │  │                    │  │   (SPL)   │  │
│  └─────┬─────┘  │                    │  └─────▲─────┘  │
│        │        │                    │        │        │
│  ┌─────▼─────┐  │                    │  ┌─────┴─────┐  │
│  │  Bridge   │  │   Lock & Mint    │  │   Bridge    │  │
│  │  Escrow   │──┼───────────────────▶│  │   Vault   │  │
│  │  Contract │  │   Burn & Unlock  │  │  Contract   │  │
│  └─────▲─────┘  │◀───────────────────┴  └───────────┘  │
│        │        │                    │                 │
└────────┴────────┘                    └─────────────────┘
         │
         ▼
┌─────────────────────────┐
│   BoTTube Bridge UI     │
│  https://bottube.ai     │
└─────────────────────────┘
```

### Components

1. **RustChain Escrow Contract**: Holds RTC tokens during bridge operations
2. **Solana Vault Contract**: Manages wRTC minting/burning
3. **Bridge Relayer**: Monitors both chains and processes bridge transactions
4. **Bridge UI**: User interface for initiating bridge operations
5. **Oracle/Validator**: Verifies cross-chain transactions (future enhancement)

---

## Technical Mechanism

### RTC → wRTC (Wrapping/Bridging to Solana)

**Step-by-Step Process:**

1. **User Initiation**
   - User connects RustChain wallet to bridge UI
   - Enters amount of RTC to bridge
   - Provides destination Solana wallet address

2. **Lock on RustChain**
   - Bridge contract creates escrow job via `POST /agent/jobs`
   - RTC tokens locked in bridge escrow address
   - Transaction confirmed on RustChain (~1-5 minutes)

3. **Verification**
   - Bridge relayer detects lock transaction
   - Validates transaction confirmations
   - Verifies source wallet and amount

4. **Mint on Solana**
   - Bridge contract mints equivalent wRTC on Solana
   - wRTC sent to destination Solana wallet
   - Transaction finalizes (~5-15 seconds)

5. **Completion**
   - Bridge UI updates status to "Completed"
   - User receives wRTC in Solana wallet
   - Transaction hash provided for verification

**API Flow:**
```
POST /agent/jobs
{
  "type": "bridge_escrow",
  "amount": 100,
  "destination": "7nx8QmzxD1wKX7QJ1FVqT5hX9YvJxKqZb8yPoR3dL8mN",
  "destination_chain": "solana"
}

→ Returns: { "job_id": "abc123", "escrow_address": "RTC...", "status": "pending" }
```

### wRTC → RTC (Unwrapping/Bridging to RustChain)

**Step-by-Step Process:**

1. **User Initiation**
   - User connects Solana wallet to bridge UI
   - Enters amount of wRTC to bridge
   - Provides destination RustChain wallet address

2. **Burn on Solana**
   - User approves wRTC burn transaction
   - wRTC tokens burned (removed from circulation)
   - Transaction finalizes on Solana (~5-15 seconds)

3. **Verification**
   - Bridge relayer detects burn transaction
   - Validates transaction on Solana
   - Confirms burn amount and source wallet

4. **Release on RustChain**
   - Bridge contract releases equivalent RTC from escrow
   - RTC sent to destination RustChain wallet
   - Transaction confirms on RustChain (~5-30 minutes)

5. **Completion**
   - Bridge UI updates status to "Completed"
   - User receives RTC in RustChain wallet
   - Transaction hash provided for verification

**API Flow:**
```
POST /wallet/transfer/signed
{
  "from": "bridge_wallet",
  "to": "user_rustchain_wallet",
  "amount": 100,
  "bridge_reference": "solana_tx_hash"
}

→ Returns: { "tx_hash": "RTC...", "status": "pending" }
```

---

## Supported Bridges

### Active Bridges

| Bridge Pair | Status | Fee | Time | UI |
|-------------|--------|-----|------|-----|
| RTC ↔ wRTC (Solana) | ✅ Live | 0.1-0.5% | 5-30 min | [bottube.ai/bridge/wrtc](https://bottube.ai/bridge/wrtc) |

### Planned Bridges

| Bridge Pair | Status | Target | Notes |
|-------------|--------|--------|-------|
| RTC ↔ wRTC (Base) | 🔄 In Development | Q2 2026 | Coinbase Base L2 |
| RTC ↔ ERG (Ergo) | 🔧 Testing | Q2 2026 | Native Ergo chain integration |
| RTC ↔ ETH (Ethereum) | 📋 Planned | Q3 2026 | Ethereum mainnet |
| RTC ↔ USDC | 📋 Planned | Q3 2026 | Stablecoin pair |

---

## User Guide

### Prerequisites

Before using the bridge, ensure you have:

- [ ] **RustChain wallet** with RTC balance (for RTC → wRTC)
- [ ] **Solana wallet** (Phantom, Solflare, or Backpack)
- [ ] **SOL for fees** (~0.001 SOL recommended)
- [ ] **Both wallets accessible** and backed up

### Step-by-Step: Bridge RTC to wRTC

1. **Navigate to Bridge**
   ```
   https://bottube.ai/bridge/wrtc
   ```
   ⚠️ **Always verify the URL** - bookmark to avoid phishing

2. **Select Direction**
   - Choose "RTC → wRTC"

3. **Connect RustChain Wallet**
   - Click "Connect RustChain Wallet"
   - Enter wallet address or connect via available method
   - Verify RTC balance displays

4. **Enter Destination**
   - Input your Solana wallet address
   - **Double-check address format** (base58, 32-44 characters)
   - Valid example: `7nx8QmzxD1wKX7QJ1FVqT5hX9YvJxKqZb8yPoR3dL8mN`

5. **Enter Amount**
   - Input amount of RTC to bridge
   - Review bridge fee (displayed in UI)
   - Ensure sufficient balance (amount + fees)

6. **Review & Confirm**
   - ✅ Source wallet has sufficient RTC
   - ✅ Destination Solana address is correct
   - ✅ Amount and fees are acceptable
   - ✅ Understand timing (5-30 minutes)
   
   Click "Bridge"

7. **Wait for Confirmation**
   - Monitor bridge UI for status updates
   - Status flow: "Pending" → "Confirming" → "Completed"

8. **Verify Receipt**
   - Check Solana wallet for wRTC balance
   - View transaction on [Solscan](https://solscan.io)
   - Token should appear automatically (or manually add mint address)

### Step-by-Step: Bridge wRTC to RTC

1. **Navigate to Bridge**
   ```
   https://bottube.ai/bridge/wrtc
   ```

2. **Select Direction**
   - Choose "wRTC → RTC"

3. **Connect Solana Wallet**
   - Click "Connect Solana Wallet"
   - Select wallet provider (Phantom, Solflare, etc.)
   - Approve connection

4. **Enter Destination**
   - Input your RustChain wallet address
   - **Double-check address** (case-sensitive, alphanumeric)

5. **Enter Amount**
   - Input amount of wRTC to bridge
   - Review bridge fee
   - Click "Max" to bridge entire balance (optional)

6. **Review & Confirm**
   - ✅ Source wRTC balance is sufficient
   - ✅ Destination RustChain address is correct
   - ✅ Amount and fees are acceptable
   - ✅ Have SOL for transaction fees
   
   Click "Bridge"

7. **Approve Solana Transaction**
   - Wallet prompts for approval
   - Review transaction details
   - Click "Approve" or "Sign"

8. **Wait for Confirmation**
   - Burn on Solana: ~5-15 seconds
   - Release on RustChain: ~5-30 minutes

9. **Verify Receipt**
   ```bash
   curl -sk "https://rustchain.org/wallet/balance?miner_id=YOUR_WALLET"
   ```
   - Check RustChain wallet balance
   - Verify on [RustChain Explorer](https://rustchain.org/explorer)

---

## API Reference

### Bridge Endpoints

#### Create Bridge Job (RTC → wRTC)

```http
POST /agent/jobs
Content-Type: application/json

{
  "type": "bridge_escrow",
  "amount": 100,
  "destination_chain": "solana",
  "destination_address": "7nx8QmzxD1wKX7QJ1FVqT5hX9YvJxKqZb8yPoR3dL8mN",
  "metadata": {
    "bridge_type": "rtc_to_wrtc",
    "user_id": "optional_user_identifier"
  }
}
```

**Response:**
```json
{
  "job_id": "bridge_abc123",
  "escrow_address": "RTC_Escrow_Address",
  "status": "pending_lock",
  "estimated_time": "5-30 minutes",
  "fee_percentage": 0.1
}
```

#### Verify Bridge Transaction

```http
GET /bridge/status/{job_id}
```

**Response:**
```json
{
  "job_id": "bridge_abc123",
  "status": "completed",
  "source_tx": "RTC_Tx_Hash",
  "destination_tx": "Solana_Tx_Hash",
  "amount": 100,
  "fee": 0.1,
  "completed_at": "2026-03-12T10:30:00Z"
}
```

#### Get Bridge Fee Quote

```http
GET /bridge/quote?amount=100&direction=rtc_to_wrtc
```

**Response:**
```json
{
  "amount": 100,
  "direction": "rtc_to_wrtc",
  "fee_percentage": 0.1,
  "fee_amount": 0.1,
  "receive_amount": 99.9,
  "estimated_time": "5-30 minutes"
}
```

### RustChain Native Endpoints

#### Check Wallet Balance

```http
GET /wallet/balance?miner_id=WALLET_NAME
```

#### Transfer Signed Transaction

```http
POST /wallet/transfer/signed
Content-Type: application/json

{
  "from": "source_wallet",
  "to": "destination_wallet",
  "amount": 100,
  "signature": "ed25519_signature_hex",
  "public_key": "ed25519_public_key_hex"
}
```

---

## Security Considerations

### Anti-Scam Checklist

**Before EVERY transaction, verify:**

| Check | Canonical Value | How to Verify |
|-------|-----------------|---------------|
| **Token Mint** | `12TAdKXxcGf6oCv4rqDz2NkgxjyHq6HQKoxKZYGf5i4X` | Must match exactly - 44 characters, base58 |
| **Decimals** | `6` | wRTC uses 6 decimal places |
| **Official Bridge** | `https://bottube.ai/bridge/wrtc` | Bookmark this URL |
| **Official Swap** | `https://raydium.io/swap/?inputMint=sol&outputMint=12TAdKXxcGf6oCv4rqDz2NkgxjyHq6HQKoxKZYGf5i4X` | Verify mint in URL |

### 🚨 Red Flags - STOP if you see these:

- [ ] Token mint address doesn't match exactly
- [ ] Website URL is slightly different (typosquatting)
- [ ] Someone DM'd you a "better" bridge link
- [ ] Token shows different decimal places (e.g., 9 or 18)
- [ ] Price seems too good to be true (likely honeypot)

### Security Best Practices

1. **Never share seed phrases or private keys**
2. **Always verify mint addresses character-by-character**
3. **Bookmark official URLs** - never click links from DMs
4. **Start with small amounts** when testing
5. **Keep software updated** - wallet apps, browsers
6. **Use hardware wallets** for large amounts
7. **Enable 2FA** where available
8. **Verify transactions** on block explorers

### Bridge Security Model

- **Escrow-Based**: RTC tokens held in secure escrow during bridge
- **1:1 Backing**: Every wRTC is backed by 1 RTC in escrow
- **Transparent**: All transactions verifiable on-chain
- **Auditable**: Complete transaction history maintained
- **Rate Limited**: Protection against abuse and attacks

---

## Troubleshooting

### Common Issues

#### Issue: "Insufficient SOL for transaction fees"

**Solution:**
- Ensure Solana wallet has at least 0.001 SOL
- Buy SOL on any exchange and transfer to wallet
- Even 0.01 SOL is sufficient for many transactions

#### Issue: "Token mint not found" or wrong token showing

**Solution:**
1. Verify correct mint: `12TAdKXxcGf6oCv4rqDz2NkgxjyHq6HQKoxKZYGf5i4X`
2. Clear wallet's token cache (settings → clear cache)
3. Manually add token using mint address

#### Issue: Bridge transaction stuck on "Pending"

**Solution:**
1. Wait up to 1 hour (network congestion)
2. Check [Solscan](https://solscan.io) for Solana transaction status
3. Check RustChain explorer for corresponding transaction
4. Contact support with transaction hash if >1 hour

#### Issue: "Slippage tolerance exceeded" on Raydium

**Solution:**
1. Increase slippage tolerance (gear icon) to 1-2%
2. Try swapping smaller amount
3. Wait and retry (price may be volatile)
4. Check DexScreener for current pool liquidity

#### Issue: Bridge shows "Failed" or "Rejected"

**Solution:**
1. Verify sufficient balance for amount + fees
2. Check both wallet addresses are correct
3. Ensure correct network (Mainnet Beta for Solana)
4. Clear browser cache and try again
5. Try smaller amount first

#### Issue: wRTC not appearing in wallet

**Solution:**
- **Phantom**: Settings → Preferences → Manage token list → Search "wRTC"
- **Solflare**: Portfolio → Click "+" → Paste mint address → Add
- **Backpack**: Tokens → Search or paste mint

#### Issue: "Invalid address format" when bridging

**Solution:**
- RustChain addresses: Alphanumeric, case-sensitive
- Solana addresses: 32-44 characters, base58 encoded
- Never use Ethereum (0x...) addresses for Solana

### Emergency Contacts

| Issue | Contact |
|-------|---------|
| Bridge problems | BoTTube support on [bottube.ai](https://bottube.ai) |
| RustChain issues | GitHub Issues: [Scottcjn/Rustchain](https://github.com/Scottcjn/Rustchain) |
| Scam reports | Report to official RustChain Discord/Telegram mods |

---

## FAQ

### General Questions

**Q: What is the difference between RTC and wRTC?**

A: RTC is the native RustChain token used for mining rewards and on-chain operations. wRTC is the wrapped version on Solana, enabling fast trading and DeFi integration. They maintain a 1:1 value ratio and can be bridged bi-directionally.

**Q: How long does bridging take?**

A: 
- RTC → wRTC: 5-30 minutes (depends on RustChain confirmation)
- wRTC → RTC: 5-30 minutes (Solana burn is fast, RustChain release takes longer)

**Q: What are the bridge fees?**

A: Bridge fees typically range from 0.1% to 0.5%, depending on network conditions and bridge direction. Fees are displayed before confirmation.

**Q: Is there a minimum/maximum bridge amount?**

A: 
- Minimum: Usually 1 RTC (to cover fees)
- Maximum: No hard limit, subject to bridge liquidity

**Q: Can I bridge to someone else's wallet?**

A: Yes, you can specify any valid destination wallet address. However, always verify the address is correct - transactions are irreversible.

### Technical Questions

**Q: How is the 1:1 peg maintained?**

A: Every wRTC token is backed 1:1 by RTC held in bridge escrow. The mint/burn mechanism ensures supply parity.

**Q: What happens if the bridge goes down?**

A: Bridge operations may be temporarily paused, but funds are never at risk. RTC remains in escrow and can be claimed once the bridge resumes.

**Q: Can I reverse a bridge transaction?**

A: No, blockchain transactions are irreversible. Always verify addresses and amounts before confirming.

**Q: Is the bridge audited?**

A: Bridge security is maintained through transparent on-chain operations and community oversight. Formal audits are planned for future bridge versions.

### Trading Questions

**Q: Where can I trade wRTC?**

A: wRTC is available on:
- [Raydium](https://raydium.io)
- [Jupiter Aggregator](https://jup.ag)
- More DEXs coming soon

**Q: How do I check the wRTC price?**

A: Check price on:
- [DexScreener](https://dexscreener.com/solana/8CF2Q8nSCxRacDShbtF86XTSrYjueBMKmfdR3MLdnYzb)
- [Jupiter](https://jup.ag)
- [Raydium](https://raydium.io)

**Q: Can I provide liquidity for wRTC?**

A: Yes! You can provide wRTC liquidity on Raydium to earn trading fees. Visit the Raydium liquidity pool for details.

---

## Quick Reference

### Token Details

| Property | Value |
|----------|-------|
| **Token Name** | Wrapped RustChain Token |
| **Symbol** | wRTC |
| **Mint Address** | `12TAdKXxcGf6oCv4rqDz2NkgxjyHq6HQKoxKZYGf5i4X` |
| **Decimals** | 6 |
| **Network** | Solana |
| **Token Standard** | SPL Token |

### Official Links

| Resource | URL |
|----------|-----|
| **BoTTube Bridge** | https://bottube.ai/bridge/wrtc |
| **Raydium Swap (SOL→wRTC)** | https://raydium.io/swap/?inputMint=sol&outputMint=12TAdKXxcGf6oCv4rqDz2NkgxjyHq6HQKoxKZYGf5i4X |
| **DexScreener** | https://dexscreener.com/solana/8CF2Q8nSCxRacDShbtF86XTSrYjueBMKmfdR3MLdnYzb |
| **RustChain Explorer** | https://rustchain.org/explorer |
| **Solscan (Solana Explorer)** | https://solscan.io |

### Bridge Fees & Times

| Direction | Typical Fee | Estimated Time |
|-----------|-------------|----------------|
| RTC → wRTC | 0.1-0.5% | 5-30 min |
| wRTC → RTC | 0.1-0.5% | 5-30 min |

### Transaction Costs

| Operation | Network Fee |
|-----------|-------------|
| Raydium Swap | ~0.001 SOL |
| Bridge (wRTC→RTC) | ~0.0001 SOL |
| Transfer wRTC | ~0.000005 SOL |

---

## Additional Resources

- [wRTC Quickstart Guide](../docs/wrtc.md)
- [wRTC Onboarding Tutorial](../docs/WRTC_ONBOARDING_TUTORIAL.md)
- [RustChain Whitepaper](https://github.com/Scottcjn/Rustchain/blob/main/docs/RustChain_Whitepaper.pdf)
- [Protocol Specification](./PROTOCOL.md)
- [API Reference](./API_REFERENCE.md)
- [Wallet User Guide](./WALLET_USER_GUIDE.md)

---

<div align="center">

**Questions?** Open an issue on [GitHub](https://github.com/Scottcjn/Rustchain) or reach out in official community channels.

*Always verify, never rush. Your security is worth the extra 30 seconds.*

**Version:** 1.0.0  
**Last Updated:** 2026-03-12  
**Maintained by:** RustChain Core Team

</div>
