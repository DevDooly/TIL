# Spring Cloud Zuul: API Gateway 및 동적 라우팅 가이드

**Zuul**은 Netflix에서 개발한 JVM 기반의 라우터이자 서버 측 부하 분산기입니다. Spring Cloud 환경에서 마이크로서비스들의 앞단에 위치하여 모든 요청을 적절한 서비스로 전달하는 **API Gateway** 역할을 수행합니다.

> ⚠️ **주의**: Zuul 1.x는 현재 유지보수 모드(Maintenance Mode)이며, Spring Boot 2.4+ 이상 및 최신 Spring Cloud에서는 **Spring Cloud Gateway** 사용을 권장합니다.

---

## 1. Zuul의 핵심 역할

1. **인증 및 보안**: 각 서비스마다 구현할 필요 없이 Gateway 레벨에서 인증/인가 처리.
2. **동적 라우팅**: 요청 URL에 따라 적절한 마이크로서비스로 요청을 전달.
3. **모니터링 및 로깅**: 모든 트래픽이 통과하므로 통합 지표 수집에 용이.
4. **부하 조절**: 정해진 한도 이상의 요청이 들어올 경우 차단.
5. **정적 응답 처리**: 특정 요청에 대해 서비스까지 가지 않고 바로 응답 반환.

---

## 2. Zuul 필터 메커니즘

Zuul의 모든 로직은 **Filter**를 통해 실행됩니다. 요청의 생명주기에 따라 4가지 타입의 필터가 존재합니다.

* **PRE Filter**: 대상 서비스로 라우팅되기 전에 실행 (인증, 로깅, 파라미터 검증 등).
* **ROUTING Filter**: 요청을 대상 서비스로 전달하는 단계.
* **POST Filter**: 대상 서비스로부터 응답을 받은 후 실행 (응답 헤더 추가, 통계 지표 수집 등).
* **ERROR Filter**: 위 단계 중 에러 발생 시 실행.

---

## 3. 기본 사용법 (Spring Boot 2.x 기준)

### 3.1 의존성 추가 (Gradle)
```gradle
dependencies {
    implementation 'org.springframework.cloud:spring-cloud-starter-netflix-zuul'
}
```

### 3.2 메인 클래스 설정
`@EnableZuulProxy` 어노테이션을 추가하여 Zuul 기능을 활성화합니다.

```java
@SpringBootApplication
@EnableZuulProxy // Zuul Proxy 활성화
public class GatewayApplication {
    public static void main(String[] args) {
        SpringApplication.run(GatewayApplication.class, args);
    }
}
```

### 3.3 라우팅 설정 (application.yml)
요청 경로와 대상 서비스(또는 URL)를 매핑합니다.

```yaml
zuul:
  routes:
    user-service: # 서비스 ID 기반 (Eureka 연동 시)
      path: /user/**
      serviceId: user-service
    google: # 외부 URL 기반
      path: /google/**
      url: https://www.google.com
```

---

## 4. 커스텀 필터 구현 예시

`ZuulFilter`를 상속받아 직접 필터를 만들 수 있습니다.

```java
@Component
public class MyPreFilter extends ZuulFilter {
    @Override
    public String filterType() { return "pre"; } // 필터 타입

    @Override
    public int filterOrder() { return 1; } // 실행 순서

    @Override
    public boolean shouldFilter() { return true; } // 필터 실행 여부

    @Override
    public Object run() {
        RequestContext ctx = RequestContext.getCurrentContext();
        HttpServletRequest request = ctx.getRequest();
        System.out.println("Request Method: " + request.getMethod());
        return null;
    }
}
```

---

## 5. 결론 및 대안

Zuul 1.x는 블로킹 I/O 기반으로 설계되어 대규모 트래픽 처리에 한계가 있을 수 있습니다. 따라서 신규 프로젝트를 시작한다면 비동기/논블로킹(Netty) 기반의 **Spring Cloud Gateway**를 사용하는 것이 강력히 권장됩니다.

* **Zuul 1**: Servlet 기반, Blocking I/O.
* **Spring Cloud Gateway**: Spring WebFlux 기반, Non-blocking I/O, 더 나은 성능.
