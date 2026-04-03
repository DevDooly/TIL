# Java 8: Modern Java의 시작

Java 8은 2014년에 출시되었지만, Java 역사상 **가장 큰 변화**를 가져온 버전으로 평가받습니다. 함수형 프로그래밍의 개념을 도입하여 코드를 간결하고 직관적으로 만들었으며, 이는 현대적인 Java 개발의 표준이 되었습니다.

## 1. Lambda Expressions (람다 표현식)

익명 클래스(Anonymous Class)를 대체하는 간결한 문법입니다. 함수를 하나의 변수처럼 다룰 수 있게 해줍니다.

**기존 방식 (익명 클래스):**
```java
Runnable runnable = new Runnable() {
    @Override
    public void run() {
        System.out.println("Hello");
    }
};
```

**Java 8 (람다):**
```java
Runnable runnable = () -> System.out.println("Hello");
```

---

## 2. Stream API

컬렉션(List, Set 등)의 데이터를 선언형으로 처리할 수 있는 강력한 도구입니다. 반복문(`for`, `while`) 없이 필터링, 매핑, 집계 작업을 수행할 수 있습니다.

```java
List<String> names = Arrays.asList("Java", "Scala", "Groovy", "Kotlin");

// "J"로 시작하는 이름만 필터링하여 대문자로 변환 후 리스트로 수집
List<String> result = names.stream()
    .filter(name -> name.startsWith("J"))
    .map(String::toUpperCase)
    .collect(Collectors.toList());
```

---

## 3. Optional

`NullPointerException` (NPE)을 방지하기 위해 도입된 Wrapper 클래스입니다. 값이 있을 수도 있고 없을 수도 있는 상황을 명시적으로 표현합니다.

```java
// 기존: null 체크 필요
if (user != null && user.getAddress() != null) { ... }

// Java 8 Optional
Optional.ofNullable(user)
    .map(User::getAddress)
    .ifPresent(address -> System.out.println(address));
```

---

## 4. Date and Time API (JSR 310)

기존의 `java.util.Date`와 `Calendar`의 문제점(불변성 부족, 헷갈리는 월 인덱스 등)을 해결하기 위해 `java.time` 패키지가 새로 추가되었습니다.

- **LocalDate:** 날짜 (예: 2023-10-01)
- **LocalTime:** 시간 (예: 14:30:00)
- **LocalDateTime:** 날짜 + 시간
- **ZonedDateTime:** 타임존 포함

```java
LocalDate today = LocalDate.now();
LocalDate nextWeek = today.plusWeeks(1);
```

---

## 5. Interface Default Methods

인터페이스에도 구현된 메서드(`default` 키워드 사용)를 가질 수 있게 되었습니다. 이를 통해 기존 인터페이스를 깨뜨리지 않고 새로운 기능을 추가할 수 있게 되었습니다. (하위 호환성 유지)

```java
interface Vehicle {
    void drive();
    
    // 구현체를 강제하지 않는 기본 메서드
    default void honk() {
        System.out.println("Honk!");
    }
}
```
