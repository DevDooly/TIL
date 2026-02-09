# OpenClaw

**OpenClaw** (과거 Clawdbot, Moltbot)는 사용자가 직접 호스팅(Self-hosted)하여 사용하는 **오픈소스 개인용 AI 에이전트**입니다. 클라우드 서비스에 의존하지 않고 로컬 환경이나 개인 서버에서 구동되어 데이터 프라이버시를 중시하는 사용자에게 적합합니다.

## 💡 주요 특징

### 1. 자율적인 작업 수행 (Autonomous Task Execution)
단순히 대화만 하는 것이 아니라, **실제 작업을 수행**할 수 있는 능력을 갖추고 있습니다.
- 쉘 명령어 실행 (Shell Execution)
- 파일 시스템 관리 (File Management)
- 웹 검색 및 브라우징
- 스크립트 작성 및 실행

### 2. 멀티 플랫폼 통신
다양한 메신저 및 협업 도구와 연동되어, 채팅을 통해 명령을 내리고 결과를 받을 수 있습니다.
- **지원 플랫폼:** WhatsApp, Telegram, Discord, Slack, Google Chat, Signal, Microsoft Teams 등

### 3. LLM 및 외부 API 연동
다양한 대규모 언어 모델(LLM)과 연결하여 자연어 명령을 해석하고 처리합니다. 또한 외부 API와 연동하여 이메일 전송, 브라우저 제어 등 확장된 기능을 수행할 수 있습니다.

---

## ⚠️ 보안 주의사항

OpenClaw는 **쉘 명령 실행, 파일 읽기/쓰기** 등 시스템에 대한 강력한 권한을 가질 수 있습니다.
- **보안 설정:** 잘못된 설정이나 악의적인 명령 주입(Prompt Injection)에 취약할 수 있으므로, 샌드박스 환경에서 실행하거나 권한을 철저히 제한해야 합니다.
- **API 키 관리:** API 키나 민감한 정보가 유출되지 않도록 주의해야 합니다.

## References
- [OpenClaw GitHub](https://github.com/OpenClaw/OpenClaw) (※ 프로젝트명이 변경되었을 수 있으니 최신 리포지토리 확인 필요)
