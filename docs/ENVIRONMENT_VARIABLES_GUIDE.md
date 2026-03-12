# RustChain 环境变量配置指南

> **奖励：** 3 RTC  
> **Issue:** #1682  
> **作者:** 牛 2 (Subagent)

---

## 📋 目录

1. [核心环境变量](#核心环境变量)
2. [配置管理](#配置管理)
3. [安全存储](#安全存储)
4. [最佳实践](#最佳实践)
5. [故障排查](#故障排查)

---

## 🔑 核心环境变量

### 必需变量

| 变量名 | 说明 | 示例值 |
|--------|------|--------|
| `RUSTCHAIN_WALLET` | 矿工钱包地址 | `my-miner-wallet` |
| `RUSTCHAIN_NODE_URL` | 节点 API 地址 | `https://rustchain.org` |
| `RUSTCHAIN_NETWORK` | 网络环境 | `mainnet` / `testnet` |

### 可选变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `RUSTCHAIN_LOG_LEVEL` | 日志级别 | `info` |
| `RUSTCHAIN_DATA_DIR` | 数据存储目录 | `~/.rustchain` |
| `RUSTCHAIN_MINER_ID` | 自定义矿工 ID | 自动生成 |

---

## ⚙️ 配置管理

### 方式一：.env 文件（推荐）

创建 `.env` 文件在项目根目录：

```bash
# .env
RUSTCHAIN_WALLET=my-miner-wallet
RUSTCHAIN_NODE_URL=https://rustchain.org
RUSTCHAIN_NETWORK=mainnet
RUSTCHAIN_LOG_LEVEL=info
```

使用 `python-dotenv` 加载：

```python
from dotenv import load_dotenv
load_dotenv()
```

### 方式二：系统环境变量

**Linux/macOS:**

```bash
# 临时设置（当前终端会话）
export RUSTCHAIN_WALLET="my-miner-wallet"
export RUSTCHAIN_NODE_URL="https://rustchain.org"

# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export RUSTCHAIN_WALLET="my-miner-wallet"' >> ~/.bashrc
source ~/.bashrc
```

**Windows PowerShell:**

```powershell
# 临时设置
$env:RUSTCHAIN_WALLET="my-miner-wallet"

# 永久设置（用户级别）
[System.Environment]::SetEnvironmentVariable('RUSTCHAIN_WALLET', 'my-miner-wallet', 'User')
```

### 方式三：配置文件

创建 `config.toml` 或 `config.yaml`：

```toml
# config.toml
[wallet]
address = "my-miner-wallet"

[node]
url = "https://rustchain.org"
network = "mainnet"

[mining]
log_level = "info"
data_dir = "~/.rustchain"
```

---

## 🔒 安全存储

### 1. 敏感信息加密

**使用 git-crypt:**

```bash
# 安装
git-crypt unlock

# 加密 .env 文件
echo ".env filter=git-crypt diff=git-crypt" >> .gitattributes
git-crypt lock
```

**使用 age 加密:**

```bash
# 生成密钥
age-keygen -o age-key.txt

# 加密 .env
age -R age-key.txt -o .env.age .env

# 解密
age -d -i age-key.txt .env.age
```

### 2. 密钥管理工具

**1Password CLI:**

```bash
# 读取密钥
op read "op://vault/RustChain/credential"

# 注入到环境变量
export RUSTCHAIN_WALLET=$(op read "op://vault/RustChain/wallet")
```

**HashiCorp Vault:**

```bash
# 读取密钥
vault kv get -field=wallet secret/rustchain

# 动态注入
export RUSTCHAIN_WALLET=$(vault kv get -field=wallet secret/rustchain)
```

### 3. .gitignore 配置

```gitignore
# 环境变量文件
.env
.env.local
.env.*.local

# 密钥文件
*.pem
*.key
age-key.txt
*.age

# 配置文件（含敏感信息）
config.local.toml
secrets.yaml
```

---

## ✅ 最佳实践

### 1. 环境分离

```bash
# .env.development
RUSTCHAIN_NETWORK=testnet
RUSTCHAIN_LOG_LEVEL=debug

# .env.production
RUSTCHAIN_NETWORK=mainnet
RUSTCHAIN_LOG_LEVEL=warn
```

### 2. 验证脚本

创建 `verify-env.sh`：

```bash
#!/bin/bash

echo "🔍 验证 RustChain 环境变量..."

# 检查必需变量
required_vars=("RUSTCHAIN_WALLET" "RUSTCHAIN_NODE_URL")

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ 错误：$var 未设置"
        exit 1
    fi
    echo "✅ $var 已设置"
done

# 验证节点连接
echo "🔗 测试节点连接..."
curl -sk "${RUSTCHAIN_NODE_URL}/health" > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ 节点连接正常"
else
    echo "❌ 节点连接失败"
    exit 1
fi

echo "✅ 所有检查通过"
```

### 3. Docker 环境变量

```dockerfile
# Dockerfile
FROM python:3.10-slim

# 使用 ARG 构建时变量
ARG RUSTCHAIN_WALLET
ENV RUSTCHAIN_WALLET=${RUSTCHAIN_WALLET}

# 或使用 --env-file
# docker run --env-file .env rustchain-miner
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  miner:
    image: rustchain-miner
    env_file:
      - .env
    environment:
      - RUSTCHAIN_LOG_LEVEL=info
```

### 4. 轮换策略

```bash
# 定期轮换密钥脚本
#!/bin/bash
# rotate-secrets.sh

echo "🔄 开始轮换密钥..."

# 备份旧配置
cp .env .env.backup.$(date +%Y%m%d)

# 生成新密钥（示例）
# op item update "RustChain" credential=$(openssl rand -hex 32)

# 重启服务
systemctl --user restart rustchain-miner

echo "✅ 密钥轮换完成"
```

---

## 🐛 故障排查

### 常见问题

| 问题 | 解决方案 |
|------|----------|
| 变量未找到 | 检查 `.env` 文件路径，确认 `load_dotenv()` 调用 |
| 节点连接失败 | 验证 `RUSTCHAIN_NODE_URL` 是否正确，检查防火墙 |
| 钱包余额为 0 | 确认 `RUSTCHAIN_WALLET` 名称正确，检查是否已创建 |
| HTTPS 证书错误 | 使用 `-sk` 标志（自签名证书），或更新 CA 证书 |

### 调试命令

```bash
# 查看所有 RustChain 相关变量
env | grep RUSTCHAIN

# 测试钱包余额
curl -sk "https://rustchain.org/wallet/balance?miner_id=$RUSTCHAIN_WALLET"

# 检查节点健康
curl -sk https://rustchain.org/health

# 查看矿工日志
journalctl --user -u rustchain-miner -f
```

---

## 📚 参考资源

- [RustChain 主仓库](https://github.com/Scottcjn/RustChain)
- [安装脚本](https://raw.githubusercontent.com/Scottcjn/RustChain/main/install-miner.sh)
- [区块浏览器](https://rustchain.org/explorer)
- [Discord 社区](https://discord.gg/VqVVS2CW9Q)

---

## 📝 更新日志

| 日期 | 版本 | 说明 |
|------|------|------|
| 2026-03-12 | 1.0.0 | 初始版本，涵盖配置管理、安全存储、最佳实践 |

---

**奖励支付信息：**
- PayPal: 待提供
- RTC 钱包地址：待提供

*本指南遵循 RustChain 社区标准，欢迎提交 PR 改进。*
