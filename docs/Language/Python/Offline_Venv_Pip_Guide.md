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

#### **Best Practice: 버전 명시 (Pinning)**
단순히 패키지 이름만 적기보다, `pip freeze`를 통해 검증된 버전을 명시하는 것이 중요합니다.
```bash
# 1. (외부망 개발환경) 테스트 완료 후 버전 박제
pip freeze > requirements.txt

# 2. 박제된 목록으로 다운로드
pip download -d ./my_project_pkgs -r requirements.txt
```

| 표기법 | 의미 | 특징 |
| :--- | :--- | :--- |
| `fastapi==0.110.0` | 정확한 버전 | **폐쇄망 배포 시 강력 권장** |
| `fastapi~=0.110.0` | 0.110.x 범위 내 최신 | 호환성을 유지하며 패치 수용 |
| `fastapi>=0.100.0` | 최소 버전 지정 | 버전 미지정보다는 낫지만 위험함 |

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

### 🔹 "No matching distribution found" 에러 (예: pandas==3.0.3)
지정한 버전을 찾지 못해 다운로드에 실패하는 경우 다음 절차를 따르세요.

1. **실제 존재 여부 확인**: `pip index versions [패키지명]` 명령어로 PyPI에 해당 버전이 존재하는지 확인합니다. (오타 확인 필수)
2. **Pip 업그레이드**: 오래된 pip는 최신 패키지를 찾지 못할 수 있습니다.
    ```bash
    python3 -m pip install --upgrade pip
    ```

3. **Python 버전 호환성 체크**: 최신 패키지는 구형 Python(예: 3.7 이하)을 지원하지 않을 수 있습니다. 대상 서버의 Python 버전과 호환되는지 확인하세요.
4. **플랫폼 불일치 (Cross-Download)**: 현재 PC와 대상 서버의 OS가 다른 경우, `--platform` 옵션을 명시하지 않으면 해당 환경에 맞는 패키지를 찾지 못해 에러가 발생합니다.
    ```bash
    # 예: Linux용 pandas 3.0.3을 Windows에서 다운로드할 때
    pip download --only-binary=:all: --platform manylinux1_x86_64 --python-version 3.12 -d ./pkgs pandas==3.0.3
    ```


---

## 5. 결론

폐쇄망 환경에서 프로젝트를 관리할 때는 **가상환경별로 패키지 묶음을 관리**하는 것이 가장 안전합니다. `pip download`와 `--no-index` 옵션만 정확히 이해하면 외부망과 동일한 개발 환경을 폐쇄망에서도 유지할 수 있습니다.
