# RustChain Anti-Sybil Mechanisms

## Overview

This document outlines comprehensive anti-Sybil mechanisms for RustChain to prevent fake miners, duplicate registrations, and other Sybil attacks that could compromise network integrity.

## 1. Identity Verification

### 1.1 Hardware-Based Attestation

**Purpose**: Ensure each miner corresponds to a unique physical machine.

**Implementation**:
- **TPM (Trusted Platform Module)**: Require TPM 2.0 for hardware identity
- **Secure Enclave**: Use platform-specific secure elements (Intel SGX, ARM TrustZone)
- **Hardware Fingerprinting**: Collect unique hardware identifiers:
  - CPU ID
  - Motherboard serial number
  - MAC address (with privacy considerations)
  - Disk drive serial numbers

**Verification Process**:
```rust
pub struct HardwareAttestation {
    pub tpm_quote: Vec<u8>,
    pub cpu_id: String,
    pub motherboard_serial: String,
    pub timestamp: u64,
    pub signature: Signature,
}

impl HardwareAttestation {
    pub fn verify(&self, public_key: &PublicKey) -> Result<bool, AttestationError> {
        // Verify TPM quote signature
        // Check timestamp freshness (< 5 minutes)
        // Validate hardware uniqueness against registry
    }
}
```

### 1.2 Proof of Personhood Integration

**Options**:
- **Worldcoin**: Integrate World ID for proof of unique humanity
- **BrightID**: Social graph-based identity verification
- **Proof of Humanity**: Ethereum-based registry of unique humans

**Implementation Strategy**:
```rust
pub enum PersonhoodProof {
    WorldID { nullifier: String, proof: ZKProof },
    BrightID { context_id: String, signature: Signature },
    ProofOfHumanity { registrant: Address, proof: Bytes },
}
```

## 2. Registration Controls

### 2.1 Stake-Based Registration

**Mechanism**: Require minimum token stake to register as miner.

**Benefits**:
- Increases cost of Sybil attacks
- Aligns miner incentives with network health
- Provides slashing collateral for misbehavior

**Parameters**:
```rust
pub struct RegistrationRequirements {
    pub minimum_stake: u64,           // e.g., 1000 RTC
    pub lockup_period: u64,           // e.g., 30 days
    pub cooldown_period: u64,         // e.g., 7 days after unstaking
}
```

### 2.2 Rate Limiting

**Prevent bulk registration attacks**:
- **Per-IP limits**: Max 3 registrations per IP per 24 hours
- **Per-wallet limits**: Max 5 miners per wallet address
- **Global rate limits**: Max 1000 new miners per epoch

**Implementation**:
```rust
pub struct RateLimiter {
    ip_registrations: HashMap<IpAddr, Vec<Timestamp>>,
    wallet_registrations: HashMap<Address, u32>,
    epoch_registrations: u32,
}

impl RateLimiter {
    pub fn check_registration_limit(
        &self,
        ip: IpAddr,
        wallet: Address,
        current_epoch: u64,
    ) -> Result<(), RateLimitError> {
        // Check IP-based limit
        // Check wallet-based limit
        // Check global epoch limit
    }
}
```

### 2.3 Registration Fee

**Dynamic fee structure**:
- Base fee: 10 RTC (non-refundable)
- Increases during high registration periods
- Fee burns to prevent economic exploitation

## 3. Continuous Verification

### 3.1 Random Challenges

**Mechanism**: Periodic random challenges to verify miner legitimacy.

**Challenge Types**:
1. **Proof of Storage**: Verify claimed storage capacity
2. **Proof of Computation**: Random computational tasks
3. **Proof of Connectivity**: Network reachability tests

**Implementation**:
```rust
pub struct Challenge {
    pub challenge_id: U256,
    pub challenge_type: ChallengeType,
    pub target_miner: MinerId,
    pub deadline: u64,
    pub verification_data: Vec<u8>,
}

pub enum ChallengeType {
    Storage { sector_id: u64, expected_hash: Hash },
    Computation { puzzle: Puzzle, difficulty: u32 },
    Connectivity { nonce: u64, timeout_ms: u32 },
}
```

**Penalty for non-response**:
- 1st failure: Warning, reduced rewards
- 2nd failure: 10% stake slash
- 3rd failure: Deregistration, full stake slash

### 3.2 Behavioral Analysis

**Monitor mining patterns for Sybil indicators**:

**Red Flags**:
- Identical submission timestamps (±1 second)
- Identical hardware fingerprints across multiple miners
- Coordinated behavior patterns
- Unusual geographic clustering
- Identical network endpoints

**Detection Algorithm**:
```rust
pub struct SybilDetector {
    miner_history: HashMap<MinerId, MiningHistory>,
    similarity_threshold: f64,
}

impl SybilDetector {
    pub fn detect_clusters(&self) -> Vec<SybilCluster> {
        // Analyze timestamp patterns
        // Compare hardware fingerprints
        // Check network topology
        // Flag suspicious clusters for review
    }
}

pub struct SybilCluster {
    pub miner_ids: Vec<MinerId>,
    pub confidence: f64,
    pub indicators: Vec<SybilIndicator>,
}
```

### 3.3 Reputation System

**Dynamic reputation scoring**:
```rust
pub struct MinerReputation {
    pub miner_id: MinerId,
    pub score: f64,              // 0.0 - 100.0
    pub uptime_percentage: f64,
    pub successful_attestations: u64,
    pub failed_challenges: u64,
    pub age_days: u32,
    pub slashing_history: Vec<SlashingEvent>,
}

impl MinerReputation {
    pub fn calculate_score(&self) -> f64 {
        // Weight factors:
        // - Uptime: 30%
        // - Attestation success: 25%
        // - Challenge responses: 25%
        // - Account age: 10%
        // - No slashing: 10%
    }
}
```

**Reputation Benefits**:
- Higher reputation = higher lottery selection probability
- Low reputation miners face increased scrutiny
- Threshold for deregistration: score < 20

## 4. Network-Level Protections

### 4.1 IP Analysis

**Prevent IP-based Sybil attacks**:
- **IP reputation database**: Track known proxy/VPN/Tor exit nodes
- **ASN analysis**: Flag datacenter IP ranges (AWS, GCP, Azure)
- **Geographic consistency**: Verify claimed location matches IP geolocation

**Implementation**:
```rust
pub struct IPAnalyzer {
    vpn_database: IpDatabase,
    datacenter_ranges: Vec<IpRange>,
    geo_database: GeoIpDatabase,
}

impl IPAnalyzer {
    pub fn assess_risk(&self, ip: IpAddr, claimed_location: Location) -> RiskLevel {
        // Check if IP is known VPN/proxy
        // Check if IP is datacenter range
        // Verify geographic consistency
        // Return risk score
    }
}

pub enum RiskLevel {
    Low,      // Residential IP, consistent location
    Medium,   // Cloud provider, some inconsistencies
    High,     // Known proxy, major inconsistencies
    Critical, // Tor exit, blacklisted IP
}
```

### 4.2 Network Graph Analysis

**Detect coordinated Sybil networks**:

**Metrics**:
- Connection patterns between miners
- Shared infrastructure indicators
- Communication timing analysis

```rust
pub struct NetworkGraph {
    nodes: HashMap<MinerId, NodeProperties>,
    edges: HashMap<(MinerId, MinerId), EdgeProperties>,
}

impl NetworkGraph {
    pub fn detect_sybil_community(&self) -> Vec<SybilCommunity> {
        // Use community detection algorithms (Louvain, Label Propagation)
        // Identify unusually dense subgraphs
        // Flag for manual review
    }
}
```

## 5. Economic Deterrents

### 5.1 Slashing Conditions

**Define clear slashing rules**:

| Violation | Slash Amount | Additional Penalty |
|-----------|--------------|-------------------|
| Fake hardware attestation | 100% stake | Permanent ban |
| Duplicate registration | 100% stake | Wallet blacklist |
| Missed 3+ challenges | 50% stake | 30-day cooldown |
| Sybil cluster participation | 100% stake | All linked accounts banned |
| False attestation | 25% stake | Reputation reset |

**Implementation**:
```rust
pub enum SlashingReason {
    FakeAttestation,
    DuplicateRegistration,
    ChallengeFailure(u32), // count
    SybilParticipation,
    FalseAttestation,
}

pub fn calculate_slash(
    reason: SlashingReason,
    stake: u64,
    reputation: f64,
) -> u64 {
    match reason {
        SlashingReason::FakeAttestation => stake, // 100%
        SlashingReason::DuplicateRegistration => stake,
        SlashingReason::ChallengeFailure(count) if count >= 3 => stake / 2,
        SlashingReason::SybilParticipation => stake,
        SlashingReason::FalseAttestation => stake / 4,
        _ => 0,
    }
}
```

### 5.2 Bounty System

**Incentivize community policing**:
- **Bounty**: 10% of slashed stake for valid Sybil reports
- **Evidence requirements**: Concrete proof of violation
- **False report penalty**: 5% reporter stake slash

```rust
pub struct BountyReport {
    pub reporter: Address,
    pub accused: Vec<MinerId>,
    pub evidence: Evidence,
    pub bond: u64, // Reporter's bond (slashed if false)
}

pub enum Evidence {
    HardwareDuplication { miner1: MinerId, miner2: MinerId, match_data: Bytes },
    IpClustering { miners: Vec<MinerId>, shared_ip: IpAddr },
    BehavioralPattern { miners: Vec<MinerId>, correlation: f64 },
}
```

## 6. Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
- [ ] Hardware attestation framework
- [ ] Stake-based registration
- [ ] Basic rate limiting
- [ ] Registration fee mechanism

### Phase 2: Detection (Week 3-4)
- [ ] Random challenge system
- [ ] Behavioral analysis engine
- [ ] IP analysis integration
- [ ] Reputation system

### Phase 3: Enforcement (Week 5-6)
- [ ] Slashing mechanism
- [ ] Bounty reporting system
- [ ] Network graph analysis
- [ ] Appeal process

### Phase 4: Optimization (Week 7-8)
- [ ] Performance tuning
- [ ] False positive reduction
- [ ] Community feedback integration
- [ ] Documentation and audits

## 7. Monitoring & Metrics

### Key Metrics to Track

```rust
pub struct AntiSybilMetrics {
    pub total_miners: u64,
    pub verified_miners: u64,
    pub flagged_miners: u64,
    pub slashed_miners: u64,
    pub sybil_clusters_detected: u64,
    pub total_slashed_amount: u64,
    pub bounties_paid: u64,
    pub false_positive_rate: f64,
    pub avg_challenge_response_time: u64,
}
```

### Alert Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| New miners/day | > 500 | > 1000 |
| Sybil clusters/week | > 5 | > 20 |
| False positive rate | > 1% | > 5% |
| Challenge failure rate | > 10% | > 25% |

## 8. Privacy Considerations

### Data Minimization
- Only collect necessary hardware identifiers
- Hash sensitive data before storage
- Implement data retention policies

### Zero-Knowledge Proofs
- Explore ZK-based attestations
- Prove uniqueness without revealing identity
- Privacy-preserving reputation proofs

## 9. Governance

### Parameter Updates
- Anti-Sybil parameters governed by DAO
- Emergency upgrade mechanism for active attacks
- Community review period: 7 days for major changes

### Appeal Process
- Slashed miners can appeal within 14 days
- Community jury review for disputes
- Transparent appeal outcomes

## 10. References

- [Sybil Attacks in P2P Networks](https://en.wikipedia.org/wiki/Sybil_attack)
- [Ethereum Staking & Slashing](https://ethereum.org/en/staking/slashing/)
- [Worldcoin Proof of Personhood](https://worldcoin.org/)
- [BrightID Identity Network](https://www.brightid.org/)

---

**Document Version**: 1.0.0  
**Last Updated**: 2026-03-12  
**Author**: RustChain Security Team  
**Status**: Draft for Community Review
