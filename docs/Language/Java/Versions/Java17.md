# Java 17: Modernization and Productivity

Java 17은 Java 11 이후 3년 만에 출시된 **LTS** 버전으로, 언어 차원의 생산성 향상과 런타임 성능 개선이 돋보이는 버전입니다.

## 1. Records

데이터를 저장하는 용도의 클래스(DTO 등)를 작성할 때 발생하는 상용구 코드(Boilerplate)를 획기적으로 줄여주는 기능입니다. 기본적으로 불변(Immutable) 객체입니다.

**기존 방식:**
```java
public class User {
    private final String name;
    private final int age;
    // 생성자, getter, equals, hashCode, toString... (매우 길어짐)
}
```

**Java 17 (Records):**
```java
public record User(String name, int age) { }
```
- 컴파일 시 생성자, Getter, `equals`, `hashCode`, `toString`이 자동으로 생성됩니다.

---

## 2. Sealed Classes (봉인된 클래스)

상속받을 수 있는 하위 클래스를 제한하는 기능입니다. 무분별한 확장을 막고, 도메인 모델을 더 안전하게 설계할 수 있습니다.

```java
public sealed interface Shape permits Circle, Square { }

public final class Circle implements Shape { ... }
public final class Square implements Shape { ... }

// Rectangle은 permits 목록에 없으므로 Shape를 구현할 수 없음
```

---

## 3. Pattern Matching for `instanceof`

객체의 타입을 확인한 후 즉시 형변환된 변수로 사용할 수 있게 되었습니다.

```java
// 기존
if (obj instanceof String) {
    String s = (String) obj;
    System.out.println(s.length());
}

// Java 17
if (obj instanceof String s) {
    System.out.println(s.length());
}
```

---

## 4. Text Blocks

멀티라인 문자열을 더 깔끔하게 작성할 수 있게 되었습니다. JSON, HTML, SQL 등을 다룰 때 유용합니다.

```java
String json = """
    {
      "name": "devdooly",
      "age": 30,
      "status": "active"
    }
    """;
```

---

## 5. Strong Encapsulation of JDK Internals

JDK 내부 API(`sun.misc.Unsafe` 등)에 대한 접근이 기본적으로 차단되었습니다. 이는 보안을 강화하고 Java 런타임의 안정성을 높이는 조치입니다.
- 기존에 내부 API를 무단으로 사용하던 라이브러리들은 Java 17 마이그레이션 시 업데이트가 필요할 수 있습니다.
