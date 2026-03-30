# Kafka Producer: 파티셔너(Partitioner) 정책 및 설정

Kafka Producer가 메시지를 발행할 때, 토픽의 여러 파티션 중 어느 곳으로 보낼지 결정하는 컴포넌트가 바로 **파티셔너(Partitioner)**입니다.

---

## 1. 파티셔너 정책의 진화

### 1.1 Kafka 2.4 이전 (Old Default)
*   **Key가 있는 경우**: Key의 해시값을 기반으로 특정 파티션에 고정적으로 할당.
*   **Key가 없는 경우**: **라운드 로빈(Round-Robin)** 방식으로 메시지를 하나씩 번갈아가며 파티션에 할당.
*   **문제점**: 메시지 하나당 하나의 배치가 생성되는 경우가 많아 네트워크 오버헤드가 크고 전송 효율이 낮았습니다.

### 1.2 Kafka 2.4 이후 (Sticky Partitioning 도입)
*   **버전**: **Kafka 2.4.0 (KIP-480)**부터 기본 파티셔너 정책으로 채택되었습니다.
*   **동작 방식**: Key가 없는 메시지의 경우, 하나의 파티션을 선택해 해당 파티션의 배치가 찰 때까지(또는 `linger.ms` 도달 시까지) **한 파티션에 몰아넣습니다.** 배치가 전송된 후에는 다음 파티션으로 이동하여 다시 '스티키'하게 동작합니다.
*   **장점**: 배치 처리 효율이 극대화되어 지연 시간(Latency)이 감소하고 처리량(Throughput)이 대폭 향상됩니다.

---

## 2. Java 설정 예제

Producer 설정 시 `partitioner.class` 속성을 통해 원하는 정책을 선택할 수 있습니다.

### 2.1 DefaultPartitioner 설정 (기본값)
기본값이므로 별도로 설정하지 않아도 되지만, 명시적으로 적으려면 다음과 같이 합니다. (2.4 이상에서는 Sticky로 동작)

```java
Properties props = new Properties();
props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
// 명시적 설정 시
props.put(ProducerConfig.PARTITIONER_CLASS_CONFIG, "org.apache.kafka.clients.producer.internals.DefaultPartitioner");

KafkaProducer<String, String> producer = new KafkaProducer<>(props);
```

### 2.2 RoundRobinPartitioner 설정
메시지를 파티션별로 정확히 하나씩 순차적으로 분배하고 싶을 때 사용합니다. (배치 효율은 낮아질 수 있음에 주의)

```java
Properties props = new Properties();
props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
// RoundRobin 설정
props.put(ProducerConfig.PARTITIONER_CLASS_CONFIG, "org.apache.kafka.clients.producer.RoundRobinPartitioner");

KafkaProducer<String, String> producer = new KafkaProducer<>(props);
```

---

## 3. 커스텀 파티셔너 (Custom Partitioner)

특정한 비즈니스 로직(예: VIP 고객의 데이터는 특정 파티션으로 우선 배정)이 필요한 경우 직접 구현할 수 있습니다.

### 3.1 Partitioner 인터페이스 구현
```java
public class MyCustomPartitioner implements Partitioner {
    @Override
    public int partition(String topic, Object key, byte[] keyBytes, Object value, byte[] valueBytes, Cluster cluster) {
        // 원하는 로직 구현
        return 0; // 특정 파티션 번호 반환
    }

    @Override
    public void close() {}

    @Override
    public void configure(Map<String, ?> configs) {}
}
```

### 3.2 Producer 설정 반영
```java
props.put(ProducerConfig.PARTITIONER_CLASS_CONFIG, "com.example.MyCustomPartitioner");
```

---

## 4. 요약 및 권장 사항

1.  **기본 전략 유지**: 대부분의 경우 Kafka 2.4+ 버전의 기본 `DefaultPartitioner`(Sticky)가 가장 성능이 좋습니다.
2.  **RoundRobin 주의**: 파티션 간 부하 균등 분배가 절대적으로 중요하다면 사용할 수 있으나, 배치 전송 효율 저하와 이전 섹션에서 다룬 **KAFKA-9965** 이슈(불균형 버그)를 고려해야 합니다.
3.  **Key 활용**: 데이터의 순서 보장이 필요하다면 적절한 Key를 부여하여 해시 기반의 파티셔닝을 활용하세요.
