# Java 25: Enhanced Stability and Modern Productivity

Java 25은 2025년 9월에 출시된 최신 **LTS(Long-Term Support)** 버전입니다. Java 21 이후의 혁신들을 안정화하고, 개발자 생산성과 런타임 효율성을 높이는 기능들이 대거 포함되었습니다.

---

## 1. Scoped Values (Final)

`ThreadLocal`의 대안으로 도입된 Scoped Values가 정식 기능으로 채택되었습니다.

- **특징:** 데이터가 불변(Immutable)이며, 특정 스코프 내에서만 유효합니다.
- **이점:** 가상 스레드(Virtual Threads) 환경에서 수천 수만 개의 스레드가 데이터를 공유할 때 메모리 효율성과 안정성이 `ThreadLocal`보다 압도적으로 뛰어납니다.

```java
private final static ScopedValue<String> USER = ScopedValue.newInstance();

ScopedValue.where(USER, "Rudy").run(() -> {
    // 이 블록 안에서만 USER.get() 가능
    System.out.println(USER.get()); 
});
```

---

## 2. Flexible Constructor Bodies (Final)

생성자 본문에서 `super(...)`나 `this(...)` 호출 전에도 코드를 작성할 수 있게 되었습니다.

- **특징:** 부모 클래스의 생성자를 호출하기 전, 인자를 계산하거나 검증하는 로직을 자유롭게 넣을 수 있습니다.
- **제한:** `super()` 호출 전에는 인스턴스 필드에 접근할 수 없습니다.

```java
public class Child extends Parent {
    public Child(int value) {
        int processed = validate(value); // super() 호출 전 로직 가능
        super(processed);
    }
}
```

---

## 3. Compact Object Headers (Final)

64비트 아키텍처에서 Java 객체의 헤더 크기를 대폭 줄였습니다.

- **효과:** 객체당 메모리 점유율이 줄어들어 전체적인 힙(Heap) 메모리 사용량이 감소하며, 데이터 지역성(Data Locality)이 개선되어 성능이 향상됩니다.
- **대상:** 대규모 객체를 다루는 애플리케이션에서 특히 큰 효과를 볼 수 있습니다.

---

## 4. Module Import Declarations (Final)

모듈 전체를 한 번에 임포트하여 중복되는 `import` 문을 획기적으로 줄일 수 있습니다.

```java
import module java.base; // java.base 모듈의 모든 공개 클래스 사용 가능

public class Main {
    public static void main(String[] args) {
        List<String> list = new ArrayList<>(); // java.util.List 등 자동 포함
    }
}
```

---

## 5. Structured Concurrency (Final/Stable)

여러 비동기 작업을 하나의 논리적인 작업 단위로 묶어 관리하는 구조적 동시성이 안정화되었습니다.

- **특징:** 하위 작업 중 하나가 실패하면 다른 작업들을 자동으로 취소하고 리소스를 정리합니다.
- **효과:** 멀티스레드 코드의 가독성, 유지보수성, 에러 처리가 비약적으로 개선됩니다.

---

## 6. 기타 주요 변경 사항

- **Primitive Types in Patterns**: `instanceof`나 `switch`에서 기본 타입(int, double 등)에 대한 패턴 매칭 지원.
- **Generational Shenandoah**: Shenandoah GC에 세대별(Generational) 관리 기능이 추가되어 효율 개선.
- **32-bit x86 Port 제거**: 레거시 아키텍처 지원을 종료하고 현대적 시스템에 집중.

---

## 요약
Java 25은 **가상 스레드 환경의 완성(Scoped Values, Structured Concurrency)**과 **언어적 현대화(Flexible Constructor, Module Import)**를 통해 Java 21보다 더 강력하고 안정적인 개발 환경을 제공하는 LTS 버전입니다.
