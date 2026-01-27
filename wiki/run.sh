#!/bin/bash

# 스크립트가 있는 디렉토리(wiki)로 이동 (어디서 실행하든 안전하게)
cd "$(dirname "$0")"

CONTAINER_NAME="my-til-wiki"
PORT=8000

# 1. 기존 컨테이너 정리
if [ "$(docker ps -aq -f name=${CONTAINER_NAME})" ]; then
    echo "🔄 기존 위키 컨테이너를 재시작합니다..."
    docker rm -f ${CONTAINER_NAME}
fi

# 2. Docker 실행
# -v $(pwd)/..:/til-project : 상위 폴더(루트) 전체를 컨테이너의 /til-project에 연결
# -w /til-project : 작업 디렉토리 설정
# -f wiki/mkdocs.yml : 설정 파일 경로 지정
echo "🚀 TIL Wiki를 시작합니다..."

docker run -d \
  --name ${CONTAINER_NAME} \
  -p ${PORT}:8000 \
  -v "$(pwd)/..":/til-project \
  -w /til-project \
  squidfunk/mkdocs-material \
  serve -f wiki/mkdocs.yml -a 0.0.0.0:8000

echo ""
echo "✅ 실행 완료! 브라우저에서 접속하세요:"
echo "👉 http://localhost:${PORT}"

