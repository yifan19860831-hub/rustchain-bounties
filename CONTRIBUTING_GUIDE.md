# RustChain Contribution Guide

> **Complete guide for contributing to the RustChain ecosystem**  
> **Last Updated:** March 2026

Welcome to RustChain! This guide will help you navigate the contribution process, from your first issue to earning RTC tokens.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Understanding RTC Bounties](#understanding-rtc-bounties)
3. [Finding Your First Issue](#finding-your-first-issue)
4. [Contribution Workflow](#contribution-workflow)
5. [Development Setup](#development-setup)
6. [Code Standards](#code-standards)
7. [Documentation Guidelines](#documentation-guidelines)
8. [Submitting Your Work](#submitting-your-work)
9. [Getting Paid](#getting-paid)
10. [FAQ](#faq)

---

## Quick Start

**New here? Follow these 5 steps:**

```bash
# 1. Browse open bounties
https://github.com/Scottcjn/rustchain-bounties/issues?q=is%3Aissue+is%3Aopen+label%3Abounty

# 2. Comment on an issue
"I would like to work on this"

# 3. Fork & Clone
git clone https://github.com/YOUR_USERNAME/rustchain-bounties.git

# 4. Create a branch
git checkout -b feature/your-contribution

# 5. Submit a PR
# Push your changes and open a Pull Request
```

---

## Understanding RTC Bounties

### What is RTC?

**RTC (RustChain Token)** is the native cryptocurrency of RustChain, a Proof-of-Antiquity blockchain where vintage hardware earns higher mining rewards.

- **Reference Rate:** 1 RTC = $0.10 USD
- **Payout:** On PR merge, RTC is sent to your wallet
- **Bridge:** Convert RTC → wRTC (Solana) via [bottube.ai/bridge](https://bottube.ai/bridge)
- **Trade:** Swap on [Raydium](https://raydium.io/swap/?inputMint=sol&outputMint=12TAdKXxcGf6oCv4rqDz2NkgxjyHq6HQKoxKZYGf5i4X)

### Bounty Tiers

| Tier | RTC Range | USD Value | Example Contributions |
|------|-----------|-----------|----------------------|
| **Micro** | 1-10 RTC | $0.10-$1 | Star repos, typo fixes, small docs |
| **Standard** | 20-50 RTC | $2-$5 | Features, Docker setup, monitoring tools |
| **Major** | 75-100 RTC | $7.50-$10 | SDK, CLI tools, CI pipelines |
| **Critical** | 100-200 RTC | $10-$20 | Security audits, protocol work, bridges |

### Contribution Categories

| Category | Description | Open Bounties |
|----------|-------------|---------------|
| **Community** | Star repos, share content, recruit contributors | 30+ |
| **Code** | Bug fixes, features, integrations, tests | 40+ |
| **Content** | Tutorials, articles, videos, documentation | 20+ |
| **Red Team** | Security audits, penetration testing | 6 |
| **Propagation** | Awesome-list PRs, social media | 15+ |
| **Integration** | Bridge to new chains, exchange listings | 10+ |

---

## Finding Your First Issue

### By Difficulty

- **🟢 Beginner:** [`good first issue`](https://github.com/Scottcjn/rustchain-bounties/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) - No experience required
- **🟡 Standard:** [`standard`](https://github.com/Scottcjn/rustchain-bounties/issues?q=is%3Aissue+is%3Aopen+label%3Astandard) - Some experience helpful
- **🔴 Major:** [`major`](https://github.com/Scottcjn/rustchain-bounties/issues?q=is%3Aissue+is%3Aopen+label%3Amajor) - Advanced skills needed
- **⚫ Critical:** [`critical`](https://github.com/Scottcjn/rustchain-bounties/issues?q=is%3Aissue+is%3Aopen+label%3Acritical), [`red-team`](https://github.com/Scottcjn/rustchain-bounties/issues?q=is%3Aissue+is%3Aopen+label%3Ared-team) - Expert level

### By Type

Filter issues by what you want to work on:

```
# Code contributions
is:issue is:open label:bounty label:code

# Documentation
is:issue is:open label:bounty label:documentation

# Security
is:issue is:open label:bounty label:red-team

# Community/Propagation
is:issue is:open label:bounty label:community
```

---

## Contribution Workflow

### Step 1: Claim an Issue

1. Browse [open bounties](https://github.com/Scottcjn/rustchain-bounties/issues?q=is%3Aissue+is%3Aopen+label%3Abounty)
2. Read the issue carefully
3. Comment: **"I would like to work on this"**
4. Wait for maintainer acknowledgment (optional but recommended)

> ⚠️ **Don't start working until you've commented** - prevents duplicate work!

### Step 2: Fork & Setup

```bash
# Fork on GitHub, then clone
git clone https://github.com/YOUR_USERNAME/rustchain-bounties.git
cd rustchain-bounties

# Create a feature branch
git checkout -b feature/issue-1234-short-description
```

### Step 3: Do the Work

- Follow the issue requirements exactly
- Test your changes locally
- Keep your branch focused on one issue

### Step 4: Submit

```bash
# Commit with clear message
git commit -m "feat(scope): description of changes

Closes #1234"

# Push to your fork
git push origin feature/issue-1234-short-description
```

### Step 5: Open a PR

1. Go to your fork on GitHub
2. Click "Compare & pull request"
3. Fill out the PR template
4. Reference the issue number
5. Submit!

---

## Development Setup

### General Setup

```bash
# Clone the repository
git clone https://github.com/Scottcjn/RustChain.git
cd RustChain

# Python environment (for Python components)
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

pip install -r requirements.txt

# Rust components (if applicable)
cargo build
```

### Testing Against Live Node

```bash
# Test health endpoint
curl -sk https://rustchain.org/health

# Check active miners
curl -sk https://rustchain.org/api/miners

# Get current epoch
curl -sk https://rustchain.org/epoch
```

### Live Infrastructure

| Endpoint | URL | Purpose |
|----------|-----|---------|
| Node Health | `https://rustchain.org/health` | Check node status |
| Active Miners | `https://rustchain.org/api/miners` | List of miners |
| Current Epoch | `https://rustchain.org/epoch` | Epoch info |
| Block Explorer | `https://rustchain.org/explorer` | View blocks/transactions |
| wRTC Bridge | `https://bottube.ai/bridge` | Bridge RTC to Solana |

---

## Code Standards

### Language Support

RustChain uses multiple languages:

- **Python** - Main node implementation, scripts
- **Rust** - Performance-critical components
- **JavaScript/TypeScript** - Frontend tools, extensions
- **Solidity** - Smart contracts (if applicable)

### Python Guidelines

```python
# Use type hints (Python 3.8+)
def calculate_reward(miner_id: str, epoch: int) -> float:
    """Calculate mining reward for a given epoch."""
    pass

# Follow PEP 8
# Use meaningful variable names
# Add docstrings to functions
```

### Rust Guidelines

```rust
// Use cargo fmt
// Add documentation comments
/// Calculates the proof-of-antiquity score
pub fn calculate_poa_score(hardware_age: u32) -> f64 {
    // Implementation
}

// Write tests
#[cfg(test)]
mod tests {
    #[test]
    fn test_calculate_poa_score() {
        // Test code
    }
}
```

### Commit Messages

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]
[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, no logic change
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks
- `security`: Security-related changes

**Examples:**
```
feat(bridge): add wRTC balance verification endpoint
fix(consensus): correct PoA difficulty adjustment
docs(readme): add POWER8 hardware requirements
test(api): add integration tests for mining endpoints
```

---

## Documentation Guidelines

### What Makes Good Documentation?

✅ **DO:**
- Write clear, step-by-step instructions
- Include copy-pastable commands
- Specify OS/architecture assumptions
- Define new terms at first use
- Test instructions on a fresh system
- Add troubleshooting sections

❌ **DON'T:**
- Assume prior knowledge
- Skip steps ("then just configure it")
- Leave broken links
- Use vague language ("might work", "should be fine")

### Documentation Checklist

Before submitting a docs PR:

- [ ] Instructions work exactly as written
- [ ] Commands are copy-pastable
- [ ] OS/architecture assumptions are explicit
- [ ] New terms are defined
- [ ] No broken links
- [ ] At least one example command/output included
- [ ] File/section names follow existing conventions

---

## Submitting Your Work

### PR Template

Use this template for your PR description:

```markdown
## What does this PR do?

Brief description of changes (2-3 sentences).

## Why?

Motivation and context. Link to any related issues.

## How to test?

Step-by-step instructions to verify the changes work:
1. Step one
2. Step two
3. Expected result

## Related Issues

Closes #<issue_number>

## Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Tests pass locally
- [ ] New code includes tests
- [ ] Documentation updated
```

### What Gets Merged ✅

- Code that works against the live node
- Tests that actually test something
- Documentation that humans can follow
- Security fixes with proof of concept
- Tools that make the ecosystem useful

### What Gets Rejected ❌

- AI-generated bulk PRs with no testing
- PRs that include all code from prior PRs (we track this)
- "Fixes" that break existing functionality
- Submissions that don't match bounty requirements
- Placeholder data, fake screenshots, fabricated metrics

---

## Getting Paid

### Payout Process

1. **PR Review:** Maintainer reviews within 48-72 hours
2. **Merge:** Once approved, PR is merged
3. **Wallet Address:** Maintainer requests your RTC wallet address
4. **Transfer:** RTC sent from community fund
5. **Bridge (optional):** Convert RTC → wRTC on Solana
6. **Trade:** Swap wRTC on Raydium DEX

### First Time Contributors

**Need a wallet?** Comment on any bounty issue and we'll help you set one up!

```markdown
"First time contributor - need help with wallet setup"
```

### Payout Tracking

View all payouts in the [Bounty Ledger](BOUNTY_LEDGER.md):

- **Total Paid:** 22,756+ RTC
- **Contributors Paid:** 14+
- **Available Pool:** 5,900+ RTC

---

## FAQ

### Q: Do I need experience with blockchain?

**A:** No! Many bounties are beginner-friendly. Start with `good first issue` labeled issues.

### Q: How do I get RTC tokens?

**A:** Complete a bounty → Submit PR → Get merged → Receive RTC in your wallet.

### Q: Can I work on multiple bounties?

**A:** Yes! But finish one before starting another to avoid conflicts.

### Q: What if I get stuck?

**A:** Ask in the issue comments or join our [Discord](https://discord.gg/VqVVS2CW9Q).

### Q: Is there a deadline?

**A:** Most bounties don't have strict deadlines, but communicate if you'll be delayed.

### Q: Can I suggest new bounties?

**A:** Yes! Open an issue with your proposal and bounty suggestion.

### Q: Do you accept AI-generated code?

**A:** AI-assisted is fine, but bulk AI-generated PRs without testing will be rejected.

---

## BCOS (Beacon Certified Open Source)

RustChain uses BCOS checks to keep contributions auditable and license-clean.

### Tier Requirements

- **BCOS-L1:** Normal features, refactors, non-sensitive changes
- **BCOS-L2:** Security-sensitive changes, transfer/wallet logic, consensus/rewards

### How to Comply

1. Add tier label to your PR: `BCOS-L1` or `BCOS-L2`
2. New code files must include SPDX header:
   ```python
   # SPDX-License-Identifier: MIT
   ```
3. CI will upload artifacts (SBOM, license report, hashes)

**Doc-only PRs** don't require BCOS labels.

---

## Start Mining

Don't just contribute — mine RTC while you help!

```bash
pip install clawrtc
clawrtc --wallet YOUR_NAME
```

**Vintage hardware bonus:** PowerPC G4/G5, POWER8 earn **2-2.5x** more!

---

## Getting Help

- **Discord:** [discord.gg/VqVVS2CW9Q](https://discord.gg/VqVVS2CW9Q)
- **GitHub Issues:** For bugs and feature requests
- **Discussions:** For questions and ideas
- **Email:** Check issue comments for maintainer contact

---

## Code of Conduct

We are committed to providing a friendly, safe, and welcoming environment for all.

**Expected Behavior:**
- Be respectful and inclusive
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

**Unacceptable Behavior:**
- Harassment or discrimination
- Trolling or insulting comments
- Publishing others' private information
- Other unethical or unprofessional conduct

**Enforcement:**
Violations will result in moderation actions, including temporary or permanent bans.

---

## License

By contributing to RustChain, you agree that your contributions will be licensed under the project's license (Apache 2.0).

---

<div align="center">

**Ready to start?** [Browse Open Bounties](https://github.com/Scottcjn/rustchain-bounties/issues?q=is%3Aissue+is%3Aopen+label%3Abounty)

**Questions?** [Open an Issue](https://github.com/Scottcjn/rustchain-bounties/issues/new) or [Join Discord](https://discord.gg/VqVVS2CW9Q)

🦀 **Happy Contributing!** 🦀

</div>
