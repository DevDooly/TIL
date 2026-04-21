# Spring Cloud LoadBalancer: 현대적인 클라이언트 측 부하 분산 가이드

**Spring Cloud LoadBalancer**는 Netflix Ribbon의 중단(Maintenance Mode) 이후, Spring Cloud 팀에서 직접 개발하여 제공하는 새로운 표준 클라이언트 측 부하 분산기입니다.

---

## 1. 주요 특징 및 Ribbon과의 차이점

| 특징 | Netflix Ribbon | Spring Cloud LoadBalancer |
| :--- | :--- | :--- |
| **I/O 모델** | Blocking I/O 위주 | **Non-blocking (Reactive) 지원** |
| **의존성** | Netflix 에코시스템 종속 | **Spring Framework 기반 (경량)** |
| **알고리즘** | 다양한 내장 알고리즘 | 기본은 라운드 로빈 (확장 가능) |
| **유연성** | 설정이 다소 복잡함 | Spring의 프로그래밍 모델과 긴밀히 통합 |

---

## 2. 기본 사용법

### 2.1 의존성 추가 (Gradle)
보통 `spring-cloud-starter-netflix-eureka-client` 등을 포함하면 자동으로 들어오지만, 단독으로 사용할 때는 다음과 같이 추가합니다.

```gradle
dependencies {
    implementation 'org.springframework.cloud:spring-cloud-starter-loadbalancer'
}
```

### 2.2 RestTemplate과 연동 (@LoadBalanced)
가장 일반적인 사용 방식입니다. 

```java
@Configuration
public class RestClientConfig {
    @Bean
    @LoadBalanced // 이 어노테이션이 핵심입니다.
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}

// 서비스 코드
@Service
public class MyService {
    @Autowired
    private RestTemplate restTemplate;

    public String callService() {
        // IP 대신 서비스 ID를 사용합니다.
        return restTemplate.getForObject("http://USER-SERVICE/info", String.class);
    }
}
```

---

## 3. 고급 활용: 커스텀 설정

특정 서비스에 대해 다른 로드 밸런싱 정책을 적용하고 싶을 때 사용합니다.

### 3.1 커스텀 설정 클래스 작성
```java
public class CustomLoadBalancerConfiguration {
    @Bean
    public ReactorLoadBalancer<ServiceInstance> randomLoadBalancer(
            Environment env, LoadBalancerClientFactory factory) {
        String name = env.getProperty(LoadBalancerClientFactory.PROPERTY_NAME);
        return new RandomLoadBalancer(factory.getLazyProvider(name, ServiceInstanceListSupplier.class), name);
    }
}
```

### 3.2 서비스별 적용
```java
@Configuration
@LoadBalancerClient(name = "user-service", configuration = CustomLoadBalancerConfiguration.class)
public class WebConfig { }
```

---

## 4. 캐싱(Caching) 기능

Spring Cloud LoadBalancer는 성능 향상을 위해 서비스 인스턴스 목록을 캐싱합니다. 기본적으로 Caffeine 기반의 캐시를 사용하도록 설정되어 있습니다.

```yaml
spring:
  cloud:
    loadbalancer:
      cache:
        enabled: true
        ttl: 30s # 캐시 유지 시간
```

---

## 5. 결론: 왜 이것을 써야 하는가?

1. **미래 보장**: Ribbon은 더 이상 발전하지 않지만, Spring Cloud LoadBalancer는 지속적으로 개선되고 있습니다.
2. **WebFlux 호환성**: 비동기 논블로킹 환경(`WebClient`)에서도 완벽하게 동작합니다.
3. **Spring 네이티브**: Spring Cloud Gateway나 OpenFeign과 같은 다른 Spring Cloud 컴포넌트들과 설정 충돌 없이 부드럽게 작동합니다.

### 요약
> **현대적인 MSA 프로젝트라면 고민 없이 Spring Cloud LoadBalancer를 선택하는 것이 표준입니다.**
