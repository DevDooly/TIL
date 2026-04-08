# Java ThreadPoolExecutor와 거부 정책(Rejection Policy)

`ThreadPoolExecutor`는 Java `java.util.concurrent` 패키지의 핵심 클래스로, 스레드 풀을 세밀하게 제어할 수 있는 기능을 제공합니다. `Executors` 팩토리 메서드보다 이 클래스를 직접 사용하는 것이 리소스 관리 측면에서 권장됩니다.

---

## 1. ThreadPoolExecutor의 7가지 파라미터

직접 생성자를 사용할 때 설정하는 핵심 요소들입니다.

1. **corePoolSize**: 풀에 유지할 최소 스레드 수.
2. **maximumPoolSize**: 풀에 허용되는 최대 스레드 수.
3. **keepAliveTime**: 스레드 수가 core보다 많을 때, 유휴 스레드가 종료되기 전 대기하는 시간.
4. **unit**: keepAliveTime의 시간 단위.
5. **workQueue**: 실행 전 대기 중인 작업을 보관하는 큐 (BlockingQueue).
6. **threadFactory**: 새로운 스레드를 생성하는 팩토리 (스레드 이름 지정 등에 사용).
7. **handler**: 큐와 스레드가 모두 가득 찼을 때 실행될 **거부 정책**.

---

## 2. 작업 처리 흐름 (Task Flow)

새로운 작업(Task)이 제출되면 다음 순서로 처리됩니다.

1. **Core Check**: 현재 실행 중인 스레드가 `corePoolSize`보다 적으면, 즉시 새 스레드를 생성하여 작업을 할당합니다.
2. **Queueing**: `corePoolSize`가 가득 찼다면, 작업을 `workQueue`에 넣습니다.
3. **Max Check**: 큐가 가득 찼는데 스레드 수가 `maximumPoolSize`보다 적다면, 새 스레드를 생성하여 작업을 실행합니다.
4. **Rejection**: 큐도 가득 차고 스레드 수도 `maximumPoolSize`에 도달했다면, 지정된 **거부 정책(Handler)**을 실행합니다.

---

## 3. 표준 거부 정책 (RejectedExecutionHandler)

Java는 `ThreadPoolExecutor` 내부 클래스로 4가지 표준 정책을 제공합니다.

### 3.1 AbortPolicy (기본값)

* **동작**: 작업을 거부하고 `RejectedExecutionException` 예외를 던집니다.
* **용도**: 작업 누락을 절대 허용하지 않고, 호출자에게 시스템 과부하를 즉시 알려야 할 때 사용합니다.

### 3.2 CallerRunsPolicy

* **동작**: 작업을 거부하지 않고, **작업을 제출한 스레드(Caller)**에서 직접 작업을 실행합니다.
* **용도**: 작업 처리를 늦추더라도 끝까지 처리해야 할 때, 그리고 자연스럽게 새로운 작업 제출 속도를 늦추는(Back-pressure) 효과가 필요할 때 사용합니다.

### 3.3 DiscardPolicy

* **동작**: 작업을 아무런 예외 없이 조용히 버립니다.
* **용도**: 작업의 중요도가 낮아 일부 유실되어도 시스템에 지장이 없을 때 사용합니다.

### 3.4 DiscardOldestPolicy

* **동작**: 큐의 맨 앞에 있는(가장 오래된) 작업을 버리고, 현재 작업을 다시 시도합니다.
* **용도**: 최신 데이터가 더 중요한 시스템(예: 실시간 상태 업데이트)에서 유용합니다.

---

## 4. 실무 권장 사항

* **Fixed vs Cached**: `Executors.newCachedThreadPool()`은 `maximumPoolSize`가 `Integer.MAX_VALUE`이므로 OOM 위험이 큽니다. 가급적 `ThreadPoolExecutor`를 직접 생성하여 제한을 두는 것이 좋습니다.
* **큐 선택**: `LinkedBlockingQueue`를 사용할 때는 반드시 **용량 제한(Capacity)**을 두어야 합니다. 무제한 큐는 스레드 풀의 거부 정책이 동작하지 않게 만듭니다.
* **모니터링**: `recordStats()`와 같은 기능은 없지만, `getPoolSize()`, `getActiveCount()`, `getQueue().size()` 등을 주기적으로 로그로 남겨 풀의 상태를 관찰해야 합니다.

---

## 5. 요약

`ThreadPoolExecutor`는 단순한 스레드 묶음이 아니라, **작업 대기열과 스레드 생성 로직, 그리고 포화 상태에서의 방어 기제**가 결합된 정교한 엔진입니다. 시스템의 특성에 맞는 적절한 거부 정책 선택이 전체 애플리케이션의 안정성을 결정합니다.
