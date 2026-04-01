# Kafka 파티셔너의 진화와 불균형(Imbalance) 문제 해결

Kafka 3.9 버전 이상을 사용함에도 불구하고 `RoundRobinPartitioner`나 기본 정책 사용 시 특정 파티션으로 Offset이 쏠리는 현상이 발생할 수 있습니다. 이는 버전별 파티셔너 정책의 변화와 Kafka의 효율적인 배치 전송 메커니즘이 충돌하면서 발생하는 구조적인 문제입니다.

---

## 1. 버전별 파티셔너 정책 변천사

| 버전 | 기본 파티셔너 정책 (Key가 없을 때) | 특징 |
| :--- | :--- | :--- |
| **~ 2.3** | **Round-Robin** | 메시지 하나마다 파티션을 순차적으로 변경 (배치 효율 낮음) |
| **2.4 ~ 3.2** | **Sticky Partitioning** | 배치가 찰 때까지 한 파티션에 고정 (처리량 대폭 향상) |
| **3.3 ~ 3.9** | **Built-in Partitioner** | Sticky 전략을 기본으로 하되, 보다 정교한 배치 관리 로직 적용 |
| **4.0 (예정)** | **Refactored Partitioner** | 레거시 파티셔너 클래스들 제거 및 내부 로직 최적화 (KRaft 전용) |

---

## 2. 왜 최신 버전에서도 불균형이 발생하는가?

Kafka 3.9 환경에서 Offset 불균형이 발생하는 주요 원인은 다음과 같습니다.

### 2.1 Sticky Partitioning의 부작용
기본 정책인 Sticky 방식은 성능을 위해 **배치가 완성될 때까지 한 파티션에 메시지를 몰아넣습니다.** 
*   만약 메시지 송신 주기가 불규칙하거나, 특정 시점에 전송이 몰리면 해당 시점에 선택된 파티션만 Offset이 급격히 증가합니다.
*   `batch.size`가 크고 `linger.ms`가 짧으면, 미처 배치가 차기 전에 전송이 일어나며 파티션 이동이 빈번해지거나 반대로 너무 고정되어 불균형이 생깁니다.

### 2.2 RoundRobinPartitioner의 한계
명시적으로 `RoundRobinPartitioner`를 설정하더라도 다음과 같은 이유로 완벽한 분배가 어려울 수 있습니다.
*   **Producer 인스턴스 개수**: 각 Producer는 독립적인 카운터를 가집니다. Producer가 여러 대일 경우 전체 클러스터 관점에서의 순차 분배는 보장되지 않습니다.
*   **내부 카운터 초기화**: Producer 재시작이나 메타데이터 갱신 시 카운터가 초기화되어 특정 파티션(보통 0번)부터 다시 시작하게 됩니다.

---

## 3. 실전 해결 방안: 불균형 최소화 전략

### 3.1 설정 튜닝 (Built-in 전략 최적화)
기본 파티셔너를 유지하면서 불균형을 줄이려면 배치 관련 설정을 조정해야 합니다.
*   **`linger.ms` 조정**: 값을 약간 높여(예: 5~10ms) 배치가 충분히 모인 뒤 전송되게 하면 파티션 이동이 더 고르게 일어납니다.
*   **`batch.size` 조정**: 메시지 크기에 맞춰 적절히 줄이면 파티션 간 이동 주기가 빨라져 분배가 균등해집니다.

### 3.2 커스텀 파티셔너 (Strict Round-Robin)
성능 저하를 감수하더라도 **절대적인 균등 분배**가 필요하다면, 배치와 상관없이 동작하는 커스텀 파티셔너를 구현해야 합니다.

```java
public class StrictRoundRobinPartitioner implements Partitioner {
    private final AtomicInteger counter = new AtomicInteger(0);

    @Override
    public int partition(String topic, Object key, byte[] keyBytes, 
                         Object value, byte[] valueBytes, Cluster cluster) {
        List<PartitionInfo> partitions = cluster.partitionsForTopic(topic);
        int numPartitions = partitions.size();
        
        // 배치와 무관하게 무조건 순차적으로 파티션 번호 부여
        int p = Math.abs(counter.getAndIncrement()) % numPartitions;
        return p;
    }

    @Override
    public void close() {}
    @Override
    public void configure(Map<String, ?> configs) {}
}
```

---

## 4. 결론 및 권장 사항

1.  **Kafka 3.9/4.0**에서는 레거시 `RoundRobinPartitioner` 클래스를 직접 쓰기보다 **`DefaultPartitioner`를 쓰고 설정을 튜닝**하는 것이 성능 면에서 유리합니다.
2.  **불균형 수용**: Kafka의 철학은 '완벽한 분배'보다 '높은 처리량'에 우선순위를 둡니다. 약간의 Offset 차이는 정상적인 동작으로 간주하고 Consumer를 충분히 배치하여 처리량을 확보하는 것이 권장됩니다.
3.  **모니터링**: `kafka-consumer-groups` 명령어로 파티션별 **LAG**을 주기적으로 모니터링하여 특정 파티션만 처리가 늦어지는지 확인하세요.
