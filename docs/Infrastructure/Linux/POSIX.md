# POSIX (Portable Operating System Interface)

**POSIX**는 IEEE가 제정한 유닉스 계열 운영체제 간의 **이식성(Portability)**을 높이기 위한 인터페이스 표준 규격입니다.

## 핵심 의미
*   **호환성:** POSIX 표준을 따르는 프로그램은 리눅스, macOS, Solaris 등 서로 다른 유닉스 시스템에서도 수정 없이(또는 최소한의 수정으로) 컴파일되고 실행될 수 있습니다.
*   **범위:** 시스템 호출(System Call), 프로세스, 스레드(pthread), 시그널, 파일 I/O, 쉘 커맨드 등 운영체제의 핵심 API를 정의합니다.

## 예시
*   **POSIX Thread (pthread):** 리눅스와 macOS에서 멀티스레드 프로그래밍을 할 때 사용하는 표준 라이브러리입니다.
*   **Shell Script:** `#!/bin/sh`로 시작하는 스크립트는 POSIX 표준 쉘 문법을 따르므로 대부분의 유닉스 시스템에서 동작합니다. (반면 `#!/bin/bash`는 Bash 고유의 기능이 있어 호환되지 않을 수 있습니다.)

## 참고
*   [Wikipedia - POSIX](https://ko.wikipedia.org/wiki/POSIX)