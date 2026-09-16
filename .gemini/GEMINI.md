# Project Context: TIL (Today I Learned)

이 프로젝트는 MkDocs를 사용하여 구축된 개인 위키/문서화 사이트입니다.

## 🛠 Workflow & Rules

### 1. Git Workflow

- **Sync First**: 작업을 시작하기 전에 반드시 원격 저장소의 변경 사항을 가져와야 합니다.
  - 먼저 `git status --short --branch`로 사용자 변경과 브랜치를 확인하고, 안전하게 동기화할 수 있을 때 `git pull --rebase`를 실행합니다.

- `docs/` 문서 업데이트는 `bash scripts/publish.sh "docs: 변경 내용"`으로 반영합니다. 스킬·설정만 바꾸는 작업에는 이 자동 게시 규칙을 확대하지 않습니다.
- 이 스크립트는 콘텐츠 커밋 → 서식·목차 생성과 검증 → 테스트·빌드 → amend → push 순서로 처리합니다. Git 이력을 읽는 생성 작업보다 콘텐츠 커밋이 먼저 있어야 합니다.
- 세부 절차와 실패 시 처리는 `.agents/skills/git-workflow/SKILL.md`를 따릅니다.


### 2. Documentation Standards

- **Language**: 문서는 **한국어**로 작성하는 것을 원칙으로 합니다.
- **문체**: 한국어 문서를 작성·수정할 때 `.agents/skills/til-natural-writing/SKILL.md`를 함께 적용합니다. 구체적인 현상과 이유부터 설명하고, 관례적인 작성일·확인일과 반복적인 편집 지시는 본문에 붙이지 않습니다. 재현에 필요한 버전과 사건의 실제 날짜는 유지합니다.
- **Structure**: 기존 디렉토리 구조(`docs/AI`, `docs/Tools` 등)를 준수하세요.
- **MkDocs**: 새로운 섹션을 추가할 때는 `mkdocs.yml` 설정과 각 폴더의 `.pages` 파일을 확인해야 합니다.

### 3. 지식 업데이트 스킬

스킬 원본은 `.agents/skills/`에 둡니다. 요청에 해당하는 스킬만 활성화하고, 자동 선택이 되지 않으면 해당 `SKILL.md`를 읽어 적용합니다. 모든 스킬 전문을 한꺼번에 불러오지 않습니다. 아래 경로는 저장소 루트 기준입니다.

| 요청 | 읽을 스킬 |
| :--- | :--- |
| 새 지식·비교·링크·메모를 TIL 문서로 저장 | `.agents/skills/til-knowledge-write/SKILL.md` |
| 기존 문서의 최신성·버전·기술 설명 갱신 | `.agents/skills/til-knowledge-refresh/SKILL.md` |
| 오류·장애·해결 과정·재현 결과 기록 | `.agents/skills/til-troubleshooting/SKILL.md` |
| 한국어 문서 작성·수정의 문체, 딱딱한 표현과 불필요한 날짜 정리 | `.agents/skills/til-natural-writing/SKILL.md` |
| 문서 편집 후 목차·링크·예제·빌드 검증 | `.agents/skills/til-doc-verify/SKILL.md` |
| 커밋·원격 반영 | `.agents/skills/git-workflow/SKILL.md` |

- 먼저 관련 기존 문서를 검색하고 필요한 파일·절만 읽습니다. 사용자의 질문과 적용 환경을 중심으로 작성합니다.
- 사용자가 선택한 Gemini 모델을 유지합니다. 이 스킬 사용을 위해 모델 ID나 전역 설정을 변경할 필요는 없습니다.
- 버전·기본값·지원 여부는 실제 읽은 공식 근거로 확인합니다. 확인한 사실, 추론, 실행하지 않은 예제를 구분합니다.
- 단순 설명 요청은 파일 저장으로 확대하지 않습니다. "검토만", "로컬 수정만", "push하지 마" 같은 현재 요청은 기본 게시 흐름보다 우선합니다.
- `publish.sh`는 모든 변경을 스테이징합니다. 작업 전후 상태를 확인하고 무관한 사용자 변경을 함께 커밋하지 않습니다. 검증만 요청받았을 때는 실행하지 않습니다.

---
*새로운 규칙은 이 라인 위에 추가하세요.*
