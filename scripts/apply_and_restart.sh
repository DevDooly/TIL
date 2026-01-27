#!/bin/bash

# 에러 발생 시 중단하지 않고 진행
set +e

echo "🔄 위키 설정을 재정비하고 재기동합니다..."

# ==========================================
# 1. 설정 파일(mkdocs.yml) 표준화
# ==========================================
echo "⚙️  mkdocs.yml 설정을 업데이트합니다..."

# 만약 wiki 폴더에 설정 파일이 있다면 루트로 가져옴
if [ -f "wiki/mkdocs.yml" ]; then
    mv wiki/mkdocs.yml ./mkdocs.yml
fi

# mkdocs.yml 파일이 없으면 생성, 있으면 내용 덮어쓰기 (확실한 복구)
cat > mkdocs.yml <<EOF
site_name: My TIL Wiki
site_url: http://devdooly.iptime.org:8000
repo_url: https://github.com/devdooly/til
edit_uri: edit/main/docs/

# 📌 404 에러 방지 핵심 설정 (URL을 .html로 고정)
use_directory_urls: false

theme:
  name: material
  language: ko
  palette: 
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/weather-sunny
        name: 다크 모드 전환
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/weather-night
        name: 라이트 모드 전환
  features:
    - navigation.expand
    - navigation.indexes
    - navigation.top
    - navigation.tracking
    - search.suggest
    - search.highlight
    - content.code.copy
    - toc.follow

markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.tabbed:
      alternate_style: true
  - toc:
      permalink: true

plugins:
  - search

# 📌 네비게이션 설정 (docs 폴더 내부 기준)
nav:
  - Home: index.md
  - Language: Language/
  - Web: Web/
  - Infrastructure: Infrastructure/
  - Data: Data/
  - Computer Science: ComputerScience/
  - Tools: Tools/
  - Life: Life/
  - Archive: Archive/
EOF

# ==========================================
# 2. 메인 페이지(docs/index.md) 복구
# ==========================================
echo "📄 docs/index.md 파일을 점검합니다..."
mkdir -p docs

# 기존 index.md 삭제 후 README.md 내용으로 새로 생성
rm -f docs/index.md
if [ -f "README.md" ]; then
    cp README.md docs/index.md
else
    echo "# 환영합니다" > docs/index.md
fi

# ==========================================
# 3. Docker 컨테이너 재기동
# ==========================================
CONTAINER_NAME="my-til-wiki"
PORT=8000

echo "🛑 기존 컨테이너를 정리합니다..."
docker rm -f ${CONTAINER_NAME} >/dev/null 2>&1

echo "🚀 위키 서버를 시작합니다..."
# 현재 폴더(Root)를 컨테이너의 /docs로 마운트
# MkDocs 표준 이미지는 /docs/mkdocs.yml을 설정 파일로 인식함
docker run -d \
  --name ${CONTAINER_NAME} \
  -p ${PORT}:8000 \
  -v "$(pwd):/docs" \
  squidfunk/mkdocs-material

echo ""
echo "✅ 재기동 완료!"
echo "👉 브라우저 주소창에 아래 URL을 입력하세요."
echo "   http://devdooly.iptime.org:${PORT}"
echo ""
echo "⚠️  [중요] 브라우저 캐시 때문에 404가 계속 뜰 수 있습니다."
echo "    반드시 '강력 새로고침 (Ctrl+Shift+R)'을 해주세요!"

