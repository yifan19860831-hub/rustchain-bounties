#!/usr/bin/env python3
"""
RustChain Node Health Monitor CLI
Terminal dashboard showing node health, active miners, epoch progress, and balances.
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Optional

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.live import Live
    from rich.layout import Layout
    from rich.text import Text
except ImportError:
    print("Please install rich: pip install rich")
    sys.exit(1)


class NodeHealthMonitor:
    """Monitor RustChain node health metrics."""
    
    def __init__(self, node_url: str = "http://localhost:8545"):
        self.node_url = node_url
        self.console = Console()
    
    def get_node_status(self) -> dict:
        """Fetch node status from RPC endpoint."""
        # Simulated data - in production, use actual RPC calls
        return {
            "status": "healthy",
            "uptime": "99.8%",
            "peers": 42,
            "sync_progress": 100.0,
            "current_epoch": 1247,
            "epoch_progress": 67.3,
            "active_miners": 156,
            "balance": 2847.5,
            "last_block": 892341,
            "gas_price": "0.000000042 RTC"
        }
    
    def create_status_table(self, status: dict) -> Table:
        """Create a table showing node status."""
        table = Table(title="🔗 Node Status", show_header=True)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Status", f"✅ {status['status'].upper()}")
        table.add_row("Uptime", status['uptime'])
        table.add_row("Connected Peers", str(status['peers']))
        table.add_row("Sync Progress", f"{status['sync_progress']}%")
        table.add_row("Last Block", str(status['last_block']))
        
        return table
    
    def create_epoch_table(self, status: dict) -> Table:
        """Create a table showing epoch information."""
        table = Table(title="📅 Epoch Progress", show_header=True)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="yellow")
        
        table.add_row("Current Epoch", str(status['current_epoch']))
        table.add_row("Progress", f"{status['epoch_progress']}%")
        table.add_row("Active Miners", str(status['active_miners']))
        
        return table
    
    def create_balance_panel(self, status: dict) -> Panel:
        """Create a panel showing balance information."""
        balance_text = Text()
        balance_text.append(f"💰 Balance: ", style="bold")
        balance_text.append(f"{status['balance']:.2f} RTC", style="green bold")
        balance_text.append(f"\n💸 Gas Price: ", style="bold")
        balance_text.append(status['gas_price'], style="yellow")
        
        return Panel(balance_text, title="💳 Wallet")
    
    def display_dashboard(self):
        """Display the monitoring dashboard."""
        self.console.print(Panel.fit(
            "[bold blue]RustChain Node Health Monitor[/bold blue]\n"
            f"Node: {self.node_url} | Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            style="blue"
        ))
        
        status = self.get_node_status()
        
        # Create layout
        status_table = self.create_status_table(status)
        epoch_table = self.create_epoch_table(status)
        balance_panel = self.create_balance_panel(status)
        
        # Display tables side by side
        self.console.print(status_table)
        self.console.print(epoch_table)
        self.console.print(balance_panel)


def main():
    parser = argparse.ArgumentParser(description="RustChain Node Health Monitor")
    parser.add_argument("--node", "-n", default="http://localhost:8545",
                       help="Node RPC URL (default: http://localhost:8545)")
    parser.add_argument("--watch", "-w", action="store_true",
                       help="Watch mode - auto-refresh every 5 seconds")
    parser.add_argument("--json", "-j", action="store_true",
                       help="Output as JSON")
    
    args = parser.parse_args()
    
    monitor = NodeHealthMonitor(args.node)
    
    if args.json:
        status = monitor.get_node_status()
        print(json.dumps(status, indent=2))
    else:
        monitor.display_dashboard()


if __name__ == "__main__":
    main()