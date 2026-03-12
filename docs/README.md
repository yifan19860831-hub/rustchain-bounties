# RustChain Community Metrics

RustChain 社区参与度指标追踪系统

## 📁 文件结构

```
docs/
├── COMMUNITY_METRICS.md    # 完整的指标文档和追踪方案
├── collect_metrics.py      # 自动化数据收集脚本
├── metrics-workflow.yml    # GitHub Actions 工作流配置
└── metrics/                # 存储收集的数据 (自动生成)
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install requests
```

### 2. 配置环境变量

```bash
# GitHub API (可选，提高限流)
export GITHUB_TOKEN="your_github_token"

# Discord API (可选)
export DISCORD_TOKEN="your_discord_bot_token"
export DISCORD_GUILD_ID="your_discord_server_id"
```

### 3. 运行收集脚本

```bash
python collect_metrics.py
```

### 4. 查看结果

数据将保存在 `metrics/` 目录：
- `metrics/metrics_YYYY-MM-DD.json` - 每日数据
- `metrics/all_metrics.jsonl` - 历史数据汇总

## 📊 核心指标

### Discord 指标
- 总成员数
- 日活跃用户 (DAU)
- 日均消息数
- 活跃频道分布

### GitHub 指标
- Star/Fork 数量
- 贡献者数量
- Issue/PR 统计
- 赏金任务完成情况

### 社交媒体指标
- Twitter/X 粉丝增长
- 互动率
- 提及次数

## 🤖 自动化部署

### GitHub Actions

1. 复制 `metrics-workflow.yml` 到 `.github/workflows/`
2. 配置 Secrets:
   - `GITHUB_TOKEN` (自动提供)
   - `DISCORD_TOKEN` (可选)
   - `DISCORD_GUILD_ID` (可选)
3. 工作流将每天自动运行

### 手动触发

在 GitHub Actions 页面手动运行工作流。

## 📈 健康评分

社区健康分计算公式：

```
总分 = (GitHub 分 × 0.4) + (Discord 分 × 0.4) + (社交媒体分 × 0.2)
```

评分标准：
- 🟢 80-100: 优秀
- 🟡 60-79: 良好
- 🟠 40-59: 一般
- 🔴 0-39: 需要改进

## 📝 报告模板

详见 `COMMUNITY_METRICS.md` 文档中的：
- 日报模板
- 周报模板
- 月报模板

## 🔧 自定义指标

编辑 `collect_metrics.py` 添加自定义指标：

```python
def collect_custom_metrics(self):
    # 添加你的自定义逻辑
    self.metrics["custom"] = {...}
```

## 📚 相关资源

- [GitHub API 文档](https://docs.github.com/en/rest)
- [Discord API 文档](https://discord.com/developers/docs)
- [RustChain 主仓库](https://github.com/Scottcjn/RustChain)
- [Discord 服务器](https://discord.gg/VqVVS2CW9Q)

## 🤝 贡献

欢迎提交 PR 改进指标系统！

## 📄 许可证

MIT License
