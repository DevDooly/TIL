# SLF4J addKeyValue와 Elastic ECS Encoder 연동 가이드

Spring Boot 3+ 환경에서 SLF4J 2.0의 Fluent API(`addKeyValue`)를 사용하여 동적 키-값 쌍을 ECS JSON 로그에 포함하는 방법을 상세히 다룹니다.

---

## 1. 공식 레퍼런스 및 버전 요구사항

`includeSlf4jKeyValues` 옵션은 Elastic ECS Logging Java 라이브러리의 **v1.5.0** 버전부터 공식적으로 지원되기 시작했습니다.

* **공식 GitHub 릴리즈 노트**: [ecs-logging-java v1.5.0 Release](https://github.com/elastic/ecs-logging-java/releases/tag/v1.5.0)
    * *내용: "Added support for SLF4J 2.0 KeyValuePairs in Logback and Log4j2."*
* **공식 문서**: [Elastic ECS Logging Logback Guide](https://www.elastic.co/guide/en/ecs-logging/java/current/logback.html)

### 필수 요구사항
| 구성 요소 | 최소 권장 버전 | 비고 |
| :--- | :--- | :--- |
| **Spring Boot** | 3.0.0+ | SLF4J 2.0 기본 포함 |
| **logback-ecs-encoder** | **1.5.0+** | Key-Value 지원 시작 버전 |
| **SLF4J API** | 2.0.0+ | Fluent API (`atInfo()`) 지원 |

---

## 2. 상세 사용 방법

### 2.1 logback.xml 설정
`includeSlf4jKeyValues` 옵션은 기본값이 `true`인 경우가 많지만, 명시적으로 설정하는 것이 가장 안전합니다.

```xml
<encoder class="co.elastic.logging.logback.EcsEncoder">
    <serviceName>my-app</serviceName>
    <!-- SLF4J 2.0 KeyValuePairs 동적 추출 활성화 -->
    <includeSlf4jKeyValues>true</includeSlf4jKeyValues>
    <includeMdc>true</includeMdc>
</encoder>
```

### 2.2 코드 작성 (Fluent API)
```java
log.atInfo()
   .addKeyValue("user_id", "user123")
   .addKeyValue("action", "login")
   .log("사용자가 로그인했습니다.");
```

---

## 3. 만약 addKeyValue가 자동으로 등록되지 않는다면? (대안)

사용 중인 라이브러리 버전을 올릴 수 없거나, 특정 환경에서 자동 추출이 작동하지 않을 경우 다음과 같은 방법을 사용할 수 있습니다.

### 방법 1: MDC (Mapped Diagnostic Context) 사용
`addKeyValue`는 해당 로그 라인에서만 유효하지만, `MDC`는 전통적으로 ECS Encoder가 가장 잘 지원하는 방식입니다.

```java
try (MDC.MDCCloseable ignored = MDC.putCloseable("user_id", "user123")) {
    log.info("사용자가 로그인했습니다.");
}
```

* `EcsEncoder`의 `<includeMdc>true</includeMdc>` 설정이 필요합니다.

### 방법 2: StructuredArguments (Logstash 지원 방식과의 혼용)
만약 `logstash-logback-encoder` 라이브러리가 함께 있다면 `StructuredArguments`를 사용할 수도 있으나, 순수 ECS 환경에서는 권장되지 않습니다.

### 방법 3: 커스텀 필드 수동 추가
로그 호출 시점에 직접 ECS 필드 규격에 맞춰 데이터를 전달해야 할 경우, `EcsEncoder`를 확장하는 대신 로그 메시지 자체를 구조화하거나 MDC를 활용하는 것이 유지보수에 유리합니다.

---

## 4. 왜 내 로그에는 안 나올까? (체크리스트)

1. **의존성 충돌**: 프로젝트 내에 구버전 `slf4j-api`나 `logback-classic`이 섞여 있는지 확인하세요 (`./gradlew dependencies`).
2. **클래스패스**: `co.elastic.logging.logback.EcsEncoder` 클래스가 실제로 `includeSlf4jKeyValues` 세터를 가지고 있는지 IDE에서 확인하세요.
3. **로그 수집기 설정**: 애플리케이션 로그 자체(JSON)에는 키가 포함되어 있는데, Logstash나 Elasticsearch 인덱싱 과정에서 해당 필드가 매핑되지 않아 안 보일 수도 있습니다. (콘솔에 찍히는 생 JSON을 먼저 확인하세요.)

---

## 5. 요약
`logback-ecs-encoder:1.5.0` 이상을 사용하면 별도의 복잡한 구현 없이 **설정 한 줄(`includeSlf4jKeyValues`)**로 SLF4J 2.0의 최신 기능을 완벽하게 누릴 수 있습니다.
