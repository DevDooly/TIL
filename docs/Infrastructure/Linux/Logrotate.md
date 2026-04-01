# Logrotate (로그로테이트)

**Logrotate**는 서버에 쌓이는 로그 파일들을 자동으로 관리(회전, 압축, 삭제)해주는 리눅스 시스템 유틸리티입니다. 디스크 용량이 로그로 인해 가득 차는 것을 방지합니다.

## 1. 주요 설정 옵션 (`/etc/logrotate.conf` 또는 `/etc/logrotate.d/`)

*   `daily` / `weekly` / `monthly`: 로그 회전 주기
*   `rotate <숫자>`: 남겨둘 로그 파일 개수 (예: 30이면 30개까지 보관하고 오래된 것은 삭제)
*   `size <용량>`: 파일 크기가 지정된 용량을 넘으면 회전 (예: 100M)
*   `compress`: 지난 로그 파일을 gzip으로 압축
*   `missingok`: 로그 파일이 없어도 에러를 내지 않음
*   `notifempty`: 로그 내용이 비어있으면 회전하지 않음
*   `copytruncate`: **중요** 현재 로그 파일을 복사(copy)한 뒤, 원본 파일 내용을 비움(truncate). 애플리케이션이 로그 파일을 계속 열고 있어도 중단 없이 회전 가능하게 함.

## 2. Docker 컨테이너 로그 관리 예시

Docker 컨테이너의 JSON 로그가 무한정 커지는 것을 막기 위한 설정입니다.

**파일:** `/etc/logrotate.d/docker-container`

```nginx
/var/lib/docker/containers/*/*.log {
  rotate 7
  daily
  compress
  missingok
  delaycompress
  copytruncate
}
```

## 3. 실행 및 테스트

```bash
# 강제로 실행 (디버그 모드 -d 옵션으로 미리 확인 가능)
logrotate -f /etc/logrotate.d/docker-container
```