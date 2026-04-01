# Kafka Consumer: 특정 Offset 재소비 (Seek API)

Kafka Consumer는 기본적으로 마지막으로 커밋된 Offset 이후의 메시지를 읽어옵니다. 하지만 특정 장애 상황 복구나 데이터 재처리가 필요한 경우, **Seek API**를 사용하여 원하는 시점(Offset)으로 되돌아가 다시 메시지를 소비할 수 있습니다.

## 1. 주요 메커니즘: `seek()`

Kafka Java Client는 `KafkaConsumer.seek()` 메서드를 제공합니다. 이 메서드를 사용하면 컨슈머가 다음에 읽을 위치를 강제로 지정할 수 있습니다.

**주의사항**:

*   `poll()`을 한 번이라도 호출하여 파티션이 할당(Assign)된 상태에서만 `seek()`를 사용할 수 있습니다.
*   수동으로 할당(`assign()`)한 경우에는 즉시 사용 가능합니다.

---

## 2. Java 예제: 특정 Offset으로 이동하여 재처리

이 예제는 특정 토픽의 0번 파티션에서 **Offset 500번**부터 다시 읽어오는 로직을 보여줍니다.

```java
import org.apache.kafka.clients.consumer.*;
import org.apache.kafka.common.TopicPartition;

import java.time.Duration;
import java.util.Collections;
import java.util.Properties;

public class KafkaSeekExample {
    public static void main(String[] args) {
        Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(ConsumerConfig.GROUP_ID_CONFIG, "re-process-group");
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringDeserializer");
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringDeserializer");
        // 자동 커밋을 끄는 것이 안전함 (재처리 도중 커밋 방지)
        props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "false");

        KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
        String topic = "my-topic";
        TopicPartition partition0 = new TopicPartition(topic, 0);

        // 1. 파티션을 수동으로 할당 (또는 subscribe 후 첫 poll로 할당 대기)
        consumer.assign(Collections.singletonList(partition0));

        // 2. 특정 Offset으로 이동 (예: 500번 Offset부터 다시 읽기)
        long targetOffset = 500L;
        consumer.seek(partition0, targetOffset);
        
        System.out.println(partition0 + " 파티션을 Offset " + targetOffset + "으로 변경했습니다.");

        try {
            while (true) {
                ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
                for (ConsumerRecord<String, String> record : records) {
                    System.out.printf("Consumed Record: offset = %d, key = %s, value = %s%n",
                            record.offset(), record.key(), record.value());
                    
                    // 비즈니스 로직 수행 후 필요한 경우 수동 커밋
                }
            }
        } finally {
            consumer.close();
        }
    }
}
```

---

## 3. 다른 시점 제어 방법

### 3.1 파티션의 맨 처음부터 다시 읽기
```java
consumer.seekToBeginning(Collections.singletonList(partition0));
```

### 3.2 파티션의 맨 마지막(최신)부터 읽기
```java
consumer.seekToEnd(Collections.singletonList(partition0));
```

### 3.3 특정 시간대(Timestamp) 기준으로 찾기
특정 날짜/시간 이후의 메시지를 재처리하고 싶을 때는 `offsetsForTimes()`를 사용하여 해당 시간의 Offset을 먼저 구한 뒤 `seek()`를 수행합니다.

```java
Map<TopicPartition, Long> timestampsToSearch = new HashMap<>();
timestampsToSearch.put(partition0, System.currentTimeMillis() - (24 * 60 * 60 * 1000)); // 24시간 전

Map<TopicPartition, OffsetAndTimestamp> offsets = consumer.offsetsForTimes(timestampsToSearch);
OffsetAndTimestamp offsetTimestamp = offsets.get(partition0);

if (offsetTimestamp != null) {
    consumer.seek(partition0, offsetTimestamp.offset());
}
```
