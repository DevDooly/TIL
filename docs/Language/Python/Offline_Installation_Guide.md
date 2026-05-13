# 폐쇄망 환경 Python 3.12 설치 가이드 (최신 안정 버전)

인터넷 연결이 불가능한 폐쇄망 환경에서 **Python 3.12**(현재 가장 권장되는 안정 버전)를 소스 컴파일 방식으로 설치하고, 필요한 라이브러리를 오프라인으로 구축하는 방법을 정리합니다.

---

## 1. 버전 선정 이유

* **지원 기간**: Python 3.12는 2028년 하반기까지 지원됩니다. (3.9는 2025년 종료 예정)
* **성능**: 3.11 버전부터 적용된 성능 최적화로 인해 이전 버전 대비 실행 속도가 크게 개선되었습니다.
* **표준**: 최신 AI/데이터 과학 라이브러리들이 3.11~3.12 버전을 기본 타겟으로 하고 있습니다.

---

## 2. 사전 준비 (외부망 환경)

### 🔹 Python 3.12 소스 코드 다운로드
[Python 공식 홈페이지](https://www.python.org/ftp/python/3.12.3/Python-3.12.3.tar.xz)에서 소스 타르볼을 받습니다.
```bash
wget https://www.python.org/ftp/python/3.12.3/Python-3.12.3.tar.xz
```

### 🔹 필수 빌드 의존성 (OS ISO 등에서 준비)
Python 3.12 빌드를 위해 다음 패키지들이 서버에 미리 설치되어 있어야 합니다.

* **필수**: `gcc`, `make`, `libffi-devel`, `zlib-devel`, `bzip2-devel`, `readline-devel`, `sqlite-devel`
* **보안/네트워크**: `openssl-devel` (최소 1.1.1 이상 필요)
* **기타**: `tk-devel`, `gdbm-devel`, `db4-devel`, `libpcap-devel`, `xz-devel`

---

## 3. 설치 과정 (폐쇄망 환경)

### ① 파일 반입 및 압축 해제
```bash
tar -xf Python-3.12.3.tar.xz
cd Python-3.12.3
```

### ② 환경 설정 (Configure)
시스템 전역을 오염시키지 않도록 별도 경로에 설치하는 것을 권장합니다.
```bash
./configure --enable-optimizations --with-ensurepip=install --prefix=/usr/local/python3.12
```

### ③ 빌드 및 설치
```bash
# CPU 코어 전체를 활용하여 빌드 (작업 속도 향상)
make -j $(nproc)
sudo make altinstall
```

* `altinstall`: `python3` 명령어를 덮어쓰지 않고 `python3.12`로 설치하여 시스템 기본 파이썬과의 충돌을 방지합니다.

---

## 4. 환경 변수 및 Alias 설정

사용자 편의를 위해 `python3` 명령어가 3.12를 가리키도록 설정할 수 있습니다.

```bash
# ~/.bashrc에 추가
export PATH=/usr/local/python3.12/bin:$PATH
alias python3='/usr/local/python3.12/bin/python3.12'
alias pip3='/usr/local/python3.12/bin/pip3.12'

# 적용
source ~/.bashrc
```

---

## 5. 오프라인 패키지 관리 (pip)

### ① 외부망에서 라이브러리 다운로드
```bash
# 특정 패키지와 그 의존성을 모두 다운로드
mkdir pkgs
pip3 download -d ./pkgs pandas fastapi uvicorn
```

### ② 폐쇄망에서 설치
```bash
pip3 install --no-index --find-links=./pkgs pandas fastapi uvicorn
```

---

## 6. 주의사항 및 팁

* **OpenSSL 버전 확인**: Python 3.10 이상은 OpenSSL 1.1.1 이상이 필수입니다. 만약 OS(CentOS 7 등)의 OpenSSL 버전이 낮다면 OpenSSL도 별도로 컴파일하여 설치해야 합니다.
* **SQLite/SSL 임포트 에러**: 설치 후 `import ssl` 또는 `import sqlite3` 실행 시 에러가 난다면, 빌드 시점에 해당 개발 라이브러리(`devel`)가 없었기 때문입니다. 라이브러리 설치 후 `make` 과정부터 다시 진행해야 합니다.
* **Conda Pack 활용**: 빌드 과정이 너무 복잡하다면, 동일 OS 환경의 외부망에서 Conda 환경을 만든 뒤 `conda-pack`으로 압축하여 옮기는 것이 가장 간편합니다.
