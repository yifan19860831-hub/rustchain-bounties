#!/usr/bin/env python3
"""
GitHub RTC Tip Bot
Listens for /tip, /balance, /leaderboard, /register commands in GitHub comments.
"""

from __future__ import annotations

import os
import re
import json
import time
from typing import Any

import requests
from github import Github

# Configuration
GITHUB_TOKEN: str | None = os.getenv("GITHUB_TOKEN")
RUSTCHAIN_NODE: str = os.getenv("RUSTCHAIN_NODE", "https://50.28.86.131")
RUSTCHAIN_ADMIN_KEY: str = os.getenv("RUSTCHAIN_ADMIN_KEY", "")

# In-memory storage for demo (use database in production)
registered_wallets: dict[str, str] = {}  # github_username -> wallet_name
tip_ledger: list[tuple[str, str, float, str, float]] = []  # [(from, to, amount, memo, timestamp)]

def check_balance(wallet_name: str) -> dict[str, Any]:
    """Check RTC balance for a wallet."""
    try:
        r: requests.Response = requests.get(
            f"{RUSTCHAIN_NODE}/wallet/balance",
            params={"miner_id": wallet_name},
            timeout=10,
            verify=False
        )
        return r.json()  # type: ignore[no-any-return]
    except Exception as e:
        return {"error": str(e)}


def register_wallet(github_user: str, wallet_name: str) -> bool:
    """Register a wallet for a GitHub user."""
    registered_wallets[github_user] = wallet_name
    return True


def process_tip(
    from_user: str,
    to_wallet: str,
    amount: float,
    memo: str = ""
) -> dict[str, Any]:
    """
    Process a tip transfer.
    
    Note: Requires admin key for actual transfers.
    
    Args:
        from_user: Sender's GitHub username
        to_wallet: Recipient's wallet name
        amount: Amount of RTC to tip
        memo: Optional memo for the tip
        
    Returns:
        Status dictionary with result
    """
    # Validate recipient has registered wallet
    recipient: str | None = None
    for user, wallet in registered_wallets.items():
        if wallet == to_wallet:
            recipient = user
            break
    
    if not recipient:
        return {
            "status": "error",
            "message": f"Wallet {to_wallet} not registered. Use /register WALLET_NAME first."
        }
    
    # Queue the tip (in production, call /wallet/transfer API with admin key)
    timestamp: float = time.time()
    tip_ledger.append((from_user, to_wallet, amount, memo, timestamp))
    
    return {
        "status": "queued",
        "amount": amount,
        "to": to_wallet,
        "from": from_user,
        "memo": memo
    }


def get_leaderboard() -> list[tuple[str, float]]:
    """Get top tipped contributors."""
    totals: dict[str, float] = {}
    for frm, to, amount, _, _ in tip_ledger:
        totals[to] = totals.get(to, 0.0) + amount
    
    sorted_users: list[tuple[str, float]] = sorted(
        totals.items(), key=lambda x: x[1], reverse=True
    )
    return sorted_users[:10]


def parse_command(body: str) -> tuple[str | None, dict[str, Any]]:
    """
    Parse command from comment body.
    
    Args:
        body: Comment body text
        
    Returns:
        Tuple of (command_name, arguments_dict)
    """
    body = body.strip()
    
    # /tip @user AMOUNT RTC [memo]
    tip_match = re.match(
        r"^\/tip\s+@(\w+)\s+(\d+(?:\.\d+)?)\s*RTC\s*(.*)?$", body, re.I
    )
    if tip_match:
        return ("tip", {
            "recipient": tip_match.group(1),
            "amount": float(tip_match.group(2)),
            "memo": tip_match.group(3) or ""
        })
    
    # /balance [wallet]
    if body.lower().startswith("/balance"):
        wallet: str = body.replace("/balance", "").strip()
        return ("balance", {"wallet": wallet})
    
    # /register WALLET_NAME
    reg_match = re.match(r"^\/register\s+(\w+)$", body, re.I)
    if reg_match:
        return ("register", {"wallet": reg_match.group(1)})
    
    # /leaderboard
    if body.lower() == "/leaderboard":
        return ("leaderboard", {})
    
    return (None, {})


def handle_comment(comment_data: dict[str, Any]) -> str | None:
    """
    Handle a comment and return response.
    
    Args:
        comment_data: GitHub comment data dictionary
        
    Returns:
        Response message string or None if not a command
    """
    body: str = comment_data.get("body", "")
    user: str = comment_data.get("user", {}).get("login", "unknown")
    
    cmd: str | None
    args: dict[str, Any]
    cmd, args = parse_command(body)
    
    if cmd == "tip":
        result: dict[str, Any] = process_tip(
            user, args["recipient"], args["amount"], args["memo"]
        )
        if result["status"] == "queued":
            return (
                f"✅ Queued: {result['amount']} RTC → {result['to']}\n"
                f"From: {user} | Memo: {result['memo']}\n"
                f"Status: Pending (confirms in 24h)"
            )
        else:
            return f"❌ Error: {result.get('message', 'Unknown error')}"
    
    elif cmd == "balance":
        wallet: str = args.get("wallet") or user
        bal: dict[str, Any] = check_balance(wallet)
        if "error" in bal:
            return f"❌ Error checking balance: {bal['error']}"
        return f"💰 Balance for {wallet}: {bal.get('amount_rtc', 0)} RTC"
    
    elif cmd == "register":
        register_wallet(user, args["wallet"])
        return f"✅ Wallet registered: {args['wallet']} for user {user}"
    
    elif cmd == "leaderboard":
        leaders: list[tuple[str, float]] = get_leaderboard()
        if not leaders:
            return "📊 No tips yet!"
        
        lines: list[str] = ["🏆 Top Tipped Contributors:"]
        for i, (wallet, total) in enumerate(leaders, 1):
            lines.append(f"{i}. {wallet}: {total} RTC")
        return "\n".join(lines)
    
    return None  # Not a command we handle

# Example usage
if __name__ == "__main__":
    # Demo
    print("=== GitHub RTC Tip Bot ===")
    
    # Register some wallets
    register_wallet("Scottcjn", "scottcjn")
    register_wallet("testuser", "testwallet")
    
    # Process some tips
    print(process_tip("Scottcjn", "testwallet", 5.0, "Great PR!"))
    
    # Check balance
    print(check_balance("testwallet"))
    
    # Get leaderboard
    print(get_leaderboard())
