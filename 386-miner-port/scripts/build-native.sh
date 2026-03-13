#!/bin/bash
#
# RustChain 386 Miner - Native Build Script
#
# This script compiles the miner directly on the 386 system.
# Run this on Slackware 3.0 or Debian 2.x running on real 386 hardware.
#
# Requirements:
#   - GCC 2.x (included in Slackware 3.0 'd' package)
#
# Usage:
#   ./build-native.sh
#

set -e

echo "=================================================="
echo "  RustChain 386 Miner - Native Build"
echo "=================================================="
echo ""

# Check for GCC
if ! command -v gcc &> /dev/null; then
    echo "ERROR: GCC not found!"
    echo ""
    echo "Install GCC on Slackware 3.0:"
    echo "  1. Mount Slackware installation media"
    echo "  2. Install 'd' package (development tools)"
    echo "     mount /dev/cdrom /mnt"
    echo "     installpkg /mnt/d/*.tgz"
    exit 1
fi

GCC_VERSION=$(gcc --version 2>&1 | head -1)
echo "Using compiler: $GCC_VERSION"
echo ""

# Compiler flags for 386
CFLAGS="-m386 -march=i386 -O2 -Wall"
CFLAGS="$CFLAGS -I./include"

# Check for ioperm support
CFLAGS="$CFLAGS -D_GNU_SOURCE"

echo "Compiler flags: $CFLAGS"
echo ""

# Create directories
mkdir -p bin
mkdir -p obj

# Compile object files
echo "Compiling source files..."

gcc $CFLAGS -c src/entropy.c -o obj/entropy.o
echo "  [OK] entropy.c"

gcc $CFLAGS -c src/fingerprint.c -o obj/fingerprint.o
echo "  [OK] fingerprint.c"

gcc $CFLAGS -c src/network.c -o obj/network.o
echo "  [OK] network.c"

gcc $CFLAGS -c src/wallet.c -o obj/wallet.o
echo "  [OK] wallet.c"

gcc $CFLAGS -c src/miner.c -o obj/miner.o
echo "  [OK] miner.c"

# Link
echo ""
echo "Linking..."
gcc $CFLAGS -o bin/rustchain-386-miner \
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
ls -l bin/rustchain-386-miner
echo ""
echo "Run the miner:"
echo "  ./bin/rustchain-386-miner"
echo ""
echo "Or install system-wide:"
echo "  cp bin/rustchain-386-miner /usr/local/bin/"
echo "  chmod +x /usr/local/bin/rustchain-386-miner"
echo ""
