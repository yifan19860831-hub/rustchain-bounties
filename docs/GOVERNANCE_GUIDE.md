# RustChain 治理指南

> **奖励：** 5 RTC  
> **Issue：** #1652  
> **状态：** 已完成

本指南说明如何参与 RustChain 的去中心化治理，包括提案创建、投票流程和社区参与。

---

## 目录

1. [治理概述](#治理概述)
2. [投票机制](#投票机制)
3. [提案流程](#提案流程)
4. [参与方式](#参与方式)
5. [API 参考](#api-参考)
6. [最佳实践](#最佳实践)

---

## 治理概述

RustChain 采用**基于硬件的链上治理**模型，核心原则：

- **一设备一票**：每个独特的硬件设备每轮次获得 1 票
- **资历加权**：投票权重乘以硬件资历乘数（古董硬件权重更高）
- **活跃矿工资格**：只有经过认证的活跃矿工才能参与投票
- **公开透明**：所有提案和投票记录在链上可查

### 治理代币：RTC

- 1 RTC = 1 基础投票权
- 最终权重 = RTC 持有量 × 硬件资历乘数
- 硬件乘数范围：1.0×（现代设备）到 2.5×（PowerPC G3/G4）

---

## 投票机制

### 投票资格

| 要求 | 说明 |
|------|------|
| 活跃矿工 | 必须是通过硬件指纹认证的矿工 |
| 钱包持有 | 提案创建者需持有 >10 RTC |
| 签名验证 | 投票需要 Ed25519 签名 |

### 投票权重计算

```
投票权重 = (持有 RTC 数量) × (硬件资历乘数)

硬件资历乘数示例：
- PowerPC G3/G4 (1997-2005): 2.5×
- PowerPC G5 (2003-2006): 2.0×
- IBM POWER8 (2014): 1.5×
- Pentium 4 (2000-2008): 1.5×
- Core 2 Duo (2006-2011): 1.3×
- Apple Silicon (2020+): 1.2×
- 现代 x86_64: 1.0×
```

### 投票流程

1. **查看提案**：浏览 `/governance/proposals` 获取所有提案
2. **签名投票**：使用 Ed25519 私钥对投票签名
3. **提交投票**：POST 到 `/governance/vote` 端点
4. **等待结果**：提案活跃期 7 天，结束后自动结算

### 通过条件

```
提案通过：yes_weight > no_weight

其中：
- yes_weight = 所有赞成票的权重之和
- no_weight = 所有反对票的权重之和
```

---

## 提案流程

### 提案生命周期

```
草稿 (Draft) → 活跃 (Active, 7 天) → 通过/失败 (Passed/Failed)
```

### 创建提案

**前置条件：**
- 钱包持有 >10 RTC
- 是活跃矿工

**步骤：**

```bash
# 1. 准备提案内容
{
  "wallet": "RTC-your-wallet-address",
  "title": "启用参数 X 调整",
  "description": "详细说明调整理由、技术实现、预期影响"
}

# 2. 提交提案
curl -sk -X POST https://rustchain.org/governance/propose \
  -H 'Content-Type: application/json' \
  -d '{
    "wallet": "RTC-your-wallet",
    "title": "Enable parameter X adjustment",
    "description": "Rationale and implementation details"
  }'
```

### 提案内容要求

| 字段 | 必填 | 说明 |
|------|------|------|
| wallet | ✅ | 提案者钱包地址 |
| title | ✅ | 简洁的提案标题（<100 字符） |
| description | ✅ | 详细说明（建议包含技术细节、影响评估） |

### 提案最佳实践

1. **清晰的问题陈述**：说明要解决什么问题
2. **技术方案**：提供具体的实现思路
3. **影响评估**：说明对网络、矿工、用户的影响
4. **时间规划**：建议的实施时间表
5. **社区讨论**：先在 Discord/论坛征求意见

---

## 参与方式

### 1. 成为矿工（基础参与）

```bash
# 安装矿工
curl -sSL https://raw.githubusercontent.com/Scottcjn/Rustchain/main/install-miner.sh | bash

# 启动挖矿
systemctl --user start rustchain-miner  # Linux
launchctl start com.rustchain.miner     # macOS
```

### 2. 参与投票

```bash
# 查看当前提案
curl -sk https://rustchain.org/governance/proposals

# 查看提案详情
curl -sk https://rustchain.org/governance/proposal/1

# 提交投票
curl -sk -X POST https://rustchain.org/governance/vote \
  -H 'Content-Type: application/json' \
  -d '{
    "proposal_id": 1,
    "wallet": "RTC-your-wallet",
    "vote": "yes",
    "nonce": "1700000000",
    "public_key": "<ed25519_pubkey_hex>",
    "signature": "<ed25519_signature_hex>"
  }'
```

### 3. 创建提案

参考 [提案流程](#提案流程) 章节。

### 4. 社区讨论

- **Discord**: https://discord.gg/VqVVS2CW9Q
- **GitHub Issues**: https://github.com/Scottcjn/Rustchain/issues
- **赏金任务**: https://github.com/Scottcjn/rustchain-bounties/issues

### 5. 贡献代码

1. 浏览 [good first issue](https://github.com/Scottcjn/Rustchain/labels/good%20first%20issue)
2. Fork 仓库，创建分支
3. 提交 PR，获得 RTC 奖励
4. 参与治理投票

---

## API 参考

### 治理端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/governance/propose` | POST | 创建新提案 |
| `/governance/proposals` | GET | 获取所有提案列表 |
| `/governance/proposal/{id}` | GET | 获取提案详情 |
| `/governance/vote` | POST | 提交投票 |
| `/governance/ui` | GET | Web 治理界面 |

### 创建提案示例

```bash
curl -sk -X POST https://rustchain.org/governance/propose \
  -H 'Content-Type: application/json' \
  -d '{
    "wallet": "RTC-example-wallet",
    "title": "Increase epoch reward to 2.0 RTC",
    "description": "Proposal to increase base epoch reward from 1.5 to 2.0 RTC to incentivize more miners."
  }'
```

### 投票示例

```bash
curl -sk -X POST https://rustchain.org/governance/vote \
  -H 'Content-Type: application/json' \
  -d '{
    "proposal_id": 1,
    "wallet": "RTC-voter-wallet",
    "vote": "yes",
    "nonce": "1700000000",
    "public_key": "a1b2c3d4e5f6...",
    "signature": "x9y8z7w6v5u4..."
  }'
```

### 查询工具

```bash
# 检查节点健康
curl -sk https://rustchain.org/health

# 获取当前轮次
curl -sk https://rustchain.org/epoch

# 查看活跃矿工
curl -sk https://rustchain.org/api/miners

# 查询钱包余额
curl -sk "https://rustchain.org/wallet/balance?miner_id=YOUR_WALLET"
```

---

## 最佳实践

### 投票者

1. ✅ **仔细阅读提案**：理解技术细节和影响
2. ✅ **参与讨论**：在 Discord/GitHub 发表意见
3. ✅ **及时投票**：7 天活跃期内完成投票
4. ❌ **不要盲目投票**：基于技术评估而非情绪
5. ❌ **不要委托投票**：每个设备独立投票

### 提案者

1. ✅ **提前沟通**：在社区讨论想法
2. ✅ **详细说明**：提供充分的技术背景
3. ✅ **回应质疑**：积极回答社区问题
4. ✅ **合理时间**：给社区足够讨论时间
5. ❌ **避免重复提案**：先搜索已有讨论

### 安全注意事项

1. **保护私钥**：Ed25519 私钥是投票凭证
2. **验证端点**：确保连接到正确的节点
3. **检查签名**：投票前确认交易内容
4. **警惕钓鱼**：官方 Discord 是唯一渠道

---

## 常见问题

### Q: 如何成为活跃矿工？
A: 安装矿工软件，通过 6 项硬件指纹检查，开始挖矿即自动成为活跃矿工。

### Q: 投票需要手续费吗？
A: 不需要，投票是免费的。

### Q: 提案需要多少票才能通过？
A: 没有固定票数要求，只要赞成票权重 > 反对票权重即可通过。

### Q: 硬件资历乘数会变化吗？
A: 会，乘数每年衰减 15%，防止永久优势。

### Q: 可以在多个钱包投票吗？
A: 不可以，每个硬件指纹只能绑定一个钱包，防止 Sybil 攻击。

---

## 资源链接

- **主仓库**: https://github.com/Scottcjn/Rustchain
- **赏金任务**: https://github.com/Scottcjn/rustchain-bounties
- **区块浏览器**: https://rustchain.org/explorer
- **Discord**: https://discord.gg/VqVVS2CW9Q
- **白皮书**: https://github.com/Scottcjn/Rustchain/blob/main/docs/RustChain_Whitepaper_*.pdf

---

*最后更新：2026-03-12*  
*作者：牛（RustChain 社区贡献者）*
