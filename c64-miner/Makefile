# Commodore 64 RustChain Miner - Makefile

CC = cl65
AS = ca65
CFLAGS = -t c64 -O -Or -Oi
ASFLAGS = -t c64

# Source files
SRCS_C = src/main.c src/miner.c src/network.c src/fingerprint.c src/ui.c
OBJS = $(SRCS_C:.c=.o)

# Output
TARGET = miner.prg

# Default target
all: $(TARGET)

# Link
$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^

# Compile C files
%.o: %.c
	$(CC) $(CFLAGS) -c $<

# Clean
clean:
	del *.o
	del $(TARGET)

# Run in VICE emulator
run: $(TARGET)
	x64 $(TARGET)

# Install dependencies (Windows)
install:
	@echo Install cc65 from: https://cc65.github.io
	@echo Install VICE from: https://vice-emu.sourceforge.io

.PHONY: all clean run install
