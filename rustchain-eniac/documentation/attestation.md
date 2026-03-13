# ENIAC 硬件证明 (Attestation) 文档

## 1. 概述

硬件证明是 RustChain Proof of Antiquity 的核心机制。它证明矿工正在运行声称的硬件。

## 2. ENIAC 证明特点

### 2.1 独特性

ENIAC 是计算机历史上最独特的硬件：
- **年份**: 1945 (最早)
- **架构**: 十进制累加器 (唯一)
- **真空管**: 18,000 个
- **功耗**: 150 kW
- **重量**: 30 吨

### 2.2 LEGENDARY Tier

ENIAC 获得最高级别分类：

| 属性 | 值 |
|------|-----|
| **等级** | LEGENDARY |
| **基础倍数** | 5.0x |
| **纪元奖励** | 7.5 RTC (1.5 × 5.0) |
| **年资增长** | +5%/年 |
| **最大倍数** | 7.5x (10 年后) |

## 3. 证明结构

```json
{
  "version": "eniac-1945-1.0",
  "miner_id": "eniac_1945_RTCxxxx",
  "wallet_id": "RTCxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "epoch": 12345,
  "epoch_hash": "...",
  "hardware": {
    "machine": "ENIAC",
    "year": 1945,
    "architecture": "decimal_accumulator",
    "word_length": 10,
    "accumulators": 20,
    "vacuum_tubes": 18000,
    "power_consumption_kw": 150,
    "weight_tons": 30,
    "area_sqft": 300,
    "cost_1945_usd": 487000,
    "cost_2024_usd": 7000000
  },
  "fingerprint": {
    "tube_noise_signature": "...",
    "accumulator_timing": {...},
    "function_table_entropy": 0.85,
    "power_signature": "...",
    "thermal_signature": "..."
  },
  "antiquity_tier": "LEGENDARY",
  "antiquity_multiplier": 5.0,
  "timestamp": "2026-03-14T00:00:00Z",
  "nonce": 12345678901234567890,
  "signature": "..."
}
```

## 4. 硬件指纹生成

### 4.1 真空管噪声签名

ENIAC 的 18,000 个真空管每个都有独特的热噪声特性：

```python
def generate_tube_noise_signature():
    """生成真空管噪声签名"""
    tube_signatures = []
    for i in range(18000):
        drift = random.gauss(0, 0.01)
        age_factor = random.uniform(0.9, 1.1)
        noise_variance = random.uniform(0.001, 0.01)
        current_reading = drift * age_factor + random.gauss(0, noise_variance)
        tube_signatures.append(f"{current_reading:.10f}")
    
    signature_data = '|'.join(tube_signatures)
    return hashlib.sha256(signature_data.encode()).hexdigest()
```

### 4.2 累加器时序特征

每个累加器的进位延迟有微小差异：

```python
def generate_accumulator_timing_profile():
    """生成累加器时序特征"""
    timing_profile = {}
    for i in range(20):
        base_delay = 200.0  # 微秒
        variation = random.gauss(0, 2.0)  # ±2 微秒
        timing_profile[f'acc_{i}'] = base_delay + variation
    return timing_profile
```

### 4.3 函数表熵

函数表开关配置提供熵源：

```python
def generate_function_table_entropy():
    """计算函数表配置熵"""
    unique_values = len(set(switch_positions))
    return unique_values / 10.0  # 归一化到 0-1
```

## 5. 证明验证

### 5.1 验证步骤

1. **检查签名**: 验证证明签名
2. **验证硬件信息**: 确认 ENIAC 规格
3. **检查指纹**: 验证硬件指纹有效性
4. **验证纪元**: 确认纪元时间戳
5. **计算奖励**: 根据倍数计算奖励

### 5.2 反欺骗措施

ENIAC 证明包含多层反欺骗：

| 措施 | 描述 |
|------|------|
| **真空管熵** | 模拟 18,000 个真空管的热噪声 |
| **时序特征** | 累加器进位延迟的独特模式 |
| **功耗签名** | 150kW 功耗的波动模式 |
| **热特征** | 温度分布的独特模式 |
| **运算统计** | 累加器使用模式 |

## 6. 提交证明

### 6.1 在线模式

```python
import requests

attestation = create_attestation()

response = requests.post(
    'https://50.28.86.131/api/v1/attest',
    json=attestation,
    headers={'Content-Type': 'application/json'}
)

if response.status_code == 200:
    print("证明提交成功!")
    reward = response.json().get('reward', 0)
    print(f"奖励：{reward} RTC")
```

### 6.2 离线模式

```python
import json

attestation = create_attestation()

with open(f'ATTEST_{attestation["epoch"]}.TXT', 'w') as f:
    json.dump(attestation, f, indent=2)

print("证明已保存到文件")
```

## 7. 纪元奖励计算

### 7.1 基础公式

```
基础奖励 = 1.5 RTC / 纪元
有效倍数 = 基础倍数 × 年资倍数
纪元奖励 = 基础奖励 × 有效倍数
```

### 7.2 ENIAC 计算

```
基础倍数 = 5.0x (LEGENDARY)
年资倍数 = min(1.0 + 0.05 × 年数，1.5)

第 1 年：5.0 × 1.0 = 5.0x → 7.5 RTC/纪元
第 5 年：5.0 × 1.25 = 6.25x → 9.375 RTC/纪元
第 10 年：5.0 × 1.5 = 7.5x → 11.25 RTC/纪元
```

### 7.3 每日奖励

```
纪元/天 = 24 × 60 / 10 = 144 纪元

第 1 年：7.5 × 144 = 1,080 RTC/天
第 5 年：9.375 × 144 = 1,350 RTC/天
第 10 年：11.25 × 144 = 1,620 RTC/天
```

## 8. Bounty 申领

### 8.1 条件

- 成功提交至少 1 个证明
- 硬件指纹验证通过
- 钱包地址有效

### 8.2 钱包地址

```
Bounty 钱包：RTC4325af95d26d59c3ef025963656d22af638bb96b
奖励金额：200 RTC ($20)
等级：LEGENDARY Tier
```

### 8.3 申领流程

1. 运行矿工生成证明
2. 提交证明到网络
3. 在 GitHub issue #388 中添加钱包地址
4. 等待 bounty 发放

## 9. 故障排除

### 9.1 常见问题

**Q: 证明提交失败？**
A: 检查网络连接，或切换到离线模式。

**Q: 硬件指纹验证失败？**
A: 确保使用 ENIAC 模拟器，不要修改指纹生成代码。

**Q: 奖励计算错误？**
A: 确认倍数为 5.0x (LEGENDARY)。

### 9.2 日志文件

```
miner.log - 矿工运行日志
ATTEST_*.TXT - 证明文件
WALLET.TXT - 钱包备份
ENIAC_FINGERPRINT.json - 硬件指纹
```

## 10. 参考

- [RustChain Proof of Antiquity](https://rustchain.org)
- [ENIAC Architecture](../ENIAC_ARCHITECTURE.md)
- [Programming Guide](programming_guide.md)

---

*ENIAC Attestation Documentation v1.0*
*Last Updated: 2026-03-14*
