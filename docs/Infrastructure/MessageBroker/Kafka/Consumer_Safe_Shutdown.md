# Kafka: Consumer의 안전한 종료 (wakeup vs close)

Java Kafka Consumer는 **스레드 세이프(Thread-safe)하지 않습니다.** 따라서 여러 스레드에서 동시에 접근하면 예기치 않은 예외가 발생합니다. 외부 스레드에서 Consumer를 안전하게 멈추고 리소스를 정리하는 올바른 방법을 정리합니다.

---

## 1. wakeup() vs close() 차이점

| 기능 | wakeup() | close() |
| :--- | :--- | :--- |
| **스레드 안전성** | **스레드 세이프 (Thread-safe)** | **스레드 안전하지 않음** |
| **주요 역할** | 블로킹된 `poll()`을 즉시 중단시킴 | 오프셋 커밋 및 커넥션 종료, 리소스 해제 |
| **결과** | `WakeupException` 발생 | Consumer 사용 불가 상태로 전환 |
| **사용 시점** | 외부 스레드에서 종료 신호를 보낼 때 | 모든 로직이 끝난 후 리소스를 정리할 때 |

---

## 2. 왜 IllegalStateException이 발생했는가?

질문하신 상황에서 `java.lang.IllegalStateException: This consumer has already been closed`가 발생한 이유는 다음과 같습니다.

1. **스레드 경합**: 외부 스레드에서 `consumer.close()`를 호출했습니다.
2. **동시 접근**: Consumer 루프를 돌고 있는 메인 스레드는 아직 `while` 문 내부에 있습니다.
3. **종료 후 작업**: 메인 스레드가 다음 루프에서 `poll()`을 호출하려고 할 때, 이미 `close`된 객체이므로 Kafka 클라이언트가 예외를 던집니다.

**핵심**: `close()`는 반드시 **Consumer 루프를 실행 중인 스레드 내에서 마지막에 한 번만 호출**되어야 합니다.

---

## 3. Graceful Shutdown 표준 패턴 (추천)

`wakeup()`을 활용하여 예외 없이 안전하게 종료하는 표준 코드 구조입니다.

```java
public class MyConsumer implements Runnable {
    private final KafkaConsumer<String, String> consumer;
    private final AtomicBoolean closed = new AtomicBoolean(false);

    public void run() {
        try {
            consumer.subscribe(List.of("my-topic"));
            while (!closed.get()) {
                // poll() 수행 중 외부에서 wakeup()이 호출되면 WakeupException이 발생함
                ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(1000));
                for (ConsumerRecord<String, String> record : records) {
                    process(record);
                }
            }
        } catch (WakeupException e) {
            // 종료 과정이므로 무시해도 됨
            if (!closed.get()) throw e;
        } finally {
            // 실제 리소스 정리는 여기서 수행 (메인 스레드)
            consumer.close();
        }
    }

    // 외부 스레드(예: 런타임 셧다운 훅)에서 호출하는 메서드
    public void shutdown() {
        closed.set(true);
        // poll() 상태에 있는 Consumer를 깨워 WakeupException을 유발함
        consumer.wakeup(); 
    }
}
```

### 동작 원리

1. 외부에서 `shutdown()`을 호출하면 `wakeup()`이 실행됩니다.
2. 차단되어 있던 `poll()` 메서드가 즉시 `WakeupException`을 던지며 중단됩니다.
3. `catch` 블록을 거쳐 `finally`로 이동합니다.
4. 루프를 실행하던 스레드가 직접 `close()`를 호출하므로 **동시성 이슈 없이** 깔끔하게 종료됩니다.

---

## 4. 요약

* **외부 스레드**에서는 오직 **`wakeup()`**만 호출하세요.
* **Consumer 실행 스레드**에서 `WakeupException`을 잡고 **`close()`**를 호출하세요.
* 이렇게 하면 "이미 종료된 Consumer"라는 에러 없이 안전하게 오프셋을 커밋하고 종료할 수 있습니다.
