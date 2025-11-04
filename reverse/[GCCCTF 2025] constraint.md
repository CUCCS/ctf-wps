## 基本信息

- 题目名称： [GCCCTF 2025] constraint
- 考点清单： 脱壳技术，约束求解

## 一、看到什么

这是一道综合性的Reverse题目，涉及壳识别、脱壳、静态分析和约束求解。题目给出一个Windows PE 64位可执行文件calme.exe。

## 二、想到什么解题思路

使用IDA Pro打开calme.exe，发现以下特征：

1. 程序段名为 **UPX0**、**UPX1**、**UPX2**
2. 入口点函数非常复杂，包含大量位操作和解压逻辑
3. 代码段中有大量0xFF填充

这些特征表明程序使用了 **UPX壳** 进行压缩。

## 三、尝试过程和结果记录

UPX是一个常见的可执行文件压缩工具，可以直接使用UPX工具进行解包：

```bash
# 安装UPX（macOS）
brew install upx

# 解包
upx -d calme.exe -o calme_unpacked.exe
```

**解包结果**：

- 原始大小：137KB (140592 bytes)
- 解包后：311KB (318256 bytes)
- 压缩率：44.18%

解包成功后，在IDA Pro中打开`calme_unpacked.exe`进行分析。

### 静态分析

使用IDA Pro分析解包后的程序，找到两个关键函数：

#### main函数 (0x4016ee)

```c
int main(int argc, const char **argv, const char **envp)
{
    char Buffer[272];
    FILE *v3;
    
    printf("Enter the flag: ");
    v3 = __acrt_iob_func(0);
    
    if (!fgets(Buffer, 256, v3))
        return 1;
    
    // 去除换行符
    size_t len = strlen(Buffer);
    if (len > 0 && Buffer[len-1] == '\n')
        Buffer[len-1] = '\0';
    
    if (verify_flag(Buffer)) {
        puts("Correct!");
        return 0;
    } else {
        puts("Wrong!");
        return 1;
    }
}
```

#### verify_flag函数 (0x401560)

这是核心验证函数，包含多个约束条件：

```c
bool verify_flag(char* a1)
{
    unsigned char v5, v6, v7, v8, v9, v10, v11, v12;
    
    // 1. 检查长度：必须为16字符
    if (strlen(a1) != 16)
        return false;
    
    // 2. 检查前缀：必须是"GCCCTF{"
    if (memcmp(a1, "GCCCTF{", 7) != 0)
        return false;
    
    // 3. 检查结尾：必须是'}'
    if (a1[15] != '}')
        return false;
    
    // 4. 提取8个字节 (flag[7]到flag[14])
    for (int i = 0; i < 8; i++)
        *(&v5 + i) = a1[i + 7];
    
    // 5. 线性方程组约束
    if (7*v5 + 3*v6 + 11*v7 + 13*v9 != 2145)
        return false;
    if (8*v6 + 12*v8 + 9*v10 + 4*v12 != 2491)
        return false;
    if (6*v5 + 5*v7 + 8*v11 + 7*v12 != 2299)
        return false;
    if (9*v8 + 11*v9 + 6*v10 + 10*v11 != 3165)
        return false;
    
    // 6. 异或约束
    return (v10 ^ (v5 ^ v6 ^ v7 ^ v8 ^ v9)) == 95;
}
```

### 建立数学模型

从验证函数中提取出约束条件：

**变量定义**：

- Flag格式：`GCCCTF{xxxxxxxx}`
- 需要求解8个字节：v5, v6, v7, v8, v9, v10, v11, v12

**约束条件**：

1. **线性方程组**（4个方程，8个未知数）：

   ```
   7*v5 + 3*v6 + 11*v7 + 0*v8 + 13*v9 + 0*v10 + 0*v11 + 0*v12 = 2145
   0*v5 + 8*v6 + 0*v7 + 12*v8 + 0*v9 + 9*v10 + 0*v11 + 4*v12 = 2491
   6*v5 + 0*v6 + 5*v7 + 0*v8 + 0*v9 + 0*v10 + 8*v11 + 7*v12 = 2299
   0*v5 + 0*v6 + 0*v7 + 9*v8 + 11*v9 + 6*v10 + 10*v11 + 0*v12 = 3165
   ```

2. **异或约束**：

   ```
   v10 ^ (v5 ^ v6 ^ v7 ^ v8 ^ v9) = 95
   ```

3. **字符范围约束**：

   - 所有变量必须是可打印ASCII字符（33-126）

### 编写求解脚本

使用Z3 SMT求解器来求解约束题目

```python
#!/usr/bin/env python3
"""
CTF题目解题脚本
使用Z3 SMT求解器来求解约束题目
"""

from z3 import *

def solve_constraint_challenge():
    """使用Z3求解约束系统"""

    print("=== Constraint Solver ===")

    # 创建Z3求解器
    solver = Solver()
    solver.set("timeout", 10000)

    # 定义8个整数变量
    b = [Int(f'b{i}') for i in range(8)]

    # 字符类型约束
    for i in range(8):
        solver.add(Or(
            And(b[i] >= 97, b[i] <= 122),  # 小写字母
            And(b[i] >= 65, b[i] <= 90),   # 大写字母
            And(b[i] >= 48, b[i] <= 57)    # 数字
        ))

    # 线性约束（每个约束至少4个变量）
    solver.add(7*b[0] + 3*b[1] + 11*b[2] + 13*b[4] == 2145)
    solver.add(8*b[1] + 12*b[3] + 9*b[5] + 4*b[7] == 2491)
    solver.add(6*b[0] + 5*b[2] + 8*b[6] + 7*b[7] == 2299)
    solver.add(9*b[3] + 11*b[4] + 6*b[5] + 10*b[6] == 3165)

    # XOR约束（使用位操作约束，确保XOR约束是必需的）
    # 为前6个字节的每一位创建布尔变量
    bits = [[Bool(f'bit_{i}_{j}') for j in range(8)] for i in range(6)]

    # 约束：位变量组合成字节值
    for i in range(6):
        byte_val = Sum([If(bits[i][j], 2**j, 0) for j in range(8)])
        solver.add(b[i] == byte_val)

    # XOR约束：每一位的XOR结果等于目标值的对应位
    target_xor = 0x5f
    target_bits = [bool(target_xor & (1 << j)) for j in range(8)]
    for j in range(8):
        bit_xor = bits[0][j]
        for i in range(1, 6):
            bit_xor = Xor(bit_xor, bits[i][j])
        solver.add(bit_xor == target_bits[j])

    # 求解
    if solver.check() == sat:
        model = solver.model()
        flag_bytes = [model[b[i]].as_long() for i in range(8)]
        flag_content = ''.join(chr(b) for b in flag_bytes)
        return f"GCCCTF{{{flag_content}}}"
    else:
        return None

def main():
    flag = solve_constraint_challenge()
    if flag:
        print(flag)
    else:
        print("No solution found")

if __name__ == "__main__":
    main()
```

flag: **GCCCTF{F14gH3re}**