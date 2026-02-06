# Lambda Expressions (람다 표현식)

람다 표현식은 메서드를 하나의 식(Expression)으로 표현한 것입니다. 익명 클래스(Anonymous Class)의 지루한 보일러플레이트 코드를 줄이고, 코드를 간결하게 만듭니다.

## 1. 기본 문법

```java
(parameters) -> expression
// 또는
(parameters) -> { statements; }
```

### 예제 비교

**기존 방식 (익명 클래스):**
```java
Comparator<Integer> comparator = new Comparator<Integer>() {
    @Override
    public int compare(Integer a, Integer b) {
        return a.compareTo(b);
    }
};
```

**람다 표현식:**
```java
Comparator<Integer> comparator = (a, b) -> a.compareTo(b);
```

---

## 2. 주요 함수형 인터페이스 (Functional Interfaces)

`java.util.function` 패키지에는 자주 사용되는 함수형 인터페이스들이 정의되어 있습니다.

| 인터페이스 | 추상 메서드 | 설명 | 예제 |
| :--- | :--- | :--- | :--- |
| **Predicate&lt;T&gt;** | `boolean test(T t)` | 조건을 검사하여 `true`/`false` 반환 | `t -> t > 0` |
| **Consumer&lt;T&gt;** | `void accept(T t)` | 입력을 받아 소비 (반환값 없음) | `t -> System.out.println(t)` |
| **Supplier&lt;T&gt;** | `T get()` | 입력 없이 값을 반환 (공급) | `() -> "Hello"` |
| **Function&lt;T, R&gt;** | `R apply(T t)` | 입력을 받아 다른 타입으로 변환 | `t -> t.length()` |

---

## 3. 메서드 참조 (Method Reference)

람다식이 단순히 다른 메서드를 호출하는 경우, 더 간결하게 표현할 수 있습니다.

```java
// 람다
Consumer<String> printer = s -> System.out.println(s);

// 메서드 참조
Consumer<String> printer = System.out::println;
```

```java
// 람다
Function<String, Integer> parser = s -> Integer.parseInt(s);

// 메서드 참조 (Static 메서드)
Function<String, Integer> parser = Integer::parseInt;
```