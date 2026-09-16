---
name: til-doc-verify
description: TIL 문서를 추가·수정한 뒤 MkDocs 탐색 구조, 내부 링크, 마크다운 서식, 코드 예제와 빌드를 검증한다. "문서 검증", "목차 누락 확인", "반영 전 점검" 또는 TIL 문서 편집 마무리에 사용한다. 기술 주장의 최신성 조사에는 til-knowledge-refresh를 사용한다.
---

# TIL 문서 검증

문서 내용 검토와 빌드 검증을 구분하고 실제 수행한 범위만 보고한다. 모든 명령은 저장소 루트에서 실행한다.

## 변경 범위

```bash
git status --short
git diff --name-status
git diff --cached --name-status
```

새 파일은 diff에 안 나올 수 있으므로 `git status`도 확인한다. 작업 시작 시 있던 사용자 변경을 구분한다. 검토만 요청받았다면 원본을 수정하지 않는다.

## 탐색과 렌더링

- 새 문서가 있는 폴더의 `.pages`에 명시적 `nav`가 있으면 실제 상대 경로로 추가한다. 상위 탐색에서도 폴더에 도달할 수 있는지 확인한다. `validate_pages.py`는 기존 경로의 유효성을 확인할 뿐 새 파일의 등록 누락은 잡아주지 않는다.
- 관련 카테고리의 `README.md` 링크를 보완한다. 트러블슈팅 사례는 `docs/Troubleshooting/README.md`의 해당 표에도 연결한다.
- 내부 링크는 그 링크를 포함한 Markdown 파일을 기준으로 해석한다. 파일·제목 변경 시 들어오는 링크와 앵커도 찾는다. Windows에서도 링크 구분자는 `/`를 쓰고 파일명의 대소문자를 정확히 맞춘다.
- 목록 앞에는 빈 줄을 넣고 코드 펜스를 닫는다. 언어 식별자를 지정하며, Mermaid·admonition·탭 문법은 `mkdocs.yml`에 설정된 확장을 따른다.
- 본문은 `til-natural-writing` 기준으로 읽는다. 반복 확인일, 편집 지시, 근거 없는 경험이나 성과를 덧붙이지 않았는지 살피되, 실제 사건 날짜와 재현에 필요한 버전·조건은 보존한다.
- `mkdocs.yml`은 새 확장이나 사이트 설정이 필요할 때만 바꾼다. 생성되는 `site/`는 편집·커밋하지 않는다.

## 검증 명령과 한계

`requirements.txt`의 Python 의존성, JDK 21 이상, Bash가 전제다. Windows에서는 Git Bash를 쓰며 시스템의 `bash`가 WSL 실행기인지 확인한다. 사용 가능한 Python 실행기를 일관되게 사용한다.

```bash
python scripts/validate_markdown_lists.py
python scripts/validate_pages.py
python -m unittest discover -s scripts/tests -p 'test_*.py'
python -m mkdocs build --strict
git diff --check
```

명령을 차례로 실행하고 각각의 종료 코드를 확인한다. PowerShell에서도 앞선 실패를 마지막 명령의 성공으로 덮어 해석하지 않는다. 실패하면 원인을 확인하고 관련 변경을 고친 뒤 해당 검증을 다시 실행한다.

- `validate_pages.py`는 `.pages` 후행 슬래시를 고칠 수 있다. 편집 작업에서는 실행 후 diff를 확인한다. 읽기 전용 검토에서는 임시 복사본에서 실행하거나 실행하지 못한 항목으로 보고한다.
- `scripts/tests/test_java_examples.py`는 일부 기존 Java 예제만 검증한다. 새 코드 블록까지 자동 검증했다고 주장하지 않는다. 실행 가능한 새 예제는 필요한 경우 별도로 컴파일·실행하고, 서비스 의존 예제는 실제 확인 범위와 남은 검증을 적는다.
- 빌드 성공은 기술 설명의 정확성, 모든 앵커·외부 링크, 실제 운영 동작을 보장하지 않는다. 변경한 링크와 중요한 예제는 직접 확인한다.
- 필수 도구가 없으면 누락 항목과 재실행 명령을 알려준다. 검증을 통과시키려고 테스트를 건너뛰거나 조건을 완화하지 않는다.

## 생성 파일과 원격 반영

루트 `README.md`는 핵심 주제와 사용 안내를 직접 관리한다. 전체 파일 목록이나 변경 이력 표를 다시 넣지 않고 `docs/Sitemap.md`와 `docs/Recent_Changes.md`로 연결한다. 두 전용 문서는 생성 결과이므로 직접 날짜나 이력을 꾸며 넣지 않는다. 카테고리 `README.md`와 `.pages`의 탐색 항목은 문서와 함께 편집한다.

`scripts/update_recent_changes.py`는 Git 이력을 읽으므로 게시 시 **콘텐츠 커밋 이후**에 실행되어야 한다. `git-workflow`의 `scripts/publish.sh`가 이 순서를 처리한다. 검증만 하려고 publish를 실행하지 않는다.

publish는 `git add .`, 커밋, 자동 수정·생성, 테스트·빌드, amend, push를 수행한다. 원격 반영 범위가 맞는지 확인한 뒤 사용하고, 무관한 변경이 섞이면 전체를 스테이징하는 이 스크립트를 바로 실행하지 않는다. 실패하면 자동 재시도하지 말고 현재 커밋·작업 트리와 실패 단계를 먼저 확인한다.

결과에는 변경 문서, 탐색 연결, 실행한 검증과 실패·미실행 항목, 커밋·push 여부를 간단히 적는다.
