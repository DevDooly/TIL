# Logstash Logback Encoder 사용 가이드

`logstash-logback-encoder`는 Java 애플리케이션의 로그를 JSON 형식으로 구조화하여 출력해주는 가장 강력하고 대중적인 라이브러리입니다. 특히 SLF4J 2.0의 `addKeyValue` 기능을 완벽하게 지원합니다.

---

## 1. 의존성 추가 (Gradle)

최신 버전(7.4 기준)을 사용하면 SLF4J 2.0 기능을 별도 설정 없이 바로 사용할 수 있습니다.

```gradle
dependencies {
    implementation 'net.logstash.logback:logstash-logback-encoder:7.4'
}
```

---

## 2. 기본 설정 (logback-spring.xml)

콘솔에 JSON 형식으로 로그를 출력하는 가장 기본적인 설정입니다.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <appender name="JSON_CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder class="net.logstash.logback.encoder.LogstashEncoder">
            <!-- 인스턴스 이름 등 공통 필드 추가 가능 -->
            <customFields>{"service_name":"my-service"}</customFields>
        </encoder>
    </appender>

    <root level="INFO">
        <appender-ref ref="JSON_CONSOLE" />
    </root>
</configuration>
```

---

## 3. 핵심 기능 사용법

### 3.1 SLF4J 2.0 addKeyValue 지원
별도의 설정 없이도 `addKeyValue`로 추가한 데이터가 JSON 루트 레벨에 포함됩니다.

```java
log.atInfo()
   .addKeyValue("order_id", "ABC-123")
   .addKeyValue("amount", 5000)
   .log("주문 처리가 완료되었습니다.");
```
**출력 결과:**
```json
{
  "@timestamp": "2026-04-08T...",
  "message": "주문 처리가 완료되었습니다.",
  "order_id": "ABC-123",
  "amount": 5000,
  "level": "INFO"
}
```

### 3.2 ECS(Elastic Common Schema) 호환 설정
Elasticsearch나 Kibana를 사용 중이라 ECS 규격이 필요하다면, 필드 이름을 매핑하여 간단히 맞출 수 있습니다.

```xml
<encoder class="net.logstash.logback.encoder.LogstashEncoder">
    <fieldNames>
        <timestamp>@timestamp</timestamp>
        <level>log.level</level>
        <levelValue>[ignore]</levelValue> <!-- 불필요한 필드 제외 -->
        <stackTrace>error.stack_trace</stackTrace>
    </fieldNames>
</encoder>
```

---

## 4. 고급 활용

### 4.1 MDC 자동 포함
MDC에 담긴 값도 자동으로 JSON 필드에 포함됩니다. 별도의 `<includeMdc>` 설정이 필요 없으며, 기본적으로 모든 MDC 값이 출력됩니다.

### 4.2 비동기 로깅 (성능 최적화)
JSON 생성 및 I/O 부하를 줄이기 위해 `LoggingEventAsyncAppender`와 함께 사용하는 것을 권장합니다.

```xml
<appender name="ASYNC_JSON" class="ch.qos.logback.classic.AsyncAppender">
    <appender-ref ref="JSON_CONSOLE" />
    <queueSize>512</queueSize>
    <discardingThreshold>0</discardingThreshold>
</appender>
```

---

## 5. 결론

`logstash-logback-encoder`는 다음과 같은 상황에서 최선의 선택입니다.

* **SLF4J 2.0의 Fluent API(`addKeyValue`)를 적극 활용**하고 싶을 때.
* Logback 환경에서 가장 **유연하고 강력한 JSON 구조화**가 필요할 때.
* ElasticSearch, 로컬 파일 시스템 등 다양한 곳으로 로그를 보낼 때 필드명을 자유롭게 제어하고 싶을 때.
