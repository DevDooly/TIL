# Kafka Producer: 파티셔닝 변화와 불균형 진단

파티션별 건수가 다르다고 항상 파티셔너 버그인 것은 아니다. 기본 정책은 Kafka client 버전에 따라 바뀌었고, 키 분포나 배치 상태도 결과에 영향을 준다. 아래는 Java client 3.9와 4.0 문서를 기준으로 정리한 변화다.

## 버전별 변화

| Client 계열 | 기본 정책에서 확인할 변화 |
| :--- | :--- |
| 2.4 이전 | 키가 있으면 해시 기반, 없으면 레코드별 분산 |
| 2.4–3.2 | null key에 sticky 정책 도입. 새 배치 시점과 연동 |
| 3.3 이후 | KIP-794에 따른 기본 내장 로직. null-key 분산과 adaptive 설정 확인 |
| 4.0 | deprecated `DefaultPartitioner` / `UniformStickyPartitioner` 클래스 제거 |

기본 정책을 쓰려면 `partitioner.class`를 생략하면 된다. 예전 `internals.DefaultPartitioner` 클래스를 직접 지정하는 설정과는 다르다. [Kafka 3.3 변경 안내](https://kafka.apache.org/33/documentation/#upgrade_330_notable), [Kafka 4.0 업그레이드](https://kafka.apache.org/40/getting-started/upgrade/)

## 무엇이 균등해야 하는가

기본 전략은 레코드를 한 건씩 순번대로 나누지 않는다. Adaptive partitioning은 빠른 브로커 쪽에 더 많은 데이터를 보내기도 한다. 따라서 짧은 구간의 건수만 보기보다 바이트 수와 처리 지연을 함께 봐야 한다. [Producer 설정](https://kafka.apache.org/39/configuration/producer-configs/)

| 관측 | 함께 확인할 원인 |
| :--- | :--- |
| 레코드 수 편중 | hot key, null-key 정책, 명시적 파티션, client 버그 |
| 건수는 비슷한데 바이트 편중 | 직렬화 크기·압축률 |
| 건수·바이트는 비슷한데 lag 편중 | 처리 비용, 외부 I/O, consumer 재시도 |
| 배포 직후 짧은 구간만 편중 | producer 수명·수, 배치 상태, 측정 시간 |
| 파티션 증가 후 순서·분포 변화 | 키 해시 매핑 변경과 기존 레코드 잔존 |

RoundRobin의 시작 파티션과 카운터 상태를 분석할 때는 사용하는 client의 구현과 인스턴스 수명을 확인한다. 카운터가 항상 0에서 시작하거나 메타데이터 갱신 때마다 초기화된다고 전제하면 실제 분포와 계산이 어긋날 수 있다.

## 검증 순서

1. callback에서 성공 건수와 bytes를 파티션별로 집계한다.
2. 키 빈도, producer 수, 파티션 수를 고정한다.
3. 배치·linger·압축·adaptive 설정을 하나씩 바꿔 비교한다.
4. 처리량, p95/p99 지연, 오류율과 lag를 함께 본다.
5. RoundRobin이면 [중복 호출 패치](Producer_Partitioner_Issue.md)를 확인한다.

단순 카운터로 직접 파티셔너를 만들 때도 주의가 필요하다. `Math.abs(counter++) % partitions`는 정수 최솟값에서 음수를 반환할 수 있고, 한 레코드에 두 번 호출되는 문제도 그대로 남는다.

구성 예제는 [파티셔너 설정](Producer_Partitioner_Policy.md)을 참고한다.
