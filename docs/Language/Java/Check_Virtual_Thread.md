# Java/Spring Boot: 현재 스레드가 가상 스레드인지 확인하는 방법

Java 21의 Project Loom 도입 이후, 현재 실행 컨텍스트가 가상 스레드(Virtual Thread)인지 플랫폼 스레드(Platform Thread)인지 구분해야 할 상황이 생깁니다. 이를 확인하는 표준 방법과 실무 예제를 정리합니다.

---

## 1. Java 표준 API 활용 (`Thread.isVirtual()`)

Java 19(Preview)부터 `Thread` 클래스에 추가된 **`isVirtual()`** 메서드를 사용하는 것이 가장 정확하고 표준적인 방법입니다.

```java
public void checkThreadType() {
    Thread currentThread = Thread.currentThread();
    
    if (currentThread.isVirtual()) {
        System.out.println("🚀 현재 가상 스레드(Virtual Thread)에서 동작 중입니다.");
    } else {
        System.out.println("💻 현재 플랫폼 스레드(Platform Thread)에서 동작 중입니다.");
    }
}
```

---

## 2. Spring Boot 활용 예제

Spring Boot 3.2+ 환경에서 가상 스레드를 활성화(`spring.threads.virtual.enabled=true`)했을 때, 실제 서비스 로직에서 이를 검증하는 예제입니다.

### 2.1 컨트롤러 예제
```java
@RestController
@Slf4j
public class ThreadCheckController {

    @GetMapping("/check-thread")
    public String check() {
        boolean isVirtual = Thread.currentThread().isVirtual();
        String threadName = Thread.currentThread().toString();
        
        log.info("Is Virtual: {}, Thread Info: {}", isVirtual, threadName);
        
        return String.format("Virtual Thread: %b, Details: %s", isVirtual, threadName);
    }
}
```

---

## 3. 로그를 통한 확인 (Logback 설정)

코드 수정 없이 로그 패턴 설정만으로도 스레드 타입을 쉽게 파악할 수 있습니다.

* **플랫폼 스레드**: 보통 이름이 `http-nio-8080-exec-1` 처럼 출력됩니다.
* **가상 스레드**: 이름에 보통 `VirtualThread`가 포함되거나, 가상 스레드 식별자가 출력됩니다.

**추천 Logback 패턴**:
```xml
<pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
```

* 가상 스레드 활성화 시 로그 예시: `[VirtualThread[#123]/runnable@ForkJoinPool-1-worker-1]`

---

## 4. 실무 활용 팁

가상 스레드 여부를 확인하는 로직은 다음과 같은 상황에서 유용합니다.

1. **Pinning 방지**: 가상 스레드에서만 특정 라이브러리(synchronized 블록이 많은 레거시 등)를 피해야 할 때.
2. **ThreadLocal 사용 주의**: 가상 스레드는 생성 비용이 싸지만 매우 많이 생성될 수 있으므로, 거대한 `ThreadLocal` 객체를 사용하는지 체크할 때.
3. **디버깅**: 특정 비동기 작업이 의도한 대로 가상 스레드 풀에서 실행되고 있는지 검증할 때.

---

## 5. 요약
현재 스레드 타입을 확인하려면 **`Thread.currentThread().isVirtual()`** 한 줄이면 충분합니다. 이는 런타임에 가장 확실하게 스레드 성격을 파악할 수 있는 도구입니다.
