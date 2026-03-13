# RustChain API Quick Reference

> 快速参考文档 - RustChain 区块链 API 端点和使用示例  
> 奖励：3 RTC  
> 作者：牛 2 (AutoClaw Agent)

---

## 📋 目录

1. [基础信息](#基础信息)
2. [节点健康检查](#节点健康检查)
3. [钱包 API](#钱包-api)
4. [矿工 API](#矿工-api)
5. [治理 API](#治理-api)
6. [高级 API](#高级-api)
7. [代码示例](#代码示例)

---

## 🔧 基础信息

### 节点地址

| 节点 | 地址 | 角色 |
|------|------|------|
| Node 1 | `https://rustchain.org` | 主节点 + 浏览器 |
| Node 2 | `https://50.28.86.153` | Ergo 锚点 |
| Node 3 | `https://76.8.228.245` | 社区节点 |

### 重要提示

- ⚠️ 节点可能使用自签名 SSL 证书
- 使用 `curl` 时建议添加 `-sk` 参数（跳过 SSL 验证）
- 1 RTC = $0.10 USD（参考价格）

---

## 🏥 节点健康检查

### 检查节点健康状态

```bash
curl -sk https://rustchain.org/health
```

**响应示例：**
```json
{
  "status": "healthy",
  "node": "Node 1",
  "uptime": "99.9%"
}
```

### 获取当前 epoch

```bash
curl -sk https://rustchain.org/epoch
```

**响应示例：**
```json
{
  "epoch": 12345,
  "slot": 3,
  "blocks_per_epoch": 10
}
```

---

## 💰 钱包 API

### 查询钱包余额

```bash
curl -sk "https://rustchain.org/wallet/balance?miner_id=YOUR_WALLET_NAME"
```

**参数：**
- `miner_id` - 钱包名称/矿工 ID

**响应示例：**
```json
{
  "miner_id": "my-wallet",
  "balance": 150.50,
  "currency": "RTC"
}
```

### 创建 Coinbase 钱包（x402 协议）

```bash
# 安装 clawrtc
pip install clawrtc[coinbase]

# 创建钱包
clawrtc wallet coinbase create

# 查看交换信息
clawrtc wallet coinbase swap-info

# 链接现有 Base 地址
clawrtc wallet coinbase link 0xYourBaseAddress
```

---

## ⛏️ 矿工 API

### 列出活跃矿工

```bash
curl -sk https://rustchain.org/api/miners
```

**响应示例：**
```json
{
  "miners": [
    {
      "miner_id": "miner-001",
      "architecture": "PowerPC G4",
      "multiplier": 2.5,
      "last_attest": "2026-03-12T11:00:00Z"
    },
    {
      "miner_id": "miner-002",
      "architecture": "x86_64",
      "multiplier": 1.0,
      "last_attest": "2026-03-12T11:05:00Z"
    }
  ],
  "total_active": 2
}
```

### 硬件乘数参考

| 硬件 | 时代 | 乘数 | 每 epoch 收益 |
|------|------|------|-------------|
| PowerPC G4 | 1999-2005 | 2.5× | 0.30 RTC |
| PowerPC G5 | 2003-2006 | 2.0× | 0.24 RTC |
| PowerPC G3 | 1997-2003 | 1.8× | 0.21 RTC |
| IBM POWER8 | 2014 | 1.5× | 0.18 RTC |
| Pentium 4 | 2000-2008 | 1.5× | 0.18 RTC |
| Core 2 Duo | 2006-2011 | 1.3× | 0.16 RTC |
| Apple Silicon | 2020+ | 1.2× | 0.14 RTC |
| Modern x86_64 | Current | 1.0× | 0.12 RTC |

> ⚠️ 乘数每年衰减 15% 以防止永久优势

---

## 🗳️ 治理 API

### 创建提案

```bash
curl -sk -X POST https://rustchain.org/governance/propose \
  -H 'Content-Type: application/json' \
  -d '{
    "wallet": "RTC...",
    "title": "Enable parameter X",
    "description": "Rationale and implementation details"
  }'
```

**要求：**
- 钱包持有 > 10 RTC

### 列出所有提案

```bash
curl -sk https://rustchain.org/governance/proposals
```

**响应示例：**
```json
{
  "proposals": [
    {
      "id": 1,
      "title": "Enable parameter X",
      "status": "active",
      "yes_weight": 150,
      "no_weight": 50,
      "ends_at": "2026-03-19T00:00:00Z"
    }
  ]
}
```

### 获取提案详情

```bash
curl -sk https://rustchain.org/governance/proposal/1
```

### 提交投票

```bash
curl -sk -X POST https://rustchain.org/governance/vote \
  -H 'Content-Type: application/json' \
  -d '{
    "proposal_id": 1,
    "wallet": "RTC...",
    "vote": "yes",
    "nonce": "1700000000",
    "public_key": "<ed25519_pubkey_hex>",
    "signature": "<ed25519_signature_hex>"
  }'
```

**投票规则：**
- 投票者必须是活跃矿工
- 需要 Ed25519 签名验证
- 权重 = 1 RTC × 硬件乘数
- 通过条件：yes_weight > no_weight

### Web UI

访问治理界面：
```bash
curl -sk https://rustchain.org/governance/ui
```

---

## 🚀 高级 API

### x402 Premium API 端点

这些端点目前免费（测试期间）：

#### 批量视频导出（BoTTube）

```bash
curl -sk https://rustchain.org/api/premium/videos
```

#### 深度代理分析（BoTTube）

```bash
curl -sk https://rustchain.org/api/premium/analytics/
```

#### 完整声誉导出（Beacon Atlas）

```bash
curl -sk https://rustchain.org/api/premium/reputation
```

#### USDC/wRTC 交换信息

```bash
curl -sk https://rustchain.org/wallet/swap-info
```

---

## 💻 代码示例

### Python 示例

```python
import requests
import json

# 禁用 SSL 警告（自签名证书）
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://rustchain.org"

def check_health():
    """检查节点健康状态"""
    response = requests.get(f"{BASE_URL}/health", verify=False)
    return response.json()

def get_epoch():
    """获取当前 epoch"""
    response = requests.get(f"{BASE_URL}/epoch", verify=False)
    return response.json()

def get_wallet_balance(miner_id):
    """查询钱包余额"""
    params = {"miner_id": miner_id}
    response = requests.get(f"{BASE_URL}/wallet/balance", params=params, verify=False)
    return response.json()

def get_active_miners():
    """获取活跃矿工列表"""
    response = requests.get(f"{BASE_URL}/api/miners", verify=False)
    return response.json()

def get_proposals():
    """获取所有提案"""
    response = requests.get(f"{BASE_URL}/governance/proposals", verify=False)
    return response.json()

def create_proposal(wallet, title, description):
    """创建新提案"""
    data = {
        "wallet": wallet,
        "title": title,
        "description": description
    }
    response = requests.post(
        f"{BASE_URL}/governance/propose",
        json=data,
        headers={"Content-Type": "application/json"},
        verify=False
    )
    return response.json()

def submit_vote(proposal_id, wallet, vote, nonce, public_key, signature):
    """提交投票"""
    data = {
        "proposal_id": proposal_id,
        "wallet": wallet,
        "vote": vote,
        "nonce": nonce,
        "public_key": public_key,
        "signature": signature
    }
    response = requests.post(
        f"{BASE_URL}/governance/vote",
        json=data,
        headers={"Content-Type": "application/json"},
        verify=False
    )
    return response.json()

# 使用示例
if __name__ == "__main__":
    print("节点健康状态:", check_health())
    print("当前 epoch:", get_epoch())
    print("钱包余额:", get_wallet_balance("my-wallet"))
    print("活跃矿工:", get_active_miners())
```

### JavaScript/Node.js 示例

```javascript
const axios = require('axios');
const https = require('https');

// 创建 axios 实例（跳过 SSL 验证）
const api = axios.create({
  baseURL: 'https://rustchain.org',
  httpsAgent: new https.Agent({ rejectUnauthorized: false })
});

// 检查节点健康
async function checkHealth() {
  const response = await api.get('/health');
  return response.data;
}

// 获取当前 epoch
async function getEpoch() {
  const response = await api.get('/epoch');
  return response.data;
}

// 查询钱包余额
async function getWalletBalance(minerId) {
  const response = await api.get('/wallet/balance', {
    params: { miner_id: minerId }
  });
  return response.data;
}

// 获取活跃矿工
async function getActiveMiners() {
  const response = await api.get('/api/miners');
  return response.data;
}

// 获取提案列表
async function getProposals() {
  const response = await api.get('/governance/proposals');
  return response.data;
}

// 创建提案
async function createProposal(wallet, title, description) {
  const response = await api.post('/governance/propose', {
    wallet,
    title,
    description
  });
  return response.data;
}

// 提交投票
async function submitVote(proposalId, wallet, vote, nonce, publicKey, signature) {
  const response = await api.post('/governance/vote', {
    proposal_id: proposalId,
    wallet,
    vote,
    nonce,
    public_key: publicKey,
    signature
  });
  return response.data;
}

// 使用示例
(async () => {
  console.log('节点健康状态:', await checkHealth());
  console.log('当前 epoch:', await getEpoch());
  console.log('钱包余额:', await getWalletBalance('my-wallet'));
  console.log('活跃矿工:', await getActiveMiners());
})();
```

### Shell 脚本示例

```bash
#!/bin/bash

# RustChain API 快速测试脚本

BASE_URL="https://rustchain.org"
CURL="curl -sk"

echo "=== RustChain API 测试 ==="
echo ""

# 1. 检查健康状态
echo "1️⃣  节点健康状态:"
$CURL "$BASE_URL/health" | jq .
echo ""

# 2. 获取当前 epoch
echo "2️⃣  当前 epoch:"
$CURL "$BASE_URL/epoch" | jq .
echo ""

# 3. 列出活跃矿工
echo "3️⃣  活跃矿工:"
$CURL "$BASE_URL/api/miners" | jq .
echo ""

# 4. 查询钱包余额（替换 YOUR_WALLET）
echo "4️⃣  钱包余额:"
$CURL "$BASE_URL/wallet/balance?miner_id=YOUR_WALLET" | jq .
echo ""

# 5. 获取治理提案
echo "5️⃣  治理提案:"
$CURL "$BASE_URL/governance/proposals" | jq .
echo ""

echo "=== 测试完成 ==="
```

---

## 🔗 相关资源

| 资源 | 链接 |
|------|------|
| GitHub 主仓库 | https://github.com/Scottcjn/Rustchain |
| 赏金任务 | https://github.com/Scottcjn/rustchain-bounties |
| 区块浏览器 | https://rustchain.org/explorer |
| Discord 社区 | https://discord.gg/VqVVS2CW9Q |
| 官方网站 | https://rustchain.org |

### wRTC (Solana)

| 资源 | 链接 |
|------|------|
| Raydium 交换 | https://raydium.io/swap/?inputMint=sol&outputMint=12TAdKXxcGf6oCv4rqDz2NkgxjyHq6HQKoxKZYGf5i4X |
| DexScreener 图表 | https://dexscreener.com/solana/8CF2Q8nSCxRacDShbtF86XTSrYjueBMKmfdR3MLdnYzb |
| BoTTube 桥接 | https://bottube.ai/bridge |
| Token Mint | `12TAdKXxcGf6oCv4rqDz2NkgxjyHq6HQKoxKZYGf5i4X` |

### wRTC (Base)

| 资源 | 链接 |
|------|------|
| Base 桥接 | https://bottube.ai/bridge/base |
| Aerodrome 交换 | https://aerodrome.finance/swap?from=0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913&to=0x5683C10596AaA09AD7F4eF13CAB94b9b74A669c6 |
| wRTC 合约地址 | `0x5683C10596AaA09AD7F4eF13CAB94b9b74A669c6` |

---

## 📝 常见问题

### Q: 为什么使用 `-sk` 参数？

A: RustChain 节点可能使用自签名 SSL 证书。`-s` 静默模式，`-k` 跳过 SSL 验证。

### Q: 如何安装矿工？

```bash
curl -sSL https://raw.githubusercontent.com/Scottcjn/Rustchain/main/install-miner.sh | bash
```

### Q: 如何管理矿工服务？

**Linux (systemd):**
```bash
systemctl --user status rustchain-miner  # 查看状态
systemctl --user stop rustchain-miner    # 停止
systemctl --user start rustchain-miner   # 启动
journalctl --user -u rustchain-miner -f  # 查看日志
```

**macOS (launchd):**
```bash
launchctl list | grep rustchain          # 查看状态
launchctl stop com.rustchain.miner       # 停止
launchctl start com.rustchain.miner      # 启动
tail -f ~/.rustchain/miner.log           # 查看日志
```

### Q: 治理提案规则是什么？

- **创建要求:** 钱包持有 > 10 RTC
- **投票资格:** 必须是活跃矿工
- **投票权重:** 1 RTC × 硬件乘数
- **通过条件:** yes_weight > no_weight
- **提案周期:** Draft → Active (7 天) → Passed/Failed

---

## 📄 许可证

本文档由 AutoClaw 代理生成，用于 rustchain-bounties #1655 任务。

**奖励:** 3 RTC  
**作者:** 牛 2 (牛马主管的 subagent)  
**日期:** 2026-03-12

---

*Made with ⚡ by RustChain - Proof of Antiquity*
