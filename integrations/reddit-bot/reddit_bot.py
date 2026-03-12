#!/usr/bin/env python3
"""
RustChain Reddit Bot - Issue #1622

Reddit 机器人，自动监控和回复 RustChain 相关问题。
监控 r/CryptoCurrency, r/ethereum, r/blockchain 等子版块，
当检测到 RustChain 相关讨论时自动回复介绍信息。

Author: 牛 (OpenClaw Agent)
Bounty: Scottcjn/rustchain-bounties#1622 (5 RTC)
"""

import os
import asyncio
from datetime import datetime, timedelta
from typing import Optional
import logging

import praw
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# ─── 日志配置 ──────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('reddit_bot.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# ─── 配置 ──────────────────────────────────────────────────────────────

# Reddit API 配置 (从 https://www.reddit.com/prefs/apps 获取)
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "RustChain-Bot/1.0 by OpenClaw-Agent")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")

# 监控的子版块
SUBREDDITS_TO_MONITOR = [
    "CryptoCurrency",
    "ethereum", 
    "blockchain",
    "CryptoMarkets",
    "altcoin",
    "CryptoTechnology",
    "defi",
    "solana",
    "Web3",
    "cryptomining"
]

# 关键词 (触发自动回复)
KEYWORDS = [
    "rustchain",
    "rtc token",
    "proof of antiquity",
    "vintage hardware mining",
    "powerpc mining",
    "retro computing crypto",
    "wrtc",
    "rust chain"
]

# 自动回复模板
AUTO_REPLY_TEMPLATE = """
🦞 **RustChain (RTC)** - Proof-of-Antiquity Blockchain

Great topic! RustChain is a unique blockchain that rewards **vintage hardware** instead of punishing it. 

**Key Features:**
• 🕰️ **Proof-of-Antiquity**: Older hardware earns 2.5× more rewards
• 🔧 **Hardware Fingerprinting**: 6-layer verification prevents emulation
• 🌉 **Solana Bridge**: wRTC available on Raydium DEX
• 🤖 **AI Agent Economy**: Machine-to-machine payments with x402 protocol

**Quick Links:**
• 📊 [Price Chart](https://dexscreener.com/solana/8CF2Q8nSCxRacDShbtF86XTSrYjueBMKmfdR3MLdnYzb)
• 💱 [Swap wRTC](https://raydium.io/swap/?inputMint=sol&outputMint=12TAdKXxcGf6oCv4rqDz2NkgxjyHq6HQKoxKZYGf5i4X)
• 📖 [Documentation](https://github.com/Scottcjn/Rustchain)
• 💬 [Discord](https://discord.gg/VqVVS2CW9Q)

**Mining Multipliers:**
| Hardware | Era | Multiplier |
|----------|-----|------------|
| PowerPC G4 | 1999-2005 | 2.5× |
| PowerPC G5 | 2003-2006 | 2.0× |
| Core 2 Duo | 2006-2011 | 1.3× |
| Modern x86 | Current | 1.0× |

*Every contribution earns RTC tokens. Check out [open bounties](https://github.com/Scottcjn/rustchain-bounties/issues)!*

---
*I'm a bot | [Report Issue](https://github.com/Scottcjn/rustchain-bounties/issues/new)*
"""

# 已回复的帖子 ID (避免重复回复)
replied_posts = set()

# Reddit 客户端
reddit = None


# ─── Reddit 功能 ────────────────────────────────────────────────────

def initialize_reddit():
    """初始化 Reddit 客户端"""
    if not all([REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD]):
        raise ValueError(
            "缺少 Reddit API 配置！请设置以下环境变量:\n"
            "- REDDIT_CLIENT_ID\n"
            "- REDDIT_CLIENT_SECRET\n"
            "- REDDIT_USERNAME\n"
            "- REDDIT_PASSWORD\n"
            "\n在 https://www.reddit.com/prefs/apps 创建应用获取 credentials"
        )
    
    reddit_instance = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT,
        username=REDDIT_USERNAME,
        password=REDDIT_PASSWORD
    )
    
    logger.info(f"Reddit 客户端已初始化 (用户：{reddit_instance.user.me()})")
    return reddit_instance


def contains_keyword(text):
    """检查文本是否包含关键词，返回匹配的关键词"""
    text_lower = text.lower()
    for keyword in KEYWORDS:
        if keyword.lower() in text_lower:
            return keyword
    return None


def process_submission(submission):
    """处理单个帖子"""
    # 跳过已回复的帖子
    if submission.id in replied_posts:
        return
    
    # 检查标题是否包含关键词
    matched_keyword = contains_keyword(submission.title)
    if not matched_keyword:
        return
    
    logger.info(f"检测到相关帖子：{submission.title} (关键词：{matched_keyword})")
    
    try:
        # 检查是否已经回复过 (避免重复)
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            if comment.author and comment.author.name == REDDIT_USERNAME:
                logger.info(f"帖子 {submission.id} 已有我们的回复，跳过")
                replied_posts.add(submission.id)
                return
        
        # 发送回复
        submission.reply(AUTO_REPLY_TEMPLATE)
        logger.info(f"已回复帖子：{submission.permalink}")
        replied_posts.add(submission.id)
        
        # 记录到日志
        with open("replies_log.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()} - {submission.permalink}\n")
            
    except Exception as e:
        logger.error(f"回复帖子失败 {submission.id}: {e}")


def monitor_subreddits():
    """持续监控子版块"""
    logger.info(f"开始监控子版块：{', '.join(SUBREDDITS_TO_MONITOR)}")
    
    while True:
        try:
            for subreddit_name in SUBREDDITS_TO_MONITOR:
                try:
                    subreddit = reddit.subreddit(subreddit_name)
                    
                    # 获取最新帖子
                    for submission in subreddit.new(limit=25):
                        # 只处理 24 小时内的帖子
                        post_time = datetime.fromtimestamp(submission.created_utc)
                        if post_time < datetime.now() - timedelta(hours=24):
                            break
                        
                        process_submission(submission)
                        
                except Exception as e:
                    logger.error(f"处理子版块 {subreddit_name} 时出错：{e}")
            
            # 每 5 分钟检查一次
            logger.info("完成一轮扫描，5 分钟后继续...")
            import time
            time.sleep(300)
            
        except Exception as e:
            logger.error(f"监控循环出错：{e}")
            import time
            time.sleep(60)


# ─── 主程序 ────────────────────────────────────────────────────

def main():
    """主程序入口"""
    global reddit
    
    logger.info("🦞 RustChain Reddit Bot 启动中...")
    
    # 初始化 Reddit 客户端
    try:
        reddit = initialize_reddit()
    except ValueError as e:
        logger.error(str(e))
        return
    
    # 加载已回复的帖子 ID
    if os.path.exists("replied_posts.txt"):
        with open("replied_posts.txt", "r") as f:
            for line in f:
                if line.strip():
                    replied_posts.add(line.strip())
        logger.info(f"已加载 {len(replied_posts)} 个已回复帖子 ID")
    
    # 启动监控
    try:
        monitor_subreddits()
    except KeyboardInterrupt:
        logger.info("收到中断信号，正在关闭...")
    finally:
        # 保存已回复的帖子 ID
        with open("replied_posts.txt", "w") as f:
            f.write("\n".join(replied_posts))
        logger.info(f"已保存 {len(replied_posts)} 个已回复帖子 ID")


if __name__ == "__main__":
    main()
