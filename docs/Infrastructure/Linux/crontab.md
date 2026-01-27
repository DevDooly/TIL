# Crontab (크론탭)

**Cron**은 유닉스 계열 운영체제의 시간 기반 작업 스케줄러입니다. **Crontab**(Cron Table)은 이 작업을 설정하는 파일을 의미합니다.

## 1. 기본 명령어

```bash
crontab -e  # 설정 파일 편집 (Edit)
crontab -l  # 현재 설정된 작업 목록 확인 (List)
crontab -r  # 설정된 모든 작업 삭제 (Remove)
```

## 2. 작성 문법

5개의 필드와 실행할 명령어로 구성됩니다.
```text
*  *  *  *  *  <command_to_execute>
│  │  │  │  │
│  │  │  │  └── 요일 (0 - 7) (0, 7 = 일요일)
│  │  │  └───── 월 (1 - 12)
│  │  └─────── 일 (1 - 31)
│  └───────── 시 (0 - 23)
└─────────── 분 (0 - 59)
```

### 예시
```bash
# 매분 실행
* * * * * /path/to/script.sh

# 매일 새벽 3시에 실행
0 3 * * * /backup/backup.sh

# 매주 월요일 오전 9시 30분에 실행
30 9 * * 1 /work/weekly_report.sh

# 재부팅 시 실행 (특수 구문)
@reboot /path/to/startup_script.sh
```

## 3. 로그 확인
Cron 작업이 실패했거나 실행 여부를 확인하려면 시스템 로그를 봐야 합니다.
*   Ubuntu: `/var/log/syslog` (grep CRON)
*   CentOS: `/var/log/cron`