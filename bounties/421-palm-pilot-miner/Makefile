# Makefile for RustChain Palm Pilot Miner
# 
# Requires: Palm OS SDK, m68k-palmos-gcc
#
# Usage:
#   make          - Build the PRC file
#   make clean    - Remove build artifacts
#   make install  - Install to Palm Pilot (requires palm-install)
#   make test     - Test in POSE emulator

# Compiler settings
CC = m68k-palmos-gcc
AS = m68k-palmos-as
LD = m68k-palmos-ld

# Palm OS SDK paths (adjust as needed)
PALM_OS_SDK = /opt/palmos-sdk
PALM_OS_INCLUDE = $(PALM_OS_SDK)/include
PALM_OS_LIB = $(PALM_OS_SDK)/lib

# Application settings
APP_NAME = RustChainMiner
APP_CREATOR = RtCh
APP_VERSION = 0.1

# Source files
SRC_DIR = src
INCLUDE_DIR = include
BUILD_DIR = build

# Source files
SOURCES = $(SRC_DIR)/miner.c
OBJECTS = $(SOURCES:$(SRC_DIR)/%.c=$(BUILD_DIR)/%.o)

# Compiler flags
CFLAGS = -O2 -Wall -Wextra
CFLAGS += -I$(PALM_OS_INCLUDE) -I$(INCLUDE_DIR)
CFLAGS += -mpilot -mshort

# Linker flags
LDFLAGS = -mpilot
LDFLAGS += -L$(PALM_OS_LIB)
LDFLAGS += -lpalm

# Target files
TARGET_PRC = $(APP_NAME).prc
TARGET_ELF = $(BUILD_DIR)/$(APP_NAME).elf

# Default target
all: $(TARGET_PRC)

# Create build directory
$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

# Compile source files
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

# Link ELF
$(TARGET_ELF): $(OBJECTS)
	$(LD) $(LDFLAGS) -o $@ $^

# Build PRC file
$(TARGET_PRC): $(TARGET_ELF)
	palm-prc --creator=$(APP_CREATOR) --version=$(APP_VERSION) -o $@ $<

# Install to Palm Pilot
install: $(TARGET_PRC)
	palm-install $(TARGET_PRC)

# Clean build artifacts
clean:
	rm -rf $(BUILD_DIR)
	rm -f $(TARGET_PRC)
	rm -f $(TARGET_ELF)

# Test in POSE emulator (requires POSE installed)
test: $(TARGET_PRC)
	@echo "To test in POSE:"
	@echo "1. Open POSE emulator"
	@echo "2. Load Palm OS ROM"
	@echo "3. Install $(TARGET_PRC) via File > Install"
	@echo "4. Run the miner app"

# Show help
help:
	@echo "RustChain Palm Pilot Miner Build System"
	@echo ""
	@echo "Targets:"
	@echo "  all      - Build the PRC file (default)"
	@echo "  clean    - Remove build artifacts"
	@echo "  install  - Install to Palm Pilot"
	@echo "  test     - Show POSE testing instructions"
	@echo "  help     - Show this help message"
	@echo ""
	@echo "Requirements:"
	@echo "  - Palm OS SDK"
	@echo "  - m68k-palmos-gcc"
	@echo "  - palm-prc (PRC builder)"
	@echo "  - palm-install (optional, for installation)"

.PHONY: all clean install test help
