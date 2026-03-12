#!/usr/bin/env python3
"""
RustChain Community Metrics Collector

自动收集 GitHub、Discord 和社交媒体数据
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path

# 配置
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")
DISCORD_GUILD_ID = os.getenv("DISCORD_GUILD_ID", "")
REPO_OWNER = "Scottcjn"
REPO_NAME = "rustchain-bounties"

class MetricsCollector:
    def __init__(self):
        self.timestamp = datetime.now().isoformat()
        self.metrics = {
            "date": self.timestamp,
            "github": {},
            "discord": {},
            "social": {}
        }
    
    def collect_github_metrics(self):
        """收集 GitHub 仓库数据"""
        print("收集 GitHub 数据...")
        
        headers = {}
        if GITHUB_TOKEN:
            headers["Authorization"] = f"token {GITHUB_TOKEN}"
        
        # 仓库基本信息
        repo_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"
        response = requests.get(repo_url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            self.metrics["github"] = {
                "stars": data.get("stargazers_count", 0),
                "forks": data.get("forks_count", 0),
                "watchers": data.get("watchers_count", 0),
                "open_issues": data.get("open_issues_count", 0),
                "subscribers": data.get("subscribers_count", 0),
                "size": data.get("size", 0)
            }
        
        # 贡献者信息
        contributors_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contributors"
        response = requests.get(contributors_url, headers=headers)
        
        if response.status_code == 200:
            contributors = response.json()
            self.metrics["github"]["total_contributors"] = len(contributors)
            self.metrics["github"]["top_contributors"] = [
                {"login": c["login"], "contributions": c["contributions"]}
                for c in sorted(contributors, key=lambda x: x["contributions"], reverse=True)[:5]
            ]
        
        # Issue 统计
        issues_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
        response = requests.get(issues_url, headers=headers, params={"state": "all"})
        
        if response.status_code == 200:
            issues = response.json()
            open_issues = [i for i in issues if i.get("state") == "open"]
            closed_issues = [i for i in issues if i.get("state") == "closed"]
            
            # 赏金任务统计
            bounty_issues = [i for i in issues if "bounty" in str(i.get("labels", []))]
            
            self.metrics["github"]["total_issues"] = len(issues)
            self.metrics["github"]["open_issues"] = len(open_issues)
            self.metrics["github"]["closed_issues"] = len(closed_issues)
            self.metrics["github"]["bounty_issues"] = len(bounty_issues)
        
        # PR 统计
        pulls_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls"
        response = requests.get(pulls_url, headers=headers, params={"state": "all"})
        
        if response.status_code == 200:
            pulls = response.json()
            open_pulls = [p for p in pulls if p.get("state") == "open"]
            closed_pulls = [p for p in pulls if p.get("state") == "closed"]
            merged_pulls = [p for p in pulls if p.get("merged_at")]
            
            self.metrics["github"]["total_pulls"] = len(pulls)
            self.metrics["github"]["open_pulls"] = len(open_pulls)
            self.metrics["github"]["closed_pulls"] = len(closed_pulls)
            self.metrics["github"]["merged_pulls"] = len(merged_pulls)
            
            if len(pulls) > 0:
                self.metrics["github"]["merge_rate"] = round(len(merged_pulls) / len(pulls) * 100, 2)
        
        print(f"✓ GitHub: Stars={self.metrics['github'].get('stars', 'N/A')}, "
              f"Contributors={self.metrics['github'].get('total_contributors', 'N/A')}")
    
    def collect_discord_metrics(self):
        """收集 Discord 服务器数据"""
        print("收集 Discord 数据...")
        
        if not DISCORD_TOKEN or not DISCORD_GUILD_ID:
            print("⚠ Discord 令牌未配置，跳过")
            return
        
        headers = {"Authorization": f"Bot {DISCORD_TOKEN}"}
        
        # 服务器信息
        guild_url = f"https://discord.com/api/guilds/{DISCORD_GUILD_ID}"
        response = requests.get(guild_url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            self.metrics["discord"] = {
                "guild_name": data.get("name", ""),
                "member_count": data.get("approximate_member_count", 0),
                "presence_count": data.get("approximate_presence_count", 0)
            }
        
        print(f"✓ Discord: Members={self.metrics['discord'].get('member_count', 'N/A')}")
    
    def calculate_health_score(self):
        """计算社区健康评分"""
        github = self.metrics.get("github", {})
        discord = self.metrics.get("discord", {})
        
        # GitHub 分数 (0-100)
        github_score = 0
        if github.get("total_contributors", 0) > 0:
            github_score += min(40, github["total_contributors"] * 2)
        if github.get("merge_rate", 0) > 0:
            github_score += min(30, github["merge_rate"] * 0.3)
        if github.get("stars", 0) > 0:
            github_score += min(30, github["stars"] * 0.1)
        
        # Discord 分数 (0-100)
        discord_score = 0
        if discord.get("member_count", 0) > 0 and discord.get("presence_count", 0) > 0:
            activity_rate = discord["presence_count"] / discord["member_count"]
            discord_score = min(100, activity_rate * 100)
        
        # 综合分数
        total_score = (github_score * 0.4) + (discord_score * 0.4)
        
        self.metrics["health_score"] = {
            "github": round(github_score, 2),
            "discord": round(discord_score, 2),
            "total": round(total_score, 2)
        }
        
        print(f"✓ 健康评分：{self.metrics['health_score']['total']}/100")
    
    def save_metrics(self, output_dir="metrics"):
        """保存数据到文件"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # 保存为 JSON
        date_str = datetime.now().strftime("%Y-%m-%d")
        json_file = output_path / f"metrics_{date_str}.json"
        
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(self.metrics, f, indent=2, ensure_ascii=False)
        
        # 追加到总记录
        all_metrics_file = output_path / "all_metrics.jsonl"
        with open(all_metrics_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(self.metrics, ensure_ascii=False) + "\n")
        
        print(f"✓ 数据已保存：{json_file}")
    
    def collect_all(self):
        """执行完整的数据收集"""
        print(f"\n{'='*50}")
        print(f"RustChain 社区数据收集 - {self.timestamp}")
        print(f"{'='*50}\n")
        
        self.collect_github_metrics()
        self.collect_discord_metrics()
        self.calculate_health_score()
        self.save_metrics()
        
        print(f"\n{'='*50}")
        print("收集完成!")
        print(f"{'='*50}\n")
        
        return self.metrics


def main():
    collector = MetricsCollector()
    metrics = collector.collect_all()
    
    # 打印摘要
    print("\n📊 数据摘要:")
    if metrics.get("github"):
        print(f"  GitHub Stars: {metrics['github'].get('stars', 'N/A')}")
        print(f"  贡献者：{metrics['github'].get('total_contributors', 'N/A')}")
        print(f"  开放 Issue: {metrics['github'].get('open_issues', 'N/A')}")
    
    if metrics.get("discord"):
        print(f"  Discord 成员：{metrics['discord'].get('member_count', 'N/A')}")
    
    if metrics.get("health_score"):
        print(f"  社区健康分：{metrics['health_score']['total']}/100")


if __name__ == "__main__":
    main()
