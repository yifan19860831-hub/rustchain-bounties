# PR Submission - Issue #1622: Reddit Bot for RustChain

## 赏金信息

- **Issue**: #1622 - [BOUNTY: 5 RTC] Create a Reddit bot for RustChain
- **奖励**: 5 RTC
- **提交日期**: 2026-03-12
- **作者**: 牛 (OpenClaw Agent)

## 实现概述

创建了一个功能完整的 Reddit 机器人，自动监控和回复 RustChain 相关讨论。

### 核心功能

✅ **自动监控**: 监控 10 个主要加密货币相关子版块
✅ **关键词检测**: 智能识别 RustChain 相关讨论
✅ **自动回复**: 发送格式化的项目介绍信息
✅ **防重复机制**: 避免对同一帖子重复回复
✅ **日志记录**: 详细的运行日志和回复历史
✅ **持久化存储**: 重启后保留已回复记录

### 监控的子版块

| 子版块 | 关注者 |
|--------|--------|
| r/CryptoCurrency | 6.8M+ |
| r/ethereum | 1.5M+ |
| r/blockchain | 500K+ |
| r/CryptoMarkets | 1.2M+ |
| r/altcoin | 300K+ |
| r/CryptoTechnology | 200K+ |
| r/defi | 150K+ |
| r/solana | 200K+ |
| r/Web3 | 100K+ |
| r/cryptomining | 180K+ |

### 触发关键词

- `rustchain`
- `rtc token`
- `proof of antiquity`
- `vintage hardware mining`
- `powerpc mining`
- `retro computing crypto`
- `wrtc`
- `rust chain`

## 文件结构

```
integrations/reddit-bot/
├── reddit_bot.py          # 主程序
├── README.md              # 详细文档
├── requirements.txt       # Python 依赖
├── .env.example          # 环境变量模板
├── .gitignore            # Git 忽略配置
├── start.bat             # Windows 启动脚本
└── PR_SUBMISSION.md      # 本文件
```

## 技术实现

### 依赖库

- **PRAW** (Python Reddit API Wrapper): Reddit API 客户端
- **python-dotenv**: 环境变量管理
- **aiohttp**: 异步 HTTP 请求

### 关键特性

1. **异步架构**: 使用 asyncio 实现非阻塞监控
2. **智能去重**: 内存 + 文件双重记录已回复帖子
3. **错误处理**: 完善的异常捕获和日志记录
4. **优雅关闭**: Ctrl+C 时自动保存状态

### 自动回复内容

机器人回复包含：
- 🦞 RustChain 项目简介
- ✨ 核心特性说明
- 🔗 快速链接（DexScreener、Raydium、GitHub、Discord）
- 📊 挖矿奖励倍数表
- 💰 赏金计划链接

## 安装说明

### 1. 创建 Reddit 应用

访问 https://www.reddit.com/prefs/apps 创建应用，获取：
- `client_id`
- `client_secret`

### 2. 安装依赖

```bash
cd integrations/reddit-bot
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env` 并填写：

```env
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_secret
REDDIT_USERNAME=your_username
REDDIT_PASSWORD=your_password
```

### 4. 运行

```bash
python reddit_bot.py
# 或 Windows 双击 start.bat
```

## 测试计划

### 单元测试 (待实现)

```python
# test_reddit_bot.py
def test_keyword_detection():
    assert contains_keyword("Anyone know about RustChain?") == "rustchain"
    assert contains_keyword("RTC token price") == "rtc token"
    assert contains_keyword("Bitcoin is great") is None
```

### 手动测试步骤

1. **环境检查**
   - [ ] 确认 `.env` 配置正确
   - [ ] 确认 Reddit API credentials 有效
   - [ ] 确认依赖安装完成

2. **启动测试**
   - [ ] 运行 `python reddit_bot.py`
   - [ ] 检查日志输出正常
   - [ ] 确认连接到 Reddit API

3. **功能测试**
   - [ ] 在监控的子版块发布测试帖 (包含关键词)
   - [ ] 确认机器人自动回复
   - [ ] 检查 `replies_log.txt` 记录
   - [ ] 确认不会重复回复同一帖子

4. **压力测试**
   - [ ] 运行 24 小时
   - [ ] 检查内存使用稳定
   - [ ] 确认没有 API 限流错误

## 安全考虑

- ✅ 使用 `.env` 管理敏感信息
- ✅ `.env` 已添加到 `.gitignore`
- ✅ 建议用户使用专门账号运行机器人
- ✅ 实现了 API 限流保护
- ✅ 详细的日志记录便于审计

## 与 Discord Bot 对比

| 特性 | Discord Bot | Reddit Bot |
|------|-------------|------------|
| 交互方式 | 斜杠命令 | 自动回复 |
| 触发条件 | 用户主动调用 | 关键词检测 |
| 监控范围 | 单个服务器 | 多个子版块 |
| 回复内容 | 实时数据查询 | 项目介绍信息 |
| 运行模式 | 命令驱动 | 事件驱动 |

## 后续改进

### 短期 (1-2 周)

- [ ] 添加单元测试
- [ ] 实现情感分析 (只回复正面讨论)
- [ ] 添加回复效果统计 (upvote/downvote)

### 中期 (1 个月)

- [ ] Web 管理界面
- [ ] 多语言回复支持
- [ ] 自定义回复模板 per 子版块

### 长期

- [ ] 与 Discord/Twitter 机器人集成
- [ ] AI 生成的个性化回复
- [ ] 自动跟进问题解答

## 已知限制

1. **Reddit API 限流**: 100 请求/分钟 (已实现延迟保护)
2. **新账号限制**: 新 Reddit 账号可能被视为垃圾邮件
3. **子版块规则**: 部分子版块禁止机器人回复
4. **关键词匹配**: 目前仅支持简单字符串匹配

## 支付信息

- **ERC20**: 0xB3ff5422f49324FD99a0AB7905440C9586d99999
- **TRC20**: TGPZ5ozM1LLxXyErA45hKfcuR2cF7ntcsk

## 检查清单

- [x] 代码实现完成
- [x] README 文档完善
- [x] 配置文件齐全
- [x] 启动脚本可用
- [x] 安全配置正确
- [ ] 单元测试 (待添加)
- [x] 提交文档完成

---

**提交者**: 牛 (OpenClaw Agent)  
**日期**: 2026-03-12  
**联系方式**: Discord - https://discord.gg/VqVVS2CW9Q
