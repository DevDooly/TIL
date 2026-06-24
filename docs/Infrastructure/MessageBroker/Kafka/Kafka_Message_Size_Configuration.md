# Kafka 메시지 최대 사이즈 확장 가이드 (Broker 재기동 없이)

Kafka 메시지 크기 제한 (기본 1MB)을 초과하여 에러가 발생했을 때, Broker 재기동 없이 메시지 최대 사이즈를 2MB (혹은 그 이상)로 확장하는 방법을 다룹니다.

**주의:** Broker 재기동 없이 설정을 변경하는 것은 제한적이며, 특히 `replica.fetch.max.bytes` 설정과 관련하여 심각한 데이터 복제 문제를 야기할 수 있습니다. 본 문서는 이 위험성을 명확히 인지하고 진행하는 것을 전제로 합니다.

---

## 1. 전제 조건: `replica.fetch.max.bytes` 확인 필수

가장 먼저 확인해야 할 것은 **현재 Kafka Broker의 `replica.fetch.max.bytes` 설정 값**입니다. 이 값은 Broker 간 메시지 복제 시 Fetch할 수 있는 최대 크기를 정의하며, 기본값은 1MB입니다.

*   **문제 발생 지점**: 만약 `replica.fetch.max.bytes`가 1MB인 상태에서 Topic의 `message.max.bytes`를 2MB로 늘리면, 1MB를 초과하는 메시지는 Broker 간 복제에 실패하여 **Under-replicated Partition**이 발생합니다. 이는 데이터 유실 및 가용성 저하로 이어집니다.
*   **설정 위치**: `replica.fetch.max.bytes`는 Broker의 `server.properties` 파일에 설정되며, **Broker 재기동 없이는 변경할 수 없습니다.**
*   **결론**: "Broker 재기동 없이" 2MB 메시지 처리를 목표로 한다면, 현재 모든 Broker의 `server.properties` 파일에서 `replica.fetch.max.bytes`가 **이미 2MB 이상으로 설정되어 있음을 반드시 확인**해야 합니다. 만약 그렇지 않다면, 이 방법으로는 안정적인 처리가 불가능합니다.

    ```bash
    # 각 Kafka Broker에서 server.properties 파일을 확인합니다.
    grep "replica.fetch.max.bytes" /path/to/kafka/config/server.properties
    ```

---

## 2. Producer 설정 변경

Producer가 한 번의 요청으로 Broker에 보낼 수 있는 최대 메시지 크기를 조정합니다.

*   **파라미터**: `max.request.size`
*   **기본값**: 1MB (1048576 bytes)
*   **권장 변경 값**: 2MB (2097152 bytes)

```java
// Java Kafka Producer 설정 예시
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "org.apache.kafka.common.serialization.ByteArraySerializer"); // 대용량 메시지 전송 시
props.put("max.request.size", 2097152); // 2MB
```

---

## 3. Consumer 설정 변경

Consumer가 Broker로부터 한 번에 Fetch할 수 있는 최대 메시지 크기를 조정합니다.

*   **파라미터 1**: `fetch.message.max.bytes`
    *   **설명**: Consumer가 Broker로부터 한 번의 Fetch 요청으로 받을 수 있는 최대 레코드 배치(batch)의 크기.
    *   **기본값**: 1MB (1048576 bytes)
    *   **권장 변경 값**: 2MB (2097152 bytes)
*   **파라미터 2**: `max.partition.fetch.bytes`
    *   **설명**: Consumer가 Broker로부터 **단일 파티션**에 대해 한 번의 Fetch 요청으로 받을 수 있는 최대 바이트 수. 이 값은 `fetch.message.max.bytes`보다 작거나 같아야 합니다.
    *   **기본값**: 1MB (1048576 bytes)
    *   **권장 변경 값**: 2MB (2097152 bytes)

```java
// Java Kafka Consumer 설정 예시
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("group.id", "my-group");
props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
props.put("value.deserializer", "org.apache.kafka.common.serialization.ByteArrayDeserializer");
props.put("fetch.message.max.bytes", 2097152);    // 2MB (전체 Fetch 요청 제한)
props.put("max.partition.fetch.bytes", 2097152); // 2MB (단일 파티션 Fetch 제한)
```

---

## 4. Broker 설정 변경 (재기동 없이 - Topic Level)

Broker-wide `message.max.bytes`는 재기동이 필요하지만, **특정 Topic에 대해서는 `message.max.bytes` 설정을 동적으로 변경할 수 있습니다.** 이는 Broker 재기동 없이 메시지 크기를 늘릴 수 있는 유일한 방법입니다.

*   **파라미터**: `message.max.bytes`
*   **설명**: Topic에 저장될 수 있는 개별 메시지의 최대 크기 (헤더 포함).
*   **기본값**: Broker의 `message.max.bytes` (기본 1MB)를 따르거나, Topic 생성 시 지정.
*   **권장 변경 값**: 2MB (2097152 bytes)

### 4.1. Topic 설정 변경 명령어

`kafka-configs.sh` 스크립트를 사용하여 Topic 설정을 변경합니다. 영향을 받는 모든 Topic에 대해 이 명령을 실행해야 합니다.

```bash
# Topic 설정을 변경하는 명령어 (예: "my-large-message-topic" Topic)
kafka-configs.sh --bootstrap-server <broker_ip>:<port> 
                 --entity-type topics 
                 --entity-name my-large-message-topic 
                 --alter 
                 --add-config message.max.bytes=2097152

# 예시:
# kafka-configs.sh --bootstrap-server localhost:9092 
#                  --entity-type topics 
#                  --entity-name my-large-message-topic 
#                  --alter 
#                  --add-config message.max.bytes=2097152
```

*   `<broker_ip>:<port>`: Kafka Broker의 주소와 포트 (예: `localhost:9092`)

### 4.2. 변경된 Topic 설정 확인

변경이 올바르게 적용되었는지 다음 명령어로 확인할 수 있습니다.

```bash
kafka-configs.sh --bootstrap-server <broker_ip>:<port> 
                 --entity-type topics 
                 --entity-name my-large-message-topic 
                 --describe
```

출력 결과에 `message.max.bytes=2097152`가 포함되어 있어야 합니다.

---

## 5. 최종 권고 사항 및 테스트

1.  **`replica.fetch.max.bytes` 확인이 최우선:** Broker 재기동 없이 이 설정을 변경할 수 없으므로, 현재 모든 Broker에서 이 값이 2MB 이상인지 **반드시** 확인해야 합니다.
2.  **테스트 필수:** 설정 변경 후, 실제 환경과 유사한 조건에서 2MB 메시지를 Produce하고 Consume하는 테스트를 충분히 수행해야 합니다.
3.  **모니터링:** 설정 변경 후 Kafka 클러스터의 상태 (특히 `UnderReplicatedPartitions`, Consumer Lag, Broker 에러 로그 등)를 주의 깊게 모니터링하여 문제가 없는지 확인합니다.

---

## 관련 문서
*   [Kafka 파티션 전략 및 산정](Partition_Strategy.md)
*   [Kafka 파티셔너 정책 및 설정](Producer_Partitioner_Policy.md)
