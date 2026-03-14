# EDSAC 2 RTC Miner — 200 RTC Bounty (LEGENDARY Tier)

## 🎯 任务目标

将 RustChain 矿工移植到 **EDSAC 2 (1958)** — 第一台微程序化计算机！

**钱包地址**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`

**奖励**: 200 RTC ($20) - LEGENDARY Tier!

---

## 📜 为什么选择 EDSAC 2？

EDSAC 2 是计算机历史上的里程碑：

- **1958 年** — 第一台微程序化计算机
- **微程序控制单元** — 确立了微编程作为计算机设计基础的可行性
- **位片式架构** — 模块化插件单元，可互换
- **磁芯内存** — 32×32 铁氧体环矩阵（取代了 EDSAC 1 的水银延迟线）
- **40 位字长** — 比 EDSAC 1 的 17 位大幅提升
- **1024 字 RAM + 768 字 ROM** — 当时领先的存储容量
- **历史意义** — 用于计算椭圆曲线，导致 Birch 和 Swinnerton-Dyer 猜想（千禧年大奖难题）

### EDSAC 2 vs EDSAC 1 vs SWAC

| 特性 | EDSAC 2 (1958) | EDSAC 1 (1949) | SWAC (1950) |
|------|----------------|----------------|-------------|
| 内存技术 | 磁芯内存 | 水银延迟线 | Williams 管 (CRT) |
| 字长 | 40 位 | 17 位 | 37 位 |
| 内存容量 | 1024 字 RAM | 512-1024 字 | 256-512 字 |
| 指令长度 | 20 位 | 17 位 | 37 位 |
| 地址长度 | 11 位 | 10 位 | 10 位 |
| 索引寄存器 | 2 个 | 无 (1953 年添加) | 无 |
| 微程序 | ✅ 是 | ❌ 否 | ❌ 否 |
| 加法时间 | 17-42 μs | 1.5 ms | 64 μs |
| 浮点加法 | 100-170 μs | ❌ 无硬件支持 | ❌ 无硬件支持 |

### EDSAC 2 5.0x 乘数

```
edsac2 / magnetic_core / microprogrammed — 5.0x base multiplier (MAXIMUM TIER)
```

来自博物馆的 EDSAC 2 = RustChain 历史上收益最高的矿工之一。

### 预期收益

| 指标 | 值 |
|------|-----|
| 基础奖励 | 0.12 RTC/epoch |
| 5.0× 乘数 | 0.60 RTC/epoch |
| 每天 (144 epochs) | 86.4 RTC |
| 每月 | ~2,592 RTC |
| 每年 | ~31,104 RTC |

按 $0.10/RTC 计算：约 **$3,110/年** 挖矿奖励。

---

## 🏗️ EDSAC 2 架构详情

### 内存系统

**磁芯内存**:
- 32×32 铁氧体环矩阵
- 40 位/字 (+ 奇偶校验位)
- 1024 字 RAM (标准)
- 768 字 ROM (微程序存储)
- 访问时间：~17-42 μs (定点加法)
- 非易失性：断电后数据保留
- 破坏性读取：读取后需要重写

### CPU 架构

| 特性 | 规格 |
|------|------|
| 指令长度 | 20 位 |
| 地址长度 | 11 位 |
| 索引寄存器 | 2 个 (B 寄存器) |
| 累加器 | 40 位 |
| 时钟 | ~500 kHz (估计) |
| 定点加法 | 17-42 μs |
| 浮点加法 | 100-170 μs |
| 乘法 | 硬件支持 (通过微程序) |

### 指令集 (EDSAC 2)

EDSAC 2 使用微程序控制，指令集比 EDSAC 1 更丰富：

| 操作码 | 助记符 | 描述 |
|--------|--------|------|
| 0x00 | STOP | 停止执行 |
| 0x01 | ADD | 加到累加器 |
| 0x02 | SUB | 从累加器减 |
| 0x03 | MUL | 乘法 (微程序) |
| 0x04 | DIV | 除法 (微程序) |
| 0x05 | AND | 按位与 |
| 0x06 | OR | 按位或 |
| 0x07 | XOR | 按位异或 |
| 0x08 | SHL | 左移 |
| 0x09 | SHR | 右移 |
| 0x0A | JMP | 无条件跳转 |
| 0x0B | JZ | 零时跳转 |
| 0x0C | JN | 负时跳转 |
| 0x0D | LD | 从内存加载 |
| 0x0E | ST | 存储到内存 |
| 0x0F | IN | 从纸带输入 |
| 0x10 | OUT | 输出到纸带 |
| 0x11 | IDX1 | 使用索引寄存器 B1 |
| 0x12 | IDX2 | 使用索引寄存器 B2 |

### 指令格式

```
┌─────────┬─────┬───────────┬──────┐
│ 操作码  │ 索引│ 地址      │ 长度 │
│ 5 位    │ 2 位 │ 11 位     │ 2 位 │
│ bits 0-4│5-6  │ bits 7-17 │18-19 │
└─────────┴─────┴───────────┴──────┘
```

- **操作码**: 5 位，定义操作类型
- **索引**: 2 位，选择索引寄存器 (00=无，01=B1，10=B2，11=保留)
- **地址**: 11 位，内存地址 (0-2047)
- **长度**: 2 位，操作数长度 (01=单字 40 位，10=双字 80 位)

---

## 📋 实施计划

### Phase 1: 模拟器开发 (50 RTC)

**目标**: 创建功能完整的 EDSAC 2 模拟器

- **实现 EDSAC 2 CPU 模拟器** (Python/C++)
  - 40 位算术
  - 2 个索引寄存器
  - 微程序控制单元模拟
  - 磁芯内存模型 (包括破坏性读取)
  
- **创建汇编器**
  - EDSAC 2 原始汇编语法
  - 符号标签支持
  - 索引寄存器自动处理
  - 纸带格式输出 (二进制/ASCII)
  
- **开发调试工具**
  - 内存转储
  - 单步执行
  - 断点支持
  - 寄存器可视化

**交付物**:
- `edsac2-sim/` — 模拟器源代码
- `edsac2-assembler/` — 交叉汇编器
- 文档：架构参考手册

### Phase 2: SHA256 实现 (75 RTC)

**目标**: 在 EDSAC 2 上实现 SHA256

- **实现 40 位算术原语**
  - 加法/减法 (17-42 μs)
  - 位移 (串行实现)
  - XOR/AND/OR — 按位操作
  - 64 位操作 (SHA256 需要) — 多字实现

- **实现 SHA256 消息调度**
  - 多遍方法 (内存限制)
  - 纸带中间存储
  - 常量表在纸带上 (64 字 × 32 位)

- **实现 SHA256 压缩函数**
  - 优化关键路径 (Σ0, Σ1, Ch, Maj)
  - 尽可能使用查找表
  - 流水线消息调度和压缩

- **测试向量验证**
  - NIST SHA256 测试向量
  - 增量哈希
  - 性能测量

**内存布局 (1024 字)**:

| 地址 | 用途 |
|------|------|
| 0x000-0x03F | 引导加载程序和初始化 |
| 0x040-0x07F | SHA256 常量 (页 1) |
| 0x080-0x0BF | SHA256 常量 (页 2) |
| 0x0C0-0x0CF | 哈希状态 (H0-H7, 8 字) |
| 0x0D0-0x0FF | 消息调度缓冲区 (16 字活动) |
| 0x100-0x13F | 临时计算缓冲区 |
| 0x140-0x15F | 网络 I/O 缓冲区 |
| 0x160-0x3FF | 栈和变量 |

**估计性能**:
- 单次 SHA256 哈希：~5-20 秒
- 哈希率：0.05-0.2 H/s
- 纸带吞吐量：~1000 字符/秒

### Phase 3: 网络桥接 (50 RTC)

**目标**: 构建 EDSAC 2 到互联网的网络接口

- **硬件接口**
  - 纸带阅读器传感器 (光学/机械)
  - 纸带穿孔机控制
  - 微控制器 (ESP32/Arduino Due)
  - 电平转换器 (EDSAC 2 逻辑电平 → 3.3V/5V)

- **固件开发**
  - TCP/IP 栈 (lwIP 或类似)
  - HTTPS 客户端 (TLS 1.2/1.3)
  - 纸带编码/解码
  - 错误检测和纠正

- **协议设计**
  - EDSAC 2 → 微控制器：矿池请求 (穿孔纸带)
  - 微控制器 → EDSAC 2：矿池响应 (打印纸带)
  - 错误处理和重试逻辑
  - 离线模式 (缓冲作业)

**纸带协议**:

请求格式 (EDSAC 2 穿孔):
```
[START][CMD][NONCE][DIFFICULTY][CHECKSUM][END]
   1      1      8         1          1       1  = 13 字符
```

响应格式 (EDSAC 2 读取):
```
[START][NONCE][HASH][CHECKSUM][END]
   1      8      32      1         1  = 43 字符
```

### Phase 4: 硬件指纹和证明 (25 RTC)

**目标**: 实现 EDSAC 2 特定硬件指纹

- **磁芯内存特征提取**
  - 磁芯翻转时间签名
  - 内存访问时序变化
  - 温度依赖行为

- **真空管特征**
  - 功耗模式
  - 热特征
  - 预热曲线
  - 管老化指纹

- **微程序特征**
  - 微指令时序签名
  - 控制存储器访问模式

- **证明生成**
  - 硬件签名计算
  - 时间戳
  - 节点验证

- **RustChain API 集成**
  - `POST /api/miners/attest`
  - 包含 EDSAC 2 特定字段
  - 处理证明续期

**指纹数据**:
```json
{
  "hardware_type": "edsac2",
  "year": 1958,
  "technology": "vacuum_tube",
  "memory_type": "magnetic_core",
  "microprogrammed": true,
  "core_flip_timing": [...],
  "tube_power_signature": {...},
  "thermal_profile": {...},
  "microcode_timing": {...}
}
```

### Phase 5: 文档和验证 (25 RTC)

**目标**: 完成文档和公开验证

- **视频录制**
  - EDSAC 2 运行矿工 (可见真空管)
  - 示波器显示磁芯内存活动
  - 纸带 I/O 操作
  - 矿池响应

- **技术文档**
  - 架构设计文档
  - 代码注释 (汇编 + 固件)
  - 用户设置指南
  - 故障排除指南

- **API 验证**
  - 矿工出现在 rustchain.org/api/miners
  - 硬件指纹已验证
  - 奖励正在赚取

- **开源发布**
  - GitHub 仓库
  - MIT/Apache 2.0 许可证
  - 社区贡献指南

---

## 🛠️ 所需硬件

| 组件 | 说明 | 估计成本 |
|------|------|----------|
| EDSAC 2 控制台 | 带磁芯内存 (1024 字) | 博物馆借阅/私人收藏 |
| 纸带阅读器 | 高速光学或机械阅读器 | $500-2,000 |
| 纸带穿孔机 | 用于输出 | $500-2,000 |
| 微控制器 | Arduino Due / Raspberry Pi 网络桥 | $50-100 |
| 定制接口 | 连接微控制器到纸带引脚 | $200-500 |
| 示波器 | 用于磁芯内存监控 (可选) | $300-1,000 |
| 备用真空管 | 数百个管子，备用更换 | $2,000-5,000 |
| 电源 | 5-10 kW，稳定 | $1,000-3,000 |

**总估计成本**: $5,000-15,000 (不包括 EDSAC 2 本身，这是无价的)

---

## 📁 项目结构

```
edsac2-miner/
├── README.md                 # 本项目文档
├── docs/
│   ├── architecture.md       # EDSAC 2 架构参考
│   ├── instruction_set.md    # 指令集详解
│   ├── sha256_implementation.md  # SHA256 实现细节
│   └── network_protocol.md   # 网络协议规范
├── simulator/
│   ├── edsac2_cpu.py         # CPU 模拟器
│   ├── edsac2_memory.py      # 磁芯内存模型
│   ├── edsac2_assembler.py   # 汇编器
│   └── tests/                # 测试套件
├── miner/
│   ├── sha256_core.asm       # SHA256 核心汇编实现
│   ├── miner_main.asm        # 主矿工程序
│   ├── network_io.asm        # 网络 I/O 例程
│   └── hardware_fingerprint.asm  # 硬件指纹
├── firmware/
│   ├── network_bridge/       # 网络桥接固件
│   │   ├── main.cpp
│   │   ├── tcp_ip.cpp
│   │   └── tape_interface.cpp
│   └── tape_reader/          # 纸带阅读器固件
├── hardware/
│   ├── interface_schematic.pdf  # 接口原理图
│   ├── pcb_design/           # PCB 设计文件
│   └── wiring_diagram.pdf    # 接线图
├── videos/                   # 演示视频
└── payouts/                  # 奖励申领证明
    └── wallet_address.txt    # RTC 钱包地址
```

---

## 🚀 快速开始

### 1. 设置模拟器

```bash
cd edsac2-miner/simulator
python3 edsac2_cpu.py --demo
```

### 2. 汇编矿工程序

```bash
python3 edsac2_assembler.py miner/miner_main.asm -o miner_main.tap
```

### 3. 在模拟器上运行

```bash
python3 edsac2_cpu.py --load miner_main.tap --run
```

### 4. 部署到真实硬件

(需要实际 EDSAC 2 硬件)

```bash
# 通过纸带接口加载程序
python3 network_bridge.py --load miner_main.tap --device /dev/ttyUSB0
```

---

## 📊 技术挑战

### 1. 内存限制

- **1024 字 = 5120 字节** (40 位/字)
- SHA256 需要 64 个常量 (256 字节)
- 状态变量：8 个字 (320 字节)
- 消息调度：16 个字 (640 字节)
- **剩余空间非常紧张**，需要多遍算法和纸带中间存储

### 2. 性能优化

- **串行架构**: 位串行操作，不是并行
- **微程序开销**: 每条指令需要多个微周期
- **内存访问**: 破坏性读取需要重写周期

优化策略:
- 使用索引寄存器减少指令大小
- 预加载常用常量到 ROM
- 流水线消息调度和压缩
- 查找表优化关键函数

### 3. 硬件可靠性

- **真空管**: 需要预热，定期更换
- **磁芯内存**: 温度敏感，需要校准
- **纸带**: 机械磨损，需要清洁和维护

---

## 🎓 历史背景

### EDSAC 2 的重大贡献

1. **微程序设计** — Maurice Wilkes 在 EDSAC 2 上首次实现了微程序控制单元，这一概念后来被 IBM System/360 等计算机广泛采用。

2. **椭圆曲线计算** — 1960 年代初，Peter Swinnerton-Dyer 使用 EDSAC 2 计算椭圆曲线上的点数，导致了 Birch 和 Swinnerton-Dyer 猜想，这是七个千禧年大奖难题之一。

3. **板块构造理论** — 1963 年，Frederick Vine 和 Drummond Matthews 使用 EDSAC 2 生成海底磁异常图，为板块构造理论提供了关键证据。

4. **第一个高级语言编译器** — 1961 年，David Hartley 在 EDSAC 2 上开发了 Autocode，一种类似 ALGOL 的高级语言。

### Maurice Wilkes 的愿景

> "EDSAC 2 的设计目标不仅是更快，而是要展示计算机设计的系统方法。微程序设计使我们能够以软件的方式实现复杂的指令集，这是计算机工程的一个转折点。"
> — Maurice Wilkes, 1958

---

## 📝 贡献指南

### 代码贡献

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

### 文档贡献

- 改进技术文档
- 添加教程
- 翻译文档

### 测试贡献

- 添加测试用例
- 验证 SHA256 实现
- 性能基准测试

---

## 📄 许可证

本项目采用 MIT 许可证 — 详见 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

- **Maurice Wilkes** 和剑桥大学数学实验室团队 — EDSAC 2 的原始设计者
- **Computer Conservation Society** — EDSAC 复制品项目
- **The National Museum of Computing** — 保存计算机历史
- **RustChain 社区** — Proof-of-Antiquity 区块链

---

## 📞 联系方式

- GitHub: [@Scottcjn](https://github.com/Scottcjn)
- Discord: [RustChain Discord](https://discord.gg/VqVVS2CW9Q)
- 网站: [rustchain.org](https://rustchain.org)

---

**最后更新**: 2026 年 3 月 14 日

**状态**: 🟡 开发中

** Bounty Issue**: [#379](https://github.com/Scottcjn/rustchain-bounties/issues/379)
