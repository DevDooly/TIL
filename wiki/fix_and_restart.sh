#!/bin/bash

# 스크립트 위치(wiki 폴더)로 이동
cd "$(dirname "$0")"

echo "🔧 404 문제 해결을 시작합니다..."

# 1. README.md를 docs/index.md로 복사 (홈페이지 생성)
if [ -f "../README.md" ]; then
    echo "📄 루트의 README.md를 docs/index.md로 복사합니다..."
    cp "../README.md" "../docs/index.md"
else
    echo "⚠️ README.md를 찾을 수 없습니다. 빈 index.md를 생성합니다."
    echo "# 환영합니다" > "../docs/index.md"
fi

# 2. 컨테이너 재시작
CONTAINER_NAME="my-til-wiki"
PORT=8000

if [ "$(docker ps -aq -f name=${CONTAINER_NAME})" ]; then
    echo "🛑 기존 위키를 종료합니다..."
    docker rm -f ${CONTAINER_NAME}
fi

echo "🚀 TIL Wiki를 재시작합니다..."
# Docker 실행 (루트 전체 마운트)
docker run -d \
  --name ${CONTAINER_NAME} \
  -p ${PORT}:8000 \
  -v "$(pwd)/..":/til-project \
  -w /til-project \
  squidfunk/mkdocs-material \
  serve -f wiki/mkdocs.yml -a 0.0.0.0:8000

echo ""
echo "✅ 완료되었습니다! 잠시 후 접속해보세요."
echo "👉 http://devdooly.iptime.org:${PORT}"

