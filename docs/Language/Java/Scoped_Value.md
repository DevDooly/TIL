# Java: Scoped Value - 가상 스레드 시대를 위한 새로운 데이터 공유 메커니즘

**Scoped Value**는 Java 21에 도입된 기능으로, 스레드 내 또는 자식 스레드 간에 불변(Immutable) 데이터를 효율적으로 공유하기 위한 도구입니다. 기존 `ThreadLocal`의 한계를 극복하고 가상 스레드(Virtual Threads) 환경에 최적화되어 설계되었습니다.

---

## 1. ThreadLocal의 한계와 Scoped Value의 등장 배경

가상 스레드 환경에서 `ThreadLocal`은 다음과 같은 문제를 일으킵니다.

1. **메모리 효율성 저하**: 가상 스레드는 수백만 개가 생성될 수 있습니다. 각 스레드가 자신만의 `ThreadLocal` 복사본을 가지면 메모리 점유율이 급격히 증가합니다.
2. **가변성(Mutability) 위험**: `ThreadLocal.set()`을 통해 누구나 값을 바꿀 수 있어, 복잡한 호출 스택에서 데이터의 출처를 추적하기 어렵습니다.
3. **생명주기 관리 어려움**: `remove()`를 명시적으로 호출하지 않으면 메모리 누수(Memory Leak)가 발생할 위험이 큽니다.
4. **상속 비용**: 자식 스레드에 데이터를 넘길 때(InheritableThreadLocal) 모든 데이터를 복사해야 하므로 비용이 큽니다.

---

## 2. Scoped Value의 핵심 특징

* **불변성(Immutability)**: 한 번 설정된 값은 스코프 내에서 변경할 수 없습니다.
* **한정된 생명주기(Bounded Lifetime)**: 데이터가 유효한 범위(Scope)가 코드 블록으로 명확히 정의됩니다. 블록을 벗어나면 자동으로 데이터가 소멸됩니다.
* **성능 및 메모리 최적화**: 가상 스레드 환경에서 매우 가볍게 동작하며, 자식 스레드와 데이터를 공유할 때 복사가 아닌 참조 방식을 사용하여 비용이 거의 없습니다.

---

## 3. 사용 방법

### 3.1 기본 선언 및 바인딩
`ScopedValue.where()`를 통해 값을 바인딩하고, `run()` 또는 `call()` 블록 내에서만 해당 값을 사용합니다.

```java
public class ContextHolder {
    // 1. ScopedValue 선언
    public final static ScopedValue<User> CURRENT_USER = ScopedValue.newInstance();
}

// 2. 값 바인딩 및 실행
User user = new User("Rudy");
ScopedValue.where(ContextHolder.CURRENT_USER, user)
           .run(() -> {
               // 이 블록 안에서만 값을 읽을 수 있음
               System.out.println("User: " + ContextHolder.CURRENT_USER.get().name());
               executeBusinessLogic();
           });

// 3. 블록을 벗어나면 CURRENT_USER.isBound()는 false가 되며 접근 시 예외 발생
```

### 3.2 자식 스레드와 공유 (Structured Concurrency와 결합)
`StructuredTaskScope`를 사용하면 부모 스레드의 Scoped Value가 자식 가상 스레드들에게 자동으로 상속됩니다.

```java
ScopedValue.where(CURRENT_USER, user).run(() -> {
    try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
        scope.fork(() -> {
            // 자식 가상 스레드에서도 부모의 CURRENT_USER에 접근 가능!
            return callExternalApi(CURRENT_USER.get());
        });
        scope.join().throwIfFailed();
    }
});
```

---

## 4. 가상 스레드에서 언제 쓰면 좋은가?

1. **사용자 인증 정보 전달**: HTTP 요청마다 생성되는 수많은 가상 스레드에 사용자 ID, 권한 등을 전달할 때.
2. **트레이싱 및 로깅 컨텍스트**: 로그 추적을 위한 `traceId` 등을 비즈니스 로직 전반에 전달할 때.
3. **데이터베이스 트랜잭션/테넌트 정보**: 멀티 테넌트 환경에서 현재 요청의 테넌트 ID를 전파할 때.

---

## 5. 요약: ThreadLocal vs Scoped Value

| 구분 | ThreadLocal | Scoped Value |
| :--- | :--- | :--- |
| **데이터 변경** | 가능 (`set()`) | **불가능 (Immutable)** |
| **생명주기** | 명시적 제거 필요 (`remove()`) | **스코프 종료 시 자동 소멸** |
| **상속 비용** | 데이터 복사 (무거움) | **참조 공유 (매우 가벼움)** |
| **가상 스레드 적합성** | 낮음 | **매우 높음** |

---

## 결론
가상 스레드를 적극적으로 사용하는 현대적인 Java 애플리케이션이라면, 전역적인 컨텍스트 공유를 위해 **`Scoped Value`**를 우선적으로 고려해야 합니다. 이는 더 안전하고, 빠르며, 메모리 효율적인 코드를 작성하는 기반이 됩니다.
