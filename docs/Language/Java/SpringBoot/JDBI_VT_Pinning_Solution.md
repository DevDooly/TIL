# JDBI와 Virtual Thread: 진단 후 제한된 실행기로 격리하기

검증 기준: JDK 21 실행기 API, 2026-09-07.

JDBI를 쓴다는 사실만으로 pinning이 발생하는 것은 아니다. JDK·JDBC driver 버전, 실제 stack, connection pool 대기를 확인한다. 구형 JDK에서 문제가 확인되고 driver/JDK 업그레이드가 당장 어렵다면 해당 blocking 경로를 플랫폼 스레드 실행기로 격리할 수 있다. [Pinning 진단](../Virtual_Threads_FTP_Pinning.md)

## 무제한 큐를 피하는 예제

`Executors.newFixedThreadPool(n)`은 작업 스레드 수만 제한하고 큐는 무제한이다. 이 상태에서 `AbortPolicy`를 설명하며 “요청이 많으면 즉시 거절”된다고 하면 잘못된 안내다. 실행 수와 대기 수를 각각 제한한다. [Executors API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/Executors.html#newFixedThreadPool(int)), [ThreadPoolExecutor API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ThreadPoolExecutor.html)

```java
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

public final class BoundedDbExecutor {
    private BoundedDbExecutor() {}

    public static ThreadPoolExecutor create(int workers, int queueCapacity) {
        if (workers <= 0 || queueCapacity <= 0) {
            throw new IllegalArgumentException("workers and queueCapacity must be positive");
        }
        return new ThreadPoolExecutor(
                workers, workers, 0L, TimeUnit.MILLISECONDS,
                new ArrayBlockingQueue<>(queueCapacity),
                Thread.ofPlatform().name("db-worker-", 0).factory(),
                new ThreadPoolExecutor.AbortPolicy());
    }
}
```

실행기는 요청마다 만들지 않고 서비스 수명 동안 재사용한다. 종료 시 새로운 요청을 차단하고 shutdown·대기·미완료 작업 처리를 수행한다. JDK 21의 `ExecutorService.close()`는 완료를 기다리므로 종료 시간 제한이 필요한 서버에서는 별도 종료 정책을 둔다.

worker 수는 DB가 허용하는 동시 쿼리와 다른 소비자의 connection pool 사용량을 고려한다. 큐 크기는 허용 대기 시간과 유입량을 측정해 정한다. 풀을 추가했다고 DB 전체 부하가 자동으로 제한되지는 않는다.

## 거절과 트랜잭션 경계

- `RejectedExecutionException`은 명시적으로 처리한다. HTTP 과부하 응답이나 상위 작업의 지연·재시도 정책에 연결한다.
- `CallerRunsPolicy`는 제출한 스레드에서 작업을 실행한다. 확인된 pinning 경로를 격리하려는 경우 그 목적을 깨뜨릴 수 있다. 모든 시스템에서 금지되는 정책이라는 뜻은 아니다.
- JDBI handle·JDBC connection·transaction을 스레드 사이로 넘기지 않는다. worker 안에서 획득하고 처리·정리한다.
- 호출자 스레드의 Spring transaction이 worker에 자동 전파된다고 가정하지 않는다. 여러 SQL을 하나의 원자적 작업으로 실행해야 하면 그 경계 전체를 worker 쪽에 둔다.
- `Future.get(timeout)`은 호출자의 대기를 제한한다. timeout이나 `cancel(true)`만으로 SQL 종료가 보장되지 않으므로 driver/socket/query timeout을 별도로 검토한다.

## 적용 전후 확인

queue 길이와 대기 시간, active worker, 거절 건수, connection 획득 시간, SQL 지연, JFR pinning 시간을 비교한다. DB가 느린 상황과 포화 상태도 재현한다.

`python scripts/tests/test_java_examples.py`는 위 실행기에서 실행 1건·대기 1건이 찬 뒤 추가 작업이 거절되는지 확인한다. 실제 DB/transaction 동작은 서비스 통합 테스트가 필요하다. [FetchSize와 스트리밍](../../../Data/Database/JDBI_FetchSize_and_VirtualThreads.md)
