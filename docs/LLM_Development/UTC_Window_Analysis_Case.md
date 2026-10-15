# AI가 제안한 UTC 구간 계산을 테스트와 JMH로 확인하기

시각 문자열의 offset을 버리면 같은 순간이 다른 시간으로 바뀐다. 알고리즘이 빨라도 그 입력부터 잘못됐다면 결과는 틀린다. 개인 Platform Lab에서는 시간 처리 오류를 먼저 재현하고, 올바른 입력을 받는 두 알고리즘의 결과와 비용을 따로 비교했다.

[포트폴리오에서 코드와 결과 보기](https://devdooly.github.io/devdooly-platform-lab/#ai-window) · [실행 가능한 Java 예제](https://github.com/DevDooly/devdooly-platform-lab/tree/main/examples/java-window-analysis) · [측정 원본에서 추출한 근거](https://github.com/DevDooly/devdooly-platform-lab/blob/main/docs/evidence/ai-window-analysis/README.md)

이 사례는 회사 코드·수율 공식·제조 데이터를 사용하지 않은 독립 합성 예제다. 기존 [레거시 코드 개선 기록](Legacy_Code_Improvement.md)의 검증 방법을 작은 공개 문제에 적용했다.

## 먼저 답을 정의했다

고정된 UTC 시간창 안에서 여러 관측 세션의 **총 관측 시간**과 **최대 동시 세션 수**를 구한다. 구간은 `[시작, 종료)`로 다루므로 한 세션이 끝나는 순간 다른 세션이 시작해도 둘은 겹치지 않는다. 최대 동시는 관측 세션 수이며 고유한 물리 센서 수는 아니다.

입력은 최대 4,096세션, 시간창은 최대 1시간이다. 각 세션에는 명시적인 offset timestamp와 알려진 시계 오차가 있다. 오차가 `기록 시각 - 기준 시각`이라면 기록에서 그 값을 뺀다. 서버 시계나 NTP를 바꾸거나 알려지지 않은 오차를 추정하는 예제는 아니다.

LLM에는 구현뿐 아니라 반례와 비용을 함께 요청했다. 기존 운영 ETL은 이미 O(n)이어서 변경 대상으로 삼지 않았고, 경계 구간을 매번 전체 검사하는 독립 O(n²) 구현을 비교 기준으로 만들었다. AI가 제안한 코드와 agent 검토는 기록했으며 저장소 소유자의 사람 검토 상태는 아직 `PENDING`이다. [AI 활용 범위와 검토 상태](https://github.com/DevDooly/devdooly-platform-lab/blob/main/examples/java-window-analysis/PROVENANCE.md)

## offset을 버리는 오류를 고정 입력으로 재현했다

`2026-10-15T09:00:00+09:00`은 UTC `2026-10-15T00:00:00Z`와 같은 순간이다. 다음 발췌 코드는 offset을 버린 local time에 UTC를 다시 붙인다.

```java
// 의도적으로 잘못 만든 오류 재현 코드의 발췌
OffsetDateTime.parse(text)
    .toLocalDateTime()
    .toInstant(ZoneOffset.UTC);
```

이 코드는 원래 UTC 00시인 세션을 UTC 09시로 옮긴다. UTC 00시부터 1분인 창에서 10초짜리 세션을 찾으면 총 관측 시간은 잘못된 0초가 된다. 올바른 변환은 offset을 유지해 `Instant`를 만들고 알려진 오차를 뺀다.

```java
// 실제 UtcNormalizer의 변환 흐름 발췌
OffsetDateTime.parse(text)
    .toInstant()
    .minusNanos(knownClockSkewNanos);
```

Java 회귀 테스트는 오류 구현의 0초·동시 0과 수정 구현의 10초·동시 1을 각각 확인한다. offset이 없는 timestamp, 같은 시작·종료, 역전 구간, 중복 ID, 입력·오차 상한도 검사한다. `OffsetDateTime.toInstant()`는 같은 timeline의 순간을 반환한다. [Java 21 API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/time/OffsetDateTime.html#toInstant())

## 같은 답을 구하는 두 알고리즘을 비교했다

| 구현 | 처리 방법 | 시간복잡도 | 추가 메모리 |
| --- | --- | --- | --- |
| 기준 구현 | 정렬한 각 경계 사이에서 모든 세션을 다시 검사 | O(n²) | O(n) |
| 개선 구현 | TreeMap에 시작 +1·종료 -1을 합친 뒤 한 번 순회 | O(n log n) | O(n) |

개선 구현도 TreeMap 삽입과 정렬 비용을 포함한다. 같은 시점의 시작과 종료는 먼저 합쳐 반영하고, 이전 경계부터 현재 경계까지 활성 세션이 있을 때만 총 시간에 더한다. 두 구현은 동일하게 정규화하고 시간창에 맞춰 자른 입력을 받는다.

기준 구현과 결과가 같다는 검사만으로는 둘이 함께 틀리는 경우를 놓친다. 독립적인 64ns 정수 격자 oracle로 고정 seed 2,000사례와 입력 순서를 바꾼 경우를 확인했다. 큰 fixture에는 다음 닫힌 형태 기대값을 사용했다.

- sparse: 11ms 세션을 17ms 간격으로 배치한다. 총 시간은 `n × 11ms`, 최대 동시는 1이다.
- nested: 모든 세션이 함께 시작하고 종료를 1ms씩 늘린다. 총 시간은 `n × 1ms`, 최대 동시는 n이다.

Java 테스트는 20개가 통과했고 실패·오류·skip은 0이었다. 전체 구현과 테스트는 [예제 소스](https://github.com/DevDooly/devdooly-platform-lab/tree/main/examples/java-window-analysis/src)에서 볼 수 있다.

## JMH에서는 무엇을 측정했나

2026-10-15 로컬 Windows 11에서 Microsoft OpenJDK 21.0.9+10-LTS와 JMH 1.37로 측정했다. sparse·nested의 128·512·2,048·4,096세션과 두 메서드를 조합한 16조건이다. 조건마다 3 forks, thread 1개, G1·heap 256MiB, warmup 2×500ms와 측정 5×500ms를 사용했다. 전체 48개 fork JVM·240개 측정 interval을 기록했다.

한 번의 `op`는 선택한 fixture 전체를 분석하는 연산이다. 자료구조 생성과 정렬은 포함하며, 문자열 파싱·UTC 정규화·fixture 생성·I/O는 trial setup에서 제외했다. UTC 오류 수정의 전후 속도를 비교한 실험은 아니다.

| 분포·세션 수 | 기준 평균 ± 오차 (µs/op) | 개선 평균 ± 오차 (µs/op) |
| --- | ---: | ---: |
| sparse · 2,048 | 11,933.210 ± 10,205.116 | 250.923 ± 11.674 |
| sparse · 4,096 | 30,221.977 ± 7,982.477 | 632.113 ± 12.280 |
| nested · 4,096 | 12,918.556 ± 2,139.630 | 331.891 ± 7.542 |

오차는 JMH가 Student t 분포로 계산한 평균의 99.9% 신뢰구간 반폭이다. sparse/2,048 기준 구현처럼 평균에 비해 오차가 큰 조건도 있다. 짧은 warmup과 로컬 호스트의 영향을 분리하지 않았으므로 이 기록은 해당 합성 조건의 비교로 읽는다. 운영 처리량·p95나 SLA는 측정하지 않았다. [JMH 1.37 통계 계산](https://github.com/openjdk/jmh/blob/1.37/jmh-core/src/main/java/org/openjdk/jmh/util/AbstractStatistics.java)

할당량 `B/op`는 연산당 allocation이며 RSS나 최대 메모리가 아니다. 전체 수치·fork별 표본·fixture와 JAR의 SHA-256은 [공개 summary](https://github.com/DevDooly/devdooly-platform-lab/blob/main/docs/evidence/ai-window-analysis/summary.json)에 연결했다. 측정 당시 소스는 미커밋 overlay였으므로 `sourceCommit:null`을 유지하고 실제 파일 manifest로 식별했다. 소스·JAR은 측정 전후 불변을 확인했고, 생성된 원본 JSON은 SHA-256으로 식별해 보존했다.

## CI는 정답과 산출물을 확인한다

GitHub Actions와 Jenkins에는 Java 예제의 `verify`, JUnit과 필수 benchmark JAR 검사를 추가했다. 기존 API·웹 검사와 같은 source SHA 게시 gate를 함께 사용한다. CI에서는 JMH 성능 측정을 반복하지 않는다. 매 빌드의 호스트 잡음으로 성능 수치를 다시 쓰는 대신, 기능 검사와 별도의 측정 기록을 구분한다. [CI 연결 검증 범위](https://github.com/DevDooly/devdooly-platform-lab/blob/main/docs/evidence/ai-window-analysis/ci-validation.md)

다음 코드 개선에서도 먼저 틀린 입력과 기대 결과를 고정하고, 구현과 독립적인 답을 만든 뒤 비용을 측정하는 순서를 사용할 수 있다. 이 사례에서 남겨 둔 사람의 검토는 AI 제안 중 무엇을 실제로 채택하거나 바꿨는지를 판단하는 단계다.
