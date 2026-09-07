# Kafka Producer: 파티셔닝 변화와 불균형 진단

기준: Java client 3.9 / 4.0 공식 문서, 2026-09-07.

## 버전별 변화

| Client 계열 | 기본 정책에서 확인할 변화 |
| :--- | :--- |
| 2.4 이전 | 키가 있으면 해시 기반, 없으면 레코드별 분산 |
| 2.4–3.2 | null key에 sticky 정책 도입. 새 배치 시점과 연동 |
| 3.3 이후 | KIP-794에 따른 기본 내장 로직. null-key 분산과 adaptive 설정 확인 |
| 4.0 | deprecated `DefaultPartitioner` / `UniformStickyPartitioner` 클래스 제거 |

“기본 파티셔너”와 옛 `internals.DefaultPartitioner` 클래스를 구분한다. 기본 정책은 `partitioner.class`를 생략한다. [Kafka 3.3 변경 안내](https://kafka.apache.org/33/documentation/#upgrade_330_notable), [Kafka 4.0 업그레이드](https://kafka.apache.org/40/getting-started/upgrade/)

## 무엇이 균등해야 하는가

기본 전략은 레코드마다 정확한 순번으로 순회하는 계약이 아니다. Adaptive partitioning은 빠른 브로커 쪽에 더 많은 데이터를 보내려는 정책이다. 짧은 구간의 건수만으로 버그라고 판단하지 않는다. [Producer 설정](https://kafka.apache.org/39/configuration/producer-configs/)

| 관측 | 함께 확인할 원인 |
| :--- | :--- |
| 레코드 수 편중 | hot key, null-key 정책, 명시적 파티션, client 버그 |
| 건수는 비슷한데 바이트 편중 | 직렬화 크기·압축률 |
| 건수·바이트는 비슷한데 lag 편중 | 처리 비용, 외부 I/O, consumer 재시도 |
| 배포 직후 짧은 구간만 편중 | producer 수명·수, 배치 상태, 측정 시간 |
| 파티션 증가 후 순서·분포 변화 | 키 해시 매핑 변경과 기존 레코드 잔존 |

RoundRobin 카운터가 항상 0에서 시작하거나 metadata 갱신마다 0으로 돌아간다고 가정하지 않는다. 구현과 client 수명을 확인한다.

## 검증 순서

1. callback에서 성공 건수와 bytes를 파티션별로 집계한다.
2. 키 빈도, producer 수, 파티션 수를 고정한다.
3. 배치·linger·압축·adaptive 설정을 하나씩 바꿔 비교한다.
4. 처리량, p95/p99 지연, 오류율과 lag를 함께 본다.
5. RoundRobin이면 [중복 호출 패치](Producer_Partitioner_Issue.md)를 확인한다.

`Math.abs(counter++) % partitions`는 정수 최솟값에서 음수가 될 수 있고 이중 호출도 해결하지 않는다. 기존 “StrictRoundRobin이면 절대 균등” 예제는 이런 보장을 제공하지 못하므로 제거했다.

구성 예제는 [파티셔너 설정](Producer_Partitioner_Policy.md)을 참고한다.
