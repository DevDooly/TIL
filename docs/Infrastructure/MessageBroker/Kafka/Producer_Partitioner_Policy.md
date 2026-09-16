# Kafka Producer: 파티셔너 정책과 설정

Kafka producer의 파티셔닝 정책은 키의 처리 순서와 배치 효율을 함께 고려해 선택한다. 아래 예제는 Java client 3.9.2 / 4.0 계열을 기준으로 하며, 실행하려면 Kafka client 의존성과 접속 가능한 브로커가 필요하다.

## 기본 정책

명시적 partition이 있는 레코드는 그 파티션을 사용한다. 기본 내장 정책은 보통 키가 있으면 직렬화한 키의 해시를, null key에는 배치 효율을 고려한 분산을 사용한다. `partitioner.ignore.keys=true`는 기본 정책에서 키를 무시하는 설정이며 커스텀 파티셔너에 자동 적용되지 않는다. [Producer 설정](https://kafka.apache.org/39/configuration/producer-configs/)

기본 정책은 `partitioner.class`를 생략하면 사용된다. 예전 설정에 `org.apache.kafka.clients.producer.internals.DefaultPartitioner`가 들어 있다면 제거한다. 이 클래스는 Kafka 4.0에서 삭제되었다. [업그레이드 안내](https://kafka.apache.org/40/getting-started/upgrade/)

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

RoundRobin은 키의 해시로 파티션을 고르지 않는다. 같은 키의 레코드를 한 파티션에 모아 순서대로 처리해야 한다면 이 정책은 맞지 않을 수 있다. [중복 호출 버그와 수정 버전](Producer_Partitioner_Issue.md), [분포 측정 기준](Partitioner_Evolution_and_Imbalance.md)을 확인한다.

## 커스텀 정책을 만들기 전에

- 동일 키의 순서 범위와 파티션 증설 시 재배치 정책을 정의한다.
- 반환하는 파티션이 실제로 존재하는지 확인한다. 모든 레코드를 0번에 보내는 예제는 분산 동작을 확인하는 데 쓸 수 없다.
- 인스턴스별 상태, 동시 호출, 카운터 overflow를 검토한다.
- 패치 전 [abortOnNewBatch 호출 흐름](AbortOnNewBatch_Issue.md)을 확인한다.

Kafka가 제공하는 순서는 파티션 단위다. 여러 producer에서 보내는 이벤트의 업무상 선후 관계는 애플리케이션에서도 다뤄야 한다. 재시도와 idempotence 설정이 전송 순서에 미치는 영향도 확인한다.
