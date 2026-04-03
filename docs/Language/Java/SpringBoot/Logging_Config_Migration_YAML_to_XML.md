# Spring Boot: 로깅 설정 YAML에서 XML로의 전환 (SDK 충돌 해결)

Spring Boot 애플리케이션에서 `application.yml`을 통해 로깅을 관리하던 중, 외부 SDK가 자체적인 `logback.xml`을 포함하고 있어 설정이 무시되거나 충돌하는 문제를 해결하기 위해 설정을 XML로 이관한 사례를 정리합니다.

---

## 1. 이슈 배경: "왜 내 로그 설정이 적용되지 않는가?"

**상황**:
*   `application.yml`에 로깅 레벨 및 패턴을 설정하여 사용 중.
*   특정 외부 SDK(라이브러리)를 도입했는데, 해당 Jar 파일 내부에 `logback.xml`이 포함되어 있음.

**문제 현상**:
*   Logback은 클래스패스에서 `logback.xml`을 발견하면 Spring Boot의 `application.yml` 설정을 무시하고 해당 XML을 우선적으로 로드합니다.
*   이 과정에서 로컬 설정과 SDK 설정이 충돌하여 에러가 발생하거나, 개발자가 의도한 로그 레벨이 적용되지 않는 현상이 발생합니다.

---

## 2. 원인 분석: Logback의 초기화 순서

Logback 라이브러리는 다음 순서로 설정 파일을 찾습니다.
1.  `logback-test.xml`
2.  **`logback.xml`** (외부 SDK에 포함된 경우 여기서 먼저 로딩됨)
3.  **Spring Boot의 내부 처리** (여기서 `application.yml` 설정을 반영하려 하지만 이미 2번에서 결정된 경우 무시됨)

**해결책**:
Spring Boot 전용 설정 파일명인 **`logback-spring.xml`**을 사용하면, Spring Boot가 로그 시스템을 완전히 제어할 수 있게 되며 XML 내부에서 Spring Profile 기능을 사용할 수 있는 이점도 얻을 수 있습니다.

---

## 3. 설정 전환 예시 (Migration)

### 3.1 기존 YAML 설정 (`application.yml`)
```yaml
logging:
  level:
    root: info
    com.myapp: debug
  pattern:
    console: "%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n"
```

### 3.2 전환된 XML 설정 (`logback-spring.xml`)
`src/main/resources/logback-spring.xml` 파일을 생성하여 다음과 같이 작성합니다.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <!-- 콘솔 앱펜더 정의 -->
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>

    <!-- 기본 로그 레벨 -->
    <root level="info">
        <appender-ref ref="CONSOLE" />
    </root>

    <!-- 특정 패키지 로그 레벨 (Spring Profile 활용 가능) -->
    <springProfile name="dev">
        <logger name="com.myapp" level="debug" additivity="false">
            <appender-ref ref="CONSOLE" />
        </logger>
    </springProfile>
</configuration>
```

---

## 4. 해결 결과 및 장점

1.  **충돌 해소**: `logback-spring.xml`을 사용함으로써 외부 SDK의 `logback.xml` 보다 Spring Boot가 제공하는 설정이 우선권을 갖게 되어 충돌이 해결되었습니다.
2.  **세밀한 제어**: XML을 사용하면 Appender 분리, 로그 로테이션(RollingFileAppender) 등 YAML보다 훨씬 상세하고 복잡한 설정을 유연하게 작성할 수 있습니다.
3.  **프로파일 지원**: `<springProfile>` 태그를 통해 환경별로 다른 로깅 전략을 하나의 파일에서 관리할 수 있습니다.

---

## 5. 요약
외부 라이브러리와의 로깅 설정 충돌이 발생한다면, 고민하지 말고 **`application.yml`의 설정을 `logback-spring.xml`로 이관**하는 것이 가장 확실하고 표준적인 해결 방법입니다.
