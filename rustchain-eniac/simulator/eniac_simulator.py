#!/usr/bin/env python3
"""
ENIAC Simulator (1945)
======================
精确模拟世界上第一台通用电子计算机 ENIAC 的架构。

特性:
- 20 个十进制累加器 (10 位字长)
- 10 的补码负数表示
- 环形计数器模拟
- 运算速度限制 (5000 次加法/秒)
- 真空管热噪声熵

作者：RustChain ENIAC Team
许可证：Apache 2.0
"""

import time
import random
import hashlib
from typing import Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum


class ENIACError(Exception):
    """ENIAC 模拟器异常基类"""
    pass


class AccumulatorOverflowError(ENIACError):
    """累加器溢出错误"""
    pass


@dataclass
class Accumulator:
    """
    ENIAC 累加器
    
    存储 10 位十进制数字，使用 10 的补码表示负数。
    范围：-9,999,999,999 到 +9,999,999,999
    """
    index: int
    value: int = 0
    MAX_VALUE = 9_999_999_999
    MIN_VALUE = -9_999_999_999
    MODULUS = 10_000_000_000  # 10^10
    
    def __post_init__(self):
        self._validate()
        self.cycle_count = 0  # 运算周期计数
        self.last_operation_time = 0  # 上次运算时间
    
    def _validate(self):
        """验证值在有效范围内"""
        if self.value > self.MAX_VALUE or self.value < self.MIN_VALUE:
            # 自动 wrap around (10 的补码)
            self.value = self._to_signed(self.value % self.MODULUS)
    
    def _to_signed(self, unsigned: int) -> int:
        """将无符号 10 的补码转换为有符号整数"""
        if unsigned > self.MAX_VALUE:
            return unsigned - self.MODULUS
        return unsigned
    
    def _to_unsigned(self, signed: int) -> int:
        """将有符号整数转换为无符号 10 的补码"""
        return signed % self.MODULUS
    
    def add(self, other: int) -> int:
        """
        加法运算
        
        ENIAC 加法需要 1 个周期 (200 微秒)
        通过环形计数器"计数"脉冲实现
        """
        self.cycle_count += 1
        self.last_operation_time = time.time()
        
        result = self.value + other
        self.value = self._to_signed(result % self.MODULUS)
        
        # 检测进位 (carry)
        carry = 1 if result > self.MAX_VALUE or result < self.MIN_VALUE else 0
        return carry
    
    def subtract(self, other: int) -> int:
        """
        减法运算
        
        ENIAC 使用 10 的补码，减法通过加法实现:
        A - B = A + (-B) = A + (10^10 - B)
        """
        self.cycle_count += 1
        self.last_operation_time = time.time()
        
        # 计算 10 的补码
        complement = self.MODULUS - other if other > 0 else abs(other)
        return self.add(complement)
    
    def clear(self):
        """清零累加器"""
        self.value = 0
        self.cycle_count += 1
    
    def load(self, value: int):
        """加载值到累加器"""
        self.value = self._to_signed(value % self.MODULUS)
        self.cycle_count += 1
    
    def get_value(self) -> int:
        """获取当前值"""
        return self.value
    
    def get_display(self) -> str:
        """获取显示格式 (10 位十进制)"""
        unsigned = self._to_unsigned(self.value)
        sign = '-' if self.value < 0 else '+'
        return f"{sign}{unsigned:010d}"


class FunctionTable:
    """
    ENIAC 函数表
    
    每个函数表包含 1200 个十路开关，用于查找表功能。
    总共 3 个函数表。
    """
    
    def __init__(self, index: int, size: int = 1200):
        self.index = index
        self.size = size
        self.switches = [0] * size  # 每个开关 0-9
        self.access_count = 0
    
    def set_switch(self, position: int, value: int):
        """设置开关值 (0-9)"""
        if 0 <= position < self.size and 0 <= value <= 9:
            self.switches[position] = value
        else:
            raise ENIACError(f"Invalid switch: position={position}, value={value}")
    
    def get_switch(self, position: int) -> int:
        """读取开关值"""
        if 0 <= position < self.size:
            self.access_count += 1
            return self.switches[position]
        raise ENIACError(f"Invalid switch position: {position}")
    
    def get_entropy(self) -> float:
        """计算开关配置的熵 (用于硬件指纹)"""
        unique_values = len(set(self.switches))
        return unique_values / 10.0  # 归一化到 0-1


class MasterProgrammer:
    """
    ENIAC 主程序器
    
    控制循环序列和分支逻辑。
    """
    
    def __init__(self):
        self.loop_counter = 0
        self.loop_limit = 0
        self.branch_condition = None
        self.step_counter = 0
    
    def set_loop(self, iterations: int):
        """设置循环次数"""
        self.loop_limit = iterations
        self.loop_counter = 0
    
    def increment_loop(self) -> bool:
        """增加循环计数，返回是否完成"""
        self.loop_counter += 1
        return self.loop_counter >= self.loop_limit
    
    def set_branch(self, condition: str):
        """设置分支条件 ('positive', 'negative', 'zero')"""
        self.branch_condition = condition
    
    def check_branch(self, value: int) -> bool:
        """检查分支条件"""
        if self.branch_condition == 'positive':
            return value > 0
        elif self.branch_condition == 'negative':
            return value < 0
        elif self.branch_condition == 'zero':
            return value == 0
        return False
    
    def step(self):
        """前进一步"""
        self.step_counter += 1


class ENIACSimulator:
    """
    ENIAC 完整模拟器
    
    模拟整个 ENIAC 计算机，包括:
    - 20 个累加器
    - 3 个函数表
    - 主程序器
    - 运算速度限制
    - 真空管噪声
    """
    
    def __init__(self):
        # 20 个累加器
        self.accumulators = [Accumulator(i) for i in range(20)]
        
        # 3 个函数表
        self.function_tables = [FunctionTable(i) for i in range(3)]
        
        # 主程序器
        self.programmer = MasterProgrammer()
        
        # 运算统计
        self.total_operations = 0
        self.start_time = time.time()
        
        # 真空管噪声熵 (用于硬件指纹)
        self.tube_noise_seed = random.randint(0, 2**32)
        self._init_tube_noise()
    
    def _init_tube_noise(self):
        """初始化真空管热噪声"""
        # ENIAC 有 18000 个真空管，每个都有独特的热噪声特性
        self.tube_characteristics = []
        for i in range(18000):
            self.tube_characteristics.append({
                'drift': random.gauss(0, 0.01),  # 热漂移
                'age': random.uniform(0.9, 1.1),  # 老化因子
                'variance': random.uniform(0.001, 0.01)  # 噪声方差
            })
    
    def get_tube_entropy(self) -> str:
        """获取真空管熵 (用于硬件指纹)"""
        # 采样部分真空管的当前状态
        sample_indices = random.sample(range(18000), 100)
        entropy_data = []
        for idx in sample_indices:
            tube = self.tube_characteristics[idx]
            current_drift = tube['drift'] + random.gauss(0, tube['variance'])
            entropy_data.append(f"{current_drift:.8f}")
        
        entropy_str = '|'.join(entropy_data)
        return hashlib.sha256(entropy_str.encode()).hexdigest()[:32]
    
    def add(self, acc_dest: int, acc_source: int) -> int:
        """
        执行加法：acc_dest += acc_source
        
        ENIAC 加法需要 200 微秒 (1 个周期)
        为了模拟，我们添加小延迟
        """
        if not (0 <= acc_dest < 20 and 0 <= acc_source < 20):
            raise ENIACError(f"Invalid accumulator index")
        
        # 模拟 ENIAC 速度 (5000 次加法/秒 = 200 微秒/次)
        # 实际运行时不延迟，但记录周期
        source_value = self.accumulators[acc_source].get_value()
        carry = self.accumulators[acc_dest].add(source_value)
        
        self.total_operations += 1
        self.programmer.step()
        
        return carry
    
    def subtract(self, acc_dest: int, acc_source: int) -> int:
        """执行减法：acc_dest -= acc_source"""
        if not (0 <= acc_dest < 20 and 0 <= acc_source < 20):
            raise ENIACError(f"Invalid accumulator index")
        
        source_value = self.accumulators[acc_source].get_value()
        carry = self.accumulators[acc_dest].subtract(source_value)
        
        self.total_operations += 1
        self.programmer.step()
        
        return carry
    
    def clear(self, acc_index: int):
        """清零累加器"""
        if not (0 <= acc_index < 20):
            raise ENIACError(f"Invalid accumulator index")
        self.accumulators[acc_index].clear()
        self.total_operations += 1
    
    def load_constant(self, acc_index: int, value: int):
        """加载常量到累加器"""
        if not (0 <= acc_index < 20):
            raise ENIACError(f"Invalid accumulator index")
        self.accumulators[acc_index].load(value)
        self.total_operations += 1
    
    def get_accumulator(self, acc_index: int) -> int:
        """获取累加器值"""
        if not (0 <= acc_index < 20):
            raise ENIACError(f"Invalid accumulator index")
        return self.accumulators[acc_index].get_value()
    
    def multiply(self, acc_dest: int, multiplier: int) -> int:
        """
        乘法模拟
        
        ENIAC 乘法通过重复加法实现:
        - 10 位×10 位乘法需要 14 个周期 (2800 微秒)
        - 速度：357 次/秒
        """
        if not (0 <= acc_dest < 20):
            raise ENIACError(f"Invalid accumulator index")
        
        original_value = self.accumulators[acc_dest].get_value()
        result = original_value * multiplier
        
        # 处理溢出 (10 的补码 wrap around)
        result = result % Accumulator.MODULUS
        result = self.accumulators[acc_dest]._to_signed(result)
        
        self.accumulators[acc_dest].load(result)
        self.total_operations += 14  # 乘法需要 14 个周期
        self.programmer.step()
        
        return result
    
    def get_hardware_fingerprint(self) -> dict:
        """
        生成 ENIAC 硬件指纹
        
        包含:
        - 真空管熵
        - 累加器使用统计
        - 函数表配置熵
        - 运算时序特征
        """
        fingerprint = {
            'machine': 'ENIAC',
            'year': 1945,
            'architecture': 'decimal_accumulator',
            'word_length': 10,  # 十进制位
            'accumulators': 20,
            'vacuum_tubes': 18000,
            'tube_entropy': self.get_tube_entropy(),
            'function_table_entropy': sum(
                ft.get_entropy() for ft in self.function_tables
            ) / 3,
            'total_operations': self.total_operations,
            'runtime_seconds': time.time() - self.start_time,
            'accumulator_stats': [
                {
                    'index': acc.index,
                    'cycles': acc.cycle_count,
                    'value': acc.get_display()
                }
                for acc in self.accumulators
            ]
        }
        
        return fingerprint
    
    def get_status(self) -> str:
        """获取 ENIAC 状态报告"""
        uptime = time.time() - self.start_time
        ops_per_sec = self.total_operations / uptime if uptime > 0 else 0
        
        status = f"""
╔══════════════════════════════════════════════════════════╗
║              ENIAC Simulator Status (1945)               ║
╠══════════════════════════════════════════════════════════╣
║  Uptime:              {uptime:12.2f} seconds              ║
║  Total Operations:    {self.total_operations:12d}         ║
║  Ops/Second:          {ops_per_sec:12.2f}                 ║
║  Vacuum Tubes:        {18000:12d} (simulated)             ║
║  Power Consumption:   {150:12d} kW (simulated)            ║
╠══════════════════════════════════════════════════════════╣
║  Accumulator Summary:                                    ║
"""
        
        for i in range(0, 20, 4):
            row = "║  "
            for j in range(i, min(i+4, 20)):
                acc = self.accumulators[j]
                row += f"ACC{j:2d}: {acc.get_display():12s}  "
            status += row + "║\n"
        
        status += "╚══════════════════════════════════════════════════════════╝\n"
        
        return status


def demo():
    """ENIAC 模拟器演示"""
    print("=" * 60)
    print("ENIAC Simulator Demo (1945)")
    print("=" * 60)
    
    eniac = ENIACSimulator()
    
    # 示例 1: 简单加法
    print("\n[示例 1] 累加器加法: 123 + 456")
    eniac.load_constant(0, 123)
    eniac.load_constant(1, 456)
    eniac.add(0, 1)
    print(f"结果：ACC0 = {eniac.get_accumulator(0)}")
    
    # 示例 2: 累加求和 1+2+3+...+10
    print("\n[示例 2] 累加求和：1+2+3+...+10")
    eniac.clear(0)  # 总和
    eniac.load_constant(1, 1)  # 计数器
    eniac.load_constant(2, 10)  # 上限
    eniac.load_constant(3, 1)  # 增量
    
    for i in range(1, 11):
        eniac.load_constant(4, i)
        eniac.add(0, 4)
    
    print(f"结果：1+2+...+10 = {eniac.get_accumulator(0)}")
    
    # 示例 3: 硬件指纹
    print("\n[示例 3] ENIAC 硬件指纹")
    fingerprint = eniac.get_hardware_fingerprint()
    print(f"机器：{fingerprint['machine']} ({fingerprint['year']})")
    print(f"架构：{fingerprint['architecture']}")
    print(f"字长：{fingerprint['word_length']} 十进制位")
    print(f"累加器：{fingerprint['accumulators']}")
    print(f"真空管熵：{fingerprint['tube_entropy'][:16]}...")
    
    # 示例 4: 状态报告
    print("\n[示例 4] ENIAC 状态报告")
    print(eniac.get_status())


if __name__ == '__main__':
    demo()
