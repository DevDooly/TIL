# Java 21: Next-Gen Concurrency and Performance

Java 21은 2023년에 출시된 최신 **LTS** 버전으로, **Virtual Threads**를 필두로 한 동시성 처리의 패러다임 변화를 가져왔습니다.

## 1. Virtual Threads (가상 스레드)

Project Loom의 결과물로, Java 21의 가장 핵심적인 기능입니다. 운영체제의 스레드(OS Thread)와 1:1로 매핑되지 않는 **경량 스레드**입니다.

- **특징:** 수백만 개의 스레드를 적은 리소스로 동시에 생성하고 관리할 수 있습니다.
- **효과:** 전통적인 Thread-per-request 모델에서도 비동기 프로그래밍(Reactive) 수준의 높은 처리량(Throughput)을 달성할 수 있습니다.

```java
// 가상 스레드 생성 예시
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    IntStream.range(0, 10_000).forEach(i -> {
        executor.submit(() -> {
            Thread.sleep(Duration.ofSeconds(1));
            return i;
        });
    });
} // executor.close()가 호출될 때 모든 작업 완료 대기
```

---

## 2. Sequenced Collections

컬렉션 프레임워크에 순서(Order)를 명확히 정의하는 인터페이스가 추가되었습니다. 첫 번째 요소와 마지막 요소에 대한 접근이 일관되게 개선되었습니다.

- **SequencedCollection**, **SequencedSet**, **SequencedMap**
- `addFirst()`, `addLast()`, `getFirst()`, `getLast()`, `reversed()` 등의 메서드 제공

```java
List<String> list = new ArrayList<>(List.of("A", "B", "C"));
list.addFirst("Z"); // [Z, A, B, C]
list.getLast();     // "C"
```

---

## 3. Record Patterns

`instanceof`나 `switch` 문에서 Record의 내부 필드를 즉시 추출하여 사용할 수 있는 패턴 매칭 기능이 강화되었습니다.

```java
public record Point(int x, int y) { }

if (obj instanceof Point(int x, int y)) {
    System.out.println(x + y);
}
```

---

## 4. Scoped Values & Structured Concurrency (Preview)

- **Scoped Values:** 스레드 간에 데이터를 안전하고 효율적으로 공유하기 위한 도구로, `ThreadLocal`의 대안으로 개발되고 있습니다.
- **Structured Concurrency:** 여러 개의 하위 작업을 하나의 작업 단위로 묶어 관리하여 에러 처리 및 취소를 용이하게 합니다.

---

## 5. String Templates (Preview)

문자열 안에 변수나 표현식을 직접 삽입할 수 있는 기능입니다. (Java 21에서는 Preview 단계)

```java
String name = "Rudy";
String message = STR."Hello, \{name}!"; // STR 템플릿 프로세서 사용
```
