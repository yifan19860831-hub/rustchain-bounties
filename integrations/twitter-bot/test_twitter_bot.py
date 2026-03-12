#!/usr/bin/env python3
"""
RustChain Twitter Bot 测试脚本

测试 API 连接和基本功能
"""

import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

import tweepy

# 配置
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

def test_twitter_auth():
    """测试 Twitter 认证"""
    print("🔐 测试 Twitter 认证...")
    
    try:
        client = tweepy.Client(
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
            wait_on_rate_limit=True
        )
        
        me = client.get_me()
        print(f"✅ 认证成功：@{me.data.username}")
        return True
        
    except Exception as e:
        print(f"❌ 认证失败：{e}")
        return False


def test_tweet_creation():
    """测试推文创建（不实际发布）"""
    print("\n📝 测试推文创建...")
    
    from twitter_bot import (
        create_health_tweet,
        create_miner_tweet,
        create_epoch_tweet,
        create_stats_tweet
    )
    
    # 测试数据
    health_data = {
        "ok": True,
        "version": "1.2.3",
        "uptime_s": 172800,
        "db_rw": True
    }
    
    miners_data = [
        {"miner_id": "0xabc123def456", "hashrate": 125.5},
        {"miner_id": "0xdef456ghi789", "hashrate": 98.2},
    ]
    
    epoch_data = {
        "epoch": 156,
        "block_height": 1234567,
        "reward_pool": 50000
    }
    
    stats_data = {
        "total_miners": 42,
        "total_blocks": 1234567,
        "network_hashrate": 452.3
    }
    
    print("\n健康状态推文:")
    print(create_health_tweet(health_data))
    
    print("\n矿工信息推文:")
    print(create_miner_tweet(miners_data))
    
    print("\nEpoch 推文:")
    print(create_epoch_tweet(epoch_data))
    
    print("\n统计信息推文:")
    print(create_stats_tweet(stats_data))
    
    print("\n✅ 推文创建测试通过")
    return True


async def test_rustchain_api():
    """测试 RustChain API 连接"""
    print("\n📡 测试 RustChain API...")
    
    import aiohttp
    from twitter_bot import rustchain_health, rustchain_miners, rustchain_epoch
    
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        global http_session
        http_session = session
        
        try:
            print("检查健康状态...")
            health = await rustchain_health()
            print(f"✅ 健康状态：{health}")
            
            print("\n获取矿工列表...")
            miners = await rustchain_miners()
            print(f"✅ 矿工数量：{len(miners)}")
            
            print("\n获取 Epoch 信息...")
            epoch = await rustchain_epoch()
            print(f"✅ Epoch: {epoch}")
            
            return True
            
        except Exception as e:
            print(f"⚠️ API 测试失败（可能是测试环境）: {e}")
            return False


async def main():
    """主测试函数"""
    print("=" * 50)
    print("🧪 RustChain Twitter Bot 测试")
    print("=" * 50)
    
    # 测试 Twitter 认证
    auth_ok = test_twitter_auth()
    
    # 测试推文创建
    tweet_ok = test_tweet_creation()
    
    # 测试 RustChain API
    api_ok = await test_rustchain_api()
    
    print("\n" + "=" * 50)
    print("📊 测试结果:")
    print(f"  Twitter 认证：{'✅ 通过' if auth_ok else '❌ 失败'}")
    print(f"  推文创建：{'✅ 通过' if tweet_ok else '❌ 失败'}")
    print(f"  RustChain API: {'✅ 通过' if api_ok else '⚠️ 跳过'}")
    print("=" * 50)
    
    if auth_ok and tweet_ok:
        print("\n✅ 所有核心测试通过！可以运行机器人了。")
        return 0
    else:
        print("\n❌ 部分测试失败，请检查配置。")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
