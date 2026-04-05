# Spring Boot 3.4: 정형 로깅(Structured Logging) 및 ECS 연동

Spring Boot 3.4.x 버전부터는 별도의 외부 라이브러리(Logstash Logback Encoder 등) 없이도 **JSON 형태의 정형 로깅(Structured Logging)**을 네이티브하게 지원합니다. 이는 AWS ECS, Kubernetes 등 클라우드 네이티브 환경에서 로그 분석을 매우 간편하게 만들어 줍니다.

---

## 1. 정형 로깅(Structured Logging)이란?

기존의 로그는 사람이 읽기 좋은 **텍스트(Plain Text)** 형태였습니다. 하지만 클라우드 환경(CloudWatch, ELK 등)에서는 기계가 분석하기 좋은 **JSON 형태**의 데이터가 훨씬 유리합니다.

Spring Boot 3.4는 이를 위해 **ECS (Elastic Common Schema)**, **Logstash**, **GELF** 등 표준화된 형식을 기본 제공합니다.

---

## 2. 주요 설정 방법

`application.yml` 설정만으로 간단히 활성화할 수 있습니다.

### 2.1 콘솔에 ECS 포맷 적용
AWS ECS 환경에서 CloudWatch Logs로 로그를 보낼 때 가장 권장되는 방식입니다.
```yaml
spring:
  main:
    banner-mode: "off" # JSON 로그와 섞이지 않도록 배너 끔
logging:
  structured:
    format:
      console: "ecs" # ecs, logstash, gelf 중 선택 가능
```

### 2.2 상세 옵션 (Customizing)
로그에 추가적인 메타데이터(서비스명, 환경 등)를 포함할 수 있습니다.
```yaml
logging:
  structured:
    ecs:
      service:
        name: "my-payment-service"
        version: "1.0.0"
        node-name: "${HOSTNAME}"
```

---

## 3. AWS ECS에서의 이점

1. **멀티라인 로그 문제 해결**: 기존 텍스트 로그는 Stack Trace 발생 시 여러 줄로 나뉘어 CloudWatch에서 한 건의 로그로 인식되지 않는 문제가 있었습니다. JSON 포맷은 전체 Trace가 하나의 JSON 객체에 담기므로 관리가 매우 쉽습니다.
2. **비용 및 성능 최적화**: 로그 파싱 부하가 줄어들고, CloudWatch Logs Insights를 통해 `@message.level`, `@message.logger` 등의 필드로 즉시 쿼리가 가능해집니다.
3. **의존성 제거**: `logstash-logback-encoder` 같은 외부 라이브러리 의존성을 제거하여 보안 취약점 관리 및 빌드 속도 개선에 도움이 됩니다.

---

## 4. 기존 방식과의 비교

| 구분 | 기존 (SB 3.3 이하) | 신규 (SB 3.4+) |
| :--- | :--- | :--- |
| **설정 방식** | `logback-spring.xml` 직접 작성 필수 | `application.yml` 속성 설정만으로 가능 |
| **외부 라이브러리** | Logstash Encoder 등 추가 필요 | **기본 지원 (Native)** |
| **유연성** | XML 수정 시 빌드/배포 필요 | 환경 변수만으로 포맷 변경 가능 |

---

## 5. 결론

Spring Boot 3.4의 정형 로깅은 현대적인 인프라 운영에 필수적인 기능입니다. 특히 **AWS ECS**를 사용 중이라면 `logging.structured.format.console=ecs` 설정을 통해 로그 운영 공수를 획기적으로 줄일 수 있습니다.
