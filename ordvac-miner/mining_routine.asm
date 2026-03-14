# ORDVAC Mining Routine
# RustChain Proof-of-Antiquity
# 
# This assembly program implements the mining algorithm
# for ORDVAC (1951) - IAS machine clone
#
# Memory Layout:
#   0x000-0x0FF: Program code
#   0x100-0x1FF: Mining data
#   0x200-0x3FF: Entropy buffer

# ============================================================
# MINING ROUTINE - ORDVAC Assembly
# ============================================================

                ORG     0           # Start at memory address 0

# --- Initialization ---
INIT            LOAD    COUNTER     # Initialize counter
                STORE   COUNTER     # Store initial value
                LOAD    ENTROPY_SEED # Load entropy seed
                STORE   ENTROPY_REG  # Store in entropy register

# --- Main Mining Loop ---
MINING_LOOP     LOAD    COUNTER     # Load current counter
                ADD     INCREMENT   # Add increment value
                STORE   COUNTER     # Store updated counter
                
                # Entropy collection via timing
                LOAD    ENTROPY_REG # Load entropy register
                MPY     MULTIPLIER  # Multiply (732μs operation)
                STORE   ENTROPY_BUF # Store entropy sample
                
                # Hardware fingerprint calculation
                LOAD    COUNTER     # Load counter for hash
                SUB     CHECKPOINT  # Subtract checkpoint
                JUMP+   CONTINUE    # If positive, continue
                JUMP    MINING_LOOP # Otherwise loop
                
CONTINUE        OUTPUT  STATUS      # Output status to operator
                LOAD    ENTROPY_BUF # Load entropy buffer
                ADD     ACCUMULATOR # Add to accumulator
                STORE   ACCUMULATOR # Store result
                
                # Check if epoch complete
                LOAD    COUNTER     # Load counter
                SUB     EPOCH_END   # Compare to epoch end
                JUMP-   MINING_LOOP # If not done, continue
                
                # Epoch complete - prepare attestation
                LOAD    ACCUMULATOR # Load final accumulator
                STORE   ATTESTATION # Store attestation value
                HALT                # Stop execution

# --- Data Section ---
                ORG     256         # Data starts at address 256

COUNTER         DW      0           # Mining counter (initialized to 0)
INCREMENT       DW      1           # Counter increment
ENTROPY_SEED    DW      12345       # Initial entropy seed
ENTROPY_REG     DW      0           # Entropy working register
MULTIPLIER      DW      31          # Multiplication factor
ENTROPY_BUF     DW      0           # Entropy sample buffer
ACCUMULATOR     DW      0           # Running accumulator
CHECKPOINT      DW      1000        # Checkpoint value
EPOCH_END       DW      10000       # Epoch end counter
STATUS          DW      0           # Status output
ATTESTATION     DW      0           # Final attestation value

# --- Constants ---
                ORG     512         # Constants section

ZERO            DW      0           # Constant zero
ONE             DW      1           # Constant one
WILLIAMS_REF    DW      72          # Williams tube refresh time (μs)
VACUUM_TUBE     DW      732         # Vacuum tube mult time (μs)

                ORG     1023        # End of memory
END_MARKER      DW      0xDEADBEEF  # Memory end marker

# ============================================================
# END OF MINING ROUTINE
# ============================================================
