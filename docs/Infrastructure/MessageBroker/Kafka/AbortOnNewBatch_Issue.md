# Kafka: abortOnNewBatch와 파티셔너 중복 호출

Kafka 3.8.0의 Java producer에는 새 배치를 만들기 전에 파티션을 다시 선택하는 경로가 있다. 여기서 `partition()`이 두 번 호출되면 RoundRobin 카운터도 두 번 움직인다. 아래는 패치 전 구현의 흐름이다.

## 새 배치가 필요할 때

`abortOnNewBatch`는 accumulator에서 새 배치가 필요할 때 먼저 producer로 제어를 돌려주는 내부 플래그다. 구형 sticky 파티셔너의 `onNewBatch()`에 선택을 갱신할 기회를 준다.

1. `partition()`으로 대상 파티션을 계산한다.
2. accumulator에 추가한다. 새 배치가 필요하고 플래그가 켜져 있으면 `abortForNewBatch` 결과를 돌려준다.
3. producer가 `onNewBatch()`를 호출하고 파티션을 다시 계산한다.
4. 두 번째 `append()`는 `abortOnNewBatch=false`로 실제 배치에 추가한다.

두 번째 `append()`에서는 `abortOnNewBatch`가 꺼져 있으므로, 같은 이유로 계속 중단하는 루프는 생기지 않는다. [Kafka 3.8.0 KafkaProducer](https://github.com/apache/kafka/blob/3.8.0/clients/src/main/java/org/apache/kafka/clients/producer/KafkaProducer.java), [RecordAccumulator](https://github.com/apache/kafka/blob/3.8.0/clients/src/main/java/org/apache/kafka/clients/producer/internals/RecordAccumulator.java)

## RoundRobin에 미치는 영향

호출마다 카운터를 증가시키면 한 레코드에 대해 두 번 진행할 수 있다. 4개 파티션에서 매번 이 경로가 발생한다고 단순화하면, 최초 선택은 0·2, 최종 전송 선택은 1·3처럼 일부만 사용될 수 있다. 실제 분포는 새 배치 생성 빈도에 따라 달라진다.

`batch.size`를 키우면 이 경로를 타는 빈도는 달라질 수 있지만 이중 호출 자체를 없애지는 못한다. `onNewBatch()`를 덮어쓰는 경우에도 두 번 진행하는 카운터를 함께 살펴봐야 한다. 수정된 client의 동작은 [같은 조건의 재현 실험](Producer_Partitioner_Issue.md)으로 비교한다. [패치 PR](https://github.com/apache/kafka/pull/17620)

## 호출 흐름을 확인할 때

- 읽은 `doSend()` / `append()`의 버전 태그
- 최초 선택과 실제 전송 파티션, 새 배치 생성 여부
- 파티셔너의 상태 변경 지점과 인스턴스별 상태
- 패치 전후 동일 조건에서의 성공 레코드 분포

운영 코드에서 내부 API를 직접 호출해 우회하기보다는, 패치된 client를 적용하고 필요한 [파티셔닝 정책](Producer_Partitioner_Policy.md)을 선택하는 편이 유지보수하기 쉽다.
