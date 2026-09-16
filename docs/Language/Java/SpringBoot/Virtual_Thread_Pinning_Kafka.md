# Kafka Consumer와 Virtual Thread: Pinning 진단 범위

Kafka Consumer를 가상 스레드에서 돌린 뒤 lag가 늘었다면, 먼저 메시지 처리 시간과 poll 간격을 살펴본다. Pinning이 의심될 때는 Kafka 버전뿐 아니라 JDK 버전과 실제 호출 스택도 필요하다.

## 먼저 분리할 문제

Consumer lag는 메시지 처리 지연, GC, 리밸런싱, DB 연결 대기로도 늘어난다. 코드에 `synchronized`가 있더라도 그 안에서 어떤 작업을 기다리는지 확인해야 pinning과 연결할 수 있다.

예를 들어 `Fetcher.poll()`이 원인인지 살펴보려면, 사용하는 버전의 소스와 JFR 스택을 대조한다. 이때 필요한 정보는 다음과 같다.

- `java -version`과 실제 `kafka-clients` 의존성 버전
- `jdk.VirtualThreadPinned` 이벤트의 stack·빈도·지속 시간
- 같은 시간대의 poll 간격, 처리 시간, lag, CPU와 GC
- 호출 경로에 있는 애플리케이션 lock과 라이브러리 소스 태그

## JDK 버전의 차이

JDK 21–23에서는 monitor를 잡은 채 blocking하는 경로가 pinning을 유발할 수 있다. JDK 24의 JEP 491은 monitor 관련 제약을 개선했다. native/foreign 호출처럼 남아 있는 경로도 있어 Kafka를 4.0으로 올리는 것만으로 모든 pinning이 해결되지는 않는다. [JEP 491](https://openjdk.org/jeps/491), [JDK 25 Virtual Threads](https://docs.oracle.com/en/java/javase/25/core/virtual-threads.html)

진단 옵션도 JDK 버전에 맞춰야 한다. JDK 24부터는 `jdk.tracePinnedThreads`가 제거되었다. [진단 절차](../Virtual_Threads_FTP_Pinning.md)

## Consumer 소유권은 별도 제약이다

JDK를 올려도 `KafkaConsumer`는 thread-safe해지지 않는다. 한 소유 스레드에서 poll·commit·close를 수행하는 구조를 유지한다. 실제로 문제가 재현되는 구형 경로라면 poll 루프를 전용 플랫폼 스레드에 두는 방안을 비교할 수 있다. [KafkaConsumer API](https://kafka.apache.org/39/javadoc/org/apache/kafka/clients/consumer/KafkaConsumer.html)

메시지 처리를 가상 스레드로 넘기면 poll 루프와 처리 완료 시점이 분리된다. 이때 처리 순서, 완료된 offset, 대기 작업 수를 관리하고 리밸런싱·종료 시 남은 작업을 어떻게 정리할지도 정해야 한다. 우선 [동기 처리와 안전 종료 예제](../../../Infrastructure/MessageBroker/Kafka/Consumer_Safe_Shutdown.md)를 기준으로 검증한다.

업그레이드 전후에는 동일 입력으로 처리량·p99·lag·pinning 시간을 비교한다. 버전 변경과 실행기 구조 변경을 한 번에 적용하면 원인 판별이 어려워진다.
