# 오프라인 환경에서 `venv` 및 `pip` 패키지 설치 가이드

폐쇄망 환경의 특정 프로젝트에서 `venv` 가상환경을 구축하고, 외부에서 반입한 패키지를 오프라인으로 설치하는 표준 절차를 정리합니다.

---

## 1. 개요 (Workflow)

1. **외부망(Online)**: 필요한 패키지와 모든 의존성 파일을 `.whl` 형태로 다운로드.
2. **데이터 반입**: 다운로드한 폴더를 폐쇄망 서버로 전송.
3. **폐쇄망(Offline)**: 가상환경 생성 후 로컬 경로를 참조하여 패키지 설치.

---

## 2. 1단계: 외부망에서 패키지 준비

인터넷이 연결된 PC에서 프로젝트에 필요한 패키지들을 다운로드합니다. 
*주의: 설치 대상 서버와 OS(Linux/Windows) 및 Python 버전이 동일해야 합니다.*

### 💻 패키지 다운로드 명령어
```bash
# 1. 프로젝트 디렉토리 이동 및 패키지 목록 작성
mkdir my_project_pkgs
echo "fastapi" >> requirements.txt
echo "uvicorn" >> requirements.txt

# 2. 패키지 및 의존성 전체 다운로드 (-d 옵션으로 경로 지정)
pip download -d ./my_project_pkgs -r requirements.txt

# (선택 사항) pip 자체 업데이트가 필요할 경우를 대비하여 필수 도구도 지참
pip download -d ./my_project_pkgs pip setuptools wheel
```

---

## 3. 2단계: 폐쇄망에서 가상환경 구축 및 설치

전송받은 `my_project_pkgs` 폴더와 `requirements.txt` 파일을 프로젝트 경로에 배치합니다.

### ① 가상환경 생성 및 활성화
```bash
cd /path/to/project

# 가상환경 생성
python3 -m venv .venv

# 가상환경 활성화
source .venv/bin/activate
```

### ② (선택) pip/setuptools 업데이트
가상환경 내의 pip 버전이 너무 낮은 경우 설치 에러가 날 수 있습니다. 반입한 파일을 이용해 먼저 업데이트합니다.
```bash
pip install --no-index --find-links=./my_project_pkgs --upgrade pip setuptools wheel
```

### ③ 프로젝트 패키지 오프라인 설치
`--no-index`는 외부망 접속을 차단하고, `--find-links`는 로컬 파일 경로를 보게 합니다.
```bash
pip install --no-index --find-links=./my_project_pkgs -r requirements.txt
```

---

## 4. 트러블슈팅 및 팁

### 🔹 플랫폼이 다른 경우 (Cross-Platform)
인터넷 PC는 Windows인데 폐쇄망은 Linux인 경우, 다운로드 시 플랫폼을 명시해야 합니다.
```bash
pip download \
    --only-binary=:all: \
    --platform manylinux1_x86_64 \
    --python-version 3.12 \
    --implementation cp \
    --abi cp312 \
    -d ./my_project_pkgs -r requirements.txt
```

### 🔹 "No matching distribution found" 에러
이 에러는 주로 다음과 같은 상황에서 발생합니다.

* 의존성 중 하나가 누락되어 반입된 경우.
* Python 버전이 맞지 않아 해당 버전에 맞는 `.whl` 파일이 없는 경우.
* OS 아키텍처(x86_64 등)가 맞지 않는 경우.

---

## 5. 결론

폐쇄망 환경에서 프로젝트를 관리할 때는 **가상환경별로 패키지 묶음을 관리**하는 것이 가장 안전합니다. `pip download`와 `--no-index` 옵션만 정확히 이해하면 외부망과 동일한 개발 환경을 폐쇄망에서도 유지할 수 있습니다.
