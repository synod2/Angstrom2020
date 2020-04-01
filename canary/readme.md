canary write up
---------------
pwn , 70pts

desc 
---------------
```
A tear rolled down her face like a tractor. “David,” she said tearfully, “I don’t want to be a farmer no more.”

—Anonymous

Can you call the flag function in this program (source)? 
Try it out on the shell server at /problems/2020/canary or by connecting with nc shell.actf.co 20701.
```

- fsb
- bof
- bypass canary

files 
---------------

- challenge 
- source

checksec 
---------------
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
solution 
---------------
no_canary와 유사한데, 이번엔 카나리가 걸려있고 , 입력을 두번받는다.
첫째 입력후 출력할때를 잘보면 fsb가 유발되는걸 알 수 있다. 
이걸로 카나리를 알아내서 두번쨰 입력때 카나리를 포함한 bof를 일으키면 될것같다. 
