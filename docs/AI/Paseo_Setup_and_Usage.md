# Paseo 설치 및 모바일 원격 제어 설정 가이드

Paseo는 서버/PC에 데몬(Daemon)을 구동하고, 스마트폰(Android/iOS 앱), 웹 브라우저, CLI를 통해 외부 어디서든 AI 코딩 에이전트(Claude Code, OpenCode, Codex 등)를 모니터링하고 원격 제어할 수 있는 오픈소스 오케스트레이터입니다.

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

## 4. Paseo에서 Google Gemini 모델 연동 방법 (OpenCode 활용)

Paseo는 제어 플레인(Control Plane)이며, 다양한 LLM을 구동하기 위해 **Provider(에이전트 엔진)**를 사용합니다. **OpenCode** Provider를 통해 **Google Gemini (Gemini 3.7 Flash, 2.5 Pro, 2.0 Flash 등)**를 손쉽게 사용할 수 있습니다.

### 4.1 OpenCode CLI 설치
```bash
npm install -g opencode-ai
```

### 4.2 Gemini API Key 설정
Google AI Studio에서 발급받은 API 키를 환경 변수에 등록합니다.

```bash
# ~/.bashrc 또는 ~/.zshrc 에 추가
export GEMINI_API_KEY="your-gemini-api-key-here"
```

*또는 `opencode auth login`을 통해 브라우저로 Google 계정 직접 로그인도 지원합니다.*

### 4.3 Paseo 데몬 재시작 및 Provider 확인
```bash
paseo daemon restart
paseo provider ls
```
`opencode`가 `available (Enabled)` 상태로 표시됩니다.

### 4.4 모바일 앱 / CLI에서 Gemini 모델 사용
* **모바일 앱**: 새 에이전트 생성 시 Provider를 **OpenCode**로 선택하고, Model 목록에서 **`google/gemini-3.7-flash`** 또는 **`google/gemini-2.5-pro`**를 선택합니다.
* **CLI 실행 예시**:
  ```bash
  paseo run --provider opencode --model google/gemini-3.7-flash "프로젝트 버그 수정해줘"
  ```

---

## 5. 유용한 Paseo CLI 관리 명령어

| 작업 | 명령어 |
| :--- | :--- |
| **데몬 시작 (외부 허용)** | `paseo daemon start --listen 0.0.0.0:6767 --hostnames "devdooly.iptime.org,localhost,true" --relay --web-ui` |
| **데몬 상태 확인** | `paseo daemon status` |
| **페어링 QR/링크 출력** | `paseo daemon pair` |
| **데몬 재시작** | `paseo daemon restart` |
| **데몬 정지** | `paseo daemon stop` |
| **지원 프로바이더 조회** | `paseo provider ls` |
| **특정 프로바이더 지원 모델 조회** | `paseo provider models opencode` |
| **실행 중인 에이전트 목록** | `paseo ls` |
| **새 에이전트 작업 실행** | `paseo run "작업 지시 내용"` |
| **에이전트 세션 접속** | `paseo attach <AGENT_ID>` |

---

## 6. systemd 서비스 등록 (서버 부팅 시 자동 실행 - 선택 사항)

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
