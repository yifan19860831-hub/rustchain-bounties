"""
ENIAC RustChain Miner Package
==============================
RustChain miner for ENIAC (1945) - The first general-purpose electronic computer.

This package provides:
- ENIAC simulator with decimal accumulators
- Hardware fingerprint generation
- RustChain mining client
- LEGENDARY Tier 5.0x multiplier

Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b
Bounty: 200 RTC ($20) - Issue #388
"""

__version__ = '1.0.0'
__author__ = 'RustChain ENIAC Team'
__license__ = 'Apache 2.0'

from .simulator.eniac_simulator import ENIACSimulator, Accumulator, FunctionTable, MasterProgrammer

__all__ = [
    'ENIACSimulator',
    'Accumulator',
    'FunctionTable',
    'MasterProgrammer',
]
