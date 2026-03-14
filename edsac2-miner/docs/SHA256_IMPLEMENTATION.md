# EDSAC 2 SHA256 实现指南

## 概述

本文档描述如何在 EDSAC 2 (1958) 上实现 SHA256 哈希算法。这是 RustChain 矿工的核心组件。

## 挑战

### 1. 内存限制

EDSAC 2 只有 1024 字 (40 位/字) = 5120 字节内存。

SHA256 需要:
- 8 个哈希状态字 (H0-H7): 8 × 4 字节 = 32 字节
- 64 个轮常量 (K): 64 × 4 字节 = 256 字节
- 消息调度数组 (W): 64 × 4 字节 = 256 字节
- 工作变量 (a-h): 8 × 4 字节 = 32 字节
- 输入缓冲区：64 字节

**总计**: ~640 字节 (在 EDSAC 2 内存范围内！)

### 2. 字长不匹配

- EDSAC 2: 40 位字
- SHA256: 32 位字

解决方案：使用 40 位字的低 32 位，高位补零。

### 3. 算术操作

SHA256 需要:
- 32 位加法 (模 2^32)
- 右旋转 (ROTR)
- 右移位 (SHR)
- 按位操作 (AND, OR, XOR)

EDSAC 2 原生支持所有操作，但需要适配 40 位字长。

## SHA256 算法

### 常量

```python
# SHA256 轮常量 (前 32 位素数的小数部分)
K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

# 初始哈希值 (前 8 个素数的平方根小数部分)
H_INIT = [
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
]
```

### SHA256 函数

```python
def rotr(x, n):
    """32 位右旋转"""
    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

def shr(x, n):
    """32 位右移位"""
    return x >> n

def ch(x, y, z):
    """选择函数"""
    return (x & y) ^ (~x & z)

def maj(x, y, z):
    """多数函数"""
    return (x & y) ^ (x & z) ^ (y & z)

def sigma0(x):
    return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22)

def sigma1(x):
    return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25)

def gamma0(x):
    return rotr(x, 7) ^ rotr(x, 18) ^ shr(x, 3)

def gamma1(x):
    return rotr(x, 17) ^ rotr(x, 19) ^ shr(x, 10)
```

### 主循环

```python
def sha256(message):
    # 预处理
    padded = pad(message)
    blocks = split_into_512_bit_blocks(padded)
    
    # 初始化哈希值
    H = H_INIT.copy()
    
    # 处理每个块
    for block in blocks:
        # 准备消息调度数组
        W = message_schedule(block)
        
        # 初始化工作变量
        a, b, c, d, e, f, g, h = H
        
        # 64 轮
        for i in range(64):
            T1 = (h + sigma1(e) + ch(e, f, g) + K[i] + W[i]) & 0xFFFFFFFF
            T2 = (sigma0(a) + maj(a, b, c)) & 0xFFFFFFFF
            h = g
            g = f
            f = e
            e = (d + T1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (T1 + T2) & 0xFFFFFFFF
        
        # 更新哈希值
        H[0] = (H[0] + a) & 0xFFFFFFFF
        H[1] = (H[1] + b) & 0xFFFFFFFF
        H[2] = (H[2] + c) & 0xFFFFFFFF
        H[3] = (H[3] + d) & 0xFFFFFFFF
        H[4] = (H[4] + e) & 0xFFFFFFFF
        H[5] = (H[5] + f) & 0xFFFFFFFF
        H[6] = (H[6] + g) & 0xFFFFFFFF
        H[7] = (H[7] + h) & 0xFFFFFFFF
    
    # 输出
    return concat(H)
```

## EDSAC 2 实现

### 内存布局

```
地址范围      用途                  大小 (字)
0x000-0x01F   引导加载程序          32
0x020-0x05F   SHA256 常量 K         64
0x060-0x06F   哈希状态 H0-H7        16
0x070-0x0AF   消息调度 W[0..63]     64
0x0B0-0x0BF   工作变量 a-h          16
0x0C0-0x0DF   输入缓冲区            32
0x0E0-0x0FF   临时计算              32
0x100-0x1FF   子程序和栈            256
0x200-0x3FF   可用空间              512
```

### 汇编实现

#### 1. 右旋转 (ROTR)

```assembly
; ROTR32 - 32 位右旋转
; 输入：ACC = 值，ADDR = 旋转位数
; 输出：ACC = 旋转后的值

ROTR32:
    ST   TEMP        ; 保存原值
    LD   ADDR        ; 加载旋转位数
    SUB  THIRTYTWO   ; n = 32 - n
    ST   SHIFT_AMT
    LD   TEMP        ; 加载原值
    SHR  SHIFT_AMT   ; x >> (32-n)
    ST   PART1
    LD   TEMP
    SHL  ADDR        ; x << n
    OR   PART1       ; (x >> (32-n)) | (x << n)
    AND  MASK32      ; 保留低 32 位
    RETURN
```

#### 2. 选择函数 (CH)

```assembly
; CH - 选择函数：(x & y) ^ (~x & z)
; 输入：B1=x, B2=y, ACC=z
; 输出：ACC = CH(x,y,z)

CH_FUNC:
    ST   TEMP_Z
    LD   B1          ; x
    AND  B2          ; x & y
    ST   PART1
    LD   B1          ; x
    XOR  ALL_ONES    ; ~x
    AND  TEMP_Z      ; ~x & z
    XOR  PART1       ; (x & y) ^ (~x & z)
    RETURN
```

#### 3. 主循环

```assembly
; SHA256_COMPRESS - SHA256 压缩函数
; 输入：W[0..63] 在消息调度区
; 输出：H[0..7] 更新

SHA256_COMPRESS:
    ; 初始化工作变量
    LD   H0
    ST   A
    LD   H1
    ST   B
    LD   H2
    ST   C
    LD   H3
    ST   D
    LD   H4
    ST   E
    LD   H5
    ST   F
    LD   H6
    ST   G
    LD   H7
    ST   H
    
    ; 64 轮循环
    LD   ZERO
    ST   ROUND Counter
    
ROUND_LOOP:
    LD   ROUND_COUNTER
    SUB  SIXTYFOUR
    JZ   ROUND_DONE
    
    ; T1 = h + sigma1(e) + ch(e,f,g) + K[i] + W[i]
    LD   H
    CALL SIGMA1
    ST   T1
    LD   E
    ST   B1
    LD   F
    ST   B2
    LD   G
    CALL CH_FUNC
    ADD  T1
    LD   ROUND_COUNTER
    CALL GET_K       ; 加载 K[i]
    ADD  ACC
    LD   ROUND_COUNTER
    CALL GET_W       ; 加载 W[i]
    ADD  ACC
    ST   T1
    
    ; T2 = sigma0(a) + maj(a,b,c)
    LD   A
    CALL SIGMA0
    ST   T2
    LD   A
    ST   B1
    LD   B
    ST   B2
    LD   C
    CALL MAJ_FUNC
    ADD  T2
    
    ; h=g, g=f, f=e, e=d+T1, d=c, c=b, b=a, a=T1+T2
    LD   G
    ST   H
    LD   F
    ST   G
    LD   E
    ST   F
    LD   D
    ADD  T1
    ST   E
    LD   C
    ST   D
    LD   B
    ST   C
    LD   A
    ST   B
    LD   T1
    ADD  T2
    ST   A
    
    ; 循环
    LD   ROUND_COUNTER
    ADD  ONE
    ST   ROUND_COUNTER
    JMP  ROUND_LOOP

ROUND_DONE:
    ; 更新哈希值
    LD   H0
    ADD  A
    ST   H0
    LD   H1
    ADD  B
    ST   H1
    ; ... 类似更新 H2-H7
    
    RETURN
```

## 性能优化

### 1. 查找表

对于常量 K 和初始哈希值 H，使用 ROM 存储：

```assembly
; ROM 中的 K 常量表 (地址 0x020-0x05F)
K_TABLE:
    0x428a2f98
    0x71374491
    0xb5c0fbcf
    ...
```

### 2. 流水线

消息调度和压缩函数可以部分重叠：

```
时间 →
W[0..15]:  [====]
W[16..31]:      [====]
W[32..47]:          [====]
W[48..63]:              [====]
压缩：                      [========]
```

### 3. 寄存器分配

```
寄存器  用途
ACC     累加器 (主要计算)
B1      工作变量 a
B2      工作变量 b
TEMP1   工作变量 c
TEMP2   工作变量 d
TEMP3   工作变量 e
TEMP4   工作变量 f
TEMP5   工作变量 g
TEMP6   工作变量 h
```

## 测试向量

### NIST SHA256 测试向量

```
输入："abc"
输出：ba7816bf 8f01cfea 414140de 5dae2223 b00361a3 96177a9c b410ff61 f20015ad

输入："abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"
输出：248d6a61 d20638b8 e5c02693 0c3e6039 a33ce459 64ff2167 f6ecedd4 19db06c1
```

### EDSAC 2 测试程序

```assembly
; 测试 SHA256 实现
TEST_SHA256:
    ; 加载测试消息 "abc"
    LD   MSG_ABC
    ST   INPUT_BUFFER
    
    ; 调用 SHA256
    CALL SHA256_HASH
    
    ; 验证结果
    LD   H0
    SUB  EXPECTED_H0
    JZ   CHECK_H1
    JMP  TEST_FAILED
    
CHECK_H1:
    LD   H1
    SUB  EXPECTED_H1
    JZ   CHECK_H2
    JMP  TEST_FAILED
    
    ; ... 检查所有 8 个哈希字
    
TEST_PASSED:
    LD   PASS_CODE
    OUT
    STOP

TEST_FAILED:
    LD   FAIL_CODE
    OUT
    STOP
```

## 挖矿集成

### 矿工主循环

```assembly
; RustChain 矿工主循环
MINER_LOOP:
    ; 从矿池获取工作
    CALL GET_WORK
    
    ; 尝试不同 nonce
    LD   ZERO
    ST   NONCE
    
NONCE_LOOP:
    ; 构建区块头
    CALL BUILD_BLOCK_HEADER
    
    ; 计算 SHA256(SHA256(header))
    CALL SHA256_HASH
    CALL SHA256_HASH  ; 双重哈希
    
    ; 检查难度
    LD   HASH_RESULT
    SUB  DIFFICULTY_TARGET
    JN   FOUND_BLOCK  ; 如果小于目标，找到区块
    
    ; 下一个 nonce
    LD   NONCE
    ADD  ONE
    ST   NONCE
    
    ; 检查是否 Exhausted
    SUB  MAX_NONCE
    JZ   GET_NEW_WORK
    
    JMP  NONCE_LOOP

FOUND_BLOCK:
    ; 提交区块
    CALL SUBMIT_BLOCK
    JMP  MINER_LOOP
```

## 预期性能

### 单次 SHA256 哈希

- 指令数：~5000 条指令
- 平均每指令：25 μs
- **总时间**: ~125 ms / 哈希

### 双重 SHA256 (挖矿)

- **总时间**: ~250 ms / 尝试
- **哈希率**: ~4 H/s (理论最大)

### 实际考虑

由于纸带 I/O 和网络延迟，实际哈希率可能为：
- **0.1-1 H/s** (受 I/O 限制)

## 结论

在 EDSAC 2 上实现 SHA256 是具有挑战性但可行的。关键优化点：

1. **内存管理**: 精心规划内存布局
2. **查找表**: 使用 ROM 存储常量
3. **子程序优化**: 最小化调用开销
4. **I/O 优化**: 批量处理减少纸带操作

这将创造历史：第一台微程序化计算机挖掘加密货币！
