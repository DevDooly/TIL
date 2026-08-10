# Claude CLI - DeepSeek 모델 연동 가이드 (Windows)

Windows 환경에서 `npm`으로 설치한 **Claude CLI (Claude Code)**에 DeepSeek의 API 및 커스텀 모델(`deepseek-v4-flash-0731` 등)을 연동하는 설정 방법입니다.

---

## 1. 설정 파일 경로 (Windows)

Claude CLI는 사용자 홈 디렉토리의 `.claude` 폴더에서 설정을 읽어옵니다.

* **전역(Global) 설정 파일 경로**:
  ```text
  %USERPROFILE%\.claude\settings.json
  # 실제 경로 예: C:\Users\<사용자명>\.claude\settings.json
  ```
* **프로젝트별(Local) 설정 파일 경로**:
  ```text
  <프로젝트_루트_디렉토리>\.claude\settings.json
  ```

> 폴더나 파일이 없다면 직접 `.claude` 폴더를 생성하고 `settings.json` 파일을 만들어주시면 됩니다.

---

## 2. 심플 `settings.json` 설정 예시

### 기본 설정 (DeepSeek API 직접 연동)

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.deepseek.com/v1",
    "ANTHROPIC_API_KEY": "sk-your-deepseek-api-key"
  },
  "model": "deepseek-v4-flash-0731"
}
```

### OpenAI 호환 / 커스텀 엔드포인트 형식

일부 CLI 패키지 또는 프록시를 사용할 경우 아래와 같은 키 구조를 사용할 수도 있습니다.

```json
{
  "apiKey": "sk-your-deepseek-api-key",
  "baseUrl": "https://api.deepseek.com/v1",
  "model": "deepseek-v4-flash-0731"
}
```

### OpenRouter 등 프록시를 경유하는 경우

OpenRouter를 통해 DeepSeek 모델을 라우팅할 때의 예시입니다.

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://openrouter.ai/api/v1",
    "ANTHROPIC_API_KEY": "sk-or-your-openrouter-key"
  },
  "model": "deepseek/deepseek-v4-flash-0731"
}
```

---

## 3. Windows PowerShell 환경 변수로 임시 실행

`settings.json` 수정 없이 터미널 세션에서 즉시 실행하고자 할 때는 PowerShell에서 환경 변수를 설정 후 실행할 수 있습니다.

```powershell
# 1. API Key 및 Base URL 설정
$env:ANTHROPIC_API_KEY="sk-your-deepseek-api-key"
$env:ANTHROPIC_BASE_URL="https://api.deepseek.com/v1"

# 2. 특정 모델을 지정하여 실행
claude --model deepseek-v4-flash-0731
```

---

## 4. 주요 확인 사항 및 트러블슈팅

1. **API Key 유효성**: DeepSeek Open Platform에서 발급받은 `sk-`로 시작하는 유효한 API Key인지 확인합니다.
2. **엔드포인트 URL**:
   * 기본 DeepSeek 엔드포인트는 `https://api.deepseek.com` 또는 `https://api.deepseek.com/v1` 입니다.
   * 클라이언트가 `/chat/completions` 또는 `/messages` 경로를 붙이는 방식에 맞춰 `v1` 포함 여부를 확인합니다.
3. **토큰 및 모델명 매핑**: `deepseek-v4-flash-0731`과 같이 사용하려는 정확한 모델 식별자명을 입력했는지 확인합니다.
