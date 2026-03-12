# 🐦 RustChain Twitter Bot

Twitter 机器人集成，自动发布 RustChain 网络状态、矿工信息、epoch 更新等动态，并与社区互动。

**Bounty**: [Scottcjn/rustchain-bounties#1621](https://github.com/Scottcjn/rustchain-bounties/issues/1621)  
**奖励**: 3 RTC  
**作者**: 牛 (OpenClaw Agent)

## 功能特性

### 📢 自动发布

- **网络健康状态** - 定期发布节点运行状态
- **矿工信息** - 展示活跃矿工 Top 5 和总算力
- **Epoch 更新** - 通知 epoch 变化和奖励池信息
- **网络统计** - 发布总算力、区块数等数据
- **欢迎推文** - 轮换发布项目介绍和特色内容

### 💬 互动回复

自动回复提及，支持关键词触发：

| 关键词 | 回复内容 |
|--------|----------|
| hello/hi | 欢迎消息 + 项目链接 |
| price | RTC 价格信息 |
| mining/mine | 挖矿指南 + Discord 链接 |

### 🔄 可配置

- 发布间隔时间（默认 4 小时）
- 自动发布开关
- 自定义 API 端点

## 安装步骤

### 1. 申请 Twitter API

1. 访问 https://developer.twitter.com/
2. 登录并创建项目
3. 创建应用（App）
4. 获取以下凭证：
   - API Key
   - API Secret
   - Access Token
   - Access Token Secret
   - Bearer Token

### 2. 安装依赖

```bash
cd integrations/twitter-bot
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 3. 配置环境变量

复制环境变量模板：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# Twitter API Credentials
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
TWITTER_BEARER_TOKEN=your_bearer_token_here

# RustChain API Configuration
RUSTCHAIN_API_URL=https://rustchain.org

# Bot Configuration
POST_INTERVAL_HOURS=4
AUTO_POST=true
```

### 4. 运行机器人

```bash
python twitter_bot.py
```

## 发布内容示例

### 健康状态
```
✅ RustChain 网络状态

版本：1.2.3
运行时间：48.5 小时
数据库：✅ 正常

#RustChain #RTC #Blockchain
```

### 矿工信息
```
⛏️ RustChain 活跃矿工 Top 5

1. 0xabc123... - 125.50 H/s
2. 0xdef456... - 98.20 H/s
3. 0xghi789... - 87.30 H/s
4. 0xjkl012... - 76.40 H/s
5. 0xmno345... - 65.10 H/s

总算力：42 矿工在线

加入挖矿：https://github.com/Scottcjn/RustChain
#RustChain #Mining #RTC
```

### Epoch 更新
```
📊 RustChain Epoch #156

区块高度：1,234,567
奖励池：50,000.00 RTC

下一个 epoch 即将开始！
#RustChain #Epoch #Crypto
```

### 网络统计
```
📈 RustChain 网络统计

矿工总数：42
区块总数：1,234,567
网络算力：452.30 H/s

1 RTC ≈ $0.10 USD

#RustChain #RTC #ProofOfAntiquity
```

## 配置选项

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `POST_INTERVAL_HOURS` | 发布间隔（小时） | 4 |
| `AUTO_POST` | 是否自动发布 | true |
| `RUSTCHAIN_API_URL` | RustChain API 地址 | https://rustchain.org |

## 运行模式

### 自动发布模式（默认）

```bash
python twitter_bot.py
```

- 每 4 小时发布一次网络状态
- 实时监控提及并回复

### 仅监控模式

编辑 `.env`：

```env
AUTO_POST=false
```

运行：

```bash
python twitter_bot.py
```

- 不自动发布推文
- 仅回复用户提及

## 部署建议

### 使用 systemd（Linux）

创建服务文件 `/etc/systemd/system/rustchain-twitter-bot.service`：

```ini
[Unit]
Description=RustChain Twitter Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/twitter-bot
Environment=PATH=/path/to/.venv/bin
ExecStart=/path/to/.venv/bin/python twitter_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl enable rustchain-twitter-bot
sudo systemctl start rustchain-twitter-bot
sudo systemctl status rustchain-twitter-bot
```

### 使用 Docker（可选）

创建 `Dockerfile`：

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "twitter_bot.py"]
```

构建和运行：

```bash
docker build -t rustchain-twitter-bot .
docker run -d --env-file .env rustchain-twitter-bot
```

## 安全注意事项

- ⚠️ **永远不要**在代码中硬编码 API 凭证
- ⚠️ 使用 `.env` 文件并通过 `python-dotenv` 加载
- ⚠️ 将 `.env` 添加到 `.gitignore`
- ⚠️ 生产环境使用 secrets 管理服务
- ⚠️ 定期轮换 API 密钥

## 故障排除

### 认证失败

```
tweepy.errors.Unauthorized: 401 Unauthorized
```

检查 `.env` 文件中的 Twitter API 凭证是否正确。

### API 限流

```
tweepy.errors.TooManyRequests: 429 Too Many Requests
```

等待限流窗口结束，或减少发布频率。

### RustChain API 连接失败

```
aiohttp.client_exceptions.ClientConnectorError
```

检查 `RUSTCHAIN_API_URL` 配置和网络连接。

## 贡献

欢迎提交 PR 增加新功能！

### 待开发功能

- [ ] 推文内容模板自定义
- [ ] 多账号支持
- [ ] 推文分析统计
- [ ] 自动转发社区内容
- [ ] 多语言支持
- [ ] 图片/图表生成

## 测试

运行测试脚本：

```bash
python test_twitter_bot.py
```

## 相关链接

- [RustChain 主仓库](https://github.com/Scottcjn/RustChain)
- [RustChain Bounties](https://github.com/Scottcjn/rustchain-bounties)
- [Twitter Developer Portal](https://developer.twitter.com/)
- [Tweepy 文档](https://docs.tweepy.org/)
- [Discord 社区](https://discord.gg/VqVVS2CW9Q)
- [官方网站](https://rustchain.org)

---

**许可证**: MIT License  
**维护者**: RustChain 社区
