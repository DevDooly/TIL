# Project Context: TIL (Today I Learned)

이 프로젝트는 MkDocs를 사용하여 구축된 개인 위키/문서화 사이트입니다.

## 🛠 Workflow & Rules

### 1. Git Workflow
- **Sync First**: 작업을 시작하기 전에 반드시 원격 저장소의 변경 사항을 가져와야 합니다.
  - Command: `git pull`

### 2. Pre-Commit Validation (필수)
변경 사항을 커밋하기 전에, **반드시** 다음 스크립트들을 순서대로 실행하여 문서의 일관성과 무결성을 확보해야 합니다.

1. **최근 변경 사항 업데이트**: `docs/Recent_Changes.md` 및 `README.md`를 갱신합니다.
   - Command: `python3 scripts/update_recent_changes.py`
2. **페이지 유효성 검사**: MkDocs의 `.pages` 설정을 검증하고 수정합니다.
   - Command: `python3 scripts/validate_pages.py`

**Commit Sequence:**
1. 콘텐츠(문서) 수정 또는 생성.
2. 위 스크립트 실행.
3. 콘텐츠 변경 사항과 스크립트에 의해 자동 업데이트된 파일들(`docs/Recent_Changes.md`, `README.md`, `.pages` 등)을 함께 Staging.
4. Commit 및 Push.

### 3. Documentation Standards
- **Language**: 문서는 **한국어**로 작성하는 것을 원칙으로 합니다.
- **Structure**: 기존 디렉토리 구조(`docs/AI`, `docs/Tools` 등)를 준수하세요.
- **MkDocs**: 새로운 섹션을 추가할 때는 `mkdocs.yml` 설정과 각 폴더의 `.pages` 파일을 확인해야 합니다.

---
*새로운 규칙은 이 라인 위에 추가하세요.*
