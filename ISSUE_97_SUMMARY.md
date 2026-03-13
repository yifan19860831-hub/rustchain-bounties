# Issue #97 - 流动性提供者计划

## 📋 快速概览

| 项目 | 详情 |
|------|------|
| **Issue** | #97 - Liquidity Provider |
| **奖励** | 500 RTC/月 ($50 USD) |
| **类型** | 持续性被动收入 |
| **钱包** | `RTC4325af95d26d59c3ef025963656d22af638bb96b` |
| **状态** | 🟡 准备中 |
| **开始日期** | 2026-03-13 |

---

## 🎯 目标

成为 BoTTube 官方认可的流动性提供者，通过提供 RTC 交易对流动性获得每月 500 RTC 的被动收入。

**年度预期收益**: 6,000 RTC ($600 USD)

---

## 📁 文档

| 文档 | 用途 | 链接 |
|------|------|------|
| **实施指南** | 详细执行步骤 | [LIQUIDITY_PROVIDER_97.md](./docs/LIQUIDITY_PROVIDER_97.md) |
| **追踪系统** | 奖励和 IL 监控 | [LP_TRACKER_97.md](./LP_TRACKER_97.md) |
| **PR 描述** | 提交用文档 | [PR_LP_PROVIDER_97.md](./PR_LP_PROVIDER_97.md) |

---

## ✅ 进度

### 阶段 1: 准备 (当前阶段)
- [x] 创建实施文档
- [x] 创建追踪系统
- [x] 编写监控脚本
- [ ] 准备资金 ($50+ USD 等值 RTC)
- [ ] 配置和测试钱包

### 阶段 2: 流动性注入
- [ ] RTC/USDT 池：250 RTC
- [ ] RTC/ETH 池：150 RTC
- [ ] wRTC/RTC 池：100 RTC

### 阶段 3: 官方注册
- [ ] 提交 LP 注册申请
- [ ] 提供流动性证明
- [ ] 确认官方 LP 身份

### 阶段 4: 持续运营
- [ ] 每周监控
- [ ] 每月申领奖励
- [ ] 季度策略审查

---

## 💰 奖励追踪

| 月份 | 预期 (RTC) | 实际 (RTC) | 状态 | 备注 |
|------|-----------|-----------|------|------|
| 2026-03 | 500 | - | ⏳ | 首月 |
| 2026-04 | 500 | - | ⏳ | - |
| 2026-05 | 500 | - | ⏳ | - |
| **Q1 小计** | **1,500** | **0** | - | - |

---

## ⚠️ 关键风险

1. **Impermanent Loss**: 价格波动可能导致相比持有亏损
2. **智能合约风险**: 协议漏洞风险
3. **市场风险**: RTC 价格波动

**缓解策略**: 分散投资、定期监控、部分奖励转稳定币

---

## 🔧 快速命令

```bash
# 查询钱包余额
rustchain-wallet balance --wallet RTC4325af95d26d59c3ef025963656d22af638bb96b

# 查询流动性位置
rustchain-wallet liquidity position --wallet RTC4325af95d26d59c3ef025963656d22af638bb96b

# 申领奖励
rustchain-wallet rewards claim --pool all

# 运行监控脚本
python lp_tracker.py
```

---

## 📅 下一步行动

1. **立即**: 准备 $50+ USD 等值的 RTC 资金
2. **本周**: 完成流动性注入（3 个资金池）
3. **下周**: 提交官方 LP 注册申请
4. **月底**: 申领首月 500 RTC 奖励

---

## 📞 联系

- GitHub: [rustchain-bounties](https://github.com/Scottcjn/rustchain-bounties)
- 区块浏览器: https://50.28.86.131/explorer
- 文档邮箱: dev@rustchain.io

---

*最后更新：2026-03-13*  
*维护者：BoTTube LP Team*
