# 🦞 RustChain Reddit Bot

Reddit 机器人集成，自动监控和回复 RustChain 相关讨论。

## 功能特性

### 自动监控

- 🔍 **关键词检测**: 监控多个加密货币相关子版块
- 🤖 **智能回复**: 当检测到 RustChain 相关讨论时自动回复介绍信息
- 📝 **防重复**: 避免对同一帖子重复回复
- 📊 **日志记录**: 详细记录所有监控和回复活动

### 监控的子版块

| 子版块 | 关注者 | 说明 |
|--------|--------|------|
| r/CryptoCurrency | 6.8M+ | 主流加密货币讨论 |
| r/ethereum | 1.5M+ | 以太坊社区 |
| r/blockchain | 500K+ | 区块链技术 |
| r/CryptoMarkets | 1.2M+ | 加密货币市场 |
| r/altcoin | 300K+ | 山寨币讨论 |
| r/CryptoTechnology | 200K+ | 加密货币技术 |
| r/defi | 150K+ | 去中心化金融 |
| r/solana | 200K+ | Solana 生态 |
| r/Web3 | 100K+ | Web3 技术 |
| r/cryptomining | 180K+ | 加密货币挖矿 |

### 触发关键词

机器人会检测以下关键词（不区分大小写）：

- `rustchain`
- `rtc token`
- `proof of antiquity`
- `vintage hardware mining`
- `powerpc mining`
- `retro computing crypto`
- `wrtc`
- `rust chain`

### 自动回复内容

当检测到相关讨论时，机器人会回复包含以下信息的格式化内容：

- 🦞 RustChain 项目简介
- ✨ 核心特性（Proof-of-Antiquity、硬件指纹、Solana 桥接等）
- 🔗 快速链接（价格图表、交易、文档、Discord）
- 📊 挖矿奖励倍数表
- 💰 赏金计划链接

## 安装步骤

### 1. 创建 Reddit 应用

1. 访问 https://www.reddit.com/prefs/apps
2. 滚动到页面底部，点击 "create another app..."
3. 填写表单：
   - **name**: RustChain Bot
   - **about url**: https://github.com/Scottcjn/Rustchain
   - **redirect uri**: http://localhost:8080
4. 选择 "script" 类型
5. 点击 "create app"
6. 记录以下信息：
   - **client_id**: 显示在 "personal use script" 下方的字符串
   - **client_secret**: 显示为 "secret" 的字符串

### 2. 准备 Reddit 账号

- 使用你的 Reddit 账号登录
- ⚠️ **注意**: 机器人将使用这个账号发帖
- 建议创建专门的账号用于机器人操作
- 确保账号有足够的 Karma 以避免被标记为垃圾邮件

### 3. 安装依赖

```bash
cd integrations/reddit-bot
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 4. 配置环境变量

复制 `.env.example` 为 `.env`：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# Reddit API 配置
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=RustChain-Bot/1.0 by OpenClaw-Agent
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password

# RustChain API 配置 (可选)
RUSTCHAIN_API_URL=https://rustchain.org
```

### 5. 运行机器人

```bash
python reddit_bot.py
```

## 运行示例

```
2026-03-12 17:30:00 - INFO - 🦞 RustChain Reddit Bot 启动中...
2026-03-12 17:30:01 - INFO - Reddit 客户端已初始化 (用户：RustChainBot)
2026-03-12 17:30:01 - INFO - 已加载 0 个已回复帖子 ID
2026-03-12 17:30:01 - INFO - 开始监控子版块：CryptoCurrency, ethereum, blockchain, ...
2026-03-12 17:32:15 - INFO - 检测到相关帖子：Anyone know about RustChain? (关键词：rustchain)
2026-03-12 17:32:16 - INFO - 已回复帖子：/r/CryptoCurrency/comments/abc123/anyone_know_about_rustchain/
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `reddit_bot.py` | 主程序 |
| `requirements.txt` | Python 依赖 |
| `.env.example` | 环境变量模板 |
| `.env` | 实际配置 (需自行创建) |
| `.gitignore` | Git 忽略配置 |
| `reddit_bot.log` | 运行日志 (自动生成) |
| `replied_posts.txt` | 已回复帖子记录 (自动生成) |
| `replies_log.txt` | 回复历史日志 (自动生成) |

## 最佳实践

### 避免被标记为垃圾邮件

1. **控制回复频率**: 机器人已经内置了 5 分钟检查间隔
2. **不要回复所有帖子**: 只回复真正相关的讨论
3. **使用成熟的账号**: 新账号容易被限制
4. **监控日志**: 定期检查是否有错误或被删除的回复

### 自定义配置

#### 添加新的子版块

编辑 `reddit_bot.py`，在 `SUBREDDITS_TO_MONITOR` 列表中添加：

```python
SUBREDDITS_TO_MONITOR = [
    "CryptoCurrency",
    "ethereum",
    "your_new_subreddit",  # 添加新的
    ...
]
```

#### 修改关键词

编辑 `KEYWORDS` 列表：

```python
KEYWORDS = [
    "rustchain",
    "your new keyword",  # 添加新的
    ...
]
```

#### 自定义回复模板

编辑 `AUTO_REPLY_TEMPLATE` 字符串。支持 Markdown 格式。

## 监控和维护

### 查看日志

```bash
# 实时查看日志
tail -f reddit_bot.log

# 查看回复历史
cat replies_log.txt
```

### 检查机器人状态

```bash
# 查看已回复的帖子数量
wc -l replied_posts.txt

# 检查进程是否运行
ps aux | grep reddit_bot
```

### 停止机器人

```bash
# 按 Ctrl+C 停止
# 机器人会自动保存已回复帖子记录
```

## 故障排除

### 认证失败

**错误**: `praw.exceptions.RedditAPIException: INVALID_USER`

**解决**:
1. 检查 `.env` 文件中的用户名和密码
2. 确认 Reddit 账号没有被锁定
3. 如果使用 2FA，需要创建应用专用密码

### 被 Rate Limit

**错误**: `praw.exceptions.RedditAPIException: RATELIMIT`

**解决**:
1. 增加检查间隔 (修改 `asyncio.sleep(300)` 为更大的值)
2. 减少监控的子版块数量
3. 使用更成熟的 Reddit 账号

### 回复被删除

**原因**: 子版块规则不允许机器人回复

**解决**:
1. 检查子版块规则
2. 从监控列表中移除该子版块
3. 联系版主申请许可

### 没有检测到相关帖子

**解决**:
1. 检查关键词列表是否足够
2. 确认机器人有权限访问这些子版块
3. 查看日志确认是否在正常扫描

## API 使用限制

Reddit API 有以下限制：

- **匿名用户**: 60 请求/分钟
- **认证用户**: 100 请求/分钟
- **OAuth 应用**: 根据使用情况调整

机器人已经实现了适当的延迟和错误处理来遵守这些限制。

## 安全注意事项

- ⚠️ **永远不要**提交 `.env` 文件到 Git
- ⚠️ 使用专门的 Reddit 账号运行机器人
- ⚠️ 定期更换密码
- ⚠️ 监控账号活动，防止滥用

## 贡献

欢迎提交 PR 改进机器人！

### 待开发功能

- [ ] 情感分析 (只回复正面/中性讨论)
- [ ] 多语言回复支持
- [ ] 自定义回复模板 per 子版块
- [ ] Web 界面管理
- [ ] 回复效果分析 (upvote/downvote 统计)
- [ ] 自动跟进回复 (当有人提问时)
- [ ] 与其他 RustChain 机器人集成

## 许可证

MIT License - 与 RustChain 主项目保持一致

## 赏金信息

- **Issue**: #1622
- **奖励**: 5 RTC
- **状态**: 已完成

---

**作者**: 牛 (OpenClaw Agent)  
**项目**: RustChain  
**Discord**: https://discord.gg/VqVVS2CW9Q  
**网站**: https://rustchain.org
