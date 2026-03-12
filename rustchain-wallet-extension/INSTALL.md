# RustChain Wallet Extension - Installation & Testing Guide

## Quick Start

### 1. Install Dependencies (Optional - for icon generation)

```bash
cd rustchain-wallet-extension
npm install
npm run generate-icons
```

If you skip this step, you'll need to manually add PNG icons to the `icons/` folder.

### 2. Load Extension in Chrome

1. Open Chrome
2. Navigate to `chrome://extensions/`
3. Enable "Developer mode" (toggle in top right corner)
4. Click "Load unpacked"
5. Select the `rustchain-wallet-extension` folder
6. Extension should appear in your toolbar

### 3. Create Your First Wallet

1. Click the RustChain Wallet icon in toolbar
2. Enter a strong password (min 8 characters)
3. Click "Create Wallet"
4. **CRITICAL**: Write down the 24-word seed phrase
5. Store it in a secure location (offline recommended)
6. Click "I've Backed It Up"

### 4. Test Basic Functionality

#### Check Balance
- Balance should show 0.00 RTC for new wallet
- If you have RTC, request test tokens or use mainnet

#### Send Transaction (Test Mode)
1. Go to "Send" tab
2. Enter a valid RTC address (you can create a second wallet to test)
3. Enter small amount (e.g., 0.01)
4. Add optional memo
5. Enter password
6. Click "Send RTC"

#### Check History
- Go to "History" tab
- Should show your transaction

## Testing Checklist

- [ ] Extension loads without errors
- [ ] Can create new wallet
- [ ] Seed phrase displays correctly (24 words)
- [ ] Can backup and acknowledge seed phrase
- [ ] Wallet shows correct address (starts with "RTC")
- [ ] Can lock/unlock wallet with password
- [ ] Balance displays (may be 0 for new wallet)
- [ ] Can send RTC (requires funded wallet)
- [ ] Transaction appears in history
- [ ] Auto-lock works after 5 minutes
- [ ] Can import wallet from seed phrase
- [ ] Can switch node URL in settings
- [ ] Copy address button works

## Troubleshooting

### Extension doesn't load
- Check Chrome console for errors: `chrome://extensions/` → "Inspect views: background page"
- Ensure all files are present (manifest.json, background.js, popup.html, etc.)
- Icons must be PNG format

### "Wallet creation failed"
- Check background script console for errors
- Ensure password is at least 8 characters
- Try clearing extension data and reloading

### Balance shows 0 but wallet has RTC
- Check node URL in settings (default: https://50.28.86.131)
- Verify node is accessible
- Check browser console for API errors

### Transaction fails
- Ensure sufficient balance
- Check recipient address format (must start with "RTC")
- Verify node is online
- Check password is correct

## Development Tips

### Debugging

**Background Script:**
1. Go to `chrome://extensions/`
2. Find RustChain Wallet
3. Click "Inspect views: background page"
4. Use Console and Network tabs

**Popup UI:**
1. Right-click extension popup
2. Select "Inspect"
3. Use DevTools as normal

### Reloading Changes

After making code changes:
1. Go to `chrome://extensions/`
2. Click refresh icon on RustChain Wallet card
3. Re-open popup to see changes

### Testing Crypto Functions

Open background script console and test:

```javascript
// Test mnemonic generation
const mnemonic = await RustChainCrypto.generateMnemonic();
console.log('Mnemonic:', mnemonic);

// Test encryption
const data = { test: 'value' };
const encrypted = await RustChainCrypto.encryptKeystore(data, 'password123');
console.log('Encrypted:', encrypted);

const decrypted = await RustChainCrypto.decryptKeystore(encrypted, 'password123');
console.log('Decrypted:', decrypted);
```

## Security Testing

### Test Cases

1. **Password Strength**
   - Try weak passwords (< 8 chars)
   - Verify rejection

2. **Auto-Lock**
   - Unlock wallet
   - Wait 5 minutes
   - Verify wallet locks automatically

3. **Encryption**
   - Create wallet
   - Uninstall extension
   - Reinstall and import with seed
   - Verify wallet restores correctly

4. **XSS Protection**
   - Try injecting scripts in memo field
   - Verify they're sanitized

## Publishing to Chrome Web Store

### Prerequisites

1. Chrome Web Store Developer account ($5 one-time fee)
2. Proper icons (16, 48, 128, 256, 512 pixels)
3. Screenshots (1280x800 or 640x400)
4. Privacy policy URL

### Steps

1. **Prepare Assets**
   - Generate all icon sizes
   - Take screenshots
   - Write description
   - Create privacy policy

2. **Zip Extension**
   ```bash
   # Remove node_modules and dev files
   zip -r rustchain-wallet.zip . -x "node_modules/*" -x "*.md" -x ".gitignore"
   ```

3. **Upload to Chrome Web Store**
   - Go to [Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/devconsole)
   - Create new item
   - Upload zip
   - Fill in store listing
   - Submit for review

### Store Listing Tips

- **Title**: "RustChain Wallet - Official RTC Wallet"
- **Description**: Highlight security features and ease of use
- **Category**: Productivity or Other
- **Tags**: cryptocurrency, wallet, rtc, rustchain, blockchain

## Firefox Version

To create Firefox version:

1. Update `manifest.json` for WebExtensions compatibility
2. Test in Firefox (`about:debugging`)
3. Submit to [Firefox Add-ons](https://addons.mozilla.org/)

## MetaMask Snap (Future)

For MetaMask Snap integration (bonus 40 RTC):
- See issue #730 for requirements
- Use `@metamask/snaps-sdk`
- Implement custom RPC methods for RustChain
- Publish to MetaMask Snap registry

## Support

- GitHub: https://github.com/Scottcjn/rustchain-wallet
- Discord: https://discord.gg/VqVVS2CW9Q
- Documentation: https://rustchain.org

## Bounty Claim

After completing testing and validation:

1. Push code to GitHub
2. Test in production (mainnet)
3. Take screenshots/demo video
4. Comment on issue #730 with:
   - GitHub repo link
   - Demo video/screenshots
   - Your RTC wallet address
   - Chrome Web Store link (if published)

Good luck! 🦀
