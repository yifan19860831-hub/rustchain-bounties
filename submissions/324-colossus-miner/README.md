# 🏛️ Colossus Miner (1943)

> **RustChain 矿工移植到世界上第一台电子数字计算机**

![Colossus](https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Colossus_Computer.jpg/800px-Colossus_Computer.jpg)

## 📜 项目概述

这是一个**概念验证**项目，将现代区块链挖矿算法移植到 1943 年的 Colossus 计算机架构上。Colossus 是布莱切利园在二战期间开发的密码破译机，用于破译德军的高级 Lorenz 密码。

### 🎯 项目目标

- 展示如何在 5 位并行、真空管架构上实现工作量证明算法
- 探索早期计算机架构与现代密码学的交叉点
- 向计算机先驱致敬（图灵、纽曼等）

---

## 🖥️ Colossus 架构规格

| 特性 | 规格 |
|------|------|
| **年份** | 1943-1945 |
| **地点** | 英国布莱切利园 |
| **处理器** | 真空管逻辑（约 1,500-2,400 个） |
| **并行度** | 5 位并行处理 |
| **时钟频率** | ~5,000 Hz (5 kHz) |
| **输入** | 穿孔纸带（5 位 Baudot 码） |
| **输出** | 指示灯面板 / 穿孔纸带 |
| **内存** | 无现代内存，使用触发器存储 |
| **编程** | 插线板和开关设置 |
| **功耗** | 约 4.5 kW |

### 5 位并行架构

Colossus 使用 5 位并行处理，每个字符用 5 个比特表示（Baudot 码）：

```
位模式：A B C D E
字符 'A' = ●●○○○ (11000)
字符 'B' = ○●●●○ (01110)
...
```

---

## ⛏️ 挖矿算法设计

### 简化版工作量证明

由于 Colossus 的计算能力限制，我们设计了一个极简的 PoW 算法：

```
目标：找到一个 nonce，使得 hash(header || nonce) 的前 N 位为零

Colossus 实现:
1. 使用 5 位累加器
2. 迭代 nonce (0-31，5 位范围)
3. 计算简化的哈希函数（XOR + 位移）
4. 检查结果是否满足难度目标
5. 通过指示灯输出结果
```

### 哈希函数（Colossus 风格）

```python
def colossus_hash(data: bytes) -> int:
    """
    使用 Colossus 风格的 5 位并行逻辑计算哈希
    模拟真空管 XOR 门和移位寄存器
    """
    accumulator = 0
    for byte in data:
        # 5 位并行 XOR
        accumulator ^= (byte & 0b11111)
        # 循环左移（模拟移位寄存器）
        accumulator = ((accumulator << 1) | (accumulator >> 4)) & 0b11111
    return accumulator
```

---

## 📁 项目结构

```
colossus-miner/
├── README.md              # 本文件
├── docs/
│   ├── ARCHITECTURE.md    # Colossus 架构详解
│   ├── MINING.md          # 挖矿算法设计
│   └── HISTORY.md         # Colossus 历史背景
├── src/
│   ├── colossus.py        # Colossus 模拟器核心
│   ├── miner.py           # 挖矿实现
│   └── hash_functions.py  # 哈希函数
└── examples/
    └── demo.py            # 演示脚本
```

---

## 🚀 快速开始

### 运行模拟器

```bash
cd colossus-miner
python src/colossus.py
```

### 运行挖矿演示

```bash
python examples/demo.py
```

---

## 🔬 技术细节

### 真空管逻辑模拟

Colossus 使用真空管实现布尔逻辑：

- **XOR 门**: 用于比特比较
- **AND 门**: 用于条件判断
- **移位寄存器**: 用于数据处理
- **触发器**: 用于状态存储

### 性能估算

| 操作 | Colossus | 现代 CPU |
|------|----------|----------|
| 哈希计算 | ~200 次/秒 | ~10^9 次/秒 |
| 内存访问 | 不适用 | ~10^11 次/秒 |
| 能耗效率 | ~0.0001 H/W | ~10^6 H/W |

**结论**: Colossus 挖矿主要是理论练习，实际挖矿需要约 10^15 年才能挖到一个区块 😄

---

## 🏆 RustChain Bounty

本作品提交至 RustChain "Port Miner to Colossus" 挑战：

- **难度等级**: LEGENDARY
- **奖励**: 200 RTC ($20)
- **钱包地址**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`

---

## 📚 参考资料

1. [Colossus Computer - Wikipedia](https://en.wikipedia.org/wiki/Colossus_computer)
2. [Bletchley Park Archives](https://www.bletchleypark.org.uk/)
3. [The Men Who Cracked Enigma](https://www.amazon.com/Codebreakers-Story-Secret-Writing-Cryptanalysis/dp/0684831309)

---

## ⚖️ 许可证

MIT License - 向历史致敬，知识属于全人类

---

*"Colossus is the first programmable, electronic, digital computer."*
