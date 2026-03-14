# RustChain Electronic Quarterback (1978) Miner

## 🏈 项目概述

将 RustChain 矿工移植到 **Mattel Electronic Quarterback (1978)** - 经典手持 LED 游戏设备！

这是 RustChain Proof-of-Antiquity 的终极挑战：**在 1978 年的 LED 手持游戏上挖矿**。

## 📋 技术规格

### Electronic Quarterback 硬件
- **发布年份**: 1978
- **制造商**: Mattel Electronics
- **显示**: 红色 LED 点阵（约 20-30 个 LED）
- **输入**: 6-8 个按钮（方向 + 动作）
- **处理器**: 定制 COB（Chip on Board）ASIC
- **内存**: 极少量（估计 < 1KB）
- **电源**: 9V 电池

### 移植方案：Badge Only

由于 Electronic Quarterback 的极端资源限制，我们采用 **Badge Only 方案**：

1. **Raspberry Pi Pico 桥接** - 模拟控制器输入/输出
2. **LED 状态捕获** - 通过光敏电阻/光电二极管读取 LED 状态
3. **时序指纹** - 测量 ASIC 响应时间作为硬件指纹
4. **模拟器验证** - Python 模拟器交叉验证行为

## 🎯 挖矿架构

```
┌─────────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Electronic         │────▶│  Raspberry Pi    │────▶│  RustChain      │
│  Quarterback 1978   │◀────│  Pico Bridge     │◀────│  Node           │
│  (LED + ASIC)       │     │  (GPIO + ADC)    │     │  (PC/Server)    │
└─────────────────────┘     └──────────────────┘     └─────────────────┘
         │                          │                        │
         │  LED 状态 (光敏)          │  串口/USB              │  HTTP API
         │  按钮响应时序             │  _attestation          │  /attest/submit
         │  ASIC 特征延迟            │  /mine               │
```

## 📁 文件结构

```
electronic-quarterback-miner/
├── README.md                      # 本文件
├── eq_miner.py                    # Python 模拟器矿工
├── eq_pico_firmware/              # Pico 固件（Arduino/C++）
│   ├── eq_bridge.ino
│   └── eq_attestation.cpp
├── hardware/                      # 硬件设计文件
│   ├── schematic_eq_adapter.pdf
│   └── pcb_adapter.kicad
├── docs/                          # 文档
│   ├── setup_guide.md
│   ├── attestation_protocol.md
│   └── badge_spec.md
└── tests/                         # 测试
    ├── test_eq_simulator.py
    └── test_pico_bridge.py
```

## 🚀 快速开始

### 方案 A: Python 模拟器（无需硬件）

```bash
# 1. 克隆仓库
git clone https://github.com/Scottcjn/Rustchain.git
cd Rustchain/miners/electronic-quarterback

# 2. 运行模拟器
python eq_miner.py --wallet YOUR_WALLET --simulate

# 3. 获取 Badge
# 模拟器会生成 "EQ Badge" NFT 证明
```

### 方案 B: 真实硬件（推荐）

```bash
# 1. 构建硬件适配器
# 参考 hardware/schematic_eq_adapter.pdf

# 2. 烧录 Pico 固件
cd eq_pico_firmware
# 使用 Arduino IDE 烧录到 Raspberry Pi Pico

# 3. 连接 Electronic Quarterback
# 将 Pico GPIO 连接到 EQ 的按钮和 LED

# 4. 运行矿工
python eq_miner.py --wallet YOUR_WALLET --pico-port COM3
```

## 🎖️ Badge Only 规范

Electronic Quarterback 矿工获得独特的 **EQ Badge**：

```json
{
  "badge_type": "electronic_quarterback_1978",
  "tier": "LEGENDARY",
  "multiplier": 3.5,
  "attributes": {
    "hardware_era": "1978-1980",
    "display_type": "LED",
    "input_type": "buttons",
    "processor": "custom_asic",
    "rarity_score": 95
  }
}
```

### Badge 获取条件

1. **模拟器模式**: 完成 100 次有效 attestation
2. **真实硬件模式**: 完成 1 次 attestation（需要光敏验证）

## 💰 奖励计算

Electronic Quarterback 属于 **LEGENDARY Tier** 复古硬件：

| 指标 | 值 |
|------|-----|
| 基础乘数 | 3.5x |
| LED 显示奖励 | +0.3x |
| 定制 ASIC 奖励 | +0.2x |
| 1970 年代奖励 | +0.5x |
| **总乘数** | **4.5x** |

**预期收益**: 0.4-0.8 RTC/epoch（取决于网络难度）

## 🔧 硬件连接

### Pico GPIO 映射

```
Pico GPIO    →  Electronic Quarterback
────────────────────────────────────────
GPIO 0 (ADC) →  LED 阵列（通过光敏电阻）
GPIO 1 (ADC) →  LED 阵列（通过光敏电阻）
GPIO 2       →  按钮 1 (Up)
GPIO 3       →  按钮 2 (Down)
GPIO 4       →  按钮 3 (Left)
GPIO 5       →  按钮 4 (Right)
GPIO 6       →  按钮 5 (Pass/Action)
GPIO 7       →  按钮 6 (Reset)
VBUS         →  EQ VCC (如果需要外部供电)
GND          →  EQ GND
```

### 光敏传感器电路

```
LED 阵列 → 光敏电阻 → 10kΩ 下拉 → GND
                    │
                    └─→ Pico ADC (GPIO 0/1)
```

## 📊 Attestation 流程

1. **挑战接收**: Pico 从 RustChain 节点获取 nonce
2. **LED 激励**: Pico 按下 EQ 按钮序列
3. **响应捕获**: 光敏电阻读取 LED 响应模式
4. **时序测量**: 记录按钮→LED 延迟（ASIC 特征）
5. **哈希计算**: SHA256(nonce || wallet || timing_data)
6. **提交证明**: 发送到 RustChain 节点验证

## 🧪 模拟器模式

Python 模拟器提供：
- 完整的 EQ 行为模拟
- LED 显示渲染（终端/图形）
- 按钮输入处理
- 时序指纹生成（基于系统熵）

```python
from eq_miner import ElectronicQuarterback

eq = ElectronicQuarterback(wallet="YOUR_WALLET")
eq.attest(simulate=True)
eq.mine()
```

## 📝 待办事项

- [ ] 完成 Pico 固件
- [ ] 设计 PCB 适配器
- [ ] 真实硬件测试
- [ ] Badge NFT 集成
- [ ] 提交 PR 到 RustChain 主仓库

## 🎮 关于 Electronic Quarterback

Mattel Electronic Quarterback 是 1978 年发布的经典手持橄榄球游戏。
玩家控制一个 LED 点（四分卫），躲避防守队员（其他 LED）并传球。

**历史意义**: 
- 最早的 LED 手持游戏之一
- 展示了 1970 年代消费电子微型化
- Mattel Electronics 的标志性产品

## 📄 许可证

Apache License 2.0（与 RustChain 一致）

## 🙏 致谢

- RustChain 团队 - Proof-of-Antiquity 区块链
- Mattel Electronics - 创造经典手持游戏
- 复古计算社区 - 保存计算历史

---

**钱包地址**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`

**Bounty Issue**: #470 - Port Miner to Electronic Quarterback (1978)

**奖励**: 200 RTC ($20) - LEGENDARY Tier!
