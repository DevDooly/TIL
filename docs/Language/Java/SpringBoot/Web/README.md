# Spring Web Development

Spring Boot를 활용한 웹 개발은 크게 두 가지 기술 스택으로 나뉩니다.

## 1. Spring MVC (Servlet Stack)
*   전통적인 서블릿 기반의 웹 프레임워크입니다.
*   Blocking I/O 모델을 사용하며, 요청당 하나의 스레드(Thread-per-Request)를 할당합니다.
*   안정성이 높고 디버깅이 쉬워 대부분의 엔터프라이즈 애플리케이션에서 사용됩니다.
*   **[Filter vs Interceptor](Filter_vs_Interceptor.md)**: 공통 로직 처리를 위한 필터와 인터셉터의 차이 이해

## 2. Spring WebFlux (Reactive Stack)
*   Spring 5.0부터 도입된 리액티브 웹 프레임워크입니다.
*   Non-blocking I/O와 Event Loop 모델을 사용하여 적은 수의 스레드로 대량의 동시 요청을 처리합니다.
*   높은 성능과 확장성이 필요한 마이크로서비스 게이트웨이나 스트리밍 서비스에 적합합니다.

## 기술 스택 선택 가이드

| 고려 사항 | Spring MVC | Spring WebFlux |
| :--- | :--- | :--- |
| **개발 난이도** | 낮음 (익숙한 모델) | 높음 (비동기 흐름 제어 필요) |
| **DB 드라이버** | JDBC (Blocking) | R2DBC (Non-blocking) |
| **적합한 환경** | 일반적인 웹 앱, CRUD | 고성능, 높은 동시성, 스트리밍 |
