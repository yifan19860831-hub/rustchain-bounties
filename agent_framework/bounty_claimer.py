#!/usr/bin/env python3
"""GitHub bounty claimer for autonomous agents."""

from __future__ import annotations

import subprocess
import sys
from typing import Optional


def claim_bounty(
    repo: str,
    issue_number: int,
    miner_id: str,
    plan: str
) -> bool:
    """
    Autonomously claims a bounty using the GitHub CLI.
    
    Args:
        repo: Repository name (e.g., "Scottcjn/rustchain-bounties")
        issue_number: GitHub issue number
        miner_id: Miner identifier
        plan: Implementation plan description
        
    Returns:
        True if claim was successful, False otherwise
    """
    body: str = f"""**Claim**
- **Agent**: RayBot (Autonomous AI)
- **Miner ID**: {miner_id}
- **Plan**: {plan}
- **Status**: Starting implementation now.
"""
    
    cmd: list[str] = [
        "gh", "issue", "comment", str(issue_number),
        "-R", repo,
        "-b", body
    ]
    
    try:
        result: subprocess.CompletedProcess[str] = subprocess.run(
            cmd, capture_output=True, text=True, check=True
        )
        print(f"✅ Successfully claimed bounty {repo}#{issue_number}")
        print(f"🔗 URL: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to claim bounty: {e.stderr}")
        return False


def main() -> None:
    """Main entry point with argument parsing."""
    if len(sys.argv) < 5:
        print("Usage: python3 bounty_claimer.py <repo> <issue_number> <miner_id> <plan>")
        sys.exit(1)
    
    repo: str = sys.argv[1]
    issue_number: int = int(sys.argv[2])
    miner_id: str = sys.argv[3]
    plan: str = sys.argv[4]
    
    success: bool = claim_bounty(repo, issue_number, miner_id, plan)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
