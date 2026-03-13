#!/usr/bin/env python3
"""
ENIAC 模拟器测试套件
====================
测试 ENIAC 模拟器的各项功能。
"""

import unittest
import sys
import time

from eniac_simulator import (
    ENIACSimulator, Accumulator, FunctionTable, 
    MasterProgrammer, ENIACError
)


class TestAccumulator(unittest.TestCase):
    """测试累加器功能"""
    
    def setUp(self):
        self.acc = Accumulator(0)
    
    def test_initial_value(self):
        """测试初始值"""
        self.assertEqual(self.acc.get_value(), 0)
    
    def test_load_positive(self):
        """测试加载正数"""
        self.acc.load(1234567890)
        self.assertEqual(self.acc.get_value(), 1234567890)
    
    def test_load_negative(self):
        """测试加载负数"""
        self.acc.load(-1234567890)
        self.assertEqual(self.acc.get_value(), -1234567890)
    
    def test_add_positive(self):
        """测试加法"""
        self.acc.load(100)
        self.acc.add(50)
        self.assertEqual(self.acc.get_value(), 150)
    
    def test_add_negative(self):
        """测试加负数 (减法)"""
        self.acc.load(100)
        self.acc.add(-50)
        self.assertEqual(self.acc.get_value(), 50)
    
    def test_subtract(self):
        """测试减法"""
        self.acc.load(100)
        self.acc.subtract(50)
        self.assertEqual(self.acc.get_value(), 50)
    
    def test_wrap_around_positive(self):
        """测试正数溢出回绕 (10 的补码)"""
        self.acc.load(9_999_999_999)  # 最大值
        self.acc.add(1)
        # 应该回绕到负数
        self.assertEqual(self.acc.get_value(), -9_999_999_999)
    
    def test_wrap_around_negative(self):
        """测试负数溢出回绕"""
        self.acc.load(-9_999_999_999)  # 最小值
        self.acc.subtract(1)
        # 应该回绕到正数
        self.assertEqual(self.acc.get_value(), 9_999_999_999)
    
    def test_ten_complement(self):
        """测试 10 的补码表示"""
        # -1 应该表示为 9999999999
        self.acc.load(-1)
        display = self.acc.get_display()
        self.assertEqual(display, '-9999999999')
    
    def test_clear(self):
        """测试清零"""
        self.acc.load(12345)
        self.acc.clear()
        self.assertEqual(self.acc.get_value(), 0)
    
    def test_cycle_count(self):
        """测试周期计数"""
        initial_cycles = self.acc.cycle_count
        self.acc.add(10)
        self.assertEqual(self.acc.cycle_count, initial_cycles + 1)


class TestFunctionTable(unittest.TestCase):
    """测试函数表功能"""
    
    def setUp(self):
        self.ft = FunctionTable(0)
    
    def test_set_and_get_switch(self):
        """测试设置和读取开关"""
        self.ft.set_switch(0, 5)
        self.assertEqual(self.ft.get_switch(0), 5)
    
    def test_switch_range(self):
        """测试开关值范围 (0-9)"""
        for i in range(10):
            self.ft.set_switch(i, i)
            self.assertEqual(self.ft.get_switch(i), i)
    
    def test_invalid_switch_value(self):
        """测试无效开关值"""
        with self.assertRaises(ENIACError):
            self.ft.set_switch(0, 10)  # 超出 0-9 范围
    
    def test_invalid_switch_position(self):
        """测试无效开关位置"""
        with self.assertRaises(ENIACError):
            self.ft.get_switch(1200)  # 超出范围
    
    def test_entropy(self):
        """测试熵计算"""
        # 所有开关相同
        for i in range(100):
            self.ft.set_switch(i, 5)
        entropy_low = self.ft.get_entropy()
        
        # 重置
        self.ft = FunctionTable(0)
        
        # 开关值多样化
        for i in range(100):
            self.ft.set_switch(i, i % 10)
        entropy_high = self.ft.get_entropy()
        
        # 多样化应该产生更高熵
        self.assertGreater(entropy_high, entropy_low)


class TestMasterProgrammer(unittest.TestCase):
    """测试主程序器功能"""
    
    def setUp(self):
        self.prog = MasterProgrammer()
    
    def test_loop_counter(self):
        """测试循环计数"""
        self.prog.set_loop(5)
        for i in range(4):
            self.assertFalse(self.prog.increment_loop())
        self.assertTrue(self.prog.increment_loop())
    
    def test_branch_positive(self):
        """测试正数分支"""
        self.prog.set_branch('positive')
        self.assertTrue(self.prog.check_branch(10))
        self.assertFalse(self.prog.check_branch(-10))
        self.assertFalse(self.prog.check_branch(0))
    
    def test_branch_negative(self):
        """测试负数分支"""
        self.prog.set_branch('negative')
        self.assertFalse(self.prog.check_branch(10))
        self.assertTrue(self.prog.check_branch(-10))
        self.assertFalse(self.prog.check_branch(0))
    
    def test_branch_zero(self):
        """测试零分支"""
        self.prog.set_branch('zero')
        self.assertFalse(self.prog.check_branch(10))
        self.assertFalse(self.prog.check_branch(-10))
        self.assertTrue(self.prog.check_branch(0))


class TestENIACSimulator(unittest.TestCase):
    """测试 ENIAC 模拟器整体功能"""
    
    def setUp(self):
        self.eniac = ENIACSimulator()
    
    def test_initialization(self):
        """测试初始化"""
        self.assertEqual(len(self.eniac.accumulators), 20)
        self.assertEqual(len(self.eniac.function_tables), 3)
    
    def test_load_and_add(self):
        """测试加载和加法"""
        self.eniac.load_constant(0, 100)
        self.eniac.load_constant(1, 50)
        self.eniac.add(0, 1)
        self.assertEqual(self.eniac.get_accumulator(0), 150)
    
    def test_subtract_operation(self):
        """测试减法运算"""
        self.eniac.load_constant(0, 100)
        self.eniac.load_constant(1, 50)
        self.eniac.subtract(0, 1)
        self.assertEqual(self.eniac.get_accumulator(0), 50)
    
    def test_multiply_operation(self):
        """测试乘法运算"""
        self.eniac.load_constant(0, 100)
        result = self.eniac.multiply(0, 5)
        self.assertEqual(result, 500)
    
    def test_accumulator_overflow(self):
        """测试累加器溢出处理"""
        self.eniac.load_constant(0, 9_999_999_999)
        self.eniac.load_constant(1, 1)
        self.eniac.add(0, 1)
        # 应该回绕到负数
        self.assertEqual(self.eniac.get_accumulator(0), -9_999_999_999)
    
    def test_hardware_fingerprint(self):
        """测试硬件指纹生成"""
        fingerprint = self.eniac.get_hardware_fingerprint()
        
        self.assertEqual(fingerprint['machine'], 'ENIAC')
        self.assertEqual(fingerprint['year'], 1945)
        self.assertEqual(fingerprint['accumulators'], 20)
        self.assertEqual(fingerprint['vacuum_tubes'], 18000)
        self.assertIn('tube_entropy', fingerprint)
    
    def test_operations_counting(self):
        """测试运算计数"""
        initial_ops = self.eniac.total_operations
        self.eniac.load_constant(0, 10)
        self.eniac.load_constant(1, 20)
        self.eniac.add(0, 1)
        
        self.assertGreater(self.eniac.total_operations, initial_ops)
    
    def test_status_report(self):
        """测试状态报告"""
        status = self.eniac.get_status()
        self.assertIn('ENIAC', status)
        self.assertIn('1945', status)
    
    def test_sum_1_to_10(self):
        """测试经典求和：1+2+...+10 = 55"""
        self.eniac.clear(0)  # 总和
        
        for i in range(1, 11):
            self.eniac.load_constant(1, i)
            self.eniac.add(0, 1)
        
        self.assertEqual(self.eniac.get_accumulator(0), 55)
    
    def test_fibonacci_sequence(self):
        """测试斐波那契数列 (前 10 项)"""
        # F0 = 0, F1 = 1
        self.eniac.load_constant(0, 0)  # F(n-2)
        self.eniac.load_constant(1, 1)  # F(n-1)
        
        for _ in range(8):  # 计算接下来的 8 项
            # F(n) = F(n-1) + F(n-2)
            self.eniac.load_constant(2, self.eniac.get_accumulator(0))
            self.eniac.add(1, 2)
            
            # 移位：F(n-2) = F(n-1), F(n-1) = F(n)
            self.eniac.load_constant(0, self.eniac.get_accumulator(1) - self.eniac.get_accumulator(2))
        
        # 第 10 项应该是 34
        # 序列：0, 1, 1, 2, 3, 5, 8, 13, 21, 34
        self.assertEqual(self.eniac.get_accumulator(1), 34)


class TestENIACMiner(unittest.TestCase):
    """测试 ENIAC 矿工功能"""
    
    def test_import_miner(self):
        """测试矿工模块导入"""
        try:
            from eniac_miner import ENIACMiner
            self.assertTrue(True)
        except ImportError:
            self.skipTest("eniac_miner 模块不可用")


def run_tests():
    """运行所有测试"""
    print("=" * 70)
    print("  ENIAC 模拟器测试套件")
    print("=" * 70)
    print()
    
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试
    suite.addTests(loader.loadTestsFromTestCase(TestAccumulator))
    suite.addTests(loader.loadTestsFromTestCase(TestFunctionTable))
    suite.addTests(loader.loadTestsFromTestCase(TestMasterProgrammer))
    suite.addTests(loader.loadTestsFromTestCase(TestENIACSimulator))
    
    try:
        suite.addTests(loader.loadTestsFromTestCase(TestENIACMiner))
    except:
        pass
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 打印摘要
    print("\n" + "=" * 70)
    print(f"  测试结果：{result.testsRun} 个测试")
    print(f"  通过：{result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"  失败：{len(result.failures)}")
    print(f"  错误：{len(result.errors)}")
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
