# Functional Interfaces (함수형 인터페이스)

함수형 인터페이스는 **추상 메서드가 오직 하나인 인터페이스**를 말합니다. Java 8의 람다 표현식(Lambda Expression)은 바로 이 함수형 인터페이스의 인스턴스를 생성하는 식입니다.

## 1. @FunctionalInterface

인터페이스 선언 시 `@FunctionalInterface` 어노테이션을 붙이면, 컴파일러가 해당 인터페이스가 함수형 인터페이스의 조건(단 하나의 추상 메서드)을 만족하는지 검사합니다. 필수는 아니지만, 실수를 방지하기 위해 권장됩니다.

```java
@FunctionalInterface
public interface MyFunctionalInterface {
    void doSomething();
    // void anotherMethod(); // 주석 해제 시 컴파일 에러 발생 (추상 메서드가 2개가 되므로)
    
    // default 메서드나 static 메서드는 개수 제한이 없습니다.
    default void print() { System.out.println("Default Method"); }
}
```

---

## 2. java.util.function 패키지

Java에서는 자주 사용되는 함수형 인터페이스를 표준 라이브러리로 제공합니다.

### 2.1 Predicate\<T\>
- **설명:** 입력을 받아 조건을 검사하고 `boolean`을 반환합니다.
- **메서드:** `boolean test(T t)`

```java
Predicate<String> isEmpty = s -> s.isEmpty();
System.out.println(isEmpty.test("")); // true
```

### 2.2 Consumer\<T\>
- **설명:** 입력을 받아서 소비하고, 반환값은 없습니다. (Side-effect 발생)
- **메서드:** `void accept(T t)`

```java
Consumer<String> printer = s -> System.out.println(s);
printer.accept("Hello"); // Hello 출력
```

### 2.3 Supplier\<T\>
- **설명:** 입력 없이 값을 반환(공급)합니다. Lazy Evaluation에 자주 사용됩니다.
- **메서드:** `T get()`

```java
Supplier<Double> random = () -> Math.random();
System.out.println(random.get());
```

### 2.4 Function\<T, R\>
- **설명:** 입력(T)을 받아 출력(R)으로 매핑(변환)합니다.
- **메서드:** `R apply(T t)`

```java
Function<String, Integer> lengthMapper = s -> s.length();
System.out.println(lengthMapper.apply("Java")); // 4
```

---

## 3. 그 외 다양한 인터페이스

### Operator (연산자)
`Function`의 특수한 형태로, 입력과 출력의 타입이 동일한 경우입니다.
- **UnaryOperator\<T\>:** `T -> T` (단항 연산)
- **BinaryOperator\<T\>:** `(T, T) -> T` (이항 연산)

```java
UnaryOperator<Integer> square = n -> n * n;
```

### Two-Arity (인자가 2개인 경우)
접두사 `Bi`가 붙습니다.
- **BiPredicate\<T, U\>:** `(T, U) -> boolean`
- **BiConsumer\<T, U\>:** `(T, U) -> void`
- **BiFunction\<T, U, R\>:** `(T, U) -> R`

```java
BiFunction<Integer, Integer, Integer> add = (a, b) -> a + b;
```

### Primitive Specializations (기본형 특화)
박싱/언박싱 오버헤드를 줄이기 위해 기본형(int, long, double)을 직접 다루는 인터페이스들입니다.
- `IntPredicate`, `LongConsumer`, `DoubleFunction` 등

```java
IntPredicate isEven = i -> i % 2 == 0; // Integer 객체 생성 없음
```
