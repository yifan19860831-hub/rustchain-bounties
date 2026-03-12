# RustChain Glossary (RustChain 术语表)

> 本术语表收录 RustChain 生态系统中的核心术语、概念和技术名词，按字母顺序排列。

---

## A

### Antiquity Multiplier (古旧乘数)
根据硬件年代和应用稀缺性计算的奖励倍率。硬件越古老、越稀有，乘数越高。例如：PowerPC G4 为 2.5×，现代 x86_64 为 1.0×。

### Attestation (硬件证明)
矿工提交的网络参与凭证，包含硬件指纹、BIOS 时间戳和熵值数据。每 10 分钟提交一次，用于验证硬件真实性和计算奖励。

### Beacon Protocol (信标协议)
AI 代理之间的通信协议，用于社交协调、加密支付和 P2P 网格发现。支持 Ed25519 签名信封、UDP 广播、Webhook 传输和 RTC 支付。

### Beacon Envelope (信标信封)
Beacon 协议中传输的签名数据包，包含消息类型（如 bounty、hello、pay）、代理身份、时间戳和 Ed25519 签名。

### Beacon Agent Card (信标代理卡片)
JSON 格式的代理公开配置文件，位于 `/.well-known/beacon.json`，包含代理 ID、公钥、能力声明和接受的信标类型。

### Blake2b256
RustChain 用于 Ergo 锚定的哈希算法，生成 32 字节承诺哈希值存储在 Ergo 盒寄存器中。

### BoTTube
基于 AI 的视频平台，119+ 代理在此创建内容。支持 Beacon 协议集成和 RTC 小费支付。

### Bridge (桥接)
连接 RustChain 原生 RTC 与 Solana 上 wRTC 的跨链桥，允许用户在两条链之间转移代币。

---

## C

### clawrtc
RustChain 官方命令行工具，用于安装矿工、管理钱包、查询余额和启动挖矿。支持 pip 和 npm 安装。

### Consensus Attack Red Team (共识攻击红队)
专门测试 RustChain 共识机制安全性的 bounty 类别，奖励高达 200 RTC。

### Current Epoch (当前纪元)
RustChain 网络的时间单位，每个纪元持续 10 分钟，产生 1.5 RTC 奖励分配给活跃矿工。

---

## D

### DEC Alpha
1992 年发布的 64 位 RISC 处理器架构，在 RustChain 中获得 2.7×基础乘数，属于高奖励复古硬件。

### DOS Mining (DOS 挖矿)
在 DOS 系统上运行 RustChain 矿工，可获得纪念徽章（如 QuickBasic Listener），属于实验性支持。

### Dual-Mining (双挖)
同时在 RustChain 和其他区块链（如 Warthog）上挖矿的集成方案。

---

## E

### Ed25519
Beacon 协议和 RustChain 治理投票使用的椭圆曲线签名算法，提供高效的公钥密码学验证。

### Elyan Labs
RustChain 的开发实验室，专注于复古硬件计算和 AI 代理研究。

### Entropy Runtime (熵运行时)
硬件指纹系统的一部分，通过 SHA256 慢解密和物理振荡器漂移生成不可预测的熵值。

### Epoch (纪元)
RustChain 网络的基本时间单位，持续 600 秒（10 分钟）。每个纪元产生固定奖励池，按矿工权重分配。

### Ergo Anchor (Ergo 锚定)
RustChain 定期将区块状态承诺哈希写入 Ergo 区块链的 R4 寄存器，提供时间戳证明和不可篡改性。

### ErgoTool CLI
用于 Ergo 钱包管理和交易签名的命令行工具，RustChain 用它处理灵魂绑定徽章的发行。

---

## F

### First Blood Achievement (首血成就)
新手 bounty 任务，奖励 3 RTC，鼓励首次贡献者完成简单的入门任务。

### FlameBridge
计划中的 EVM 跨链桥，用于 RustChain 与以太坊虚拟机生态系统的互操作性。

### Fingerprint Checks (指纹检查)
6 层硬件验证系统，包括时钟漂移、缓存时序、SIMD 单元识别、热漂移熵、指令路径抖动和反虚拟化检测。

---

## G

### G3 / G4 / G5
Apple PowerPC 处理器系列。G4（1999-2005）获得 2.5×乘数，G5（2003-2006）获得 2.0×乘数，G3（1997-2003）获得 1.8×乘数。

### Governance Proposal (治理提案)
RustChain 链上治理机制，持有超过 10 RTC 的钱包可创建提案，活跃矿工可投票，7 天后根据权重决定通过与否。

---

## H

### Hardware Fingerprint (硬件指纹)
每台矿机的唯一物理特征标识，通过 6 项检测生成，绑定到单一钱包地址，防止 Sybil 攻击。

### Hardware Entropy (硬件熵)
利用 POWER8 mftb 指令读取物理晶振产生的真随机数，注入 LLM 推理过程实现可证明的非确定性。

---

## I

### IBM POWER8
2014 年发布的服务器处理器架构，在 RustChain 中获得 1.5×基础乘数，支持 128 线程和 VSX 向量扩展。

### Install Miner Script (矿工安装脚本)
`install-miner.sh`，跨平台矿工安装器，自动检测操作系统和 CPU 架构，配置虚拟环境和开机自启。

---

## L

### Ledger Integrity Red Team (账本完整性红队)
安全审计 bounty 类别，测试 RustChain 账本系统的抗攻击能力，奖励高达 200 RTC。

### Lore Metadata (背景元数据)
可选附加到区块的历史叙事数据，用于记录矿工故事或硬件背景，增强网络的文化价值。

---

## M

### Miner ID (矿工 ID)
矿工的唯一标识符，通常与钱包地址关联，用于查询余额和统计贡献。

### Moltbook
AI 社交网络平台，集成 Beacon 协议，支持代理之间的社交互动和内容分享。

### Multiplier Decay (乘数衰减)
古旧乘数随时间递减的机制，年衰减率 15%，防止早期矿工获得永久性优势。

---

## N

### NFT Badges (NFT 徽章)
基于 Ergo 的灵魂绑定代币，奖励特殊成就或里程碑，如"Bondi G3 Flamekeeper"、"DOS WiFi Alchemist"。

### Non-Bijective Permutation Collapse (非双射排列坍缩)
利用 AltiVec vec_perm 指令在 1 个周期内完成多对一映射，比 x86/ARM 快 27-96 倍，用于 LLM 注意力优化。

### NUMA Weight Banking (NUMA 权重银行)
在非统一内存访问架构上优化 LLM 推理的技术，实现 8.81 倍加速。

---

## P

### PSE (Physical Silicon Entropy, 物理硅熵)
通过硬件指令（如 POWER8 mftb）获取的真随机熵源，用于 LLM 输出扰动和行为多样性。

### Proof-of-Antiquity (PoA, 古旧证明)
RustChain 的核心共识机制，根据硬件年代和稀缺性分配奖励，而非算力或持币量。口号："1 CPU = 1 Vote"。

### Proof-of-Work (PoW, 工作量证明)
传统区块链共识机制，奖励最快硬件。RustChain 反其道而行，奖励最老硬件。

### Proposal Lifecycle (提案生命周期)
治理提案状态流转：Draft（草案）→ Active（活跃，7 天投票期）→ Passed/Failed（通过/失败）。

---

## R

### RAM Coffers (RAM 金库)
利用 NUMA 架构的分布式权重存储技术，优化 LLM 推理速度，在 POWER8 上达到 147 tokens/s。

### Raydium DEX
Solana 上的去中心化交易所，wRTC 在此提供流动性池，支持 RTC/SOL 交易对。

### RIP-200
RustChain 改进提案 #200，定义任期增长乘数机制：所有矿工每年增益 5%，10 年封顶 50%。

### RTC (RustChain Token)
RustChain 原生加密货币，参考价格 $0.10 USD。总量 830 万枚，70% 用于挖矿奖励。

### Rust
此处指 30 年老硅上的氧化铁（铁锈），而非 Rust 编程语言。名称来源于一台端口氧化但仍能运行 DOS 并挖矿的 486 笔记本。

### RustChain Node (RustChain 节点)
网络基础设施，负责验证交易、存储账本和处理矿工证明。主节点位于 50.28.86.131。

---

## S

### SheepShaver
PowerPC 模拟器，RustChain 的指纹系统可检测并大幅降低其奖励（10 亿分之一），防止虚拟机农场攻击。

### SIMD Unit Identity (SIMD 单元识别)
硬件指纹检查之一，识别 AltiVec、SSE、NEON 等向量处理单元的特征延迟模式。

### Slot Height (槽高度)
RustChain 区块高度的另一种表述，用于 Ergo 锚定时的时间戳对齐。

### Sophia's House
RustChain 社区口号："We educate, we don't reject"（我们教育，不拒绝），体现包容性贡献文化。

### Soulbound Badge (灵魂绑定徽章)
不可转移的 NFT 成就徽章，绑定到矿工钱包，记录特殊贡献或里程碑。

### SPARCstation
Sun Microsystems 1987 年发布的工作站，使用 SPARC v7 架构，在 RustChain 中获得 2.9×基础乘数。

---

## T

### Tenure-Grown Multiplier (任期增长乘数)
根据挖矿时长增加的奖励乘数，公式：`tenure_formula = base * min(1.0 + 0.05 * years_mining, 1.5)`。

### Tip Bot (小费机器人)
BoTTube 平台上的 RTC 小费功能，允许用户通过 Beacon 协议向内容创作者发送小额支付。

---

## V

### vec_perm
PowerPC AltiVec 向量指令，执行非双射排列坍缩，1 周期完成 x86 需 27-96 周期的操作。

### Virtual Machine Detection (虚拟机检测)
通过 ROM 指纹聚类、行为分析和硬件指纹异常识别 QEMU、VMware、VirtualBox 等虚拟化环境。

### Vote Weight (投票权重)
治理投票中的权重计算：`1 RTC = 1 基础票 × 矿工古旧乘数`，持有更多 RTC 和使用复古硬件的矿工投票权更大。

### VM Penalty (虚拟机惩罚)
虚拟机矿工获得的奖励仅为正常硬件的 10 亿分之一（0.000000001×），防止大规模虚拟化攻击。

---

## W

### wRTC (Wrapped RTC)
RTC 在 Solana 上的包装代币版本，遵循 SPL 代币标准，合约地址：`12TAdKXxcGf6oCv4rqDz2NkgxjyHq6HQKoxKZYGf5i4X`。

### Wallet (钱包)
RustChain 矿工的身份和奖励接收地址，通过 `clawrtc wallet` 命令管理。首次使用者可通过 bounty 评论获得帮助设置。

### x402 Protocol (x402 协议)
基于 HTTP 402 Payment Required 的机器间支付协议，RustChain 代理可使用此协议进行自动微支付。

---

## 快速参考表

### 硬件乘数速查

| 硬件架构 | 年代 | 基础乘数 | 1 年后 | 5 年后 |
|---------|------|---------|--------|--------|
| Motorola 68000 | 1979 | 3.0× | 3.15× | 3.75× |
| Intel 386/486 | 1985-1989 | 3.0× | 3.15× | 3.75× |
| SPARCstation | 1987 | 2.9× | 3.05× | 3.63× |
| DEC Alpha | 1992 | 2.7× | 2.84× | 3.38× |
| PowerPC G4 | 1999-2005 | 2.5× | 2.63× | 3.13× |
| PowerPC G5 | 2003-2006 | 2.0× | 2.1× | 2.5× |
| IBM POWER8 | 2014 | 1.5× | 1.58× | 1.88× |
| Apple Silicon | 2020+ | 1.2× | 1.26× | 1.5× |
| Modern x86_64 | 当前 | 0.8× | 0.84× | 1.0× |
| Generic ARM | 当前 | 0.0005× | 0.0005× | 0.0006× |

### Bounty 奖励等级

| 等级 | 奖励范围 | 示例 |
|-----|---------|------|
| Micro | 1-10 RTC | 拼写错误修复、简单文档 |
| Standard | 20-50 RTC | 功能开发、重构 |
| Major | 75-100 RTC | 安全修复、共识优化 |
| Critical | 100-150 RTC | 漏洞补丁、协议升级 |
| Red Team | 200 RTC | 共识攻击、账本完整性审计 |

---

## 贡献

本术语表由社区维护。如发现遗漏或错误，请在 rustchain-bounties 仓库提交 Issue 或 PR。

**最后更新**: 2026-03-12  
**版本**: 1.0.0
