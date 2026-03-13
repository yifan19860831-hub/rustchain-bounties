# wRTC Onboarding Tutorial — Bridge + Swap Safety Guide

## Quick Start

This guide explains what RTC vs wRTC means and how to bridge/swap safely.

## What is RTC vs wRTC?

| Token | Chain | Purpose |
|-------|-------|---------|
| **RTC** | RustChain (native) | Mining rewards, governance, attestation |
| **wRTC** | Solana (wrapped) | Trading, liquidity, DeFi integration |

**wRTC** is a wrapped representation of RTC on Solana. Use wRTC for Solana-native trading and liquidity tools like Raydium.

## Official Links

### Token Mint (Solana)
```
12TAdKXxcGf6oCv4rqDz2NkgxjyHq6HQKoxKZYGf5i4X
```

### Bridge & Swap
| Resource | Link |
|----------|------|
| Bridge UI | [bottube.ai/bridge](https://bottube.ai/bridge) |
| Direct Bridge (wRTC) | [bottube.ai/bridge/wrtc](https://bottube.ai/bridge/wrtc) |
| Raydium Swap (SOL → wRTC) | [raydium.io/swap](https://raydium.io/swap/?inputMint=sol&outputMint=12TAdKXxcGf6oCv4rqDz2NkgxjyHq6HQKoxKZYGf5i4X) |
| Price Chart | [DexScreener](https://dexscreener.com/solana/8CF2Q8nSCxRacDShbtF86XTSrYjueBMKmfdR3MLdnYzb) |

---

## Step 1: Bridge RTC ↔ wRTC

### Open the Bridge
1. Go to [https://bottube.ai/bridge](https://bottube.ai/bridge)
2. Select direction:
   - **RTC → wRTC** (to use on Solana for trading)
   - **wRTC → RTC** (to return to RustChain for mining/governance)

### Connect Wallets
- Connect your **RustChain wallet** on the source side
- Connect your **Solana wallet** (Phantom, Solflare, etc.) on the destination side

### Enter Amount & Review
1. Enter the amount to bridge
2. Review the summary (fees, estimated arrival time)
3. **Double-check the destination address format**

### Confirm Transaction
1. Click "Bridge" or "Confirm"
2. Wait for blockchain confirmation
3. Verify receipt in your destination wallet
4. Check bridge history for transaction details

---

## Step 2: Swap SOL ↔ wRTC on Raydium

### Open Raydium Swap
1. Go to the [official Raydium swap link](https://raydium.io/swap/?inputMint=sol&outputMint=12TAdKXxcGf6oCv4rqDz2NkgxjyHq6HQKoxKZYGf5i4X)
2. **Verify the output token mint is exactly:**
   ```
   12TAdKXxcGf6oCv4rqDz2NkgxjyHq6HQKoxKZYGf5i4X
   ```

### Execute Swap
1. Select SOL (or another token) as input
2. Select wRTC as output (verify mint address!)
3. Set slippage (start with 1-2%, increase if needed)
4. Review and confirm the swap
5. Wait for confirmation

---

## Common Failure Modes & Safety Notes

### ⚠️ Wrong Wallet Format/Network
**Problem:** Bridge transactions fail if you provide an incompatible address or wrong chain wallet.

**Solution:**
- Double-check chain selection before connecting
- Verify address format matches the chain (Solana addresses are Base58, ~44 chars)
- Don't mix up Ethereum-style addresses with Solana addresses

### ⚠️ Fake Mint / Scam Token
**Problem:** Scammers create fake tokens with similar names.

**Solution:**
- **ALWAYS verify mint equals:** `12TAdKXxcGf6oCv4rqDz2NkgxjyHq6HQKoxKZYGf5i4X`
- Never trust copied symbols/names alone
- Only use official links from RustChain docs or verified channels
- Bookmark official URLs

### ⚠️ Slippage Too Tight
**Problem:** Volatile pools can fail with low slippage settings.

**Solution:**
- Start with 1-2% slippage
- Increase carefully in small steps if transaction fails
- Check pool liquidity on DexScreener first

### ⚠️ Wrong Direction in Bridge
**Problem:** Confusing RTC → wRTC (wrapping) with wRTC → RTC (unwrapping).

**Solution:**
- Confirm your goal before starting:
  - Want to trade on Solana? → **RTC → wRTC**
  - Want to mine or vote on RustChain? → **wRTC → RTC**

### ⚠️ Insufficient Balance for Fees
**Problem:** Transaction fails due to gas fee shortage.

**Solution:**
- Keep enough SOL in your Solana wallet for transaction fees
- Keep enough RTC in your RustChain wallet for bridge fees
- Fees are typically small but required

### ⚠️ Phishing Links
**Problem:** Fake bridge/swap sites steal your tokens.

**Solution:**
- **Bookmark official URLs** and use only those
- Never click bridge/swap links from unknown DMs or emails
- Verify URL spelling before connecting wallet
- Official bridge: `bottube.ai/bridge` (NOT bottube-bridge.com or similar)

---

## Pre-Transaction Checklist

Before signing any transaction, verify:

- [ ] Official bridge URL is correct (`bottube.ai/bridge`)
- [ ] Mint address is exactly `12TAdKXxcGf6oCv4rqDz2NkgxjyHq6HQKoxKZYGf5i4X`
- [ ] Wallet network and destination address are correct
- [ ] Slippage and amount are reviewed
- [ ] You understand bridge direction (RTC → wRTC or wRTC → RTC)
- [ ] You have enough balance for fees on both chains

---

## If Something Looks Wrong

**STOP before signing!**

1. Re-open this tutorial and re-check mint + URL
2. Ask in official RustChain channels with tx hash
3. **NEVER share your seed phrase or private key**

---

## Need Help?

- **Block Explorer:** [rustchain.org/explorer](https://rustchain.org/explorer)
- **Network Health:** `curl -sk https://rustchain.org/health`
- **Active Miners:** `curl -sk https://rustchain.org/api/miners`
- **Discord:** [discord.gg/VqVVS2CW9Q](https://discord.gg/VqVVS2CW9Q)

---

## Summary

| Action | Link | Key Check |
|--------|------|-----------|
| Bridge | [bottube.ai/bridge](https://bottube.ai/bridge) | Correct direction, wallet format |
| Swap | [Raydium](https://raydium.io/swap/?inputMint=sol&outputMint=12TAdKXxcGf6oCv4rqDz2NkgxjyHq6HQKoxKZYGf5i4X) | Mint = `12TAdK...5i4X` |
| Chart | [DexScreener](https://dexscreener.com/solana/8CF2Q8nSCxRacDShbtF86XTSrYjueBMKmfdR3MLdnYzb) | Verify pool liquidity |

**Remember:** When in doubt, stop and verify. Your tokens are your responsibility.
