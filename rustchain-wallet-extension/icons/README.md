# RustChain Wallet Extension - Icons

This folder contains icons for the RustChain Wallet browser extension.

## Required Icons

- `icon16.png` - 16x16 pixels (toolbar icon)
- `icon48.png` - 48x48 pixels (extensions page)
- `icon128.png` - 128x128 pixels (Chrome Web Store)

## Creating Icons

You can convert the provided `icon.svg` to PNG using:

### Online Tools
- https://cloudconvert.com/svg-to-png
- https://svgtopng.com/

### Command Line (ImageMagick)
```bash
# Install ImageMagick first
convert -background none -resize 16x16 icon.svg icon16.png
convert -background none -resize 48x48 icon.svg icon48.png
convert -background none -resize 128x128 icon.svg icon128.png
```

### Using Node.js (sharp)
```bash
npm install sharp
```

```javascript
const sharp = require('sharp');

async function convertIcons() {
  await sharp('icon.svg').resize(16, 16).png().toFile('icon16.png');
  await sharp('icon.svg').resize(48, 48).png().toFile('icon48.png');
  await sharp('icon.svg').resize(128, 128).png().toFile('icon128.png');
}

convertIcons();
```

## Icon Design

The icon features:
- Purple gradient background (matching the wallet UI)
- Yellow crab (RustChain mascot)
- "RTC" text

## Placeholder Icons

If you need placeholder icons immediately, you can use any 16x16, 48x48, and 128x128 PNG files temporarily. The extension will load without errors, but you should replace them with proper icons before publishing.
