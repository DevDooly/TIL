# Python Web Server 실행 방식 비교: `python main.py` vs CLI Runner

Python 웹 프레임워크(FastAPI, Flask 등)를 실행할 때 사용하는 두 가지 주요 방식의 차이점과 용도별 권장 사항을 정리합니다.

---

## 1. 직접 실행 방식 (`python main.py`)

Python 인터프리터가 소스 코드를 직접 읽어서 실행하는 방식입니다. 이 방식이 작동하려면 코드 내부에 서버를 구동하는 "엔트리 포인트(Entry Point)" 코드가 포함되어야 합니다.

### 💻 코드 예시 (FastAPI)
```python
import uvicorn
from fastapi import FastAPI

app = FastAPI()

if __name__ == "__main__":
    # 코드가 직접 실행될 때만 uvicorn 서버를 구동함
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

* **특징**:
    * **IDE 디버깅 최적화**: PyCharm이나 VS Code에서 브레이크포인트를 걸고 디버깅할 때 가장 편리합니다.
    * **명시적 구성**: 호스트, 포트 등 서버 설정을 코드 내에서 로직으로 제어할 수 있습니다.
* **주의**: 운영 환경에서는 이 방식을 거의 사용하지 않습니다.

---

## 2. CLI Runner 방식 (`uvicorn`, `flask run`)

프레임워크나 ASGI/WSGI 서버 라이브러리에서 제공하는 전용 실행 도구를 사용하는 방식입니다. 서버 프로그램이 내 코드를 **임포트(Import)**하여 실행합니다.

### 💻 명령어 예시
```bash
# FastAPI (Uvicorn)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Flask
export FLASK_APP=main.py
flask run --reload
```

* **특징**:
    * **관심사의 분리**: 코드에는 비즈니스 로직만 남기고, 서버 설정(포트, 워커 수 등)은 명령어 인자로 관리합니다.
    * **기능 확장성**: `--reload`(코드 수정 시 자동 재시작), `--workers`(멀티 프로세스) 등 개발 및 운영 편의 기능을 명령어로 쉽게 제어합니다.
    * **운영 표준**: 실제 서비스 배포 환경과 가장 유사한 구조를 가집니다.

---

## 3. 주요 차이점 비교

| 구분 | `python main.py` | CLI Runner (`uvicorn`, `flask run`) |
| :--- | :--- | :--- |
| **주도권** | 내 코드가 서버를 호출함 | 서버가 내 코드를 불러옴(Import) |
| **엔트리 포인트** | `if __name__ == "__main__":` 필요 | 필요 없음 (비즈니스 로직에 집중) |
| **설정 관리** | 코드 내 변수로 관리 | CLI 인자 또는 환경 변수 |
| **디버깅** | IDE 디버거와 호환성 매우 좋음 | 추가 설정 필요 (예: Remote Debug) |
| **운영 환경** | 비권장 | **권장** (Gunicorn 등과 조합) |

---

## 4. 상황별 권장 패턴

### ✅ 개발 및 디버깅

* 단순 코딩 및 테스트: **CLI Runner** (`uvicorn main:app --reload`)
* 깊이 있는 로직 디버깅: **직접 실행** (`python main.py`) 후 IDE 브레이크포인트 활용

### ✅ 운영 환경 (Production)

* **FastAPI**: `gunicorn -k uvicorn.workers.UvicornWorker main:app` (Gunicorn의 프로세스 관리 + Uvicorn의 비동기 성능 조합)
* **Flask**: `gunicorn -w 4 main:app`

---

## 5. 결론

`python main.py`는 **"내가 서버를 라이브러리로서 부리는 것"**이고, `uvicorn` 등은 **"전문 서버 엔진에 내 코드를 탑재하는 것"**입니다. 개발 시에는 편리한 CLI 옵션을 제공하는 후자를 주로 사용하되, 정밀한 디버깅이 필요할 때만 전자를 사용하는 것이 효율적입니다.
