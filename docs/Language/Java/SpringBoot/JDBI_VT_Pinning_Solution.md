# JDBI & 가상 스레드: Pinning 이슈 해결을 위한 하이브리드 모델

Java 21의 가상 스레드(Virtual Thread) 환경에서 JDBI(JDBC)를 사용할 때, 드라이버 내부의 `synchronized` 블록으로 인해 캐리어 스레드가 차단되는 Pinning 현상을 방지하고 효율적으로 자원을 사용하는 최적의 패턴을 정리합니다.

---

## 1. 이슈의 핵심: 왜 플랫폼 스레드를 섞어 쓰는가?

* **문제**: 많은 JDBC 드라이버(Oracle, MySQL 등) 내부에는 여전히 `synchronized` 블록이 존재합니다. 가상 스레드가 이 블록 안에서 DB I/O를 기다리면 캐리어 스레드(Platform Thread)가 점유되어 다른 가상 스레드들이 멈추는 **Pinning**이 발생합니다.
* **해결 전략**: 
    * **가상 스레드**: 높은 동시성이 필요한 비즈니스 로직 및 가벼운 I/O 처리.
    * **플랫폼 스레드 (Dedicated Pool)**: 실제 무거운 DB Blocking I/O가 발생하는 JDBI 호출부 담당.

---

## 2. 하이브리드 모델 구현 예제

### 2.1 JDBI DAO 정의
```java
public interface UserRepo {
    @SqlQuery("SELECT * FROM users WHERE id = :id")
    User findById(@Bind("id") Long id);
}
```

### 2.2 서비스 계층 (혼용 모델)
플랫폼 스레드 풀을 별도로 두고, 가상 스레드에서 이를 호출하여 결과를 기다리는 방식입니다.

```java
@Service
public class UserService {
    private final UserRepo userRepo;
    private final ExecutorService dbExecutor; // 플랫폼 스레드 풀 (DB 전용)

    public UserService(UserRepo userRepo) {
        this.userRepo = userRepo;
        // DB 작업을 위한 고정된 플랫폼 스레드 풀 생성
        this.dbExecutor = Executors.newFixedThreadPool(50); 
    }

    public void handleRequest(Long userId) {
        // 1. 가상 스레드에서 비즈니스 로직 시작
        Thread.startVirtualThread(() -> {
            log.info("비즈니스 로직 시작 (가상 스레드)");

            // 2. [Blocking I/O 구간] 플랫폼 스레드 풀로 위임하여 Pinning 방지
            User user = CompletableFuture.supplyAsync(() -> {
                log.info("DB 조회 중 (플랫폼 스레드)");
                return userRepo.findById(userId);
            }, dbExecutor).join(); // 가상 스레드는 여기서 Block 되지만 캐리어를 반납함

            // 3. 다시 가상 스레드에서 결과 처리
            processUser(user);
            log.info("요청 처리 완료 (가상 스레드)");
        });
    }

    private void processUser(User user) {
        // 순수 CPU 로직이나 추가적인 비압착 I/O 처리
    }
}
```

---

## 3. 주의사항: 거부 정책(Rejection Policy) 선택

플랫폼 스레드 풀을 생성할 때 `RejectedExecutionHandler` 설정을 주의해야 합니다.

* **AbortPolicy (추천)**: 풀이 가득 차면 예외를 발생시킵니다. 가상 스레드의 Pinning을 확실히 방지할 수 있습니다.
* **CallerRunsPolicy (절대 금지)**: 풀이 가득 찼을 때 작업을 요청한 스레드가 직접 실행하게 하는 정책입니다. 가상 스레드 환경에서 이 정책을 쓰면 **가상 스레드가 직접 DB Blocking I/O를 수행하게 되어 Pinning 현상이 발생**합니다. 오프로딩의 목적이 사라지므로 절대 사용해서는 안 됩니다.

---

## 4. 작동 원리 및 이점

1. **캐리어 스레드 보호**: 가상 스레드에서 `CompletableFuture.join()`이나 `get()`을 호출하여 대기할 때, 가상 스레드 스케줄러는 현재 캐리어 스레드를 다른 가상 스레드가 쓸 수 있도록 **Unmount** 시킵니다.
2. **Pinning 회피**: 실제 `synchronized`가 걸릴 수 있는 JDBI 호출은 미리 정의된 **플랫폼 스레드 풀(`dbExecutor`)**에서 실행되므로, 가상 스레드의 캐리어 스레드 풀(ForkJoinPool)은 Pinning의 영향을 받지 않습니다.
3. **안정적인 커넥션 관리**: DB 커넥션 풀(HikariCP 등)의 크기에 맞춰 플랫폼 스레드 풀을 설정함으로써, 과도한 DB 요청으로 인한 리소스 고갈을 방지하는 **스로틀링(Throttling)** 효과를 얻습니다.

---

## 4. 요약

| 구성 요소 | 역할 | 스레드 타입 |
| :--- | :--- | :--- |
| **Request Handler** | 요청 접수 및 로직 흐름 제어 | **가상 스레드** |
| **JDBI Repository** | 실제 DB 쿼리 실행 (Blocking) | **플랫폼 스레드 (Managed Pool)** |
| **Business Logic** | 데이터 가공 및 계산 | **가상 스레드** |

이 모델을 사용하면 가상 스레드의 높은 확장성을 누리면서도, 레거시 JDBC 드라이버의 Pinning 위험으로부터 시스템을 안전하게 보호할 수 있습니다.
