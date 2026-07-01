# Java: Collections.emptyList() vs List.of() 비교

Java에서 비어 있는 불변(Immutable) 리스트를 생성할 때 사용하는 `Collections.emptyList()`와 `List.of()`의 차이점을 알아보고, Java 버전에 따라 어떤 메서드를 사용하는 것이 좋은지 정리합니다.

---

## 1. `Collections.emptyList()`

*   **Java 버전:** 1.5부터 사용 가능합니다.
*   **반환 타입:** 제네릭을 지원하는 `List<T>`를 반환합니다.
*   **핵심 특징:**
    *   **싱글톤(Singleton) 보장:** 이 메서드를 호출하면 항상 **동일한 `static final` 인스턴스**(`Collections.EMPTY_LIST`)를 반환합니다. 따라서 여러 번 호출해도 추가적인 메모리 할당이 없습니다.
    *   **불변(Immutable):** 반환된 리스트에 원소를 추가하거나 삭제하려고 하면 `UnsupportedOperationException`이 발생합니다.
    *   **타입 안정성:** `Collections.<String>emptyList()`와 같이 제네릭을 사용하여 컴파일 시 타입 안정성을 보장합니다.

```java
// Java 1.5+
List<String> list1 = Collections.emptyList();
List<Integer> list2 = Collections.emptyList();

System.out.println(list1 == list2); // true (항상 동일한 인스턴스)
```

---

## 2. `List.of()`

*   **Java 버전:** 9부터 사용 가능한 "불변 컬렉션 팩토리 메서드(Immutable Collection Factory Methods)" 중 하나입니다.
*   **반환 타입:** `List<E>`를 반환하지만, 실제로는 내부 구현 클래스(`ImmutableCollections.ListN`)의 인스턴스입니다.
*   **핵심 특징:**
    *   **현대적이고 간결한 API:** `List.of()`는 빈 리스트를, `List.of(e1, e2, ...)`는 원소를 가진 불변 리스트를 생성하는 등 일관되고 간결한 API를 제공합니다.
    *   **불변(Immutable):** 반환된 리스트는 완벽히 불변이며, `null` 요소를 허용하지 않습니다. 수정 시도 시 `UnsupportedOperationException`이 발생합니다.
    *   **싱글톤 미보장:** Javadoc에서는 빈 리스트에 대해 항상 동일한 인스턴스를 반환한다고 **보장하지는 않습니다.** 하지만 현재 대부분의 JDK 구현에서는 성능 최적화를 위해 싱글톤 인스턴스를 반환합니다.

```java
// Java 9+
List<String> list = List.of(); 
```

---

## 3. 주요 차이점 비교

| 특징 | `Collections.emptyList()` | `List.of()` |
| :--- | :--- | :--- |
| **Java 버전** | 1.5+ | **9+** |
| **API 스타일** | 정적 유틸리티 메서드 | 인터페이스의 정적 팩토리 메서드 |
| **가독성** | 다소 장황함 (`Collections.emptyList()`) | 간결하고 명확함 (`List.of()`) |
| **싱글톤 보장** | **보장됨 (Guaranteed)** | 보장되지 않음 (Not guaranteed by spec) |
| **Null 요소** | (비어 있으므로 해당 없음) | 허용하지 않음 (Not-null) |

---

## 4. 어떤 것을 사용해야 할까? (Java 버전에 따른 권장 사항)

결론은 프로젝트에서 사용하는 **Java 버전에 따라 달라집니다.**

### ✅ Java 8 이하를 사용하는 경우

*   `List.of()`를 사용할 수 없으므로, **반드시 `Collections.emptyList()`를 사용해야 합니다.**
*   오랜 기간 검증된 안정적인 방법입니다.

### ✅ Java 9 이상을 사용하는 경우

*   **`List.of()` 사용을 강력히 권장합니다.**
*   **이유:**
    1.  **가독성과 일관성:** `List.of()`는 현대 Java의 표준적인 불변 컬렉션 생성 방식입니다. `Set.of()`, `Map.of()`와 API 스타일이 일관되어 코드를 더 쉽게 이해할 수 있습니다.
    2.  **의도의 명확성:** 코드를 읽는 사람이 "불변 리스트를 생성하려는 의도"를 즉시 파악할 수 있습니다.
    3.  **간결함:** 코드가 더 짧고 깔끔해집니다.

---

## 결론

*   **Java 8 이하:** `new ArrayList<>()` 대신 `Collections.emptyList()`를 사용하여 불필요한 객체 생성을 피하세요.
*   **Java 9 이상:** `Collections.emptyList()`보다 현대적이고 가독성이 좋은 **`List.of()`**를 사용하세요. 이는 Java 커뮤니티의 모범 사례(Best Practice)로 자리 잡고 있습니다.

따라서, 레거시 코드를 유지보수하는 경우가 아니라면, Java 9 이상의 환경에서는 `List.of()`를 일관되게 사용하는 것이 좋습니다.
