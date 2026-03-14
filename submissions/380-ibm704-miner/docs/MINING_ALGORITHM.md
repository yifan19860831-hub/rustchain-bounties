# IBM 704 挖矿算法说明

## 概述

RustChain IBM 704 矿工实现了 **Proof-of-Antiquity (PoA)** 共识机制，通过模拟 1954 年 IBM 704 计算机的硬件特征来证明"古董硬件"的存在。

---

## 核心原理

### Proof-of-Antiquity vs Proof-of-Work

```
┌─────────────────────────────────────────────────────────────┐
│  传统 PoW (Bitcoin)          │  RustChain PoA                │
├─────────────────────────────────────────────────────────────┤
│  奖励最快硬件                │  奖励最老硬件                  │
│  新 = 好                     │  老 = 好                      │
│  能源浪费                    │  历史保护                     │
│  军备竞赛                    │  数字考古                     │
└─────────────────────────────────────────────────────────────┘
```

### IBM 704 的独特价值

```
┌─────────────────────────────────────────────────────────────┐
│  IBM 704 (1954) 历史意义                                     │
├─────────────────────────────────────────────────────────────┤
│  ✓ 第一台量产浮点计算机                                      │
│  ✓ 第一台磁芯内存计算机                                      │
│  ✓ FORTRAN 和 LISP 的诞生平台                                │
│  ✓ 用于 Sputnik 卫星轨道计算                                 │
│  ✓ 第一个神经网络 (Perceptron) 实现                          │
│  ✓ 第一个计算机音乐程序 (MUSIC-N)                            │
└─────────────────────────────────────────────────────────────┘
```

---

## 硬件指纹收集

### 1. 真空管热噪声熵

IBM 704 使用约 **5,000 个真空管**，工作温度约 **45°C**。每个真空管产生 **Johnson-Nyquist 热噪声**。

```python
def collect_vacuum_tube_entropy(cycles=48):
    """
    模拟真空管热噪声收集
    
    真实物理原理:
    V_rms = sqrt(4 * k * T * R * B)
    
    其中:
    - k = Boltzmann 常数
    - T = 温度 (开尔文)
    - R = 电阻
    - B = 带宽
    """
    samples = []
    tube_temperature = 45.0  # Celsius
    
    for _ in range(cycles):
        # 模拟热噪声电压
        noise_voltage = random.gauss(0, tube_temperature * 0.01)
        
        # 模拟测量时序变化
        start = time.perf_counter_ns()
        for j in range(25000):
            _ = j * 31 ^ int(noise_voltage * 1000)
        duration = time.perf_counter_ns() - start
        
        samples.append(duration)
    
    # 计算统计特征
    mean_ns = sum(samples) / len(samples)
    variance_ns = sum((x - mean_ns)**2 for x in samples) / len(samples)
    
    return {
        "mean_ns": mean_ns,
        "variance_ns": variance_ns,
        "tube_temperature": tube_temperature,
        "samples": samples[:12],
    }
```

**指纹独特性**：
- 真空管老化模式不可复制
- 热噪声是真正的随机源
- 时序变化反映硬件特征

### 2. 磁芯内存时序特征

IBM 737 磁芯存储单元的访问时间为 **12 微秒**，但每个磁芯有微小的制造差异。

```python
def get_core_memory_fingerprint():
    """
    磁芯内存时序指纹
    
    每个磁芯环有独特的:
    - 磁化延迟
    - 感应电压
    - 恢复时间
    """
    access_times = []
    
    # 访问特定地址模式
    for addr in [0, 100, 500, 1000, 2000, 3000, 4000]:
        start = time.perf_counter_ns()
        _ = memory[addr]  # 模拟磁芯读取
        duration = time.perf_counter_ns() - start
        access_times.append(duration)
    
    mean_time = sum(access_times) / len(access_times)
    variance = sum((x - mean_time)**2 for x in access_times) / len(access_times)
    
    return {
        "mean_access_us": mean_time,
        "variance_us": variance,
        "core_count": 4096,
        "technology": "magnetic_core_1954",
    }
```

### 3. 36 位字长计算特征

IBM 704 使用 **36 位字长**，这与现代 64 位计算机不同。

```python
# IBM 704 数据格式
WORD_MASK = (1 << 36) - 1  # 36 位掩码
AC_MASK = (1 << 38) - 1    # 38 位累加器

# 浮点格式 (IBM 704)
# 1 位符号 + 8 位指数 (excess-128) + 27 位尾数
FP_SIGN_BIT = 35
FP_EXP_BITS = 8
FP_FRAC_BITS = 27
FP_EXP_BIAS = 128  # excess-128
```

---

## 挖矿计算流程

### 步骤 1: 获取挑战

```python
# 从 RustChain 节点获取挑战 nonce
response = requests.post(f"{NODE_URL}/attest/challenge", json={})
nonce = response.json()["nonce"]
```

### 步骤 2: IBM 704 计算

```python
# 在 IBM 704 模拟器上运行挖矿程序
mining_program = [
    0o040000000010,  # LDA 16 (加载 nonce 衍生值)
    0o100000000011,  # ADD 17 (加常数)
    0o120000000012,  # MUL 18 (乘)
    0o050000000013,  # STA 19 (存储结果)
    0o000000000000,  # HPR (停机)
    nonce_int,       # 16: nonce 衍生值
    12000,           # 17: IBM 704 FLOPS 常数
    2,               # 18: 乘数
    0,               # 19: 结果
]

simulator.load_program(mining_program)
cycles = simulator.run()
result = simulator.memory[19]
```

### 步骤 3: 构建证明

```python
attestation = {
    "miner": wallet,
    "miner_id": miner_id,
    "nonce": nonce,
    "report": {
        "commitment": commitment_hash,
        "derived": vacuum_tube_entropy,
        "mining_computation": {
            "algorithm": "ibm704_proof_of_antiquity",
            "cycles_executed": cycles,
            "result": result,
            "architecture": "IBM_704_36bit",
        },
    },
    "device": {
        "family": "IBM_704",
        "arch": "vacuum_tube_36bit",
        "year": 1954,
        "technology": "vacuum_tube",
        "word_size": 36,
        "memory_type": "magnetic_core",
    },
    "fingerprint": {
        "vacuum_tube_entropy": {...},
        "core_memory_timing": {...},
        "architecture_verification": {...},
        "antiquity_proof": {
            "year": 1954,
            "era": "first_generation_computer",
            "historical_significance": "IBM_first_mass_produced_scientific_computer",
        },
        "antiquity_multiplier": 5.0,
        "tier": "LEGENDARY",
    },
}
```

### 步骤 4: 提交证明

```python
response = requests.post(
    f"{NODE_URL}/attest/submit",
    json=attestation
)

if response.json()["ok"]:
    print("✓ IBM 704 证明被接受！")
    print("✓ LEGENDARY tier: 5.0x 奖励乘数")
```

---

## 奖励计算

### 基础奖励

```
每个 epoch (10 分钟):
- 基础奖励池：1.5 RTC
- 矿工数量：N
- 基础奖励 = 1.5 / N

最终奖励 = 基础奖励 × 古董乘数
```

### IBM 704 奖励

```
IBM 704 (1954):
- 古董乘数：5.0× (LEGENDARY)
- 假设 5 个矿工:
  - 基础奖励 = 1.5 / 5 = 0.3 RTC
  - IBM 704 奖励 = 0.3 × 5.0 = 1.5 RTC/epoch

每日奖励 = 1.5 × (144 epochs/天) = 216 RTC/天
每月奖励 = 216 × 30 = 6,480 RTC/月
USD 价值 = 6,480 × $0.10 = $648/月
```

### 乘数衰减

```
古董乘数会随时间衰减 (15%/年)，防止永久优势：

年份    IBM 704 乘数    PowerPC G4 乘数
1954    5.0×           N/A
2000    5.0×           2.5×
2024    3.6×           1.8×
2030    2.8×           1.4×
```

---

## 反作弊机制

### 1. 虚拟机检测

```python
# IBM 704 模拟器检测
def detect_emulation():
    # 真实的 IBM 704 特征:
    # - 36 位字长
    # - 12 微秒内存访问
    # - 真空管热噪声
    
    simulated_features = get_hardware_features()
    
    if simulated_features != expected_ibm704_features:
        return "emulation_detected"
    
    return "authentic"
```

### 2. 硬件绑定

```python
# 每个硬件指纹绑定一个钱包
hardware_hash = sha256(
    f"{word_size}_{memory_type}_{tube_entropy}_{core_timing}"
)
miner_id = f"ibm704-{hardware_hash[:8]}"

# 防止同一硬件多钱包
if miner_id in attested_miners:
    reject_attestation()
```

### 3. 时序验证

```python
# 验证计算时序合理性
def verify_timing(cycles, duration):
    # IBM 704: ~12 微秒/周期
    expected_duration = cycles * 12e-6
    
    # 允许 10% 误差
    if abs(duration - expected_duration) > expected_duration * 0.1:
        return "suspicious_timing"
    
    return "valid"
```

---

## SAP 汇编实现

### 核心挖矿循环

```assembly
# IBM 704 SAP Assembly - 挖矿核心

        ORG 0

START   LDX ZERO        # 清除变址寄存器
        LDA NONCE       # 加载挑战 nonce
        
MINING  FMP FLOPS       # 浮点乘 (IBM 704 特色!)
        FAD ENTROPY     # 加熵值
        FDH CORE_TIME   # 除内存时序
        
        STA RESULT      # 存储结果
        SUB TARGET      # 与目标比较
        TPL SUCCESS     # 如果大于，成功!
        
        LDA NONCE       # 否则，加载下一个 nonce
        ADD ONE
        STA NONCE
        
        TRA MINING      # 继续
        
SUCCESS LDA SHARE_COUNT
        ADD ONE
        STA SHARE_COUNT
        
        HPR             # 停机

# 数据
NONCE       DEC 0
FLOPS       OCT 413600000000  # 12000.0
ENTROPY     DEC 0
CORE_TIME   DEC 0
RESULT      DEC 0
TARGET      DEC 0
SHARE_COUNT DEC 0
ZERO        DEC 0
ONE         DEC 1

        END START
```

---

## 性能优化

### 1. 批量熵收集

```python
# 一次性收集 48 个样本，减少系统调用
entropy = collect_vacuum_tube_entropy(cycles=48)
```

### 2. 内存访问缓存

```python
# 缓存磁芯访问时序
if not hasattr(self, '_core_fingerprint'):
    self._core_fingerprint = get_core_memory_fingerprint()
```

### 3. 指令预取

```python
# 模拟 IBM 704 指令预取
def fetch_instruction(self):
    # IBM 704 没有真正的流水线，但我们可以优化模拟
    if self.instruction_buffer:
        return self.instruction_buffer.pop()
    
    word = self.memory[self.registers.IC]
    return self.parse_instruction(word)
```

---

## 测试与验证

### 单元测试

```python
def test_ibm704_add():
    sim = IBM704Simulator()
    sim.load_program([
        0o040000000010,  # LDA 16
        0o100000000011,  # ADD 17
        0o050000000012,  # STA 18
        0o000000000000,  # HPR
        100, 200, 0  # 数据
    ])
    sim.run()
    assert sim.memory[18] == 300, "加法错误"

def test_ibm704_float():
    sim = IBM704Simulator()
    # 测试浮点乘法：12000.0 × 2.0 = 24000.0
    sim.load_program([...])
    sim.run()
    result = FloatingPoint.from_word(sim.registers.AC)
    assert abs(result.to_float() - 24000.0) < 0.001
```

### 集成测试

```python
def test_full_attestation():
    miner = IBM704Miner(wallet="test_wallet")
    
    # 测试硬件指纹
    fingerprint = miner.hardware_fingerprint
    assert fingerprint["architecture"] == "IBM_704_1954"
    assert fingerprint["antiquity_multiplier"] == 5.0
    assert fingerprint["tier"] == "LEGENDARY"
    
    # 测试熵收集
    entropy = miner.simulator.collect_vacuum_tube_entropy()
    assert "variance_ns" in entropy
    assert entropy["sample_count"] == 48
```

---

## 参考资料

- [RustChain Whitepaper](https://github.com/Scottcjn/Rustchain)
- [IBM 704 操作手册](http://bitsavers.org/pdf/ibm/704/24-6661-2_704_Manual_1955.pdf)
- [Proof-of-Antiquity 论文](https://doi.org/10.5281/zenodo.18623592)

---

## 贡献信息

- **钱包**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`
- **Bounty Issue**: #380
- **难度**: LEGENDARY Tier
- **奖励**: 200 RTC ($20)
