# Project Context: TIL (Today I Learned)

이 프로젝트는 MkDocs를 사용하여 구축된 개인 위키/문서화 사이트입니다.

## 🛠 Workflow & Rules

### 1. Git Workflow
- **Sync First**: 작업을 시작하기 전에 반드시 원격 저장소의 변경 사항을 가져와야 합니다.
  - Command: `git pull`

### 2. Pre-Commit Validation & Update
`update_recent_changes.py` 스크립트는 **Git Log**를 기반으로 동작하므로, 변경 사항이 커밋된 후에만 인식할 수 있습니다. 따라서 다음 순서를 따르세요.

**Commit Sequence:**
1. **콘텐츠 커밋**: 문서 변경 사항을 먼저 커밋합니다.
   - `git add <files>`
   - `git commit -m "docs: ..."`
2. **스크립트 실행**: 변경 내역을 반영하고 유효성을 검사합니다.
   - `python3 scripts/update_recent_changes.py`
   - `python3 scripts/validate_pages.py`
3. **Amend Commit**: 스크립트에 의해 변경된 파일(`Recent_Changes.md` 등)을 이전 커밋에 합칩니다.
   - `git add .`
   - `git commit --amend --no-edit`
4. **Push**: 최종 결과물을 원격 저장소에 반영합니다.
   - `git push`

### 3. Documentation Standards
- **Language**: 문서는 **한국어**로 작성하는 것을 원칙으로 합니다.
- **Structure**: 기존 디렉토리 구조(`docs/AI`, `docs/Tools` 등)를 준수하세요.
- **MkDocs**: 새로운 섹션을 추가할 때는 `mkdocs.yml` 설정과 각 폴더의 `.pages` 파일을 확인해야 합니다.

---
*새로운 규칙은 이 라인 위에 추가하세요.*
