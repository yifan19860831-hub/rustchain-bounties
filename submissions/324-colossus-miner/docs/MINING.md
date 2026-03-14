# 挖矿算法设计

## 🎯 设计目标

在 Colossus (1943) 的极端限制下实现工作量证明：

| 限制 | 规格 | 解决方案 |
|------|------|----------|
| 位宽 | 5 位并行 | 使用 5 位哈希输出 |
| 内存 | ~40 比特 | 无状态哈希函数 |
| 速度 | 5 kHz | 简化算法 |
| 编程 | 插线板 | 固定逻辑 |

---

## ⛏️ 工作量证明算法

### 标准 PoW (现代)

```python
def modern_pow(block_header, difficulty):
    target = 2 ** (256 - difficulty)
    nonce = 0
    while True:
        hash = SHA256(SHA256(block_header + nonce))
        if hash < target:
            return nonce
        nonce += 1
```

**问题**: SHA256 需要 32 位运算，Colossus 只有 5 位！

### Colossus PoW (简化版)

```python
def colossus_pow(block_header, difficulty):
    # 难度：2-5 位（前 N 位为零）
    target_mask = (1 << difficulty) - 1
    
    for nonce in range(32):  # 5 位 nonce: 0-31
        data = block_header + nonce
        hash = colossus_hash(data)  # 5 位输出
        
        if (hash & target_mask) == 0:
            return nonce
    
    return None  # 无解
```

---

## 🔐 Colossus 哈希函数

### 算法

```
输入：任意长度字节串
输出：5 位整数 (0-31)

步骤:
1. 初始化累加器 = 0 (5 位)
2. 对于每个输入字节:
   a. 提取低 5 位
   b. 与累加器 XOR
   c. 循环左移 1 位
3. 返回累加器
```

### 伪代码

```
ACC ← 0
FOR each byte B in input:
    B5 ← B AND 0b11111      // 提取 5 位
    ACC ← ACC XOR B5        // 并行 XOR
    ACC ← ROTATE_LEFT(ACC)  // 5 位循环左移
RETURN ACC
```

### 电路实现

```
输入字节 → [5 位提取] ──┐
                       ├──[XOR]──[5 位寄存器]──┐
累加器 ←───────────────┘                      │
           ↑                                  │
           └──────[循环左移]←─────────────────┘
```

---

## 📊 难度设置

### 难度级别

| 难度 | 前导零位数 | 概率 | 期望尝试 |
|------|-----------|------|----------|
| 1    | 1         | 1/2  | 2        |
| 2    | 2         | 1/4  | 4        |
| 3    | 3         | 1/8  | 8        |
| 4    | 4         | 1/16 | 16       |
| 5    | 5         | 1/32 | 32       |

### 推荐难度

- **演示**: 难度 2 (4 次尝试)
- **测试**: 难度 3 (8 次尝试)
- **挑战**: 难度 4 (16 次尝试)
- **极限**: 难度 5 (32 次尝试，可能无解)

---

## 🔍 示例计算

### 示例 1: 难度 2

```
区块头："BLOCK1"
难度：2 (需要前 2 位为零)

尝试 0:
  输入："BLOCK1" + 0
  哈希：0b10110 (22)
  检查：22 & 0b11 = 2 ≠ 0 ❌

尝试 1:
  输入："BLOCK1" + 1
  哈希：0b00101 (5)
  检查：5 & 0b11 = 1 ≠ 0 ❌

尝试 2:
  输入："BLOCK1" + 2
  哈希：0b00011 (3)
  检查：3 & 0b11 = 3 ≠ 0 ❌

尝试 3:
  输入："BLOCK1" + 3
  哈希：0b00000 (0)
  检查：0 & 0b11 = 0 ✅ 成功!

结果：Nonce = 3, 尝试次数 = 4
```

---

## ⚡ 性能分析

### Colossus 性能

```
时钟频率：5,000 Hz
每哈希周期：~100 时钟 (估计)
哈希率：5,000 / 100 = 50 H/s

难度 2: 期望 4 次尝试 → 0.08 秒
难度 3: 期望 8 次尝试 → 0.16 秒
难度 4: 期望 16 次尝试 → 0.32 秒
难度 5: 期望 32 次尝试 → 0.64 秒
```

### 现代对比

```
现代 CPU: ~10^9 H/s
现代 GPU: ~10^9 H/s
ASIC:     ~10^14 H/s

Colossus: ~50 H/s

性能比：
CPU : Colossus = 20,000,000 : 1
ASIC : Colossus = 2,000,000,000,000 : 1
```

---

## 🎓 教育意义

### 为什么这样做？

1. **历史教育**: 理解早期计算机的限制
2. **架构对比**: 展示计算机发展的巨大进步
3. **算法设计**: 学习如何在极端限制下设计算法
4. **致敬先驱**: 向计算机科学的奠基人致敬

### 学习成果

通过这个项目，你将理解：

- ✅ 5 位并行处理的工作原理
- ✅ 真空管逻辑门如何构建计算机
- ✅ 工作量证明的基本概念
- ✅ 哈希函数的设计原则
- ✅ 计算机架构的历史演进

---

## 🔧 扩展想法

### 可能的改进

1. **更复杂的哈希**: 添加更多轮次
2. **默克尔树**: 模拟交易验证
3. **难度调整**: 根据找到时间自动调整
4. **网络模拟**: 多 Colossus 节点"挖矿"

### 物理实现

如果有硬件条件：

- 使用 FPGA 模拟真空管
- 构建真实的 5 位并行数据通路
- 制作指示灯面板
- 使用穿孔纸带输入

---

## 📝 参考实现

参见 `src/colossus.py`:

```python
def compute_hash(self, data: bytes) -> int:
    """Colossus 风格的哈希函数"""
    tape = self.load_tape(data)
    accumulator = ShiftRegister(bits=5)
    
    for symbol in tape:
        # XOR 累积
        acc_value = accumulator.value
        accumulator.load(acc_value ^ symbol)
        # 循环移位
        accumulator.rotate_left()
    
    return accumulator.value
```

---

**项目**: RustChain Colossus Miner  
**钱包**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`  
**Bounty**: #393 - LEGENDARY Tier
