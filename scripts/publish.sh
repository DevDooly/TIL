#!/bin/bash
# scripts/publish.sh
# 
# 이 스크립트는 TIL 문서의 정합성을 맞추고 모든 인덱스를 업데이트한 뒤 서버에 푸시합니다.
# 순서: 컨텐츠 커밋 -> 스크립트 실행 -> 인덱스 파일들 Amend -> 푸시

set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
trap 'echo "❌ 검증 또는 Git 작업 실패: 원격 푸시를 중단합니다." >&2' ERR

MESSAGE=${1:-}
PYTHON_BIN=${PYTHON:-python3}

if [ -z "$MESSAGE" ]; then
    echo "❌ 에러: 커밋 메시지를 입력해주세요."
    echo "사용법: ./scripts/publish.sh \"커밋 메시지\""
    exit 1
fi

# 1. 현재 변경된 모든 문서 스테이징 및 커밋 (Scripts가 git log를 읽을 수 있게 하기 위함)
echo "📦 1. 컨텐츠 임시 커밋 중..."
git add .
if git diff --cached --quiet; then
    echo "변경 사항이 없습니다."
    exit 0
fi
git commit -m "$MESSAGE"

# 2. 관리 및 검증 스크립트 실행
echo "⚙️ 2. 관리 스크립트 실행 중..."
"$PYTHON_BIN" scripts/auto_fix_markdown_lists.py
"$PYTHON_BIN" scripts/validate_markdown_lists.py
"$PYTHON_BIN" scripts/validate_pages.py
"$PYTHON_BIN" scripts/fix_pages_syntax.py
"$PYTHON_BIN" scripts/update_recent_changes.py
"$PYTHON_BIN" scripts/generate_sitemap.py
"$PYTHON_BIN" scripts/validate_pages.py
"$PYTHON_BIN" -m unittest discover -s scripts/tests -p 'test_*.py'
"$PYTHON_BIN" -m mkdocs build --strict

# 3. 스크립트에 의해 자동 갱신된 파일들 스테이징 (마크다운 포맷팅 수정 포함)
echo "📝 3. 자동 생성 및 수정된 파일 동기화 중..."
git add .

# 4. 이전 커밋에 합치기 (Amend)
echo "🔨 4. 커밋 수정(Amend) 중..."
git commit --amend --no-edit

# 5. 원격 저장소 푸시
echo "🚀 5. 원격 저장소 푸시 중..."
git push

echo "✅ 모든 작업이 성공적으로 완료되었습니다!"
