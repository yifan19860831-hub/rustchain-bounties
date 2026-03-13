#!/bin/bash
# Test build script for Amiga 500 miner
# This script validates the build process without requiring actual Amiga hardware

set -e

echo "=========================================="
echo "RustChain Amiga 500 Miner - Build Test"
echo "=========================================="
echo ""

# Check for required tools
echo "Checking build tools..."

if command -v vc &> /dev/null; then
    echo "✓ vbcc found: $(which vc)"
    VBCC_AVAILABLE=true
else
    echo "✗ vbcc not found (optional)"
    VBCC_AVAILABLE=false
fi

if command -v m68k-amigaos-gcc &> /dev/null; then
    echo "✓ m68k-amigaos-gcc found: $(which m68k-amigaos-gcc)"
    GCC_AVAILABLE=true
else
    echo "✗ m68k-amigaos-gcc not found (optional)"
    GCC_AVAILABLE=false
fi

if command -v vasmm68k_mot &> /dev/null; then
    echo "✓ vasm found: $(which vasmm68k_mot)"
    VASM_AVAILABLE=true
else
    echo "✗ vasm not found (optional)"
    VASM_AVAILABLE=false
fi

echo ""
echo "Source files:"
ls -lh rustchain_miner_amiga.c fingerprint.asm Makefile 2>/dev/null || echo "  (files not in current directory)"

echo ""
echo "Syntax validation (if tools available):"

# Test C syntax with gcc if available
if [ "$GCC_AVAILABLE" = true ]; then
    echo "  Checking C syntax with gcc..."
    m68k-amigaos-gcc -fsyntax-only -m68000 rustchain_miner_amiga.c && echo "  ✓ C syntax OK" || echo "  ✗ C syntax errors"
fi

# Test assembly syntax with vasm if available
if [ "$VASM_AVAILABLE" = true ]; then
    echo "  Checking assembly syntax with vasm..."
    vasmm68k_mot -Fbin -mot -devpac -o test.o fingerprint.asm && echo "  ✓ Assembly syntax OK" && rm -f test.o || echo "  ✗ Assembly syntax errors"
fi

echo ""
echo "=========================================="
echo "Build test complete!"
echo "=========================================="
echo ""
echo "To build for real Amiga 500 hardware:"
echo "  1. Install vbcc or m68k-amigaos-gcc"
echo "  2. Run: make"
echo "  3. Transfer binary to Amiga 500"
echo "  4. Execute: ./rustchain_miner"
echo ""
echo "For questions, see README.md"
