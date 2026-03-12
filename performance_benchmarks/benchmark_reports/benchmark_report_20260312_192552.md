# RustChain Performance Benchmark Report

**Generated:** 2026-03-12T19:25:52.849487

**Target:** https://rustchain.org


## Network Performance

| Test | Samples | Min (ms) | Avg (ms) | Median (ms) | P95 (ms) | P99 (ms) | Success Rate |
|------|---------|----------|----------|-------------|----------|----------|--------------|
| API Latency Benchmark | 150 | 293.96 | 888.85 | 301.86 | 2468.58 | 3088.61 | 100.0% |
| Throughput Benchmark | 20 | 5063.90 | 11623.84 | 12798.59 | 20373.22 | 20373.22 | 100.0% |
| Connection Stability Benchmark | 30 | 2266.79 | 2767.96 | 2573.64 | 4095.88 | 4456.88 | 100.0% |


## Transaction Performance

| Test | Samples | Min (ms) | Avg (ms) | Median (ms) | P95 (ms) | P99 (ms) | Success Rate |
|------|---------|----------|----------|-------------|----------|----------|--------------|
| Transaction Submission Benchmark | 30 | 293.51 | 299.08 | 297.48 | 309.71 | 312.35 | 100.0% |
| Transaction Validation Benchmark | 30 | 1684.68 | 2228.14 | 1998.78 | 3385.18 | 3637.35 | 100.0% |


## Consensus Performance

| Test | Samples | Min (ms) | Avg (ms) | Median (ms) | P95 (ms) | P99 (ms) | Success Rate |
|------|---------|----------|----------|-------------|----------|----------|--------------|
| Block Generation Benchmark | 15 | 294.21 | 352.60 | 301.42 | 1032.21 | 1032.21 | 100.0% |
| Consensus Rounds Benchmark | 20 | 315.80 | 323.33 | 321.55 | 336.90 | 336.90 | 100.0% |
| Miner Sync Benchmark | 20 | 316.58 | 321.30 | 319.48 | 336.00 | 336.00 | 100.0% |


## Summary

- **Total Tests Run:** 8
- **Total Errors:** 0
- **Average Success Rate:** 100.0%
- **Average API Latency:** 2151.79ms