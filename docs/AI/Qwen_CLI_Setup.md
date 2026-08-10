# Qwen CLI - API Key 재등록 및 설정 가이드

Qwen CLI(또는 DashScope 기반 Qwen 도구)를 설치한 후 잘못된 API Key를 등록했거나 키를 갱신해야 할 때 **API Key를 재등록/재설정하는 방법**입니다.

---

## 1. CLI 명령어로 재등록

대부분의 Qwen CLI 도구는 `config` 또는 `auth` 서브커맨드를 제공합니다.

```bash
# config 명령어를 통한 재설정
qwen config set api_key <새로운_API_KEY>

# 또는 환경변수 키 이름 명시
qwen config set DASHSCOPE_API_KEY <새로운_API_KEY>

# 인증 초기화/재로그인
qwen auth login
# 또는
qwen init
```

---

## 2. 설정 파일 직접 수정

CLI 실행 시 자동 생성된 설정 파일에서 잘못 입력된 키를 직접 수정할 수 있습니다.

### 설정 파일 위치
* **Windows**:
  * `%USERPROFILE%\.qwen\config.json` (예: `C:\Users\<사용자명>\.qwen\config.json`)
  * `%USERPROFILE%\.dashscope\api_key`
  * `%APPDATA%\qwen\config.json`
* **Linux / macOS**:
  * `~/.qwen/config.json`
  * `~/.dashscope/api_key`
  * `~/.config/qwen/config.json`

### `config.json` 수정 예시
```json
{
  "api_key": "sk-your-new-dashscope-api-key",
  "model": "qwen-max"
}
```

---

## 3. 환경 변수(Environment Variable)로 재설정

Qwen 및 DashScope SDK는 설정 파일보다 **환경 변수(`DASHSCOPE_API_KEY`)를 우선 참조**합니다. 환경 변수를 새로 지정하면 잘못된 설정 파일 값을 즉시 덮어쓸 수 있습니다.

### Windows 환경

#### PowerShell (권장)
```powershell
# 1. 현재 터미널 세션에 적용
$env:DASHSCOPE_API_KEY="sk-your-new-dashscope-api-key"

# 2. 윈도우 사용자 환경변수에 영구 저장
[System.Environment]::SetEnvironmentVariable('DASHSCOPE_API_KEY', 'sk-your-new-dashscope-api-key', 'User')
```

#### 명령 프롬프트 (CMD)
```cmd
:: 1. 현재 세션 적용
set DASHSCOPE_API_KEY=sk-your-new-dashscope-api-key

:: 2. 영구 등록
setx DASHSCOPE_API_KEY "sk-your-new-dashscope-api-key"
```

### Linux / macOS 환경

```bash
# 1. 현재 세션 적용
export DASHSCOPE_API_KEY="sk-your-new-dashscope-api-key"

# 2. 영구 적용 (~/.bashrc 또는 ~/.zshrc)
echo 'export DASHSCOPE_API_KEY="sk-your-new-dashscope-api-key"' >> ~/.bashrc
source ~/.bashrc
```

---

## 4. API Key 등록 확인 및 테스트

키를 재등록한 후 정상 작동 여부를 확인합니다.

```bash
# 간단한 질의 테스트
qwen "Hello, who are you?"
# 또는
qwen run --prompt "테스트 확인"
```
