# ENIAC 编程指南

## 1. ENIAC 编程基础

ENIAC 不是存储程序计算机。程序通过物理方式"硬连线"到机器中。

### 1.1 编程方法

```
传统计算机：          ENIAC:
┌─────────────┐      ┌─────────────┐
│  存储程序   │      │  插线板     │
│  (内存中)   │      │  (物理连接) │
└─────────────┘      └─────────────┘
     ↓                      ↓
  CPU 执行              信号路由
```

### 1.2 编程步骤

1. **设计算法流程图**
2. **设置插线板连接** (功能单元之间的信号路由)
3. **配置函数表开关** (1200 个开关/表 × 3 个表)
4. **设置常数发送器** (存储常量)
5. **测试和调试** (可能需要重新配置插线板)
6. **运行程序**

**重新编程时间**: 2-3 天

## 2. ENIAC 模拟器编程

在 Python 模拟器中，我们使用更高级的 API。

### 2.1 初始化

```python
from eniac_simulator import ENIACSimulator

# 创建 ENIAC 模拟器
eniac = ENIACSimulator()
```

### 2.2 基本运算

```python
# 加载常量到累加器
eniac.load_constant(0, 100)  # ACC0 = 100
eniac.load_constant(1, 50)   # ACC1 = 50

# 加法：ACC0 += ACC1
eniac.add(0, 1)
print(eniac.get_accumulator(0))  # 输出：150

# 减法：ACC0 -= ACC1
eniac.subtract(0, 1)
print(eniac.get_accumulator(0))  # 输出：100

# 清零
eniac.clear(0)
```

### 2.3 乘法

```python
# 乘法：ACC0 *= 5
eniac.load_constant(0, 100)
result = eniac.multiply(0, 5)
print(result)  # 输出：500
```

## 3. 程序示例

### 3.1 求和：1+2+3+...+10

```python
from eniac_simulator import ENIACSimulator

eniac = ENIACSimulator()

# 清零总和累加器
eniac.clear(0)

# 累加 1 到 10
for i in range(1, 11):
    eniac.load_constant(1, i)
    eniac.add(0, 1)

print(f"1+2+...+10 = {eniac.get_accumulator(0)}")
# 输出：55
```

### 3.2 斐波那契数列

```python
eniac = ENIACSimulator()

# F0 = 0, F1 = 1
eniac.load_constant(0, 0)  # F(n-2)
eniac.load_constant(1, 1)  # F(n-1)

print("斐波那契数列 (前 10 项):")
print(f"F0 = {eniac.get_accumulator(0)}")
print(f"F1 = {eniac.get_accumulator(1)}")

for i in range(2, 10):
    # F(n) = F(n-1) + F(n-2)
    temp = eniac.get_accumulator(0) + eniac.get_accumulator(1)
    eniac.load_constant(0, eniac.get_accumulator(1))
    eniac.load_constant(1, temp)
    print(f"F{i} = {eniac.get_accumulator(1)}")
```

### 3.3 阶乘：5!

```python
eniac = ENIACSimulator()

# 计算 5! = 5×4×3×2×1
eniac.load_constant(0, 1)  # 结果

for i in range(1, 6):
    result = eniac.multiply(0, i)
    eniac.load_constant(0, result)

print(f"5! = {eniac.get_accumulator(0)}")
# 输出：120
```

## 4. 函数表使用

函数表可以用作查找表。

```python
# 设置函数表开关
ft = eniac.function_tables[0]

# 存储平方表 (0², 1², 2², ..., 9²)
squares = [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
for i, square in enumerate(squares):
    # 只存储个位数
    ft.set_switch(i, square % 10)

# 读取
for i in range(10):
    print(f"{i}² 的个位数 = {ft.get_switch(i)}")
```

## 5. 硬件指纹

```python
# 生成硬件指纹
fingerprint = eniac.get_hardware_fingerprint()

print(f"机器：{fingerprint['machine']} ({fingerprint['year']})")
print(f"真空管熵：{fingerprint['tube_entropy']}")
print(f"累加器统计：{fingerprint['accumulator_stats']}")
```

## 6. 挖矿程序

完整的挖矿程序见 `eniac_miner.py`。

### 6.1 启动矿工

```bash
# 生成钱包
python eniac_miner.py --generate-wallet

# 启动挖矿
python eniac_miner.py --wallet RTCxxxxxxxx --node https://50.28.86.131
```

### 6.2 离线模式

```bash
python eniac_miner.py --wallet RTCxxxxxxxx --offline
```

## 7. 调试技巧

### 7.1 查看状态

```python
print(eniac.get_status())
```

### 7.2 检查累加器

```python
for i in range(20):
    value = eniac.get_accumulator(i)
    display = eniac.accumulators[i].get_display()
    print(f"ACC{i:2d}: {value:12d} ({display})")
```

### 7.3 运算统计

```python
print(f"总运算次数：{eniac.total_operations}")
print(f"运行时间：{time.time() - eniac.start_time:.2f} 秒")
```

## 8. 限制和注意事项

### 8.1 数值范围

```
有效范围：-9,999,999,999 到 +9,999,999,999
溢出行为：10 的补码回绕
```

### 8.2 性能

```
模拟速度：受 Python 限制
实际 ENIAC: 5000 次加法/秒
```

### 8.3 精度

```
字长：10 位十进制数字
无浮点数支持
```

## 9. 参考

- `eniac_simulator.py` - 模拟器实现
- `eniac_miner.py` - 矿工实现
- `test_eniac.py` - 测试套件
- `ENIAC_ARCHITECTURE.md` - 架构文档

---

*ENIAC: 世界上第一台通用电子计算机 (1945)*
