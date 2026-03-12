# RustChain 矿工常见问题解答 (FAQ)

## 目录

1. [快速开始](#快速开始)
2. [安装问题](#安装问题)
3. [配置与钱包](#配置与钱包)
4. [挖矿原理](#挖矿原理)
5. [奖励机制](#奖励机制)
6. [硬件支持](#硬件支持)
7. [故障排除](#故障排除)
8. [常用命令](#常用命令)
9. [治理与投票](#治理与投票)
10. [获取更多帮助](#获取更多帮助)

---

## 快速开始

### 一分钟开始挖矿

```bash
# 1. 安装矿工（自动检测平台）
curl -sSL https://raw.githubusercontent.com/Scottcjn/Rustchain/main/install-miner.sh | bash

# 2. 检查矿工状态
systemctl --user status rustchain-miner  # Linux
launchctl list | grep rustchain          # macOS

# 3. 查看钱包余额
curl -sk "https://rustchain.org/wallet/balance?miner_id=YOUR_WALLET_NAME"
```

### 系统要求

- **Linux**: Ubuntu 20.04+, Debian 11+, Fedora 38+ (x86_64, ppc64le)
- **macOS**: 12+ (Intel, Apple Silicon, PowerPC)
- **Python**: 3.10+
- **网络**: 需要访问 rustchain.org

---

## 安装问题

### Q1: 安装脚本如何工作？

安装脚本 `install-miner.sh` 会：
- ✅ 自动检测你的平台（Linux/macOS, x86_64/ARM/PowerPC）
- ✅ 创建隔离的 Python 虚拟环境（不污染系统）
- ✅ 下载适合你硬件的正确矿工版本
- ✅ 设置开机自启动（systemd/launchd）
- ✅ 提供简单的卸载功能

### Q2: 如何指定钱包名称安装？

```bash
curl -sSL https://raw.githubusercontent.com/Scottcjn/Rustchain/main/install-miner.sh | bash -s -- --wallet my-miner-wallet
```

### Q3: 如何预览安装操作而不实际执行？

```bash
bash install-miner.sh --dry-run --wallet YOUR_WALLET_NAME
```

### Q4: 如何卸载矿工？

```bash
curl -sSL https://raw.githubusercontent.com/Scottcjn/Rustchain/main/install-miner.sh | bash -s -- --uninstall
```

### Q5: 安装脚本报权限错误怎么办？

**问题**: `permission denied` 或无法写入 `~/.local`

**解决方案**:
```bash
# 确保你有/home 目录的写入权限
# 不要在系统 Python 的全局 site-packages 中运行
# 使用有写入权限的账户重新运行
```

### Q6: Python 版本错误怎么办？

**问题**: `SyntaxError` 或 `ModuleNotFoundError`

**解决方案**:
```bash
# 检查 Python 版本
python3 --version  # 需要 3.10+

# 如果版本过低，安装 Python 3.10+ 后重新运行
curl -sSL https://raw.githubusercontent.com/Scottcjn/Rustchain/main/install-miner.sh | bash
```

---

## 配置与钱包

### Q7: 如何创建钱包？

钱包在安装时自动创建。你也可以手动指定：

```bash
# 安装时指定钱包名称
bash install-miner.sh --wallet YOUR_WALLET_NAME

# 或者使用 clawrtc（如果已安装）
pip install clawrtc
clawrtc wallet create YOUR_WALLET_NAME
```

### Q8: 如何查看钱包余额？

```bash
# 注意：使用 -sk 标志，因为节点可能使用自签名 SSL 证书
curl -sk "https://rustchain.org/wallet/balance?miner_id=YOUR_WALLET_NAME"
```

### Q9: 钱包余额显示 "could not reach network" 怎么办？

**解决方案**:
```bash
# 1. 验证节点连接
curl -sk https://rustchain.org/health

# 2. 直接检查钱包
curl -sk "https://rustchain.org/wallet/balance?miner_id=YOUR_WALLET_NAME"

# 3. 检查网络连接
curl -I https://rustchain.org
```

**注意**: 较旧的 helper 构建可能引用已退役的 `bulbous-bouffant.metalseed.net` 主机。

### Q10: 如何管理多个钱包？

每个硬件指纹绑定一个钱包。你可以在不同机器上使用不同钱包名称安装：

```bash
# 机器 1
bash install-miner.sh --wallet miner-office

# 机器 2
bash install-miner.sh --wallet miner-home
```

---

## 挖矿原理

### Q11: 什么是 Proof of Antiquity (PoA)？

RustChain 使用 **Proof of Antiquity** 共识机制，与传统 PoW 相反：

| 传统 PoW | Proof of Antiquity |
|---------|-------------------|
| 奖励最快硬件 | 奖励最老硬件 |
| 越新越好 | 越老越好 |
| 浪费能源 | 保护计算历史 |
| 强者通吃 | 每台设备一票 |

### Q12: 硬件检查如何工作？

每台矿工必须通过 6 项硬件指纹检查，证明是真实硬件而非模拟器：

```
┌─────────────────────────────────────────────────────────────┐
│ 6 项硬件检查                                                │
├─────────────────────────────────────────────────────────────┤
│ 1. 时钟偏移与振荡器漂移 ← 硅老化模式                        │
│ 2. 缓存时序指纹 ← L1/L2/L3 延迟特征                         │
│ 3. SIMD 单元识别 ← AltiVec/SSE/NEON 特征                    │
│ 4. 热漂移熵 ← 散热曲线唯一性                                │
│ 5. 指令路径抖动 ← 微架构抖动图                              │
│ 6. 反模拟检查 ← 检测虚拟机/模拟器                           │
└─────────────────────────────────────────────────────────────┘
```

**为什么重要**: SheepShaver 虚拟机伪装成 G4 Mac 会失败。真实的复古硅芯片有无法伪造的独特老化模式。

### Q13: 共识机制如何运作？

- 每个唯一硬件设备每轮（epoch）获得 **恰好 1 票**
- 奖励平均分配给所有投票者，然后乘以古老度倍数
- 运行多个线程或更快的 CPU 没有优势

**轮次时长**: 10 分钟（600 秒）  
**基础奖励池**: 每轮 1.5 RTC  
**分配方式**: 平均分配 × 古老度倍数

---

## 奖励机制

### Q14: 奖励如何计算？

```
个人奖励 = (基础奖励池 / 活跃矿工数) × 古老度倍数
```

**示例**（5 台矿工）:

| 硬件 | 倍数 | 奖励/轮 |
|-----|------|---------|
| G4 Mac (1999-2005) | 2.5× | 0.30 RTC |
| G5 Mac (2003-2006) | 2.0× | 0.24 RTC |
| 现代 PC | 1.0× | 0.12 RTC |
| 现代 PC | 1.0× | 0.12 RTC |
| 现代 PC | 1.0× | 0.12 RTC |
| **总计** | | **0.90 RTC** |

### Q15: 硬件倍数会变化吗？

是的，倍数会随时间衰减（**每年 15%**），防止永久优势。

### Q16: 完整硬件倍数列表

| 硬件 | 年代 | 倍数 | 示例收益/轮 |
|-----|------|------|------------|
| PowerPC G4 | 1999-2005 | 2.5× | 0.30 RTC |
| PowerPC G5 | 2003-2006 | 2.0× | 0.24 RTC |
| PowerPC G3 | 1997-2003 | 1.8× | 0.21 RTC |
| IBM POWER8 | 2014 | 1.5× | 0.18 RTC |
| Pentium 4 | 2000-2008 | 1.5× | 0.18 RTC |
| Core 2 Duo | 2006-2011 | 1.3× | 0.16 RTC |
| Apple Silicon | 2020+ | 1.2× | 0.14 RTC |
| 现代 x86_64 | 当前 | 1.0× | 0.12 RTC |

### Q17: RTC 代币价值是多少？

**参考汇率**: 1 RTC = $0.10 USD

RTC 可作为 wRTC 在 Solana 上使用：
- **交易**: [Raydium DEX](https://raydium.io/swap/?inputMint=sol&outputMint=12TAdKXxcGf6oCv4rqDz2NkgxjyHq6HQKoxKZYGf5i4X)
- **价格图表**: [DexScreener](https://dexscreener.com/solana/8CF2Q8nSCxRacDShbtF86XTSrYjueBMKmfdR3MLdnYzb)
- **桥接**: [BoTTube Bridge](https://bottube.ai/bridge)

---

## 硬件支持

### Q18: 支持哪些操作系统？

| 平台 | 架构 | 状态 | 说明 |
|-----|------|------|------|
| Mac OS X Tiger | PowerPC G4/G5 | ✅ 完全支持 | Python 2.5 兼容矿工 |
| Mac OS X Leopard | PowerPC G4/G5 | ✅ 完全支持 | 推荐用于复古 Mac |
| Ubuntu Linux | ppc64le/POWER8 | ✅ 完全支持 | 最佳性能 |
| Ubuntu Linux | x86_64 | ✅ 完全支持 | 标准矿工 |
| macOS Sonoma | Apple Silicon | ✅ 完全支持 | M1/M2/M3 芯片 |
| Windows 10/11 | x86_64 | ✅ 完全支持 | Python 3.8+ |
| DOS | 8086/286/386 | 🔧 实验性 | 仅徽章奖励 |

### Q19: 虚拟机可以挖矿吗？

可以，但会被检测并获得 **十亿分之一** 的正常奖励：

```
真实 G4 Mac: 2.5× 倍数 = 0.30 RTC/轮
模拟 G4: 0.0000000025× = 0.0000000003 RTC/轮
```

### Q20: 可以在同一硬件上使用多个钱包吗？

**不可以**。每个硬件指纹绑定一个钱包，防止：
- 同一硬件使用多个钱包
- 硬件欺骗
- Sybil 攻击

### Q21: 我的老电脑能挖矿吗？

很可能可以！RustChain 支持：
- PowerPC G3/G4/G5 Mac
- IBM POWER8 服务器
- Pentium 4 及更早的 x86 电脑
- Core 2 Duo 时代的电脑
- 现代 Mac 和 PC（奖励较低）

**名称由来**: RustChain 的名字来自一台真正生锈端口的 486 笔记本，它仍能启动到 DOS 并挖掘 RTC。"Rust" 指的是 30 年旧硅芯片上的氧化铁——不是 Rust 编程语言（虽然我们也有 Rust 组件）。

---

## 故障排除

### Q22: 矿工立即退出怎么办？

**问题**: 矿工启动后立即退出

**检查步骤**:
```bash
# 1. 验证钱包是否存在
curl -sk "https://rustchain.org/wallet/balance?miner_id=YOUR_WALLET"

# 2. 检查服务状态
systemctl --user status rustchain-miner  # Linux
launchctl list | grep rustchain          # macOS

# 3. 查看日志
journalctl --user -u rustchain-miner -f  # Linux
tail -f ~/.rustchain/miner.log           # macOS
```

### Q23: HTTPS 证书错误怎么办？

**问题**: `curl: (60) SSL certificate problem`

**解决方案**:
```bash
# 使用 -sk 标志跳过证书验证（节点可能使用自签名证书）
curl -sk https://rustchain.org/health

# 或者先检查连接
curl -I https://rustchain.org
```

### Q24: 如何检查节点健康状态？

```bash
# 检查节点健康
curl -sk https://rustchain.org/health

# 获取当前轮次
curl -sk https://rustchain.org/epoch

# 列出活跃矿工
curl -sk https://rustchain.org/api/miners

# 访问区块浏览器
open https://rustchain.org/explorer
```

### Q25: 如何管理矿工服务？

**Linux (systemd)**:
```bash
# 检查状态
systemctl --user status rustchain-miner

# 停止挖矿
systemctl --user stop rustchain-miner

# 启动挖矿
systemctl --user start rustchain-miner

# 查看日志
journalctl --user -u rustchain-miner -f
```

**macOS (launchd)**:
```bash
# 检查状态
launchctl list | grep rustchain

# 停止挖矿
launchctl stop com.rustchain.miner

# 启动挖矿
launchctl start com.rustchain.miner

# 查看日志
tail -f ~/.rustchain/miner.log
```

### Q26: 问题持续存在怎么办？

如果问题持续，请在新 issue 或赏金评论中提供：
- 完整的错误输出
- 操作系统详情
- `install-miner.sh --dry-run` 结果
- 相关日志文件

---

## 常用命令

### 网络查询

```bash
# 检查节点健康
curl -sk https://rustchain.org/health

# 获取当前轮次
curl -sk https://rustchain.org/epoch

# 列出活跃矿工
curl -sk https://rustchain.org/api/miners

# 检查钱包余额
curl -sk "https://rustchain.org/wallet/balance?miner_id=YOUR_WALLET"

# 访问区块浏览器
open https://rustchain.org/explorer
```

### 矿工管理

```bash
# Linux - 检查状态
systemctl --user status rustchain-miner

# Linux - 重启矿工
systemctl --user restart rustchain-miner

# macOS - 检查状态
launchctl list | grep rustchain

# macOS - 重启矿工
launchctl stop com.rustchain.miner && launchctl start com.rustchain.miner
```

### 安装与卸载

```bash
# 标准安装
curl -sSL https://raw.githubusercontent.com/Scottcjn/Rustchain/main/install-miner.sh | bash

# 指定钱包安装
curl -sSL https://raw.githubusercontent.com/Scottcjn/Rustchain/main/install-miner.sh | bash -s -- --wallet my-wallet

# 预览安装（不执行）
bash install-miner.sh --dry-run --wallet my-wallet

# 卸载
curl -sSL https://raw.githubusercontent.com/Scottcjn/Rustchain/main/install-miner.sh | bash -s -- --uninstall
```

---

## 治理与投票

### Q27: 如何参与治理？

RustChain 有链上治理系统：

**提案要求**:
- 创建提案：钱包持有 > 10 RTC
- 投票资格：必须是活跃矿工
- 提案周期：草稿 → 活跃（7 天）→ 通过/失败
- 通过条件：yes_weight > no_weight

**投票权重**:
```
投票权重 = 1 RTC × 古老度倍数
```

### Q28: 如何创建提案？

```bash
curl -sk -X POST https://rustchain.org/governance/propose \
  -H 'Content-Type: application/json' \
  -d '{
    "wallet":"RTC...",
    "title":"启用参数 X",
    "description":"理由和实现细节"
  }'
```

### Q29: 如何投票？

```bash
# 列出提案
curl -sk https://rustchain.org/governance/proposals

# 查看提案详情
curl -sk https://rustchain.org/governance/proposal/1

# 提交签名投票
curl -sk -X POST https://rustchain.org/governance/vote \
  -H 'Content-Type: application/json' \
  -d '{
    "proposal_id":1,
    "wallet":"RTC...",
    "vote":"yes",
    "nonce":"1700000000",
    "public_key":"<ed25519_pubkey_hex>",
    "signature":"<ed25519_signature_hex>"
  }'
```

**Web UI**: 访问 `https://rustchain.org/governance/ui` 查看提案和投票。

---

## 获取更多帮助

### 官方资源

- **网站**: [rustchain.org](https://rustchain.org)
- **区块浏览器**: [rustchain.org/explorer](https://rustchain.org/explorer)
- **GitHub**: [github.com/Scottcjn/Rustchain](https://github.com/Scottcjn/Rustchain)
- **Discord**: [discord.gg/VqVVS2CW9Q](https://discord.gg/VqVVS2CW9Q)

### 文档

- **白皮书**: [RustChain Whitepaper](https://github.com/Scottcjn/Rustchain/blob/main/docs/RustChain_Whitepaper_*.pdf)
- **架构文档**: [chain_architecture.md](https://github.com/Scottcjn/Rustchain/blob/main/docs/chain_architecture.md)
- **wRTC 快速入门**: [wRTC Quickstart](https://github.com/Scottcjn/Rustchain/blob/main/docs/wrtc.md)

### 赏金任务

- **开放赏金**: [rustchain-bounties/issues](https://github.com/Scottcjn/rustchain-bounties/issues)
- **新手任务**: [good first issue](https://github.com/Scottcjn/Rustchain/labels/good%20first%20issue)
- **贡献指南**: [CONTRIBUTING.md](https://github.com/Scottcjn/Rustchain/blob/main/CONTRIBUTING.md)

### 社区

- **Dev.to 文章**:
  - [Proof of Antiquity: A Blockchain That Rewards Vintage Hardware](https://dev.to/scottcjn/proof-of-antiquity-a-blockchain-that-rewards-vintage-hardware-4ii3)
  - [I Run LLMs on a 768GB IBM POWER8 Server](https://dev.to/scottcjn/i-run-llms-on-a-768gb-ibm-power8-server-and-its-faster-than-you-think-1o)

---

## 徽章系统

### Q30: 有哪些挖矿徽章？

挖矿达到里程碑可获得纪念徽章：

| 徽章 | 要求 | 稀有度 |
|-----|------|--------|
| 🔥 Bondi G3 Flamekeeper | 在 PowerPC G3 上挖矿 | 稀有 |
| ⚡ QuickBasic Listener | 在 DOS 机器上挖矿 | 传奇 |
| 🛠️ DOS WiFi Alchemist | 联网的 DOS 机器 | 神话 |
| 🏛️ Pantheon Pioneer | 前 100 名矿工 | 限定 |

---

## 外部集成

### wRTC on Solana

RustChain Token (RTC) 现已作为 wRTC 在 Solana 上可用：

| 资源 | 链接 |
|-----|------|
| 交易 wRTC | [Raydium DEX](https://raydium.io/swap/?inputMint=sol&outputMint=12TAdKXxcGf6oCv4rqDz2NkgxjyHq6HQKoxKZYGf5i4X) |
| 价格图表 | [DexScreener](https://dexscreener.com/solana/8CF2Q8nSCxRacDShbtF86XTSrYjueBMKmfdR3MLdnYzb) |
| 桥接 RTC ↔ wRTC | [BoTTube Bridge](https://bottube.ai/bridge) |
| Token Mint | `12TAdKXxcGf6oCv4rqDz2NkgxjyHq6HQKoxKZYGf5i4X` |

### wRTC on Coinbase Base

RustChain 代理可以拥有 Coinbase Base 钱包并使用 x402 协议进行机器间支付：

| 资源 | 链接 |
|-----|------|
| 代理钱包文档 | [rustchain.org/wallets.html](https://rustchain.org/wallets.html) |
| wRTC on Base | `0x5683C10596AaA09AD7F4eF13CAB94b9b74A669c6` |
| 交易 USDC 到 wRTC | [Aerodrome DEX](https://aerodrome.finance/swap?from=0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913&to=0x5683C10596AaA09AD7F4eF13CAB94b9b74A669c6) |
| Base 桥接 | [bottube.ai/bridge/base](https://bottube.ai/bridge/base) |

---

**最后更新**: 2026-03-12  
**维护者**: RustChain 社区  
**许可证**: MIT
