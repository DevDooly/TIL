# Paseo 설치 및 모바일 원격 제어 설정 가이드

Paseo는 서버/PC에 데몬(Daemon)을 구동하고, 스마트폰(Android/iOS 앱), 웹 브라우저, CLI를 통해 외부 어디서든 AI 코딩 에이전트(Claude Code, Codex 등)를 모니터링하고 원격 제어할 수 있는 오픈소스 오케스트레이터입니다.

---

## 1. Paseo CLI 및 데몬 설치

### 1.1 사전 요구사항
* Node.js (v18 이상 권장, v24 지원)
* npm

### 1.2 글로벌 설치
```bash
npm install -g @getpaseo/cli
```

버전 확인:
```bash
paseo --version
```

---

## 2. 외부 접속을 위한 데몬 실행 및 네트워크 설정 (중요)

외부 도메인(DDNS)이나 모바일 앱에서 직접 접속(Direct IP/Domain) 및 Relay 접속이 가능하도록 설정합니다.

### 2.1 로컬 방화벽 (UFW) 포트 허용
```bash
sudo ufw allow 6767/tcp
```

### 2.2 데몬 백그라운드 시작 (외부 리슨 및 도메인 허용)
기본 실행 시 `127.0.0.1`로만 바인딩되므로, 외부 접속을 허용하려면 `--listen 0.0.0.0:6767`과 호스트네임 허용(`--hostnames`) 옵션을 반드시 추가해야 합니다.

```bash
# 0.0.0.0 바인딩, 도메인 허용, Relay 및 Web UI 활성화
paseo daemon start --listen 0.0.0.0:6767 --hostnames "devdooly.iptime.org,localhost,127.0.0.1,true" --relay --web-ui
```

### 2.3 데몬 상태 확인
```bash
paseo daemon status
```

출력 예시:
```text
KEY               VALUE                                          
Server ID         srv_xxxxxxxxxxxx                               
Local Daemon      running                                        
Connected Daemon  reachable                                      
Home              /home/user/.paseo                              
Listen            0.0.0.0:6767                                   
Relay             wss://relay.paseo.sh:443                       
PID               1234567                                        
Logs              /home/user/.paseo/daemon.log                   
```

---

## 3. 스마트폰 (Android / iOS) 앱 페어링 방법

Paseo 데몬이 실행된 상태에서 페어링 QR 코드 또는 링크를 생성하여 스마트폰 앱에 등록합니다.

### 3.1 페어링 코드 생성
```bash
paseo daemon pair
```

터미널에 **QR 코드**와 함께 **Pairing link**가 출력됩니다.

### 3.2 안드로이드 앱에서 연결 절차
1. 스마트폰에서 **Paseo 앱** 실행
2. **Scan QR Code**를 눌러 터미널의 QR 코드를 스캔하거나, **Pairing Link** URL을 복사하여 입력
3. 페어링이 완료되면 서버의 워크스페이스 및 에이전트 목록이 스마트폰 화면에 즉시 동기화됩니다.

---

## 4. 유용한 Paseo CLI 관리 명령어

| 작업 | 명령어 |
| :--- | :--- |
| **데몬 시작 (외부 허용)** | `paseo daemon start --listen 0.0.0.0:6767 --hostnames "devdooly.iptime.org,localhost,true" --relay --web-ui` |
| **데몬 상태 확인** | `paseo daemon status` |
| **페어링 QR/링크 출력** | `paseo daemon pair` |
| **데몬 재시작** | `paseo daemon restart` |
| **데몬 정지** | `paseo daemon stop` |
| **지원 프로바이더 조회** | `paseo provider ls` |
| **실행 중인 에이전트 목록** | `paseo ls` |
| **새 에이전트 작업 실행** | `paseo run "작업 지시 내용"` |
| **에이전트 세션 접속** | `paseo attach <AGENT_ID>` |

---

## 5. systemd 서비스 등록 (서버 부팅 시 자동 실행 - 선택 사항)

서버 재부팅 시에도 Paseo 데몬이 자동으로 기동되도록 `systemd` 사용자 서비스를 등록할 수 있습니다.

`~/.config/systemd/user/paseo.service` 생성:
```ini
[Unit]
Description=Paseo AI Agent Daemon
After=network.target

[Service]
Type=simple
ExecStart=%h/.nvm/versions/node/v24.12.0/bin/node %h/.nvm/versions/node/v24.12.0/bin/paseo daemon start --foreground --listen 0.0.0.0:6767 --hostnames "devdooly.iptime.org,localhost,true" --relay --web-ui
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
```

서비스 활성화 및 시작:
```bash
systemctl --user daemon-reload
systemctl --user enable --now paseo
```
