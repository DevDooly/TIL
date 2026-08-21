# Antigravity CLI (`agy`) 스킬 설치, 설정 및 활용 가이드

Google Antigravity(AGY)의 **스킬(Skills) 시스템**은 에이전트에게 프로젝트 전용 워크플로우, 복잡한 런북, 코딩 컨벤션, 자동화 도구를 온디맨드(On-Demand / Progressive Disclosure) 방식으로 주입하여 생산성을 극대화하는 커스터마이징 기능입니다.

---

## 1. 스킬(Skills) 설치 및 저장 위치 (Discovery Locations)

`agy`는 작업 디렉토리에서 프로젝트 루트까지 상위 경로를 탐색하여 스킬을 자동으로 검색(Discovery)하고 로드합니다.

```mermaid
graph TD
    subgraph 1. Workspace Project Skills 최우선
    WS[프로젝트 루트/.agents/skills/<skill-name>/] -->|Git 형상 관리 & 팀 공유| Agent
    end

    subgraph 2. Global Machine Skills
    Global[~/.gemini/config/skills/<skill-name>/] -->|모든 프로젝트 공통 적용| Agent
    end

    subgraph 3. Built-in Skills
    Builtin[AGY 내장 기본 스킬] --> Agent[Antigravity 에이전트]
    end
```

| 스킬 위치 | 경로 | 특징 및 용도 |
| :--- | :--- | :--- |
| **Workspace (프로젝트 전용)** | `<PROJECT_ROOT>/.agents/skills/<skill-name>/` | Git에 커밋하여 팀원 전체와 동일한 스킬을 공유할 때 사용 (**권장**) |
| **Global (사용자/머신 전역)** | `~/.gemini/config/skills/<skill-name>/` | 내 PC의 모든 프로젝트에서 공통으로 쓰고 싶은 개인 스킬 |
| **선언적 JSON 설정** | `<PROJECT_ROOT>/skills.json` | 외부 경로에 있는 스킬이나 공유 패키지를 명시적으로 임포트할 때 |

---

## 2. 스킬 디렉토리 표준 구조

하나의 스킬은 폴더 단위로 관리되며, 필수 파일인 `SKILL.md`와 보조 자원으로 구성됩니다.

```text
.agents/skills/my-awesome-skill/
├── SKILL.md          # [필수] 메인 지침 파일 (YAML Frontmatter + 가이드라인)
├── scripts/          # [선택] 스킬이 실행할 Python / Bash 보조 스크립트
├── examples/         # [선택] 참고할 예제 코드 및 템플릿
└── references/       # [선택] 대용량 매뉴얼 및 참조 문서
```

---

## 3. 스킬 설치 및 생성 방법 (3가지 방식)

### 방법 1: 로컬 프로젝트에 직접 생성 (가장 기본)

1. 프로젝트 루트에 스킬 디렉토리를 생성합니다:
   ```bash
   mkdir -p .agents/skills/git-commit-helper
   ```
2. `.agents/skills/git-commit-helper/SKILL.md` 파일을 생성하고 지침을 작성합니다:
   ```markdown
   ---
   name: git-commit-helper
   description: 코드 변경점을 분석하여 Conventional Commits 규칙에 맞춘 명확한 한글 커밋 메시지를 생성하는 스킬
   ---

   # Git 커밋 메시지 작성 규칙
   - 형식: `<type>(<scope>): <한글 설명>`
   - 제목은 50자 이내, 명령조(동사 원형)로 작성
   - 변경 사항이 문서일 경우 `docs:`, 버그 수정일 경우 `fix:`, 기능 추가는 `feat:` 사용
   ```

---

### 방법 2: 공개 스킬 리포지토리 클론 (Git Submodule 활용)

오픈소스 스킬 모음이나 사내 공유 스킬 리포지토리를 서브모듈로 추가합니다:

```bash
git submodule add https://github.com/my-org/shared-agy-skills.git .agents/skills/shared
```

---

### 방법 3: `skills.json`을 통한 외부 스킬 등록

프로젝트 루트의 `skills.json`에 외부 경로나 전역 스킬의 경로를 명시합니다:

```json
{
  "skills": [
    {
      "name": "corporate-security-audit",
      "path": "/opt/company-rules/skills/security-audit"
    }
  ]
}
```

---

## 4. `SKILL.md` 작성 규격 및 Frontmatter 스펙

`SKILL.md` 파일 상단의 YAML Frontmatter는 **에이전트가 해당 스킬을 언제 로드할지 결정하는 가장 중요한 메타데이터**입니다.

```markdown
---
name: k8s-deploy-helper
description: >
  Kubernetes Deployment, Service, Ingress YAML 매니페스트를 검증하고,
  리소스 리밋, 헬스체크 프로브, 보안 컨텍스트(SecurityContext) 누락을 점검하는 스킬.
  K8s YAML 작성 또는 배포 관련 질문 시 활성화됨.
---

# 쿠버네티스 매니페스트 검증 및 가이드라인

## 1. 보안 필수 점검 항목
- `runAsNonRoot: true` 설정 확인
- `readOnlyRootFilesystem: true` 권장

## 2. 리소스 설정
- 모든 컨테이너는 `requests`와 `limits` (CPU/Memory)를 반드시 명시해야 함
```

> **💡 작성 팁 (Progressive Disclosure)**  
> Antigravity는 모든 스킬의 전문을 항상 컨텍스트에 띄워두지 않고, `description`만 메모리에 올려둡니다. 사용자의 요청이 `description`의 내용과 부합할 때만 전체 문서를 온디맨드로 로드하므로, **`description`에 어떤 상황에서 이 스킬을 써야 하는지 구체적으로 기술**해야 정확히 작동합니다.

---

## 5. 스킬 실행 및 동작 방식

1. **자동 활성화 (자연어 트리거)**:
   - 사용자가 `"k8s 배포 파일 검토해줘"`라고 요청하면, 에이전트가 `k8s-deploy-helper`의 description을 인식하고 자동으로 스킬 문서를 읽어 지침을 준수합니다.
2. **명시적 호출**:
   - 대화창에서 특정 스킬을 콕 집어 호출할 수도 있습니다:
     > *"git-commit-helper 스킬을 참고해서 이번 작업 커밋해줘"*

---

## 6. 실무 추천 스킬 카테고리 & 활용 예제

| 스킬 분류 | 스킬 이름 예시 | 주요 역할 |
| :--- | :--- | :--- |
| **🛠️ 코드 품질 & 리팩토링** | `code-refactor` | 복잡도 높은 함수 분해, 디자인 패턴 적용, 클린 코드 준수 |
| **🧪 테스트 & TDD** | `test-generator` | JUnit, Pytest, Jest 테스트 코드 자동 생성 및 Mock 설정 |
| **🚀 Git & DevOps** | `git-workflow` | Conventional Commit 한글 커밋 메시지, PR 설명 자동 작성 |
| **📚 문서화** | `til-doc-sync` | Recent_Changes.md, README 동기화 및 검증 스크립트 실행 |
| **🛡️ 보안 검증** | `security-scan` | 하드코딩된 Secret, SQL Injection, 의존성 취약점 탐지 |

---

## 7. 필수 내장 슬래시 커맨드 (Slash Commands)

| 슬래시 커맨드 | 용도 및 특징 | 추천 활용 상황 |
| :--- | :--- | :--- |
| **`/plan`** | 복잡한 작업 전 **단계별 실행 계획(Plan)** 수립 | 3개 이상의 파일 수정이나 아키텍처 설계 시 |
| **`/goal`** | **장시간 자율 모드** (목표 완료 시까지 멈추지 않고 반복 수행) | 대규모 리팩토링이나 빌드/테스트 에러가 완전히 잡힐 때까지 |
| **`/grill-me`** | **인터뷰 모드** (에이전트가 개발자에게 역질문하여 요구사항 구체화) | 설계 결정이 모호하거나 트레이드오프 검토 시 |
| **`/learn`** | 사용자의 교정 사항이나 선호도를 **영구 메모리(Memory)**로 저장 | 커밋 규칙, 언어 설정, 자동 push 선호도 등을 학습시킬 때 |
| **`/schedule`** | 일회성 타이머 또는 Cron 주기 작업 스케줄링 | 배포 상태 폴링이나 백그라운드 주기 작업 감시 |

---

## 8. MCP (Model Context Protocol) 도구 연동

외부 도구(DB, GitHub, 웹 검색 등)를 `agy`에 붙여 에이전트가 도구로 직접 호출하게 합니다.

`~/.gemini/config/mcp_config.json` 설정:
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
