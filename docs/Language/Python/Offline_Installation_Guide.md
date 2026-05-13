# 폐쇄망 환경 Python 3.9 설치 가이드

인터넷 연결이 불가능한 폐쇄망 환경에서 Python 3.9를 소스 컴파일 방식으로 설치하고, 필요한 라이브러리를 오프라인으로 구축하는 방법을 정리합니다.

---

## 1. 사전 준비 (외부망 환경)

폐쇄망으로 반입하기 위해 외부망에서 다음 파일들을 다운로드합니다.

### 🔹 Python 소스 코드 다운로드
[Python 공식 홈페이지](https://www.python.org/ftp/python/3.9.18/Python-3.9.18.tar.xz)에서 소스 타르볼을 받습니다.
```bash
wget https://www.python.org/ftp/python/3.9.18/Python-3.9.18.tar.xz
```

### 🔹 빌드 의존성 패키지 확인
컴파일 시 `gcc`, `make`, `zlib-devel`, `openssl-devel`, `libffi-devel` 등이 필요합니다. 운영체제 설치 ISO(Yum/Apt 로컬 저장소)에 해당 패키지들이 있는지 확인하고, 없다면 RPM/DEB 파일을 개별적으로 미리 준비해야 합니다.

---

## 2. 설치 과정 (폐쇄망 환경)

### ① 파일 반입 및 압축 해제
준비한 소스 파일을 서버의 적절한 경로(예: `/opt`)로 전송한 후 압축을 해제합니다.
```bash
tar -xf Python-3.9.18.tar.xz
cd Python-3.9.18
```

### ② 환경 설정 (Configure)
설치 경로를 지정하고 최적화 옵션을 추가합니다.
```bash
./configure --enable-optimizations --prefix=/usr/local/python3.9
```

* `--enable-optimizations`: Python 실행 속도를 약 10-20% 향상시키지만 빌드 시간이 길어집니다.
* `--prefix`: 설치될 경로를 지정합니다.

### ③ 빌드 및 설치
기존 시스템 파이썬을 덮어쓰지 않도록 `altinstall` 명령어를 사용하는 것을 권장합니다.
```bash
make -j $(nproc)
sudo make altinstall
```

* `make -j $(nproc)`: CPU 코어 수를 모두 사용하여 빌드 속도를 높입니다.
* `altinstall`: `python3` 명령어가 아닌 `python3.9`라는 별도의 명령어로 설치되어 시스템 안정성을 보장합니다.

---

## 3. 환경 변수 설정

설치가 완료되면 어디서든 사용할 수 있도록 환경 변수를 추가합니다.

```bash
# ~/.bashrc 또는 /etc/profile에 추가
export PATH=/usr/local/python3.9/bin:$PATH

# 적용
source ~/.bashrc
```

---

## 4. 오프라인 패키지(라이브러리) 설치 방법

외부망에서 필요한 라이브러리와 그 의존성들을 한꺼번에 다운로드하여 옮겨야 합니다.

### ① 외부망에서 다운로드
```bash
# 예: pandas 설치를 위한 패키지 다운로드
mkdir python_packages
pip download -d ./python_packages pandas
```

### ② 폐쇄망에서 설치
다운로드한 폴더를 통째로 옮긴 후 다음 명령어를 실행합니다.
```bash
# --no-index: PyPI 서버를 찾지 않음
# --find-links: 지정한 경로에서 패키지를 찾음
pip install --no-index --find-links=./python_packages pandas
```

---

## 5. 트러블슈팅

* **OpenSSL 관련 에러**: `pip` 사용 시 SSL 에러가 발생한다면, 빌드 시 `openssl-devel`이 설치되어 있지 않았기 때문입니다. 해당 패키지를 설치한 후 다시 컴파일해야 합니다.
* **Libffi 에러**: `ctypes` 모듈을 로드하지 못한다면 `libffi-devel` 패키지가 필요합니다.

---

## 6. 결론

폐쇄망 환경의 Python 설치는 **사전 의존성 패키지 확보**가 성공의 90%를 결정합니다. 소스 빌드 방식이 번거롭다면, 동일한 OS 환경의 외부망에서 `Conda`를 설치하고 환경 전체를 압축하여 옮기는 방식(Conda Pack)도 좋은 대안이 될 수 있습니다.
