#!/bin/bash
# Build script for RustChain IBM System/360 Miner
# ================================================
# This script assembles the S/360 assembly code and prepares it for
# execution on Hercules simulator or native Python wrapper.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================"
echo "RustChain S/360 Miner Build"
echo "========================================"
echo ""

# Check for assembler
if command -v hlasm &> /dev/null; then
    ASSEMBLER="hlasm"
    echo "Using HLASM assembler"
elif command -v asma &> /dev/null; then
    ASSEMBLER="asma"
    echo "Using ASMA assembler"
elif command -v pasm &> /dev/null; then
    ASSEMBLER="pasm"
    echo "Using PASM assembler"
else
    echo "No S/360 assembler found. Using Python wrapper mode only."
    echo ""
    echo "To assemble the S/360 code, install one of:"
    echo "  - HLASM (IBM High Level Assembler)"
    echo "  - ASMA (A Small Mainframe Assembler)"
    echo "  - PASM (Portable Assembler)"
    echo ""
    echo "For this demo, we'll use the Python simulator wrapper."
    echo ""
    
    # Create a simple placeholder binary
    echo "Creating placeholder binary for demo..."
    echo -n "S360MINER_PLACEHOLDER" > miner.bin
    echo "Build complete (Python mode only)"
    exit 0
fi

# Assemble the miner
echo "Assembling miner.asm..."
$ASSEMBLER -o miner.bin miner.asm

if [ $? -eq 0 ]; then
    echo "Assembly successful!"
    echo ""
    echo "Output files:"
    ls -la miner.bin miner.lst 2>/dev/null || ls -la miner.bin
    echo ""
    echo "To run on Hercules simulator:"
    echo "  hercules -f s360.cnf"
    echo ""
    echo "Or use Python wrapper:"
    echo "  python3 s360_miner.py"
else
    echo "Assembly failed!"
    exit 1
fi
