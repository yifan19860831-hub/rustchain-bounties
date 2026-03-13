# RustChain Community Engagement Metrics

## 概述

本文档定义了 RustChain 社区参与度的核心指标体系，用于追踪和衡量社区健康度、增长趋势和贡献者活跃度。

---

## 一、核心指标分类

### 1. Discord 社区指标

#### 1.1 基础指标
| 指标名称 | 说明 | 追踪方式 |
|---------|------|---------|
| 总成员数 | Discord 服务器总人数 | Discord API / 手动记录 |
| 日活跃用户 (DAU) | 每日发送消息的独立用户数 | Discord API |
| 周活跃用户 (WAU) | 每周发送消息的独立用户数 | Discord API |
| 月活跃用户 (MAU) | 每月发送消息的独立用户数 | Discord API |
| 新增成员数 | 每日/周/月新加入成员数 | Discord API |
| 成员流失率 | 每日/周/月离开成员数 | Discord API |

#### 1.2 互动质量指标
| 指标名称 | 说明 | 追踪方式 |
|---------|------|---------|
| 日均消息数 | 每日总消息数量 | Discord API |
| 人均消息数 | 日均消息数 / DAU | 计算得出 |
| 活跃频道分布 | 各频道消息占比 | Discord API |
| 回复率 | 有回复的对话线程占比 | Discord API |
| 平均响应时间 | 问题发出到首次回复的时间 | Discord API |
| 高峰时段 | 消息最活跃的时间段 | Discord API |

#### 1.3 追踪方法

**使用 Discord API:**
```bash
# 获取服务器成员数
GET /guilds/{guild.id}

# 获取频道消息
GET /channels/{channel.id}/messages

# 需要 Bot Token 和适当权限
```

**手动追踪模板 (每日记录):**
```markdown
## Discord 日报 - YYYY-MM-DD
- 总成员：XXX
- 新增：+XX
- 流失：-XX
- 日活：XXX
- 总消息：XXX
- 最活跃频道：#general (XX 条)
```

---

### 2. GitHub 社区指标

#### 2.1 仓库增长指标
| 指标名称 | 说明 | 追踪方式 |
|---------|------|---------|
| Star 总数 | 仓库总 Star 数 | GitHub API |
| Star 增长率 | 每日/周/月新增 Star 数 | GitHub API |
| Fork 总数 | 仓库总 Fork 数 | GitHub API |
| Watcher 数 | 关注仓库的用户数 | GitHub API |
| 仓库访问数 | 仓库页面访问次数 | GitHub Insights |
| 独立访客数 | 独立 IP 访问数 | GitHub Insights |

#### 2.2 贡献者指标
| 指标名称 | 说明 | 追踪方式 |
|---------|------|---------|
| 贡献者总数 | 历史贡献者数量 | GitHub API |
| 活跃贡献者 | 近 30 天有提交的用户 | GitHub API |
| 新增贡献者 | 首次提交的用户数 | GitHub API |
| 提交频率 | 每日/周提交次数 | GitHub API |
| PR 数量 | 开放/关闭/合并的 PR 数 | GitHub API |
| Issue 数量 | 开放/关闭的 Issue 数 | GitHub API |
| PR 合并率 | 合并 PR 数 / 总 PR 数 | 计算得出 |
| 平均合并时间 | PR 创建到合并的时间 | GitHub API |

#### 2.3 赏金任务指标
| 指标名称 | 说明 | 追踪方式 |
|---------|------|---------|
| 开放赏金数 | 当前开放的 bounty 数量 | GitHub API |
| 已完成赏金数 | 已完成的 bounty 数量 | GitHub API |
| 赏金参与人数 | 参与 bounty 的独立用户 | GitHub API |
| 平均完成时间 | Issue 创建到关闭的时间 | GitHub API |
| 赏金分布 | 各难度级别的任务分布 | GitHub API |

#### 2.4 追踪方法

**使用 GitHub API:**
```bash
# 获取仓库统计
GET /repos/Scottcjn/rustchain-bounties

# 获取贡献者
GET /repos/Scottcjn/rustchain-bounties/contributors

# 获取 Issue 统计
GET /repos/Scottcjn/rustchain-bounties/issues?state=all

# 获取 Star 历史 (需第三方工具)
https://api.github.com/repos/Scottcjn/rustchain-bounties/stargazers
```

**使用 gh CLI:**
```bash
# 查看仓库统计
gh repo view Scottcjn/rustchain-bounties --json stargazersCount,forksCount

# 查看 Issue
gh issue list --repo Scottcjn/rustchain-bounties --limit 100

# 查看 PR
gh pr list --repo Scottcjn/rustchain-bounties --limit 100
```

**手动追踪模板 (每周记录):**
```markdown
## GitHub 周报 - YYYY-MM-DD
- Stars: XXX (本周 +XX)
- Forks: XXX (本周 +XX)
- 贡献者：XXX (本周 +XX)
- 开放 Issue: XX
- 开放 PR: XX
- 本周提交：XX 次
```

---

### 3. 社交媒体指标

#### 3.1 Twitter/X 指标
| 指标名称 | 说明 | 追踪方式 |
|---------|------|---------|
| 粉丝总数 | 账号总粉丝数 | Twitter API |
| 粉丝增长率 | 每日/周新增粉丝 | Twitter API |
| 推文互动率 | (点赞 + 转发 + 回复) / 曝光量 | Twitter API |
| 平均曝光量 | 每条推文的平均曝光 | Twitter API |
| 提及次数 | 被用户提及的次数 | Twitter API |
| 话题标签使用 | #RustChain 标签使用次数 | 搜索 API |

#### 3.2 其他平台指标
| 平台 | 核心指标 | 追踪方式 |
|-----|---------|---------|
| Reddit | 订阅数、帖子互动 | Reddit API |
| Telegram | 成员数、消息数 | Telegram Bot API |
| YouTube | 订阅、观看、互动 | YouTube API |
| Medium | 文章阅读、点赞 | Medium API |
| 知乎/微博 (中文社区) | 关注、转发、评论 | 平台 API |

#### 3.3 追踪方法

**使用社交媒体管理工具:**
- Hootsuite / Buffer: 多平台统一管理
- Social Blade: 粉丝增长追踪
- Google Analytics: 社交媒体引流统计

**手动追踪模板 (每周记录):**
```markdown
## 社交媒体周报 - YYYY-MM-DD

### Twitter/X
- 粉丝：XXX (本周 +XX)
- 本周推文：X 条
- 平均互动：XX 点赞/条

### 其他平台
- Telegram 成员：XXX
- Reddit 订阅：XXX
```

---

## 二、综合健康度指标

### 2.1 社区健康评分

```
社区健康分 = (Discord 活跃分 × 0.4) + (GitHub 贡献分 × 0.4) + (社交媒体影响分 × 0.2)
```

#### Discord 活跃分 (0-100)
```
= (DAU / 总成员) × 50 + (日均消息 / 总成员) × 50
```

#### GitHub 贡献分 (0-100)
```
= (活跃贡献者 / 总贡献者) × 40 + (PR 合并率) × 30 + (Star 增长率) × 30
```

#### 社交媒体影响分 (0-100)
```
= (粉丝增长率) × 40 + (平均互动率) × 40 + (提及增长) × 20
```

### 2.2 增长趋势指标

| 指标 | 计算方式 | 健康阈值 |
|-----|---------|---------|
| 成员增长率 | (本月新增 - 本月流失) / 月初总数 | > 5%/月 |
| 贡献者留存率 | 上月活跃且本月仍活跃的贡献者占比 | > 60% |
| 内容产出率 | 每周新内容 (PR/Issue/推文) 数量 | > 20/周 |
| 互动深度 | 平均对话轮次 / 平均响应时间 | > 3 轮 / <2h |

---

## 三、数据收集自动化方案

### 3.1 推荐工具栈

| 工具 | 用途 | 成本 |
|-----|------|-----|
| GitHub Actions | 定时收集 GitHub 数据 | 免费 |
| Discord Webhook | Discord 事件通知 | 免费 |
| Google Sheets | 数据存储和可视化 | 免费 |
| Grafana | 数据仪表板 | 免费/付费 |
| Python 脚本 | API 数据收集 | 免费 |

### 3.2 自动化脚本示例

**GitHub 数据收集 (Python):**
```python
import requests
import json
from datetime import datetime

GITHUB_TOKEN = "your_token"
REPO = "Scottcjn/rustchain-bounties"

def get_repo_stats():
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(f"https://api.github.com/repos/{REPO}", headers=headers)
    data = response.json()
    
    return {
        "date": datetime.now().isoformat(),
        "stars": data["stargazers_count"],
        "forks": data["forks_count"],
        "open_issues": data["open_issues_count"],
        "subscribers": data["subscribers_count"]
    }
```

**Discord 数据收集 (Python):**
```python
import discord
import asyncio

intents = discord.Intents.default()
intents.members = True
intents.messages = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild = client.get_guild(GUILD_ID)
    print(f"Members: {guild.member_count}")
    # 收集更多数据...
    
client.run("BOT_TOKEN")
```

### 3.3 定时任务配置

**GitHub Actions 工作流 (.github/workflows/metrics.yml):**
```yaml
name: Community Metrics Collection

on:
  schedule:
    - cron: '0 0 * * *'  # 每天 UTC 0 点

jobs:
  collect:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Collect GitHub metrics
        run: python scripts/collect_github.py
      - name: Commit metrics
        run: |
          git config --local user.email "bot@rustchain.org"
          git config --local user.name "Metrics Bot"
          git add metrics/
          git commit -m "Daily metrics $(date)" || exit 0
          git push
```

---

## 四、报告模板

### 4.1 日报模板

```markdown
## RustChain 社区日报 - YYYY-MM-DD

### Discord
- 总成员：XXX (±XX)
- 日活：XXX
- 消息数：XXX

### GitHub
- Stars: XXX (+XX)
- 新 Issue: X
- 新 PR: X
- 合并 PR: X

### 亮点
- [今日重要事件或成就]
```

### 4.2 周报模板

```markdown
## RustChain 社区周报 - YYYY-MM-DD

### 核心指标概览
| 指标 | 本周 | 上周 | 变化 |
|-----|------|------|------|
| Discord 成员 | XXX | XXX | +X% |
| GitHub Stars | XXX | XXX | +X% |
| 活跃贡献者 | XX | XX | +X% |

### 本周成就
- [列出重要成就]

### 下周目标
- [列出目标]
```

### 4.3 月报模板

```markdown
## RustChain 社区月报 - YYYY 年 MM 月

### 月度概览
- 社区健康分：XX/100
- 新增成员：XXX
- 新增贡献者：XX
- 完成赏金：XX 个

### 趋势分析
[图表和趋势说明]

### 下月计划
[战略规划]
```

---

## 五、最佳实践建议

### 5.1 数据收集
- ✅ 自动化优先：减少手动工作
- ✅ 一致性：固定时间收集数据
- ✅ 备份：定期导出数据备份
- ❌ 避免过度收集：只收集有用的指标

### 5.2 数据分析
- ✅ 关注趋势而非单点数据
- ✅ 设定基准线和目标
- ✅ 定期回顾和调整指标
- ❌ 避免虚荣指标 (只看总数不看增长率)

### 5.3 报告分享
- ✅ 保持透明：向社区公开指标
- ✅ 可视化：使用图表展示趋势
- ✅ 简洁：突出关键信息
- ❌ 避免信息过载

---

## 六、资源链接

- [GitHub API 文档](https://docs.github.com/en/rest)
- [Discord API 文档](https://discord.com/developers/docs)
- [Twitter API 文档](https://developer.twitter.com/en/docs)
- [GitHub Insights](https://github.com/Scottcjn/rustchain-bounties/pulse)
- [Discord 服务器](https://discord.gg/VqVVS2CW9Q)

---

## 七、维护记录

| 日期 | 更新内容 | 作者 |
|-----|---------|------|
| 2026-03-12 | 初始版本创建 | 社区贡献者 |

---

*本文档为 RustChain 社区度量标准，欢迎贡献者提出改进建议。*
