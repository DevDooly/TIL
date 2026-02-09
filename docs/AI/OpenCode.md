# OpenCode

**OpenCode**는 개발자를 위해 설계된 오픈소스 AI 코딩 어시스턴트입니다. 터미널, IDE, 또는 데스크탑 애플리케이션 형태로 동작하며, 로컬 개발 환경과 깊게 통합되어 강력한 기능을 제공합니다.

## 💡 주요 특징

### 1. 터미널 기반 인터페이스 (TUI)
Go 언어로 작성된 CLI 애플리케이션으로, 터미널 내에서 바로 AI 모델과 상호작용할 수 있습니다. 개발자가 터미널을 떠나지 않고도 AI의 도움을 받을 수 있어 문맥 전환 비용을 줄여줍니다.

### 2. 문맥 인식 (Context Awareness)
단순한 챗봇과 달리, OpenCode는 **로컬 파일 시스템, Git 히스토리, 현재 작업 중인 코드의 문맥**을 이해합니다.
- `opencode explain this function`과 같은 명령을 내리면 관련 코드를 자동으로 파악하여 답변합니다.

### 3. 다양한 모델 지원
- **Models.dev**를 통해 75개 이상의 LLM 제공업체와 연결됩니다.
- **GitHub Copilot**, **ChatGPT Plus/Pro** 계정과 연동할 수 있습니다.
- **Ollama** 등을 통해 로컬에서 실행되는 오픈소스 모델도 지원합니다.

### 4. 에이전트 (Agents)
단순한 질의응답을 넘어 특정 작업을 수행하는 에이전트 기능을 내장하고 있습니다.
- **Build Agent:** 개발 빌드 관련 작업을 지원
- **Plan Agent:** 코드 분석 및 탐색 계획 수립

---

## 🚀 설치 및 사용

GitHub 저장소에서 소스를 받아 빌드하거나 바이너리를 설치하여 사용할 수 있습니다.

```bash
# 설치 예시 (Go 필요)
go install github.com/opencode-ai/opencode@latest
```

## References
- [Official Website](https://opencode.ai)
- [GitHub Repository](https://github.com/opencode-ai/opencode)
