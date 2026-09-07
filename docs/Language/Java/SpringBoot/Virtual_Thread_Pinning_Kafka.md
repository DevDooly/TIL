# Kafka Consumer와 Virtual Thread: Pinning 진단 범위

확인일: 2026-09-07. Kafka 버전만으로 pinning 여부를 단정하지 않고 JDK·client·실행 경로를 함께 기록한다.

## 먼저 분리할 문제

consumer lag는 pinning 외에도 업무 처리 지연, GC, 재균형, DB 연결 대기 때문에 증가한다. 라이브러리에 `synchronized`가 있다는 것만으로 원인이 확정되지는 않는다.

기존 문서의 “`Fetcher.poll()` 내부가 원인”이라는 특정 메서드 단정은 해당 버전의 소스와 JFR stack 없이 일반화할 수 없다. 다음 증거를 함께 남긴다.

- `java -version`과 실제 `kafka-clients` 의존성 버전
- `jdk.VirtualThreadPinned` 이벤트의 stack·빈도·지속 시간
- 같은 시간대의 poll 간격, 처리 시간, lag, CPU와 GC
- 호출 경로에 있는 애플리케이션 lock과 라이브러리 소스 태그

## JDK 버전의 차이

JDK 21–23에서는 monitor를 잡은 채 blocking하는 경로가 pinning을 유발할 수 있다. JDK 24의 JEP 491은 monitor 관련 제약을 개선했다. native/foreign 호출 등 남는 경우가 있으므로 “Kafka 4.0이면 모든 pinning이 사라진다”는 보장은 없다. [JEP 491](https://openjdk.org/jeps/491), [JDK 25 Virtual Threads](https://docs.oracle.com/en/java/javase/25/core/virtual-threads.html)

진단 옵션도 버전에 따라 다르다. `jdk.tracePinnedThreads`를 모든 JDK에서 유효한 진단법으로 안내하지 않는다. [진단 절차](../Virtual_Threads_FTP_Pinning.md)

## Consumer 소유권은 별도 제약이다

JDK를 올려도 `KafkaConsumer`는 thread-safe해지지 않는다. 한 소유 스레드에서 poll·commit·close를 수행하는 구조를 유지한다. 실제로 문제가 재현되는 구형 경로라면 poll 루프를 전용 플랫폼 스레드에 두는 방안을 비교할 수 있다. [KafkaConsumer API](https://kafka.apache.org/39/javadoc/org/apache/kafka/clients/consumer/KafkaConsumer.html)

메시지 처리를 가상 스레드에 넘기는 것만으로 끝나지 않는다. 순서, 완료 offset, backpressure, rebalance와 종료 시 drain을 설계해야 한다. 우선 [동기 처리와 안전 종료 예제](../../../Infrastructure/MessageBroker/Kafka/Consumer_Safe_Shutdown.md)를 기준으로 검증한다.

업그레이드 전후에는 동일 입력으로 처리량·p99·lag·pinning 시간을 비교한다. 버전 변경과 실행기 구조 변경을 한 번에 적용하면 원인 판별이 어려워진다.
