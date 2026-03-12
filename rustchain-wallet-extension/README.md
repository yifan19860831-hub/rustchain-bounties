# RustChain Wallet Browser Extension

🦀 Official RustChain (RTC) wallet browser extension for Chrome and Firefox.

## Features

- ✅ **Create Wallet**: Generate BIP39 24-word seed phrase with Ed25519 keypair
- ✅ **Import Wallet**: Restore from existing seed phrase
- ✅ **View Balance**: Check RTC balance from RustChain node
- ✅ **Send RTC**: Sign and submit transfers securely
- ✅ **Transaction History**: View recent transactions
- ✅ **Encrypted Storage**: AES-256-GCM encrypted keystores
- ✅ **Multiple Wallets**: Manage multiple RTC addresses
- ✅ **Network Selector**: Switch between mainnet and custom nodes
- ✅ **Auto-Lock**: Automatic wallet lock after 5 minutes of inactivity

## Security

- Private keys encrypted at rest with user password
- Seed phrase shown only once during creation
- Transaction signing requires password
- No external key servers - all crypto happens locally
- Web Crypto API for secure cryptographic operations
- Content Security Policy (CSP) enabled

## Installation

### Development

1. Clone or download this repository
2. Open Chrome and navigate to `chrome://extensions/`
3. Enable "Developer mode" (toggle in top right)
4. Click "Load unpacked"
5. Select the `rustchain-wallet-extension` folder

### Firefox (Coming Soon)

1. Open Firefox and navigate to `about:debugging`
2. Click "This Firefox"
3. Click "Load Temporary Add-on"
4. Select `manifest.json` from the extension folder

## Usage

### Creating a New Wallet

1. Click the extension icon
2. Enter a strong password (min 8 characters)
3. Click "Create Wallet"
4. **IMPORTANT**: Write down your 24-word seed phrase and store it safely
5. Click "I've Backed It Up"

### Importing an Existing Wallet

1. Click "Import Wallet" tab
2. Enter your 12-24 word seed phrase
3. Enter a password
4. Click "Import Wallet"

### Sending RTC

1. Unlock your wallet with password
2. Go to "Send" tab
3. Enter recipient address (must start with "RTC")
4. Enter amount in RTC
5. (Optional) Add a memo
6. Enter your password to confirm
7. Click "Send RTC"

### Receiving RTC

1. Go to "Receive" tab
2. Copy your address and share it with the sender
3. QR code support coming soon

## API Endpoints

The extension communicates with RustChain nodes:

- **Balance**: `GET /wallet/balance?miner_id={address}`
- **Transfer**: `POST /wallet/transfer/signed`
- **Nonce**: `GET /wallet/nonce?address={address}`
- **Transactions**: `GET /wallet/transactions?address={address}&limit={limit}`

Default node: `https://50.28.86.131`

## Technical Details

### Cryptography

- **BIP39**: 24-word mnemonic generation
- **Ed25519**: Digital signatures for transactions
- **PBKDF2**: Key derivation (100,000 iterations)
- **AES-256-GCM**: Encrypted keystores
- **Address Format**: `RTC` + SHA256(pubkey)[:40]

### Manifest V3

This extension uses Chrome Manifest V3 specification:
- Service worker background script
- Secure content security policy
- Minimal permissions

### File Structure

```
rustchain-wallet-extension/
├── manifest.json          # Extension manifest (V3)
├── background.js          # Service worker
├── popup.html            # Main UI
├── popup.js              # UI logic
├── src/
│   ├── crypto.js         # Cryptographic utilities
│   └── api.js            # RustChain API client
└── icons/
    ├── icon16.png
    ├── icon48.png
    └── icon128.png
```

## Development

### Building Icons

Generate icons using any image editor or online tool. Recommended sizes:
- 16x16 (toolbar icon)
- 48x48 (extensions page)
- 128x128 (Chrome Web Store)

### Testing

1. Test wallet creation and backup
2. Test wallet import
3. Test balance fetching
4. Test transaction signing (use testnet first!)
5. Test auto-lock functionality

### Debugging

- Open `chrome://extensions/` and click "Inspect views: background page"
- Right-click extension popup and select "Inspect"

## Roadmap

- [ ] Firefox compatibility
- [ ] QR code generation for receive address
- [ ] MetaMask Snap integration
- [ ] Hardware wallet support
- [ ] Multi-chain support
- [ ] Enhanced transaction details
- [ ] Push notifications for incoming transactions
- [ ] Dark mode theme

## Security Considerations

⚠️ **IMPORTANT**:
- Never share your seed phrase with anyone
- Always backup your seed phrase in a secure location
- This is beta software - test with small amounts first
- Report security issues immediately to the maintainers

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

- GitHub Issues: https://github.com/Scottcjn/rustchain-wallet/issues
- Discord: https://discord.gg/VqVVS2CW9Q
- Documentation: https://rustchain.org

## Acknowledgments

Built on the RustChain blockchain with Proof-of-Antiquity consensus.

---

**Version**: 1.0.0  
**Manifest**: V3  
**Last Updated**: March 2026
