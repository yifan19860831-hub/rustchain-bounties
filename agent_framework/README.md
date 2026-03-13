# RustChain Agent Framework

Autonomous AI agent framework for bounty hunting in the RustChain ecosystem.

## 🤖 What is RayBot?

RayBot is an autonomous AI agent that discovers, claims, and completes bounties in the RustChain ecosystem. It operates on a "result-first" basis, prioritizing monetizable outcomes with minimal human intervention.

## 📁 Structure

```
agent_framework/
├── meat_finder.py      # Bounty discovery engine
├── bounty_claimer.py   # Automated claim handler
├── WORKFLOW.md         # Autonomous workflow documentation
├── README.md           # This file
└── __init__.py         # Package initialization
```

## 🔧 Components

### Meat Finder (`meat_finder.py`)

Scans for profitable bounties across:
- GitHub Issues (labeled `bounty`)
- Farcaster (Bountycaster)
- X (Twitter)

Ranks tasks by:
- Capability fit (Python/Web/Docs)
- Reward-to-effort ratio
- Competition level

### Bounty Claimer (`bounty_claimer.py`)

Handles automated claim process:
- Posts claim comments on GitHub issues
- Provides Miner ID for settlement
- Outlines implementation plans

## 🌊 Autonomous Loop

1. **Discovery** - Scan for new bounties
2. **Assessment** - Evaluate capability fit
3. **Claim** - Post intent to work
4. **Implementation** - Develop solution
5. **Submission** - Push code and open PR

## 📊 Track Record

| # | Repo | PR | Reward | Status |
|---|------|----|--------|--------|
| #132 | BoTTube | PR #124 | 60 RTC | ✅ Merged/Paid |
| #79 | BoTTube | PR #117 | 75 RTC | ✅ Merged/Paid |
| #122 | BoTTube | PR #125 | 5 RTC | ✅ Merged/Paid |

## 🔒 Safety

- No private key handling
- Human oversight for withdrawals
- Hardware attestation enabled

## 📖 Documentation

- [Workflow Guide](WORKFLOW.md) - Detailed autonomous loop documentation

## 🚀 Usage

```python
from agent_framework import MeatFinder, BountyClaimer

finder = MeatFinder()
bounties = finder.scan_github("Scottcjn/rustchain-bounties")

claimer = BountyClaimer(miner_id="your_miner_id")
claimer.claim(bounties[0])
```

## 📝 License

MIT License - RustChain Community
