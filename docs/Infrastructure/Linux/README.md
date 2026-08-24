---
title: Linux Administration & Performance Engineering
---

# 🐧 Linux Administration & Performance

서버 운영, 고성능 네트워크 전송, 보안 강화 및 자동화를 위한 **Linux 커널 설정, 시스템 관리 및 명령어 활용 가이드**입니다.

---

## 📚 주요 기술 문서 목차

### 1. High-Performance File & Network Transfer
* **[대량 파일 전송 가이드 (Large File Transfer)](Large_File_Transfer.md)**: `rsync`, `tar`, `netcat`을 이용한 대용량 파일 고속 전송, 네트워크 튜닝 및 용량 검증

### 2. Server Setup & Security
* **[Linux 초기 서버 세팅 & 보안 (Initial Setup)](Initial_Setup.md)**: 유저 권한, SSH 키 인증 및 보안 강화
* **[Fail2Ban](Fail2Ban.md)**: SSH 무차별 대입 공격(Brute-force) 탐지 및 차단

### 3. System Automation & Logs
* **[Crontab](crontab.md)**: 작업 스케줄러 설정 및 주기적 배치 실행
* **[Logrotate](Logrotate.md)**: 대용량 로그 파일 자동 분할, 압축 및 보존 주기 관리

### 4. Core Concepts & Shell
* **[POSIX 표준](POSIX.md)**: 유닉스 계열 운영체제 간 이식성 표준 규격
* **[Standard Streams (Stdin, Stdout, Stderr)](Stdin,%20stdout,%20stderr.md)**: 표준 I/O 스트림 및 파이프라인/리다이렉션
* **[TL;DR](TL;DR.md)**: 실용적인 커맨드라인 예제 요약 도구
