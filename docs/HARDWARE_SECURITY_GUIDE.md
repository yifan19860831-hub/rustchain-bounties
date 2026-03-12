# RustChain Hardware Security Guide

> **奖励：** 3 RTC  
> **难度：** Standard  
> **类别：** 安全文档

## 目录

1. [概述](#概述)
2. [硬件指纹验证机制](#硬件指纹验证机制)
3. [防虚拟机检测](#防虚拟机检测)
4. [安全最佳实践](#安全最佳实践)
5. [故障排查](#故障排查)
6. [参考资料](#参考资料)

---

## 概述

RustChain 使用 **Proof-of-Antiquity** 共识机制，通过硬件指纹验证确保只有真实的物理硬件能够获得完整的挖矿奖励。本指南详细说明硬件安全机制的工作原理、如何防止虚拟机/模拟器攻击，以及矿工应遵循的安全最佳实践。

### 核心原则

- **每个硬件设备 = 1 票**：无论硬件速度如何，每个通过验证的设备在每个 epoch 获得恰好 1 票
- **古老硬件奖励更高**： vintage 硬件获得 1.5-2.5 倍奖励乘数
- **严格反模拟**：虚拟机/模拟器获得 10 亿分之一的惩罚性奖励

---

## 硬件指纹验证机制

RustChain 执行 **6+1 项独立检查** 来验证硬件真实性。必须通过至少 **5 项检查** 才能获得完整奖励。

### 检查 1：时钟偏移与振荡器漂移 (Clock-Skew & Oscillator Drift)

#### 原理
每个物理 CPU 都有晶体振荡器，存在制造缺陷和老化特征。真实硬件有可测量的漂移（5-50 ppm）和抖动（100-2000 ns）。虚拟机使用宿主机时钟，过于完美。

#### 检测阈值

| 硬件类型 | 漂移 (ppm) | 抖动 (ns) | 判定 |
|---------|-----------|----------|------|
| 真实 vintage (G4/G5) | 15-50 | 500-2000 | ✅ 通过 |
| 真实现代 (x86) | 5-20 | 100-800 | ✅ 通过 |
| VM (VMware/QEMU) | <1 | <10 | ❌ 失败 |
| 模拟器 (SheepShaver) | <0.5 | <5 | ❌ 失败 |

#### 指纹结构
```json
{
  "clock_skew": {
    "drift_ppm": 24.3,
    "jitter_ns": 1247,
    "oscillator_age_estimate": 24
  }
}
```

### 检查 2：缓存时序指纹 (Cache Timing Fingerprint)

#### 原理
真实 CPU 具有多级缓存层次结构（L1 → L2 → L3），具有明显的延迟差异。L1 为 3-5 周期，L2 为 10-20 周期。模拟器会扁平化这种层次结构。

#### 检测阈值

| 硬件类型 | L1 (ns) | L2 (ns) | L2/L1 比率 | 判定 |
|---------|--------|--------|-----------|------|
| PowerPC G4 | 4-6 | 12-18 | 3.0-3.5 | ✅ 通过 |
| x86_64 (现代) | 1-2 | 4-8 | 3.0-4.0 | ✅ 通过 |
| VM (VMware) | 10-20 | 15-25 | 1.2-1.5 | ❌ 失败 |
| 模拟器 (QEMU) | 50-100 | 50-100 | ~1.0 | ❌ 失败 |

#### 指纹结构
```json
{
  "cache_timing": {
    "l1_latency_ns": 5,
    "l2_latency_ns": 15,
    "l3_latency_ns": null,
    "hierarchy_ratio": 3.0
  }
}
```

### 检查 3：SIMD 单元识别 (SIMD Unit Identity)

#### 原理
每个 SIMD 指令集（AltiVec、SSE、NEON）具有独特的流水线特征。通过计时向量操作，我们可以指纹识别确切的实现。

#### 检测阈值

| SIMD 类型 | 流水线偏置 | 判定 |
|----------|-----------|------|
| AltiVec (G4/G5) | 0.65-0.85 | ✅ 通过 |
| SSE2 (x86) | 0.45-0.65 | ✅ 通过 |
| NEON (ARM) | 0.55-0.75 | ✅ 通过 |
| 模拟 AltiVec | 0.3-0.5 | ❌ 失败 |

#### 指纹结构
```json
{
  "simd_identity": {
    "instruction_set": "AltiVec",
    "pipeline_bias": 0.76,
    "vector_width": 128
  }
}
```

### 检查 4：热漂移熵 (Thermal Drift Entropy)

#### 原理
真实 CPU 在负载下会产生热量并具有自然方差。虚拟机报告静态温度或传递与工作量不相关的宿主机温度。

#### 检测阈值

| 硬件类型 | 空闲 (°C) | 负载 (°C) | 方差 | 判定 |
|---------|----------|----------|-----|------|
| 真实 G4/G5 | 35-50 | 60-85 | 2-6 | ✅ 通过 |
| 真实 x86 | 30-45 | 50-80 | 1-4 | ✅ 通过 |
| VM (VMware) | 40 | 40 | <0.1 | ❌ 失败 |

#### 指纹结构
```json
{
  "thermal_entropy": {
    "idle_temp_c": 42.1,
    "load_temp_c": 71.3,
    "variance": 3.8,
    "sensor_count": 3
  }
}
```

### 检查 5：指令路径抖动 (Instruction Path Jitter)

#### 原理
真实硅芯片由于分支预测、缓存冲突和流水线停顿，存在纳秒级执行方差。虚拟机具有确定性执行，抖动接近零。

#### 检测阈值

| 硬件类型 | 平均值 (ns) | 标准差 (ns) | 判定 |
|---------|------------|------------|------|
| 真实 G4/G5 | 2000-5000 | 500-2000 | ✅ 通过 |
| 真实 x86 | 500-2000 | 50-500 | ✅ 通过 |
| VM (QEMU) | 10000-50000 | <10 | ❌ 失败 |

#### 指纹结构
```json
{
  "instruction_jitter": {
    "mean_ns": 3200,
    "stddev_ns": 890,
    "samples": 10000
  }
}
```

### 检查 6：反模拟检查 (Anti-Emulation Checks)

#### 原理
虚拟机管理程序在 CPUID、MAC 地址 OUI、DMI/SMBIOS 数据和 PCI 设备 ID 中留下可检测的签名。

#### 虚拟机签名检测

| 检查项 | 虚拟机指标 |
|-------|-----------|
| CPUID | 虚拟机管理程序位被设置 |
| MAC OUI | 00:05:69, 00:0C:29 (VMware), 08:00:27 (VirtualBox), 52:54:00 (QEMU) |
| DMI | 系统信息中包含 "vmware"、"virtualbox"、"qemu" |
| 进程 | 运行 vmware、vbox、qemu 进程 |

#### 指纹结构
```json
{
  "behavioral_heuristics": {
    "cpuid_clean": true,
    "mac_oui_valid": true,
    "no_hypervisor": true,
    "dmi_authentic": true
  }
}
```

### +1. 行为启发式检查 (Behavioral Heuristics)

额外的虚拟机管理程序签名检测，作为第 6 项检查的补充。

---

## 防虚拟机检测

### 组合验证流程

```
┌─────────────────┐
│ 接收指纹数据     │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│           6 项检查执行                   │
│  1. 时钟偏移      ✓/✗                   │
│  2. 缓存时序      ✓/✗                   │
│  3. SIMD 识别     ✓/✗                   │
│  4. 热熵          ✓/✗                   │
│  5. 指令抖动      ✓/✗                   │
│  6. 反模拟        ✓/✗                   │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│ 计算通过次数     │
└────────┬────────┘
         │
    ┌────┴────┐
    │ ≥5 通过？│
    └────┬────┘
         │
    ┌────┴────┐
    │         │
   是        否
    │         │
    ▼         ▼
┌───────┐ ┌──────────────┐
│ 1.0×  │ │ 0.0000000025×│
│ 奖励  │ │ 惩罚性奖励    │
└───────┘ └──────────────┘
```

### 惩罚乘数

| 失败检查数 | 乘数 | 效果 |
|-----------|------|------|
| 0 | 1.0× | 完整奖励 |
| 1 | 0.5× | 50% 惩罚 |
| 2+ | 0.0000000025× | 10 亿分之一（虚拟机惩罚） |

### 实际对比示例

#### 真实 PowerPC G4 ✅
```json
{
  "clock_skew": {"drift_ppm": 24.3, "jitter_ns": 1247},
  "cache_timing": {"hierarchy_ratio": 3.0},
  "simd_identity": {"pipeline_bias": 0.76},
  "thermal_entropy": {"variance": 3.8},
  "instruction_jitter": {"stddev_ns": 890},
  "behavioral_heuristics": {"cpuid_clean": true, "no_hypervisor": true}
}
```
**结果**：6 项检查全部通过 → 2.5× 乘数

#### SheepShaver 模拟器 ❌
```json
{
  "clock_skew": {"drift_ppm": 0.3, "jitter_ns": 4},
  "cache_timing": {"hierarchy_ratio": 1.04},
  "simd_identity": {"pipeline_bias": 0.42},
  "thermal_entropy": {"variance": 0},
  "instruction_jitter": {"stddev_ns": 2},
  "behavioral_heuristics": {"no_hypervisor": false}
}
```
**结果**：5 项检查失败 → 0.0000000025× 乘数

---

## 安全最佳实践

### 对矿工的建議

#### 1. 硬件准备
- **使用真实物理硬件**：不要尝试在虚拟机中挖矿
- **保持硬件稳定**：避免超频，这可能导致指纹特征异常
- **确保温度传感器工作**：热熵检查需要准确的温度读数
- **使用原生操作系统**：避免在模拟层上运行

#### 2. 网络配置
- **使用真实 MAC 地址**：不要使用虚拟化网络适配器
- **避免 NAT 链过长**：可能导致时钟同步问题
- **稳定网络连接**：attestation 提交需要可靠连接

#### 3. 系统配置
```bash
# Linux - 禁用可能干扰指纹的虚拟化功能
sudo rmmod kvm_intel  # 或 kvm_amd
sudo rmmod vboxdrv   # 如果安装了 VirtualBox

# macOS - 确保温度传感器可访问
sudo pmset -a thermlog 1
```

#### 4. 钱包安全
- **每个硬件 = 一个钱包**：不要尝试多个钱包绑定同一硬件
- **保护私钥**：使用安全的密钥存储
- **定期备份**：备份钱包配置文件

### 对开发者的建议

#### 1. 指纹验证代码
```python
def validate_fingerprint(fingerprint: dict) -> tuple[bool, float]:
    """
    验证硬件指纹并返回乘数
    
    Returns:
        (is_valid, multiplier): 验证结果和奖励乘数
    """
    checks = [
        check_clock_skew(fingerprint),
        check_cache_timing(fingerprint),
        check_simd_identity(fingerprint),
        check_thermal_entropy(fingerprint),
        check_instruction_jitter(fingerprint),
        check_anti_emulation(fingerprint),
    ]
    
    passed = sum(1 for check in checks if check)
    
    if passed >= 5:
        return True, 1.0
    elif passed == 4:
        return True, 0.5
    else:
        return False, 0.0000000025
```

#### 2. 模糊测试 (Fuzzing)
对 attestation 接口进行模糊测试，确保能够处理恶意输入：

```bash
# 运行回归测试
python -m pytest tests/test_attestation_fuzz.py -v

# 10,000 次变异测试
ATTEST_FUZZ_CASES=10000 python -m pytest tests/test_attestation_fuzz.py -v
```

#### 3. 输入验证
- **严格 JSON Schema 验证**：拒绝格式错误的 attestation
- **范围检查**：验证所有数值在合理范围内
- **签名验证**：使用 Ed25519 验证 attestation 签名

### 攻击缓解

| 攻击类型 | 缓解措施 |
|---------|---------|
| 时钟注入 | 交叉引用缓存时序 |
| 伪造热数据 | 与指令抖动关联 |
| MAC 欺骗 | 结合 DMI 检查 |
| CPUID 屏蔽 | 行为分析 |
| 重放攻击 | Nonce + 时间戳验证 |

---

## 故障排查

### 常见问题

#### 问题 1：验证失败 - 时钟偏移异常
**症状**：`clock_skew` 检查失败  
**可能原因**：
- 系统时间同步服务干扰（NTP）
- 虚拟机环境
- 硬件时钟故障

**解决方案**：
```bash
# 临时禁用 NTP 进行 attestation
sudo systemctl stop systemd-timesyncd
# 执行 attestation
# 重新启用
sudo systemctl start systemd-timesyncd
```

#### 问题 2：验证失败 - 缓存层次结构扁平
**症状**：`cache_timing` 比率接近 1.0  
**可能原因**：
- 虚拟机环境
- 模拟器（如 SheepShaver、QEMU）

**解决方案**：在真实物理硬件上运行矿工

#### 问题 3：验证失败 - 检测到虚拟机管理程序
**症状**：`behavioral_heuristics.no_hypervisor` 为 false  
**可能原因**：
- 在 VM 中运行
- 启用了虚拟化功能

**解决方案**：
```bash
# 检查是否运行在 VM 中
systemd-detect-virt

# 禁用 KVM 模块
sudo rmmod kvm_intel kvm
```

#### 问题 4：温度读数缺失
**症状**：`thermal_entropy` 检查失败  
**可能原因**：
- 温度传感器不可访问
- 驱动程序问题

**解决方案**：
```bash
# Linux - 安装 lm-sensors
sudo apt install lm-sensors
sudo sensors-detect

# 读取温度
sensors

# macOS - 使用 osx-cpu-temp
pip install osx-cpu-temp
```

### 验证测试

使用以下命令测试硬件验证：

```bash
# 检查节点健康
curl -sk https://rustchain.org/health

# 查看活动矿工
curl -sk https://rustchain.org/api/miners

# 测试 attestation 提交
curl -sk -X POST https://rustchain.org/attest/submit \
  -H "Content-Type: application/json" \
  -d @fingerprint.json
```

---

## 参考资料

### 文档
- [Protocol Specification](./PROTOCOL.md) - RIP-200 共识协议完整规范
- [Hardware Fingerprinting](./hardware-fingerprinting.md) - 硬件指纹技术细节
- [Token Economics](./token-economics.md) - RTC 供应和分配
- [Attestation Fuzzing](./attestation_fuzzing.md) - 模糊测试指南

### API 端点
- `GET /health` - 节点健康检查
- `GET /epoch` - 当前 epoch 信息
- `GET /api/miners` - 活动矿工列表
- `POST /attest/submit` - 提交硬件 attestation
- `GET /wallet/balance?miner_id={id}` - 查询钱包余额

### 外部资源
- [RustChain Whitepaper](./RustChain_Whitepaper_Flameholder_v0.97.pdf)
- [GitHub Repository](https://github.com/Scottcjn/Rustchain)
- [Discord Community](https://discord.gg/VqVVS2CW9Q)
- [Block Explorer](https://rustchain.org/explorer)

---

## 版本历史

| 版本 | 日期 | 变更 |
|-----|------|------|
| 1.0 | 2026-03-12 | 初始版本 |

---

**维护者**: RustChain Security Team  
**许可证**: MIT License  
**最后更新**: 2026-03-12
