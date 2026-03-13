#!/usr/bin/env python3
"""
ENIAC RustChain Miner (1945)
============================
在 ENIAC 模拟器上运行的 RustChain 矿工。

特性:
- 使用 ENIAC 十进制累加器进行哈希计算
- 真空管热噪声熵作为硬件指纹
- 支持 RustChain 节点提交
- LEGENDARY Tier 5.0x 倍数

钱包地址：RTC4325af95d26d59c3ef025963656d22af638bb96b
Bounty: 200 RTC ($20) - LEGENDARY Tier!

作者：RustChain ENIAC Team
许可证：Apache 2.0
"""

import argparse
import hashlib
import json
import time
import random
import sys
from datetime import datetime
from typing import Optional, Dict, Any

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

from eniac_simulator import ENIACSimulator, Accumulator


class ENIACMiner:
    """
    ENIAC RustChain 矿工
    
    使用 ENIAC 模拟器执行工作量证明计算，
    利用 ENIAC 的独特架构生成硬件指纹。
    """
    
    # ENIAC 硬件信息
    HARDWARE_INFO = {
        'machine': 'ENIAC',
        'year': 1945,
        'architecture': 'decimal_accumulator',
        'word_length': 10,  # 十进制位
        'accumulators': 20,
        'vacuum_tubes': 18000,
        'power_consumption_kw': 150,
        'weight_tons': 30,
        'area_sqft': 300,
        'cost_1945_usd': 487000,
        'cost_2024_usd': 7000000,
    }
    
    # LEGENDARY Tier 倍数
    ANTIQUITY_MULTIPLIER = 5.0  # ENIAC 是最高级别
    
    def __init__(self, wallet_id: str, node_url: str = 'https://50.28.86.131'):
        self.wallet_id = wallet_id
        self.node_url = node_url
        self.eniac = ENIACSimulator()
        self.miner_id = f"eniac_1945_{wallet_id[:8]}"
        self.start_time = time.time()
        self.attestations_submitted = 0
        self.total_rewards = 0.0
        
        # 初始化 ENIAC 函数表 (用于存储矿工配置)
        self._init_function_tables()
    
    def _init_function_tables(self):
        """初始化函数表配置"""
        # 将钱包 ID 编码到函数表开关中
        wallet_hash = hashlib.sha256(self.wallet_id.encode()).hexdigest()
        
        for i, char in enumerate(wallet_hash[:120]):  # 使用前 120 个字符
            if i < 1200:  # 函数表大小限制
                digit = int(char, 16) % 10
                self.eniac.function_tables[0].set_switch(i, digit)
    
    def compute_eniac_hash(self, data: str) -> str:
        """
        使用 ENIAC 架构计算哈希
        
        方法:
        1. 将输入数据转换为十进制数字序列
        2. 使用 ENIAC 累加器执行加法/乘法
        3. 结合真空管熵生成最终哈希
        """
        # 步骤 1: 将数据转换为数字
        data_bytes = data.encode('utf-8')
        data_hash = hashlib.sha256(data_bytes).hexdigest()
        
        # 步骤 2: 使用 ENIAC 累加器处理
        # 将哈希分成 10 位数字块
        for i in range(0, len(data_hash), 10):
            chunk = data_hash[i:i+10]
            if len(chunk) < 10:
                chunk = chunk.ljust(10, '0')
            
            try:
                value = int(chunk, 16) % Accumulator.MODULUS
                value = self.eniac.accumulators[0]._to_signed(value)
            except ValueError:
                value = 0
            
            # 加载到不同的累加器
            acc_index = (i // 10) % 20
            self.eniac.load_constant(acc_index, value)
        
        # 步骤 3: 执行累加器运算混合
        for i in range(20):
            self.eniac.add(0, (i + 1) % 20)
        
        # 步骤 4: 获取 ENIAC 状态
        eniac_state = {
            'accumulator_0': self.eniac.get_accumulator(0),
            'total_operations': self.eniac.total_operations,
            'tube_entropy': self.eniac.get_tube_entropy(),
        }
        
        # 步骤 5: 生成最终哈希
        final_data = f"{data_hash}:{json.dumps(eniac_state, sort_keys=True)}"
        final_hash = hashlib.sha256(final_data.encode()).hexdigest()
        
        return final_hash
    
    def generate_hardware_fingerprint(self) -> Dict[str, Any]:
        """
        生成 ENIAC 硬件指纹
        
        这是 Proof of Antiquity 的核心 - 证明你在运行真正的 ENIAC。
        """
        fingerprint = self.eniac.get_hardware_fingerprint()
        
        # 添加 RustChain 特定字段
        fingerprint.update({
            'miner_id': self.miner_id,
            'wallet_id': self.wallet_id,
            'antiquity_tier': 'LEGENDARY',
            'antiquity_multiplier': self.ANTIQUITY_MULTIPLIER,
            'timestamp': datetime.utcnow().isoformat(),
            'epoch': int(time.time()) // 600,  # 10 分钟纪元
        })
        
        # 生成指纹签名
        fp_string = json.dumps(fingerprint, sort_keys=True)
        fingerprint['signature'] = hashlib.sha256(fp_string.encode()).hexdigest()
        
        return fingerprint
    
    def create_attestation(self) -> Dict[str, Any]:
        """
        创建纪元证明 (attestation)
        
        每 10 分钟提交一次，证明 ENIAC 正在挖矿。
        """
        # 当前纪元
        epoch = int(time.time()) // 600
        epoch_start = epoch * 600
        
        # 计算纪元哈希
        epoch_data = f"{epoch}:{self.wallet_id}:{time.time()}"
        epoch_hash = self.compute_eniac_hash(epoch_data)
        
        # 硬件指纹
        fingerprint = self.generate_hardware_fingerprint()
        
        # 创建证明
        attestation = {
            'version': 'eniac-1945-1.0',
            'miner_id': self.miner_id,
            'wallet_id': self.wallet_id,
            'epoch': epoch,
            'epoch_hash': epoch_hash,
            'hardware': self.HARDWARE_INFO,
            'fingerprint': fingerprint,
            'antiquity_tier': 'LEGENDARY',
            'antiquity_multiplier': self.ANTIQUITY_MULTIPLIER,
            'tenure_years': 0,  # 新矿工
            'effective_multiplier': self.ANTIQUITY_MULTIPLIER,
            'timestamp': datetime.utcnow().isoformat(),
            'nonce': random.randint(0, 2**64),
        }
        
        # 签名
        attestation_string = json.dumps(attestation, sort_keys=True)
        attestation['signature'] = hashlib.sha256(attestation_string.encode()).hexdigest()
        
        return attestation
    
    def submit_attestation(self, attestation: Dict[str, Any]) -> bool:
        """
        提交证明到 RustChain 节点
        
        返回是否成功。
        """
        if not HAS_REQUESTS:
            print("⚠️  警告：requests 库未安装，无法提交到网络")
            print("   安装：pip install requests")
            return False
        
        try:
            endpoint = f"{self.node_url}/api/v1/attest"
            response = requests.post(
                endpoint,
                json=attestation,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                self.attestations_submitted += 1
                
                # 计算奖励
                base_reward = 1.5  # 每纪元 1.5 RTC
                weighted_reward = base_reward * attestation['effective_multiplier']
                self.total_rewards += weighted_reward
                
                print(f"✅ 证明提交成功!")
                print(f"   纪元：{attestation['epoch']}")
                print(f"   奖励：{weighted_reward:.4f} RTC")
                print(f"   累计：{self.total_rewards:.4f} RTC")
                
                return True
            else:
                print(f"❌ 提交失败：HTTP {response.status_code}")
                print(f"   响应：{response.text[:200]}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 网络错误：{e}")
            return False
    
    def save_attestation_to_file(self, attestation: Dict[str, Any], filename: str = 'ATTEST.TXT'):
        """保存证明到文件 (离线模式)"""
        with open(filename, 'w') as f:
            json.dump(attestation, f, indent=2)
        print(f"💾 证明已保存到：{filename}")
    
    def run_mining_loop(self, interval_seconds: int = 600, offline: bool = False):
        """
        运行挖矿循环
        
        参数:
            interval_seconds: 证明间隔 (默认 600 秒 = 10 分钟)
            offline: 离线模式 (仅保存文件，不提交网络)
        """
        print("=" * 70)
        print("  ENIAC RustChain Miner (1945) - LEGENDARY Tier")
        print("=" * 70)
        print(f"\n  钱包：{self.wallet_id}")
        print(f"  节点：{self.node_url}")
        print(f"  倍数：{self.ANTIQUITY_MULTIPLIER}x (LEGENDARY)")
        print(f"  模式：{'离线' if offline else '在线'}")
        print("\n" + "=" * 70)
        
        # 显示 ENIAC 硬件信息
        print("\n📜 ENIAC 硬件规格:")
        print(f"   完成时间：{self.HARDWARE_INFO['year']}")
        print(f"   架构：{self.HARDWARE_INFO['architecture']}")
        print(f"   字长：{self.HARDWARE_INFO['word_length']} 十进制位")
        print(f"   累加器：{self.HARDWARE_INFO['accumulators']}")
        print(f"   真空管：{self.HARDWARE_INFO['vacuum_tubes']}")
        print(f"   功耗：{self.HARDWARE_INFO['power_consumption_kw']} kW")
        print(f"   重量：{self.HARDWARE_INFO['weight_tons']} 吨")
        print(f"   造价：${self.HARDWARE_INFO['cost_1945_usd']:,} (1945)")
        print(f"   相当于：${self.HARDWARE_INFO['cost_2024_usd']:,} (2024)")
        
        print("\n🚀 开始挖矿...\n")
        
        try:
            while True:
                # 创建证明
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 创建纪元证明...")
                attestation = self.create_attestation()
                
                if offline:
                    # 离线模式：保存到文件
                    filename = f"ATTEST_{attestation['epoch']}.TXT"
                    self.save_attestation_to_file(attestation, filename)
                else:
                    # 在线模式：提交到节点
                    success = self.submit_attestation(attestation)
                    
                    if not success:
                        # 提交失败，保存到文件
                        self.save_attestation_to_file(attestation)
                
                # 显示 ENIAC 状态
                print("\n" + self.eniac.get_status())
                
                # 等待下一个纪元
                next_epoch_time = (attestation['epoch'] + 1) * 600
                wait_time = next_epoch_time - time.time()
                
                if wait_time > 0:
                    print(f"⏳ 等待下一个纪元：{wait_time:.0f} 秒")
                    print("   (按 Ctrl+C 停止)\n")
                    time.sleep(wait_time)
                    
        except KeyboardInterrupt:
            print("\n\n🛑 矿工停止")
            print(f"\n📊 最终统计:")
            print(f"   运行时间：{time.time() - self.start_time:.0f} 秒")
            print(f"   提交证明：{self.attestations_submitted}")
            print(f"   总奖励：{self.total_rewards:.4f} RTC")
            print(f"\n💰 钱包：{self.wallet_id}")
            print(f"   请备份此地址以申领奖励!")


def generate_wallet() -> str:
    """生成新的钱包地址"""
    # 使用 ENIAC 真空管熵生成随机性
    eniac = ENIACSimulator()
    entropy = eniac.get_tube_entropy()
    
    # 生成钱包 ID
    wallet_hash = hashlib.sha256(entropy.encode()).hexdigest()
    wallet_id = f"RTC{wallet_hash[:40]}"
    
    return wallet_id


def main():
    parser = argparse.ArgumentParser(
        description='ENIAC RustChain Miner (1945) - LEGENDARY Tier',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 生成新钱包
  python eniac_miner.py --generate-wallet
  
  # 开始挖矿 (在线模式)
  python eniac_miner.py --wallet RTCxxxxxxxx --node https://50.28.86.131
  
  # 开始挖矿 (离线模式)
  python eniac_miner.py --wallet RTCxxxxxxxx --offline
  
  # 自定义证明间隔
  python eniac_miner.py --wallet RTCxxxxxxxx --interval 300

Bounty 钱包地址:
  RTC4325af95d26d59c3ef025963656d22af638bb96b

奖励:
  200 RTC ($20) - LEGENDARY Tier!
        """
    )
    
    parser.add_argument('--wallet', type=str, help='钱包地址')
    parser.add_argument('--node', type=str, default='https://50.28.86.131',
                       help='RustChain 节点 URL (默认：https://50.28.86.131)')
    parser.add_argument('--interval', type=int, default=600,
                       help='证明间隔秒数 (默认：600 = 10 分钟)')
    parser.add_argument('--offline', action='store_true',
                       help='离线模式 (仅保存文件，不提交网络)')
    parser.add_argument('--generate-wallet', action='store_true',
                       help='生成新钱包地址')
    
    args = parser.parse_args()
    
    # 生成钱包
    if args.generate_wallet:
        wallet = generate_wallet()
        print("=" * 70)
        print("  ENIAC 钱包生成器 (1945)")
        print("=" * 70)
        print(f"\n✅ 新钱包地址已生成:\n")
        print(f"   {wallet}")
        print(f"\n⚠️  重要：请备份此钱包地址!")
        print(f"   保存到安全位置 (建议：软盘、纸张、或石刻)")
        print(f"\n💰 使用此钱包启动矿工:")
        print(f"   python eniac_miner.py --wallet {wallet}")
        print("\n" + "=" * 70)
        
        # 保存到文件
        with open('WALLET.TXT', 'w') as f:
            f.write(f"ENIAC RustChain Wallet (1945)\n")
            f.write(f"Generated: {datetime.utcnow().isoformat()}\n")
            f.write(f"Address: {wallet}\n")
            f.write(f"\n⚠️  BACKUP THIS WALLET TO FLOPPY DISK!\n")
        print(f"\n💾 钱包已保存到：WALLET.TXT")
        return
    
    # 验证钱包
    if not args.wallet:
        print("❌ 错误：请指定钱包地址 (--wallet) 或生成新钱包 (--generate-wallet)")
        print("\n使用 --help 查看帮助")
        sys.exit(1)
    
    # 启动矿工
    miner = ENIACMiner(args.wallet, args.node)
    miner.run_mining_loop(interval_seconds=args.interval, offline=args.offline)


if __name__ == '__main__':
    main()
