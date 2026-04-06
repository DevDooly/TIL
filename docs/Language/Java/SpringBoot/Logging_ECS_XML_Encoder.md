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

## 5. 결론

Spring Boot 3.4 이상의 단순한 환경이라면 YAML 설정을 권장하지만, 로그를 파일과 콘솔에 동시에 다른 포맷으로 출력하거나 특정 패키지만 별도의 ECS 속성을 부여해야 한다면 **`logback-ecs-encoder`**를 통한 XML 설정이 가장 강력한 대안입니다.
