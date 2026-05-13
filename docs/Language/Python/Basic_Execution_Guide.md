# Python 스크립트 실행 가이드: `python3 main.py`

Python 인터프리터를 사용하여 스크립트 파일(.py)을 실행하는 기본 방법과 실무에서 자주 쓰이는 실행 옵션들을 정리합니다.

---

## 1. 기본 실행 방법

가장 기본적인 형태는 `python3` 명령어 뒤에 실행하고자 하는 파일명을 입력하는 것입니다.

```bash
python3 main.py
```

* **참고**: Windows 환경이나 특정 설정에서는 `python` 또는 `py` 명령어를 사용하기도 하지만, 리눅스/macOS 표준은 `python3`입니다.

---

## 2. 명령행 인자 전달 (Arguments)

스크립트 실행 시 외부에서 데이터를 전달해야 할 때 사용합니다.

### 💻 코드 예시 (`main.py`)
```python
import sys

# sys.argv[0]은 스크립트 이름, sys.argv[1]부터 실제 인자입니다.
if len(sys.argv) > 1:
    name = sys.argv[1]
    print(f"Hello, {name}!")
else:
    print("Hello, World!")
```

### 🚀 실행 방법
```bash
python3 main.py "Dooly"
# 출력: Hello, Dooly!
```

---

## 3. 환경 변수와 함께 실행

API 키나 데이터베이스 접속 정보 등 민감한 정보를 환경 변수로 전달하며 실행할 때 유용합니다.

```bash
# 1회성 환경 변수 설정과 함께 실행
DB_URL="localhost:5432" python3 main.py
```

스크립트 내부에서는 `os.environ`을 통해 접근합니다.
```python
import os
db_url = os.environ.get("DB_URL")
```

---

## 4. 가상환경(Virtual Environment)에서의 실행

패키지 충돌을 방지하기 위해 가상환경을 활성화한 후 실행하는 것이 관례입니다.

### 🍃 venv (표준)
```bash
# 가상환경 활성화
source venv/bin/activate
# 실행
python3 main.py
```

### 📦 Conda
```bash
# 가상환경 활성화
conda activate myenv
# 실행
python3 main.py
```

---

## 5. 백그라운드 및 로그 기록 실행

서버에서 터미널을 종료해도 스크립트가 계속 실행되도록 하거나 로그를 파일로 남길 때 사용합니다.

```bash
# 1. 백그라운드 실행 (&)
python3 main.py &

# 2. 터미널 종료 후에도 유지 (nohup) + 로그 기록
nohup python3 main.py > output.log 2>&1 &
```

* `> output.log`: 표준 출력을 파일로 저장.
* `2>&1`: 에러 메시지(stderr)도 표준 출력(stdout)과 같은 곳으로 보냄.
* `&`: 백그라운드 실행.

---

## 6. 요약 및 팁

* **버전 확인**: 실행 전 `python3 --version`으로 올바른 버전을 사용하는지 확인하세요.
* **패키지 경로**: 스크립트 내에서 다른 모듈을 임포트하지 못한다면 `PYTHONPATH` 환경 변수를 확인해야 합니다.
* **Shebang 활용**: 파일 최상단에 `#!/usr/bin/env python3`를 추가하고 실행 권한(`chmod +x main.py`)을 주면 `./main.py`만으로도 실행 가능합니다.
