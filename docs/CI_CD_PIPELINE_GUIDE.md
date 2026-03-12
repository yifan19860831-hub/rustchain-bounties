# RustChain CI/CD Pipeline Guide

> **Category:** DevOps / Automation  
> **Reward:** 3 RTC  
> **Status:** Complete ✅

---

## Table of Contents

1. [Overview](#overview)
2. [GitHub Actions Setup](#github-actions-setup)
3. [Automated Testing Workflow](#automated-testing-workflow)
4. [Deployment Pipeline](#deployment-pipeline)
5. [Security Scanning](#security-scanning)
6. [Release Automation](#release-automation)
7. [Monitoring & Alerts](#monitoring--alerts)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

---

## Overview

This guide provides a comprehensive CI/CD pipeline setup for RustChain projects using GitHub Actions. The pipeline automates testing, security scanning, building, and deployment processes to ensure reliable and secure software delivery.

### Pipeline Architecture

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│   Code Push │───▶│  CI Pipeline │───▶│  Security   │───▶│   Deploy     │
│   PR Create │    │  (Test)      │    │  Scan       │    │   (CD)       │
└─────────────┘    └──────────────┘    └─────────────┘    └──────────────┘
                          │                   │                  │
                          ▼                   ▼                  ▼
                   ┌─────────────┐    ┌─────────────┐    ┌──────────────┐
                   │ Unit Tests  │    │ Cargo Audit │    │ Node Deploy  │
                   │ Integration │    │ Safety      │    │ Docker Hub   │
                   │ E2E Tests   │    │ Dependabot  │    │ Documentation│
                   └─────────────┘    └─────────────┘    └──────────────┘
```

### Key Features

- ✅ **Automated Testing:** Unit, integration, and E2E tests on every push
- ✅ **Security Scanning:** Dependency vulnerability detection
- ✅ **Multi-Platform:** Windows, macOS, Linux support
- ✅ **Docker Integration:** Containerized builds and deployments
- ✅ **Release Automation:** Automatic versioning and changelog generation
- ✅ **Performance Benchmarks:** Regression detection

---

## GitHub Actions Setup

### Prerequisites

1. **GitHub Repository** with admin access
2. **RustChain CLI** installed locally for testing
3. **Docker Hub** account (optional, for container deployments)
4. **PyPI** account (optional, for Python package publishing)

### Repository Structure

```
rustchain-project/
├── .github/
│   └── workflows/
│       ├── ci.yml              # Main CI pipeline
│       ├── cd.yml              # Deployment pipeline
│       ├── security.yml        # Security scanning
│       ├── release.yml         # Release automation
│       └── benchmark.yml       # Performance benchmarks
├── src/
├── tests/
├── docs/
├── Dockerfile
├── requirements.txt
├── Cargo.toml                  # If using Rust components
└── README.md
```

### Environment Variables Setup

Configure these secrets in your GitHub repository settings (`Settings > Secrets and variables > Actions`):

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `RUSTCHAIN_API_KEY` | RustChain API authentication | `rc_live_xxx` |
| `RUSTCHAIN_WALLET` | Wallet address for bounties | `RTC...` |
| `DOCKER_USERNAME` | Docker Hub username | `youruser` |
| `DOCKER_PASSWORD` | Docker Hub access token | `xxx` |
| `PYPI_TOKEN` | PyPI API token | `pypi-xxx` |
| `DEPLOY_SSH_KEY` | SSH key for server deployment | `-----BEGIN...` |

---

## Automated Testing Workflow

### Main CI Workflow (`.github/workflows/ci.yml`)

```yaml
name: RustChain CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC

env:
  CARGO_TERM_COLOR: always
  PYTHON_VERSION: '3.11'
  RUST_VERSION: '1.75'

jobs:
  # ─────────────────────────────────────────────────────────────
  # Job 1: Lint & Code Quality
  # ─────────────────────────────────────────────────────────────
  lint:
    name: 🔍 Lint & Code Quality
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install flake8 black mypy pylint

      - name: Run Black (formatting check)
        run: black --check src/ tests/

      - name: Run Flake8 (linting)
        run: flake8 src/ tests/ --max-line-length=120 --ignore=E203,W503

      - name: Run MyPy (type checking)
        run: mypy src/ --ignore-missing-imports

      - name: Run Pylint
        run: pylint src/ --disable=C0114,C0115,C0116 || true

  # ─────────────────────────────────────────────────────────────
  # Job 2: Unit Tests (Multi-Platform)
  # ─────────────────────────────────────────────────────────────
  test-unit:
    name: 🧪 Unit Tests (${{ matrix.os }})
    runs-on: ${{ matrix.os }}
    needs: lint
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.9', '3.10', '3.11']

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Cache pip dependencies
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ matrix.python-version }}-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-${{ matrix.python-version }}-
            ${{ runner.os }}-pip-

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-asyncio

      - name: Run unit tests with coverage
        run: |
          pytest tests/unit/ -v --cov=src --cov-report=xml --cov-report=html

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
          flags: unittests
          name: codecov-${{ matrix.os }}-${{ matrix.python-version }}

  # ─────────────────────────────────────────────────────────────
  # Job 3: Integration Tests
  # ─────────────────────────────────────────────────────────────
  test-integration:
    name: 🔗 Integration Tests
    runs-on: ubuntu-latest
    needs: test-unit
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: rustchain_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-asyncio

      - name: Wait for database
        run: |
          until pg_isready -h localhost -p 5432; do
            echo "Waiting for PostgreSQL..."
            sleep 2
          done

      - name: Run integration tests
        env:
          DATABASE_URL: postgresql://postgres:testpass@localhost:5432/rustchain_test
          RUSTCHAIN_TEST_MODE: true
        run: |
          pytest tests/integration/ -v --tb=short

  # ─────────────────────────────────────────────────────────────
  # Job 4: RustChain API Tests
  # ─────────────────────────────────────────────────────────────
  test-rustchain-api:
    name: ⛓️ RustChain API Tests
    runs-on: ubuntu-latest
    needs: test-integration
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-asyncio

      - name: Run RustChain API tests
        env:
          RUSTCHAIN_API_KEY: ${{ secrets.RUSTCHAIN_API_KEY }}
          RUSTCHAIN_NODE_URL: https://node1.rustchain.org
        run: |
          pytest tests/rustchain_api/ -v --tb=short

      - name: Verify miner registration
        run: |
          python -c "
          import requests
          response = requests.get('https://node1.rustchain.org/api/miners')
          assert response.status_code == 200
          print('✅ Miner API verification passed')
          "

  # ─────────────────────────────────────────────────────────────
  # Job 5: Build & Package
  # ─────────────────────────────────────────────────────────────
  build:
    name: 📦 Build Package
    runs-on: ubuntu-latest
    needs: [test-integration, test-rustchain-api]
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install build tools
        run: |
          python -m pip install --upgrade pip
          pip install build wheel twine

      - name: Build package
        run: python -m build

      - name: Verify package
        run: twine check dist/*

      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: python-package
          path: dist/
```

---

## Deployment Pipeline

### CD Workflow (`.github/workflows/cd.yml`)

```yaml
name: RustChain CD Pipeline

on:
  workflow_run:
    workflows: ["RustChain CI Pipeline"]
    types:
      - completed
    branches: [main]

env:
  REGISTRY: docker.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # ─────────────────────────────────────────────────────────────
  # Job 1: Build Docker Image
  # ─────────────────────────────────────────────────────────────
  build-docker:
    name: 🐳 Build Docker Image
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix=
            type=ref,event=branch
            type=semver,pattern={{version}}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=registry,ref=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:buildcache
          cache-to: type=registry,ref=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:buildcache,mode=max

  # ─────────────────────────────────────────────────────────────
  # Job 2: Deploy to Staging
  # ─────────────────────────────────────────────────────────────
  deploy-staging:
    name: 🚀 Deploy to Staging
    runs-on: ubuntu-latest
    needs: build-docker
    environment:
      name: staging
      url: https://staging.rustchain.org

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Deploy to staging server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.STAGING_HOST }}
          username: ${{ secrets.STAGING_USER }}
          key: ${{ secrets.DEPLOY_SSH_KEY }}
          script: |
            cd /opt/rustchain/staging
            docker-compose pull
            docker-compose up -d
            echo "✅ Staging deployment complete"

      - name: Health check
        run: |
          until curl -f https://staging.rustchain.org/health; do
            echo "Waiting for staging to be healthy..."
            sleep 5
          done
          echo "✅ Staging health check passed"

  # ─────────────────────────────────────────────────────────────
  # Job 3: Deploy to Production (Manual Approval)
  # ─────────────────────────────────────────────────────────────
  deploy-production:
    name: 🎯 Deploy to Production
    runs-on: ubuntu-latest
    needs: deploy-staging
    environment:
      name: production
      url: https://rustchain.org
    if: github.ref == 'refs/heads/main'

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Deploy to production server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.PROD_HOST }}
          username: ${{ secrets.PROD_USER }}
          key: ${{ secrets.DEPLOY_SSH_KEY }}
          script: |
            cd /opt/rustchain/production
            docker-compose pull
            docker-compose up -d
            echo "✅ Production deployment complete"

      - name: Verify deployment
        run: |
          curl -f https://rustchain.org/health || exit 1
          echo "✅ Production health check passed"

      - name: Notify deployment success
        if: success()
        run: |
          echo "::notice::Production deployment successful for ${{ github.sha }}"
```

---

## Security Scanning

### Security Workflow (`.github/workflows/security.yml`)

```yaml
name: RustChain Security Scanning

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight

jobs:
  # ─────────────────────────────────────────────────────────────
  # Job 1: Python Dependency Scan
  # ─────────────────────────────────────────────────────────────
  security-python:
    name: 🐍 Python Security Scan
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pip-audit safety bandit

      - name: Run pip-audit
        run: |
          pip-audit --format json > pip-audit-report.json || true
          cat pip-audit-report.json

      - name: Run Safety
        run: |
          safety check --json > safety-report.json || true
          cat safety-report.json

      - name: Run Bandit (security linter)
        run: |
          bandit -r src/ -f json -o bandit-report.json || true

      - name: Upload security reports
        uses: actions/upload-artifact@v4
        with:
          name: security-reports-python
          path: |
            pip-audit-report.json
            safety-report.json
            bandit-report.json

  # ─────────────────────────────────────────────────────────────
  # Job 2: Rust Dependency Scan
  # ─────────────────────────────────────────────────────────────
  security-rust:
    name: 🦀 Rust Security Scan
    runs-on: ubuntu-latest
    if: hashFiles('Cargo.toml') != ''

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install Rust
        uses: actions-rs/toolchain@v1
        with:
          toolchain: stable

      - name: Install cargo-audit
        run: cargo install cargo-audit

      - name: Run cargo audit
        run: |
          cargo audit --json > cargo-audit-report.json || true
          cat cargo-audit-report.json

      - name: Upload security reports
        uses: actions/upload-artifact@v4
        with:
          name: security-reports-rust
          path: cargo-audit-report.json

  # ─────────────────────────────────────────────────────────────
  # Job 3: CodeQL Analysis
  # ─────────────────────────────────────────────────────────────
  codeql:
    name: 🔬 CodeQL Analysis
    runs-on: ubuntu-latest
    permissions:
      actions: read
      contents: read
      security-events: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: python

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3
        with:
          category: "/language:python"

  # ─────────────────────────────────────────────────────────────
  # Job 4: Secret Detection
  # ─────────────────────────────────────────────────────────────
  secret-detection:
    name: 🔐 Secret Detection
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITLEAKS_LICENSE: ${{ secrets.GITLEAKS_LICENSE }}

      - name: Run TruffleHog
        run: |
          pip install truffleHog
          trufflehog --regex --entropy=False . || true
```

---

## Release Automation

### Release Workflow (`.github/workflows/release.yml`)

```yaml
name: RustChain Release Automation

on:
  push:
    tags:
      - 'v*.*.*'

permissions:
  contents: write
  packages: write

jobs:
  # ─────────────────────────────────────────────────────────────
  # Job 1: Create Release
  # ─────────────────────────────────────────────────────────────
  release:
    name: 📝 Create Release
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Generate changelog
        run: |
          pip install git-changelog
          git-changelog --output CHANGELOG_RELEASE.md

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          body_path: CHANGELOG_RELEASE.md
          generate_release_notes: true
          files: |
            dist/*

  # ─────────────────────────────────────────────────────────────
  # Job 2: Publish to PyPI
  # ─────────────────────────────────────────────────────────────
  publish-pypi:
    name: 📦 Publish to PyPI
    runs-on: ubuntu-latest
    needs: release

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install build tools
        run: |
          python -m pip install --upgrade pip
          pip install build twine

      - name: Build package
        run: python -m build

      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
        run: twine upload dist/*

  # ─────────────────────────────────────────────────────────────
  # Job 3: Publish Docker Image
  # ─────────────────────────────────────────────────────────────
  publish-docker:
    name: 🐳 Publish Docker
    runs-on: ubuntu-latest
    needs: release

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Extract version from tag
        id: version
        run: echo "VERSION=${GITHUB_REF#refs/tags/v}" >> $GITHUB_OUTPUT

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/rustchain:${{ steps.version.outputs.VERSION }}
            ${{ secrets.DOCKER_USERNAME }}/rustchain:latest
```

---

## Monitoring & Alerts

### Monitoring Workflow (`.github/workflows/monitoring.yml`)

```yaml
name: RustChain Monitoring

on:
  schedule:
    - cron: '*/15 * * * *'  # Every 15 minutes
  workflow_dispatch:

jobs:
  # ─────────────────────────────────────────────────────────────
  # Job 1: API Health Check
  # ─────────────────────────────────────────────────────────────
  api-health:
    name: 🏥 API Health Check
    runs-on: ubuntu-latest

    steps:
      - name: Check Node 1
        run: |
          response=$(curl -s -o /dev/null -w "%{http_code}" https://node1.rustchain.org/health)
          if [ "$response" != "200" ]; then
            echo "::error::Node 1 health check failed with status $response"
            exit 1
          fi
          echo "✅ Node 1 healthy"

      - name: Check Node 2
        run: |
          response=$(curl -s -o /dev/null -w "%{http_code}" https://node2.rustchain.org/health)
          if [ "$response" != "200" ]; then
            echo "::error::Node 2 health check failed with status $response"
            exit 1
          fi
          echo "✅ Node 2 healthy"

      - name: Check Epoch Status
        run: |
          response=$(curl -s https://node1.rustchain.org/api/epoch)
          echo "Current epoch: $response"

  # ─────────────────────────────────────────────────────────────
  # Job 2: Performance Metrics
  # ─────────────────────────────────────────────────────────────
  performance:
    name: 📊 Performance Metrics
    runs-on: ubuntu-latest

    steps:
      - name: Measure API Response Time
        run: |
          start=$(date +%s%N)
          curl -s https://node1.rustchain.org/api/health > /dev/null
          end=$(date +%s%N)
          duration=$(( (end - start) / 1000000 ))
          echo "API response time: ${duration}ms"
          if [ $duration -gt 1000 ]; then
            echo "::warning::API response time exceeds 1000ms"
          fi

  # ─────────────────────────────────────────────────────────────
  # Job 3: Alert on Failures
  # ─────────────────────────────────────────────────────────────
  alert:
    name: 🚨 Send Alerts
    runs-on: ubuntu-latest
    needs: [api-health, performance]
    if: failure()

    steps:
      - name: Send Feishu Alert
        run: |
          curl -X POST "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK" \
            -H "Content-Type: application/json" \
            -d '{
              "msg_type": "text",
              "content": {
                "text": "🚨 RustChain CI/CD Alert: Health check failed!\nWorkflow: ${{ github.workflow }}\nRun: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
              }
            }'

      - name: Send Email Alert
        uses: dawidd6/action-send-mail@v3
        with:
          server_address: smtp.gmail.com
          server_port: 587
          username: ${{ secrets.SMTP_USERNAME }}
          password: ${{ secrets.SMTP_PASSWORD }}
          subject: "RustChain CI/CD Alert"
          body: "Health check failed. Check: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
          to: ${{ secrets.ALERT_EMAIL }}
          from: RustChain CI/CD
```

---

## Best Practices

### 1. Workflow Optimization

```yaml
# ✅ Use job dependencies to parallelize where possible
jobs:
  lint:
    # Runs first
  test:
    needs: lint  # Waits for lint
  deploy:
    needs: test  # Waits for test

# ✅ Use caching for dependencies
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}

# ✅ Use matrix builds for multi-platform testing
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    python-version: ['3.9', '3.10', '3.11']
```

### 2. Security Best Practices

```yaml
# ✅ Use OIDC for cloud authentication instead of long-lived secrets
- uses: azure/login@v1
  with:
    client-id: ${{ secrets.AZURE_CLIENT_ID }}
    tenant-id: ${{ secrets.AZURE_TENANT_ID }}
    subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

# ✅ Scan for secrets before pushing
- uses: gitleaks/gitleaks-action@v2

# ✅ Use Dependabot for automated dependency updates
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
```

### 3. Cost Optimization

```yaml
# ✅ Use self-hosted runners for frequent workflows
runs-on: self-hosted

# ✅ Cancel redundant workflows
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

# ✅ Use appropriate runner sizes
runs-on: ubuntu-latest  # Default is fine for most cases
# runs-on: ubuntu-latest-4-cores  # For heavy builds
```

### 4. RustChain-Specific Tips

```yaml
# ✅ Always verify miner registration before running tests
- name: Verify Miner
  run: |
    python -c "
    import requests
    response = requests.get('https://node1.rustchain.org/api/miners')
    miners = response.json()
    print(f'Active miners: {len(miners)}')
    "

# ✅ Use test mode for API calls
env:
  RUSTCHAIN_TEST_MODE: true
  RUSTCHAIN_NODE_URL: https://testnet.rustchain.org

# ✅ Cache RustChain CLI downloads
- uses: actions/cache@v4
  with:
    path: ~/.rustchain
    key: ${{ runner.os }}-rustchain-cli-${{ hashFiles('**/rustchain-version.txt') }}
```

---

## Troubleshooting

### Common Issues

#### 1. Workflow Not Triggering

**Problem:** Workflow doesn't run on push/PR

**Solution:**
```yaml
# Ensure correct trigger configuration
on:
  push:
    branches: [main, develop]  # Must match your branch names
  pull_request:
    branches: [main]
```

#### 2. Secrets Not Available

**Problem:** `${{ secrets.MY_SECRET }}` is empty

**Solution:**
1. Go to `Settings > Secrets and variables > Actions`
2. Add the secret with exact name
3. Ensure workflow has `permissions` to access secrets
4. For forked repos, secrets are not passed by default

#### 3. Docker Build Fails

**Problem:** Docker image build fails in CI

**Solution:**
```yaml
# Enable BuildKit for better caching
- uses: docker/setup-buildx-action@v3

# Use cache-from and cache-to
- uses: docker/build-push-action@v5
  with:
    cache-from: type=registry,ref=user/app:buildcache
    cache-to: type=registry,ref=user/app:buildcache,mode=max
```

#### 4. Tests Pass Locally but Fail in CI

**Problem:** Inconsistent test results

**Solution:**
```yaml
# Ensure same environment
env:
  PYTHON_VERSION: '3.11'
  DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test

# Use fixed versions for dependencies
pip install -r requirements.txt  # Ensure requirements.txt is pinned

# Add debug output
- name: Debug Environment
  run: |
    python --version
    pip list
    env | sort
```

#### 5. Deployment Fails

**Problem:** SSH deployment doesn't work

**Solution:**
```yaml
# Ensure SSH key has correct permissions
- name: Setup SSH
  run: |
    mkdir -p ~/.ssh
    echo "${{ secrets.DEPLOY_SSH_KEY }}" > ~/.ssh/id_rsa
    chmod 600 ~/.ssh/id_rsa
    ssh-keyscan -H ${{ secrets.DEPLOY_HOST }} >> ~/.ssh/known_hosts

# Test SSH connection
- name: Test SSH
  run: ssh -o StrictHostKeyChecking=no ${{ secrets.DEPLOY_USER }}@${{ secrets.DEPLOY_HOST }} "echo 'Connection successful'"
```

### Debug Mode

Enable debug logging for workflows:

```yaml
# Add to workflow job
- name: Enable Debug
  run: echo "::debug::Debug mode enabled"

# Set environment variable for verbose output
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true
```

### View Workflow Logs

1. Go to repository `Actions` tab
2. Select the workflow run
3. Click on individual job to see logs
4. Download logs for offline analysis

---

## Appendix

### A. Complete File Structure

```
.github/
├── workflows/
│   ├── ci.yml              # Main CI pipeline
│   ├── cd.yml              # Deployment pipeline
│   ├── security.yml        # Security scanning
│   ├── release.yml         # Release automation
│   └── monitoring.yml      # Health checks
├── dependabot.yml          # Automated dependency updates
└── CODEOWNERS              # Code ownership
```

### B. Dependabot Configuration

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "09:00"
      timezone: "UTC"
    open-pull-requests-limit: 10
    labels:
      - "dependencies"
      - "security"
    commit-message:
      prefix: "chore(deps)"

  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

### C. CODEOWNERS

```
# .github/CODEOWNERS
# Default owners for all files
* @rustchain-maintainers

# Specific path owners
/docs/ @rustchain-docs
/src/api/ @rustchain-api-team
/tests/ @rustchain-qa
.github/workflows/ @rustchain-devops
```

### D. Quick Start Checklist

- [ ] Copy workflow files to `.github/workflows/`
- [ ] Configure repository secrets
- [ ] Test workflows on a feature branch
- [ ] Enable branch protection rules
- [ ] Set up Dependabot
- [ ] Configure CODEOWNERS
- [ ] Add repository to monitoring dashboard
- [ ] Document deployment process

---

## Related Issues

- Issue #1591: Create a GitHub Action workflow for any Elyan Labs repo
- Issue #1613: Set up Dependabot or Renovate for any Elyan Labs repo
- Issue #1678: RustChain dependency management guide

---

**Document Version:** 1.0.0  
**Last Updated:** 2026-03-12  
**Maintainer:** RustChain DevOps Team  
**License:** MIT

---

*Ready for review! ✅*
