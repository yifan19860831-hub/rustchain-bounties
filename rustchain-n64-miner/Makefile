# RustChain N64 Miner Makefile
# 
# Build system for Nintendo 64 miner

# Targets
TARGET := mips64-unknown-none
TARGET_RELEASE := mips64-unknown-linux-gnu

# Project name
PROJECT := rustchain-n64

# Build directories
BUILD_DIR := target/$(TARGET)/release
BUILD_DIR_LINUX := target/$(TARGET_RELEASE)/release

# Output files
OUTPUT_ROM := $(PROJECT).z64
OUTPUT_BIN := $(PROJECT)-linux

# Features
FEATURES := n64-homebrew

# Default target
all: rom linux

# Build N64 ROM (bare-metal)
rom:
	@echo "Building N64 ROM..."
	cargo build --release --target $(TARGET) --features $(FEATURES)
	@echo "ROM built at $(BUILD_DIR)/$(PROJECT)"

# Build Linux binary (for flash carts with OS)
linux:
	@echo "Building Linux binary..."
	cargo build --release --target $(TARGET_RELEASE) --features network
	@echo "Binary built at $(BUILD_DIR_LINUX)/$(PROJECT)"

# Clean build artifacts
clean:
	cargo clean
	rm -f $(OUTPUT_ROM) $(OUTPUT_BIN)

# Install MIPS targets
install-targets:
	rustup target add $(TARGET)
	rustup target add $(TARGET_RELEASE)

# Run clippy
lint:
	cargo clippy --target $(TARGET) --features $(FEATURES)
	cargo clippy --target $(TARGET_RELEASE) --features network

# Format code
fmt:
	cargo fmt

# Run tests (std only)
test:
	cargo test --features std

# Create ROM file (requires N64 toolchain)
create-rom: rom
	@echo "Creating Z64 ROM..."
	# In production, use N64 SDK tools to create proper ROM
	cp $(BUILD_DIR)/$(PROJECT) $(OUTPUT_ROM)

# Upload to 64drive
upload-64drive: rom
	@echo "Uploading to 64drive..."
	# Requires 64drive CLI tool
	64drive upload $(OUTPUT_ROM)

# Upload to EverDrive
upload-everdrive: rom
	@echo "Copy $(OUTPUT_ROM) to EverDrive SD card"

# Benchmark
bench:
	cargo bench --features std

# Generate documentation
doc:
	cargo doc --features $(FEATURES) --no-deps

# Help
help:
	@echo "RustChain N64 Miner Build System"
	@echo ""
	@echo "Targets:"
	@echo "  all            - Build ROM and Linux binary"
	@echo "  rom            - Build N64 ROM (bare-metal)"
	@echo "  linux          - Build Linux binary"
	@echo "  clean          - Clean build artifacts"
	@echo "  install-targets- Install MIPS targets"
	@echo "  lint           - Run clippy"
	@echo "  fmt            - Format code"
	@echo "  test           - Run tests"
	@echo "  create-rom     - Create Z64 ROM file"
	@echo "  upload-64drive - Upload to 64drive"
	@echo "  upload-everdrive- Upload to EverDrive"
	@echo "  bench          - Run benchmarks"
	@echo "  doc            - Generate documentation"
	@echo "  help           - Show this help"

.PHONY: all rom linux clean install-targets lint fmt test create-rom upload-64drive upload-everdrive bench doc help
