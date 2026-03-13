# 流动性提供者追踪系统 - Issue #97

## 钱包信息

**主钱包**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`  
**开始日期**: 2026-03-13  
**状态**: 🟡 准备中

---

## 流动性池分配

| 资金池 | 目标金额 (RTC) | 目标金额 (USD) | 当前状态 | 注入日期 | 交易哈希 |
|--------|---------------|---------------|---------|---------|---------|
| RTC/USDT | 250 | $25 | ⏳ 待注入 | - | - |
| RTC/ETH | 150 | $15 | ⏳ 待注入 | - | - |
| wRTC/RTC | 100 | $10 | ⏳ 待注入 | - | - |
| **总计** | **500** | **$50** | - | - | - |

---

## 月度奖励追踪

### 2026 年

| 月份 | 预期奖励 (RTC) | 实际到账 (RTC) | 状态 | 到账日期 | 交易哈希 | 备注 |
|------|---------------|---------------|------|---------|---------|------|
| 3 月 | 500 | - | ⏳ 待开始 | - | - | 首月 |
| 4 月 | 500 | - | ⏳ 预期 | - | - | - |
| 5 月 | 500 | - | ⏳ 预期 | - | - | - |
| 6 月 | 500 | - | ⏳ 预期 | - | - | - |
| 7 月 | 500 | - | ⏳ 预期 | - | - | - |
| 8 月 | 500 | - | ⏳ 预期 | - | - | - |
| 9 月 | 500 | - | ⏳ 预期 | - | - | - |
| 10 月 | 500 | - | ⏳ 预期 | - | - | - |
| 11 月 | 500 | - | ⏳ 预期 | - | - | - |
| 12 月 | 500 | - | ⏳ 预期 | - | - | - |

**2026 年累计**: 0 / 6,000 RTC (0%)

---

## Impermanent Loss 追踪

| 日期 | RTC/USDT IL | RTC/ETH IL | wRTC/RTC IL | 总 IL | 净收益 (含奖励) |
|------|------------|-----------|------------|------|----------------|
| 2026-03-13 | 0% | 0% | 0% | 0% | 0 RTC |

---

## 检查清单

### 准备阶段
- [ ] 钱包设置完成
- [ ] 资金准备到位 (≥$50 USD 等值 RTC)
- [ ] 阅读并理解 IL 风险
- [ ] 备份钱包私钥（离线存储）

### 执行阶段
- [ ] 注入 RTC/USDT 流动性
- [ ] 注入 RTC/ETH 流动性
- [ ] 注入 wRTC/RTC 流动性
- [ ] 验证所有 LP Token 到账
- [ ] 截图保存交易证明

### 注册阶段
- [ ] 向 BoTTube 团队提交 LP 注册
- [ ] 提供钱包地址和流动性证明
- [ ] 确认注册成功
- [ ] 创建 GitHub issue 追踪

### 监控阶段
- [ ] 设置每周检查提醒
- [ ] 创建监控脚本（可选）
- [ ] 加入 RustChain LP Discord 频道

---

## 自动化监控脚本

### Python 监控脚本

```python
#!/usr/bin/env python3
"""
LP 监控脚本 - 追踪流动性提供者奖励和位置
运行：python lp_tracker.py
"""

import requests
import json
from datetime import datetime

WALLET_ADDRESS = "RTC4325af95d26d59c3ef025963656d22af638bb96b"
EXPLORER_BASE_URL = "https://50.28.86.131"
EXPECTED_MONTHLY_REWARD = 500  # RTC

def get_wallet_balance():
    """获取钱包余额"""
    try:
        response = requests.get(
            f"{EXPLORER_BASE_URL}/api/wallet/balance?miner_id={WALLET_ADDRESS}"
        )
        if response.status_code == 200:
            data = response.json()
            return data.get('balance', 0)
    except Exception as e:
        print(f"获取余额失败：{e}")
    return None

def get_lp_positions():
    """获取流动性位置"""
    # 这里需要根据实际 API 调整
    print(f"钱包 {WALLET_ADDRESS} 的流动性位置:")
    print("  - RTC/USDT: 待注入")
    print("  - RTC/ETH: 待注入")
    print("  - wRTC/RTC: 待注入")
    return []

def get_pending_rewards():
    """获取待领取奖励"""
    # 模拟数据，实际需要从链上获取
    return 0

def print_status():
    """打印状态报告"""
    print("=" * 60)
    print(f"流动性提供者状态报告 - {WALLET_ADDRESS}")
    print(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    balance = get_wallet_balance()
    if balance is not None:
        print(f"钱包余额：{balance:.2f} RTC")
    
    print("\n流动性位置:")
    get_lp_positions()
    
    pending = get_pending_rewards()
    print(f"\n待领取奖励：{pending:.2f} RTC")
    print(f"月度预期奖励：{EXPECTED_MONTHLY_REWARD} RTC")
    
    print("=" * 60)

if __name__ == "__main__":
    print_status()
```

### 定时任务设置 (cron)

```bash
# 每周运行一次监控脚本
0 9 * * 1 /usr/bin/python3 /path/to/lp_tracker.py >> /var/log/lp_tracker.log 2>&1

# 每月 1 号检查奖励到账
0 10 1 * * /usr/bin/python3 /path/to/lp_tracker.py --check-rewards >> /var/log/lp_rewards.log 2>&1
```

---

## 重要日期

| 日期 | 事件 | 状态 |
|------|------|------|
| 2026-03-13 | 任务开始，文档创建 | ✅ 完成 |
| 2026-03-15 | 目标：完成流动性注入 | ⏳ 待完成 |
| 2026-03-31 | 首次奖励发放日 | ⏳ 预期 |
| 2026-04-01 | 月度检查点 | ⏳ 预期 |

---

## 备注和决策日志

### 2026-03-13
- 创建流动性提供者计划文档
- 确定钱包地址：`RTC4325af95d26d59c3ef025963656d22af638bb96b`
- 设定初始流动性目标：$50 USD 等值 RTC
- 分配策略：50% RTC/USDT, 30% RTC/ETH, 20% wRTC/RTC

---

## 相关文档

- [流动性提供者实施指南](./LIQUIDITY_PROVIDER_97.md)
- [BOUNTY_LEDGER.md](./BOUNTY_LEDGER.md)
- [Issue #97](https://github.com/Scottcjn/rustchain-bounties/issues/97)

---

*最后更新：2026-03-13*  
*维护者：BoTTube LP Team*
