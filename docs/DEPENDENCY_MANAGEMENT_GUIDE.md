# RustChain 依赖管理指南

> **奖励：** 3 RTC  
> **状态：** ✅ 完成  
> **最后更新：** 2026-03-12

本指南提供 RustChain 项目中 Python 和 Rust 依赖管理的完整最佳实践，涵盖依赖更新、安全审计和版本锁定。

---

## 📋 目录

1. [Python 依赖管理](#python-依赖管理)
2. [Rust 依赖管理](#rust-依赖管理)
3. [安全审计](#安全审计)
4. [版本锁定策略](#版本锁定策略)
5. [CI/CD 集成](#cicd-集成)
6. [常见问题](#常见问题)

---

## Python 依赖管理

### 1.1 依赖文件结构

RustChain Python 项目使用以下依赖文件：

```
project/
├── pyproject.toml          # 项目元数据和依赖声明（推荐）
├── requirements.txt        # 生产依赖（锁定版本）
├── requirements-dev.txt    # 开发依赖
├── requirements-base.txt   # 基础依赖（未锁定版本）
└── constraints.txt         # 全局版本约束
```

### 1.2 安装依赖

```bash
# 创建虚拟环境（推荐）
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或 .venv\Scripts\activate  # Windows

# 安装生产依赖
pip install -r requirements.txt

# 安装开发依赖
pip install -r requirements-dev.txt

# 使用约束文件安装
pip install -c constraints.txt -r requirements-base.txt
```

### 1.3 添加新依赖

```bash
# 添加到基础依赖文件
echo "package-name>=1.0.0" >> requirements-base.txt

# 或使用 pip 安装后更新依赖列表
pip install package-name
pip freeze > requirements.txt
```

### 1.4 更新依赖

```bash
# 更新所有依赖到最新兼容版本
pip install --upgrade -r requirements-base.txt

# 更新特定包
pip install --upgrade package-name

# 查看可更新的包
pip list --outdated

# 重新生成锁定的依赖文件
pip freeze > requirements.txt
```

### 1.5 使用 pip-tools（推荐）

```bash
# 安装 pip-tools
pip install pip-tools

# 编译依赖（从 requirements.in 生成 requirements.txt）
pip-compile requirements-base.in

# 同步环境
pip-sync requirements.txt
```

---

## Rust 依赖管理

### 2.1 Cargo.toml 结构

```toml
[package]
name = "rustchain-component"
version = "0.1.0"
edition = "2024"

[dependencies]
# 语义化版本控制
serde = "1.0"           # >=1.0.0, <2.0.0
serde_json = "1.0.115"  # 精确版本
tokio = { version = "1.0", features = ["full"] }

# Git 依赖
clawrtc-rs = { git = "https://github.com/Scottcjn/clawrtc-rs", branch = "main" }

# 本地路径依赖
local-crate = { path = "../local-crate" }

[dev-dependencies]
criterion = "0.5"

[build-dependencies]
cc = "1.0"
```

### 2.2 版本说明符

| 说明符 | 含义 | 示例 |
|--------|------|------|
| `=` | 精确版本 | `=1.2.3` |
| `>` | 大于 | `>1.2.3` |
| `>=` | 大于等于 | `>=1.2.3` |
| `<` | 小于 | `<2.0.0` |
| `^` | 兼容版本（默认） | `^1.2.3` (= `>=1.2.3, <2.0.0`) |
| `~` | 近似版本 | `~1.2.3` (= `>=1.2.3, <1.3.0`) |

### 2.3 Cargo.lock 管理

```bash
# 构建项目（自动更新 Cargo.lock）
cargo build

# 更新所有依赖
cargo update

# 更新特定包
cargo update -p package-name

# 更新特定包到特定版本
cargo update -p package-name --precise 1.2.3

# 检查可更新的包
cargo outdated  # 需要 cargo-outdated
```

### 2.4 依赖树查看

```bash
# 查看依赖树
cargo tree

# 查看特定包的依赖
cargo tree -p package-name

# 查找重复依赖
cargo tree --duplicates

# 反向查找（谁依赖这个包）
cargo tree -i package-name

# 导出依赖图为文本
cargo tree > dependencies.txt
```

---

## 安全审计

### 3.1 Python 安全审计

#### 使用 pip-audit

```bash
# 安装
pip install pip-audit

# 审计当前环境
pip-audit

# 审计 requirements.txt
pip-audit -r requirements.txt

# 输出详细报告
pip-audit -r requirements.txt -v

# 输出 JSON 格式
pip-audit -r requirements.txt --format json

# 自动修复（升级有漏洞的包）
pip-audit --fix
```

#### 使用 Safety

```bash
# 安装
pip install safety

# 审计
safety check

# 审计 requirements 文件
safety check -r requirements.txt

# 生成完整报告
safety check --full-report

# 忽略特定漏洞
safety check --ignore 12345 --ignore 67890
```

#### 使用 GitHub Dependabot

在 `.github/dependabot.yml` 中配置：

```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    reviewers:
      - "security-team"
```

### 3.2 Rust 安全审计

#### 使用 cargo-audit

```bash
# 安装
cargo install cargo-audit

# 审计项目
cargo audit

# 输出 JSON 格式
cargo audit --json

# 忽略特定漏洞（创建 .cargo/audit.toml）
cargo audit --ignore RUSTSEC-2020-0001

# 定期审计（添加到 CI）
cargo audit --deny warnings
```

#### 使用 cargo-deny

```bash
# 安装
cargo install cargo-deny

# 检查许可证和漏洞
cargo deny check

# 仅检查漏洞
cargo deny check advisories

# 检查许可证
cargo deny check licenses

# 检查重复依赖
cargo deny check bans
```

#### 创建 deny.toml 配置

```toml
[advisories]
vulnerability = "deny"
unmaintained = "warn"
yanked = "warn"
notice = "warn"
ignore = [
    "RUSTSEC-2020-0001",  # 忽略特定漏洞
]

[licenses]
allow = [
    "MIT",
    "Apache-2.0",
    "BSD-3-Clause",
]

[bans]
multiple-versions = "warn"
deny = [
    { name = "insecure-crate" },
]
```

### 3.3 GitHub Security Alerts

启用 GitHub Advanced Security：

1. 进入仓库 Settings → Security & analysis
2. 启用 Dependabot alerts
3. 启用 Dependabot security updates
4. 启用 Code scanning（可选）

---

## 版本锁定策略

### 4.1 Python 版本锁定

#### 策略 1：完全锁定（生产环境）

```txt
# requirements.txt
package-name==1.2.3
another-package==4.5.6
```

**优点：** 完全可重现的构建  
**缺点：** 需要手动更新

#### 策略 2：混合锁定

```txt
# requirements-base.txt（开发用）
package-name>=1.2.0,<2.0.0
another-package~=4.5.0

# requirements.txt（生产用，由 pip-compile 生成）
package-name==1.2.3
another-package==4.5.6
```

**优点：** 平衡灵活性和稳定性  
**推荐：** ✅ RustChain 使用此策略

### 4.2 Rust 版本锁定

#### Cargo.lock 提交策略

| 项目类型 | 提交 Cargo.lock? | 原因 |
|----------|------------------|------|
| 应用程序 | ✅ 是 | 确保可重现构建 |
| 库 | ❌ 否 | 让使用者解析依赖 |
| 工作空间 | ✅ 是 | 保持内部一致性 |

**RustChain 策略：** 提交 Cargo.lock（我们是应用程序）

#### 版本更新工作流

```bash
# 1. 定期更新依赖（每周）
cargo update

# 2. 运行测试
cargo test

# 3. 运行审计
cargo audit

# 4. 提交更新
git add Cargo.lock
git commit -m "chore: update dependencies"
```

### 4.3 语义化版本控制

遵循 [SemVer 2.0.0](https://semver.org/)：

- **MAJOR.MINOR.PATCH** (例如：1.2.3)
- **MAJOR**：不兼容的 API 变更
- **MINOR**：向后兼容的功能新增
- **PATCH**：向后兼容的问题修复

**RustChain 约定：**

```toml
# 库依赖：允许 MINOR 和 PATCH 更新
serde = "1.0"        # >=1.0.0, <2.0.0

# 关键依赖：锁定 PATCH
critical-lib = "1.2.3"  # 精确版本

# 开发依赖：允许最新
criterion = "0.5"    # >=0.5.0, <0.6.0
```

---

## CI/CD 集成

### 5.1 GitHub Actions 工作流

创建 `.github/workflows/dependencies.yml`：

```yaml
name: Dependency Management

on:
  schedule:
    - cron: '0 2 * * 1'  # 每周一 2:00 UTC
  workflow_dispatch:

jobs:
  python-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pip-audit safety
      
      - name: Run pip-audit
        run: pip-audit -r requirements.txt
      
      - name: Run Safety
        run: safety check -r requirements.txt --full-report

  rust-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install Rust
        uses: dtolnay/rust-action@stable
      
      - name: Install cargo-audit
        run: cargo install cargo-audit
      
      - name: Run cargo audit
        run: cargo audit --deny warnings
      
      - name: Install cargo-deny
        run: cargo install cargo-deny
      
      - name: Run cargo deny
        run: cargo deny check

  update-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check for updates (Python)
        run: |
          pip install --upgrade pip
          pip list --outdated
      
      - name: Check for updates (Rust)
        run: |
          cargo install cargo-outdated
          cargo outdated
```

### 5.2 预提交钩子

创建 `.pre-commit-config.yaml`：

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-yaml
      - id: end-of-file-fixer
  
  - repo: https://github.com/PyCQA/pip-audit
    rev: v2.6.1
    hooks:
      - id: pip-audit
        args: [-r, requirements.txt]
  
  - repo: local
    hooks:
      - id: cargo-audit
        name: cargo audit
        entry: cargo audit
        language: system
        files: Cargo\.toml$
        pass_filenames: false
```

### 5.3 定期更新脚本

创建 `scripts/update-dependencies.sh`：

```bash
#!/bin/bash
set -e

echo "🔄 Updating Python dependencies..."
pip install --upgrade pip
pip install --upgrade -r requirements-base.txt
pip freeze > requirements.txt

echo "🦀 Updating Rust dependencies..."
cargo update

echo "🔒 Running security audits..."
pip-audit -r requirements.txt || echo "⚠️  Python vulnerabilities found"
cargo audit || echo "⚠️  Rust vulnerabilities found"

echo "✅ Update complete!"
```

---

## 常见问题

### Q1: 依赖冲突怎么办？

**Python:**
```bash
# 查看冲突
pip install package-name --dry-run

# 使用约束文件解决
echo "conflicting-package<2.0.0" >> constraints.txt
pip install -c constraints.txt package-name
```

**Rust:**
```bash
# 查看重复依赖
cargo tree --duplicates

# 强制使用特定版本
cargo update -p conflicting-package --precise 1.2.3
```

### Q2: 如何回滚依赖更新？

**Python:**
```bash
# 从 Git 恢复 requirements.txt
git checkout HEAD -- requirements.txt

# 重新安装
pip install -r requirements.txt
```

**Rust:**
```bash
# 从 Git 恢复 Cargo.lock
git checkout HEAD -- Cargo.lock

# 重新构建
cargo build
```

### Q3: 离线环境如何管理依赖？

**Python:**
```bash
# 下载所有依赖
pip download -r requirements.txt -d ./wheels

# 离线安装
pip install --no-index --find-links=./wheels -r requirements.txt
```

**Rust:**
```bash
# 配置 Cargo 镜像（.cargo/config.toml）
[source.crates-io]
replace-with = 'mirror'

[source.mirror]
registry = "sparse+https://mirror.example.com/index/"

# 或 vendoring
cargo vendor ./vendor
```

### Q4: 如何监控新漏洞？

1. **启用 GitHub Security Alerts**
2. **订阅 RustSec 公告：** https://rustsec.org/advisories/
3. **订阅 PyPI Security Advisories：** https://pypi.org/security/
4. **使用 dependabot/renovate 自动 PR**

### Q5: 依赖更新频率建议？

| 依赖类型 | 更新频率 | 说明 |
|----------|----------|------|
| 安全补丁 | ⚠️ 立即 | 发现漏洞后 24 小时内 |
| PATCH 版本 | 每周 | 向后兼容的修复 |
| MINOR 版本 | 每月 | 新功能，需测试 |
| MAJOR 版本 | 每季度 | 破坏性变更，需评估 |

---

## 检查清单

### 新依赖添加前

- [ ] 检查包的健康状况（stars、维护频率、issues）
- [ ] 审查许可证是否兼容
- [ ] 运行安全审计（pip-audit / cargo audit）
- [ ] 评估依赖树大小
- [ ] 文档化添加原因

### 发布前

- [ ] 运行所有安全审计
- [ ] 更新 Cargo.lock / requirements.txt
- [ ] 检查依赖许可证
- [ ] 测试所有功能
- [ ] 生成 SBOM（软件物料清单）

### 定期维护（每月）

- [ ] 检查可更新的依赖
- [ ] 运行安全审计
- [ ] 清理未使用的依赖
- [ ] 更新文档
- [ ] 审查依赖树

---

## 资源链接

- **Python:**
  - [pip 官方文档](https://pip.pypa.io/)
  - [Python Packaging Guide](https://packaging.python.org/)
  - [pip-audit](https://pypi.org/project/pip-audit/)
  - [Safety](https://pyup.io/safety/)

- **Rust:**
  - [Cargo Book](https://doc.rust-lang.org/cargo/)
  - [cargo-audit](https://github.com/rustsec/rustsec)
  - [cargo-deny](https://github.com/EmbarkStudios/cargo-deny)
  - [RustSec Advisory Database](https://rustsec.org/)

- **安全:**
  - [GitHub Advisory Database](https://github.com/advisories)
  - [CVE Database](https://cve.mitre.org/)
  - [OSV Database](https://osv.dev/)

---

## 贡献

本指南由 RustChain 社区维护。发现问题或有改进建议？

- 📝 提交 Issue: https://github.com/Scottcjn/rustchain-bounties/issues
- 🔧 提交 PR: https://github.com/Scottcjn/rustchain-bounties/pulls
- 💬 Discord: https://discord.gg/VqVVS2CW9Q

---

**最后审核：** 2026-03-12  
**维护者：** RustChain Security Team  
**许可证：** MIT
