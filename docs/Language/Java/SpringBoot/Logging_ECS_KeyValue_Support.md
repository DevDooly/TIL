# Spring Boot: SLF4J addKeyValue를 ECS 로그에 포함하기

Spring Boot 3.x(SLF4J 2.0+) 환경에서 `log.atInfo().addKeyValue("key", "value").log()` 형식을 사용할 때, 이 커스텀 키-값 쌍이 Elastic ECS 로그에 나타나지 않는 문제를 해결하는 방법을 설명합니다.

---

## 1. 해결 방법 요약

1. **라이브러리 버전 확인**: `logback-ecs-encoder` 버전이 **1.5.0 이상**이어야 합니다.
2. **Logback 설정**: `logback.xml`의 `<encoder>` 설정 내에 `<includeSlf4jKeyValues>true</includeSlf4jKeyValues>`를 추가해야 합니다.

---

## 2. 상세 설정 단계

### 2.1 의존성 확인 (Gradle 기준)
SLF4J 2.0의 Key-Value 기능을 지원하는 최소 버전 이상의 인코더를 사용해야 합니다.

```gradle
dependencies {
    // 최소 1.5.0 이상 필수
    implementation 'co.elastic.logging:logback-ecs-encoder:1.5.0'
}
```

### 2.2 logback.xml 설정 수정
`EcsEncoder` 설정 내부에 `includeSlf4jKeyValues` 옵션을 명시적으로 활성화합니다.

```xml
<appender name="ECS_JSON" class="ch.qos.logback.core.ConsoleAppender">
    <encoder class="co.elastic.logging.logback.EcsEncoder">
        <serviceName>my-spring-app</serviceName>
        <!-- SLF4J 2.0 Key-Value 쌍 포함 활성화 -->
        <includeSlf4jKeyValues>true</includeSlf4jKeyValues>
        <!-- 필요 시 MDC도 포함 -->
        <includeMdc>true</includeMdc>
    </encoder>
</appender>
```

---

## 3. 코드 사용 예시

Java 코드에서 다음과 같이 호출하면 ECS JSON 로그의 루트 레벨에 해당 키가 추가됩니다.

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class MyService {
    private static final Logger log = LoggerFactory.getLogger(MyService.class);

    public void process(String orderId) {
        log.atInfo()
           .addKeyValue("order_id", orderId)
           .addKeyValue("custom_tag", "urgent")
           .log("주문 처리를 시작합니다.");
    }
}
```

### 출력 결과 (ECS JSON)
```json
{
  "@timestamp": "2026-04-07T...",
  "log.level": "INFO",
  "message": "주문 처리를 시작합니다.",
  "ecs.version": "1.2.0",
  "order_id": "12345",         // addKeyValue로 추가된 값
  "custom_tag": "urgent"       // addKeyValue로 추가된 값
}
```

---

## 4. 주의사항

* **MDC와의 차이**: `MDC`는 해당 스레드의 모든 로그에 유지되지만, `addKeyValue`는 **해당 로그 라인 딱 하나**에만 기록됩니다. 일시적인 컨텍스트 전달에 매우 유리합니다.
* **중복 키**: ECS 표준 필드(예: `message`, `log.level`)와 겹치는 키를 사용하면 인코더 설정에 따라 덮어쓰거나 무시될 수 있으므로 주의가 필요합니다.
