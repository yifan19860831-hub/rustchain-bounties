# RustChain API Load Test Suite

Load testing suite for RustChain API using [Locust](https://locust.io/).

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Web UI Mode
```bash
locust -f locustfile.py --host=http://localhost:8545
# Open http://localhost:8089 in browser
```

### Headless Mode
```bash
# 100 users, 10 spawn rate, 5 minutes
locust -f locustfile.py --host=http://localhost:8545 --headless -u 100 -r 10 -t 300s

# Stress test with 500 users
locust -f locustfile.py --host=http://localhost:8545 --headless -u 500 -r 50 -t 600s
```

## Test Scenarios

### RustChainUser (Normal Load)
- `get_balance` (weight: 3) - Balance queries
- `get_epoch_info` (weight: 2) - Epoch information
- `get_miner_stats` (weight: 2) - Miner statistics
- `submit_attestation` (weight: 1) - Attestation submission
- `get_network_status` (weight: 1) - Network status
- `health_check` (weight: 1) - Health check endpoint

### HeavyLoadUser (Stress Test)
- `rapid_balance_check` - Rapid fire balance queries

## Output

Locust provides:
- Requests per second
- Average response time
- Median response time
- 95th/99th percentile response times
- Failure rate
- Real-time charts and graphs

## Integration with CI/CD

Add to GitHub Actions:
```yaml
- name: Run Load Tests
  run: |
    pip install -r tests/load/requirements.txt
    locust -f tests/load/locustfile.py --headless -u 50 -r 5 -t 60s --expect-failures
```