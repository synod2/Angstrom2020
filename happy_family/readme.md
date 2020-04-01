happy family / deja vu write up
---------------
pwn/rev , 100/120pts

desc 
---------------
```

```

- 

files 
---------------

- challenge 
- source
- 
checksec 
---------------
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
solution 
---------------
특이하게도 한 문제에 리버싱과 퍼너블이 둘다 들어있다.
프로그램 실행 후 입력을 받는데 , 길이가 32바이트가 아니라면 프로그램을 종료한다. 
32바이트의 입력값이 조건에 일치하면 리버싱 플래그를 출력해준다. 

입력한 문자열은 inp 배열에 들어가는데, 해당 배열은 shalf와 fhalf 로 나뉘어 각기 짝/홀수 자리벼로 나누어진다.



