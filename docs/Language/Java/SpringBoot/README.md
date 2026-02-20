# Spring Boot

Spring Boot 관련 학습 내용을 정리합니다.

## 목차
*   **[Spring Boot Introduction](SpringBoot_Intro.md)**: Spring Boot의 핵심 목표, 특징 및 Legacy Spring과의 차이점
*   **[DI & IoC](DI_IoC.md)**: 의존성 주입(DI)과 제어의 역전(IoC) 개념 및 주입 방식
*   **[AOP (Aspect Oriented Programming)](AOP.md)**: 관점 지향 프로그래밍과 Spring AOP 적용
*   **[Bean Lifecycle](Bean_Lifecycle.md)**: 스프링 빈의 생명주기와 콜백 메소드
*   **[OAuth2 Implementation](OAuth2_Implementation.md)**: Spring Security를 이용한 OAuth2 Client 및 Resource Server 구현
*   **[Spring MVC](SpringMVC.md)**: DispatcherServlet을 중심으로 한 MVC 패턴 구조 및 요청 처리 흐름
*   **[Spring WebFlux](Web/SpringWebFlux.md)**: 리액티브 프로그래밍(Non-blocking I/O) 모델과 Mono/Flux 개념 이해
*   **[Spring Data JPA](JPA/Persistence_Context.md)**: 영속성 컨텍스트와 JPA의 핵심 동작 원리

## 학습 예정 (To-Be Added)

### 1. Spring Data JPA (데이터 접근 계층)
*   **JPA Persistence Context (영속성 컨텍스트)**: 1차 캐시, 더티 체킹의 원리.
*   **N+1 문제와 Fetch Join**: 실무 성능 최적화의 핵심.
*   **QueryDSL**: 복잡한 동적 쿼리 처리 방법.
*   **@Transactional**: 트랜잭션 전파 레벨(Propagation)과 격리 수준(Isolation) 설정.

### 2. Spring Security (보안)
*   **Spring Security Architecture**: FilterChainProxy와 인증/인가 프로세스.
*   **JWT 구현**: Spring Security Filter를 커스텀하여 JWT 인증 구현하기.
*   **OAuth2 Client**: 구글, 카카오 로그인 연동.

### 3. Testing (테스트)
*   **Unit Test vs Integration Test**: `@SpringBootTest`와 `@WebMvcTest`, `@DataJpaTest`의 차이와 용도.
*   **Mockito**: Service 계층 테스트 시 Mock 객체 활용법.
*   **RestDocs**: 테스트 코드를 기반으로 API 문서 자동화.

### 4. Integration (인프라 연동)
*   **Spring Boot + Redis**: 캐싱 전략 (`@Cacheable`) 및 Session Clustering.
*   **Spring Boot + Message Broker**: RabbitMQ/Kafka 연동 및 이벤트 기반 아키텍처 구현.
*   **Scheduling & Batch**: 주기적인 작업(`@Scheduled`)과 대용량 배치 처리(Spring Batch).

### 5. Observability (운영 및 모니터링)
*   **Actuator**: 애플리케이션 상태 모니터링 및 메트릭 수집.
*   **Prometheus & Grafana 연동**: Actuator 데이터를 시각화.
