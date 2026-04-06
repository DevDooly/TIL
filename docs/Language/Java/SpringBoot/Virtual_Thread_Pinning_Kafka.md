# Java Virtual Thread: Kafka Consumer Pinning 이슈 분석

Java 21의 가상 스레드(Virtual Thread)를 사용하여 Kafka Message Listener나 Consumer 루프를 실행할 때, Kafka Client 내부의 `synchronized` 블록으로 인해 캐리어 스레드(Carrier Thread)가 차단되는 **Pinning 현상**과 이로 인한 시스템 성능 저하 사례를 정리합니다.

---

## 1. 이슈 배경 (Symptom)

* **상황**: 대량의 메시지를 처리하기 위해 Kafka Consumer를 실행하는 루프 프로세스를 가상 스레드(Virtual Thread)로 생성하여 운영함.
* **현상**: 가상 스레드 수는 충분함에도 불구하고, 메시지 처리 속도가 급격히 떨어지거나 애플리케이션 전체가 응답하지 않는 현상 발생.
* **원인**: Kafka Client 라이브러리 내부의 `synchronized` 블록에서 I/O 작업이나 대기(wait)가 발생하면서 캐리어 스레드가 고갈됨.

---

## 2. 상세 원인 분석 (Root Cause)

### 2.1 Virtual Thread Pinning
가상 스레드는 `synchronized` 블록 내에서 차단 작업(Blocking I/O 등)을 수행할 때, 자신을 실행 중인 캐리어 스레드(Platform Thread)에서 내려오지 못하고 점유해 버립니다. 이를 **Pinning**이라고 합니다.

### 2.2 Kafka Fetcher.poll()의 synchronized
문제가 된 지점은 Kafka Client의 **`Fetcher.poll()`** 내부입니다.

* Kafka Consumer는 데이터를 가져오기 위해 주기적으로 `poll()`을 호출합니다.
* 구 버전의 Kafka Client(특히 3.x 버전의 일부 내부 로직)는 스레드 안전성을 보장하기 위해 `synchronized` 블록을 광범위하게 사용합니다.
* 가상 스레드가 이 블록 안에서 네트워크 I/O 응답을 기다리게 되면, 캐리어 스레드 풀(ForkJoinPool)의 실제 스레드들이 모두 차단되어 다른 가상 스레드들이 실행 기회를 얻지 못하게 됩니다.

---

## 3. 해결 방안 (Solutions)

### 3.1 Kafka Client 버전 상황 (3.7 ~ 3.9)

* ** Apache Kafka 3.7 ~ 3.9**: 가상 스레드 친화적인 구조(`ReentrantLock` 교체)로 개선하기 위한 작업이 단계적으로 진행되고 있으나, **3.9 버전에서도 모든 `synchronized` 블록이 제거된 것은 아닙니다.** 여전히 특정 실행 경로에서 Pinning이 발생할 수 있습니다.

* **Kafka 4.0**: 최소 요구 사양이 상향되면서 가상 스레드에 최적화된 구조가 완성될 것으로 기대되는 버전입니다.



### 3.2 JDK 24 도입 (가장 확실한 해결책)

* 라이브러리의 수정을 기다리기 어렵다면 **JDK 24**로 업그레이드하는 것을 권장합니다.

* **JEP 491**에 의해 `synchronized` 블록 내에서도 가상 스레드가 캐리어 스레드로부터 마운트 해제(Unmount)될 수 있게 되어, 라이브러리 코드 수정 없이 Pinning 이슈를 해결할 수 있습니다.



### 3.3 Platform Thread 사용 (현실적 권장 사항)


현재 Kafka Client 구조상 완벽한 Pinning 자유가 보장되지 않는다면, Consumer 루프 자체는 가상 스레드가 아닌 **플랫폼 스레드(기존 방식)**에서 실행하는 것이 안정적입니다.

* 메시지를 가져오는 루프는 플랫폼 스레드에서 수행.
* 가져온 메시지의 **비즈니스 로직 처리** 부분만 가상 스레드 풀에 위임.

---

## 4. 교훈

* 가상 스레드는 모든 상황의 "은총알(Silver Bullet)"이 아닙니다.
* 사용 중인 라이브러리(Kafka, JDBC, FTP 등) 내부에 `synchronized` 블록이 대거 포함되어 있다면 가상 스레드 도입 시 반드시 **`-Djdk.tracePinnedThreads=full`** 옵션을 통해 모니터링을 수행해야 합니다.
