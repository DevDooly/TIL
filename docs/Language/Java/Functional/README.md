# Java Functional Programming

Java 8부터 도입된 **함수형 프로그래밍(Functional Programming)** 패러다임은 코드를 더 간결하고, 가독성 높으며, 유지보수하기 쉽게 만들어 주었습니다.

이 섹션에서는 Java의 함수형 프로그래밍을 구성하는 핵심 요소들을 다룹니다.

## 🎯 핵심 요소

### 1. [Lambda Expressions (람다 표현식)](Lambda.md)
익명 클래스를 대체하는 간결한 문법으로, 메서드를 하나의 식(Expression)으로 표현합니다.

### 2. [Stream API](Stream.md)
데이터 컬렉션을 선언형으로 처리하는 도구입니다. 반복문 없이 데이터를 필터링, 변환, 집계할 수 있습니다.

### 3. [Optional](Optional.md)
`NullPointerException`을 방지하고, 값이 없는 상황을 명시적으로 처리하는 컨테이너입니다.

### 4. Functional Interfaces
추상 메서드가 하나만 있는 인터페이스로, 람다식의 타겟 타입이 됩니다.

-   `Predicate<T>`: 조건 검사 (boolean 반환)
-   `Function<T, R>`: 입력 -> 출력 변환
-   `Consumer<T>`: 입력 소비 (리턴 없음)
-   `Supplier<T>`: 값 공급 (입력 없음)
