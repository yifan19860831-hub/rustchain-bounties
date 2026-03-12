# RustChain API Versioning Policy

**Status:** Active  
**Effective Date:** 2026-03-12  
**Owner:** RustChain Core Team  
**Related:** [RustChain Whitepaper](docs/RustChain_Whitepaper_Flameholder_v0.97-1.pdf), [API Endpoints](README.md#-api-endpoints)

---

## Table of Contents

1. [Overview](#overview)
2. [Version Numbering](#version-numbering)
3. [Versioning Strategy](#versioning-strategy)
4. [Deprecation Process](#deprecation-process)
5. [Migration Guide](#migration-guide)
6. [Support & Timeline](#support--timeline)
7. [Examples](#examples)

---

## 1. Overview

This document defines the versioning policy for the RustChain public API. Our goal is to:

- **Maintain backward compatibility** whenever possible
- **Communicate changes clearly** to API consumers
- **Provide adequate migration time** for breaking changes
- **Support the ecosystem** of miners, wallets, and third-party tools

### 1.1 Current API Version

**Active Version:** `v1` (implicit, no version prefix required)

**Base URL:** `https://rustchain.org`

**Example Endpoints:**
```bash
# Current (v1 - implicit)
curl -sk https://rustchain.org/health
curl -sk https://rustchain.org/epoch
curl -sk https://rustchain.org/api/miners
curl -sk "https://rustchain.org/wallet/balance?miner_id=YOUR_WALLET"
```

### 1.2 When Versioning Applies

API versioning is triggered by **breaking changes** only:

| Change Type | Version Impact | Examples |
|-------------|----------------|----------|
| **Breaking** | Major version bump (v1 → v2) | Removing endpoints, changing response format, modifying request/response types |
| **Non-Breaking** | Minor version bump (v1.0 → v1.1) | Adding new endpoints, adding optional parameters, adding response fields |
| **Patch** | Patch version bump (v1.0.0 → v1.0.1) | Bug fixes, performance improvements, documentation updates |

---

## 2. Version Numbering

RustChain API uses **Semantic Versioning** (SemVer) format: `MAJOR.MINOR.PATCH`

### 2.1 Version Components

```
vMAJOR.MINOR.PATCH
│   │      │
│   │      └─ Patch: Backward-compatible bug fixes
│   └──────── Minor: Backward-compatible new features
└────────────── Major: Breaking changes
```

### 2.2 Version Examples

| Version | Type | Description |
|---------|------|-------------|
| `v1.0.0` | Major | Initial stable release |
| `v1.1.0` | Minor | Added `/governance/proposals` endpoint |
| `v1.1.1` | Patch | Fixed epoch calculation bug |
| `v2.0.0` | Major | Breaking: Changed response format from XML to JSON |

### 2.3 API Version Identification

**In URLs (URI Versioning):**
```
https://rustchain.org/v1/health
https://rustchain.org/v2/health
```

**In Response Headers:**
```http
X-RustChain-API-Version: 1.2.0
X-RustChain-API-Deprecated: false
X-RustChain-API-Sunset: 2026-12-31
```

**In Response Body:**
```json
{
  "api_version": "1.2.0",
  "data": { ... }
}
```

---

## 3. Versioning Strategy

### 3.1 URI Versioning (Primary)

RustChain uses **URI versioning** as the primary method:

```bash
# Versioned endpoint
curl -sk https://rustchain.org/v1/api/miners

# Unversioned (defaults to latest stable)
curl -sk https://rustchain.org/api/miners
```

**Rationale:**
- Simple and explicit
- Easy to debug and test
- Widely adopted pattern (GitHub, Stripe, Facebook)
- Clear separation between versions

### 3.2 Content Negotiation (Secondary)

For programmatic clients, content negotiation via Accept header is supported:

```bash
curl -sk https://rustchain.org/api/miners \
  -H "Accept: application/vnd.rustchain.v1+json"
```

### 3.3 Version Routing

| Request | Behavior |
|---------|----------|
| `/v1/...` | Routes to v1 API |
| `/v2/...` | Routes to v2 API |
| `/...` (no version) | Routes to latest stable version |

---

## 4. Deprecation Process

### 4.1 Deprecation Timeline

```
┌─────────────────────────────────────────────────────────────┐
│                    API Deprecation Flow                     │
├─────────────────────────────────────────────────────────────┤
│ Day 0:    Announce deprecation (email, GitHub, docs)        │
│ Day 0:    Add deprecation headers to API responses          │
│ Day 90:   Send reminder to active API users                 │
│ Day 180:  Send final warning                                │
│ Day 365:  Sunset - API version returns 410 Gone             │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Deprecation Headers

When an API version is deprecated, all responses include:

```http
HTTP/1.1 200 OK
X-RustChain-API-Version: 1.0.0
X-RustChain-API-Deprecated: true
X-RustChain-API-Sunset: 2027-03-12
Link: <https://rustchain.org/docs/api/v2/migration>; rel="successor-version"
```

### 4.3 Deprecation Response Body

Deprecated endpoints return additional metadata:

```json
{
  "api_version": "1.0.0",
  "deprecated": true,
  "sunset_date": "2027-03-12",
  "successor_version": "v2",
  "migration_guide": "https://rustchain.org/docs/api/v2/migration",
  "data": { ... }
}
```

### 4.4 Breaking Change Policy

Breaking changes require:

1. **Minimum 12-month notice** before sunset
2. **Clear migration documentation**
3. **Backward compatibility layer** (when feasible)
4. **Communication via multiple channels:**
   - GitHub announcements
   - Email to registered API users
   - Discord notifications
   - Documentation updates

---

## 5. Migration Guide

### 5.1 General Migration Principles

1. **Monitor deprecation headers** in your API responses
2. **Subscribe to API changelog** at `https://rustchain.org/docs/api/changelog`
3. **Test against new versions** before they become mandatory
4. **Update incrementally** - don't wait for sunset dates

### 5.2 Migration Checklist

When migrating from v1 to v2:

- [ ] Read the [v2 Migration Guide](docs/API_V2_MIGRATION.md)
- [ ] Update base URLs in your application
- [ ] Test all API calls against v2 endpoints
- [ ] Update response parsing logic (if format changed)
- [ ] Update error handling (if error codes changed)
- [ ] Deploy to staging environment
- [ ] Monitor logs for API errors
- [ ] Deploy to production
- [ ] Verify all integrations

### 5.3 Common Migration Scenarios

#### Scenario 1: Endpoint Moved

**v1:**
```bash
curl -sk https://rustchain.org/api/miners
```

**v2:**
```bash
curl -sk https://rustchain.org/v2/miners
```

**Action:** Update endpoint paths in your code.

#### Scenario 2: Response Format Changed

**v1 Response:**
```json
{
  "miners": [
    {"id": "miner1", "balance": 100}
  ]
}
```

**v2 Response:**
```json
{
  "api_version": "2.0.0",
  "data": {
    "miners": [
      {"id": "miner1", "balance": 100, "status": "active"}
    ]
  }
}
```

**Action:** Update JSON parsing to access `response.data.miners`.

#### Scenario 3: Authentication Method Changed

**v1:** Query parameter authentication
```bash
curl -sk "https://rustchain.org/api/miners?api_key=YOUR_KEY"
```

**v2:** Header authentication
```bash
curl -sk https://rustchain.org/v2/miners \
  -H "Authorization: Bearer YOUR_KEY"
```

**Action:** Update authentication mechanism.

---

## 6. Support & Timeline

### 6.1 Version Support Matrix

| Version | Status | Released | Sunset | Support Level |
|---------|--------|----------|--------|---------------|
| v1.0.x  | ✅ Active | 2026-01-15 | TBD | Full support |
| v1.1.x  | ✅ Active | 2026-02-20 | TBD | Full support |
| v2.0.x  | 🚧 Beta | 2026-03-12 | N/A | Preview only |

### 6.2 Support Levels

| Level | Description | Response Time |
|-------|-------------|---------------|
| **Full Support** | Actively maintained, bug fixes, security patches | 24-48 hours |
| **Maintenance** | Security fixes only, no new features | 72 hours |
| **Deprecated** | No support, migration recommended | Best effort |
| **Sunset** | No longer available (410 Gone) | N/A |

### 6.3 API Stability Guarantee

**Stable APIs (v1.0+):**
- Breaking changes only in major versions
- 12-month minimum support for each major version
- Clear deprecation timeline

**Beta APIs (v2.0+ beta):**
- May change without notice
- Not recommended for production use
- Feedback welcome

---

## 7. Examples

### 7.1 Versioned API Calls

```bash
# Explicit v1
curl -sk https://rustchain.org/v1/health
# Response: {"status": "ok", "api_version": "1.0.0"}

# Explicit v2 (beta)
curl -sk https://rustchain.org/v2/health
# Response: {"status": "ok", "api_version": "2.0.0-beta"}

# Implicit (latest stable)
curl -sk https://rustchain.org/health
# Response: {"status": "ok", "api_version": "1.1.0"}
```

### 7.2 Checking Deprecation Status

```bash
curl -skI https://rustchain.org/v1/api/miners | grep -i x-rustchain

# Output:
# X-RustChain-API-Version: 1.1.0
# X-RustChain-API-Deprecated: false
```

### 7.3 Handling Deprecated API

```python
import requests

response = requests.get('https://rustchain.org/v1/api/miners', verify=False)

# Check deprecation headers
if response.headers.get('X-RustChain-API-Deprecated') == 'true':
    sunset_date = response.headers.get('X-RustChain-API-Sunset')
    migration_guide = response.headers.get('Link')
    
    print(f"⚠️  API version deprecated! Sunset: {sunset_date}")
    print(f"Migration guide: {migration_guide}")
    
    # Schedule migration...

data = response.json()
```

### 7.4 API Version Detection

```javascript
async function checkApiVersion() {
  const response = await fetch('https://rustchain.org/health');
  const version = response.headers.get('X-RustChain-API-Version');
  const deprecated = response.headers.get('X-RustChain-API-Deprecated');
  
  console.log(`API Version: ${version}`);
  console.log(`Deprecated: ${deprecated}`);
  
  if (deprecated === 'true') {
    const sunset = response.headers.get('X-RustChain-API-Sunset');
    console.warn(`⚠️  This API version will be sunset on ${sunset}`);
  }
}
```

---

## 8. Governance & Feedback

### 8.1 Proposing API Changes

API changes are proposed via GitHub Issues:

1. Create issue at `github.com/Scottcjn/RustChain/issues`
2. Label: `api`, `enhancement`, or `breaking-change`
3. Provide use case and examples
4. Community discussion and review
5. Core team decision

### 8.2 API Changelog

All API changes are documented at:
- **Changelog:** `https://rustchain.org/docs/api/changelog`
- **GitHub Releases:** `github.com/Scottcjn/RustChain/releases`

### 8.3 Contact & Support

- **Documentation:** `https://rustchain.org/docs/api`
- **Discord:** `discord.gg/VqVVS2CW9Q`
- **GitHub Issues:** `github.com/Scottcjn/RustChain/issues`
- **Email:** api@rustchain.org

---

## Appendix A: Version History

| Version | Release Date | Key Changes |
|---------|--------------|-------------|
| v1.0.0 | 2026-01-15 | Initial stable release |
| v1.1.0 | 2026-02-20 | Added governance endpoints |
| v1.1.1 | 2026-03-01 | Fixed epoch timestamp bug |
| v2.0.0-beta | 2026-03-12 | New response format, authentication overhaul |

---

## Appendix B: Quick Reference

### Current Endpoints (v1)

```bash
# Health check
GET /health

# Current epoch
GET /epoch

# List miners
GET /api/miners

# Wallet balance
GET /wallet/balance?miner_id={wallet}

# Governance (v1.1+)
GET /governance/proposals
POST /governance/propose
POST /governance/vote
```

### Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Not Found |
| 410 | Gone (sunset version) |
| 429 | Rate Limited |
| 500 | Server Error |

---

**Document Version:** 1.0.0  
**Last Updated:** 2026-03-12  
**Next Review:** 2026-06-12
