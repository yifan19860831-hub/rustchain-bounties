#!/bin/bash
#
# RustChain 386 Miner - Cross-Compilation Build Script
#
# This script compiles the miner on a modern Linux system
# for deployment to Intel 386 hardware.
#
# Requirements:
#   - i686-linux-gnu-gcc (or i386-elf-gcc)
#
# Usage:
#   ./build-cross.sh
#

set -e

echo "=================================================="
echo "  RustChain 386 Miner - Cross-Compilation Build"
echo "=================================================="

# Detect available cross-compiler
if command -v i686-linux-gnu-gcc &> /dev/null; then
    CC="i686-linux-gnu-gcc"
    echo "Using compiler: i686-linux-gnu-gcc"
elif command -v i386-elf-gcc &> /dev/null; then
    CC="i386-elf-gcc"
    echo "Using compiler: i386-elf-gcc"
else
    echo "ERROR: No cross-compiler found!"
    echo ""
    echo "Install one of the following:"
    echo "  Ubuntu/Debian: sudo apt-get install gcc-i686-linux-gnu"
    echo "  Or build i386-elf-gcc from source"
    exit 1
fi

# Compiler flags for 386
CFLAGS="-m386 -march=i386 -O2 -Wall -Wextra"
CFLAGS="$CFLAGS -I./include"

# Check for ioperm support (needed for ISA timing)
CFLAGS="$CFLAGS -D_GNU_SOURCE"

echo ""
echo "Compiler flags: $CFLAGS"
echo ""

# Create output directory
mkdir -p bin
mkdir -p obj

# Compile object files
echo "Compiling source files..."

$CC $CFLAGS -c src/entropy.c -o obj/entropy.o
echo "  [OK] entropy.c"

$CC $CFLAGS -c src/fingerprint.c -o obj/fingerprint.o
echo "  [OK] fingerprint.c"

$CC $CFLAGS -c src/network.c -o obj/network.o
echo "  [OK] network.c"

$CC $CFLAGS -c src/wallet.c -o obj/wallet.o
echo "  [OK] wallet.c"

$CC $CFLAGS -c src/miner.c -o obj/miner.o
echo "  [OK] miner.c"

# Link
echo ""
echo "Linking..."
$CC $CFLAGS -o bin/rustchain-386-miner \
    obj/entropy.o \
    obj/fingerprint.o \
    obj/network.o \
    obj/wallet.o \
    obj/miner.o \
    -lm

echo ""
echo "=================================================="
echo "  BUILD SUCCESSFUL!"
echo "=================================================="
echo ""
echo "Output: bin/rustchain-386-miner"
echo ""
echo "File info:"
file bin/rustchain-386-miner
ls -lh bin/rustchain-386-miner
echo ""
echo "To deploy to 386 system:"
echo "  1. Copy bin/rustchain-386-miner to 386 system"
echo "  2. Also copy: miner.cfg, scripts/"
echo "  3. Run: ./rustchain-386-miner"
echo ""
echo "Transfer methods:"
echo "  - FTP: scp bin/rustchain-386-miner user@386-host:/usr/local/bin/"
echo "  - Serial: kermit -c -s bin/rustchain-386-miner"
echo "  - CF card: Mount CF card on modern system, copy file"
echo ""
