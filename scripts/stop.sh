#!/bin/bash
CONTAINER_NAME="my-til-wiki"

if [ "$(docker ps -aq -f name=${CONTAINER_NAME})" ]; then
    echo "🛑 TIL Wiki($CONTAINER_NAME)를 종료합니다..."
    docker rm -f ${CONTAINER_NAME}
    echo "✅ 종료되었습니다."
else
    echo "⚠️ 실행 중인 위키가 없습니다."
fi

