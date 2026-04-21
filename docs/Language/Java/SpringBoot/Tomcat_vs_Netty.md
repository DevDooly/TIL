# Spring Boot: Tomcat vs Netty 비교 가이드

Spring Boot 애플리케이션 개발 시 사용되는 두 가지 대표적인 임베디드 서버 엔진, **Tomcat**과 **Netty**의 기술적 차이와 선택 기준을 정리합니다.

---

## 1. 핵심 아키텍처 차이

가장 큰 차이는 **요청 처리 모델(I/O 모델)**에 있습니다.

### 1.1 Apache Tomcat (Blocking I/O)

* **모델**: Thread-per-request 모델입니다.
* **동작**: 하나의 HTTP 요청당 하나의 워커 스레드(Worker Thread)가 할당됩니다. 요청이 들어와서 처리가 끝날 때까지 해당 스레드는 다른 일을 하지 못하고 기다립니다(Block).
* **스택**: 전통적인 **Spring MVC**의 기본 엔진입니다.

### 1.2 Netty (Non-blocking I/O)

* **모델**: Event-loop 모델입니다.
* **동작**: 소수의 스레드(Event-loop)가 수많은 요청을 처리합니다. I/O 작업(DB 조회, API 호출 등)이 발생하면 스레드는 기다리지 않고 다른 요청을 처리하러 이동하며, 작업이 완료되면 이벤트 알림을 받아 후속 처리를 합니다.
* **스택**: 비동기 논블로킹 기반의 **Spring WebFlux**의 기본 엔진입니다.

---

## 2. 장단점 비교

| 구분 | Apache Tomcat | Netty |
| :--- | :--- | :--- |
| **I/O 방식** | Blocking (BIO/NIO) | **Non-blocking (NIO)** |
| **리소스 사용** | 스레드가 많아 메모리 소비 큼 | 적은 스레드로 효율적 리소스 관리 |
| **복잡도** | 단순하고 직관적 (동기식) | 비동기 프로그래밍 지식 필요 |
| **최적 상황** | 전통적인 비즈니스 로직, CRUD | 대규모 접속, 실시간 스트리밍, Gateway |
| **안정성** | 검증된 기술, 풍부한 레퍼런스 | 고성능 처리에 특화 |

---

## 3. 어떤 것을 선택해야 할까?

### Tomcat이 유리한 경우

* 대부분의 **일반적인 엔터프라이즈 웹 애플리케이션**.
* 기존의 **JDBC** 기반 DB 드라이버나 동기식 라이브러리를 많이 사용하는 경우.
* 트래픽이 극단적으로 높지 않고, 개발 생산성과 익숙함이 중요한 경우.

### Netty가 유리한 경우

* **대규모 동시 접속** 처리가 필요한 서비스 (채팅, 알림 등).
* **API Gateway** (예: Spring Cloud Gateway).
* 마이크로서비스 간의 통신이 빈번하고 응답 지연을 최소화해야 하는 경우.
* **R2DBC**와 같은 비동기 DB 드라이버를 활용하는 **Spring WebFlux** 환경.

---

## 4. Spring Boot에서의 전환 방법

Spring Boot는 의존성 설정을 통해 서버를 쉽게 바꿀 수 있습니다.

### Tomcat에서 Netty로 (WebFlux 사용 시)
```gradle
dependencies {
    // web 대신 webflux를 포함하면 기본적으로 Netty가 사용됨
    implementation 'org.springframework.boot:spring-boot-starter-webflux'
}
```

### MVC에서 Netty를 쓰고 싶은 경우
기본적으로 Spring MVC는 서블릿 컨테이너(Tomcat)에 최적화되어 있어 Netty를 직접 쓰는 것은 권장되지 않지만, 특수한 경우 의존성을 수동으로 조정해야 합니다.

---

## 5. 결론

성능 수치만 보면 Netty가 우월해 보이지만, **Blocking 라이브러리가 섞여 있는 환경에서 Netty를 쓰면 오히려 성능이 급격히 저하(Event-loop 차단)**될 수 있습니다. 

따라서 **애플리케이션 전체 스택이 비동기를 지원하는지**를 먼저 판단한 후, 그에 맞춰 엔진을 선택하는 것이 가장 현명한 전략입니다.
