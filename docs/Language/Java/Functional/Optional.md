# Optional

**Optional<T>**은 null이 될 수 있는 객체를 감싸는 Wrapper 클래스입니다. Java 8에서 도입되었으며, 지긋지긋한 `NullPointerException` (NPE)을 방지하고 null 체크 로직을 표준화하기 위해 만들어졌습니다.

## 1. Optional 생성

```java
// 1. 값이 확실히 있는 경우
Optional<String> opt = Optional.of("Hello");

// 2. 값이 null일 수도 있는 경우 (가장 많이 사용)
Optional<String> opt = Optional.ofNullable(someValue);

// 3. 빈 Optional (null 표현)
Optional<String> empty = Optional.empty();
```

---

## 2. 값 꺼내기 (지양해야 할 패턴 vs 권장 패턴)

### ❌ `get()` 사용 (위험)
값이 없으면 `NoSuchElementException`이 발생합니다. null 체크 없이 쓰는 것과 다를 바 없습니다.

```java
String value = opt.get(); // 위험!
```

### ✅ `orElse()` / `orElseGet()` / `orElseThrow()` (권장)

```java
// 값이 없으면 기본값 반환
String value = opt.orElse("Default");

// 값이 없으면 람다식 실행 결과 반환 (Lazy)
String value = opt.orElseGet(() -> findDefaultValue());

// 값이 없으면 예외 던지기
String value = opt.orElseThrow(() -> new IllegalArgumentException("값 없음"));
```

---

## 3. 값 처리하기 (ifPresent)

값이 있을 때만 특정 로직을 수행합니다.

```java
// 기존 방식
if (user != null) {
    System.out.println(user.getName());
}

// Optional 방식
optUser.ifPresent(user -> System.out.println(user.getName()));
```

---

## 4. Optional 변환 (map, filter)

Stream API와 유사한 방식으로 값을 다룰 수 있습니다.

```java
User user = new User("Alice", "Seoul");
Optional<User> optUser = Optional.ofNullable(user);

// 유저의 주소를 가져오는데, 유저가 null이거나 주소가 null이면 "Unknown" 반환
String city = optUser
    .map(User::getAddress)  // Optional<User> -> Optional<Address>
    .map(Address::getCity)  // Optional<Address> -> Optional<String>
    .orElse("Unknown");
```

---

## 💡 언제 써야 할까?

1.  **반환 타입(Return Type)으로만 사용**하는 것이 권장됩니다.
    - 메서드가 값을 반환할 수 없을 때 `null` 대신 `Optional.empty()`를 반환하여 클라이언트에게 명시적으로 알립니다.
2.  **필드, 매개변수, 생성자 인자**로는 사용하지 않는 것이 좋습니다.
    - `Optional` 자체가 객체이므로 오버헤드가 발생하며, 직렬화(Serializable)를 지원하지 않습니다.
