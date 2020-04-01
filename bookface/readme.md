bookface write up
---------------
pwn , 270pts

desc 
---------------
```
I made a new social networking service. It's a little glitchy, but no way that could result in a data breach, right?

Connect with nc pwn.2020.chall.actf.co 20733.

Author: kmh

```

- 

files 
---------------

- challenge 
- source
- Dockerfile
- libc.so.6 -> glibc.2.23(ubuntu 16.04)
- server.sh 
- xinetd.conf

checksec 
---------------
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
    
solution 
---------------
```
Please enter your user ID: 113
Welcome to bookface!
What's your name? hello
You have 0 friends. What would you like to do?
[1] Make friends
[2] Lose friends
[3] Delete account
[4] Log out
>
```
보호기법이 다걸려있다. 프로그램 시작시에 login함수로 진입한다.
user id를 입력받고, sprintf 함수를 이용해 해당 내용을 file이라는 문자열에 users/ 의 뒤에 덧붙여서 저장한다.
이후에 access 함수를 통해 해당 경로에 있는 파일에 접근권한이 있는지를 확인하고, 
접근이 가능하다면 survey 배열에 4번에 걸쳐 3글자씩 입력을 받는다. 
이후 배열내에 문자열 n이 포함되면 exit으로 프로그램을 종료시키거나, 입력했던 점수가 모두 10점이 아니라면
printf 로 입력했던 내용을 출력시키면서 같은 위치에 다시 입력을 받게 만든다. 

```
user = mmap(rand()&0xfffffffffffff000, sizeof (struct profile), 
PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED, -1, 0);
```
이후에 mmap함수가 실행되어 그 리턴값이 user에 저장되는데, 이는 access함수가 실패한 경우에도 동일하게 동작한다. 
mmap 함수는 인자로 매핑될 주소, 크기, 보호모드, 매핑옵션, fd, 시작 주소 가 지정되는데 이 경우에는 
rand함수의 결과값의 하위 3바이트를 필터링 한 곳이 매핑될 주소가 되고, 크기는 profile 구조체의 크기인 0x108바이트,
fd는 -1로 지정되고 오프셋은 0이 된다. fd가 -1인 경우는 어떻게 동작하는거지?

어찌됐든 그 다음 fopen 함수로 아까전에 그 파일을 열고 , fread함수로 0x108바이트만큼 읽어와 user에 저장한 다음 
fclose 함수로 파일을 닫는다. 이때 survey시 10외에 다른걸 입력했다면 user 구조체의 friends를 0 으로 만들어버린다. 

else 문으로 진입했을경우도 mmap까지는 동일하게 동작하고, 
fgets 함수를 통해 user->name 위치에 0x100 만큼 입력을 받는다. 

login이 끝난 다음, 1번이나 2번 메뉴를 선택하면 user->friends의 갯수를 조절할 수 있게 되는데 ,
입력하는 숫자에 따라 값은 커지거나 작아질 수 있다. 

3번 메뉴를 선택하면 경로에 있던 파일을 삭제후에 login함수를 실행시키고
4번 메뉴를 선택하면 sprintf 함수를 통해 file 배열에 파일 디렉토리를 복사하고 
fopen함수가 해당 디렉토리에 있는 파일을 연 다음 fwrite 로 구조체의 내용을 써넣고 fclose 한다. 
이후 login 함수를 실행, 평점 매기기로 들어간다. 

취약점이 발생할만한 곳들을 찾아보자.

```
if (strchr(survey, 'n') != NULL) {
	//a bug bounty report said something about hacking and the letter n
	puts("ERROR: HACKING DETECTED");
	puts("Exiting...");
	exit(1);
}
if (strcmp(survey, "10\n10\n10\n10\n") != 0) {
	puts("Those ratings don't seem quite right. Please review them and try again:");
	printf(survey);
```
우선 printf 실행시 FSB가 유발되는 부분이 있다. 다만 n 문자열을 검사하기 때문에 덮어쓰는 동작은 불가해보이고, 주소 leak 정도만 가능할걸로 보인다. 



