# 폐쇄망 환경 Python 3.12 설치 가이드 (최신 안정 버전)

인터넷 연결이 불가능한 폐쇄망 환경에서 **Python 3.12**(현재 가장 권장되는 안정 버전)를 소스 컴파일 방식으로 설치하고, 필요한 라이브러리를 오프라인으로 구축하는 방법을 정리합니다.

---

## 1. 버전 선정 이유

* **지원 기간**: Python 3.12는 2028년 하반기까지 지원되는 장기 안정 버전입니다.
* **성능**: 3.11부터 적용된 성능 최적화가 완성 단계에 접어들어 매우 안정적입니다.
* **생태계**: 거의 모든 주요 라이브러리(Pandas, TensorFlow, PyTorch 등)가 3.12에서 완벽하게 검증되었습니다.

### ⚠️ Python 3.13, 3.14를 추천하지 않는 이유

1. **실험적 기능 (3.13 free-threading)**: 3.13의 핵심인 GIL 제거(free-threading)는 아직 실험적 단계입니다. 폐쇄망 환경에서 예상치 못한 멀티스레딩 버그가 발생할 경우 외부 도움 없이 해결하기 어렵습니다.
2. **라이브러리 호환성 (Binary Wheels)**: 3.14 등 최신 버전은 많은 서드파티 라이브러리들이 아직 전용 바이너리(Wheel)를 제공하지 않을 수 있습니다. 폐쇄망에서는 소스 코드를 직접 빌드해야 하는 경우가 빈번해지는데, 이는 설치 난이도를 비약적으로 높입니다.
3. **C-API 변경**: 최근 버전들은 내부 C-API가 크게 변경되어, 기존에 잘 동작하던 C 기반 라이브러리(numpy, 사이킷런 등)와 충돌이 발생할 가능성이 높습니다.
4. **검증된 레퍼런스 부족**: 기업 환경이나 폐쇄망 서버에서는 "최신"보다 "검증된" 버전이 우선입니다. 3.12는 이미 수많은 운영 환경에서 검증을 마친 상태입니다.


---

## 2. 사전 준비 (외부망 환경)

### 🔹 Python 3.12 소스 코드 다운로드
[Python 공식 홈페이지](https://www.python.org/ftp/python/3.12.3/Python-3.12.3.tar.xz)에서 소스 타르볼을 받습니다.
```bash
wget https://www.python.org/ftp/python/3.12.3/Python-3.12.3.tar.xz
```

### 🔹 필수 빌드 의존성 (OS ISO 등에서 준비)
Python 3.12 및 OpenSSL 3.0 빌드를 위해 다음 패키지들이 서버에 미리 설치되어 있어야 합니다.

* **필수**: `gcc`, `make`, `perl-core` (OpenSSL 3.0 빌드 시 필수), `libffi-devel`, `zlib-devel`, `bzip2-devel`, `readline-devel`, `sqlite-devel`
* **보안/네트워크**: `openssl-devel` (시스템 기본용)
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

## 6. 주의사항 및 팁 (특히 CentOS 7 환경)

### ⚠️ CentOS 7의 OpenSSL 버전 문제
CentOS 7의 기본 OpenSSL 버전은 `1.0.2k`입니다. 하지만 **Python 3.10 이상은 OpenSSL 1.1.1 이상**을 요구하므로, 그대로 빌드하면 `_ssl` 모듈 임포트에 실패하거나 `make` 중 에러가 발생합니다.

#### ① 현재 OpenSSL 버전 확인
```bash
openssl version
# OpenSSL 1.0.2k-fips  26 Jan 2017 -> (업데이트 필요)
```

#### ② 해결 방법: OpenSSL 1.1.1w 별도 빌드 (또는 기존 설치 경로 활용)
보안상 3.0 이상이 권장되나, 특정 환경에 따라 1.1.1w 버전을 사용해야 할 경우 다음 경로를 기준으로 작업합니다. (예: `/opt/openssl-1.1.1`에 이미 설치된 경우)

```bash
# (새로 설치가 필요한 경우만 실행) OpenSSL 1.1.1w 빌드 및 설치
tar -xf openssl-1.1.1w.tar.gz
cd openssl-1.1.1w
./config --prefix=/opt/openssl-1.1.1 --openssldir=/opt/openssl-1.1.1 shared zlib
make -j $(nproc)
sudo make install
```

#### ③ Python 빌드 시 새 OpenSSL 연결
Python `configure` 실행 시 설치된 OpenSSL 1.1.1w 경로(`/opt/openssl-1.1.1`)를 명시합니다.

```bash
cd ../Python-3.12.3
./configure --enable-optimizations \
            --with-openssl=/opt/openssl-1.1.1 \
            --with-openssl-rpath=auto \
            --prefix=/usr/local/python3.12

make -j $(nproc)
sudo make altinstall
```

* `--with-openssl`: `/opt/openssl-1.1.1` 경로를 지정하여 1.1.1w 버전을 사용하도록 설정.
* `--with-openssl-rpath=auto`: 실행 시 라이브러리 경로를 수동으로 지정하지 않아도 자동으로 찾도록 설정.


### 💡 기타 팁

* **OpenSSL 빌드 시 Makefile 없음**: `./config` 실행 후 `Makefile`이 생기지 않는다면 대부분 **Perl(특히 perl-core)** 패키지가 설치되지 않아 설정이 중간에 실패한 것입니다. `./config`의 마지막 출력 메시지를 확인하여 에러 여부를 체크하세요.
* **SQLite/SSL 임포트 에러**: 설치 후 `import ssl` 또는 `import sqlite3` 실행 시 에러가 난다면, 빌드 시점에 해당 개발 라이브러리(`devel`)가 없었기 때문입니다. 라이브러리 설치 후 `make` 과정부터 다시 진행해야 합니다.
* **Conda Pack 활용**: 빌드 과정이 너무 복잡하다면, 동일 OS 환경의 외부망에서 Conda 환경을 만든 뒤 `conda-pack`으로 압축하여 옮기는 것이 가장 간편합니다.

---

## 7. 결론

폐쇄망 환경의 Python 설치는 **사전 의존성 패키지 확보**가 성공의 90%를 결정합니다. 특히 CentOS 7과 같이 오래된 OS를 사용하는 경우 OpenSSL 버전을 반드시 미리 체크해야 합니다.
