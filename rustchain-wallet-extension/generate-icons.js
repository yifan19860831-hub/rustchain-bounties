const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

async function generateIcons() {
  const svgPath = path.join(__dirname, 'icons', 'icon.svg');
  const iconsDir = path.join(__dirname, 'icons');
  
  // Check if sharp is available
  try {
    require.resolve('sharp');
  } catch (e) {
    console.log('Sharp not installed. Creating placeholder PNGs...');
    createPlaceholderIcons();
    return;
  }
  
  const sizes = [16, 48, 128];
  
  try {
    for (const size of sizes) {
      const outputPath = path.join(iconsDir, `icon${size}.png`);
      await sharp(svgPath)
        .resize(size, size)
        .png()
        .toFile(outputPath);
      console.log(`✓ Generated icon${size}.png`);
    }
    console.log('\nAll icons generated successfully!');
  } catch (error) {
    console.error('Error generating icons:', error.message);
    console.log('\nCreating placeholder icons instead...');
    createPlaceholderIcons();
  }
}

function createPlaceholderIcons() {
  // Create simple colored square PNGs using Buffer
  const sizes = [16, 48, 128];
  const iconsDir = path.join(__dirname, 'icons');
  
  for (const size of sizes) {
    const outputPath = path.join(iconsDir, `icon${size}.png`);
    
    // Create a simple purple square
    const buffer = Buffer.alloc(size * size * 4);
    for (let i = 0; i < size * size; i++) {
      const offset = i * 4;
      // Purple color (RGBA)
      buffer[offset] = 102;     // R
      buffer[offset + 1] = 126; // G
      buffer[offset + 2] = 234; // B
      buffer[offset + 3] = 255; // A
    }
    
    // Note: This is a raw RGBA buffer, not a real PNG
    // For real PNGs, install sharp: npm install
    fs.writeFileSync(outputPath, buffer);
    console.log(`⚠ Created placeholder icon${size}.png (install sharp for proper icons)`);
  }
  
  console.log('\n⚠ Placeholder icons created. For proper icons:');
  console.log('  1. Run: npm install');
  console.log('  2. Run: npm run generate-icons');
}

generateIcons();
