# OpenCode

**OpenCode**는 개발자를 위해 설계된 모델 독립적(Model-agnostic) 오픈소스 AI 코딩 어시스턴트입니다. 터미널(TUI/CLI), IDE, 데스크탑 또는 **Paseo**와 같은 오케스트레이터의 백엔드 프로바이더로 동작하며, 로컬 파일과 Git 히스토리를 이해하여 코딩 작업을 돕습니다.

---

## 💡 주요 특징

### 1. 터미널 기반 인터페이스 (TUI) & Provider 모드
CLI 인터페이스를 제공하여 터미널 내에서 바로 AI 모델과 상호작용하거나, Paseo와 같은 에이전트 제어 플레인의 실행 엔진으로 연동됩니다.

### 2. 폭넓은 LLM 모델 지원 (Google Gemini, OpenAI, Claude, DeepSeek 등)
* **Google Gemini 지원**: `GEMINI_API_KEY` 환경 변수 또는 Google AI Studio 계정 연동을 통해 **Gemini 3.7 Flash, 2.5 Pro, 2.0 Flash** 등 최신 제미나이 모델을 바로 사용 가능합니다.
* **OpenAI / Anthropic**: GPT-4o, GPT-5 계열, Claude 3.5 Sonnet 등 지원
* **Ollama**: 로컬에서 구동되는 오픈소스 LLM(DeepSeek R1, Llama 3 등) 연동 지원

### 3. 문맥 인식 (Context Awareness)
로컬 파일 시스템, Git 히스토리, 현재 작업 중인 코드의 문맥을 깊이 있게 분석하여 패치 및 리팩토링을 수행합니다.

---

## 🚀 설치 및 Gemini 연동

### 1) 글로벌 설치 (Node.js / npm)
```bash
npm install -g opencode-ai
```

### 2) Gemini API Key 설정
```bash
# 환경 변수 등록
export GEMINI_API_KEY="your-gemini-api-key"
```

### 3) 실행 예시
```bash
# CLI 직접 실행 (모델 지정)
opencode --model google/gemini-3.7-flash

# 또는 TUI 대화 모드
opencode
```

---

## 🔗 Paseo와의 연동

Paseo 데몬을 구동하면 OpenCode가 자동으로 프로바이더로 등록되어, **스마트폰(Paseo 모바일 앱)에서 Provider를 OpenCode로 선택하고 Gemini 모델로 코딩 에이전트를 원격 제어**할 수 있습니다.

## References

- [Official Website](https://opencode.ai)
- [GitHub Repository](https://github.com/opencode-ai/opencode)
