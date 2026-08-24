---
title: Spring Boot & Cloud Architecture
---

# 🍃 Spring Boot Framework

엔터프라이즈 마이크로서비스 및 고성능 백엔드 애플리케이션 구축을 위한 **Spring Boot 핵심 원리, Spring Cloud, 관찰 가능성(Logging/Metrics), 웹 계층(MVC/WebFlux) 및 데이터 접근 전략**을 다룹니다.

---

## 📚 주요 기술 문서 목차

### 1. Spring Core & Internals
* **[Spring Boot Introduction](SpringBoot_Intro.md)**: 자동 구성(Auto-Configuration) 및 스프링 부트 철학
* **[DI & IoC](DI_IoC.md)**: 의존성 주입(DI)과 제어의 역전(IoC) 패턴
* **[AOP (Aspect Oriented Programming)](AOP.md)**: 프록시 기반의 횡단 관심사 분리
* **[Bean Lifecycle](Bean_Lifecycle.md)**: 빈 생성, 초기화 콜백 및 소멸 과정
* **[BeanPostProcessor](BeanPostProcessor.md)**: 빈 인스턴스화 후처리 및 동적 빈 조작
* **[@EnableAutoConfiguration vs @ConfigurationPropertiesScan](EnableAutoConfiguration_vs_ConfigurationPropertiesScan.md)**: 프로퍼티 바인딩 및 자동 구성 메커니즘
* **[ThreadPoolTaskScheduler](ThreadPoolTaskScheduler.md)**: 작업 예약 및 스케줄러 스레드 풀 튜닝

### 2. Concurrency & Performance Tuning
* **[Finding Blocking Operations](Finding_Blocking_Operations.md)**: 블로킹 I/O 감지 및 진단 기법
* **[JDBI Virtual Thread Pinning Solution](JDBI_VT_Pinning_Solution.md)**: DB 블로킹 I/O와 가상 스레드 조화
* **[Virtual Thread Pinning in Kafka Consumer](Virtual_Thread_Pinning_Kafka.md)**: 카프카 컨슈머 폴링 루프 스레드 최적화
* **[Tomcat vs Netty](Tomcat_vs_Netty.md)**: 전통적 멀티스레드 서블릿 컨테이너와 이벤트 기반 리액티브 엔진 비교

### 3. Web & Security
* **[Spring MVC](Web/SpringMVC.md)**: DispatcherServlet 중심의 동기 요청 처리 흐름
* **[Spring WebFlux](Web/SpringWebFlux.md)**: Project Reactor 기반 논블로킹 리액티브 웹 스택
* **[Filter vs Interceptor](Web/Filter_vs_Interceptor.md)**: 서블릿 필터와 스프링 인터셉터의 라이프사이클 및 용도 차이
* **[Servlet vs Servlet Container](Web/Servlet_vs_ServletContainer.md)**: 서블릿 명세와 톰캣 동작 원리
* **[OAuth2 Implementation](OAuth2_Implementation.md)**: Spring Security 기반 OAuth2 Client 및 리소스 서버

### 4. Logging & Observability (Spring Boot 3.4+)
* **[Spring Boot 3.4 Structured Logging](Structured_Logging_SpringBoot_3_4.md)**: Elastic Common Schema(ECS) 포맷 구조화 로깅
* **[Logback JSON Composite Encoder](Logback_JSON_Composite_Encoder.md)**: 커스텀 JSON 로깅 인코더 구현
* **[Logstash Logback Encoder Guide](Logstash_Logback_Encoder_Guide.md)**: ELK 연동을 위한 JSON 로깅
* **[Logging Config Migration (YAML to XML)](Logging_Config_Migration_YAML_to_XML.md)**: 복잡한 로깅 설정 마이그레이션

### 5. Spring Cloud & Microservices
* **[Spring Cloud Gateway](Spring_Cloud_Gateway.md)**: 비동기 논블로킹 API 게이트웨이 라우팅
* **[SCG vs Netflix Zuul](SCG_vs_Zuul_Comparison.md)**: 블로킹 vs 논블로킹 게이트웨이 아키텍처 비교
* **[Spring Cloud LoadBalancer](Spring_Cloud_LoadBalancer.md)**: 클라이언트 사이드 로드 밸런싱

### 6. Testing & Quality
* **[Mockito 단위 테스트 활용 가이드](Testing/Mockito_Guide.md)**: 단위 테스트를 위한 Mockito 모킹 및 행위 검증
