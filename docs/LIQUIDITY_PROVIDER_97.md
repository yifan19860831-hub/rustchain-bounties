# BoTTube 流动性提供者计划 - Issue #97

## 任务概述

**Issue**: #97 - Liquidity Provider  
**奖励**: 500 RTC/月 ($50 USD) - **每月重复收益**  
**优先级**: 🔴 最高  
**钱包地址**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`

---

## 目标

成为 BoTTube 官方认可的流动性提供者，为 RustChain/BoTTube 生态系统提供稳定的流动性支持，同时获得每月 500 RTC 的被动收入。

---

## 流动性提供机制

### 什么是流动性提供？

流动性提供者 (LP) 向交易对资金池注入资金，使其他用户能够进行交易。作为回报，LP 获得：
- 交易手续费分成
- 协议奖励代币
- 治理权（如适用）

### BoTTube 流动性需求

根据 RustChain 生态系统需求，主要流动性对可能包括：
1. **RTC/USDT** - 主要交易对
2. **RTC/ETH** - 跨链流动性
3. **wRTC/RTC** - 包装代币桥接流动性

---

## 实施步骤

### 阶段 1: 准备 (第 1-2 天)

#### 1.1 资金准备
- [ ] 确认可用资金：建议至少 $500-1000 USD 等值的 RTC
- [ ] 将资金转入 RustChain 钱包
- [ ] 备份钱包私钥和助记词（安全存储）

#### 1.2 技术准备
- [ ] 安装 RustChain 钱包 CLI 工具
- [ ] 配置钱包连接到主网
- [ ] 测试小额转账确保钱包正常工作

#### 1.3 了解协议
- [ ] 阅读 RustChain 白皮书相关章节
- [ ] 研究 wRTC 桥接机制
- [ ] 了解 Impermanent Loss (IL) 风险

### 阶段 2: 资金池配置 (第 3-5 天)

#### 2.1 选择流动性池
根据风险和收益评估，推荐配置：

| 资金池 | 分配比例 | 风险等级 | 预期 APR |
|--------|---------|---------|---------|
| RTC/USDT | 50% | 中 | 15-25% |
| RTC/ETH | 30% | 中高 | 20-35% |
| wRTC/RTC | 20% | 低 | 8-12% |

#### 2.2 注入流动性
```bash
# 示例：添加 RTC/USDT 流动性
rustchain-wallet liquidity add \
  --pool RTC/USDT \
  --amount-rtc 250 \
  --amount-usdt 25 \
  --slippage 0.5
```

#### 2.3 验证流动性
- [ ] 在区块浏览器确认 LP Token 到账
- [ ] 记录初始 LP Token 数量
- [ ] 截图保存交易哈希

### 阶段 3: 注册为官方 LP (第 6-7 天)

#### 3.1 提交申请
向 BoTTube 团队提交流动性提供者注册：
- 钱包地址：`RTC4325af95d26d59c3ef025963656d22af638bb96b`
- 流动性证明（交易哈希）
- 承诺锁定期（建议 3-6 个月）

#### 3.2 创建追踪文档
- [ ] 在 rustchain-bounties repo 创建 LP 追踪 issue
- [ ] 添加 `liquidity-provider` 标签
- [ ] 关联 issue #97

### 阶段 4: 监控与维护 (持续)

#### 4.1 每周检查
- [ ] 检查流动性池价值变化
- [ ] 计算累积奖励
- [ ] 评估 Impermanent Loss

#### 4.2 每月申领奖励
- [ ] 确认 500 RTC 奖励到账
- [ ] 记录到 BOUNTY_LEDGER.md
- [ ] 更新本文档的奖励追踪表

---

## 奖励追踪

| 月份 | 奖励 (RTC) | 奖励 (USD) | 状态 | 交易哈希 |
|------|-----------|-----------|------|---------|
| 2026-03 | 500 | $50 | ⏳ 待开始 | - |
| 2026-04 | 500 | $50 | ⏳ 预期 | - |
| 2026-05 | 500 | $50 | ⏳ 预期 | - |

**年度预期收益**: 6,000 RTC ($600 USD)

---

## 风险管理

### Impermanent Loss (IL)

**风险**: 当池中代币价格比率变化时，相比持有代币可能产生损失。

**缓解策略**:
1. 选择相关性高的交易对（如 RTC/wRTC）
2. 定期再平衡持仓
3. 长期持有以抵消 IL（奖励累积）

### 智能合约风险

**风险**: 协议漏洞可能导致资金损失。

**缓解策略**:
1. 仅使用经过审计的合约
2. 分散流动性到多个池
3. 不超过总资金的 20-30%

### 市场风险

**风险**: RTC 价格波动影响 LP 价值。

**缓解策略**:
1. 定期将部分奖励转换为稳定币
2. 设置止损阈值
3. 关注 RustChain 生态发展

---

## 技术实现细节

### 所需工具

```bash
# RustChain 钱包
cargo install rustchain-wallet

# 查询流动性位置
rustchain-wallet liquidity position --wallet RTC4325af95d26d59c3ef025963656d22af638bb96b

# 申领奖励
rustchain-wallet rewards claim --pool all --wallet RTC4325af95d26d59c3ef025963656d22af638bb96b
```

### 监控脚本

创建自动化监控脚本（可选）:

```python
#!/usr/bin/env python3
# lp_monitor.py - 监控流动性位置和奖励

import requests

WALLET = "RTC4325af95d26d59c3ef025963656d22af638bb96b"
EXPLORER_API = "https://50.28.86.131/api"

def check_lp_position():
    response = requests.get(f"{EXPLORER_API}/wallet/{WALLET}/liquidity")
    data = response.json()
    print(f"Total LP Value: {data['total_value']} RTC")
    print(f"Pendings Rewards: {data['pending_rewards']} RTC")
    return data

if __name__ == "__main__":
    check_lp_position()
```

---

## 成功标准

### 短期 (1 个月)
- [ ] 完成流动性注入（≥$500 等值）
- [ ] 成功注册为官方 LP
- [ ] 收到第一笔 500 RTC 奖励

### 中期 (3 个月)
- [ ] 持续获得月度奖励（累计 1,500 RTC）
- [ ] IL 控制在 -5% 以内
- [ ] 建立自动化监控

### 长期 (12 个月)
- [ ] 年度收益达到 6,000 RTC
- [ ] 考虑增加流动性规模
- [ ] 参与 RustChain 治理投票

---

## 相关资源

- [RustChain 白皮书](../RustChain_Whitepaper_Flameholder_v0.97.pdf)
- [wRTC 文档](../Rustchain/docs/wrtc.md)
- [区块浏览器](https://50.28.86.131/explorer)
- [BOUNTY_LEDGER.md](./BOUNTY_LEDGER.md)

---

## 联系与支持

如有问题，请联系：
- RustChain Discord: [链接]
- GitHub Issues: [rustchain-bounties](https://github.com/Scottcjn/rustchain-bounties/issues)
- 文档邮箱: dev@rustchain.io

---

*最后更新: 2026-03-13*  
*状态: 🟡 实施中*
