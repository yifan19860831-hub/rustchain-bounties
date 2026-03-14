"""
Game & Watch RustChain Miner Simulator

Emulates mining on Nintendo Game & Watch (1980) hardware.
"""

from .main import GameWatchMiner, main
from .lcd_display import SegmentedDisplay, LCDSegment
from .sm5xx_cpu import SharpSM5xxEmulator
from .miner_badge import GameWatchMemory, MiningBadge

__version__ = "1.0.0"
__author__ = "RustChain Community"
__wallet__ = "RTC4325af95d26d59c3ef025963656d22af638bb96b"

__all__ = [
    "GameWatchMiner",
    "main",
    "SegmentedDisplay",
    "LCDSegment",
    "SharpSM5xxEmulator",
    "GameWatchMemory",
    "MiningBadge",
]
