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

### 3.2 <providers> 섹션
`LoggingEventCompositeJsonEncoder`는 여러 `Provider`를 합쳐서 하나의 JSON 객체를 만듭니다.

1. **`<timestamp>`**: 로그 발생 시간을 추가합니다.
2. **`<pattern>`**: **로그마다 내용이 바뀌는 동적 필드**를 정의할 때 사용합니다. Logback의 패턴 치환자(`%level`, `%message`)를 사용합니다.
3. **`<customFields>` 또는 `<globalCustomFields>`**: **모든 로그에 공통으로 들어가는 고정된 정적 필드**를 추가할 때 사용합니다. 사용하는 인코더 클래스에 따라 태그 이름이 다를 수 있습니다.
4. **`<stackTrace>`**: 예외 발생 시 상세 스택트레이스를 필드로 분리합니다.

---

## 4. customFields vs globalCustomFields (인코더별 차이)

라이브러리 내부적으로 정적 필드를 처리하는 방식은 인코더 타입에 따라 태그 이름이 달라지므로 주의해야 합니다.

| 인코더 클래스 | 태그 이름 | 특징 |
| :--- | :--- | :--- |
| **LogstashEncoder** | `<customFields>` | 인코더의 직접 속성으로 설정 |
| **LoggingEventCompositeJsonEncoder** | **`<globalCustomFields>`** | `providers` 내부의 하위 프로바이더로 설정 |

### 4.1 LoggingEventCompositeJsonEncoder에서의 설정 (추천)

복합 인코더를 쓸 때는 프로바이더 이름으로 `globalCustomFields`를 사용해야 합니다.



* **공식 레퍼런스**: [Logstash Logback Encoder Javadoc - GlobalCustomFieldsJsonProvider](https://javadoc.io/static/net.logstash.logback/logstash-logback-encoder/7.4/net/logstash/logback/composite/GlobalCustomFieldsJsonProvider.html)

* **동작 원리 (성능 이점)**: 

    * 해당 라이브러리의 소스 코드([GitHub](https://github.com/logstash/logstash-logback-encoder/blob/main/src/main/java/net/logstash/logback/composite/GlobalCustomFieldsJsonProvider.java))를 보면, XML에 설정된 JSON 문자열은 프로바이더가 시작되는 **`start()` 단계에서 단 한 번만 파싱**되어 메모리에 객체 형태로 저장됩니다.

    * 실제 로그가 기록되는 시점(`writeTo`)에는 이미 파싱된 객체를 출력 스트림에 쓰기만 하므로, 매 로그마다 JSON을 해석하는 오버헤드가 없어 정적 데이터 처리에 매우 최적화되어 있습니다.



```xml

<encoder class="net.logstash.logback.encoder.LoggingEventCompositeJsonEncoder">


    <providers>
        <globalCustomFields>
            <customFields>
                {
                  "service_id": "payment-api",
                  "version": "v1.2.0"
                }
            </customFields>
        </globalCustomFields>
        <pattern>
            <pattern>
                { "msg": "%message" }
            </pattern>
        </pattern>
    </providers>
</encoder>
```

* **구조적 특징**: `<globalCustomFields>` 태그 안에 다시 `<customFields>` 태그를 써서 JSON 문자열을 감싸는 구조입니다.

---

## 5. customFields vs pattern 상세 비교


| 구분 | customFields | pattern |
| :--- | :--- | :--- |
| **데이터 성격** | **정적 (Static)** | **동적 (Dynamic)** |
| **사용 방식** | 순수 JSON 형태 문자열 | Logback 패턴 치환자 (`%...`) 사용 |
| **주요 용도** | 서비스명, 버전, 호스트명, 리전 등 | 메시지, 레벨, 스레드명, 호출 클래스 등 |
| **성능** | 파싱 오버헤드가 거의 없음 | 매 로그마다 패턴을 해석해야 함 |

### 4.1 customFields 활용 예시
인프라 수준에서 부여되는 고정 정보들을 넣기에 최적입니다.

```xml
<encoder class="net.logstash.logback.encoder.LoggingEventCompositeJsonEncoder">
    <providers>
        <customFields>
            {
              "service_id": "payment-api",
              "version": "v1.2.0",
              "cloud_region": "ap-northeast-2"
            }
        </customFields>
        <pattern>
            <pattern>
                { "msg": "%message" }
            </pattern>
        </pattern>
    </providers>
</encoder>
```

### 4.2 pattern 활용 예시
로그 발생 시점의 컨텍스트 정보를 구조화할 때 사용합니다.

```xml
<pattern>
    <pattern>
        {
          "level": "%level",
          "trace_id": "%mdc{traceId:-none}",
          "logger": "%logger"
        }
    </pattern>
</pattern>
```

---

## 5. 어떤 상황에 무엇을 쓸까?

* **customFields를 써야 할 때**:
    * 배포 시점에 결정되는 정보 (서비스 이름, 버전, 서버 ID).
    * `springProperty`로 가져온 값을 단순히 모든 로그에 박아넣고 싶을 때.
    * **이유**: 설정 시점에 한 번만 해석되므로 성능상 유리합니다.

* **pattern을 써야 할 때**:
    * Logback 내부의 특수 기호(`%`)를 써서 값을 추출해야 할 때.
    * 로그마다 값이 변하는 필드 (시간, 레벨, 메시지, MDC 등).
    * JSON의 계층 구조(Nested)를 복잡하게 설계해야 할 때.

---

## 6. 요약

1. **설정값 연동**: `application.yml`의 값을 가져올 때는 `<springProperty>`를 사용하고, 반드시 파일명을 **`logback-spring.xml`**로 설정해야 합니다.
2. **구조 커스터마이징**: JSON 구조를 직접 설계하고 싶다면 유연성이 높은 **`LoggingEventCompositeJsonEncoder`**를 권장합니다.
3. **정적 데이터 처리**: 서비스명, 버전 등 고정된 값은 **`globalCustomFields`**를 사용하세요. 초기화 시점에 단 한 번만 파싱되어 캐싱되므로 성능상 가장 유리합니다.
4. **동적 데이터 처리**: 로그마다 변하는 레벨, 메시지, MDC 등은 **`pattern`** 프로바이더를 통해 정의하세요.
5. **성능 최적화**: JSON 생성 및 I/O 부하를 고려하여 실운영 환경에서는 `AsyncAppender`와 함께 사용하는 것이 좋습니다.
