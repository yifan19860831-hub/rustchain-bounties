# RustChain Release Checklist

> **Purpose:** Ensure consistent, safe, and verified releases across all RustChain components.
> **Scope:** RustChain core, clawrtc miner, Windows miner builds, and documentation.

---

## 📋 Pre-Release Verification (Before Tagging)

### Code Quality & Testing

- [ ] **All CI pipelines pass**
  - [ ] `ci.yml` - Main CI workflow
  - [ ] `rust-ci.yml` - Rust component tests
  - [ ] `build-windows.yml` - Windows build verification
  - [ ] `ci_ledger_invariants.yml` - Ledger integrity checks
  - [ ] No workflow failures in last 24 hours

- [ ] **Test Coverage**
  - [ ] Unit tests pass locally (`pytest` / `cargo test`)
  - [ ] Integration tests pass on all supported platforms
  - [ ] Hardware attestation tests verified (6 fingerprint checks)
  - [ ] Anti-emulation tests confirm VM detection works

- [ ] **Code Review**
  - [ ] All PRs merged and closed
  - [ ] No open critical/high severity issues
  - [ ] Security audit completed (if applicable)
  - [ ] CHANGELOG.md updated with all changes

### Platform Compatibility

- [ ] **Linux Builds**
  - [ ] x86_64 build compiles and runs
  - [ ] ppc64le/POWER8 build compiles and runs
  - [ ] install-miner.sh tested on Ubuntu 20.04+, Debian 11+, Fedora 38+
  - [ ] systemd service file validates correctly

- [ ] **macOS Builds**
  - [ ] Apple Silicon (M1/M2/M3) build works
  - [ ] Intel Mac build works
  - [ ] PowerPC G4/G5 builds work (Mac OS X Tiger/Leopard)
  - [ ] launchd plist validates correctly

- [ ] **Windows Builds**
  - [ ] RustChainMiner.exe compiles without errors
  - [ ] GUI mode launches and functions
  - [ ] Headless mode (`--headless`) works
  - [ ] Wallet generation works on first launch
  - [ ] Installer (RustChain-Miner-Installer.zip) tested

- [ ] **Python Package (clawrtc)**
  - [ ] `pip install clawrtc` succeeds
  - [ ] All subcommands work: `install`, `start`, `mine`, `wallet`
  - [ ] Hardware multipliers display correctly
  - [ ] Network connectivity to node verified

### Security Checks

- [ ] **Dependency Audit**
  - [ ] `pip-audit` or `safety` scan passes (Python deps)
  - [ ] `cargo audit` passes (Rust deps)
  - [ ] No known CVEs in dependencies
  - [ ] All dependencies pinned to specific versions

- [ ] **Secrets & Credentials**
  - [ ] No API keys or secrets in code
  - [ ] No hardcoded wallet addresses
  - [ ] SSL certificates valid (rustchain.org)
  - [ ] Self-signed certs documented for node

- [ ] **Hardware Attestation**
  - [ ] All 6 fingerprint checks execute correctly
  - [ ] VM/emulator detection returns ~0x rewards
  - [ ] Vintage multipliers apply correctly (G4: 2.5×, G5: 2.0×, etc.)
  - [ ] Anti-Sybil measures functional

### Documentation

- [ ] **README.md**
  - [ ] Installation instructions up to date
  - [ ] CLI flags documented
  - [ ] Hardware multiplier table accurate
  - [ ] Network endpoints correct

- [ ] **Release Notes**
  - [ ] New features listed
  - [ ] Breaking changes highlighted
  - [ ] Migration guide (if needed)
  - [ ] Known issues documented

- [ ] **API Documentation**
  - [ ] `/health`, `/epoch`, `/api/miners` endpoints documented
  - [ ] Wallet balance endpoint documented
  - [ ] Governance endpoints (if applicable) documented

---

## 🚀 Release Execution (Tagging & Publishing)

### Version Numbering

- [ ] **Semantic Versioning**
  - [ ] Format: `vMAJOR.MINOR.PATCH` (e.g., `v1.2.3`)
  - [ ] MAJOR: Breaking changes
  - [ ] MINOR: New features (backward compatible)
  - [ ] PATCH: Bug fixes only

### GitHub Release

- [ ] **Create Release Tag**
  ```bash
  git tag -a v1.2.3 -m "RustChain v1.2.3 - Release summary"
  git push origin v1.2.3
  ```

- [ ] **GitHub Release Page**
  - [ ] Title: `RustChain v1.2.3`
  - [ ] Tag: `v1.2.3`
  - [ ] Description: Copy from CHANGELOG.md
  - [ ] Mark as "Latest release" (if stable)
  - [ ] Mark as pre-release (if beta)

- [ ] **Upload Binaries**
  - [ ] `RustChainMiner.exe` (Windows standalone)
  - [ ] `RustChain-Miner-Installer.zip` (Windows installer)
  - [ ] `install-miner.sh` (Linux/macOS installer)
  - [ ] Platform-specific miner binaries (if applicable)
  - [ ] SHA256 checksums file

### Python Package (clawrtc)

- [ ] **PyPI Release**
  ```bash
  python setup.py sdist bdist_wheel
  twine upload dist/*
  ```
  - [ ] Version number matches GitHub tag
  - [ ] Package uploads successfully to PyPI
  - [ ] `pip install clawrtc` installs new version

- [ ] **Other Package Managers**
  - [ ] npm package updated (if applicable)
  - [ ] Homebrew tap updated (`brew update && brew upgrade clawrtc`)
  - [ ] AUR package updated (`yay -S clawrtc`)
  - [ ] .deb package built and attached

### Documentation Sync

- [ ] **Website Updates**
  - [ ] rustchain.org reflects new version
  - [ ] Download links point to new release
  - [ ] Block explorer shows correct node version

- [ ] **Announcement**
  - [ ] Discord announcement in #announcements
  - [ ] Twitter/X post with release highlights
  - [ ] GitHub Discussions post (if applicable)

---

## ✅ Post-Release Verification (After Publishing)

### Installation Testing

- [ ] **Fresh Install Tests** (on clean VMs/containers)
  - [ ] Linux: `curl -sSL ... | bash` succeeds
  - [ ] macOS: `brew install clawrtc` succeeds
  - [ ] Windows: EXE downloads and runs
  - [ ] Python: `pip install clawrtc` succeeds

- [ ] **Upgrade Tests**
  - [ ] Existing miners auto-update (if applicable)
  - [ ] Wallet data preserved after upgrade
  - [ ] Configuration files migrate correctly

### Network Verification

- [ ] **Node Health**
  ```bash
  curl -sk https://rustchain.org/health
  curl -sk https://rustchain.org/epoch
  ```
  - [ ] Node responds with 200 OK
  - [ ] Epoch number increments correctly
  - [ ] No consensus issues

- [ ] **Miner Connectivity**
  ```bash
  curl -sk https://rustchain.org/api/miners
  ```
  - [ ] Active miners list returns
  - [ ] New miners can register
  - [ ] Wallet balances queryable

- [ ] **Block Explorer**
  - [ ] https://rustchain.org/explorer loads
  - [ ] Latest blocks display correctly
  - [ ] Wallet lookup works

### Community Monitoring

- [ ] **GitHub Issues**
  - [ ] Monitor for bug reports (first 24-48 hours)
  - [ ] Respond to installation issues promptly
  - [ ] Tag known issues in release notes

- [ ] **Discord/Community**
  - [ ] Monitor #support channel for issues
  - [ ] Help users with upgrade problems
  - [ ] Collect feedback on new features

- [ ] **Social Media**
  - [ ] Track mentions of release
  - [ ] Respond to questions on Twitter/X
  - [ ] Monitor Reddit (if applicable)

### Metrics & Analytics

- [ ] **Download Stats** (first week)
  - [ ] GitHub release download count
  - [ ] PyPI download stats (`pypistats`)
  - [ ] Homebrew install count

- [ ] **Mining Stats**
  - [ ] Number of active miners increased
  - [ ] No spike in failed attestations
  - [ ] Epoch rewards distributing correctly

- [ ] **Error Monitoring**
  - [ ] Node error logs reviewed
  - [ ] No spike in 5xx errors
  - [ ] Attestation failure rate normal

---

## 🔧 Rollback Procedure (If Issues Found)

### Critical Issues (Immediate Rollback)

- [ ] **Conditions for Rollback**
  - [ ] Consensus-breaking bug discovered
  - [ ] Security vulnerability found
  - [ ] >50% of miners unable to attest
  - [ ] Wallet corruption reported

- [ ] **Rollback Steps**
  1. Announce issue on Discord/Twitter
  2. Mark release as "pre-release" on GitHub
  3. Revert PyPI package (if possible) or yank version
  4. Update website download links to previous version
  5. Create emergency patch release (v1.2.4)

- [ ] **Communication**
  - [ ] GitHub issue created explaining the bug
  - [ ] Migration guide for rollback
  - [ ] Timeline for fix communicated

---

## 📊 Release Checklist Template (Copy for Each Release)

```markdown
## Release: v[VERSION]

### Pre-Release
- [ ] CI/CD pipelines pass
- [ ] All tests pass (unit + integration)
- [ ] Platform builds verified (Linux, macOS, Windows)
- [ ] Security audit complete
- [ ] Documentation updated

### Release Execution
- [ ] Git tag created and pushed
- [ ] GitHub release published with binaries
- [ ] PyPI package uploaded
- [ ] Package managers updated (brew, npm, AUR)
- [ ] Website updated

### Post-Release
- [ ] Fresh install tests pass
- [ ] Node health verified
- [ ] Community monitoring active
- [ ] Download metrics tracked
- [ ] No critical issues reported (48h)

**Released by:** @[username]
**Release Date:** YYYY-MM-DD
**Wallet for payout:** [miner-id]
```

---

## 🎯 Reward Distribution

Upon successful completion and verification of this checklist:

- **RTC Payout:** 3 RTC to contributor wallet
- **Verification:** Checklist must be reviewed and approved by maintainer
- **Wallet:** Include miner ID in PR description for payout

---

## 📝 Notes

- This checklist should be updated as new platforms or distribution channels are added.
- For major releases (MAJOR version bump), additional security audits and community testing periods are recommended.
- Keep release notes concise but informative — focus on user-impactful changes.
- Always test on actual vintage hardware when possible (G4, G5, POWER8) before release.

---

**Contributed for:** [BOUNTY #1686](https://github.com/Scottcjn/rustchain-bounties/issues/1686)
**Reward:** 3 RTC
