# AI Tools & Agents

인공지능(AI) 기술이 발전함에 따라 개발 생산성을 높이고 작업을 자동화하는 다양한 AI 도구와 에이전트들이 등장하고 있습니다. 이 섹션에서는 오픈소스로 제공되는 유용한 AI 도구들을 정리합니다.

## 🤖 Featured Tools & Guides

### [AI Agent 개발 직군 및 엔지니어링 가이드](AI_Agent_Developer_Role_and_Engineering.md)
채용 시장에서 요구하는 **AI Agent 개발자의 역할과 의미**, 챗봇과의 차이점, 4대 핵심 아키텍처(Brain, Planning, Memory, Tools), LangGraph 기반 상태 머신 설계, 결정론적 가드레일 및 Observability(Eval) 파이프라인 실무 가이드입니다.

### [TypeSafe AI Jev (`jev.`) - System One 의사결정 모델](TypeSafe_AI_Jev.md)
2026년 9월 TypeSafe AI가 공개한 **비생성형 인공지능 의사결정 모델(System One Model)**로, 텍스트 생성 없이 단일 병렬 패스로 `Choice`(범주 선택), `Score`(척도 평가), `Noul`(참/거짓 확률)을 반환하는 아키텍처와 활용법을 다룹니다.

### [OpenCode](OpenCode.md)
개발자를 위한 **오픈소스 AI 코딩 어시스턴트**입니다. 터미널(CLI/TUI) 기반으로 동작하며, 로컬 파일과 Git 히스토리를 이해하여 코딩 작업을 돕습니다.

### [OpenClaw](OpenClaw.md)
사용자의 디바이스나 서버에서 직접 구동되는 **오픈소스 개인용 AI 에이전트**입니다. 메시징 앱(Discord, Telegram 등)과 연동되어 쉘 명령 실행, 파일 관리, 웹 검색 등 다양한 작업을 자율적으로 수행할 수 있습니다.

### [Gemini CLI](Gemini_CLI.md)
터미널 기반 **대화형 AI 에이전트**입니다. 코드베이스 분석, 리팩토링, 버그 수정, 문서 작성 등 소프트웨어 엔지니어링 작업에 특화되어 있습니다.

### [Gemini 4 Argon 추론 단계(Low · Medium · High) 비교](Gemini_4_Argon_Reasoning_Levels.md)
`gemini-4-argon` 모델의 `thinking_level`(`low`, `medium`, `high`) 설정별 추론 토큰 소비량, 응답 지연 시간, 과금 구조와 `max_output_tokens`·Long Decode 설정 기준을 정리합니다.

### [Antigravity CLI 설정](Antigravity_CLI_Configuration.md)
Google Antigravity CLI(`agy`)에서 파일 생성, 수정 및 명령어 실행 시 확인(Approval) 절차를 생략하고 자동 승인(Auto-approve)하는 설정 가이드입니다.

### [Antigravity CLI 스킬 및 확장 가이드](Antigravity_CLI_Skills_Guide.md)
`agy`에서 생산성을 극대화하기 위한 추천 스킬 분류(리팩토링, 테스트, CI/CD, 문서화), 핵심 슬래시 커맨드(`/plan`, `/goal`, `/grill-me`), MCP 서버 연동 및 커스텀 스킬 제작 가이드입니다.

### [Antigravity CLI (agy) vs OpenCode 비교](AGY_vs_OpenCode_Comparison.md)
Google DeepMind의 고도화된 에이전트 플랫폼 **Antigravity CLI (`agy`)**와 가볍고 유연한 오픈소스 코딩 도구 **OpenCode (+ Gemini)**의 아키텍처, 기능, 장단점 및 상황별 선택 가이드입니다.

### [MCP (Model Context Protocol) 서버 개발 가이드](MCP_Server_Development_Guide.md)
AI 클라이언트(Claude, Cursor, AGY 등)와 외부 도구/데이터를 표준화된 방식으로 연결하는 **MCP 서버 개발 가이드**(Python FastMCP, TypeScript SDK, MCP Inspector 디버깅 및 실무 주의사항)입니다.

### [Claude CLI (다중 모델 & DeepSeek 연동)](Claude_CLI_DeepSeek_Setup.md)
Claude CLI(Claude Code)에서 `settings.json`, PowerShell 프로필 및 환경 변수를 활용하여 DeepSeek 등 다중 모델을 연동하고 전환하는 설정 가이드입니다.

### [Qwen CLI](Qwen_CLI_Setup.md)
Qwen CLI 및 DashScope 환경에서 API Key를 재등록하거나 환경 변수를 재설정하는 가이드입니다.

### [AI 코딩 에이전트 오케스트레이터 (Orca & Paseo)](AI_Coding_Agent_Orchestrators_Orca_Paseo.md)
Claude Code, Codex 등 다중 자율형 AI 코딩 에이전트를 병렬로 실행하고 조율하는 대표적인 오케스트레이터인 **Orca**(Git Worktree 격리 기반 ADE)와 **Paseo**(셀프 호스팅 데몬 기반 멀티 디바이스 제어 플레인)의 개념, 아키텍처 및 비교 분석 가이드입니다.

### [Paseo 설치 및 모바일 연동](Paseo_Setup_and_Usage.md)
Paseo CLI 및 데몬 설치, Relay 기반 외부 접속 설정 및 스마트폰(Android/iOS) 앱 페어링 가이드입니다.

### [n8n](n8n.md)
확장성이 뛰어난 **워크플로우 자동화 도구**입니다. 노드 기반 인터페이스를 통해 다양한 앱과 AI 모델(OpenAI, LangChain 등)을 연결하여 강력한 자동화 시스템을 구축할 수 있습니다.
