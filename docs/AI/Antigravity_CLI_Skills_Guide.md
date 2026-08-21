# Antigravity CLI (`agy`) 유용한 스킬 및 확장 가이드

Google Antigravity(AGY)의 **스킬(Skills) 시스템**은 에이전트에게 프로젝트 전용 워크플로우, 복잡한 런북, 코딩 컨벤션, 자동화 도구를 온디맨드(On-Demand / Progressive Disclosure) 방식으로 주입하여 생산성을 극대화하는 커스터마이징 기능입니다.

실무에서 바로 활용하기 좋은 **추천 스킬 분류**, **핵심 슬래시 커맨드**, **MCP 서버 연동**, 그리고 **나만의 커스텀 스킬 제작법**을 정리합니다.

---

## 1. 실무 추천 스킬 카테고리 (Featured Skills)

```mermaid
graph TD
    AGY[Antigravity CLI agy] --> S1[🛠️ 코드 품질 & 리팩토링 스킬]
    AGY --> S2[🧪 테스트 & TDD 자동화 스킬]
    AGY --> S3[🚀 Git & CI/CD DevOps 스킬]
    AGY --> S4[📚 문서화 & 지식 베이스 관리 스킬]
    AGY --> S5[🔌 MCP 외부 도구 연동 스킬]
```

### 1) 🛠️ 코드 품질 & 대규모 리팩토링 스킬
* **`code-refactoring` (클린 코드 & 아키텍처 리팩토링)**:
  * 중복 코드 탐지, 레거시 코드 패턴 현대화, 디자인 패턴 적용.
  * 복잡도(Cyclomatic Complexity)가 높은 함수를 작은 단위로 분해.
* **`security-audit` (보안 취약점 및 민감 정보 스캐닝)**:
  * 소스 코드 내 하드코딩된 API Key, 토큰, 비밀번호 탐지.
  * SQL Injection, XSS, 취약한 의존성 라이브러리 검사 및 패치.

### 2) 🧪 테스트 & TDD 자동화 스킬
* **`test-generator` (단위/통합 테스트 자동 생성)**:
  * 변경된 코드 및 엣지 케이스(Edge cases)에 대한 JUnit/Pytest/Jest 테스트 코드 자동 작성.
  * Mock 객체 구성 및 테스트 커버리지 리포트 분석.
* **`e2e-browser-test` (Playwright / Puppeteer 웹 UI 검증)**:
  * 웹 애플리케이션 화면 렌더링, 폼 입력, 버튼 클릭 흐름을 가상 브라우저로 자동 검증.

### 3) 🚀 Git & CI/CD / DevOps 스킬
* **`git-workflow` (커밋 & PR 자동화)**:
  * Conventional Commits 규칙에 맞춘 간결하고 명확한 한글 커밋 메시지 생성.
  * 변경 사항을 요약한 GitHub Pull Request 본문(Description) 및 릴리즈 노트 자동 작성.
* **`k8s-manifest-linter` (쿠버네티스 & Docker 검증)**:
  * Dockerfile 멀티스테이지 빌드 최적화.
  * K8s Deployment, Service, Ingress YAML의 보안(SecurityContext), 리소스 리밋 설정 검증.

### 4) 📚 문서화 & 지식 베이스(TIL/Wiki) 동기화 스킬
* **`doc-updater` (문서 자동 동기화)**:
  * 코드 변경에 따른 `README.md`, API 문서, 변경 이력(Recent Changes) 자동 갱신.
  * MkDocs `.pages` 네비게이션 트리 정합성 자동 검증.

---

## 2. 필수 내장 슬래시 커맨드 (Slash Commands)

별도의 스킬 설치 없이도 `agy` 대화 중 즉시 실행할 수 있는 핵심 모드입니다.

| 슬래시 커맨드 | 용도 및 특징 | 실무 활용 팁 |
| :--- | :--- | :--- |
| **`/plan`** | 복잡한 요구사항에 대해 실행 전 **단계별 계획(Plan)**을 수립 | 3개 이상의 파일 수정이나 아키텍처 설계 시 필수 사용 |
| **`/goal`** | 장시간 자율 모드 (목표 달성 시까지 멈추지 않고 반복 수행) | 대규모 리팩토링이나 빌드/테스트 성공할 때까지 자동 수정 |
| **`/grill-me`** | 인터뷰 모드 (에이전트가 개발자에게 역질문하여 요구사항 구체화) | 불명확한 설계 결정이나 아키텍처 선택 시 최적의 답 도출 |
| **`/learn`** | 사용자의 교정 사항이나 선호도를 **영구 규칙(Memory)**으로 저장 | 프로젝트 룰, 컨벤션, 자동 push 선호도 등을 학습시킬 때 |
| **`/schedule`** | 일회성 타이머 또는 Cron 주기 작업 스케줄링 | 배포 상태 폴링이나 백그라운드 주기 작업 감시 |

---

## 3. 강력한 MCP (Model Context Protocol) 연동 스킬

MCP(Model Context Protocol)를 통해 `agy`에 데이터베이스, 외부 모니터링, 검색 도구를 연결할 수 있습니다.

`~/.gemini/config/mcp_config.json` 또는 `.agents/mcp_config.json` 설정:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your-github-token"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://user:password@localhost:5432/mydb"]
    },
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "your-brave-api-key"
      }
    }
  }
}
```

* **효과**: 에이전트가 DB 스키마 직접 조회, GitHub 이슈/PR 실시간 조회, 최신 웹 검색을 도구(Tool)로 직접 호출하여 작업합니다.

---

## 4. 나만의 커스텀 스킬(Skill) 만들기

프로젝트 저장소의 `.agents/skills/<스킬이름>/SKILL.md` (또는 `~/.gemini/config/skills/<스킬이름>/SKILL.md`)에 작성하면 `agy`가 자동으로 인식합니다.

### 📝 예시: `til-doc-sync` 스킬 만들기

`.agents/skills/til-doc-sync/SKILL.md`:
```markdown
---
name: til-doc-sync
description: TIL 문서 작성 후 최근 변경 이력(Recent_Changes.md)과 README를 갱신하고 Git push까지 자동 처리하는 스킬
---

# TIL 문서 동기화 및 검증 절차

문서 변경 작업이 발생하면 반드시 다음 순서를 준수하여 실행합니다:

1. **내용 커밋**: 변경된 마크다운 문서를 먼저 스테이징 및 한글 커밋 메시지로 커밋합니다.
2. **검증 스크립트 실행**:
   ```bash
   python3 scripts/update_recent_changes.py
   python3 scripts/validate_pages.py
   ```
3. **자동 갱신 파일 커밋**: 업데이트된 `README.md`, `docs/Recent_Changes.md`를 amend 커밋에 포함합니다.
4. **원격 푸시**: `git push origin main`을 실행하여 원격 저장소에 반영합니다.
```

---

## 5. 로딩 우선순위 (Priority)

Antigravity는 커스터마이징 요소를 다음 우선순위로 로드합니다:

1. **Workspace Project (`.agents/skills/`)** - 프로젝트별 전용 스킬 (최우선)
2. **Global Config (`~/.gemini/config/skills/`)** - PC 로컬 전역 스킬
3. **Built-in Skills** - Antigravity 기본 내장 스킬
