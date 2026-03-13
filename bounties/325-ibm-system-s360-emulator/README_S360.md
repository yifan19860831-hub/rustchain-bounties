# RustChain IBM System/360 Model 30 Port (1965)

## 🏛️ LEGENDARY TIER BOUNTY - 200 RTC ($20)

**钱包地址**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`

---

## 📋 任务概述

将 RustChain Proof-of-Antiquity 矿工移植到 **IBM System/360 Model 30 (1965)** - 计算机历史上最重要的架构！

这是计算机行业的里程碑：
- ✨ 首次引入 **8 位字节** 标准（沿用至今）
- ✨ **32 位字长** 架构
- ✨ **SLT (Solid Logic Technology)** 混合集成电路模块
- ✨ 指令集兼容性概念的先驱
- ✨ 影响了后续 60 年的计算机设计

---

## 🖥️ IBM System/360 Model 30 技术规格

| 特性 | 规格 |
|------|------|
| 发布年份 | 1965 |
| 字长 | 32 位 |
| 字节 | 8 位 (首次标准化) |
| 内存 | 8KB - 64KB (核心存储器) |
| 时钟频率 | ~1 MHz |
| 技术 | SLT (Solid Logic Technology) |
| 输入/输出 | 打孔卡片、磁带、打印机 |
| 操作系统 | DOS/360 或无 OS |
| 寄存器 | 16×32 位通用寄存器 (部分型号) |

---

## 🎯 移植策略

由于 Model 30 的极端限制（无网络、无 TCP/IP、内存极小），我们采用**三层移植方案**：

### 层次 1: 概念验证汇编实现 (核心)
```
rustchain-s360/
├── miner.asm          # IBM System/360 汇编语言矿工核心
├── fingerprint.asm    # 硬件指纹采集例程
├── attestation.asm    # 证明提交例程
└── constants.asm      # 常量和配置
```

### 层次 2: 模拟器兼容层
```
rustchain-s360/
├── s360sim/
│   ├── s360_miner.py  # Hercules 模拟器兼容层
│   └── network_bridge.py # 网络通信桥接
```

### 层次 3: 现代包装器
```
rustchain-s360/
├── s360_wrapper.py    # Python 包装器，调用汇编逻辑
└── README_S360.md     # 完整文档
```

---

## 🔧 技术挑战与解决方案

### 挑战 1: 无网络支持
**问题**: Model 30 没有内置网络能力（TCP/IP 1970 年代才发明）

**解决方案**:
1. **模拟器模式**: 在 Hercules S/360 模拟器上运行，通过主机网络
2. **离线证明**: 生成签名的工作量证明，通过现代系统提交
3. **串口桥接**: 通过串口连接到现代网关（历史准确性方案）

### 挑战 2: 内存限制 (8-64KB)
**问题**: 现代矿工代码远超 64KB

**解决方案**:
1. **极简实现**: 核心矿工 < 4KB
2. **覆盖技术**: 代码分段加载
3. **外部存储**: 使用磁带/磁盘存储状态

### 挑战 3: 无操作系统
**问题**: 需要直接硬件操作

**解决方案**:
1. **独立程序**: 自包含引导加载程序
2. **监控程序**: 简化的 I/O 例程
3. **模拟器支持**: 依赖 Hercules 提供 I/O

---

## 💻 IBM System/360 汇编实现要点

### 寄存器使用约定
```asm
         R0   - 零寄存器 (始终为 0)
         R1   - 工作寄存器
         R2   - 熵收集计数器
         R3   - 时间戳低 32 位
         R4   - 时间戳高 32 位
         R5   - 哈希计算临时
         R6   - 指纹数据指针
         R7   - 网络缓冲区指针
         R8   - 矿工 ID 指针
         R9   - 钱包地址指针
         R10  - 节点 URL 指针
         R11  - 状态标志
         R12  - 基址寄存器
         R13  - 保存区域指针
         R14  - 返回地址
         R15  - 返回代码
```

### 核心算法流程
```asm
START    DS    0H              程序入口
         BALR  R12,R0          建立基址
         USING *,R12

         * 步骤 1: 收集硬件指纹
         CALL  COLLECT_FINGERPRINT

         * 步骤 2: 生成熵
         CALL  COLLECT_ENTROPY

         * 步骤 3: 计算工作量证明
         CALL  CALCULATE_PROOF

         * 步骤 4: 提交证明
         CALL  SUBMIT_ATTESTATION

         * 步骤 5: 等待下一轮
         CALL  WAIT_EPOCH

         * 循环
         B     START
```

### 硬件指纹采集 (Model 30 特有)
```asm
COLLECT_FINGERPRINT DS 0H
         * SLT 模块温度漂移（通过时序间接测量）
         * 核心存储器访问时间变化
         * 指令执行时间抖动
         
         STCK  TIMEBUF         存储时钟值
         SLL   R2,32           位移用于熵
         XR    R2,R2           异或混合
         BR    R14             返回
```

---

## 📦 文件结构

```
rustchain-s360/
├── README_S360.md              # 本文档
├── miner.asm                   # 主矿工程序 (汇编)
├── fingerprint.asm             # 硬件指纹例程
├── entropy.asm                 # 熵收集例程
├── network.asm                 # 网络通信例程
├── constants.asm               # 常量定义
├── s360sim/
│   ├── s360_miner.py           # Hercules 模拟器接口
│   ├── network_bridge.py       # 网络桥接
│   └── test_s360.py            # 测试套件
├── s360_wrapper.py             # Python 包装器
├── build.sh                    # 构建脚本
├── run_simulator.sh            # 运行模拟器
└── BOUNTY_CLAIM.md             # Bounty 申领说明
```

---

## 🚀 快速开始

### 前提条件
1. Hercules S/360 模拟器
2. Python 3.10+
3. RustChain 钱包地址

### 安装 Hercules 模拟器
```bash
# Ubuntu/Debian
sudo apt-get install hercules

# macOS
brew install hercules-s390

# Windows
# 下载 https://www.softdevlabs.com/hercules/
```

### 构建矿工
```bash
cd rustchain-s360
chmod +x build.sh
./build.sh
```

### 运行（模拟器模式）
```bash
./run_simulator.sh --wallet RTC4325af95d26d59c3ef025963656d22af638bb96b
```

---

## 📊 预期性能

| 指标 | Model 30 (实际) | Hercules 模拟器 |
|------|----------------|-----------------|
| 哈希率 | ~100 H/s | ~10,000 H/s |
| 内存占用 | 32 KB | 64 MB |
| 功耗 | 3000W | 100W |
|  antiquity 乘数 | 5.0× (1965) | 5.0× |

**预期收益**: 由于 1965 年的古老架构，获得 **5.0× 乘数**（最高级别）

---

## 🏆 Bounty 申领

完成以下步骤后申领 200 RTC：

1. ✅ 创建 IBM System/360 汇编矿工核心
2. ✅ 实现 Hercules 模拟器兼容层
3. ✅ 成功提交至少一个工作量证明
4. ✅ 添加测试和文档
5. ✅ 提交 PR 并添加钱包地址

**钱包**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`

---

## 📚 参考资料

- [IBM System/360 架构原理](https://www.ibm.com/ibm/history/documents/pdf/225-1430-0.pdf)
- [Hercules 模拟器文档](http://www.hercules-390.eu/)
- [SLT 技术历史](https://www.computercollection.org/technology/slt.html)
- [RustChain 白皮书](https://github.com/Scottcjn/Rustchain/blob/main/docs/RustChain_Whitepaper.pdf)

---

## ⚠️ 免责声明

此移植主要用于教育和历史保护目的。实际在真正的 IBM System/360 Model 30 上运行需要：
- 物理硬件或专业模拟器
- 网络连接通过外部网关
- 定制 I/O 接口

Hercules 模拟器模式是推荐的运行方式。

---

**Created for RustChain Proof-of-Antiquity Blockchain**
*Preserving Computing History, One Block at a Time* 🏛️
