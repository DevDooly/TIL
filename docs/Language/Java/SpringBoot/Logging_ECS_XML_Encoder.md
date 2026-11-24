# Logback XML: logback-ecs-encoder를 이용한 정형 로깅 (ECS)

Spring Boot 3.4+에서는 YAML 설정만으로 ECS(Elastic Common Schema) 포맷을 지원하지만, 복잡한 로깅 요구사항(필터링, 멀티 앱펜더 등)으로 인해 `logback-spring.xml`을 직접 제어해야 하는 경우 오픈소스 라이브러리인 **`logback-ecs-encoder`**를 사용합니다.

---

## 1. 의존성 추가 (Dependency)

먼저 프로젝트의 `build.gradle` 또는 `pom.xml`에 Elastic에서 제공하는 ECS 인코더 의존성을 추가합니다.

**Gradle**:
```gradle
dependencies {
    implementation 'co.elastic.logging:logback-ecs-encoder:1.6.0'
}
```

**Maven**:
```xml
<dependency>
    <groupId>co.elastic.logging</groupId>
    <artifactId>logback-ecs-encoder</artifactId>
    <version>1.6.0</version>
</dependency>
```

---

## 2. logback-spring.xml 설정

`EcsEncoder`를 사용하여 로그를 JSON 포맷으로 변환하도록 설정합니다.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <property name="LOG_FILE" value="logs/app.log"/>

    <!-- 콘솔 앱펜더: ECS JSON 포맷 -->
    <appender name="ECS_CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder class="co.elastic.logging.logback.EcsEncoder">
            <serviceName>my-app-service</serviceName>
            <eventDataset>application.log</eventDataset>
            <includeMarkers>true</includeMarkers>
            <stackTraceAsArray>true</stackTraceAsArray>
        </encoder>
    </appender>

    <!-- 파일 앱펜더: ECS JSON 포맷 (Rolling 방식) -->
    <appender name="ECS_FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>${LOG_FILE}.json</file>
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <fileNamePattern>${LOG_FILE}.%d{yyyy-MM-dd}.json.gz</fileNamePattern>
            <maxHistory>30</maxHistory>
        </rollingPolicy>
        <encoder class="co.elastic.logging.logback.EcsEncoder">
            <serviceName>my-app-service</serviceName>
        </encoder>
    </appender>

    <root level="info">
        <appender-ref ref="ECS_CONSOLE" />
        <appender-ref ref="ECS_FILE" />
    </root>
</configuration>
```

---

## 3. 주요 설정 파라미터

* **`serviceName`**: 로그를 생성하는 서비스의 이름입니다. Elastic 검색 시 필터링 용도로 사용됩니다.
* **`stackTraceAsArray`**: Stack Trace를 문자열이 아닌 JSON 배열 형태로 저장하여 가독성을 높입니다.
* **`includeMarkers`**: SLF4J Marker를 로그 필드에 포함할지 여부를 결정합니다.
* **`additionalField`**: 고정된 커스텀 필드를 추가할 때 사용합니다. (예: `environment=prod`)

---

## 4. Spring Boot 3.4 네이티브 방식 vs XML 방식

| 구분 | SB 3.4 네이티브 (`ecs`) | logback-ecs-encoder (XML) |
| :--- | :--- | :--- |
| **추가 의존성** | 없음 (내장) | **필요** (`logback-ecs-encoder`) |
| **설정 위치** | `application.yml` | `logback-spring.xml` |
| **장점** | 설정이 매우 간결함 | 세밀한 커스터마이징, 복수 앱펜더 구성 가능 |
| **권장 환경** | 표준적인 ECS 로깅 | 로깅 전략이 복잡한 대규모 서비스 |

---

## 5. SLF4J 2.0 `addKeyValue()` 사용 시 주의점과 대안

Spring Boot 3.x(SLF4J 2.0+)에서 제공하는 Fluent Logging API(`log.atInfo().addKeyValue("order_id", 123).log()`)를 사용할 때, `logback-ecs-encoder`(v1.5~1.6 기준)는 `addKeyValue`로 넣은 키-값 쌍을 자동으로 JSON 루트 필드로 추출하지 못하는 제약이 있다. 이를 해결하려면 다음 두 가지 방법 중 하나를 선택한다.

### 방법 1: `MDC.putCloseable()` 사용 (`logback-ecs-encoder` 유지 시)
`EcsEncoder`는 MDC(Mapped Diagnostic Context)를 기본 지원하므로 `<includeMdc>true</includeMdc>`를 켜고 `MDC.putCloseable`로 컨텍스트를 주입한다.

```java
try (var ignored = org.slf4j.MDC.putCloseable("order_id", "12345")) {
    log.info("주문 처리를 시작합니다.");
}
```

### 방법 2: `logstash-logback-encoder`로 전환 (`addKeyValue` 네이티브 지원)
SLF4J 2.0의 `addKeyValue()`와 `StructuredArguments`를 코드 변경 없이 JSON 필드에 자동 반영하려면 [Logstash Logback Encoder](Logstash_Logback_Encoder_Guide.md)(`net.logstash.logback:logstash-logback-encoder`) 또는 [Composite JSON Encoder](Logback_JSON_Composite_Encoder.md)를 사용하는 편이 유리하다.

---

## 6. 결론

Spring Boot 3.4 이상의 단순한 환경이라면 YAML 설정을 권장하지만, 로그를 파일과 콘솔에 동시에 다른 포맷으로 출력하거나 특정 패키지만 별도의 ECS 속성을 부여해야 한다면 **`logback-ecs-encoder`**를 통한 XML 설정을 사용한다.
