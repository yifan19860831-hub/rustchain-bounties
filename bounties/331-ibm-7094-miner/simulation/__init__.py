# IBM 7094 Miner Simulation Package
"""
IBM 7094 Miner - RustChain Proof-of-Antiquity

Simulation modules for the legendary IBM 7094 (1962) mainframe computer.

Wallet: RTC4325af95d26d59c3ef025963656d22af638bb96b
Bounty: #331 - LEGENDARY Tier (200 RTC / $20)
"""

from .core_memory import CoreMemory
from .index_registers import IndexRegisters
from .data_channels import DataChannels, TapeDrive
from .punched_card import PunchedCard
from .magnetic_tape import MagneticTape
from .ibm7094_miner import IBM7094Miner

__all__ = [
    'CoreMemory',
    'IndexRegisters',
    'DataChannels',
    'TapeDrive',
    'PunchedCard',
    'MagneticTape',
    'IBM7094Miner',
]

__version__ = '1.0.0'
__author__ = 'RustChain IBM 7094 Team'
