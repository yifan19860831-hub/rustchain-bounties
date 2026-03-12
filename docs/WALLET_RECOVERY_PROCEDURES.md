# RustChain 钱包恢复流程

> **文档版本：** 1.0  
> **创建日期：** 2026-03-12  
> **适用网络：** RustChain Mainnet  
> **奖励：** 3 RTC

---

## ⚠️ 重要安全提示

**在阅读恢复流程之前，请务必了解：**

1. **私钥即资产** - 谁拥有私钥，谁就完全控制钱包中的所有 RTC
2. **永不分享私钥** - RustChain 团队永远不会询问你的私钥或助记词
3. **备份优先** - 预防胜于治疗，请定期备份钱包数据
4. **验证环境** - 在恢复钱包时，确保使用官方软件和节点

---

## 📋 目录

1. [钱包类型识别](#1-钱包类型识别)
2. [场景一：私钥丢失](#2-场景一私钥丢失)
3. [场景二：设备损坏](#3-场景二设备损坏)
4. [场景三：助记词恢复](#4-场景三助记词恢复)
5. [场景四：矿工钱包迁移](#5-场景四矿工钱包迁移)
6. [场景五：跨链钱包恢复](#6-场景五跨链钱包恢复)
7. [预防措施与最佳实践](#7-预防措施与最佳实践)
8. [故障排查](#8-故障排查)
9. [获取帮助](#9-获取帮助)

---

## 1. 钱包类型识别

RustChain 支持多种钱包形式，恢复方法因类型而异：

### 1.1 Miner ID 钱包（默认）

- **格式：** 自定义字符串（如 `my-miner-wallet`）或 SHA1 哈希 + `RTC` 后缀
- **特点：** 与矿工绑定，用于接收挖矿奖励
- **恢复方式：** 重新安装矿工并使用相同 Miner ID

### 1.2 Ed25519 密钥对钱包

- **格式：** 64 字符十六进制公钥 + 私钥
- **特点：** 支持签名转账，完全去中心化
- **恢复方式：** 使用私钥重新生成密钥对

### 1.3 Coinbase Base 钱包（x402）

- **格式：** 0x 开头的以太坊地址（如 `0x5683C10596AaA09AD7F4eF13CAB94b9b74A669c6`）
- **特点：** 用于 AI Agent 支付，支持 wRTC on Base
- **恢复方式：** 使用 Coinbase Wallet 或兼容钱包导入

### 1.4 Solana wRTC 钱包

- **格式：** Base58 编码的 Solana 地址
- **特点：** 用于 Solana 生态的 wrapped RTC
- **恢复方式：** 使用 Phantom 等 Solana 钱包恢复

---

## 2. 场景一：私钥丢失

### 2.1 情况评估

**如果你有：**
- ✅ 助记词/种子短语 → 跳转到 [场景三](#4-场景三助记词恢复)
- ✅ 钱包备份文件 → 跳转到 [场景二](#3-场景二设备损坏)
- ✅ Miner ID 但没有私钥 → 继续本节
- ❌ 什么都没有 → 很遗憾，资产无法恢复

### 2.2 Miner ID 钱包恢复（无私钥）

Miner ID 钱包的特殊性：**只要知道 Miner ID 字符串，就可以恢复访问**。

**步骤：**

```bash
# 1. 重新安装 RustChain 矿工
curl -sSL https://raw.githubusercontent.com/Scottcjn/Rustchain/main/install-miner.sh | bash -s -- --wallet YOUR_WALLET_NAME

# 2. 验证钱包余额
curl -sk "https://rustchain.org/wallet/balance?miner_id=YOUR_WALLET_NAME" | jq .

# 3. 检查矿工状态
curl -sk https://rustchain.org/api/miners | jq .

# 4. 启动矿工服务
# Linux (systemd)
systemctl --user start rustchain-miner

# macOS (launchd)
launchctl start com.rustchain.miner
```

**预期输出：**
```json
{
  "amount_i64": 118357193,
  "amount_rtc": 118.357193,
  "miner_id": "YOUR_WALLET_NAME"
}
```

### 2.3 Ed25519 私钥丢失

**残酷的现实：** 如果丢失了 Ed25519 私钥且没有备份，**资产永久丢失**。

**尝试以下方法：**

1. **搜索备份位置：**
   - `~/.rustchain/` 目录
   - 密码管理器（1Password、Bitwarden 等）
   - 加密的 USB 驱动器
   - 纸质备份（检查重要文件、保险箱）
   - 云存储（加密的备份文件）

2. **检查历史命令：**
   ```bash
   # 查看是否有创建钱包的命令历史
   history | grep -i wallet
   history | grep -i clawrtc
   ```

3. **查找配置文件：**
   ```bash
   # Linux/macOS
   find ~ -name "*rustchain*" -o -name "*rtc*" 2>/dev/null
   
   # 检查常见配置目录
   ls -la ~/.rustchain/
   ls -la ~/.local/share/rustchain/
   ls -la ~/.config/rustchain/
   ```

---

## 3. 场景二：设备损坏

### 3.1 硬件故障但数据可访问

**如果硬盘仍可读取：**

```bash
# 1. 挂载旧硬盘或连接外部存储
# 2. 备份钱包数据目录
cp -r /path/to/old/drive/.rustchain ~/backup-rustchain

# 3. 关键文件位置
~/.rustchain/wallet.dat          # 钱包数据（如果有）
~/.rustchain/miner_id            # Miner ID 配置
~/.rustchain/keys/               # Ed25519 密钥对
~/.rustchain/config.json         # 配置文件
```

### 3.2 完全硬件损坏

**前提：** 你有 Miner ID 字符串或助记词备份

**恢复步骤：**

```bash
# 1. 在新设备上安装 RustChain
curl -sSL https://raw.githubusercontent.com/Scottcjn/Rustchain/main/install-miner.sh | bash

# 2. 使用相同的 Miner ID 恢复
curl -sSL https://raw.githubusercontent.com/Scottcjn/Rustchain/main/install-miner.sh | bash -s -- --wallet YOUR_WALLET_NAME

# 3. 验证余额
curl -sk "https://rustchain.org/wallet/balance?miner_id=YOUR_WALLET_NAME"

# 4. 重新配置矿工服务
# Linux
systemctl --user enable rustchain-miner
systemctl --user start rustchain-miner

# macOS
launchctl load -w ~/Library/LaunchAgents/com.rustchain.miner.plist
```

### 3.3 从时间机器（Time Machine）恢复

**macOS 用户：**

```bash
# 1. 从 Time Machine 恢复 .rustchain 目录
# 2. 或者手动复制
cp -r /Volumes/TimeMachine/Backups.backupdb/[Your-Mac]/[Date]/Users/[Your-Name]/.rustchain ~/.rustchain

# 3. 验证恢复
clawrtc wallet show  # 如果支持此命令
curl -sk "https://rustchain.org/wallet/balance?miner_id=YOUR_WALLET_NAME"
```

---

## 4. 场景三：助记词恢复

### 4.1 标准 BIP39 助记词

如果你使用支持 BIP39 的钱包（如 Ledger、Trezor、MetaMask）：

**步骤：**

1. **选择兼容钱包：**
   - RustChain CLI（如果支持）
   - MetaMask（用于 Base 链上的 wRTC）
   - Phantom（用于 Solana 上的 wRTC）

2. **导入助记词：**
   ```
   ⚠️ 警告：在离线环境中执行此操作！
   
   1. 打开钱包应用
   2. 选择"导入现有钱包"
   3. 输入 12/24 词助记词
   4. 设置新密码
   5. 验证导入成功
   ```

3. **添加 RustChain 网络：**
   - **Base Mainnet:**
     - Chain ID: 8453
     - RPC: https://mainnet.base.org
     - wRTC: `0x5683C10596AaA09AD7F4eF13CAB94b9b74A669c6`
   
   - **Solana Mainnet:**
     - RPC: https://api.mainnet-beta.solana.com
     - wRTC Mint: `12TAdKXxcGf6oCv4rqDz2NkgxjyHq6HQKoxKZYGf5i4X`

### 4.2 RustChain 原生助记词

如果使用 `clawrtc` CLI 创建的钱包：

```bash
# 1. 安装 clawrtc
pip install clawrtc

# 2. 从助记词恢复钱包
clawrtc wallet recover --mnemonic "your twelve word mnemonic phrase here"

# 3. 验证恢复
clawrtc wallet balance

# 4. 重新链接到矿工
clawrtc mine --wallet YOUR_WALLET_NAME
```

---

## 5. 场景四：矿工钱包迁移

### 5.1 为什么需要迁移？

- 更换挖矿设备
- 合并多个钱包
- 安全升级（从简单 Miner ID 到 Ed25519）

### 5.2 迁移前准备

```bash
# 1. 记录旧钱包信息
curl -sk "https://rustchain.org/wallet/balance?miner_id=OLD_WALLET" | jq .
curl -sk "https://rustchain.org/wallet/history?miner_id=OLD_WALLET&limit=50" | jq .

# 2. 截图保存交易历史（重要！）

# 3. 确认没有待处理的奖励
# 等待当前 epoch 结束（最多 10 分钟）
curl -sk https://rustchain.org/epoch | jq .
```

### 5.3 执行迁移

```bash
# 1. 停止旧矿工
# Linux
systemctl --user stop rustchain-miner

# macOS
launchctl stop com.rustchain.miner

# 2. 备份旧配置
mv ~/.rustchain ~/.rustchain.backup.$(date +%Y%m%d)

# 3. 安装新矿工（使用新钱包 ID）
curl -sSL https://raw.githubusercontent.com/Scottcjn/Rustchain/main/install-miner.sh | bash -s -- --wallet NEW_WALLET_NAME

# 4. 验证新钱包
curl -sk "https://rustchain.org/wallet/balance?miner_id=NEW_WALLET_NAME"

# 5. 启动新矿工
# Linux
systemctl --user start rustchain-miner

# macOS
launchctl start com.rustchain.miner
```

### 5.4 迁移后验证

```bash
# 1. 检查新矿工是否在列表中
curl -sk https://rustchain.org/api/miners | jq ".[] | select(.miner == \"NEW_WALLET_NAME\")"

# 2. 监控第一个 epoch 奖励
watch -n 60 'curl -sk "https://rustchain.org/wallet/balance?miner_id=NEW_WALLET_NAME" | jq .amount_rtc'

# 3. 确认旧钱包不再接收奖励
# （等待 1-2 个 epoch 后检查）
```

---

## 6. 场景五：跨链钱包恢复

### 6.1 Solana wRTC 恢复

**前提：** 你有 Solana 钱包的私钥或助记词

**使用 Phantom 钱包：**

1. 安装 Phantom 浏览器扩展
2. 选择"导入现有钱包"
3. 输入助记词或私钥
4. 添加 wRTC 代币：
   - 打开 Phantom
   - 点击"+"添加代币
   - 输入 Mint 地址：`12TAdKXxcGf6oCv4rqDz2NkgxjyHq6HQKoxKZYGf5i4X`
   - 确认添加

**使用 CLI：**

```bash
# 1. 安装 Solana CLI
sh -c "$(curl -sSfL https://release.anza.xyz/stable/install)"

# 2. 恢复密钥对
solana-keygen recover

# 3. 添加 wRTC 代币
spl-token accounts

# 4. 检查余额
spl-token balance 12TAdKXxcGf6oCv4rqDz2NkgxjyHq6HQKoxKZYGf5i4X
```

### 6.2 Base wRTC 恢复

**前提：** 你有以太坊兼容钱包的私钥或助记词

**使用 MetaMask：**

1. 安装 MetaMask 浏览器扩展
2. 导入钱包（助记词或私钥）
3. 添加 Base 网络：
   - 网络名称：Base Mainnet
   - RPC URL: `https://mainnet.base.org`
   - Chain ID: `8453`
   - 货币符号：ETH
   - 区块浏览器：`https://basescan.org`
4. 添加 wRTC 代币：
   - 合约地址：`0x5683C10596AaA09AD7F4eF13CAB94b9b74A669c6`
   - 名称：wrapped RTC
   - 符号：wRTC
   - 小数：6

**使用 Coinbase Wallet：**

```bash
# 如果使用 Coinbase SDK
clawrtc wallet coinbase recover --private-key YOUR_PRIVATE_KEY

# 检查余额
clawrtc wallet coinbase balance

# 查看 swap 信息
clawrtc wallet coinbase swap-info
```

### 6.3 跨链桥接恢复

如果你使用 BoTTube Bridge：

```bash
# 1. 访问桥接界面
# https://bottube.ai/bridge

# 2. 连接恢复后的钱包

# 3. 检查桥接历史
# 桥接交易记录在链上，可以随时查询

# 4. 如有卡住的桥接交易
curl -sk https://bottube.ai/bridge/status?tx=YOUR_TRANSACTION_HASH
```

---

## 7. 预防措施与最佳实践

### 7.1 备份策略

**3-2-1 规则：**
- **3 份** 备份副本
- **2 种** 不同介质（硬盘 + 纸质）
- **1 份** 异地备份

**推荐备份内容：**

```bash
# 创建加密备份
cd ~/.rustchain
tar -czf rustchain-backup-$(date +%Y%m%d).tar.gz .
gpg -c rustchain-backup-$(date +%Y%m%d).tar.gz

# 备份到多个位置
cp rustchain-backup-*.tar.gz.gpg /media/usb/
cp rustchain-backup-*.tar.gz.gpg ~/cloud-storage/
# 打印纸质备份（二维码形式）
```

### 7.2 安全存储

**推荐：**
- ✅ 硬件钱包（Ledger、Trezor）
- ✅ 加密的 USB 驱动器
- ✅ 保险箱中的纸质备份
- ✅ 密码管理器（用于加密文件）

**避免：**
- ❌ 明文存储在电脑硬盘
- ❌ 截图保存在手机相册
- ❌ 通过微信/QQ/邮件发送私钥
- ❌ 存储在联网的云盘（未加密）

### 7.3 定期验证

```bash
# 每月检查一次
# 1. 验证备份可恢复性（在测试环境）
# 2. 确认钱包余额
curl -sk "https://rustchain.org/wallet/balance?miner_id=YOUR_WALLET" | jq .

# 3. 检查矿工状态
curl -sk https://rustchain.org/api/miners | jq ".[] | select(.miner == \"YOUR_WALLET\")"

# 4. 记录检查结果到日志
echo "$(date): Balance check OK" >> ~/rustchain-health.log
```

### 7.4 多重签名（未来支持）

当 RustChain 支持多签钱包时：

- 设置 2-of-3 或 3-of-5 多签
- 分散保管签名密钥
- 单点故障不会导致资产丢失

---

## 8. 故障排查

### 8.1 常见问题

**问题 1：恢复后余额显示为 0**

```bash
# 可能原因：
# 1. Miner ID 拼写错误
# 2. 使用了不同的钱包
# 3. 奖励尚未结算

# 解决方案：
# 1. 仔细检查 Miner ID
curl -sk "https://rustchain.org/wallet/balance?miner_id=EXACT_WALLET_NAME"

# 2. 检查交易历史
curl -sk "https://rustchain.org/wallet/history?miner_id=YOUR_WALLET&limit=100"

# 3. 等待 epoch 结算（最多 10 分钟）
curl -sk https://rustchain.org/epoch
```

**问题 2：矿工无法连接到网络**

```bash
# 检查节点健康
curl -sk https://rustchain.org/health

# 检查防火墙
# Linux
sudo ufw status
sudo iptables -L -n

# macOS
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate

# 测试连接
curl -sk https://rustchain.org/health -v
```

**问题 3：私钥格式错误**

```bash
# Ed25519 私钥应为 64 字符十六进制
# 示例：a1b2c3d4e5f6...（64 字符）

# 验证格式
echo "YOUR_PRIVATE_KEY" | grep -E '^[a-f0-9]{64}$'

# 如果包含 0x 前缀，去掉它
echo "YOUR_PRIVATE_KEY" | sed 's/^0x//'
```

### 8.2 恢复失败检查清单

- [ ] 确认使用的正确的网络（Mainnet vs Testnet）
- [ ] 验证 Miner ID/地址拼写完全正确
- [ ] 检查 RustChain 节点是否在线
- [ ] 确认钱包类型匹配恢复方法
- [ ] 尝试不同的恢复工具/客户端
- [ ] 查看官方文档是否有更新
- [ ] 在 Discord 社区寻求帮助

---

## 9. 获取帮助

### 9.1 官方资源

- **GitHub:** https://github.com/Scottcjn/Rustchain
- **网站:** https://rustchain.org
- **区块浏览器:** https://rustchain.org/explorer
- **Discord:** https://discord.gg/VqVVS2CW9Q
- **文档:** https://github.com/Scottcjn/Rustchain/tree/main/docs

### 9.2 报告问题时提供

1. **钱包类型：** Miner ID / Ed25519 / Base / Solana
2. **问题描述：** 详细说明了发生了什么
3. **错误信息：** 完整的错误输出
4. **时间戳：** 问题发生的 UTC 时间
5. **交易哈希：** 相关的 tx hash（如有）
6. **Miner ID：** 钱包地址（**不要提供私钥！**）

### 9.3 社区支持

- **GitHub Issues:** 提交技术问题
- **Discord:** 实时社区帮助
- **Dev.to:** https://dev.to/scottcjn（教程和公告）

---

## 🔐 安全提醒

**最后再次强调：**

1. **RustChain 团队永远不会询问你的私钥**
2. **不要在不明网站输入助记词**
3. **验证所有 URL 和合约地址**
4. **小额测试后再进行大额操作**
5. **保持软件更新到最新版本**

---

## 📝 修订历史

| 版本 | 日期 | 修改内容 |
|------|------|----------|
| 1.0 | 2026-03-12 | 初始版本，涵盖 5 大恢复场景 |

---

## 📄 许可证

本文档遵循 RustChain 项目的 MIT 许可证。

**贡献者：** RustChain Community  
**审核者：** Security Team  
**状态：** ✅ 生产就绪
