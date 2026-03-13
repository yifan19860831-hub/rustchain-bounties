#!/usr/bin/env python3
"""
Basic API Demo - Demonstrates RustChain and BoTTube API usage
"""

from __future__ import annotations

import sys
from typing import Any

sys.path.insert(0, '.')

from rustchain_client import RustChainClient, BoTTubeClient


def print_section_header(text: str) -> None:
    """Print a formatted section header."""
    print("=" * 60)
    print(text)
    print("=" * 60)


def print_health_info(health: dict[str, Any]) -> None:
    """Print node health information."""
    print("\n1. Checking node health...")
    print(f"   OK: {health.get('ok')}")
    print(f"   Version: {health.get('version')}")
    uptime_hours: float = health.get('uptime_s', 0) / 3600
    print(f"   Uptime: {uptime_hours:.1f} hours")


def print_epoch_info(epoch: dict[str, Any]) -> None:
    """Print epoch information."""
    print("\n2. Getting epoch info...")
    print(f"   Epoch: {epoch.get('epoch')}")
    print(f"   Slot: {epoch.get('slot')}")
    print(f"   Blocks/Epoch: {epoch.get('blocks_per_epoch')}")
    total_supply: int = epoch.get('total_supply_rtc', 0)
    print(f"   Total Supply: {total_supply:,} RTC")
    print(f"   Epoch POT: {epoch.get('epoch_pot')} RTC")


def print_miners_info(miners: list[dict[str, Any]]) -> None:
    """Print active miners information."""
    print("\n3. Listing active miners...")
    print(f"   Active miners: {len(miners)}")
    for m in miners[:3]:
        miner_id: str = m.get('miner', 'unknown')
        hw_type: str = m.get('hardware_type', 'unknown')
        arch: str = m.get('device_arch', 'unknown')
        print(f"   - {miner_id}: {hw_type} ({arch})")


def print_balance_info(wallet: str, balance: Any) -> None:
    """Print wallet balance information."""
    print("\n4. Checking balance...")
    print(f"   Wallet: {wallet}")
    print(f"   Balance: {balance}")


def print_bottube_stats() -> None:
    """Print BoTTube statistics."""
    print("\n5. Getting BoTTube stats...")
    bt = BoTTubeClient()
    try:
        stats: dict[str, Any] = bt.get_stats()
        print(f"   Stats: {stats}")
    except Exception as e:
        print(f"   (BoTTube API not available: {e})")


def main() -> None:
    """Main demo function."""
    print_section_header("RustChain API Demo")
    
    # Initialize clients
    rc: RustChainClient = RustChainClient()
    
    # 1. Health Check
    health: dict[str, Any] = rc.health()
    print_health_info(health)
    
    # 2. Epoch Info
    epoch: dict[str, Any] = rc.get_epoch()
    print_epoch_info(epoch)
    
    # 3. Miners
    miners: list[dict[str, Any]] = rc.get_miners()
    print_miners_info(miners)
    
    # 4. Balance (example wallet)
    wallet: str = "aric-saxp-alpha"
    balance: Any = rc.get_balance(wallet)
    print_balance_info(wallet, balance)
    
    # 5. BoTTube Stats
    print_bottube_stats()
    
    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
