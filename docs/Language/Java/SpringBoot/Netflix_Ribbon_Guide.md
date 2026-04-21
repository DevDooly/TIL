# Netflix Ribbon: 클라이언트 측 부하 분산(Load Balancing) 가이드

**Netflix Ribbon**은 MSA(Microservice Architecture) 환경에서 여러 서비스 인스턴스 중 하나를 선택하여 요청을 보낼 수 있게 해주는 **Client-side Load Balancer** 라이브러리입니다.

---

## 1. Ribbon이란?

전통적인 부하 분산(L4, L7 스위치 등)은 서버 앞단에 위치하지만, Ribbon은 **클라이언트(요청을 보내는 서비스) 내부에 위치**합니다.

### 핵심 작동 원리

1. **서비스 목록 조회**: Eureka와 같은 Service Discovery로부터 대상 서비스의 인스턴스 리스트를 가져옵니다.
2. **부하 분산 알고리즘 적용**: 라운드 로빈, 응답 시간 가중치 등 설정된 규칙에 따라 하나의 인스턴스를 선택합니다.
3. **요청 수행**: 선택된 인스턴스의 IP/Port로 실제 HTTP 요청을 보냅니다.

---

## 2. Zuul과 Ribbon의 관계

Zuul 1.x는 내부적으로 Ribbon을 사용하여 동적 라우팅과 부하 분산을 수행합니다.

* Zuul이 요청을 받으면 Ribbon을 통해 어떤 인스턴스로 보낼지 결정하고, Hystrix를 통해 장애 내성을 확보합니다.

---

## 3. Spring Cloud Gateway(SCG)에서도 Ribbon을 쓸 수 있나요?

결론부터 말씀드리면, **SCG에서는 Ribbon을 사용하지 않습니다.**

### 이유 및 대안

* **상태**: Ribbon은 현재 유지보수 모드(Maintenance Mode)입니다.
* **SCG의 방식**: SCG는 Ribbon 대신 Spring Cloud 팀에서 직접 만든 **Spring Cloud LoadBalancer**를 기본으로 사용합니다.
* **호환성**: Ribbon은 Blocking I/O 기반인 반면, SCG는 Non-blocking(WebFlux) 기반이므로 아키텍처적으로 어울리지 않습니다.

---

## 4. 사용 방법 (레거시 Zuul 환경 기준)

### 4.1 의존성 추가 (Gradle)
```gradle
dependencies {
    implementation 'org.springframework.cloud:spring-cloud-starter-netflix-ribbon'
}
```

### 4.2 설정 (application.yml)
특정 서비스에 대한 로드 밸런싱 규칙을 정의할 수 있습니다.

```yaml
# user-service에 대한 Ribbon 설정
user-service:
  ribbon:
    NFLoadBalancerRuleClassName: com.netflix.loadbalancer.WeightedResponseTimeRule # 응답 시간 기반
    ListOfServers: localhost:8081,localhost:8082 # (Eureka 없을 시 수동 지정)
```

---

## 5. 어떨 때 사용하면 좋은가?

1. **레거시 유지보수**: 이미 Zuul + Ribbon 기반으로 구축된 프로젝트를 관리할 때.
2. **단순 클라이언트 분산**: 서버 측 로드밸런서(L4/L7)를 별도로 두기 어려운 환경에서 애플리케이션 레벨의 분산이 필요할 때.

---

## 6. 결론: 현대적인 선택

현재 시점에서 Ribbon을 신규 프로젝트에 도입하는 것은 권장되지 않습니다.

* **Zuul 1.x 사용자**: Ribbon을 계속 사용하게 됩니다.
* **Spring Cloud Gateway 사용자**: **Spring Cloud LoadBalancer**를 사용하세요. 별도의 설정 없이 `lb://SERVICE-NAME` 형식을 사용하면 자동으로 동작합니다.
* **Feign Client 사용자**: 최신 버전에서는 자동으로 Spring Cloud LoadBalancer와 연동됩니다.

### 요약
> **Ribbon은 화려했던 과거의 유산이며, 현재는 Spring Cloud LoadBalancer가 그 자리를 대체했습니다.**
