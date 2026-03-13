# RustChain Security Incident Response Runbook

**Version:** 1.0  
**Created:** 2026-03-12  
**Author:** 牛 (AI Agent)  
**Bounty:** #1689 (3 RTC)  
**Classification:** Internal Use

---

## Table of Contents

1. [Overview](#overview)
2. [Incident Severity Levels](#incident-severity-levels)
3. [Response Team Roles](#response-team-roles)
4. [Incident Response Workflow](#incident-response-workflow)
5. [Security Scenario Playbooks](#security-scenario-playbooks)
6. [Communication Templates](#communication-templates)
7. [Post-Incident Review](#post-incident-review)
8. [Appendix](#appendix)

---

## Overview

### Purpose

This runbook provides step-by-step procedures for detecting, responding to, and recovering from security incidents affecting the RustChain ecosystem, including:

- RustChain blockchain nodes
- BoTTube platform
- Beacon Atlas
- Smart contracts and wallet infrastructure
- User data and credentials

### Scope

**In Scope:**
- Production infrastructure (nodes, APIs, databases)
- User accounts and wallets
- Smart contracts
- GitHub repositories
- Community channels (Discord, social media)

**Out of Scope:**
- Personal developer environments
- Testnet incidents (unless they affect mainnet)
- Third-party services outside RustChain control

### Guiding Principles

1. **Speed over perfection** - Rapid containment minimizes damage
2. **Evidence first** - Document everything before making changes
3. **Communicate clearly** - Keep stakeholders informed without causing panic
4. **Learn and improve** - Every incident is a learning opportunity

---

## Incident Severity Levels

| Level | Name | Response Time | Examples |
|-------|------|---------------|----------|
| **P0** | Critical | Immediate (<15 min) | Active exploit, funds at risk, full service outage |
| **P1** | High | <1 hour | Partial service outage, potential data leak, suspicious activity |
| **P2** | Medium | <4 hours | Bug with security implications, phishing attempts |
| **P3** | Low | <24 hours | Minor vulnerabilities, policy violations |

### Severity Decision Matrix

```
Is user funds/data at immediate risk?
├─ YES → P0
└─ NO → Is service degraded or unavailable?
    ├─ YES (full outage) → P0
    ├─ YES (partial) → P1
    └─ NO → Is there potential for future exploitation?
        ├─ YES → P2
        └─ NO → P3
```

---

## Response Team Roles

| Role | Responsibility | Backup |
|------|----------------|--------|
| **Incident Commander (IC)** | Overall coordination, decision-making | Lead Developer |
| **Technical Lead** | Technical investigation and remediation | Senior Engineer |
| **Communications Lead** | Internal/external communications | Community Manager |
| **Security Analyst** | Forensics, evidence collection | External Consultant |
| **Legal/Compliance** | Regulatory considerations, liability | Founder |

### Contact Escalation

```
P0: Page ALL team members immediately via phone/SMS
P1: Page IC + Technical Lead, notify others via Slack/Discord
P2: Notify IC during business hours, page if no response in 1h
P3: Create GitHub issue, discuss in next team sync
```

---

## Incident Response Workflow

### Phase 1: Detection & Triage (0-30 minutes)

**Step 1.1: Identify the Incident**
- [ ] Receive alert or report (automated monitoring, user report, team member)
- [ ] Log initial details in incident tracking system
- [ ] Assign preliminary severity level

**Step 1.2: Initial Assessment**
- [ ] Verify the incident is real (not a false positive)
- [ ] Identify affected systems/users
- [ ] Determine if incident is ongoing or historical

**Step 1.3: Activate Response**
- [ ] For P0/P1: Page relevant team members
- [ ] Create dedicated communication channel (Slack/Discord war room)
- [ ] Assign Incident Commander

**Step 1.4: Initial Documentation**
- [ ] Create incident timeline (start with T=0)
- [ ] Record all known facts
- [ ] Note what is NOT known

### Phase 2: Containment (30 min - 2 hours)

**Step 2.1: Short-term Containment**
- [ ] Isolate affected systems (do NOT power off - preserve evidence)
- [ ] Block malicious IPs/accounts
- [ ] Rotate compromised credentials
- [ ] Enable enhanced logging

**Step 2.2: Assess Impact**
- [ ] How many users affected?
- [ ] What data/systems compromised?
- [ ] Is the attack vector still active?

**Step 2.3: Long-term Containment**
- [ ] Apply temporary fixes to allow service restoration
- [ ] Prepare clean systems for recovery
- [ ] Document all containment actions

### Phase 3: Eradication (2-24 hours)

**Step 3.1: Root Cause Analysis**
- [ ] Identify how the attacker gained access
- [ ] Determine what vulnerabilities were exploited
- [ ] Find all compromised assets

**Step 3.2: Remove Threat**
- [ ] Delete malware/backdoors
- [ ] Patch vulnerabilities
- [ ] Remove attacker access

**Step 3.3: Verify Eradication**
- [ ] Scan systems for remaining threats
- [ ] Verify patches are effective
- [ ] Confirm attacker access is revoked

### Phase 4: Recovery (24-72 hours)

**Step 4.1: Restore Services**
- [ ] Restore from clean backups (if needed)
- [ ] Gradually bring systems online
- [ ] Monitor closely for re-infection

**Step 4.2: Validate Functionality**
- [ ] Test all affected features
- [ ] Verify data integrity
- [ ] Confirm monitoring is active

**Step 4.3: Lift Containment**
- [ ] Remove temporary restrictions
- [ ] Restore normal access levels
- [ ] Notify users (if required)

### Phase 5: Post-Incident (1-2 weeks)

**Step 5.1: Lessons Learned**
- [ ] Conduct post-mortem meeting within 5 business days
- [ ] Document what went well
- [ ] Document what could be improved
- [ ] Create action items with owners and deadlines

**Step 5.2: Update Procedures**
- [ ] Update this runbook based on learnings
- [ ] Implement new monitoring/alerting
- [ ] Schedule training if needed

**Step 5.3: Follow-up**
- [ ] Review action item completion
- [ ] Share anonymized learnings with community (if appropriate)
- [ ] Recognize team members who responded effectively

---

## Security Scenario Playbooks

### Playbook 1: Unauthorized Access to Node

**Scenario:** Attacker gains SSH or API access to a RustChain node

**Severity:** P0 (if production node)

**Immediate Actions:**
1. **DO NOT** power off the node (preserve evidence)
2. Disconnect node from network (disable network interface, don't shutdown)
3. Rotate all credentials (SSH keys, API keys, database passwords)
4. Check other nodes for similar compromise

**Investigation:**
```bash
# Check recent logins
last -a
who -a
cat /var/log/auth.log | grep -i "accepted"

# Check for suspicious processes
ps auxf
netstat -tulpn

# Check for unauthorized SSH keys
cat ~/.ssh/authorized_keys
cat /root/.ssh/authorized_keys

# Check cron jobs
crontab -l
ls -la /etc/cron.*
```

**Recovery:**
1. Rebuild node from known-good image
2. Restore data from backup (verify backup integrity first)
3. Reconnect to network
4. Monitor for 48 hours

---

### Playbook 2: Smart Contract Vulnerability

**Scenario:** Critical vulnerability discovered in RustChain smart contracts

**Severity:** P0 (if exploitable), P1 (if theoretical)

**Immediate Actions:**
1. Assess exploitability:
   - Can funds be drained?
   - Can contract be paused?
   - Is there a known exploit in the wild?

2. If actively exploited:
   - Pause contract (if pause function exists)
   - Notify affected users immediately
   - Contact law enforcement (if funds stolen)

3. If not yet exploited:
   - Prepare patch silently
   - Plan coordinated disclosure
   - Consider bug bounty for reporter

**Communication:**
- **Internal:** Full technical details in private channel
- **External (if exploited):** "We are aware of an issue and are investigating"
- **External (post-fix):** Detailed disclosure with credit to reporter

---

### Playbook 3: DDoS Attack

**Scenario:** RustChain services under distributed denial-of-service attack

**Severity:** P1 (degraded service), P0 (full outage)

**Immediate Actions:**
1. Identify attack type:
   - Volumetric (bandwidth saturation)
   - Application layer (HTTP flood)
   - Protocol attack (SYN flood)

2. Enable DDoS mitigation:
   - Activate cloud provider DDoS protection
   - Enable rate limiting
   - Deploy WAF rules

3. Scale infrastructure:
   - Add capacity if possible
   - Enable CDN caching
   - Implement geographic blocking (if attack is region-specific)

**Monitoring:**
```bash
# Check traffic patterns
iftop -P
nethogs

# Check for specific attack signatures
tcpdump -n 'tcp[tcpflags] & tcp-syn != 0'
tail -f /var/log/nginx/access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head -20
```

---

### Playbook 4: Data Breach

**Scenario:** User data (emails, wallets, personal info) potentially compromised

**Severity:** P0 (financial data), P1 (personal data)

**Immediate Actions:**
1. Contain the breach:
   - Identify and close the vulnerability
   - Revoke compromised access tokens
   - Preserve evidence for forensics

2. Assess scope:
   - How many users affected?
   - What data types exposed?
   - Duration of exposure?

3. Legal obligations:
   - Determine notification requirements (GDPR, CCPA, etc.)
   - Consult legal counsel
   - Prepare regulatory filings if required

**User Notification Template:**
```
Subject: Important Security Notice from RustChain

Dear [User],

We are writing to inform you of a security incident that may have affected 
your personal information.

What happened: [Brief, clear description]
What information was involved: [Specific data types]
What we are doing: [Remediation steps]
What you can do: [Recommended user actions]

We sincerely apologize for any inconvenience this may cause.

For more information: [Link to FAQ]
Contact: [Security team email]

Sincerely,
The RustChain Team
```

---

### Playbook 5: Phishing/Social Engineering

**Scenario:** Attackers impersonating RustChain team to steal credentials

**Severity:** P2 (attempted), P1 (successful)

**Immediate Actions:**
1. Document the attack:
   - Screenshot phishing emails/messages
   - Record fake URLs
   - Save sender information

2. Takedown:
   - Report to hosting provider
   - Submit to Google Safe Browsing
   - Report to domain registrar

3. User notification:
   - Post warning on official channels
   - Email users if targeted list is known
   - Never ask users to click links in security emails

**Prevention:**
- Publish official communication channels prominently
- Implement DMARC, SPF, DKIM for email
- Educate community regularly

---

### Playbook 6: Private Key Compromise

**Scenario:** Founder/team wallet private key potentially compromised

**Severity:** P0

**Immediate Actions:**
1. **DO NOT** announce publicly yet (gives attacker time to act)
2. Immediately transfer funds to new secure wallet
3. Revoke any DeFi approvals or staking positions
4. Notify exchanges to freeze suspicious transfers

**Recovery:**
1. Generate new keys on air-gapped device
2. Create new multi-sig wallet (if applicable)
3. Update all public addresses
4. Announce address change through verified channels only

---

### Playbook 7: GitHub Repository Compromise

**Scenario:** Attacker gains write access to RustChain GitHub repos

**Severity:** P0 (if code can be modified), P1 (if read-only access)

**Immediate Actions:**
1. Revoke all access tokens and OAuth apps
2. Enable required 2FA for all collaborators
3. Review recent commits for malicious code
4. Check for modified GitHub Actions workflows

**Investigation:**
```markdown
Checklist:
- [ ] Review last 50 commits for suspicious changes
- [ ] Check for new deploy keys
- [ ] Audit OAuth app permissions
- [ ] Review GitHub Actions secrets
- [ ] Check for modified webhook URLs
```

**Recovery:**
1. Remove malicious code
2. Rotate all secrets and tokens
3. Audit all third-party integrations
4. Consider making repo private temporarily

---

### Playbook 8: Insider Threat

**Scenario:** Team member or contractor acting maliciously

**Severity:** P1 (suspected), P0 (confirmed)

**Immediate Actions:**
1. **DO NOT** confront the individual yet
2. Preserve evidence quietly
3. Revoke access gradually (avoid tipping off)
4. Consult legal counsel before any action

**Investigation:**
- Review access logs
- Check for unusual data transfers
- Interview other team members
- Engage external forensics if needed

**Important:** Handle with extreme care to avoid wrongful accusation claims

---

## Communication Templates

### Internal Alert (P0/P1)

```
🚨 SECURITY INCIDENT ALERT 🚨

Severity: P0/P1
Time Detected: [timestamp]
Affected Systems: [list]
Status: [Investigating/Contained/Resolved]

War Room: [Slack/Discord channel link]
Incident Commander: [name]

All hands on deck. Acknowledge receipt.
```

### External Status Update

```
**Service Update**

We are currently investigating an issue affecting [service]. 

Our team is actively working on a resolution. We will provide updates 
every [30 minutes/hour] until resolved.

Current Status: [Investigating/Identified/Fixing/Monitoring]
Next Update: [timestamp]

Thank you for your patience.
```

### Post-Incident Summary

```
**Incident Resolution Summary**

Issue: [brief description]
Duration: [start time] - [end time]
Impact: [users/systems affected]

Root Cause: [technical summary]

Resolution: [what was done to fix]

Next Steps: [preventive measures being implemented]

We apologize for the disruption and are committed to preventing recurrence.

Full post-mortem: [link when available]
```

---

## Post-Incident Review

### Post-Mortem Template

```markdown
# Incident Post-Mortem: [Incident Name]

**Date:** [date]
**Severity:** [P0-P3]
**Duration:** [X hours Y minutes]
**Author:** [name]

## Summary

[2-3 sentence overview]

## Timeline

| Time (UTC) | Event |
|------------|-------|
| T+0min | Initial alert received |
| T+Xmin | [event] |
| ... | ... |

## Impact

- Users affected: [number/percentage]
- Services impacted: [list]
- Data compromised: [if any]
- Financial impact: [if quantifiable]

## Root Cause

[Detailed technical explanation]

## What Went Well

- [item]
- [item]

## What Could Be Improved

- [item]
- [item]

## Action Items

| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| [task] | [name] | [date] | [ ] |

## Lessons Learned

[Key takeaways for the team]
```

### Action Item Tracking

- Review action items weekly until complete
- Escalate overdue items to leadership
- Close loop with all stakeholders

---

## Appendix

### A. Emergency Contacts

| Role | Name | Phone | Email |
|------|------|-------|-------|
| Incident Commander | [name] | [phone] | [email] |
| Technical Lead | [name] | [phone] | [email] |
| Legal Counsel | [name] | [phone] | [email] |
| External Security | [firm] | [phone] | [email] |

### B. Tool Access

| Tool | Purpose | Credentials Location |
|------|---------|---------------------|
| AWS Console | Infrastructure | 1Password vault |
| GitHub Admin | Repository access | 1Password vault |
| Cloudflare | DNS/WAF | 1Password vault |
| Monitoring | Alerts | [URL] |

### C. Evidence Preservation

**DO:**
- Take screenshots with timestamps
- Export logs before rotation
- Document command outputs
- Hash all files (sha256sum)

**DON'T:**
- Modify production systems without documenting
- Delete anything (even if malicious)
- Discuss incident publicly before resolution
- Power off compromised systems

### D. Legal & Compliance

**Data Breach Notification Requirements:**
- GDPR (EU): 72 hours to supervisory authority
- CCPA (California): "Most expedient time possible"
- PIPEDA (Canada): "As soon as feasible"

**Preserve Privilege:**
- Mark communications "Attorney-Client Privileged"
- Limit distribution to need-to-know
- Engage legal counsel early for significant incidents

### E. Training & Drills

**Quarterly:**
- Tabletop exercise (simulated incident)
- Review and update this runbook
- Test backup restoration

**Annually:**
- Full incident response drill
- External security audit
- Team training refresh

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-12 | 牛 (AI Agent) | Initial creation for Bounty #1689 |

---

*This runbook is a living document. Update it after every incident with lessons learned.*

**For questions or updates, contact:** security@rustchain.org
