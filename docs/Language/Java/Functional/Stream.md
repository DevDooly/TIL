# Stream API

**Stream API**는 데이터 소스(컬렉션, 배열 등)를 추상화하여 데이터를 다루는데 자주 사용되는 연산(검색, 필터링, 변환, 정렬 등)을 정의해 놓은 것입니다.

## 💡 특징
- **선언형 코드:** "어떻게(How)"가 아니라 **"무엇을(What)"** 할지에 집중합니다.
- **원본 데이터 불변:** 스트림은 원본 데이터를 변경하지 않습니다.
- **일회용:** 스트림은 한 번 사용하면 닫혀서 다시 사용할 수 없습니다.
- **지연 연산 (Lazy Evaluation):** 최종 연산이 호출되기 전까지는 중간 연산이 실행되지 않습니다.

---

## 1. 스트림 생성 (Creation)

```java
// 컬렉션에서 생성
List<String> list = Arrays.asList("a", "b", "c");
Stream<String> stream = list.stream();

// 배열에서 생성
String[] arr = {"a", "b", "c"};
Stream<String> stream = Arrays.stream(arr);

// 직접 생성
Stream<Integer> stream = Stream.of(1, 2, 3);
```

---

## 2. 중간 연산 (Intermediate Operations)

스트림을 변환하며, 또 다른 스트림을 반환합니다. 여러 번 연결(Chaining)할 수 있습니다.

### Filter (필터링)
조건(`Predicate`)에 맞는 요소만 걸러냅니다.

```java
stream.filter(s -> s.startsWith("a")); // "a"로 시작하는 요소만 남김
```

### Map (변환)
각 요소를 변환(`Function`)하여 새로운 값을 만듭니다.

```java
stream.map(String::toUpperCase); // 모든 문자열을 대문자로 변환
// "a" -> "A"
```

### Sorted (정렬)
요소를 정렬합니다.

```java
stream.sorted(); // 기본 정렬 (오름차순)
stream.sorted(Comparator.reverseOrder()); // 내림차순 정렬
stream.sorted((a, b) -> a.length() - b.length()); // 길이순 정렬
```

### Distinct (중복 제거)
중복된 요소를 제거합니다.

```java
stream.distinct();
```

### Peek (조회)
요소를 소비하지 않고 엿봅니다. 주로 디버깅용으로 사용됩니다.

```java
stream.peek(System.out::println);
```

---

## 3. 최종 연산 (Terminal Operations)

스트림의 요소를 소모하며 결과를 반환합니다. 이 연산 후에는 스트림이 닫힙니다.

### forEach (순회)
각 요소를 소비합니다.

```java
stream.forEach(System.out::println);
```

### collect (수집)
요소들을 리스트, 셋, 맵 등으로 수집합니다.

```java
List<String> result = stream.collect(Collectors.toList());
String joined = stream.collect(Collectors.joining(", "));
```

### count, min, max (통계)

```java
long count = stream.count();
Optional<Integer> max = intStream.max();
```

### reduce (누적)
요소들을 하나로 줄여가며(Reduction) 연산합니다.

```java
// 1부터 n까지 합계
int sum = intStream.reduce(0, (a, b) -> a + b);
```

### anyMatch, allMatch, noneMatch (매칭)

```java
boolean hasEven = intStream.anyMatch(n -> n % 2 == 0); // 하나라도 짝수면 true
```

---

## 🚀 실전 예제

```java
List<User> users = Arrays.asList(
    new User("Alice", 30),
    new User("Bob", 20),
    new User("Charlie", 25),
    new User("David", 30)
);

// 25세 이상인 사용자의 이름을 대문자로 변환하여 이름순으로 정렬한 리스트
List<String> result = users.stream()
    .filter(u -> u.getAge() >= 25)
    .map(u -> u.getName().toUpperCase())
    .sorted()
    .collect(Collectors.toList());

// 결과: ["ALICE", "CHARLIE", "DAVID"]
```
