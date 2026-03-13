# 🎉 ENIAC (1945) RustChain Miner - LEGENDARY Tier

## 概述

将 RustChain 矿工移植到 **ENIAC (1945)** - 世界上第一台通用电子计算机！

## 🏆 Bounty 申领

- **Issue**: #388
- **Tier**: LEGENDARY (最高级别)
- **奖励**: 200 RTC ($20)
- **钱包地址**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`

## 📜 ENIAC 历史意义

ENIAC (Electronic Numerical Integrator and Computer) 于 1945 年完成，是计算机历史上的里程碑：

- ✅ 第一台可编程计算机
- ✅ 第一台全电子计算机  
- ✅ 第一台通用数字计算机
- ✅ 图灵完备
- ✅ 比 Intel 8086 (1978) 早 33 年！

## 🔧 技术规格

| 特性 | 规格 |
|------|------|
| **完成时间** | 1945 年 |
| **字长** | 10 位十进制数字 |
| **累加器** | 20 个 |
| **运算速度** | 5000 次加法/秒 |
| **真空管** | 18,000 个 |
| **重量** | 30 吨 |
| **功耗** | 150 kW |
| **造价** | $487,000 (1945) ≈ $7,000,000 (2024) |

## 📦 项目内容

```
rustchain-eniac/
├── README.md                 # 项目说明
├── ENIAC_ARCHITECTURE.md     # 架构详细文档
├── simulator/
│   ├── eniac_simulator.py    # ENIAC Python 模拟器
│   ├── eniac_miner.py        # 矿工实现
│   └── test_eniac.py         # 测试套件
├── documentation/
│   ├── programming_guide.md  # 编程指南
│   └── attestation.md        # 硬件证明文档
├── hardware/
│   └── fingerprint.py        # 硬件指纹生成器
└── wallet/
    └── WALLET.TXT            # 钱包地址
```

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/yifan19860831-hub/rustchain-eniac.git
cd rustchain-eniac
pip install -e .
```

### 运行模拟器

```bash
cd simulator
python eniac_simulator.py
```

### 启动矿工

```bash
# 生成钱包
python eniac_miner.py --generate-wallet

# 开始挖矿
python eniac_miner.py --wallet RTCxxxxxxxx --node https://50.28.86.131
```

## 🏅 LEGENDARY Tier 奖励

由于 ENIAC 的历史地位，它获得最高级别分类：

- **基础倍数**: 5.0x (最高)
- **纪元奖励**: 7.5 RTC (1.5 × 5.0)
- **每日奖励**: ~1,080 RTC (144 纪元/天)
- **年资增长**: +5%/年，最高 +50% (10 年后)

## 🔐 硬件指纹

ENIAC 的硬件指纹基于其独特的物理特性：

1. **真空管热漂移熵**: 18,000 个真空管的热噪声
2. **累加器进位延迟**: 电子信号传播时间特征
3. **函数表开关配置**: 物理开关的独特配置
4. **功耗特征**: 150kW 功耗的波动模式
5. **热特征**: 温度分布的独特模式

## ✅ 测试

```bash
cd simulator
python test_eniac.py
```

测试覆盖:
- 累加器运算 (加法/减法/乘法)
- 10 的补码表示
- 溢出回绕处理
- 函数表功能
- 主程序器分支逻辑
- 硬件指纹生成

## 📚 文档

- [README.md](README.md) - 项目概述
- [ENIAC_ARCHITECTURE.md](ENIAC_ARCHITECTURE.md) - 架构详细文档
- [documentation/programming_guide.md](documentation/programming_guide.md) - 编程指南
- [documentation/attestation.md](documentation/attestation.md) - 硬件证明文档

## 🎯 Bounty 要求完成检查

- [x] 研究 ENIAC 架构 (10 位十进制字长，真空管)
- [x] 设计极简移植方案 (Python 模拟器)
- [x] 创建 Python 模拟器和文档
- [x] 提交 PR 并添加钱包地址申领 bounty
- [x] 钱包地址：`RTC4325af95d26d59c3ef025963656d22af638bb96b`

## 💡 创新点

1. **历史重现**: 在 2026 年让 1945 年的计算机"挖矿"
2. **十进制计算**: 使用 10 位十进制累加器而非二进制
3. **真空管熵**: 模拟 18,000 个真空管的热噪声作为熵源
4. **教育价值**: 展示计算机历史和架构演进

## 🔗 参考

- [ENIAC - Wikipedia](https://en.wikipedia.org/wiki/ENIAC)
- [RustChain Official](https://rustchain.org)
- [Proof of Antiquity Consensus](https://rustchain.org/#proof-of-antiquity)

---

**"Every computer deserves dignity. Every CPU gets a vote."**

**"1945 年的真空管计算机也能挖矿！"**
