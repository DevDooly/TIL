# JDBI와 Virtual Thread: 진단 후 제한된 실행기로 격리하기

JDBI 호출이 오래 걸린다면 먼저 JDBC 드라이버에서 막힌 것인지, 연결 풀에서 기다리는 것인지 구분한다. JDK·드라이버 버전과 스택을 확인해 pinning으로 좁혀졌는데 당장 업그레이드하기 어렵다면, 문제가 생기는 호출을 플랫폼 스레드 실행기로 옮기는 방법이 있다. 아래 예제는 JDK 21 API를 사용한다. [Pinning 진단](../Virtual_Threads_FTP_Pinning.md)

## 무제한 큐를 피하는 예제

`Executors.newFixedThreadPool(n)`은 스레드 수만 제한한다. 대기 큐에는 상한이 없어 DB가 느려지면 요청이 계속 쌓일 수 있다. 아래처럼 큐 크기도 제한해야 실행 슬롯과 큐가 모두 찼을 때 `AbortPolicy`로 추가 요청을 거절할 수 있다. [Executors API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/Executors.html#newFixedThreadPool(int)), [ThreadPoolExecutor API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ThreadPoolExecutor.html)

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

작업 스레드 수는 DB가 감당할 동시 쿼리 수와 다른 코드의 연결 풀 사용량을 함께 보고 정한다. 큐 크기는 허용할 대기 시간과 요청 유입량에 맞춘다. 이 실행기를 거치지 않는 쿼리도 있으므로 DB 전체 부하는 따로 확인해야 한다.

## 거절과 트랜잭션 경계

- `RejectedExecutionException`은 명시적으로 처리한다. HTTP 과부하 응답이나 상위 작업의 지연·재시도 정책에 연결한다.
- `CallerRunsPolicy`는 작업을 제출한 스레드에서 실행한다. 이번처럼 pinning이 생기는 호출을 분리하려는 상황에서는 원래 스레드가 다시 그 호출을 맡게 되므로 적합하지 않을 수 있다.
- JDBI handle·JDBC connection·transaction을 스레드 사이로 넘기지 않는다. worker 안에서 획득하고 처리·정리한다.
- 호출자 스레드의 Spring transaction이 worker에 자동 전파된다고 가정하지 않는다. 여러 SQL을 하나의 원자적 작업으로 실행해야 하면 그 경계 전체를 worker 쪽에 둔다.
- `Future.get(timeout)`은 호출자의 대기를 제한한다. timeout이나 `cancel(true)`만으로 SQL 종료가 보장되지 않으므로 driver/socket/query timeout을 별도로 검토한다.

## 적용 전후 확인

적용 후에는 큐가 얼마나 쌓이는지, 연결을 얻는 데 얼마나 기다리는지부터 본다. 활성 작업 스레드 수, 거절 건수, SQL 지연, JFR pinning 시간도 함께 비교한다. DB가 느려지거나 큐가 가득 찼을 때 요청을 제대로 거절하는지도 확인한다.

`python scripts/tests/test_java_examples.py`는 위 실행기에서 실행 1건·대기 1건이 찬 뒤 추가 작업이 거절되는지 확인한다. 실제 DB/transaction 동작은 서비스 통합 테스트가 필요하다. [FetchSize와 스트리밍](../../../Data/Database/JDBI_FetchSize_and_VirtualThreads.md)
