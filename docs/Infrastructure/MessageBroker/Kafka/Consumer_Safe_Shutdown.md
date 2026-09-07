# Kafka Consumer: wakeup과 close, 처리 완료 offset

기준: Kafka Java client 3.9, 2026-09-07.

`KafkaConsumer`는 thread-safe하지 않다. 한 소유 스레드에서 subscribe·poll·commit·close를 수행하고, 외부 스레드는 종료 플래그와 `wakeup()`으로 종료를 요청하는 구조가 단순하다. [KafkaConsumer API](https://kafka.apache.org/39/javadoc/org/apache/kafka/clients/consumer/KafkaConsumer.html)

| API | 의미 |
| :--- | :--- |
| `wakeup()` | 외부 스레드에서 호출 가능. 현재 또는 다음 wakeup 가능한 작업이 `WakeupException`을 던지게 함 |
| `close()` | 자원 정리. 동시 접근을 피해야 하며 wakeup으로 close를 중단할 수 없음 |
| `commitSync()` | offset 저장. 애플리케이션의 처리 성공 범위를 기준으로 호출 |

`wakeup()`은 실행 중인 업무 처리나 SQL을 취소하지 않는다. `close()`의 자동 커밋도 `enable.auto.commit` 설정에 의존한다.

## 동기 배치 처리 예제

생성한 consumer에 **`enable.auto.commit=false`를 설정**하고 전달한다. handler는 레코드 처리가 완료된 뒤 반환해야 한다. 이 Runnable은 한 번만 실행한다.

```java
import java.time.Duration;
import java.util.Collection;
import java.util.List;
import java.util.concurrent.atomic.AtomicBoolean;
import org.apache.kafka.clients.consumer.Consumer;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.common.errors.WakeupException;

public final class ConsumerLoop implements Runnable {
    private final Consumer<String, String> consumer;
    private final List<String> topics;
    private final java.util.function.Consumer<ConsumerRecord<String, String>> handler;
    private final AtomicBoolean stopping = new AtomicBoolean();

    public ConsumerLoop(Consumer<String, String> consumer,
                        Collection<String> topics,
                        java.util.function.Consumer<ConsumerRecord<String, String>> handler) {
        this.consumer = consumer;
        this.topics = List.copyOf(topics);
        this.handler = handler;
    }

    @Override
    public void run() {
        try {
            consumer.subscribe(topics);
            while (!stopping.get()) {
                var records = consumer.poll(Duration.ofSeconds(1));
                for (var record : records) {
                    handler.accept(record);
                }
                if (!records.isEmpty()) {
                    consumer.commitSync();
                }
            }
        } catch (WakeupException e) {
            if (!stopping.get()) {
                throw e;
            }
        } finally {
            consumer.close(Duration.ofSeconds(10));
        }
    }

    public void shutdown() {
        if (stopping.compareAndSet(false, true)) {
            consumer.wakeup();
        }
    }
}
```

이 예제는 한 poll 배치를 동기 처리하고 커밋한다. 처리 실패나 커밋 중 wakeup·재균형이 발생하면 성공한 작업도 재전달될 수 있으므로, DB 갱신이나 외부 호출에 중복 처리 대책이 필요하다. 종료 신호만으로 마지막 offset 저장을 보장하지 않는다.

## 종료와 병렬 처리의 경계

종료 요청 후 소유 스레드의 종료를 `join` 등으로 기다린다. 애플리케이션의 최대 처리 시간과 close 시간을 고려해 Kubernetes의 종료 유예 시간을 정한다. handler와 외부 I/O에도 timeout을 둔다.

가상 스레드 등으로 처리를 넘긴 뒤 즉시 commit하면 아직 끝나지 않은 레코드까지 커밋할 수 있다. 병렬 처리에는 다음 설계가 추가로 필요하다.

- 파티션별 완료 offset과 연속으로 완료된 구간 추적
- 동일 파티션 처리 순서와 실패 시 재처리
- 제한된 in-flight 작업 수와 pause/resume
- revoke·종료 시 대기 중 작업 정리와 커밋 범위
- `max.poll.interval.ms`와 실제 처리 시간의 관계

이 항목은 위 동기 예제에 구현되어 있지 않다. [Consumer와 스레딩 모델](https://kafka.apache.org/39/javadoc/org/apache/kafka/clients/consumer/KafkaConsumer.html)
