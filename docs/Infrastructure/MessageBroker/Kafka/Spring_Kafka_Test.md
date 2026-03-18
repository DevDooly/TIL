# Spring Kafka: 테스트 코드에서 단일 메시지 소비

Spring Boot 애플리케이션 개발 중, 테스트 코드에서 실제로 Kafka 메시지가 정상적으로 발행되었는지 확인하기 위해 **테스트용 Group ID**를 사용하여 메시지를 딱 한 건만 컨슘하고 내용을 출력해야 하는 경우가 있습니다.

이 가이드에서는 `application.yml` 설정을 유지하면서, 테스트 코드 내에서만 설정을 동적으로 변경하여 메시지를 확인하는 방법을 다룹니다.

---

## 1. 주요 전략: `KafkaConsumer` 직접 활용

스프링의 `@KafkaListener`는 비동기로 동작하므로 테스트 코드에서 결과를 즉시 확인하기 까다롭습니다. 가장 확실한 방법은 테스트 메서드 내에서 **직접 `KafkaConsumer`를 생성**하여 `poll()` 하는 것입니다.

### 핵심 포인트
*   **Group ID 변경**: 기존 서비스의 컨슈머와 간섭을 피하기 위해 임의의 테스트용 그룹 ID를 할당합니다.
*   **Offset 초기화**: 테스트 시점 이전에 쌓인 메시지를 무시하려면 `auto.offset.reset`을 `latest`로, 특정 메시지를 처음부터 확인하려면 `earliest`로 설정합니다.

---

## 2. 테스트 코드 예제

`DefaultKafkaConsumerFactory`를 사용하여 테스트 전용 컨슈머를 생성하는 예시입니다.

```java
import org.apache.kafka.clients.consumer.Consumer;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.kafka.core.DefaultKafkaConsumerFactory;
import org.springframework.kafka.test.utils.KafkaTestUtils;

import java.time.Duration;
import java.util.Collections;
import java.util.Map;

@SpringBootTest
public class KafkaSingleConsumeTest {

    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;

    @Test
    void testSingleMessageConsume() {
        String topic = "test-topic";
        String testMessage = "Hello Kafka Test!";
        String testGroupId = "test-group-" + System.currentTimeMillis(); // 매번 새로운 그룹 ID 생성

        // 1. Consumer 설정 생성 (application.yml 기반 + 테스트용 설정 덮어쓰기)
        Map<String, Object> consumerProps = KafkaTestUtils.consumerProps("localhost:9092", "false", "true");
        consumerProps.put(ConsumerConfig.GROUP_ID_CONFIG, testGroupId);
        consumerProps.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        consumerProps.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        consumerProps.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);

        // 2. Consumer 생성 및 토픽 구독
        DefaultKafkaConsumerFactory<String, String> cf = new DefaultKafkaConsumerFactory<>(consumerProps);
        Consumer<String, String> consumer = cf.createConsumer();
        consumer.subscribe(Collections.singletonList(topic));

        // 3. 메시지 발행 (테스트 대상)
        kafkaTemplate.send(topic, testMessage);

        // 4. 단일 메시지 컨슘 및 확인
        try {
            // 최대 10초 동안 대기하며 메시지 폴링
            ConsumerRecords<String, String> records = consumer.poll(Duration.ofSeconds(10));
            
            if (!records.isEmpty()) {
                ConsumerRecord<String, String> record = records.iterator().next();
                System.out.println("✅ Consumed Message: " + record.value());
                System.out.println("📍 Offset: " + record.offset());
                System.out.println("👥 Group ID: " + testGroupId);
                
                // Assertions.assertThat(record.value()).isEqualTo(testMessage);
            } else {
                System.out.println("❌ 메시지를 수신하지 못했습니다.");
            }
        } finally {
            consumer.close();
        }
    }
}
```

---

## 3. 유용한 테스트 유틸리티 (Spring Kafka Test)

Spring Kafka는 테스트를 돕기 위한 `KafkaTestUtils` 클래스를 제공합니다.

*   `KafkaTestUtils.consumerProps(...)`: 기본 컨슈머 설정을 Map 형태로 반환해줍니다.
*   `KafkaTestUtils.getSingleRecord(consumer, topic)`: 더 간결하게 단일 레코드를 가져올 수 있는 유틸리티 메서드입니다.

```java
// 유틸리티를 사용한 더 간결한 방법
ConsumerRecord<String, String> singleRecord = KafkaTestUtils.getSingleRecord(consumer, topic, Duration.ofSeconds(10));
System.out.println("Received: " + singleRecord.value());
```
