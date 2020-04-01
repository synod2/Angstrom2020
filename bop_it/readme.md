bop it write up
---------------
pwn , 80pts

desc 
---------------
```
Can you bop it? Source. Connect with nc shell.actf.co 20702.

```

- BOF 
- Nullbyte bug

files 
---------------

- challenge 
- source

checksec 
---------------
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
    
solution 
---------------
온갖 보호기법이 다걸려있다.
구조를 보면, Twist / Pull / Bop / Flag 중에 하나를 출력하고
그때마다 거기에 맞는 문자열 앞자리 한글자를 입력해야 다음 루틴으로 넘어가는 식이다.
0xff를 입력하면 프로그램이 종료된다. 
반복문이 실행될때마다 fopen 함수로 flag를 열고 내용을 읽어오는데, 
이때 Flag 에 해당하는 루틴이라면 flag에서 읽어온 내용과 첫 문자 이후의 내용을 비교하여 일치하는지 비교하고,
일치하지 않는다면 입력한 문자열을 wrong 문자열에 더하고, 지정한 문자열을 뒤에 덧붙여서 write 함수를 통해 출력시킨다. 

이때 스택과 복사하는 부분을 잘 분석해보면, 복사시엔 아래와 같은 형태로 배열을 지정하고 , 스택 지정은 다음과 같다. 
```
char wrong[strlen(guess)+35];

읽어온값 복사하는 위치 : rbp-0x150
입력버퍼 : rbp-0x130 
복사하는 위치 : rbp-0x1d0 
입력버퍼 길이 저장 위치 : rbp-0x198
```
입력 당시엔 복사하는 위치를 덮어쓸 수 없겠지만, 복사하는 시점에서는 덮어쓰는게 가능할 수도 있다. 어셈블리를 분석해보자.

```
   0x55db42d3d4fc <main+707>:   repnz scas al,BYTE PTR es:[rdi]
   0x55db42d3d4fe <main+709>:   mov    rax,rcx
   0x55db42d3d501 <main+712>:   not    rax
=> 0x55db42d3d504 <main+715>:   sub    rax,0x1
   0x55db42d3d508 <main+719>:   add    rax,rdx
   
   	strncat(wrong, guess, guessLen);
	strncat(wrong, " was wrong. Better luck next time!\n", 35);
	write(1, wrong, guessLen+35);
   
```
저 어셈코드가 아래 c 코드에서 guessLen을 가져오는 과정인데, 보면 guessLen이 처음에는 스택 공간에 저장되어있었으나 
첫번째 strncat 복사 이후에는 값으로 저장되지 않고 문자열의 길이를 통해 가져오는 식으로 변환된다. 
그런데 저 문자열의 길이를 가져오는 어셈코드가 해당 주소값 영역에 0x0이 있는지를 비교하다가 0x0이 나오면 그때를 문자열의 끝으로 간주하고 레지스터를 통해 길이를 계산한다. 
이를 이용하면, 스택에 이미 값이 있는곳 직전까지 문자열을 덮어씌워 값을 크게 만들어볼 수 있을것 같았는데, 
스택이 그만큼 밀려서 예상하던대로 동작하지는 않았다.

```
			int guessLen = read(0, guess+1, 255)+1; //add to already entered char
             ~~~~~~
				char wrong[strlen(guess)+35];
```
이부분을 잘 보자. guesslen은 read 함수를 통해 입력받은 문자열의 길이만큼을 가지는데, wrong은 guess문자열의 길이를 가져온다. 
strlen 함수가 문자열의 길이를 판단하는 기준은 널바이트까지이므로, 널바이트가 입력 문자열의 제일 앞에 오게되면 strlen의 결과값은 0이 될것이다. 
그러나 guesslen은 0보다 큰 값이므로, wrong 배열이 선언될 때 스택의 크기가 실제 입력한 문자열의 크기보다 작게 만들어진다. 
따라서, 적절한 길이를 조절하여 널바이트 이후에 입력해주면 이후에 문자열을 복사할때 0바이트만큼 복사해줄 것이고, 
이후 write 함수가 실행될때는 실제 입력한 길이만큼 출력해줄테지만 실제 입력해준만큼 복사되지 않았으므로, 스택에 있는 값을 계속 읽어올 것이다. 

풀이 완료. 








