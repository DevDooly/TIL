# Spring Kafka: 테스트 코드에서 단일 메시지 소비

Spring Boot 애플리케이션 개발 중, `spring-kafka-test` 라이브러리(KafkaTestUtils 등)를 사용할 수 없는 환경에서도 순수 Kafka Client API만을 사용하여 테스트용 메시지를 단일 건만 컨슘하고 확인하는 방법을 다룹니다.

---

## 1. 주요 전략

`application.yml`에 정의된 빈(Bean) 설정을 그대로 사용하기보다, 테스트 메서드 내에서 **직접 `KafkaConsumer`를 설정하고 생성**하여 제어하는 것이 가장 독립적이고 확실한 테스트 방법입니다.

### 핵심 로직
1.  기존 서비스 컨슈머와 겹치지 않는 **고유한 Group ID** 할당.
2.  테스트 메시지를 놓치지 않기 위해 **`auto.offset.reset`을 `earliest`**로 설정.
3.  원하는 메시지를 찾을 때까지 **`poll()`** 수행 후 즉시 종료.

---

## 2. 테스트 코드 예제 (순수 Kafka API 활용)

`KafkaTestUtils` 없이 표준 `Properties`와 `KafkaConsumer`를 직접 사용하는 예시입니다.

```java
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.kafka.core.KafkaTemplate;

import java.time.Duration;
import java.util.Collections;
import java.util.Properties;

@SpringBootTest
public class KafkaSingleConsumeTest {

    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;

    @Test
    void testSingleMessageConsumeWithoutUtils() {
        String topic = "test-topic";
        String testMessage = "Hello Kafka Without Utils!";
        
        // 1. Consumer 설정 (Properties 직접 작성)
        Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092"); // 환경에 맞게 수정
        props.put(ConsumerConfig.GROUP_ID_CONFIG, "test-group-" + System.currentTimeMillis());
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "true");
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());

        // 2. Consumer 생성 및 구독
        try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props)) {
            consumer.subscribe(Collections.singletonList(topic));

            // 3. 테스트 데이터 발행
            kafkaTemplate.send(topic, testMessage);

            // 4. 단일 메시지 컨슘 루프
            boolean found = false;
            long timeoutMillis = 10000; // 최대 10초 대기
            long start = System.currentTimeMillis();

            while (System.currentTimeMillis() - start < timeoutMillis) {
                ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(500));
                
                if (!records.isEmpty()) {
                    for (ConsumerRecord<String, String> record : records) {
                        System.out.println("✅ 수신된 메시지: " + record.value());
                        System.out.println("📍 Offset: " + record.offset());
                        
                        // 원하는 메시지인지 검증 후 루프 탈출
                        if (record.value().equals(testMessage)) {
                            found = true;
                            break;
                        }
                    }
                }
                if (found) break;
            }

            if (!found) {
                throw new RuntimeException("❌ 10초 내에 메시지를 수신하지 못했습니다.");
            }
        }
    }
}
```

---

## 3. 주의 사항

*   **포트 번호**: `BOOTSTRAP_SERVERS_CONFIG`의 값은 테스트 환경(Embedded Kafka 사용 시 포트 유동적)에 따라 `@Value("${spring.kafka.bootstrap-servers}")` 등으로 주입받아 사용하는 것이 좋습니다.
*   **Deserializer**: 메시지 타입에 따라 `StringDeserializer` 대신 실제 프로젝트에서 사용하는 Deserializer 클래스를 지정해야 합니다.
*   **자원 해제**: `try-with-resources` 구문을 사용하여 테스트 종료 후 컨슈머가 정상적으로 닫히도록 관리합니다.