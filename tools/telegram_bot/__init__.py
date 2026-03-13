"""
RustChain Telegram Bot Package

A Telegram bot for RustChain community that provides quick access to network information.

Commands:
    /balance <wallet> - Check RTC balance for any wallet
    /miners - List all active miners on the network
    /price - Current wRTC price information
    /health - Node health status
    /epoch - Current epoch information

API: https://rustchain.org
"""

from .bot import main, start_command, balance_command, miners_command, price_command, health_command, epoch_command

__version__ = "1.0.0"
__author__ = "RustChain Community"
__all__ = [
    "main",
    "start_command",
    "balance_command",
    "miners_command",
    "price_command",
    "health_command",
    "epoch_command",
]
