# Docker: No space left on device 해결 방법

Docker를 오래 사용하다 보면 "No space left on device" 에러와 함께 디스크 용량 부족 현상이 발생할 수 있습니다. 이는 사용하지 않는 이미지, 컨테이너, 볼륨 등이 쌓여있기 때문입니다.

## 1. Docker System Prune (권장)
가장 간단하고 강력한 청소 명령어입니다. 중지된 컨테이너, 사용되지 않는 네트워크, 댕글링(Dangling) 이미지를 모두 삭제합니다.
```bash
docker system prune -a
```
*   `-a`: 사용되지 않는 모든 이미지를 삭제합니다 (현재 실행 중인 컨테이너가 쓰지 않는 것들).
*   `--volumes`: 볼륨까지 삭제하려면 추가합니다.

## 2. 수동 정리

### Dangling Volume 정리
어떤 컨테이너에도 연결되지 않은 볼륨을 삭제합니다.
```bash
docker volume rm $(docker volume ls -qf dangling=true)
```

### Dangling Image 정리
태그가 `<none>`인 이미지들을 삭제합니다.
```bash
docker rmi $(docker images -f "dangling=true" -q)
```

### Exited Container 정리
중지된(Exited) 모든 컨테이너를 삭제합니다.
```bash
docker rm $(docker ps -a -q -f status=exited)
```

## 3. 용량 확인
현재 Docker가 사용하고 있는 디스크 용량을 확인합니다.
```bash
docker system df
```