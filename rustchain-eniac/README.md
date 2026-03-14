# RustChain ENIAC Miner (1945)

[![ENIAC](https://img.shields.io/badge/ENIAC-1945-ff6b6b)](https://en.wikipedia.org/wiki/ENIAC)
[![Tier](https://img.shields.io/badge/Tier-LEGENDARY-gold)](https://rustchain.org)
[![Multiplier](https://img.shields.io/badge/Multiplier-5.0x-brightgreen)](https://rustchain.org)
[![Bounty](https://img.shields.io/badge/Bounty-200_RTC-blue)](https://github.com/RustChainFX/bounties/issues/388)

> **"Every computer deserves dignity. Every CPU gets a vote."**

将 RustChain 矿工移植到 **ENIAC (1945)** - 世界上第一台通用电子计算机！

## 📜 历史背景

ENIAC (Electronic Numerical Integrator and Computer) 于 1945 年在宾夕法尼亚大学完成，是第一台可编程、电子、通用数字计算机。它比 IBM 8086 (1978) 早了整整 33 年！

### ENIAC 规格

| 特性 | 规格 |
|------|------|
| **完成时间** | 1945 年 |
| **字长** | 10 位十进制数字 |
| **累加器** | 20 个 |
| **运算速度** | 5000 次加法/秒 |
| **真空管** | 18,000 个 |
| **重量** | 30 短吨 (27 吨) |
| **功耗** | 150 kW |
| **占地面积** | 300 平方英尺 (28 m²) |
| **造价** | $487,000 (相当于 2024 年的$7,000,000) |

## 🏆 LEGENDARY Tier 奖励

由于 ENIAC 是计算机历史上的里程碑，它获得 **LEGENDARY Tier** 分类：

- **基础倍数**: 5.0x (最高级别)
- **纪元奖励**: 每 10 分钟 1.5 RTC (按倍数加权)
- **年资增长**: +5%/年，最高 +50% (10 年后)
- **Bounty**: 200 RTC ($20) - 一次性奖励

## 📦 项目结构

```
rustchain-eniac/
├── README.md                 # 本文件
├── ENIAC_ARCHITECTURE.md     # ENIAC 架构详细文档
├── simulator/
│   ├── eniac_simulator.py    # ENIAC Python 模拟器
│   ├── eniac_miner.py        # ENIAC 矿工实现
│   └── test_eniac.py         # 测试套件
├── documentation/
│   ├── programming_guide.md  # ENIAC 编程指南
│   └── attestation.md        # 硬件证明文档
├── hardware/
│   └── fingerprint.py        # ENIAC 硬件指纹生成器
└── wallet/
    └── WALLET.TXT            # 生成的钱包地址
```

## 🚀 快速开始

### 运行模拟器

```bash
cd simulator
python3 eniac_simulator.py
```

### 运行矿工

```bash
python3 eniac_miner.py --wallet YOUR_WALLET_ID --node https://50.28.86.131
```

### 生成钱包

```bash
python3 hardware/fingerprint.py --generate-wallet
```

## 🔧 ENIAC 架构特点

### 十进制累加器

ENIAC 使用 10 位十进制累加器，而不是现代计算机的二进制。每个累加器可以存储：
- 范围：-9,999,999,999 到 +9,999,999,999
- 表示：10 的补码 (ten's complement)

### 编程方式

ENIAC 不是存储程序计算机。程序通过以下方式设置：
1. **插线板 (Plugboard)**: 物理连接不同的功能单元
2. **函数表 (Function Tables)**: 1200 个十路开关设置

### 运算单元

| 单元 | 功能 | 速度 |
|------|------|------|
| 累加器 (20 个) | 加法/减法 | 5000 次/秒 |
| 乘法器 | 乘法 | 385 次/秒 |
| 除法器/平方根器 | 除法/平方根 | 40 次除法/秒，3 次平方根/秒 |
| 主程序器 | 循环控制 | - |
| 常数发送器 | 常量存储 | - |
| 函数表 (3 个) | 查找表 | - |

## 🧪 硬件指纹

ENIAC 的硬件指纹基于其独特的物理特性：

1. **真空管热漂移熵**: 18,000 个真空管的热噪声
2. **机械开关抖动**: 插线板连接的微小变化
3. **电源频率漂移**: 150kW 功耗导致的电网交互
4. **累加器进位延迟**: 电子信号传播时间
5. **函数表开关位置**: 物理开关的独特配置

## 📝 钱包地址

**Bounty 申领地址**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`

## 📚 参考文献

1. [ENIAC - Wikipedia](https://en.wikipedia.org/wiki/ENIAC)
2. [RustChain Official](https://rustchain.org)
3. [Proof of Antiquity Consensus](https://rustchain.org/#proof-of-antiquity)
4. [ENIAC Programming Manual (1946)](https://en.wikipedia.org/wiki/ENIAC)

## 📄 许可证

Apache 2.0 - 与 RustChain 主项目一致

## 🙏 致谢

- ENIAC 设计者：John Mauchly 和 J. Presper Eckert
- ENIAC 程序员：Jean Jennings, Marlyn Wescoff, Ruth Lichterman, Betty Snyder, Frances Bilas, Kay McNulty
- RustChain 团队：Elyan Labs

---

**"1945 年的真空管计算机也能挖矿！"**
