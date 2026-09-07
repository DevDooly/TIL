# Kafka Producer: 파티셔너 정책과 설정

기준: Java client 3.9.2 / 4.0 계열, 2026-09-07. Kafka client 의존성과 접근 가능한 브로커가 필요하다.

## 기본 정책

명시적 partition이 있는 레코드는 그 파티션을 사용한다. 기본 내장 정책은 보통 키가 있으면 직렬화한 키의 해시를, null key에는 배치 효율을 고려한 분산을 사용한다. `partitioner.ignore.keys=true`는 기본 정책에서 키를 무시하는 설정이며 커스텀 파티셔너에 자동 적용되지 않는다. [Producer 설정](https://kafka.apache.org/39/configuration/producer-configs/)

`partitioner.class`를 생략한다. Kafka 4.0에서 제거된 `org.apache.kafka.clients.producer.internals.DefaultPartitioner`를 명시하지 않는다. [업그레이드 안내](https://kafka.apache.org/40/getting-started/upgrade/)

```java
import java.util.Properties;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;

public final class ProducerExample {
    public static void main(String[] args) throws Exception {
        Properties props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);

        try (KafkaProducer<String, String> producer = new KafkaProducer<>(props)) {
            // 단일 전송 확인용. 처리량 측정에서는 비동기 callback으로 집계한다.
            var metadata = producer.send(
                    new ProducerRecord<>("events", "device-001", "sample")).get();
            System.out.println(metadata.partition());
        }
    }
}
```

## RoundRobin 선택

producer 생성 전에 아래 설정을 추가한다.

```java
props.put(ProducerConfig.PARTITIONER_CLASS_CONFIG,
        "org.apache.kafka.clients.producer.RoundRobinPartitioner");
```

RoundRobin은 키 해시 기반 배정을 제공하지 않으므로 동일 키를 같은 파티션에 모아야 하는 요구와 충돌할 수 있다. [중복 호출 버그와 수정 버전](Producer_Partitioner_Issue.md), [분포 측정 기준](Partitioner_Evolution_and_Imbalance.md)을 확인한다.

## 커스텀 정책을 만들기 전에

- 동일 키의 순서 범위와 파티션 증설 시 재배치 정책을 정의한다.
- 없는 파티션을 반환하거나 모든 레코드를 0번에 고정하는 예제를 운영 코드로 사용하지 않는다.
- 인스턴스별 상태, 동시 호출, 카운터 overflow를 검토한다.
- 패치 전 [abortOnNewBatch 호출 흐름](AbortOnNewBatch_Issue.md)을 확인한다.

순서는 파티션 단위이며 여러 producer 사이의 업무상 선후 관계까지 자동 보장하지 않는다. 재시도와 idempotence 설정도 함께 검토한다.
