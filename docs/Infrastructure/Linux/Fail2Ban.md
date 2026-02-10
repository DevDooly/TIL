# Fail2Ban

**Fail2Ban**은 로그 파일을 모니터링하여 비밀번호 추측 공격(Brute-force attack) 등 의심스러운 활동을 감지하고, 해당 IP 주소를 방화벽(iptables, UFW 등)을 통해 차단하는 침입 차단 소프트웨어입니다.

## 1. 설치

Ubuntu/Debian 환경에서는 `apt`를 통해 간단하게 설치할 수 있습니다.

```bash
sudo apt update
sudo apt install fail2ban -y
```

설치 후 서비스가 실행 중인지 확인합니다.
```bash
sudo systemctl status fail2ban
```

---

## 2. 설정 (Configuration)

기본 설정 파일은 `/etc/fail2ban/jail.conf`에 있지만, 이 파일은 패키지 업데이트 시 덮어씌워질 수 있습니다.  
따라서 **`.local` 파일을 생성하여 사용자 설정을 관리**해야 합니다.

### 설정 파일 복사
```bash
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
```

### 주요 설정 (`jail.local` 수정)

`sudo vim /etc/fail2ban/jail.local` 명령어로 파일을 열어 기본 설정(`[DEFAULT]`)을 수정합니다.

```ini
[DEFAULT]
# 차단 시간 (초 단위). -1은 영구 차단
bantime = 10m

# 감지 기간 (이 시간 동안 maxretry 횟수만큼 실패하면 차단)
findtime = 10m

# 최대 허용 실패 횟수
maxretry = 5

# 차단하지 않을 신뢰할 수 있는 IP (예: 로컬 네트워크, 관리자 IP)
ignoreip = 127.0.0.1/8 ::1 192.168.1.0/24
```

---

## 3. SSH 보호 설정 (sshd)

SSH 접속 시도를 모니터링하여 차단하는 설정입니다. `jail.local` 파일에서 `[sshd]` 섹션을 찾아 활성화합니다.

```ini
[sshd]
enabled = true
port    = ssh    # 포트를 변경했다면 숫자(예: 2222)로 지정
logpath = %(sshd_log)s
backend = %(sshd_backend)s
maxretry = 3
```

설정 변경 후 반드시 서비스를 재시작해야 적용됩니다.
```bash
sudo systemctl restart fail2ban
```

---

## 4. 주요 명령어

### 상태 확인
현재 실행 중인 감옥(Jail) 목록과 상태를 확인합니다.

```bash
# 전체 상태 확인
sudo fail2ban-client status

# 특정 Jail(sshd) 상세 확인 (차단된 IP 목록 확인)
sudo fail2ban-client status sshd
```

### IP 차단 해제 (Unban)
실수로 본인이 차단되었거나, 특정 IP의 차단을 해제해야 할 때 사용합니다.

```bash
# sudo fail2ban-client set [Jail이름] unbanip [IP주소]
sudo fail2ban-client set sshd unbanip 192.168.1.100
```

### 로그 확인
Fail2Ban의 동작 로그를 실시간으로 확인합니다.

```bash
sudo tail -f /var/log/fail2ban.log
```
