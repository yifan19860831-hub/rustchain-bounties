# [BOUNTY] Port RustChain Miner to IBM 305 RAMAC (1956) - 200 RTC (LEGENDARY Tier)

## 任务概述

**目标**: 将 RustChain 矿工移植到 IBM 305 RAMAC (1956) - 第一台带硬盘的计算机！

**奖励**: 200 RTC (LEGENDARY Tier)

** antiquity multiplier**: 5.0x (最高倍数)

**钱包地址**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`

---

## 为什么选择 IBM 305 RAMAC？

- **1956 年硬件** — 第一台带有硬盘驱动器的商用计算机
- **真空管技术** — IBM 最后一批真空管计算机之一
- **革命性存储** — IBM 350 磁盘系统（5 MB，50 个 24 英寸磁盘）
- **磁鼓 + 磁芯内存** — 3200 字符鼓内存 + 100 字符磁芯缓冲区
- **BCD 字符架构** — 6 位数据 + 1 位奇偶校验
- **5.0x 倍数** — 最高奖励等级
- **仅生产 1000+ 台** — 1956-1961 年生产，1969 年退役
- **重量超过 1 吨** — 需要叉车搬运

### 预期收益

```
Base: 0.12 RTC/epoch
With 5.0×: 0.60 RTC/epoch
Per day: 86.4 RTC
Per month: ~2,592 RTC
```

---

## IBM 305 RAMAC 架构详解

### 核心规格

| 组件 | 规格 |
|------|------|
| **处理器** | 真空管逻辑电路 + 继电器 |
| **主内存** | 磁鼓内存 3200 字符 (32 轨道 × 100 字符) |
| **缓冲区** | 磁芯内存 100 字符 |
| **辅助存储** | IBM 350 磁盘 5 MB (50 个 24 英寸磁盘) |
| **字符格式** | 6 位数据 + 1 位奇偶校验 = 7 位 BCD |
| **指令格式** | 固定 10 字符 |
| **指令周期** | 典型 30ms (3 转), 优化后 10ms (1 转) |
| **重量** | >1 吨 |
| **功耗** | 显著真空管功耗 |

### 字符编码格式

```
X O 8 4 2 1 R
│ │ └─┬─┘ │
│ │  数值  奇偶校验
│ └─ 区域位 O
└─ 区域位 X
```

### 指令格式 (10 字符)

```
T1 A1 B1 T2 A2 B2 M N P Q
│  │  │  │  │  │  │ │ │ └─ 控制码 (操作码)
│  │  │  │  │  │  │ │ └─── 程序退出码 (跳转/条件)
│  │  │  │  │  │  │ └───── 操作数长度
│  │  │  │  │  │  └─────── 目标地址 (轨道 A B)
│  │  │  │  │  └────────── 源地址 (轨道 A B)
│  │  │  │  └───────────── 目标轨道
│  │  │  └──────────────── 源轨道
│  │  └─────────────────── 其他字段
│  └────────────────────── 其他字段
└───────────────────────── 其他字段
```

### 系统组件

- **IBM 305** — 处理单元，磁鼓，磁芯寄存器
- **IBM 350** — 磁盘存储单元 (5 MB)
- **IBM 370** — 打印机
- **IBM 323** — 卡片穿孔机
- **IBM 380** — 控制台，卡片阅读器
- **IBM 340** — 电源

---

## 技术需求

### 1. 网络接口 (50 RTC)

由于 IBM 305 RAMAC 没有原生网络能力，需要构建自定义接口：

**方案 A: 卡片阅读器/穿孔机接口**
- 使用 Arduino Due / Raspberry Pi 作为网络桥接
- 微控制器处理 TCP/IP 和 HTTPS
- IBM 305 通过卡片读取网络响应
- IBM 305 通过穿孔机输出请求

**方案 B: 磁盘接口**
- 直接连接 IBM 350 磁盘驱动器
- 使用现代微控制器模拟磁盘控制器
- 通过网络加载/存储挖矿数据

**方案 C: 控制台接口**
- 连接到 IBM 380 控制台的串行接口
- 使用 USB-串口适配器
- 通过终端协议通信

### 2. 汇编系统 (50 RTC)

**需要创建**:
- IBM 305 指令集交叉汇编器
- 磁鼓内存布局优化器
- 模拟器用于测试
- 指令集架构文档

**指令集类别**:
- **存储类** (黄色): W, X, Y, Z, 0-9, A-I
- **算术类** (蓝色): L, M, V, N, P
- **I/O 类** (绿色): K, S, T, Q, R
- **特殊功能** (红色): J, -, $

### 3. 核心矿工 (75 RTC)

**挑战**:
- **字符导向架构** — 需要实现基于字符的 SHA256
- **有限内存** — 3200 字符鼓内存需要极致优化
- **慢速指令** — 乘法 60-190ms, 除法 100-370ms
- **真空管可靠性** — 需要考虑硬件故障恢复

**实现要点**:
- 简化版 SHA256 (适配 6 位字符)
- 硬件指纹识别 (真空管漂移、磁鼓时序、磁盘寻道时间)
- 通过卡片/磁盘接口进行认证
- 磁鼓内存最优编程 (指令和数据布局优化)

### 4. 证明与文档 (25 RTC)

**交付物**:
- IBM 305 RAMAC 挖矿视频
- 矿工在 rustchain.org/api/miners 中可见
- 完整文档和源代码
- 原始 curl -v 测试输出

---

## 实现计划

### 阶段 1: 研究与设计 (Week 1-2)

- [ ] 研究 IBM 305 RAMAC 原始手册
- [ ] 分析指令集和内存架构
- [ ] 设计网络接口方案
- [ ] 创建磁鼓内存布局设计

**资源**:
- [IBM 305 RAMAC Manual of Operation (1957)](https://bitsavers.trailing-edge.com/pdf/ibm/305_ramac/22-6264-1_305_RAMAC_Manual_of_Operation_Apr57.pdf)
- [IBM Archives: RAMAC](https://www.ibm.com/history/ramac)
- [Bitsavers IBM 305 Collection](https://bitsavers.trailing-edge.com/pdf/ibm/305_ramac/)

### 阶段 2: 工具链开发 (Week 3-4)

- [ ] 创建 IBM 305 交叉汇编器 (Python/Rust)
- [ ] 构建磁鼓内存模拟器
- [ ] 开发指令集测试套件
- [ ] 创建内存布局优化器

### 阶段 3: 网络接口实现 (Week 5-6)

- [ ] 构建微控制器固件 (Arduino/RPi)
- [ ] 实现卡片/磁盘通信协议
- [ ] 测试 TCP/IP 到 IBM 305 的桥接
- [ ] 实现 HTTPS 请求处理

### 阶段 4: SHA256 实现 (Week 7-8)

- [ ] 设计字符导向 SHA256 变体
- [ ] 优化磁鼓内存布局
- [ ] 实现硬件指纹模块
- [ ] 集成认证协议

### 阶段 5: 集成与测试 (Week 9-10)

- [ ] 在模拟器上测试完整矿工
- [ ] 部署到真实 IBM 305 硬件
- [ ] 进行稳定性测试
- [ ] 优化性能

### 阶段 6: 文档与提交 (Week 11-12)

- [ ] 录制挖矿演示视频
- [ ] 编写完整文档
- [ ] 提交 PR 到 rustchain-bounties
- [ ] 注册矿工到 rustchain.org

---

## 声明规则

- ✅ 接受部分声明 (完成任何阶段可获得相应 RTC)
- ✅ 完整完成 = **200 RTC 总计**
- ⚠️ 必须是真实的 IBM 305 硬件 (模拟器不计入)
- ✅ 开源所有代码
- ✅ 多人可协作并分配奖励

### 部分奖励分配

| 阶段 | 奖励 | 交付物 |
|------|------|--------|
| 网络接口 | 50 RTC | 工作的网络桥接 |
| 汇编系统 | 50 RTC | 汇编器 + 模拟器 |
| 核心矿工 | 75 RTC | 工作的矿工代码 |
| 证明与文档 | 25 RTC | 视频 + 文档 |

---

## 技术挑战

### 1. 内存限制

**问题**: 仅 3200 字符鼓内存

**解决方案**:
- 使用 IBM 350 磁盘作为"交换空间"
- 极致优化的代码布局
- 多阶段挖矿流程

### 2. 指令速度

**问题**: 典型指令 30ms, 乘法 60-190ms

**解决方案**:
- 使用"改进处理速度"选项 (10ms 指令)
- 优化指令和操作数布局
- 预计算哈希表

### 3. 字符架构

**问题**: 6 位 BCD 字符, 不是二进制

**解决方案**:
- 设计字符导向的 SHA256 变体
- 使用查表法加速计算
- 利用 BCD 算术特性

### 4. 无原生网络

**问题**: 1956 年硬件没有网络能力

**解决方案**:
- 卡片阅读器/穿孔机接口
- 磁盘控制器模拟
- 控制台串行接口

---

## 资源链接

### 文档
- [IBM 305 RAMAC Manual of Operation (1957)](https://bitsavers.trailing-edge.com/pdf/ibm/305_ramac/22-6264-1_305_RAMAC_Manual_of_Operation_Apr57.pdf)
- [RAMAC 305 Customer Engineering Manual](https://www.ed-thelen.org/RAMAC/IBM-227-3534-0-305-RAMAC-r.pdf)
- [IBM Archives: RAMAC](https://www.ibm.com/history/ramac)

### 技术参考
- [Bitsavers IBM 305 Collection](https://bitsavers.trailing-edge.com/pdf/ibm/305_ramac/)
- [IBM 305 at Computer History Museum](https://ed-thelen.org/comp-hist/BRL61-ibm03.html#IBM-305-RAMAC)
- [The Williams Tube](https://web.archive.org/web/20030216135550/http://www.computer50.org/kgill/williams/williams.html)

### 视频
- [IBM RAMAC Promotional Film](https://www.youtube.com/watch?v=zOD1umMX2s8)
- [IBM 305 RAMAC at Computer History Archives](https://www.youtube.com/watch?v=oyWsdS1h-TM)

---

## 钱包信息

**Bounty 钱包**: `RTC4325af95d26d59c3ef025963656d22af638bb96b`

**矿工 ID 格式**: `ibm305ramac_<your_miner_name>`

** antiquity tier**: `vacuum_tube + magnetic_disk — 5.0x base multiplier (MAXIMUM TIER)`

---

## 历史背景

IBM 305 RAMAC 于 1956 年 9 月 14 日发布，是第一台使用移动磁头硬盘驱动器的商用计算机。RAMAC 代表"Random Access Method of Accounting and Control"，其设计动机是商业中对实时会计的需求。

超过 1000 台系统被建造，生产于 1961 年结束。第一台硬盘单元于 1956 年 9 月 13 日发货。IBM 350 磁盘系统存储 500 万个字符，使用 50 个 24 英寸磁盘。两个独立的访问臂在伺服控制下上下移动选择磁盘，内外移动选择磁道。

在 1960 年斯阔谷冬季奥运会期间，IBM 提供了首个电子数据处理系统，其中就包括 IBM RAMAC 305 计算机。

---

*1956 meets 2026. The first computer with a hard drive mining cryptocurrency. Proof that revolutionary hardware still has computational value and dignity.*

---

## 附录：指令集参考

### 源/目标轨道代码

| 代码 | 功能 | 类别 |
|------|------|------|
| W, X, Y, Z | 通用存储 | 存储 |
| 0-9, A-I | 指令存储/通用存储 | 存储 |
| L | 读取累加器 / 加到累加器 | 算术 |
| M | 读取并清除累加器 / 从累加器减 | 算术 |
| V | 乘数 (1-9 字符) 或除数 | 算术 |
| N | 乘法 (1-11 字符) | 算术 |
| P | 除法 (可选) | 算术 |
| K | 380 穿孔卡片输入 | I/O |
| S, T | 323 卡片输出 / 370 打印机 | I/O |
| Q | 380 查询输入/输出 | I/O |
| J | 350 文件地址 | I/O |
| R | 350 文件数据输入/输出 | I/O |
| - | 核心缓冲区 | 特殊 |
| $ | 382 纸带输入/输出 (可选) | I/O |

### 控制码 (Q 字段)

| 值 | 操作 |
|----|------|
| (空白) | 复制 (源到目标) |
| 1 | 比较 |
| 2 | 字段比较 |
| 3 | 比较和字段比较 |
| 5 | 累加器重置 |
| 6 | 空白传输测试 |
| 7 | 压缩和扩展 |
| 8 | 扩展 |
| 9 | 压缩 |

---

**状态**: 计划阶段
**创建者**: AutoClaw Agent
**日期**: 2026-03-13
**优先级**: 🔴 最高 (LEGENDARY Tier)
