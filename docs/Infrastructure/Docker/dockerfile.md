# Dockerfile

**Dockerfile**은 Docker 이미지를 생성(Build)하기 위한 설정 파일입니다. 사용자가 이미지를 조립하기 위해 명령줄에서 호출할 수 있는 모든 명령어를 텍스트 문서 형태로 포함하고 있습니다.

## 1. 빌드 (Build)

```bash
docker build -t <이미지이름>:<태그> .
```
*   `docker build` 명령어는 Docker 클라이언트가 아닌 **Docker 데몬(Docker Daemon)**에 의해 실행됩니다.
*   빌드 프로세스의 첫 단계는 **빌드 컨텍스트(Build Context, 현재 디렉토리 `.`의 모든 파일)**를 데몬에게 전송하는 것입니다.

```text
[internal] load build definition from Dockerfile                       0.1s
 => transferring dockerfile: 60B                                        0.0s
 [internal] load .dockerignore                                          0.1s
 => transferring context: 2B                                            0.0s
```

## 2. 기본 문법 (Syntax)

```dockerfile
# 주석 (Comment)
INSTRUCTION arguments
```
*   명령어(`INSTRUCTION`)는 대소문자를 구분하지 않으나, 가독성을 위해 **대문자** 사용을 권장합니다.
*   모든 Dockerfile은 **`FROM`** 명령어로 시작해야 합니다.

## 3. 주요 명령어

### FROM
새로운 빌드 단계를 초기화하고, 후속 명령어를 위한 **베이스 이미지(Base Image)**를 설정합니다.
```dockerfile
FROM ubuntu:20.04
FROM python:3.9-slim AS builder
```

### RUN
현재 이미지 위에서 명령어를 실행하고, 그 결과를 새로운 레이어(Layer)로 커밋합니다. 패키지 설치 등에 사용됩니다.
```dockerfile
RUN apt-get update && apt-get install -y git
```

### CMD vs ENTRYPOINT
컨테이너가 시작될 때 실행될 명령을 정의합니다.
*   **CMD:** 컨테이너 실행 시 인자(`docker run myapp <arg>`)를 주면 덮어씌워집니다 (기본값 역할).
*   **ENTRYPOINT:** 인자를 주어도 덮어씌워지지 않고, 인자가 뒤에 추가됩니다 (실행 파일 역할).

```dockerfile
CMD ["python", "app.py"]
```

### COPY vs ADD
호스트의 파일을 이미지 안으로 복사합니다.
*   **COPY:** 단순히 로컬 파일을 복사합니다. (권장)
*   **ADD:** URL에서 다운로드하거나 압축 파일(tar)을 자동으로 해제하는 기능이 있습니다.

### WORKDIR
작업 디렉토리를 설정합니다. (`cd`와 유사)
```dockerfile
WORKDIR /app
```

### EXPOSE
컨테이너가 런타임에 리스닝할 포트를 명시합니다. (실제 포트 개방은 `docker run -p` 옵션 필요)
```dockerfile
EXPOSE 8080
```

## 4. 예제 (Example)

다음은 Python Flask 애플리케이션을 위한 실용적인 `Dockerfile` 예제입니다.

```dockerfile
# 1. 베이스 이미지 설정 (경량화된 alpine 버전 사용)
FROM python:3.9-slim

# 2. 메타데이터 설정
LABEL maintainer="devdooly"
LABEL description="My TIL Python App"

# 3. 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 4. 작업 디렉토리 생성 및 설정
WORKDIR /app

# 5. 의존성 파일 복사 및 설치
# 레이어 캐싱을 위해 소스 코드보다 먼저 복사합니다.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. 소스 코드 복사
COPY . .

# 7. 실행 포트 명시
EXPOSE 5000

# 8. 컨테이너 실행 명령어
CMD ["python", "app.py"]
```