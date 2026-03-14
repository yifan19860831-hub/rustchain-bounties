# RIP-EQ: Electronic Quarterback Attestation Protocol

## 概述

本规范定义了 Electronic Quarterback (1978) 设备的 RustChain Attestation 协议。

**文档版本**: 1.0.0  
**状态**: Draft  
**Bounty**: #470 - 200 RTC ($20)

## 1. 设计目标

1. **证明真实硬件**: 区分真实 1978 年 ASIC 与模拟器/FPGA
2. **最小侵入性**: 不修改原始设备 PCB
3. **可重复性**: 多次 attestation 结果一致
4. **抗欺骗**: 防止重放攻击和代理攻击

## 2. 硬件指纹特征

### 2.1 ASIC 时序特征

Electronic Quarterback 的定制 ASIC 具有独特的时序特征：

| 特征 | 典型值 | 容差 | 说明 |
|------|--------|------|------|
| 按钮响应延迟 | 847 μs | ±15% | 按钮按下到 LED 变化 |
| LED 上升时间 | 2.3 μs | ±10% | LED 从 10% 到 90% 亮度 |
| 时钟频率 | ~500 kHz | ±20% | 估计 ASIC 时钟 |
| 指令周期 | 8-12 μs | ±10% | 单条指令执行时间 |

### 2.2 温度漂移特性

ASIC 时序随温度变化：

```
延迟 (μs) = 847 × (1 + 0.003 × (T - 25))

其中 T 为摄氏温度
温度系数：0.3%/°C
```

### 2.3 电源噪声特征

电池电压波动影响时序：

```
延迟 (μs) = 847 × (1 + 0.02 × (9.0 - Vbat))

其中 Vbat 为电池电压 (V)
电压系数：2%/V
```

## 3. Attestation 流程

### 3.1 协议概览

```
┌─────────┐      ┌─────────┐      ┌─────────┐      ┌─────────┐
│  Miner  │      │  Pico   │      │    EQ   │      │   Node  │
│  (PC)   │      │ Bridge  │      │ (1978)  │      │         │
└────┬────┘      └────┬────┘      └────┬────┘      └────┬────┘
     │                │                │                │
     │ ATTEST nonce   │                │                │
     │───────────────>│                │                │
     │                │ BUTTON press   │                │
     │                │───────────────>│                │
     │                │                │                │
     │                │ LED response   │                │
     │                │<───────────────│                │
     │                │                │                │
     │                │ timing_data    │                │
     │<───────────────│                │                │
     │                │                │                │
     │ SUBMIT proof   │                │                │
     │─────────────────────────────────────────────────>│
     │                │                │                │
     │ OK/FAIL        │                │                │
     │<─────────────────────────────────────────────────│
     │                │                │                │
```

### 3.2 详细步骤

#### 步骤 1: 挑战生成

```python
import hashlib
import time
import uuid

# 节点生成挑战
nonce = hashlib.sha256(
    f"{time.time()}-{uuid.uuid4()}".encode()
).hexdigest()[:16]

# 挑战有效期：60 秒
challenge = {
    "nonce": nonce,
    "timestamp": time.time(),
    "expiry": 60
}
```

#### 步骤 2: 按钮激励序列

Pico 执行预定义按钮序列：

```
序列：[2, 0, 4, 1, 5, 3, 0, 2, 4, 1, 5, 3]
      (Down, Up, Left, Down, Reset, Right, ...)

每个按钮:
1. GPIO 输出 HIGH (50ms)
2. 等待 ASIC 响应
3. 读取光敏传感器
4. 记录响应时间
5. GPIO 输出 LOW
6. 延迟 50ms (防止连击)
```

#### 步骤 3: 时序数据采集

```python
timing_samples = []

for button_id in button_sequence:
    t0 = time.perf_counter_ns()
    
    # 按下按钮
    pico.press_button(button_id)
    
    # 等待 LED 变化
    baseline = pico.read_led_sensor()
    timeout = 1_000_000  # 1 秒
    
    while time.perf_counter_ns() - t0 < timeout:
        current = pico.read_led_sensor()
        if abs(current - baseline) > threshold:
            break
    
    t1 = time.perf_counter_ns()
    response_time = (t1 - t0) // 1000  # μs
    timing_samples.append(response_time)
```

#### 步骤 4: 统计计算

```python
import statistics

mean_time = statistics.mean(timing_samples)
variance = statistics.pvariance(timing_samples)
std_dev = statistics.stdev(timing_samples)
min_time = min(timing_samples)
max_time = max(timing_samples)

# 计算变异系数 (CV)
cv = std_dev / mean_time

# 真实硬件 CV 应该在 0.10-0.20 之间
# 模拟器/ FPGA 通常 CV < 0.05 (过于均匀)
```

#### 步骤 5: 哈希计算

```python
# 构建 attestation 数据
attestation = {
    "nonce": nonce,
    "wallet": wallet,
    "timing": {
        "mean": mean_time,
        "variance": variance,
        "samples": timing_samples
    },
    "led_pattern": led_pattern,
    "timestamp": time.time()
}

# 计算承诺哈希
hash_input = f"{nonce}{wallet}{json.dumps(timing, sort_keys=True)}"
commitment = hashlib.sha256(hash_input.encode()).hexdigest()
```

#### 步骤 6: 提交验证

```python
payload = {
    "miner": wallet,
    "miner_id": f"eq1978-{uuid.uuid4().hex[:8]}",
    "nonce": nonce,
    "report": {
        "commitment": commitment,
        "timing_fingerprint": timing,
        "led_pattern": led_pattern
    },
    "device": {
        "type": "electronic_quarterback_1978",
        "manufacturer": "Mattel Electronics",
        "year": 1978,
        "tier": "LEGENDARY"
    },
    "badge": {
        "type": "electronic_quarterback_1978",
        "multiplier": 4.5
    }
}

response = requests.post(
    f"{NODE_URL}/attest/submit",
    json=payload
)
```

## 4. 验证规则

### 4.1 时序有效性检查

节点验证时序数据：

```python
def validate_timing(timing_data) -> Tuple[bool, str]:
    mean = timing_data["mean"]
    variance = timing_data["variance"]
    cv = (variance ** 0.5) / mean
    
    # 检查均值范围 (700-1000 μs)
    if not (700 <= mean <= 1000):
        return False, f"Mean out of range: {mean}"
    
    # 检查变异系数 (0.08-0.25)
    if not (0.08 <= cv <= 0.25):
        return False, f"CV suspicious: {cv:.4f}"
    
    # 检查样本数量
    if len(timing_data["samples"]) < 8:
        return False, "Insufficient samples"
    
    # 检查异常值
    samples = timing_data["samples"]
    for s in samples:
        if abs(s - mean) > mean * 0.5:
            return False, f"Outlier detected: {s}"
    
    return True, "OK"
```

### 4.2 重放攻击防护

```python
# 节点维护 nonce 缓存 (最近 5 分钟)
used_nonces = {}

def check_replay(nonce: str, timestamp: float) -> bool:
    current_time = time.time()
    
    # 清理过期 nonce
    expired = [n for n, t in used_nonces.items() 
               if current_time - t > 300]
    for n in expired:
        del used_nonces[n]
    
    # 检查重复
    if nonce in used_nonces:
        return False  # 重放攻击
    
    # 检查时间戳 (不能是未来)
    if timestamp > current_time + 60:
        return False
    
    # 记录 nonce
    used_nonces[nonce] = current_time
    return True
```

### 4.3 集群检测

```python
def detect_fleet(attestations: List[Dict]) -> List[str]:
    """
    检测可能的矿场攻击（多个 EQ 在同一位置）
    """
    suspicious = []
    
    # 按 IP 分组
    by_ip = defaultdict(list)
    for att in attestations:
        by_ip[att["ip"]].append(att)
    
    # 检查同一 IP 的多个 EQ
    for ip, atts in by_ip.items():
        if len(atts) > 3:  # 阈值：3 个设备
            suspicious.extend([a["miner_id"] for a in atts])
    
    # 检查时序相关性
    # (真实独立设备的时序应该是独立的)
    
    return suspicious
```

## 5. Badge 规范

### 5.1 Badge 类型

```json
{
  "badge_type": "electronic_quarterback_1978",
  "tier": "LEGENDARY",
  "version": "1.0",
  "attributes": {
    "hardware_era": "1970s",
    "display_type": "LED",
    "input_type": "buttons",
    "processor": "custom_asic",
    "rarity_score": 95,
    "historical_significance": "high"
  }
}
```

### 5.2 获取条件

| 模式 | 要求 | Badge 进度 |
|------|------|------------|
| 模拟器 | 100 次有效 attestation | +1%/次 |
| 真实硬件 | 1 次有效 attestation | 100% (立即获得) |

### 5.3 Badge 奖励

- **基础乘数**: 4.5x
- **LED 显示奖励**: +0.3x
- **定制 ASIC 奖励**: +0.2x
- **1970 年代奖励**: +0.5x
- **总乘数**: **5.5x** (最高)

## 6. 安全考虑

### 6.1 已知攻击向量

| 攻击类型 | 风险 | 缓解措施 |
|----------|------|----------|
| 模拟器冒充 | 中 | 时序指纹 CV 检查 |
| FPGA 重放 | 高 | 温度/电压漂移验证 |
| 代理 attestation | 中 | 集群检测 |
| 光传感器欺骗 | 低 | 多传感器交叉验证 |

### 6.2 未来改进

1. **温度传感器集成**: 验证 ASIC 温度漂移
2. **电压监测**: 验证电池电压影响
3. **声学指纹**: 录制 ASIC 工作声音（独特噪声）
4. **电磁辐射**: 测量 ASIC 电磁特征

## 7. 参考实现

### 7.1 Python 矿工

```python
from eq_miner import ElectronicQuarterbackMiner

miner = ElectronicQuarterbackMiner(wallet="YOUR_WALLET")
miner.attest(simulate=False)  # 真实硬件模式
```

### 7.2 Pico 固件

```cpp
// 见 eq_pico_firmware/eq_bridge.ino
void handle_attest(char* nonce, char* wallet) {
  collect_timing_fingerprint();
  compute_sha256();
  send_response();
}
```

## 8. 变更日志

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-14 | 初始版本 |

## 9. 参考资料

- [RustChain Proof-of-Antiquity Whitepaper](../whitepaper/RustChain_Whitepaper.pdf)
- [RIP-0683: Console Mining](../CONSOLE_MINING_SETUP.md)
- [Electronic Quarterback Technical Analysis](https://www.handheldmuseum.com/)

---

**作者**: RustChain Core Team  
**许可**: Apache License 2.0  
**Bounty Wallet**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`
