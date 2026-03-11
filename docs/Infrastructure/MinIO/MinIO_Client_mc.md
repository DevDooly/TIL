# MinIO Client (mc) 설치 및 사용 가이드

MinIO Client (`mc`)는 Amazon S3 호환 클라우드 스토리지 및 로컬 파일 시스템을 관리하기 위한 강력한 커맨드라인 도구입니다. `ls`, `cat`, `cp`, `rm` 등과 같은 전통적인 UNIX 명령어를 클라우드 스토리지 관리에 맞게 제공합니다.

---

## 1. 리눅스(Linux)에 `mc` 바이너리 설치

가장 간단한 설치 방법은 64비트 Linux용 독립 실행형(Standalone) 바이너리 파일을 다운로드하여 실행 권한을 부여하는 것입니다.

### 다운로드 및 권한 설정

```bash
# 1. 64-bit Linux용 mc 바이너리 다운로드
curl https://dl.min.io/client/mc/release/linux-amd64/mc \
  --create-dirs -o $HOME/minio-binaries/mc

# 2. 실행 권한 부여
chmod +x $HOME/minio-binaries/mc

# 3. 환경변수 PATH에 추가 (선택 사항이지만 권장)
export PATH=$PATH:$HOME/minio-binaries/
```

> **Tip**: `PATH` 설정을 영구적으로 적용하려면 `~/.bashrc` 또는 `~/.zshrc` 파일의 맨 아래에 `export PATH=$PATH:$HOME/minio-binaries/` 를 추가하고 `source ~/.bashrc` 를 실행하세요.

설치가 완료되었는지 버전을 확인해 봅니다.
```bash
mc --version
```

---

## 2. 서버 연결 설정 (Alias 등록)

`mc`를 사용하려면 먼저 관리하려는 MinIO(또는 S3) 서버의 연결 정보를 **alias(별칭)**로 등록해야 합니다.

### Alias 추가 명령어 (`mc alias set`)

```bash
# 기본 문법
# mc alias set <ALIAS_NAME> <SERVER_URL> <ACCESS_KEY> <SECRET_KEY>

# 예시: 로컬에 9000번 포트로 떠있는 MinIO 서버를 'myminio'라는 이름으로 등록
mc alias set myminio http://127.0.0.1:9000 ROOTUSER ROOTPASSWORD123
```

*등록된 전체 alias 목록을 확인하려면 `mc alias list` 를 입력합니다.*

---

## 3. 기본 사용법 (CRUD 명령어)

`mc` 명령어는 `mc <명령어> <원본> <대상>` 형태로 사용되며, 클라우드 경로는 항상 `alias명/버킷명/경로` 형태로 지정합니다.

### 3.1 버킷(Bucket) 생성 및 목록 조회
```bash
# 버킷 생성 (mb: Make Bucket)
mc mb myminio/test-bucket

# 버킷 및 파일 목록 조회 (ls: List)
mc ls myminio/
mc ls myminio/test-bucket/
```

### 3.2 파일 업로드 / 다운로드 / 복사 (cp: Copy)
```bash
# 1. 업로드: 로컬의 sample.txt를 MinIO 버킷으로 복사
mc cp sample.txt myminio/test-bucket/

# 2. 다운로드: MinIO 버킷의 파일을 로컬 현재 디렉토리로 복사
mc cp myminio/test-bucket/sample.txt .

# 3. 서버 간 복사: 하나의 버킷에서 다른 버킷으로 복사
mc cp myminio/test-bucket/sample.txt myminio/another-bucket/
```

### 3.3 파일 삭제 (rm: Remove)
```bash
# 단일 파일 삭제
mc rm myminio/test-bucket/sample.txt

# 버킷 내의 모든 파일 강제 삭제 (버저닝된 경우 삭제 마커 추가됨)
mc rm --recursive --force myminio/test-bucket/

# 버킷 자체를 삭제 (rb: Remove Bucket, 내부가 비어있어야 함)
mc rb myminio/test-bucket
```

---

## 4. 버저닝(Versioning) 환경에서의 고급 기능

버저닝이 켜진 버킷에서는 `mc`를 통해 버전 이력을 조회하거나 특정 버전을 제어할 수 있습니다.

### 4.1 모든 버전 이력 조회
`--versions` 옵션을 사용하면 파일의 모든 버전과 삭제 마커(Delete Marker) 내역을 시간순으로 볼 수 있습니다.
```bash
mc ls --versions myminio/test-bucket/sample.txt
```

### 4.2 특정 버전 되돌리기 (특정 버전으로 복사)
버저닝된 파일의 과거 버전을 현재 최신 버전으로 되돌리고 싶을 때, 해당 버전을 다시 덮어쓰기 복사하는 방식을 사용합니다.
```bash
# 특정 버전(예: v1)의 내용을 동일한 위치로 복사하여 최신 버전으로 만듦
mc cp --vid "특정_버전_ID_문자열" myminio/test-bucket/sample.txt myminio/test-bucket/sample.txt
```

### 4.3 특정 버전 영구 삭제
특정 `versionId`를 지정하여 지우면 해당 버전의 데이터가 물리적으로 영구 삭제됩니다.
```bash
mc rm --vid "특정_버전_ID_문자열" myminio/test-bucket/sample.txt
```