# Kafka Producer: RoundRobinPartitioner 이슈 (KAFKA-9965)

Kafka Producer에서 메시지 분배를 위해 `RoundRobinPartitioner`를 설정했을 때, 기대와 달리 특정 파티션으로 메시지가 쏠리는 불균형(Uneven Distribution) 현상이 발생할 수 있습니다. 이는 특히 Kafka 2.4~3.3 버전 사이에서 두드러진 이슈입니다.

---

## 1. 이슈 개요 (KAFKA-9965)

*   **현상**: `partitioner.class`를 `RoundRobinPartitioner`로 설정했음에도 불구하고, 파티션 간 메시지 인입량이 균등하지 않고 불균형하게 분배됨.
*   **원인**: Kafka 2.4에 도입된 **KIP-480 (Sticky Partitioning)**과의 상호작용 버그.
*   **상태**: 해결됨 (KAFKA-17632로 통합 관리되어 패치됨).

---

## 2. 상세 원인 분석

### 2.1 Sticky Partitioning과의 충돌
Kafka 2.4부터 Producer의 효율성을 높이기 위해 **Sticky Partitioning**이 도입되었습니다. 이는 메시지를 보낼 때 매번 파티션을 바꾸는 대신, 하나의 배치(Batch)가 찰 때까지 한 파티션에 머무르는 전략입니다.

### 2.2 중복 호출 문제
`RoundRobinPartitioner`의 `partition()` 메서드가 내부적으로 메시지 배치 생성 시점에 **여러 번 호출**되는 경우가 발생했습니다.
1.  메시지를 보낼 파티션을 결정하기 위해 `partition()` 호출.
2.  이때 새로운 배치가 필요하다고 판단되면, 내부 로직에 의해 `partition()`이 다시 호출됨.
3.  `RoundRobinPartitioner`는 호출될 때마다 내부 카운터를 증가시키는데, 한 레코드에 대해 카운터가 두 번 증가하면서 논리적인 순서가 꼬이게 됨.

---

## 3. 해결 방법 및 권장 사항

### 3.1 DefaultPartitioner 사용 (권장)
Kafka 2.4 이후 버전이라면 `RoundRobinPartitioner`를 명시적으로 설정하기보다, **`DefaultPartitioner`**를 그대로 사용하는 것이 가장 좋습니다.
*   `DefaultPartitioner`는 키(Key)가 없을 때 자동으로 Sticky 전략을 사용하며, 전체적으로는 파티션 간 균등한 분배를 보장하면서도 처리량(Throughput)은 훨씬 높습니다.

### 3.2 클라이언트 버전 업그레이드
만약 반드시 `RoundRobinPartitioner`를 사용해야 한다면, 해당 버그가 수정된 **Kafka 3.3.0 이상** 버전의 클라이언트를 사용하는 것이 안전합니다.

### 3.3 커스텀 Partitioner 구현
특수하게 엄격한 라운드 로빈이 필요하다면, `Partitioner` 인터페이스를 직접 구현하여 배치 생성 시점의 중복 호출에 영향을 받지 않도록 카운팅 로직을 정교하게 설계해야 합니다.

---

## 4. 요약
`RoundRobinPartitioner`는 이름과 달리 현대적인 Kafka Producer 환경(배치 처리 및 Sticky 전략)에서 성능과 균등 분배 두 마리 토끼를 모두 놓칠 위험이 있습니다. 성능이 중요하다면 **Default 전략**을, 이슈 방지가 중요하다면 **최신 버전 업그레이드**를 선택하세요.
