---
title: Backend & Programming Languages
---

# ☕ Language & Runtime Ecosystem

현대 백엔드 아키텍처와 고성능 데이터 처리를 뒷받침하는 핵심 프로그래밍 언어 및 런타임 기술을 정리한 공간입니다.

단순한 문법 학습을 넘어, **메모리 모델(JVM / CPython), 동시성 제어(Virtual Threads / Event Loop / Asyncio), 프로세스 간 제로카피 IPC(Apache Arrow mmap), 프레임워크 내부 원리(Spring Boot / FastAPI)**를 다룹니다.

---

## 🗂️ Language Categories

<div class="grid cards" markdown>

-   :material-language-java: **[Java & Spring Ecosystem](Java/README.md)**

    ---

    - **JVM Internals**: Runtime Data Areas, Garbage Collection
    - **Modern Concurrency**: Java 21+ Virtual Threads, Scoped Value
    - **Spring Boot 3.x**: Bean Lifecycle, WebFlux, Structured Logging
    - **High-Performance Data**: Apache Arrow & mmap Zero-copy IPC

    [:octicons-arrow-right-24: Java 문서 보기](Java/README.md)

-   :material-language-python: **[Python & Asynchronous Web](Python/README.md)**

    ---

    - **Concurrency & Web**: FastAPI 동시성 모델, Gunicorn vs Uvicorn
    - **Advanced Python**: Decorators, Metaclass, Concurrency, Socket
    - **Distributed Systems**: Pika (RabbitMQ Asynchronous Consumer)
    - **Production Readiness**: 오프라인 폐쇄망 배포, 가상환경 전략

    [:octicons-arrow-right-24: Python 문서 보기](Python/README.md)

-   :material-nodejs: **[Node.js & Runtime](NodeJs/README.md)**

    ---

    - **Core Engine**: Libuv 비동기 I/O 및 6개 Event Loop Phases
    - **Modern Tooling**: Yarn Berry (Zero-installs & PnP)

    [:octicons-arrow-right-24: Node.js 문서 보기](NodeJs/README.md)

</div>
