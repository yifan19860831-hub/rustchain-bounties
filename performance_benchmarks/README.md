# RustChain Performance Benchmark Suite

Comprehensive performance benchmarking suite for RustChain blockchain, testing network, transaction, and consensus performance.

## 🎯 Bounty

**Issue:** #1657 - Create a RustChain performance benchmarking suite  
**Reward:** 3 RTC  
**Tags:** performance, benchmark, testing, network, consensus, transaction

## 📋 Overview

This benchmark suite provides detailed performance analysis across three key areas:

### 1. Network Performance
- **API Latency**: Response times for core endpoints
- **Throughput**: Maximum requests per second
- **Connection Stability**: Connection establishment and reliability

### 2. Transaction Performance
- **Submission Time**: Time to submit transactions
- **Validation Time**: Time to validate transactions
- **Confirmation Time**: Time to confirm transactions

### 3. Consensus Performance
- **Block Generation**: Time to generate new blocks
- **Consensus Rounds**: Time for consensus agreement
- **Miner Sync**: Time for miner synchronization

## 🚀 Quick Start

### Installation

```bash
cd performance_benchmarks
pip install -r requirements.txt
```

### Run Full Benchmark

```bash
# Default target (https://rustchain.org)
python benchmark_suite.py

# Custom target
python benchmark_suite.py https://your-rustchain-node.com
```

### Programmatic Usage

```python
import asyncio
from benchmark_suite import RustChainBenchmark

async def run_custom_benchmark():
    async with RustChainBenchmark("https://rustchain.org") as benchmark:
        # Run specific tests
        await benchmark.benchmark_api_latency(samples=100)
        await benchmark.benchmark_throughput(duration_seconds=30)
        
        # Generate report
        benchmark.generate_report()

asyncio.run(run_custom_benchmark())
```

## 📊 Output

### Generated Reports

The benchmark suite generates two types of reports:

1. **Markdown Report** (`benchmark_report_YYYYMMDD_HHMMSS.md`)
   - Detailed performance analysis
   - Statistical breakdowns
   - Error summaries

2. **CSV Summary** (`benchmark_summary_YYYYMMDD_HHMMSS.csv`)
   - Machine-readable format
   - Easy to import into spreadsheets
   - Suitable for trend analysis

### Example Output

```
======================================================================
RustChain Performance Benchmark Suite
======================================================================
Target: https://rustchain.org
Started: 2026-03-12T19:30:00.000000
======================================================================

📡 Running API Latency Benchmark (50 samples)...
  Progress: 10/50 samples
  Progress: 20/50 samples
  Progress: 30/50 samples
  Progress: 40/50 samples
  Progress: 50/50 samples

📊 Running Throughput Benchmark (20s)...

...

======================================================================
Benchmark Complete!
======================================================================
Report: benchmark_reports/benchmark_report_20260312_193045.md
Finished: 2026-03-12T19:32:15.000000

📊 Quick Summary:
  API Latency Benchmark: 145.23ms avg, 98.5% success
  Throughput Benchmark: 132.45ms avg, 99.2% success
  Connection Stability Benchmark: 178.90ms avg, 97.8% success
  Transaction Submission Benchmark: 156.78ms avg, 96.7% success
  Transaction Validation Benchmark: 148.34ms avg, 98.3% success
  Block Generation Benchmark: 142.56ms avg, 99.1% success
  Consensus Rounds Benchmark: 139.87ms avg, 98.9% success
  Miner Sync Benchmark: 141.23ms avg, 99.0% success
```

## 📈 Metrics Explained

### Latency Percentiles

- **Min**: Fastest response time
- **Avg**: Mean response time
- **Median**: Middle value (50th percentile)
- **P90**: 90% of requests faster than this
- **P95**: 95% of requests faster than this
- **P99**: 99% of requests faster than this

### Success Rate

Percentage of successful requests (HTTP 200-299 responses).

### Standard Deviation

Measure of latency consistency. Lower values indicate more consistent performance.

## 🔧 Configuration

### Adjusting Sample Sizes

```python
# More samples = more accurate but slower
await benchmark.benchmark_api_latency(samples=200)  # Default: 50

# Fewer samples for quick tests
await benchmark.benchmark_api_latency(samples=10)
```

### Custom Test Duration

```python
# Longer throughput test
await benchmark.benchmark_throughput(duration_seconds=60)  # Default: 30
```

### Specific Test Categories

```python
# Only network tests
await benchmark.benchmark_api_latency()
await benchmark.benchmark_throughput()
await benchmark.benchmark_connection_stability()

# Only transaction tests
await benchmark.benchmark_transaction_submission()
await benchmark.benchmark_transaction_validation()

# Only consensus tests
await benchmark.benchmark_block_generation()
await benchmark.benchmark_consensus_rounds()
await benchmark.benchmark_miner_sync()
```

## 📝 Test Descriptions

### Network Performance Tests

#### API Latency Benchmark
- **Purpose**: Measure response times for core API endpoints
- **Endpoints**: `/health`, `/epoch`, `/api/miners`
- **Samples**: 50 (default)
- **Output**: Latency statistics across all endpoints

#### Throughput Benchmark
- **Purpose**: Measure maximum requests per second
- **Duration**: 30 seconds (default)
- **Output**: Achieved RPS, latency under load

#### Connection Stability Benchmark
- **Purpose**: Test connection establishment reliability
- **Iterations**: 50 (default)
- **Output**: Connection times, failure rate

### Transaction Performance Tests

#### Transaction Submission Benchmark
- **Purpose**: Measure time to submit transactions
- **Samples**: 50 (default)
- **Output**: Submission latency, success rate

#### Transaction Validation Benchmark
- **Purpose**: Measure time to validate transactions
- **Samples**: 50 (default)
- **Output**: Validation latency, consistency

### Consensus Performance Tests

#### Block Generation Benchmark
- **Purpose**: Measure block generation timing
- **Samples**: 20 (default)
- **Output**: Block generation latency

#### Consensus Rounds Benchmark
- **Purpose**: Measure consensus agreement timing
- **Samples**: 30 (default)
- **Output**: Consensus round duration

#### Miner Sync Benchmark
- **Purpose**: Measure miner synchronization time
- **Samples**: 30 (default)
- **Output**: Sync latency across miners

## 🐛 Troubleshooting

### SSL Certificate Errors

The benchmark suite automatically handles self-signed certificates. If you encounter SSL errors:

```python
# The connector is already configured with ssl=False
async with RustChainBenchmark("https://rustchain.org") as benchmark:
    # SSL verification is disabled by default
    await benchmark.benchmark_api_latency()
```

### Timeout Errors

If you see frequent timeouts, increase the timeout value:

```python
# Modify the timeout in measure_request method
latency, data, error = await self.measure_request(
    endpoint, 
    timeout=60  # Increase from default 30 seconds
)
```

### High Error Rates

If error rates exceed 10%:
1. Check network connectivity
2. Verify the target node is healthy
3. Reduce concurrent requests
4. Increase timeout values

## 📊 Interpreting Results

### Good Performance Indicators

- **API Latency**: < 200ms average
- **Throughput**: > 50 RPS
- **Success Rate**: > 95%
- **P99 Latency**: < 500ms

### Warning Signs

- **High P99 vs Avg**: Indicates occasional slow requests
- **Low Success Rate**: May indicate instability
- **High Standard Deviation**: Inconsistent performance
- **Connection Errors**: Network or server issues

## 🔬 Advanced Usage

### Custom Metrics

Add custom metrics by extending the benchmark class:

```python
class CustomBenchmark(RustChainBenchmark):
    async def benchmark_custom_metric(self):
        # Your custom benchmark logic
        pass
```

### Real-time Monitoring

Integrate with monitoring systems:

```python
async with RustChainBenchmark() as benchmark:
    result = await benchmark.benchmark_api_latency()
    
    # Send to monitoring system
    send_to_prometheus(result)
    send_to_datadog(result)
```

### Automated Testing

Integrate into CI/CD:

```yaml
# .github/workflows/benchmark.yml
- name: Run Performance Benchmarks
  run: |
    cd performance_benchmarks
    pip install -r requirements.txt
    python benchmark_suite.py
```

## 📚 Additional Resources

- [RustChain Documentation](https://rustchain.org)
- [RustChain Whitepaper](../docs/RustChain_Whitepaper_Flameholder_v0.97-1.pdf)
- [Load Test Suite](../load_tests/) - Complementary load testing tools

## 🏆 Bounty Completion Checklist

- [x] Network performance benchmarks
- [x] Transaction performance benchmarks
- [x] Consensus performance benchmarks
- [x] Statistical analysis (min, max, avg, percentiles)
- [x] Markdown report generation
- [x] CSV export for further analysis
- [x] Error tracking and reporting
- [x] Async implementation for efficiency
- [x] Comprehensive documentation
- [x] Example usage and configuration

## 📄 License

Same license as the main RustChain project (MIT).

## 👤 Author

Created for RustChain Bounties #1657

---

**Note**: This benchmark suite is designed to be non-intrusive. However, running benchmarks against production nodes may generate significant load. Use with caution and consider running against test/staging environments first.
