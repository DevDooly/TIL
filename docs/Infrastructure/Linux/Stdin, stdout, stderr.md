# Stdin, Stdout, Stderr (표준 스트림)

리눅스(유닉스) 환경에서 프로그램이 실행될 때 기본적으로 연결되는 3가지 표준 입출력 스트림입니다.

## 1. 개념

| 이름 | 파일 디스크립터 (FD) | 설명 | 기본 장치 |
| :--- | :---: | :--- | :--- |
| **stdin** (Standard Input) | 0 | 프로그램으로 들어가는 입력 | 키보드 |
| **stdout** (Standard Output) | 1 | 프로그램이 정상적으로 출력하는 결과 | 모니터 (터미널) |
| **stderr** (Standard Error) | 2 | 오류 메시지나 진단 정보를 출력 | 모니터 (터미널) |

## 2. 리다이렉션 (Redirection)

스트림의 방향을 파일이나 다른 장치로 돌리는 기능입니다.

*   `>`: stdout을 파일로 저장 (덮어쓰기)
*   `>>`: stdout을 파일 끝에 추가 (append)
*   `2>`: stderr만 파일로 저장
*   `2>&1`: stderr을 stdout과 같은 곳으로 보냄
*   `<`: 파일 내용을 stdin으로 입력

### 예시
```bash
# 정상 출력은 out.log에, 에러는 err.log에 저장
python app.py > out.log 2> err.log

# 정상 출력과 에러 모두를 같은 파일에 저장
python app.py > all.log 2>&1
```

## 3. 파이프 (Pipe, `|`)
한 프로그램의 **stdout**을 다음 프로그램의 **stdin**으로 연결합니다.
```bash
# ls의 결과를 grep의 입력으로 넘김
ls -l | grep "txt"
```