---
title: Python Engineering & Concurrency
---

# 🐍 Python Engineering & Concurrency

데이터 엔지니어링, 비동기 고성능 웹 서비스, 분산 작업 처리 및 프로덕션 환경 구축을 위한 **Python 심화 문법, 비동기 I/O(FastAPI/Asyncio), Pika(RabbitMQ) 메시징 및 폐쇄망 패키징 기법**을 다룹니다.

---

## 📚 주요 기술 문서 목차

### 1. Concurrency & Web Architecture
* **[FastAPI 동시성(Concurrency) 처리 메커니즘](FastAPI_Concurrency_Mechanism.md)**: `async def` vs 일반 `def` 라우트 핸들러의 스레드 풀 할당 차이
* **[Gunicorn vs Uvicorn](Gunicorn_vs_Uvicorn.md)**: ASGI/WSGI 아키텍처 및 프로덕션 멀티 프로세스 워커 운영 전략
* **[Python Web Server 실행 방식 비교](Server_Execution_Methods.md)**: CLI Runner vs 스크립트 기반 실행 장단점
* **[AIOHTTP vs Flask](AIOHTTP%20vs%20Flask.md)**: 비동기 논블로킹 클라이언트/서버와 동기 프레임워크 비교

### 2. Distributed Messaging & Async I/O
* **[Pika (RabbitMQ) 비동기 컨슈머 구현 가이드](pika/Asynchronous%20consumer%20example.md)**: `SelectConnection` 기반의 고성능 논블로킹 이벤트 루프 컨슈머
* **[Pika BlockingConnection](pika/BlockingConnection.md)**: 동기 방식 메시지 큐 통신 및 재연결 패턴
* **[Asyncio Streams](Asyncio_Streams.md)**: TCP 고수준 스트림을 활용한 비동기 소켓 클라이언트/서버
* **[Socket Programming](Socket%20Programming.md)**: 저수준 소켓 통신 기본 원리

### 3. Advanced Python & Clean Code
* **[Python Decorator (데코레이터)](Decorator.md)**: `@functools.wraps`, 매개변수 데코레이터, 클래스 데코레이터 및 실무 활용
* **[MetaClass (메타클래스)](메타클래스.md)**: 클래스 생성 가로채기 및 프레임워크 수준의 검증 로직
* **[정적메소드 (@staticmethod vs @classmethod)](정적메소드.md)**: 팩토리 메서드 및 유틸리티 메서드 설계 원칙
* **[Designing Modules in Python](Designing%20Modules%20in%20Python.md)**: 모듈 인터페이스 추상화 및 결합도 완화
* **[Retry Decorator](retry.md)**: 지수 백오프(Exponential Backoff)를 적용한 안정적인 재시도 패턴
* **[orjson](orjson.md)**: C/Rust 기반 초고속 JSON 직렬화/역직렬화 라이브러리

### 4. Production & Offline Deployment (폐쇄망 환경)
* **[폐쇄망 환경 Python 3.12 설치 가이드](Offline_Installation_Guide.md)**: 외부망이 차단된 서버에서 소스 컴파일 및 RPM 의존성 패키징
* **[오프라인 venv 및 pip 패키지 설치 가이드](Offline_Venv_Pip_Guide.md)**: Wheel 번들링을 통한 완전 오프라인 환경 배포 자동화
* **[venv vs Conda](venv_vs_Conda.md)**: 시스템 라이브러리 의존성과 가상 환경 선택 기준
* **[Conda, Anaconda, Miniconda](Conda_Anaconda_Miniconda.md)**: 가상환경 아키텍처 비교
