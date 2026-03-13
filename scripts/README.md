# RustChain Scripts

Collection of utility scripts for RustChain network operations, monitoring, and maintenance.

## 📁 Scripts Overview

### Core Scripts

| Script | Purpose | Language |
|--------|---------|----------|
| `agent_bounty_hunter.py` | Autonomous bounty discovery and claiming | Python |
| `auto_triage_claims.py` | Automated claim triage and validation | Python |
| `node_miner_weekly_scan.py` | Weekly node/miner health scanning | Python |
| `prometheus_exporter.py` | Prometheus metrics exporter | Python |
| `supply_chain_lint.py` | Supply chain security scanning | Python |
| `sybil_risk_scorer.py` | Sybil attack risk assessment | Python |
| `run_stress_test.py` | Network stress testing | Python |

### Shell Scripts

| Script | Purpose |
|--------|---------|
| `post_issue374_followup.sh` | Automated follow-up for issue #374 |

### Docker

| File | Purpose |
|------|---------|
| `Dockerfile.metrics` | Metrics service container |

## 🔧 Quick Start

### Install Dependencies

```bash
pip install -r requirements-metrics.txt
```

### Run Node Scanner

```bash
python node_miner_weekly_scan.py
```

### Run Stress Test

```bash
python run_stress_test.py --nodes 50 --duration 300
```

### Start Prometheus Exporter

```bash
python prometheus_exporter.py --port 9090
```

## 📊 Metrics

The Prometheus exporter provides:
- Node health status
- Miner count
- Epoch progression
- Attestation rates
- Network latency

Access metrics at: `http://localhost:9090/metrics`

## 🔒 Security

- `supply_chain_lint.py` - Scans for supply chain vulnerabilities
- `sybil_risk_scorer.py` - Identifies potential Sybil attacks

## 🤖 Automation

Scripts are designed for:
- Cron job scheduling
- CI/CD integration
- Autonomous agent execution

## 📝 License

MIT License - RustChain Community
