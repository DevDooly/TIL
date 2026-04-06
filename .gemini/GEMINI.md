# Project Context: TIL (Today I Learned)

이 프로젝트는 MkDocs를 사용하여 구축된 개인 위키/문서화 사이트입니다.

## 🛠 Workflow & Rules

### 1. Git Workflow
- **Sync First**: 작업을 시작하기 전에 반드시 원격 저장소의 변경 사항을 가져와야 합니다.
  - Command: `git pull`

- For this project (TIL), use the following single-step command for all documentation updates:
  './scripts/publish.sh "[Commit Message]"'
  This script automatically handles:
  1. Staging and initial commit.
  2. Running all validation and maintenance scripts (Recent Changes, Sitemap, etc.).
  3. Amending the commit with auto-generated updates.
  4. Pushing to the remote repository.
  This ensures the git log used by the scripts is always up to date and consistent.


### 3. Documentation Standards
- **Language**: 문서는 **한국어**로 작성하는 것을 원칙으로 합니다.
- **Structure**: 기존 디렉토리 구조(`docs/AI`, `docs/Tools` 등)를 준수하세요.
- **MkDocs**: 새로운 섹션을 추가할 때는 `mkdocs.yml` 설정과 각 폴더의 `.pages` 파일을 확인해야 합니다.

---
*새로운 규칙은 이 라인 위에 추가하세요.*
