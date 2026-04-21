# Spring Cloud Gateway vs Netflix Zuul: 아키텍처 비교 및 선택 가이드

MSA 환경의 입구 역할을 하는 API Gateway 도구인 **Spring Cloud Gateway(SCG)**와 **Netflix Zuul**의 기술적 차이점을 심층 분석하고, 최적의 선택안을 제시합니다.

---

## 1. 기술 아키텍처 비교

가장 결정적인 차이는 **요청을 처리하는 방식(I/O 모델)**에 있습니다.

| 구분 | Netflix Zuul (1.x) | Spring Cloud Gateway |
| :--- | :--- | :--- |
| **기반 프레임워크** | Servlet 프레임워크 | Spring WebFlux (Project Reactor) |
| **네트워킹 서버** | Tomcat (Blocking I/O) | Netty (Non-blocking I/O) |
| **I/O 모델** | **Thread-per-request** | **Event-loop 기반 Non-blocking** |
| **의존성** | Spring Cloud Netflix | Spring Cloud Starter Gateway |

### Netflix Zuul 1.x (Blocking)

* 하나의 요청당 하나의 스레드를 할당합니다.
* I/O 작업(예: 하위 서비스 호출)이 발생하면 스레드는 응답이 올 때까지 기다립니다(Block).
* 동시 접속자가 많아지면 스레드 풀이 고갈되어 성능이 급격히 저하될 수 있습니다.

### Spring Cloud Gateway (Non-blocking)

* 적은 수의 스레드로 수많은 요청을 처리합니다.
* I/O 작업 시 스레드는 기다리지 않고 다른 요청을 처리하러 이동합니다(Event-loop).
* 대규모 트래픽과 높은 동시성을 처리하는 데 훨씬 유리합니다.

---

## 2. 주요 기능 차이

1. **유연성**: SCG는 Java DSL(Fluent API)을 지원하여 프로그래밍 방식으로 라우팅을 정의하기 훨씬 수월합니다.
2. **통합성**: SCG는 Spring 생태계(Security, Monitoring 등)와 더 긴밀하게 통합되어 있습니다.
3. **장기 지원**: Zuul 1.x는 현재 유지보수 모드입니다. Spring 진영은 공식적으로 SCG를 밀고 있습니다.

---

## 3. 어떤 것이 더 나은가? (결론: SCG의 승리)

결론부터 말씀드리면, **거의 모든 면에서 Spring Cloud Gateway가 더 낫습니다.**

### 왜 SCG인가?

1. **압도적 성능**: 논블로킹 방식 덕분에 동시 접속자가 많을수록 Zuul보다 적은 리소스로 훨씬 높은 처리량(Throughput)을 보여줍니다.
2. **Spring 공식 지원**: Spring Cloud 팀에서 직접 개발하고 관리하므로 안정성과 미래 가치가 높습니다.
3. **WebFlux 활용**: 비동기 프로그래밍 모델을 사용하여 복잡한 필터 로직을 더 효율적으로 작성할 수 있습니다.

---

## 4. 모든 상황에서 SCG가 나은가? (예외 상황)

이론적으로는 SCG가 뛰어나지만, **다음과 같은 경우에는 Zuul(또는 기존 방식)을 유지하거나 고려**할 수 있습니다.

1. **레거시 인프라**: 이미 Zuul로 구축된 시스템이 안정적으로 동작 중이며, 전환 비용(테스트, 공수)이 성능 이점보다 훨씬 클 경우.
2. **Servlet 기반 제약**: 전체 시스템이 서블릿 필터나 세션 방식에 강하게 결합되어 있어, WebFlux(논블로킹) 환경으로 옮기기 어려운 특수한 경우.
3. **간단한 소규모 앱**: 트래픽이 매우 적고 성능이 중요하지 않으며, 이미 Zuul에 익숙한 팀원들만 있을 때.

---

## 5. 최종 제안

* **신규 프로젝트**: 고민할 필요 없이 **Spring Cloud Gateway**를 선택하세요.
* **기존 Zuul 1.x 프로젝트**: 트래픽이 증가하여 성능 한계가 느껴진다면 **SCG로의 마이그레이션**을 강력히 권장합니다.
* **Zuul 2.x**: Netflix에서 비동기 기반인 Zuul 2.x를 내놓았지만, Spring Cloud와의 호환성 및 생태계 점유율 면에서 SCG에 밀려 현재는 주류가 아닙니다.

### 요약
> **성능, 확장성, 향후 지원 모든 면에서 Spring Cloud Gateway가 표준입니다.**
