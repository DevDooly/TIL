#!/bin/bash

# 프로젝트 루트로 이동 (스크립트 위치 기준 상위 폴더)
cd "$(dirname "$0")/.."

CONTAINER_NAME="my-til-wiki"
PORT=8000

# 1. 기존 컨테이너 정리
docker rm -f ${CONTAINER_NAME} >/dev/null 2>&1

echo "🚀 Standard MkDocs 서버를 시작합니다..."

# 2. Docker 실행
# -v $(pwd):/docs  -> 현재 루트 폴더를 컨테이너의 /docs에 마운트
# (MkDocs 이미지는 기본적으로 /docs 폴더에서 mkdocs.yml을 찾습니다)
docker run -d \
  --name ${CONTAINER_NAME} \
  -p ${PORT}:8000 \
  -v "$(pwd):/docs" \
  squidfunk/mkdocs-material

echo ""
echo "✅ 실행 완료! 접속 주소:"
echo "👉 http://devdooly.iptime.org:${PORT}"

