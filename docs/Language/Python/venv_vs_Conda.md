# venv vs Conda: 어떤 가상환경을 선택해야 할까?

Python 프로젝트 시작 시 가상환경 도구로 `venv`와 `Conda` 중 무엇을 선택해야 할지에 대한 판단 기준과 가이드를 정리합니다.

---

## 1. 한 줄 요약 및 권장 사항

* **웹 개발 (FastAPI, Flask, Django)**: 👉 **`venv`** 권장
* **데이터 과학 / AI / ML**: 👉 **`Conda` (Miniconda)** 권장

---

## 2. 상세 비교

| 항목 | venv | Conda (Miniconda) |
| :--- | :--- | :--- |
| **설격** | Python 표준 라이브러리 | 데이터 과학 특화 배포판 |
| **관리 범위** | Python 패키지만 관리 | Python 버전 + 시스템 라이브러리 관리 |
| **무게** | 매우 가볍고 빠름 | 무겁고 패키지 분석에 시간이 걸림 |
| **배포 편의성** | Docker 등 표준 배포에 최적화 | 로컬 연구 환경 및 복잡한 의존성 해결에 최적화 |
| **설치 방법** | 기본 내장 | 별도 설치 필요 |

---

## 3. 웹 서버(FastAPI 등) 개발 시 `venv`가 유리한 이유

1. **가벼운 컨테이너 이미지**: Docker 배포 시 `venv` 기반은 이미지가 작고 빌드 속도가 빠릅니다.
2. **표준성**: 대부분의 클라우드 서비스(AWS, GCP 등)와 CI/CD 도구가 `pip` 기반의 표준 워크플로우를 우선 지원합니다.
3. **의존성 단순성**: 웹 프레임워크는 보통 시스템 라이브러리 의존성이 낮아 `pip`만으로도 충분히 안정적인 관리가 가능합니다.

---

## 4. `venv` 실전 활용 가이드 (FastAPI 예시)

### ① 가상환경 생성 및 활성화
```bash
# 가상환경 생성 (.venv라는 이름 권장)
python3 -m venv .venv

# 가상환경 활성화 (Linux/macOS)
source .venv/bin/activate

# 가상환경 활성화 (Windows)
# .venv\Scripts\activate
```

### ② 패키지 관리
```bash
# 패키지 설치
pip install fastapi uvicorn

# 설치된 패키지 목록 저장
pip freeze > requirements.txt

#설치된 목록으로부터 패키지 설치
pip install -r requirements.txt
```

---

## 5. Conda 배포판 비교(Anaconda vs Miniconda) 및 필수 명령어

데이터 과학이나 C/CUDA 의존성이 있는 프로젝트에서 Conda를 선택했다면, 불필요한 패키지(3GB+)가 포함된 **Anaconda** 대신 최소 필수 도구(약 400MB)만 포함된 **Miniconda**를 설치해 필요한 패키지만 구성하는 편이 훨씬 가볍다.

| 구분 | Anaconda | Miniconda (권장) |
| :--- | :--- | :--- |
| **설치 용량** | 약 3GB 이상 (250개+ 과학 패키지 기본 포함) | 약 400MB (Python + Conda 코어만 포함) |
| **주 용도** | 초기 설정 없이 바로 실습하는 입문·교육 환경 | 서버 배포, 컨테이너 빌드, 실무 개발 환경 |

### 주요 Conda 가상환경 및 `conda-forge` 설정 명령어

```bash
# 1. 커뮤니티 표준 채널(conda-forge) 추가 및 엄격한 우선순위 설정
conda config --add channels conda-forge
conda config --set channel_priority strict

# 2. 특정 Python 버전으로 가상환경 생성 및 활성화
conda create -n myenv python=3.12
conda activate myenv

# 3. 패키지 설치 및 가상환경 목록 확인
conda install numpy pandas
conda env list
```

---

## 6. 결론: 무엇을 쓸까?

* **간단한 API 서버, 마이크로서비스, 웹 앱**을 만든다면 고민하지 말고 **`venv`**를 사용하세요.
* **GPU를 사용한 딥러닝, 복잡한 데이터 분석, 라이브러리 간의 C-Extension 충돌**이 우려되는 환경이라면 **`Miniconda`**가 답입니다.
