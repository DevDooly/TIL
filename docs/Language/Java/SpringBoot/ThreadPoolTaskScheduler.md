# ThreadPoolTaskScheduler: Spring 작업 예약 및 스레드 풀 관리

`ThreadPoolTaskScheduler`는 Spring 환경에서 주기적인 작업이나 특정 시간에 실행되어야 하는 작업을 관리하기 위한 스레드 풀 기반의 스케줄러입니다.

---

## 1. 핵심 특징

*   **인터페이스 구현**: Spring의 `TaskScheduler`와 `TaskExecutor` 인터페이스를 모두 구현합니다. 즉, 작업을 즉시 실행할 수도 있고 예약 실행할 수도 있습니다.
*   **표준 기술 기반**: 내부적으로 Java의 `ScheduledThreadPoolExecutor`를 사용합니다.
*   **Spring 통합**: 빈(Bean)으로 등록하여 사용 시 Spring의 생명주기에 맞춰 안전하게 종료(Shutdown)되며, 에러 핸들러(`ErrorHandler`) 설정이 용이합니다.

---

## 2. ThreadPoolTaskExecutor vs ThreadPoolTaskScheduler

많은 개발자가 혼동하는 두 클래스의 차이점입니다.

| 구분 | ThreadPoolTaskExecutor | ThreadPoolTaskScheduler |
| :--- | :--- | :--- |
| **주 목적** | 대량의 비동기 작업 처리 (Execution) | 정해진 시간/주기에 따른 작업 처리 (Scheduling) |
| **기반 클래스** | `ThreadPoolExecutor` | `ScheduledThreadPoolExecutor` |
| **주요 활용** | `@Async`, 병렬 처리 | `@Scheduled`, 예약 작업, 지연 실행 |

---

## 3. 설정 및 사용 방법 (Java Config)

Spring Boot에서 커스텀 스케줄러 풀을 설정하는 예시입니다.

```java
@Configuration
@EnableScheduling
public class SchedulerConfig {

    @Bean
    public ThreadPoolTaskScheduler taskScheduler() {
        ThreadPoolTaskScheduler scheduler = new ThreadPoolTaskScheduler();
        
        scheduler.setPoolSize(5); // 스레드 풀 사이즈 설정
        scheduler.setThreadNamePrefix("my-scheduler-");
        scheduler.setErrorHandler(t -> {
            // 스케줄링 작업 중 발생한 예러 처리 로직
            System.err.println("Scheduled task error: " + t.getMessage());
        });
        scheduler.setWaitForTasksToCompleteOnShutdown(true); // 종료 시 작업 완료 대기
        scheduler.setAwaitTerminationSeconds(60);
        
        scheduler.initialize();
        return scheduler;
    }
}
```

---

## 4. 주요 메서드 활용

빈으로 주입받아 프로그래밍 방식으로 스케줄링을 제어할 수 있습니다.

### 4.1 Fixed Rate (고정 주기 실행)
작업 시작 시점부터 일정 간격으로 실행합니다.
```java
taskScheduler.scheduleAtFixedRate(() -> {
    // 비즈니스 로직
}, Duration.ofMinutes(1));
```

### 4.2 Fixed Delay (고정 지연 실행)
이전 작업이 끝난 시점부터 일정 시간 뒤에 실행합니다.
```java
taskScheduler.scheduleWithFixedDelay(() -> {
    // 비즈니스 로직
}, Duration.ofSeconds(30));
```

### 4.3 Cron Expression (크론 표현식)
```java
taskScheduler.schedule(() -> {
    // 매일 새벽 2시에 실행
}, new CronTrigger("0 0 2 * * *"));
```

---

## 5. 주의 사항 및 팁

1.   **기본 설정의 한계**: Spring Boot에서 별도 설정 없이 `@Scheduled`를 사용하면 단일 스레드(`poolSize=1`)에서 동작합니다. 작업이 많을 경우 반드시 `ThreadPoolTaskScheduler`를 빈으로 등록하여 풀 사이즈를 조정해야 합니다.
2.   **예외 처리**: 스케줄링 작업 내부에서 예외가 발생하여 밖으로 던져지면, 해당 작업의 다음 주기가 실행되지 않을 수 있습니다. 반드시 `try-catch`로 감싸거나 `ErrorHandler`를 설정하세요.
3.   **가상 스레드 결합**: Java 21 이상이라면 `setThreadFactory`를 통해 가상 스레드(Virtual Threads)를 스케줄러에 적용하여 리소스를 더 효율적으로 관리할 수도 있습니다.
