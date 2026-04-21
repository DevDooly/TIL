# Spring Cloud Gateway (SCG): 차세대 API Gateway 가이드

**Spring Cloud Gateway**는 Spring WebFlux 위에서 구축된 API Gateway 서비스입니다. 비동기 및 논블로킹 방식으로 동작하며, 마이크로서비스 아키텍처(MSA)에서 요청을 효율적으로 라우팅하고 공통적인 횡단 관심사(보안, 모니터링, 부하 제한 등)를 처리합니다.

---

## 1. 핵심 구성 요소

Spring Cloud Gateway는 세 가지 주요 개념으로 구성됩니다.

1. **Route (경로)**: Gateway의 기본 빌딩 블록입니다. ID, 목적지 URI, Predicate 세트, Filter 세트로 구성됩니다.
2. **Predicate (조건)**: HTTP 요청이 경로와 일치하는지 판단하는 조건입니다. (예: 특정 헤더, 경로, 파라미터 등)
3. **Filter (필터)**: 요청 또는 응답을 수정할 수 있는 WebFilter 인스턴스입니다. (예: 헤더 추가, 인증 등)

---

## 2. Spring Cloud Gateway vs Netflix Zuul

| 구분 | Netflix Zuul (1.x) | Spring Cloud Gateway |
| :--- | :--- | :--- |
| **기반 기술** | Servlet (Blocking I/O) | WebFlux (Non-blocking I/O) |
| **성능** | 상대적으로 낮음 | **매우 높음** |
| **유연성** | 제한적임 | 매우 높음 (Java DSL 지원) |
| **장기 지원** | 유지보수 모드 | **활발한 개발 진행 중** |

---

## 3. 기본 사용법

### 3.1 의존성 추가 (Gradle)
```gradle
dependencies {
    implementation 'org.springframework.cloud:spring-cloud-starter-gateway'
}
```

### 3.2 라우팅 설정 (application.yml)
가장 일반적인 YAML 방식의 설정 예시입니다.

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: user-service # 고유 아이디
          uri: lb://USER-SERVICE # 목적지 (Load Balancer 사용 시)
          predicates:
            - Path=/user/** # /user/로 시작하는 요청만 매핑
          filters:
            - AddRequestHeader=X-Request-Foo, Bar # 요청 헤더 추가
            - AddResponseHeader=X-Response-Hello, World # 응답 헤더 추가
```

### 3.3 Java DSL 방식 설정
프로그래밍 방식으로 더 동적인 라우팅이 필요한 경우 사용합니다.

```java
@Bean
public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
    return builder.routes()
        .route("order-route", r -> r.path("/order/**")
            .filters(f -> f.addRequestHeader("Hello", "World"))
            .uri("http://order-service:8081"))
        .build();
}
```

---

## 4. 주요 내장 필터 활용

* **RewritePath**: 요청 경로를 변경하여 전달합니다.
    ```yaml
    filters:
      - RewritePath=/old/(?<segment>.*), /new/${segment}
    ```

* **RequestRateLimiter**: Redis 등을 사용하여 API 호출 속도를 제한합니다.
* **Retry**: 요청 실패 시 자동으로 재시도합니다.

---

## 5. 결론

Spring Cloud Gateway는 현대적인 MSA 환경에서 **성능과 유연성을 모두 잡은 표준 API Gateway**입니다. Zuul을 사용 중인 프로젝트라면 SCG로의 전환을 강력히 고려해야 하며, 신규 프로젝트라면 반드시 SCG를 선택하는 것이 좋습니다.
