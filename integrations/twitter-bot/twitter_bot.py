#!/usr/bin/env python3
"""
RustChain Twitter Bot - Issue #1621

Twitter 机器人，自动发布 RustChain 网络状态、矿工信息、epoch 更新等动态。

功能：
- 定期发布网络健康状态
- 发布活跃矿工信息
- Epoch 更新通知
- 社区互动回复

Author: 牛 (OpenClaw Agent)
Bounty: Scottcjn/rustchain-bounties#1621 (3 RTC)
"""

import os
import asyncio
import random
from datetime import datetime, timedelta
from typing import Optional, List

import tweepy
from dotenv import load_dotenv
import aiohttp

# 加载环境变量
load_dotenv()

# ─── 配置 ──────────────────────────────────────────────────────────────

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

RUSTCHAIN_API_URL = os.getenv("RUSTCHAIN_API_URL", "https://rustchain.org")
POST_INTERVAL_HOURS = int(os.getenv("POST_INTERVAL_HOURS", "4"))
AUTO_POST = os.getenv("AUTO_POST", "true").lower() == "true"

# Twitter 客户端
client = tweepy.Client(
    consumer_key=TWITTER_API_KEY,
    consumer_secret=TWITTER_API_SECRET,
    access_token=TWITTER_ACCESS_TOKEN,
    access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
    wait_on_rate_limit=True
)

# HTTP Session for API calls
http_session: Optional[aiohttp.ClientSession] = None


# ─── RustChain API 客户端 ──────────────────────────────────────────────

async def rustchain_health() -> dict:
    """检查节点健康状态"""
    url = f"{RUSTCHAIN_API_URL}/health"
    async with http_session.get(url, ssl=False) as response:
        return await response.json()


async def rustchain_miners() -> list:
    """获取活跃矿工列表"""
    url = f"{RUSTCHAIN_API_URL}/api/miners"
    async with http_session.get(url, ssl=False) as response:
        return await response.json()


async def rustchain_epoch() -> dict:
    """获取当前 epoch 信息"""
    url = f"{RUSTCHAIN_API_URL}/epoch"
    async with http_session.get(url, ssl=False) as response:
        return await response.json()


async def rustchain_stats() -> dict:
    """获取网络统计信息"""
    url = f"{RUSTCHAIN_API_URL}/api/stats"
    async with http_session.get(url, ssl=False) as response:
        return await response.json()


# ─── Twitter 发布功能 ─────────────────────────────────────────────────

def create_health_tweet(health_data: dict) -> str:
    """创建健康状态推文"""
    status = "✅" if health_data.get("ok") else "⚠️"
    version = health_data.get("version", "未知")
    uptime_hours = health_data.get('uptime_s', 0) / 3600
    
    tweet = f"""{status} RustChain 网络状态

版本：{version}
运行时间：{uptime_hours:.1f} 小时
数据库：{"✅ 正常" if health_data.get("db_rw") else "⚠️ 维护"}

#RustChain #RTC #Blockchain"""
    
    return tweet.strip()


def create_miner_tweet(miners_data: list) -> str:
    """创建矿工信息推文"""
    if not miners_data:
        return "🔍 正在搜索活跃矿工..."
    
    top_miners = miners_data[:5]
    miner_list = "\n".join([
        f"{i+1}. {m.get('miner_id', 'Unknown')[:12]}... - {m.get('hashrate', 0):.2f} H/s"
        for i, m in enumerate(top_miners)
    ])
    
    tweet = f"""⛏️ RustChain 活跃矿工 Top 5

{miner_list}

总算力：{len(miners_data)} 矿工在线

加入挖矿：https://github.com/Scottcjn/RustChain
#RustChain #Mining #RTC"""
    
    return tweet.strip()


def create_epoch_tweet(epoch_data: dict) -> str:
    """创建 Epoch 更新推文"""
    epoch_num = epoch_data.get("epoch", 0)
    block_height = epoch_data.get("block_height", 0)
    reward_pool = epoch_data.get("reward_pool", 0)
    
    tweet = f"""📊 RustChain Epoch #{epoch_num}

区块高度：{block_height:,}
奖励池：{reward_pool:,.2f} RTC

下一个 epoch 即将开始！
#RustChain #Epoch #Crypto"""
    
    return tweet.strip()


def create_stats_tweet(stats_data: dict) -> str:
    """创建统计信息推文"""
    total_miners = stats_data.get("total_miners", 0)
    total_blocks = stats_data.get("total_blocks", 0)
    network_hashrate = stats_data.get("network_hashrate", 0)
    
    tweet = f"""📈 RustChain 网络统计

矿工总数：{total_miners}
区块总数：{total_blocks:,}
网络算力：{network_hashrate:.2f} H/s

1 RTC ≈ $0.10 USD

#RustChain #RTC #ProofOfAntiquity"""
    
    return tweet.strip()


def create_welcome_tweet() -> str:
    """创建欢迎推文"""
    tweets = [
        """🎉 欢迎来到 RustChain！

RustChain 是一个基于 Proof-of-Antiquity 的创新区块链，
让复古硬件也能获得更高的挖矿奖励！

🔗 开始：https://github.com/Scottcjn/RustChain
💬 社区：https://discord.gg/VqVVS2CW9Q

#RustChain #RTC #Crypto""",
        
        """💡 你知道吗？

在 RustChain 上，老旧的 CPU 和 GPU 可以获得比新硬件更高的挖矿奖励！

这就是 Proof-of-Antiquity 的魅力 - 
让每一代硬件都有价值！

#RustChain #Mining #GreenCrypto""",
        
        """🚀 RustChain 生态系统

✅ PoA 共识机制
✅ 复古硬件奖励
✅ 社区驱动
✅ 开源透明

加入我们的挖矿革命！
https://rustchain.org

#Blockchain #RTC #DeFi"""
    ]
    
    return random.choice(tweets)


async def post_tweet(text: str) -> bool:
    """发布推文"""
    try:
        response = client.create_tweet(text=text)
        tweet_id = response.data['id']
        print(f"✅ 推文已发布：https://twitter.com/user/status/{tweet_id}")
        return True
    except Exception as e:
        print(f"❌ 发布推文失败：{e}")
        return False


# ─── 自动发布任务 ────────────────────────────────────────────────────

async def scheduled_posts():
    """定时发布任务"""
    post_count = 0
    
    while AUTO_POST:
        try:
            post_count += 1
            print(f"\n[{datetime.now()}] 第 {post_count} 次发布...")
            
            # 轮换发布不同类型的推文
            post_type = post_count % 4
            
            if post_type == 0:
                # 健康状态
                health = await rustchain_health()
                tweet = create_health_tweet(health)
            elif post_type == 1:
                # 矿工信息
                miners = await rustchain_miners()
                tweet = create_miner_tweet(miners)
            elif post_type == 2:
                # Epoch 信息
                epoch = await rustchain_epoch()
                tweet = create_epoch_tweet(epoch)
            else:
                # 统计信息或欢迎推文
                if random.random() > 0.5:
                    stats = await rustchain_stats()
                    tweet = create_stats_tweet(stats)
                else:
                    tweet = create_welcome_tweet()
            
            # 发布推文
            await post_tweet(tweet)
            
            # 等待下一次发布
            wait_time = POST_INTERVAL_HOURS * 3600
            print(f"⏰ 等待 {POST_INTERVAL_HOURS} 小时后发布...")
            await asyncio.sleep(wait_time)
            
        except Exception as e:
            print(f"❌ 发布任务出错：{e}")
            await asyncio.sleep(300)  # 出错后等待 5 分钟


# ─── 互动功能 ───────────────────────────────────────────────────────

async def monitor_mentions():
    """监控提及并回复"""
    print("🔍 开始监控提及...")
    
    last_checked = datetime.now()
    
    while True:
        try:
            # 获取提及
            mentions = client.get_users_mentions(
                id=client.get_user(username="RustChain").data.id,
                max_results=5,
                tweet_fields=["created_at", "author_id"]
            )
            
            for mention in mentions.data or []:
                if mention.created_at > last_checked:
                    # 简单回复逻辑
                    text = mention.text.lower()
                    
                    if "hello" in text or "hi" in text:
                        reply = f"👋 你好！欢迎了解 RustChain！\n\n访问 https://rustchain.org 了解更多！"
                        client.create_tweet(text=reply, in_reply_to_tweet_id=mention.id)
                    
                    elif "price" in text or "price" in text:
                        reply = "💰 1 RTC ≈ $0.10 USD\n\nRustChain 专注于长期价值而非短期炒作！"
                        client.create_tweet(text=reply, in_reply_to_tweet_id=mention.id)
                    
                    elif "mining" in text or "mine" in text:
                        reply = "⛏️ 开始挖矿：https://github.com/Scottcjn/RustChain\n\n加入我们的 Discord：https://discord.gg/VqVVS2CW9Q"
                        client.create_tweet(text=reply, in_reply_to_tweet_id=mention.id)
            
            last_checked = datetime.now()
            await asyncio.sleep(60)  # 每分钟检查一次
            
        except Exception as e:
            print(f"❌ 监控提及出错：{e}")
            await asyncio.sleep(300)


# ─── 主程序 ─────────────────────────────────────────────────────────

async def main():
    """主程序入口"""
    global http_session
    
    print("🚀 RustChain Twitter Bot 启动中...")
    print(f"📡 API URL: {RUSTCHAIN_API_URL}")
    print(f"⏰ 发布间隔：{POST_INTERVAL_HOURS} 小时")
    
    # 创建 HTTP Session
    connector = aiohttp.TCPConnector(ssl=False)
    http_session = aiohttp.ClientSession(connector=connector)
    
    try:
        # 验证 Twitter 连接
        me = client.get_me()
        print(f"✅ 已连接到 Twitter 账号：@{me.data.username}")
        
        # 启动定时发布任务
        if AUTO_POST:
            print("📢 自动发布已启用")
            await asyncio.gather(
                scheduled_posts(),
                monitor_mentions()
            )
        else:
            print("📢 自动发布已禁用，仅监控提及")
            await monitor_mentions()
            
    except Exception as e:
        print(f"❌ 启动失败：{e}")
    finally:
        if http_session:
            await http_session.close()


if __name__ == "__main__":
    asyncio.run(main())
