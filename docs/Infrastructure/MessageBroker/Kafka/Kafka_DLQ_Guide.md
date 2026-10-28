# Kafka DLQ(Dead Letter Queue) 개념, 메시지 확인 및 구현 가이드

Kafka에서 컨슈머가 특정 메시지를 처리하다가 반복해서 실패할 때, 해당 메시지 때문에 파티션 전체의 오프셋 진행이 멈추는 현상을 막기 위해 실패한 레코드를 별도 토픽으로 격리하는 패턴을 **DLQ(Dead Letter Queue)** 또는 **DLT(Dead Letter Topic)**라고 부른다.

RabbitMQ나 AWS SQS와 달리 **Kafka 브로커 자체에는 내장된 DLQ 기능이 없다.** 대신 컨슈머 애플리케이션(Spring Kafka, Kafka Connect, Kafka Streams 등)이 재시도 횟수를 초과한 레코드를 `<원본토픽>.DLT`(또는 `<원본토픽>-dlt`, `<원본토픽>.dlq`)라는 일반 Kafka 토픽에 프로듀싱한 뒤 원본 토픽의 오프셋을 커밋하는 방식으로 동작한다.

## 1. 왜 DLQ가 필요한가: Poison Pill과 파티션 블로킹

Kafka 컨슈머는 파티션 단위로 오프셋을 순서대로 읽는다. 만약 잘못된 JSON 포맷이나 스키마 불일치처럼 **아무리 재시도해도 성공할 수 없는 메시지(Poison Pill)**가 들어왔을 때 예외를 그대로 던지기만 하면 다음 문제가 발생한다.

1. 컨슈머가 같은 오프셋을 무한히 다시 읽으며 실패를 반복한다.
2. 해당 파티션의 뒤쪽 정상 메시지들이 전혀 처리되지 못해 **Consumer Lag이 급증**한다.
3. 재시도 시간이 `max.poll.interval.ms`를 넘기면 컨슈머 그룹 리밸런싱(Rebalancing)까지 반복적으로 일어난다.

따라서 오류 유형에 따라 재시도 여부와 DLQ 이동을 분리해야 한다.

| 오류 유형 | 예시 | 권장 처리 방식 |
| :--- | :--- | :--- |
| **일시적 오류 (Transient Error)** | 외부 API 일시 타임아웃, DB 커넥션 일시 고갈, 네트워크 순단 | 백오프(Backoff) 간격을 두고 2~3회 재시도한 뒤에도 실패하면 DLQ로 이동 |
| **영구적 오류 (Non-retryable / Poison Pill)** | JSON/Avro 역직렬화 실패(`DeserializationException`), 필수 필드 누락(`NullPointerException`, `IllegalArgumentException`) | 재시도해도 결과가 같으므로 **재시도 없이 즉시 DLQ로 이동** |

---

## 2. DLQ 메시지 및 실패 원인 확인 방법 (CLI 점검)

장애 알람이 발생했거나 DLQ 토픽에 메시지가 들어왔는지 확인할 때는 토픽의 오프셋 증가량과 레코드 헤더(Header)에 기록된 예외 정보를 함께 본다.

### 2.1 DLQ 토픽 존재 여부 및 적재 건수 확인

먼저 클러스터에 생성된 DLT/DLQ 토픽 이름을 찾고, `kafka-get-offsets.sh`(Kafka 3.0 이상)로 파티션별 마지막 오프셋을 조회해 메시지가 몇 건 쌓였는지 확인한다.

```bash
# 1. DLT 또는 DLQ 토픽 목록 조회
kafka-topics.sh --bootstrap-server localhost:9092 --list | grep -iE 'dlt|dlq'

# 2. 특정 DLQ 토픽의 파티션별 최신 오프셋(적재 건수) 확인
kafka-get-offsets.sh \
  --bootstrap-server localhost:9092 \
  --topic orders.DLT \
  --time -1
```

```text
orders.DLT:0:3
orders.DLT:1:0
orders.DLT:2:1
```

위 출력에서 `orders.DLT:0:3`은 0번 파티션에 3건(오프셋 0, 1, 2)이 적재되어 있음을 뜻한다(보존 기간 만료로 삭제된 세그먼트가 없는 경우).

### 2.2 DLQ 메시지 본문과 실패 원인 헤더 출력

Spring Kafka나 Kafka Connect는 메시지를 DLQ로 보낼 때 **왜 실패했는지, 원래 어느 토픽·파티션·오프셋에서 왔는지를 Kafka Record Header에 담는다.** 따라서 `kafka-console-consumer.sh`를 실행할 때 반드시 `print.headers=true` 옵션을 넣어야 원인을 파악할 수 있다.

```bash
kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic orders.DLT \
  --from-beginning \
  --max-messages 5 \
  --property print.timestamp=true \
  --property print.key=true \
  --property print.headers=true \
  --property print.value=true
```

### 2.3 Spring Kafka DLT 헤더 구조 해석

Spring Kafka의 `DeadLetterPublishingRecoverer`가 추가하는 주요 헤더는 다음과 같다.

| 헤더 키 (Header Key) | 값 타입 | 설명 |
| :--- | :--- | :--- |
| `kafka_dlt-original-topic` | UTF-8 String | 실패가 발생한 원본 토픽 이름 (예: `orders`) |
| `kafka_dlt-original-partition` | 4-byte Binary (`int`) | 원본 파티션 번호 (콘솔에서는 이진 바이트로 보일 수 있음) |
| `kafka_dlt-original-offset` | 8-byte Binary (`long`) | 원본 오프셋 번호 |
| `kafka_dlt-original-timestamp` | 8-byte Binary (`long`) | 원본 메시지의 타임스탬프 |
| `kafka_dlt-exception-fqcn` | UTF-8 String | 발생한 예외의 전체 클래스명 |
| `kafka_dlt-exception-message` | UTF-8 String | 예외 메시지 (`Exception.getMessage()`) |
| `kafka_dlt-exception-stacktrace` | UTF-8 String | 실패 지점의 전체 스택트레이스 |

Kafka Connect의 경우 설정(`errors.deadletterqueue.context.headers.enable=true`)을 켜면 `__connect.errors.topic`, `__connect.errors.exception.class.name`, `__connect.errors.exception.message` 헤더가 붙는다.

---

## 3. Spring Kafka에서 DLQ를 구현하는 2가지 방식

Spring Kafka 3.x 환경에서는 요구사항에 따라 **동기 블로킹 방식(`DefaultErrorHandler`)**과 **비동기 재시도 토픽 방식(`@RetryableTopic`)** 중 하나를 선택한다.

| 비교 항목 | `DefaultErrorHandler` + `DeadLetterPublishingRecoverer` | `@RetryableTopic` (Non-blocking Retry) |
| :--- | :--- | :--- |
| **재시도 중 파티션 블로킹** | 재시도 백오프 동안 해당 파티션의 다음 메시지 소비가 대기함 | 실패 메시지를 별도 `*-retry-*` 토픽으로 보내고 원본 파티션은 즉시 다음 메시지 처리 |
| **메시지 순서 보장** | 재시도 성공 시 같은 파티션 내 순서 유지 가능 | 실패 메시지가 뒤로 밀리므로 원본 순서가 바뀔 수 있음 |
| **필요한 토픽 수** | 원본 토픽 + `<원본>.DLT` (총 2개) | 원본 토픽 + 단계별 `retry` 토픽 N개 + `dlt` 토픽 |
| **적합한 상황** | 짧은 백오프(1~3초) 내 재시도로 충분하거나 순서가 중요한 경우 | 외부 API 장애 등으로 수십 초~수 분 단위의 긴 지연 재시도가 필요한 경우 |

### 3.1 방식 1: `DefaultErrorHandler`와 `DeadLetterPublishingRecoverer` 설정

기본 규칙으로 원본 토픽 이름 뒤에 `.DLT`를 붙인 토픽으로 실패 레코드를 전송하며, 역직렬화 예외나 잘못된 인자 예외는 재시도하지 않고 즉시 DLT로 보낸다.

```java
// Spring Boot 3.x / Spring Kafka 3.x 설정 예시 (발췌)
import org.apache.kafka.common.TopicPartition;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.core.KafkaOperations;
import org.springframework.kafka.listener.CommonErrorHandler;
import org.springframework.kafka.listener.DeadLetterPublishingRecoverer;
import org.springframework.kafka.listener.DefaultErrorHandler;
import org.springframework.kafka.support.serializer.DeserializationException;
import org.springframework.util.backoff.FixedBackOff;

@Configuration
public class KafkaErrorHandlerConfig {

    @Bean
    public CommonErrorHandler kafkaErrorHandler(KafkaOperations<Object, Object> kafkaTemplate) {
        // 기본 목적지: <원본토픽>.DLT, 동일한 파티션 번호(record.partition())로 전송
        DeadLetterPublishingRecoverer recoverer = new DeadLetterPublishingRecoverer(
                kafkaTemplate,
                (record, ex) -> new TopicPartition(record.topic() + ".DLT", record.partition())
        );

        // 1초 간격으로 최대 3회 재시도(최초 1회 + 재시도 3회 = 총 4회 시도) 후 recoverer 실행
        DefaultErrorHandler errorHandler = new DefaultErrorHandler(
                recoverer,
                new FixedBackOff(1000L, 3L)
        );

        // 영구적 오류는 재시도 없이 즉시 DLT로 이동
        errorHandler.addNotRetryableExceptions(
                DeserializationException.class,
                IllegalArgumentException.class
        );

        return errorHandler;
    }
}
```

#### 역직렬화 실패(Poison Pill) 처리를 위한 필수 설정

컨슈머가 메시지를 읽을 때 `JsonDeserializer`에서 역직렬화 예외가 발생하면 `@KafkaListener` 메서드에 진입하기도 전에 `poll()` 단계에서 예외가 터진다. 이를 `DefaultErrorHandler`가 잡아서 DLT로 보내려면 반드시 **`ErrorHandlingDeserializer`로 실제 Deserializer를 감싸야 한다.**

```yaml
spring:
  kafka:
    consumer:
      key-deserializer: org.springframework.kafka.support.serializer.ErrorHandlingDeserializer
      value-deserializer: org.springframework.kafka.support.serializer.ErrorHandlingDeserializer
      properties:
        spring.deserializer.key.delegate.class: org.apache.kafka.common.serialization.StringDeserializer
        spring.deserializer.value.delegate.class: org.springframework.kafka.support.serializer.JsonDeserializer
        spring.json.trusted.packages: "com.example.order.*"
```

### 3.2 방식 2: `@RetryableTopic`과 `@DltHandler`

어노테이션만으로 비동기 재시도 토픽 체인과 DLT 후처리를 구성할 수 있다.

```java
// Spring Kafka @RetryableTopic 예시 (발췌)
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.kafka.annotation.DltHandler;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.annotation.RetryableTopic;
import org.springframework.kafka.retrytopic.DltStrategy;
import org.springframework.kafka.support.KafkaHeaders;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.retry.annotation.Backoff;
import org.springframework.stereotype.Component;

@Component
public class OrderEventConsumer {

    private static final Logger log = LoggerFactory.getLogger(OrderEventConsumer.class);

    @RetryableTopic(
            attempts = "3",
            backoff = @Backoff(delay = 2000, multiplier = 2.0),
            exclude = {IllegalArgumentException.class},
            dltStrategy = DltStrategy.FAIL_ON_ERROR
    )
    @KafkaListener(topics = "orders", groupId = "order-service-group")
    public void consumeOrder(String payload) {
        if (payload.contains("\"amount\":-1")) {
            throw new IllegalArgumentException("결제 금액은 음수일 수 없습니다.");
        }
        // 주문 처리 로직 수행
    }

    @DltHandler
    public void handleDlt(
            ConsumerRecord<String, String> record,
            @Header(name = KafkaHeaders.DLT_EXCEPTION_MESSAGE, required = false) String errorMessage
    ) {
        log.error("DLT 적재 확인 - key={}, offset={}, 사유={}, payload={}",
                record.key(), record.offset(), errorMessage, record.value());
        // 슬랙 알람 전송 또는 장애 테이블 저장
    }
}
```

---

## 4. 운영 및 재처리(Replay) 시 주의할 점

1. **원본 토픽과 DLT 토픽의 파티션 수 일치**
   - `DeadLetterPublishingRecoverer`의 기본 목적지 리졸버는 원본 레코드의 파티션 번호(`record.partition()`)를 그대로 사용해 DLT에 보낸다.
   - 만약 원본 `orders` 토픽은 파티션이 6개인데 `orders.DLT` 토픽이 브로커 기본값(예: 파티션 1개)으로 자동 생성되었다면, 1~5번 파티션에서 실패한 메시지를 DLT로 보낼 때 존재하지 않는 파티션을 찾다가 `TimeoutException`이 발생한다.
   - 따라서 DLT 토픽의 파티션 수를 원본과 같게 생성하거나, 파티션을 고정하지 않으려면 `new TopicPartition(record.topic() + ".DLT", -1)`(또는 `null`)을 반환하도록 설정한다.
2. **재처리(Replay) 시 무한 루프 방지**
   - 버그를 수정한 뒤 DLT의 메시지를 원본 토픽으로 다시 밀어 넣을 때, 여전히 깨진 데이터가 섞여 있으면 `원본 → DLT → 원본` 무한 루프가 돌 수 있다.
   - 재발행 시 커스텀 헤더(예: `x-replay-count`)를 증가시키고 일정 횟수를 초과하면 자동 재발행을 멈추고 폐기·수동 검토하도록 설계한다.
3. **DLQ 토픽 보존 기간(Retention)과 모니터링**
   - 주말이나 연휴 동안 발생한 장애 메시지가 유실되지 않도록 DLQ 토픽의 `retention.ms`는 일반 이벤트 토픽보다 길게(예: 14일~30일) 잡는다.
   - DLQ 토픽의 `BytesInPerSec` 또는 오프셋 증가량이 0보다 커지면 즉시 알람이 발생하도록 모니터링을 연결해야 한다.

## 관련 문서 및 참고 자료

- 내부 문서
  - [Kafka Consumer: 특정 Offset 재소비 (Seek API)](Consumer_Offset_Control.md)
  - [Kafka 파티션 전략 및 산정](Partition_Strategy.md)
  - [Spring Kafka 테스트 예제](Spring_Kafka_Test.md)
- 외부 공식 자료
  - [Spring for Apache Kafka 공식 문서 - Sending Failed Records to Dead-Letter Topics](https://docs.spring.io/spring-kafka/reference/kafka/annotation-error-handling.html#dead-letters)
  - [Spring for Apache Kafka 공식 문서 - Non-Blocking Retries (`@RetryableTopic`)](https://docs.spring.io/spring-kafka/reference/retrytopic.html)
  - [Apache Kafka 공식 문서 - Connect Error Reporting and Dead Letter Queue](https://kafka.apache.org/documentation/#connect_errorreporting)
