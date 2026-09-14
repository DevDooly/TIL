---
name: git-workflow
description: TIL의 Git 동기화, 한글 Conventional Commits, 문서 생성 목차 갱신과 검증 후 원격 반영을 처리한다. Git 작업, 커밋, push, 브랜치 요청과 docs 문서 편집 후 게시에 사용한다.
---

# TIL Git Workflow

아래 경로와 명령은 저장소 루트 기준이다. 문서 게시의 실행 순서는 `scripts/publish.sh`를 기준으로 한다.

## 작업 시작과 범위

```bash
git status --short --branch
git branch --show-current
git remote -v
```

작업 시작 시 사용자 변경을 파악하고 현재 브랜치의 upstream에서 `git pull --rebase`로 동기화한다. upstream이 없으면 대상 원격·브랜치를 먼저 확인한다. 작업 트리가 더럽거나 충돌하면 변경을 보존하며 해결하고, 임의로 reset·clean·stash하지 않는다.

`docs/` 문서 편집은 아래 자동 게시 흐름으로 마무리한다. 사용자가 "검토만", "로컬 수정만", "push하지 마"라고 요청하면 해당 범위가 우선이다. 스킬·설정만 변경하는 작업에 문서 자동 게시 규칙을 확대하지 않는다. 현재 브랜치와 이미 승인된 작업 범위를 유지한다.

## 한글 Conventional Commits

| Type | 사용 범위 | 예시 |
| :--- | :--- | :--- |
| `docs:` | 문서·가이드 | `docs: Oracle JSON 인덱스 선택 기준 추가` |
| `feat:` | 기능·도구·스크립트 추가 | `feat: 문서 검증 도구 추가` |
| `fix:` | 오류·깨진 링크 수정 | `fix: 데이터베이스 목차 경로 수정` |
| `refactor:` | 동작을 유지한 구조 개선 | `refactor: 문서 생성 로직 정리` |
| `chore:` | 설정·의존성·스킬 관리 | `chore: TIL 지식 업데이트 스킬 추가` |

제목은 50자 이내의 간결한 한글로 작성한다. 본문이 필요하면 변경 이유와 주요 내용을 적는다.

## 문서 게시

문서 내용과 탐색 연결은 `til-doc-verify`로 점검한다. `git diff`, `git diff --cached`, `git status --short`로 게시 대상과 새 파일을 확인한다. 비밀값·임시 결과물이나 무관한 사용자 변경을 포함하지 않는다.

`publish.sh`는 **`git add .`로 모든 변경을 스테이징**한다. 현재 변경 전체가 이번 작업에 속할 때 실행한다. 무관한 변경이 있으면 해당 변경을 건드리지 않는 별도 작업 공간 등으로 게시 범위를 분리한 뒤 진행한다.

```bash
bash scripts/publish.sh "docs: 변경 내용"
```

Windows에서는 Git Bash를 사용한다. 기본 Python 명령은 `python3`이며, Git Bash에서 다른 실행기를 쓰려면 다음처럼 지정한다.

```bash
PYTHON=python bash scripts/publish.sh "docs: 변경 내용"
```

이 스크립트는 다음 순서로 실행된다. 같은 작업을 별도로 먼저 커밋하거나 생성 스크립트를 중복 실행할 필요는 없다.

1. 콘텐츠를 스테이징하고 1차 커밋한다.
2. Markdown 자동 수정·검증, `.pages` 검증·정리, Recent Changes와 Sitemap 생성을 수행한다.
3. `.pages`를 다시 검증하고 기존 테스트와 `mkdocs build --strict`를 실행한다.
4. 생성·수정 결과를 스테이징하고 방금 만든 커밋을 amend한다.
5. 현재 브랜치의 설정된 upstream으로 `git push`한다.

`update_recent_changes.py`가 Git 이력을 읽으므로 콘텐츠 커밋이 생성 작업보다 먼저 와야 한다. 생성되는 README 영역과 `docs/Recent_Changes.md`, `docs/Sitemap.md`는 수동으로 이력을 만들어 채우지 않는다.

## 실패와 완료 확인

- 검증 실패 시 원격 반영은 중단되지만 로컬 콘텐츠 커밋과 자동 수정 파일은 남을 수 있다. 실패 단계와 `git status`, `git log -1`을 확인한 뒤 원인을 고친다.
- 변경이 없는 상태에서 publish를 재실행하면 즉시 끝나므로 실패한 게시가 완료됐다고 판단하지 않는다. 남은 생성·검증 단계를 통과한 뒤 해당 작업의 미게시 커밋만 보완하고 정상 push한다.
- push가 거절되면 원격 변경과 로컬 상태를 확인해 동기화한다. 이미 공유된 커밋을 amend하거나 force push하지 않는다.
- 마지막으로 `git status --short --branch`와 최신 커밋을 확인한다. 변경 내용, 검증 결과, 커밋·push 여부와 남은 작업을 간단히 전달한다.
