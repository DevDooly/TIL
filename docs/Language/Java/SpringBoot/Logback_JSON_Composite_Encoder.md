# Logback: LoggingEventCompositeJsonEncoder와 springProperty 활용 가이드

Spring Boot 환경에서 로그를 JSON 파일로 저장할 때, `application.yml`의 설정값을 포함하여 JSON 구조를 커스터마이징하는 방법을 설명합니다.

---

## 1. 의존성 추가 (Gradle)
JSON 인코딩을 위해 `logstash-logback-encoder`가 필요합니다.

```gradle
dependencies {
    implementation 'net.logstash.logback:logstash-logback-encoder:7.4'
}
```

---

## 2. logback-spring.xml 설정 예시

`LoggingEventCompositeJsonEncoder`를 사용하여 표준 필드와 `springProperty`로 가져온 커스텀 필드를 조합합니다.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <!-- application.yml에서 설정값 가져오기 -->
    <springProperty scope="context" name="APP_NAME" source="spring.application.name" defaultValue="unknown-app"/>
    <springProperty scope="context" name="ENV" source="spring.profiles.active" defaultValue="local"/>

    <!-- 파일 앱인더 설정 -->
    <appender name="JSON_FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>logs/app-json.log</file>
        <rollingPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedRollingPolicy">
            <fileNamePattern>logs/archive/app-json.%d{yyyy-MM-dd}.%i.log.gz</fileNamePattern>
            <maxFileSize>10MB</maxFileSize>
            <maxHistory>7</maxHistory>
        </rollingPolicy>

        <!-- Composite Json Encoder 설정 -->
        <encoder class="net.logstash.logback.encoder.LoggingEventCompositeJsonEncoder">
            <providers>
                <timestamp>
                    <timeZone>UTC</timeZone>
                </timestamp>
                <pattern>
                    <pattern>
                        {
                          "level": "%level",
                          "app_name": "${APP_NAME}",
                          "env": "${ENV}",
                          "thread": "%thread",
                          "class": "%logger{40}",
                          "message": "%message",
                          "stack_trace": "%exception"
                        }
                    </pattern>
                </pattern>
                <stackTrace/> <!-- 예외 발생 시 상세 스택트레이스 포함 -->
            </providers>
        </encoder>
    </appender>

    <root level="INFO">
        <appender-ref ref="JSON_FILE" />
    </root>
</configuration>
```

---

## 3. 주요 설정 설명

### 3.1 `<springProperty>`

* `source`: `application.yml`의 경로를 지정합니다.
* `name`: Logback 설정 내에서 사용할 변수명을 지정합니다. (예: `${APP_NAME}`)
* **주의**: 파일명이 `logback.xml`이 아닌 **`logback-spring.xml`**이어야 Spring의 설정을 정상적으로 읽어올 수 있습니다.

### 3.2 `<providers>` 섹션
`LoggingEventCompositeJsonEncoder`는 여러 `Provider`를 합쳐서 하나의 JSON 객체를 만듭니다.

* `<timestamp>`: 로그 발생 시간을 추가합니다.
* `<pattern>`: **가장 중요한 부분**입니다. 여기서 자유로운 JSON 구조를 정의할 수 있으며, Logback의 표준 패턴 문자열(`%level`, `%message`)과 앞서 정의한 `${변수}`를 섞어서 사용할 수 있습니다.
* `<stackTrace>`: 에러 로그 시 예외 객체를 JSON 필드로 분리해서 깔끔하게 보여줍니다.

---

## 4. 왜 이 클래스가 좋은가요?

단순한 `LogstashEncoder`보다 `LoggingEventCompositeJsonEncoder`가 유리한 점은 다음과 같습니다.

1. **필드명 제어**: 기본 필드명(`level`, `message` 등)을 인프라 표준(ECS 등)에 맞춰 자유롭게 바꿀 수 있습니다.
2. **구조의 유연성**: 중첩된(Nested) JSON 구조도 `<pattern>` 내부에서 정의하여 내보낼 수 있습니다.
3. **필터링**: 특정 조건에서만 특정 필드가 나타나도록 정교하게 제어할 수 있는 확장성을 제공합니다.

---

## 5. 요약

* `application.yml`의 값을 가져올 때는 `<springProperty>`를 사용하세요.
* JSON 구조를 직접 설계하고 싶다면 `LoggingEventCompositeJsonEncoder` 내부의 `<pattern>` 프로바이더를 활용하세요.
* 설정 파일은 반드시 `logback-spring.xml`로 명명하세요.
