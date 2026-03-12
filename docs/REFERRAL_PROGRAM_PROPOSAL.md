# RustChain Referral Program Proposal

## Executive Summary

This proposal outlines a comprehensive referral program designed to accelerate RustChain ecosystem growth through community-driven user acquisition. The program incentivizes existing community members to refer new contributors, developers, and miners to the RustChain ecosystem.

**Program Name:** RustChain Ambassador Referral Program

**Token:** RTC (RustChain Token)

**Reference Rate:** 1 RTC = $0.10 USD

---

## Program Objectives

1. **Increase Developer Adoption**: Attract more developers to contribute to RustChain ecosystem
2. **Grow Miner Network**: Expand the decentralized mining network through referrals
3. **Community Building**: Strengthen community engagement and retention
4. **Ecosystem Expansion**: Drive traffic to RustChain, BoTTube, and related projects

---

## Referral Tiers & Rewards

### Tier 1: Community Referrals (1-5 RTC)

**Target**: General community members, social media followers

| Action | Reward (RTC) | Validation |
|--------|--------------|------------|
| Referred user stars RustChain repo | 1 RTC | GitHub API verification |
| Referred user joins Discord | 2 RTC | Discord username verification |
| Referred user comments on first issue | 1 RTC | GitHub activity check |
| **Total per referral** | **4 RTC** | |

### Tier 2: Contributor Referrals (5-25 RTC)

**Target**: Active contributors, content creators

| Action | Reward (RTC) | Validation |
|--------|--------------|------------|
| Referred user completes first bounty (1-5 RTC value) | 5 RTC | Bounty completion verification |
| Referred user completes first bounty (5-25 RTC value) | 10 RTC | Bounty completion verification |
| Referred user submits first merged PR | 15 RTC | PR merge verification |
| Referred user creates tutorial/content | 25 RTC | Content review & approval |

### Tier 3: Developer/Miner Referrals (25-100 RTC)

**Target**: Core developers, node operators, miners

| Action | Reward (RTC) | Validation |
|--------|--------------|------------|
| Referred user sets up mining node | 25 RTC | Node verification on network |
| Referred user runs node for 30 days | 50 RTC | Uptime verification |
| Referred user contributes core feature | 75 RTC | Feature merge & deployment |
| Referred user becomes maintainer | 100 RTC | Maintainer status grant |

---

## Referral Tracking Mechanism

### Method 1: GitHub Referral Links

```
https://github.com/Scottcjn/RustChain?referral=<referrer_username>
```

- Referrers share personalized links
- System tracks first-time visitors who star/fork/engage
- Automated validation via GitHub API

### Method 2: Discord Referral Codes

```
Discord Invite: discord.gg/VqVVS2CW9Q?ref=<referrer_username>
```

- Custom referral codes for Discord invites
- Bot tracks new member referrals
- Weekly reward distribution

### Method 3: Manual Claim System

For referrals that cannot be tracked automatically:

```markdown
## Referral Claim Template

**Referrer**: @github_username
**Referee**: @referred_username
**Action Completed**: [Star/Discord/Bounty/PR/Node]
**Proof Link**: [GitHub/Discord/Network verification]
**Requested Reward**: X RTC
```

---

## Reward Distribution Schedule

| Frequency | Distribution Day | Minimum Claim |
|-----------|------------------|---------------|
| Weekly | Every Friday | 5 RTC |
| Monthly | 1st of month | 20 RTC |
| Milestone | Upon verification | 50+ RTC |

### Payment Process

1. Referrer submits claim via issue template
2. Maintainer verifies within 48 hours
3. RTC transferred to referrer's wallet
4. Transaction recorded in BOUNTY_LEDGER.md

---

## Anti-Abuse Measures

### Detection Mechanisms

1. **Duplicate Accounts**: Check for newly created GitHub accounts with no activity
2. **Self-Referrals**: Cross-reference wallet addresses and Discord IDs
3. **Bot Activity**: Monitor for automated starring patterns
4. **Time-Based Limits**: Maximum 10 referrals per user per week (Tier 1)

### Penalties

- **First Violation**: Warning and claim rejection
- **Second Violation**: 7-day suspension from referral program
- **Third Violation**: Permanent ban and forfeiture of pending rewards

---

## Program Budget & Sustainability

### Initial Allocation

- **Phase 1 (Months 1-3)**: 500 RTC reserve
- **Phase 2 (Months 4-6)**: 1000 RTC reserve (based on Phase 1 performance)
- **Phase 3 (Months 7-12)**: 2000 RTC reserve (scaled by ecosystem growth)

### ROI Metrics

- **Cost per Acquired Developer**: Target < 50 RTC
- **Cost per Active Miner**: Target < 100 RTC
- **Referral Conversion Rate**: Target > 30%
- **Retention Rate (90 days)**: Target > 60%

---

## Implementation Timeline

### Phase 1: Foundation (Week 1-2)

- [ ] Create referral tracking infrastructure
- [ ] Set up Discord bot for referral code management
- [ ] Design claim templates and documentation
- [ ] Train maintainers on validation process

### Phase 2: Beta Launch (Week 3-4)

- [ ] Invite 20 existing community members as beta referrers
- [ ] Test tracking mechanisms with controlled group
- [ ] Gather feedback and iterate on process
- [ ] Refine anti-abuse detection rules

### Phase 3: Public Launch (Month 2)

- [ ] Announce program on Discord, Twitter, GitHub
- [ ] Open referral program to all community members
- [ ] Weekly reward distributions begin
- [ ] Monthly performance reports published

### Phase 4: Optimization (Month 3+)

- [ ] Analyze conversion metrics and adjust rewards
- [ ] Introduce seasonal bonus campaigns
- [ ] Expand to additional platforms (Telegram, Reddit)
- [ ] Integrate with RustChain dashboard for self-service tracking

---

## Success Metrics

### Key Performance Indicators (KPIs)

| Metric | Baseline | Target (3 months) | Target (12 months) |
|--------|----------|-------------------|--------------------|
| New GitHub Stars | 97 | 300 | 1000 |
| Active Contributors | 14 | 50 | 200 |
| Mining Nodes | Current | +50 | +200 |
| Discord Members | Current | +500 | +2000 |
| Bounties Completed/Month | Current | 2x | 5x |

### Reporting

- **Weekly**: Referral claims processed, RTC distributed
- **Monthly**: KPI dashboard, top referrers leaderboard
- **Quarterly**: Program review, reward structure adjustments

---

## Top Referrer Leaderboard (Gamification)

### Monthly Rewards

| Rank | Bonus (RTC) | Badge |
|------|-------------|-------|
| #1 | 50 RTC | 🥇 RustChain Ambassador |
| #2 | 30 RTC | 🥈 Community Leader |
| #3 | 20 RTC | 🥉 Growth Champion |
| Top 10 | 5 RTC each | 🏅 Referral Master |

### Achievement Badges

- **First Blood**: First successful referral (1 RTC bonus)
- **Centurion**: 100 successful referrals (special NFT badge)
- **Developer Magnet**: 10 developer referrals (exclusive Discord role)
- **Node Recruiter**: 25 mining nodes referred (featured on website)

---

## Integration with Existing Programs

### Synergy with Current Bounties

1. **Referral + Bounty Stacking**: Referrers can also earn bounties directly
2. **Multiplier Effect**: Referred users' bounty completions count toward referrer milestones
3. **Cross-Promotion**: Referral program promoted within bounty issues

### Alignment with RustChain Goals

- Supports Proof-of-Antiquity mission by expanding miner network
- Drives quality contributions over quantity (tiered rewards)
- Builds sustainable community-led growth engine

---

## Risk Assessment

### Identified Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Abuse/fraud | Medium | High | Multi-layer verification, limits |
| Budget overrun | Low | Medium | Phased rollout, monthly caps |
| Low participation | Medium | Medium | Marketing push, incentive adjustments |
| Poor retention | Medium | High | Focus on quality referrals, follow-up |

### Contingency Plans

- **Budget Cap**: Monthly spending limit of 200 RTC in Phase 1
- **Program Pause**: Ability to suspend if abuse detected
- **Reward Adjustment**: Dynamic tuning based on ROI metrics

---

## Technical Requirements

### Infrastructure Needs

1. **GitHub Integration**: API access for tracking stars, PRs, issues
2. **Discord Bot**: Custom referral code generation and tracking
3. **Database**: Simple ledger for referral relationships and claims
4. **Dashboard**: Optional web interface for referrers to track progress

### Estimated Development Effort

- **Discord Bot**: 20-30 hours (can use existing bounty bot framework)
- **Tracking Database**: 10-15 hours (simple SQLite or Airtable)
- **Documentation**: 5-10 hours (templates, guides, FAQs)
- **Total**: ~40-55 hours (8-12 RTC at standard developer rates)

---

## Budget Request

### Initial Setup Costs

| Item | Cost (RTC) |
|------|------------|
| Development (Discord bot + tracking) | 12 RTC |
| Documentation & templates | 3 RTC |
| Phase 1 reward reserve | 500 RTC |
| Marketing materials | 5 RTC |
| **Total Phase 1** | **520 RTC** |

### Ongoing Monthly Budget

| Item | Cost (RTC/month) |
|------|------------------|
| Reward distributions (estimated) | 150-300 RTC |
| Leaderboard bonuses | 100 RTC |
| Administrative overhead | 20 RTC |
| **Total Monthly** | **270-420 RTC** |

---

## Conclusion

The RustChain Referral Program provides a scalable, community-driven growth mechanism that aligns incentives between existing members and newcomers. By offering tiered rewards based on referral quality and implementing robust anti-abuse measures, the program can sustainably expand the RustChain ecosystem while maintaining high contributor quality standards.

**Recommended Next Steps:**

1. ✅ Approve proposal and allocate Phase 1 budget (520 RTC)
2. ✅ Assign developer to build tracking infrastructure (2 weeks)
3. ✅ Recruit 20 beta referrers from existing community
4. ✅ Launch beta program and gather metrics (2 weeks)
5. ✅ Iterate and launch publicly based on beta results

---

## Appendix A: Claim Template

```markdown
# Referral Reward Claim

## Referrer Information
- **GitHub Username**: @your_username
- **Discord Username**: your_discord#1234
- **RTC Wallet Address**: 0x...

## Referral Details
- **Referred User**: @referred_username
- **Referral Date**: YYYY-MM-DD
- **Referral Link/Code**: [link or code used]

## Action Completed
- [ ] Starred RustChain repo (1 RTC)
- [ ] Joined Discord (2 RTC)
- [ ] First issue comment (1 RTC)
- [ ] Completed bounty (5-25 RTC)
- [ ] Merged PR (15 RTC)
- [ ] Set up mining node (25 RTC)
- [ ] Other: ____________

## Proof Links
- GitHub profile: https://github.com/...
- Discord join confirmation: ...
- Transaction/network verification: ...

## Total Claimed: X RTC

## Checklist
- [ ] I have verified that the referred user completed the claimed actions
- [ ] This is not a duplicate claim
- [ ] I understand that fraudulent claims result in program ban
```

---

## Appendix B: FAQ

**Q: Can I refer myself with alternate accounts?**
A: No. Self-referrals are prohibited and will result in permanent ban.

**Q: How long does validation take?**
A: Most claims are validated within 48 hours. Complex claims (nodes, core features) may take up to 1 week.

**Q: Can I refer the same user multiple times?**
A: Yes, for different actions. Example: You can earn rewards when they star, join Discord, AND complete a bounty.

**Q: What if my referral leaves the community?**
A: Rewards are based on completed actions, not long-term retention. However, retention bonuses may be added in Phase 3.

**Q: Is there a limit to how many users I can refer?**
A: Tier 1 (community) referrals are limited to 10 per week. Tier 2 and 3 have no limits but undergo stricter validation.

---

**Proposal Author**: [Your GitHub Username]
**Date**: 2026-03-12
**Contact**: [Discord/Email]
**Related Issue**: #1635
