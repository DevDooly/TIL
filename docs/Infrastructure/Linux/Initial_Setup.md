# Ubuntu Server 초기 셋팅 가이드

Ubuntu 서버를 처음 설치한 후, 보안과 안정성을 위해 필수적으로 수행해야 하는 초기 설정 과정입니다.

## 1. 시스템 패키지 업데이트

설치 직후에는 패키지 리스트를 갱신하고 최신 버전으로 업그레이드하여 보안 취약점을 해결해야 합니다.

```bash
sudo apt update && sudo apt upgrade -y
```
- `update`: 저장소(Repository)의 패키지 목록 갱신
- `upgrade`: 실제 설치된 패키지들을 최신 버전으로 업그레이드

---

## 2. 사용자(User) 생성 및 권한 부여

보안상 **root 계정으로 직접 로그인해서 사용하는 것은 권장하지 않습니다.** 관리자 권한(`sudo`)을 가진 별도 사용자를 생성하여 사용합니다.

### 2.1 새 사용자 추가
```bash
# 'devdooly'라는 사용자 생성 (원하는 ID로 변경)
adduser devdooly
```
비밀번호 설정 및 추가 정보를 입력합니다.

### 2.2 Sudo 권한 부여
생성한 사용자를 `sudo` 그룹에 추가하여 관리자 명령을 수행할 수 있게 합니다.

```bash
usermod -aG sudo devdooly
```

이제 `exit` 후 생성한 계정으로 다시 로그인하여 테스트해 봅니다.

---

## 3. SSH 보안 설정

서버 보안 침해의 대부분은 SSH를 통해 발생합니다. 기본 설정을 변경하여 보안을 강화합니다.

### 3.1 설정 파일 수정
`/etc/ssh/sshd_config` 파일을 수정합니다.

```bash
sudo vim /etc/ssh/sshd_config
```

### 3.2 주요 보안 옵션
다음 항목들을 찾아 수정하거나 주석을 해제합니다.

```conf
# 1. Root 로그인 차단 (필수)
PermitRootLogin no

# 2. 비밀번호 인증 차단 (SSH Key 사용 시 권장)
# SSH Key가 등록된 상태에서만 설정해야 합니다!
PasswordAuthentication no

# 3. 빈 비밀번호 로그인 차단
PermitEmptyPasswords no

# 4. SSH 포트 변경 (선택 사항, 예: 2222)
# 포트 변경 시 방화벽 설정도 함께 변경해야 함
Port 2222
```

### 3.3 SSH 데몬 재시작
설정을 적용하기 위해 서비스를 재시작합니다.

```bash
sudo service ssh restart
```

---

## 4. 방화벽 (UFW) 설정

Ubuntu의 기본 방화벽인 **UFW (Uncomplicated Firewall)**를 활성화하여 불필요한 접근을 차단합니다.

### 4.1 기본 정책 설정 (모두 차단)
```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

### 4.2 필수 포트 허용
**주의:** SSH 포트(기본 22)를 허용하지 않고 활성화하면 서버에 접속할 수 없게 됩니다.

```bash
# SSH (기본 22번인 경우)
sudo ufw allow ssh
# 또는 포트를 변경했다면 (예: 2222)
sudo ufw allow 2222/tcp

# 웹 서버 (HTTP/HTTPS)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

### 4.3 방화벽 활성화
```bash
sudo ufw enable
```
상태 확인: `sudo ufw status`

---

## 5. 타임존 (Timezone) 설정

서버 로그의 시간이 한국 시간(KST)과 다르면 디버깅이 어렵습니다.

### 현재 시간 확인
```bash
date
```

### 타임존 변경 (Asia/Seoul)
```bash
sudo timedatectl set-timezone Asia/Seoul
```
다시 `date` 명령어로 KST로 변경되었는지 확인합니다.

---

## 6. Swap 메모리 설정 (선택 사항)

AWS EC2 프리티어 등 메모리가 적은 환경에서는 메모리 부족(OOM)으로 프로세스가 죽을 수 있습니다. 디스크의 일부를 메모리처럼 사용하는 Swap 파일을 생성합니다.

### 6.1 Swap 파일 생성 (예: 2GB)
```bash
# 2GB 크기의 파일 할당
sudo fallocate -l 2G /swapfile

# 권한 설정 (root만 읽기/쓰기 가능)
sudo chmod 600 /swapfile

# Swap 영역으로 포맷
sudo mkswap /swapfile

# Swap 활성화
sudo swapon /swapfile
```

### 6.2 영구 적용 (재부팅 시 유지)
`/etc/fstab` 파일에 내용을 추가합니다.

```bash
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

## 7. 필수 도구 설치

개발 및 운영에 자주 사용되는 기본 도구들을 설치합니다.

```bash
sudo apt install -y net-tools htop curl wget vim git unzip
```
