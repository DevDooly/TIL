# Kafka Producer: RoundRobinPartitioner 불균형과 수정 버전

공식 이슈 확인: 2026-09-07. 버전은 애플리케이션의 `kafka-clients` 기준이다.

## 원인과 패치

라운드 로빈 파티셔너는 호출할 때마다 카운터를 이동한다. 구형 producer 경로에서는 새 배치를 만들 때 한 레코드에 대해 `partition()`이 두 번 호출될 수 있었다. 실제 전송에 사용하지 않은 파티션까지 카운터가 진행해 일부 파티션을 건너뛸 수 있다.

`KAFKA-17632`은 영향 버전에 **3.8.0**, 수정 버전에 **3.9.2 / 4.0.0**을 명시한다. 기존 문서의 “3.3.0 이상이면 해결”은 잘못된 안내다. 이 목록만으로 다른 모든 버전의 안전 여부를 단정하지 않는다. [KAFKA-17632](https://issues.apache.org/jira/browse/KAFKA-17632), [수정 PR #17620](https://github.com/apache/kafka/pull/17620)

이전 보고 [KAFKA-9965](https://issues.apache.org/jira/browse/KAFKA-9965)도 참고하되, 적용 판단은 사용하는 client 버전과 패치 코드로 한다.

## 재현 시 고정할 조건

- client/JDK 버전, `partitioner.class`, 키 유무와 producer 수
- 파티션 수, 레코드 수·직렬화 크기, `batch.size`와 `linger.ms`
- send callback의 `RecordMetadata.partition()`별 성공 건수
- 오류·재시도와 측정 구간, 브로커 상태

짝수 개 파티션에 동일 크기의 null-key 레코드를 보내 업그레이드 전후의 성공 레코드 분포를 비교한다. 단순 카운터로 만든 커스텀 파티셔너도 이중 호출에 영향받을 수 있다.

## 정책 선택과 운영 검증

키 기반 순서가 필요하면 키의 분포와 파티션 수 변경 영향을 먼저 검토한다. 배치 효율을 원한다면 `partitioner.class`를 생략한 기본 전략을 기준으로 측정한다. RoundRobin의 레코드 개수 균등함이 바이트 수·처리 시간·consumer lag의 균등함을 뜻하지는 않는다.

업그레이드 후에도 hot key, 느린 브로커, consumer 처리 비용 차이로 쏠림이 남을 수 있다. [설정 예제](Producer_Partitioner_Policy.md), [정책 변화와 측정 기준](Partitioner_Evolution_and_Imbalance.md), [내부 호출 흐름](AbortOnNewBatch_Issue.md)
