# EDSAC 2 架构参考手册

## 概述

EDSAC 2 (Electronic Delay Storage Automatic Calculator 2) 是由剑桥大学数学实验室于 1958 年开发的早期真空管计算机。它是 EDSAC (1949) 的继任者，具有多项开创性创新。

## 历史意义

### 第一台微程序化计算机

EDSAC 2 是世界上第一台采用**微程序控制单元**的计算机。这一概念由 Maurice Wilkes 提出，后来被 IBM System/360 等计算机广泛采用。

### 位片式架构

EDSAC 2 采用**位片式** (bit-sliced) 硬件架构，使用可互换的插件单元。这种模块化设计简化了制造和维护。

### 磁芯内存

EDSAC 2 用**磁芯内存**取代了 EDSAC 1 的水银延迟线，提供了更快、更可靠的存储。

## 技术规格

### CPU 架构

| 特性 | 规格 |
|------|------|
| 字长 | 40 位 |
| 指令长度 | 20 位 |
| 地址长度 | 11 位 |
| 索引寄存器 | 2 个 (B1, B2) |
| 累加器 | 40 位 |
| 时钟频率 | ~500 kHz (估计) |
| 技术 | 真空管 |

### 内存系统

| 特性 | 规格 |
|------|------|
| RAM | 1024 字 (40 位/字) |
| ROM | 768 字 (微程序存储) |
| 内存技术 | 磁芯内存 (32×32 铁氧体环) |
| 访问时间 | ~17-42 μs (定点加法) |
| 特性 | 非易失性，破坏性读取 |

### 性能

| 操作 | 时间 |
|------|------|
| 定点加法 | 17-42 μs |
| 浮点加法 | 100-170 μs |
| 乘法 | ~200 μs (微程序) |
| 除法 | ~300 μs (微程序) |

## 指令集架构

### 指令格式

```
┌─────────┬─────┬───────────┬──────┐
│ 操作码  │ 索引│ 地址      │ 长度 │
│ 5 位    │ 2 位 │ 11 位     │ 2 位 │
│ bits 0-4│5-6  │ bits 7-17 │18-19 │
└─────────┴─────┴───────────┴──────┘
```

- **操作码 (Opcode)**: 5 位，定义操作类型 (0-31)
- **索引 (Index)**: 2 位，选择索引寄存器
  - `00` = 无索引
  - `01` = B1
  - `10` = B2
  - `11` = 保留
- **地址 (Address)**: 11 位，内存地址 (0-2047)
- **长度 (Length)**: 2 位，操作数长度
  - `01` = 单字 (40 位)
  - `10` = 双字 (80 位)

### 指令编码

指令字编码为 40 位字的高 20 位：

```python
def encode_instruction(opcode, index, address, length):
    word = 0
    word |= (opcode & 0x1F) << 35    # 操作码在 bits 35-39
    word |= (index & 0x03) << 33     # 索引在 bits 33-34
    word |= (address & 0x7FF) << 22  # 地址在 bits 22-32
    word |= (length & 0x03) << 20    # 长度在 bits 20-21
    return word
```

### 指令集详解

#### 数据传输指令

| 操作码 | 助记符 | 描述 | 周期 |
|--------|--------|------|------|
| 0x0D | LD | 加载：ACC ← MEM[addr] | 25 |
| 0x0E | ST | 存储：MEM[addr] ← ACC | 25 |
| 0x11 | IDX1 | 加载索引 B1：B1 ← MEM[addr] | 25 |
| 0x12 | IDX2 | 加载索引 B2：B2 ← MEM[addr] | 25 |

#### 算术指令

| 操作码 | 助记符 | 描述 | 周期 |
|--------|--------|------|------|
| 0x01 | ADD | 加法：ACC ← ACC + MEM[addr] | 42 |
| 0x02 | SUB | 减法：ACC ← ACC - MEM[addr] | 42 |
| 0x03 | MUL | 乘法：ACC ← ACC × MEM[addr] | 200 |
| 0x04 | DIV | 除法：ACC ← ACC ÷ MEM[addr] | 300 |

#### 逻辑指令

| 操作码 | 助记符 | 描述 | 周期 |
|--------|--------|------|------|
| 0x05 | AND | 按位与：ACC ← ACC & MEM[addr] | 17 |
| 0x06 | OR | 按位或：ACC ← ACC \| MEM[addr] | 17 |
| 0x07 | XOR | 按位异或：ACC ← ACC ^ MEM[addr] | 17 |

#### 移位指令

| 操作码 | 助记符 | 描述 | 周期 |
|--------|--------|------|------|
| 0x08 | SHL | 左移：ACC ← ACC << addr | 17 |
| 0x09 | SHR | 右移：ACC ← ACC >> addr (算术) | 17 |

#### 控制流指令

| 操作码 | 助记符 | 描述 | 周期 |
|--------|--------|------|------|
| 0x00 | STOP | 停止执行 | - |
| 0x0A | JMP | 无条件跳转：PC ← addr | 25 |
| 0x0B | JZ | 零时跳转：if Z then PC ← addr | 25 |
| 0x0C | JN | 负时跳转：if N then PC ← addr | 25 |

#### I/O 指令

| 操作码 | 助记符 | 描述 | 周期 |
|--------|--------|------|------|
| 0x0F | IN | 输入：ACC ← 纸带 | 50 |
| 0x10 | OUT | 输出：纸带 ← ACC | 50 |

### 寻址模式

#### 直接寻址

```assembly
LD  0x100    ; 从地址 0x100 加载
```

#### 索引寻址

```assembly
LD  0x100,B1  ; 从地址 0x100 + B1 加载
LD  0x100,B2  ; 从地址 0x100 + B2 加载
```

有效地址计算：
```python
effective_address = (base_address + index_register) & 0x7FF
```

## 寄存器

### 用户可见寄存器

| 寄存器 | 宽度 | 描述 |
|--------|------|------|
| ACC | 40 位 | 累加器 - 主要计算寄存器 |
| B1 | 40 位 | 索引寄存器 1 |
| B2 | 40 位 | 索引寄存器 2 |
| PC | 11 位 | 程序计数器 |

### 状态标志

| 标志 | 描述 | 设置条件 |
|------|------|----------|
| Z (Zero) | 零标志 | ACC = 0 |
| N (Negative) | 负标志 | ACC[39] = 1 |
| V (Overflow) | 溢出标志 | 算术溢出 |

## 内存布局

### 物理内存

```
地址范围      大小        类型        用途
0x000-0x3FF   1024 字     RAM         主内存
0x400-0x6FF   768 字      ROM         微程序存储
```

### 推荐软件布局

```
地址范围      用途                  大小
0x000-0x01F   引导加载程序          32 字
0x020-0x05F   常量表                64 字
0x060-0x09F   全局变量              64 字
0x0A0-0x0FF   I/O 缓冲区            96 字
0x100-0x2FF   程序代码              512 字
0x300-0x3FF   栈和临时存储          256 字
```

## I/O 系统

### 纸带阅读器

- **类型**: 5 级纸带
- **速度**: 最高 1000 字符/秒
- **格式**: ASCII 或二进制
- **接口**: 并行输入到输入缓冲区

### 纸带穿孔机

- **类型**: 5 级纸带
- **速度**: 最高 300 字符/秒
- **格式**: ASCII 或二进制
- **接口**: 并行输出从输出缓冲区

### I/O 协议

```
输入协议:
1. 纸带阅读器读取字符
2. 字符存入输入缓冲区
3. IN 指令从缓冲区加载到 ACC

输出协议:
1. OUT 指令将 ACC 低 8 位存入输出缓冲区
2. 穿孔机从缓冲区读取并穿孔
```

## 微程序设计

### 微指令格式

EDSAC 2 的微指令存储在 ROM 中，控制 CPU 操作：

```
┌──────────┬─────────┬──────────┬─────────┐
│ 控制字段 │ ALU 操作 │ 内存控制 │ 下一地址 │
│ 8 位     │ 4 位    │ 4 位     │ 10 位    │
└──────────┴─────────┴──────────┴─────────┘
```

### 微程序示例

ADD 指令的微程序：

```
微地址  控制信号              描述
0x000   FETCH                 取指令
0x010   DECODE                译码
0x020   READ_MEM              读取操作数
0x030   ALU_ADD               执行加法
0x040   UPDATE_FLAGS          更新标志
0x050   NEXT_INSTR            下一条指令
```

## 编程示例

### 示例 1: 两数相加

```assembly
; 将地址 0x100 和 0x101 的值相加，结果存入 0x102

        LD   0x100      ; 加载第一个数
        ADD  0x101      ; 加第二个数
        ST   0x102      ; 存储结果
        STOP            ; 停止

; 数据
0x100:  10              ; 第一个数
0x101:  20              ; 第二个数
0x102:  0               ; 结果位置
```

### 示例 2: 循环计数

```assembly
; 从 10 倒数到 0

START:  LD   COUNT      ; 加载计数器
        JZ   DONE       ; 如果为零，完成
        OUT             ; 输出当前值
        SUB  ONE        ; 减 1
        ST   COUNT      ; 存储计数器
        JMP  START      ; 循环

DONE:   STOP            ; 完成

COUNT:  10
ONE:    1
```

### 示例 3: 使用索引寄存器

```assembly
; 对数组求和 (10 个元素)

        LD   ZERO       ; 初始化 sum = 0
        ST   SUM
        LD   ZERO       ; 初始化 index = 0
        ST   B1         ; 存入索引寄存器

LOOP:   LD   B1         ; 加载索引
        SUB  TEN        ; 检查是否 < 10
        JN   DONE       ; 如果 >= 10，完成
        
        LD   ARRAY,B1   ; 加载 array[index]
        ADD  SUM        ; 加到 sum
        ST   SUM        ; 存储 sum
        
        LD   B1         ; 索引++
        ADD  ONE
        ST   B1
        JMP  LOOP       ; 继续

DONE:   LD   SUM        ; 加载结果
        OUT             ; 输出
        STOP

ARRAY:  1, 2, 3, 4, 5, 6, 7, 8, 9, 10
SUM:    0
ZERO:   0
ONE:    1
TEN:    10
```

## 性能优化

### 1. 使用索引寄存器

索引寻址可以减少指令数量：

```assembly
; 低效：直接寻址
LD   0x200
ADD  0x201
ADD  0x202
ADD  0x203

; 高效：索引寻址
LD   ZERO
ST   B1
LD   0x200,B1
ADD  0x201,B1
ADD  0x202,B1
ADD  0x203,B1
```

### 2. 减少内存访问

内存访问较慢，尽量使用寄存器：

```assembly
; 低效：多次内存访问
LD   0x100
ADD  0x101
ST   0x102
LD   0x102
ADD  0x103
ST   0x102

; 高效：使用累加器
LD   0x100
ADD  0x101
ADD  0x103
ST   0x102
```

### 3. 循环展开

对于小循环，展开可以减少分支开销：

```assembly
; 原始循环
LD   ZERO
ST   SUM
; ... 循环 10 次 ...

; 展开版本
LD   0x200
ADD  0x201
ADD  0x202
ADD  0x203
ADD  0x204
ADD  0x205
ADD  0x206
ADD  0x207
ADD  0x208
ADD  0x209
ST   SUM
```

## 调试技术

### 1. 内存转储

```assembly
; 转储内存区域 0x100-0x10F
DUMP:   LD   0x100
        OUT
        LD   0x101
        OUT
        ; ... 继续 ...
        STOP
```

### 2. 断点

```assembly
; 在特定条件停止
LD   VALUE
SUB  EXPECTED
JZ   BREAKPOINT
; ... 继续执行 ...

BREAKPOINT: STOP  ; 调试断点
```

### 3. 单步执行

使用模拟器单步执行指令，观察寄存器和内存变化。

## 参考资料

1. Wilkes, M.V. (1992). "EDSAC 2". IEEE Annals of the History of Computing.
2. Wilkes, M.V., Wheeler, D.J., Gill, S. (1951). "The Preparation of Programs for an Electronic Digital Computer".
3. Computer Conservation Society. "EDSAC Replica Project".
4. The National Museum of Computing. "EDSAC 2 Collection".

---

**文档版本**: 1.0  
**最后更新**: 2026 年 3 月 14 日  
**作者**: RustChain EDSAC 2 Miner Project
