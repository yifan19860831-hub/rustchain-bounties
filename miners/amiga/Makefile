# RustChain Miner for Amiga 500 - Makefile
# =========================================
# Build system for cross-compilation and native compilation
#
# Requirements:
#   - vbcc (http://sun.hasenbraten.de/vbcc/)
#   - OR m68k-amigaos-gcc (Amiga GCC cross-compiler)
#   - OR SAS/C 6.0+ (native Amiga compilation)
#
# Usage:
#   make              - Build with vbcc (default)
#   make gcc          - Build with m68k-amigaos-gcc
#   make sasc         - Build with SAS/C (on Amiga)
#   make clean        - Remove build artifacts
#   make all          - Build all variants
# ============================================================================

CC_VBCC = vc
CC_GCC = m68k-amigaos-gcc
CC_SASC = sc

CFLAGS_VBCC = +m68k -O2 -I$(VBCC)/include
CFLAGS_GCC = -O2 -m68000 -ffunction-sections -fdata-sections
CFLAGS_SASC = OPTIMIZE=TIME STRINGS DATA=CLOSE NOICONS

AS_VASM = vasmm68k_mot
ASFLAGS = -Fbin -mot -devpac

TARGET = rustchain_miner
TARGET_GCC = rustchain_miner_gcc
TARGET_SASC = rustchain_miner_sasc

SOURCES = rustchain_miner_amiga.c
ASM_SOURCES = fingerprint.asm

OBJECTS = rustchain_miner_amiga.o fingerprint.o

.PHONY: all clean gcc sasc help

all: $(TARGET)

# Default build with vbcc
$(TARGET): $(SOURCES) $(ASM_SOURCES)
	@echo "Building with vbcc..."
	$(AS_VASM) $(ASFLAGS) -o fingerprint.o $(ASM_SOURCES)
	$(CC_VBCC) $(CFLAGS_VBCC) -o=$(TARGET) $(SOURCES) fingerprint.o
	@echo "Build complete: $(TARGET)"

# Build with m68k-amigaos-gcc
gcc: $(SOURCES)
	@echo "Building with m68k-amigaos-gcc..."
	$(CC_GCC) $(CFLAGS_GCC) -o $(TARGET_GCC) $(SOURCES)
	@echo "Build complete: $(TARGET_GCC)"

# Build with SAS/C (native Amiga)
sasc: $(SOURCES)
	@echo "Building with SAS/C..."
	$(CC_SASC) $(CFLAGS_SASC) LINK $(SOURCES) TO $(TARGET_SASC)
	@echo "Build complete: $(TARGET_SASC)"

# Clean build artifacts
clean:
	@echo "Cleaning..."
	rm -f *.o $(TARGET) $(TARGET_GCC) $(TARGET_SASC) *.map *.lnk
	@echo "Clean complete."

# Help target
help:
	@echo "RustChain Miner for Amiga 500 - Build Options"
	@echo "=============================================="
	@echo ""
	@echo "  make          - Build with vbcc (default, recommended)"
	@echo "  make gcc      - Build with m68k-amigaos-gcc"
	@echo "  make sasc     - Build with SAS/C 6.0+ (on Amiga)"
	@echo "  make clean    - Remove all build artifacts"
	@echo "  make all      - Build all variants"
	@echo "  make help     - Show this help message"
	@echo ""
	@echo "Output:"
	@echo "  rustchain_miner        - vbcc build (default)"
	@echo "  rustchain_miner_gcc    - GCC cross-compiled build"
	@echo "  rustchain_miner_sasc   - SAS/C native build"
	@echo ""

# Installation helper
install: $(TARGET)
	@echo "Installing to Amiga..."
	@echo "Copy $(TARGET) to your Amiga system via:"
	@echo "  - Network (FTP/SMB)"
	@echo "  - Floppy disk"
	@echo "  - CompactFlash/SD card"
	@echo "  - Serial transfer (XModem)"
	@echo ""

# Test build (syntax check only)
test:
	@echo "Testing syntax..."
	$(CC_VBCC) $(CFLAGS_VBCC) -c $(SOURCES)
	$(AS_VASM) $(ASFLAGS) -o test.o $(ASM_SOURCES)
	rm -f *.o test.o
	@echo "Syntax check passed."
