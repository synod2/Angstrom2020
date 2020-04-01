no_canary write up
---------------
pwn , 50pts

desc 
---------------
```
Agriculture is the most healthful, most useful and most noble employment of man.

—George Washington

Can you call the flag function in this program (source)? 
Try it out on the shell server at /problems/2020/no_canary or by connecting with nc shell.actf.co 20700.

```

- bof

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
프로그램 실행시 gets 함수로 문자열을 입력받는데 길이 제한같은건 없고, 프로그램 내에 flag를 출력하는  함수가 존재한다. 
bof 발생시키고 ret를 해당 함수의 주소로 덮어씌우면 될것같다. 그런데 바이너리와 소스코드의 내용이 조금 다른듯 싶다..?
어찌됐든, 0x20 + rbp + ret(flag 주소) 하면 끝. 
