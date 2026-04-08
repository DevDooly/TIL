# Spring Boot: SLF4J addKeyValue를 ECS 로그에 포함하기 (대안 가이드)

Spring Boot 3.x(SLF4J 2.0+) 환경에서 `addKeyValue` 기능을 사용할 때, 현재 공식 `logback-ecs-encoder`는 이 데이터를 자동으로 JSON 필드에 포함하는 옵션을 제공하지 않습니다.

---

## 1. 현재 상황 (확인된 사실)

* **`logback-ecs-encoder`**: 현재 `includeSlf4jKeyValues`와 같은 자동 추출 옵션이 존재하지 않습니다. (v1.5.0 기준 확인됨)
* **문제점**: `log.atInfo().addKeyValue("key", "value").log()`를 호출해도 JSON 결과물에 `key` 필드가 나타나지 않습니다.

---

## 2. 해결 방법: 대안 제시

### 방법 1: MDC (Mapped Diagnostic Context) 사용 (가장 안정적)
`logback-ecs-encoder`가 기본적으로 지원하는 MDC를 활용합니다. `addKeyValue`와 유사한 기능을 하면서 ECS 로그에 자동으로 포함됩니다.

```java
// Spring Boot 애플리케이션 코드
try (var ignored = MDC.putCloseable("order_id", "12345")) {
    log.info("주문 처리를 시작합니다.");
}
```

**logback.xml 설정**:
```xml
<encoder class="co.elastic.logging.logback.EcsEncoder">
    <includeMdc>true</includeMdc>
</encoder>
```

### 방법 2: logstash-logback-encoder 사용 (강력 추천)
이미 정교한 정형 로깅(Structured Logging)이 필요하다면, Elastic에서 제공하는 인코더 대신 **`logstash-logback-encoder`**를 사용하는 것이 훨씬 강력합니다. 이 인코더는 SLF4J 2.0의 `addKeyValue`를 **기본적으로 자동 인식**하여 JSON 필드에 넣어줍니다.

**의존성 추가**:
```gradle
dependencies {
    implementation 'net.logstash.logback:logstash-logback-encoder:7.4'
}
```

**logback.xml 설정 (ECS 호환 모드)**:
```xml
<encoder class="net.logstash.logback.encoder.LogstashEncoder">
    <!-- ECS 필드 이름으로 커스텀 매핑 가능 -->
    <fieldNames>
        <level>log.level</level>
        <timestamp>@timestamp</timestamp>
    </fieldNames>
</encoder>
```

---

## 3. 요약 및 권장 사항

1. **단순 키 추가**: MDC(`MDC.putCloseable`)를 사용하세요.
2. **본격적인 정형 로깅**: `logstash-logback-encoder`로 전환하는 것을 고려하세요. `addKeyValue`를 가장 완벽하게 지원하는 라이브러리입니다.

잘못된 정보로 혼란을 드려 다시 한번 사과드리며, 현재의 기술적 한계를 고려한 위 대안들 중 하나를 선택하시길 권장합니다.