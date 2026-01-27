# Google Java Style Guide

구글에서 제공하는 Java 프로그래밍 스타일 가이드이다. 코드를 작성할 때 일관성을 유지하고 가독성을 높이기 위한 표준 규칙(Naming, Formatting 등)을 정의하고 있다.

## 1. 개요
이 문서는 Java 소스 코드의 **표준(Standard)** 역할을 한다. 단순히 코드를 예쁘게 만드는 것을 넘어, 유지보수하기 좋고 버그를 줄이는 패턴을 지향한다.

## 2. 소스 파일 구조
소스 파일은 다음 순서로 작성한다.
1. **라이선스 정보** (있는 경우)
2. **Package 구문** (줄바꿈 없음)
3. **Import 구문** (줄바꿈 없음, 와일드카드 `*` 사용 지양)
4. **Top-Level Class** (파일당 하나만 존재해야 함)

## 3. 명명 규칙 (Naming)
모든 식별자는 아스키(ASCII) 문자와 숫자만 사용하며, 목적을 명확히 드러내는 이름을 사용한다.

| 식별자 | 규칙 | 예시 | 비고 |
| :--- | :--- | :--- | :--- |
| **Package** | 모두 소문자 | `com.google.common` | 언더스코어(`_`) 사용 안 함 |
| **Class** | UpperCamelCase | `XmlHttpRequest` | 명사 또는 명사구 |
| **Method** | lowerCamelCase | `sendMessage` | 동사 또는 동사구 |
| **Variable** | lowerCamelCase | `userName` | |
| **Constant** | CONSTANT_CASE | `MAX_WIDTH` | `static final` 불변 필드 |

## 4. 포맷팅 (Formatting)
### 중괄호 (Braces)
* **K&R 스타일**을 따른다. 여는 중괄호(`{`)는 줄을 바꾸지 않고 바로 뒤에 붙인다.
* `if`, `else`, `for`, `do`, `while` 문은 본문이 비어있거나 한 줄이라도 **반드시 중괄호를 사용**한다.

```java
// Good
if (condition) {
  doSomething();
} else {
  doSomethingElse();
}

// Bad
if (condition) doSomething();
```

### 들여쓰기 (Indentation)
* **Space 2칸**을 사용한다. (Tab 문자 사용 금지)
* 연속된 들여쓰기는 4칸, 6칸 식으로 2칸씩 늘어난다.

### 줄바꿈 (Line Wrapping)
* 한 줄은 **100자(column)** 제한을 원칙으로 한다.
* 줄바꿈 시 연산자 앞에서 끊는 것을 권장한다.

```java
// Good: 연산자가 줄의 시작에 옴
String longString = "This represents a very long string that "
    + "concatenates two strings.";
```

## 5. 프로그래밍 관례 (Programming Practices)
* **@Override**: 상위 클래스 메서드를 재정의할 때는 반드시 `@Override` 어노테이션을 붙인다.
* **예외 처리**: `catch` 블록을 비워두지 않는다. 만약 비워야 한다면 이유를 주석으로 명시하거나 변수명을 `expected`로 짓는다.
* **Static 멤버 접근**: 클래스 인스턴스가 아닌 **클래스 이름**으로 접근한다.
    * `Foo.aStaticMethod();` (O)
    * `fooInstance.aStaticMethod();` (X)

## References
* [Google Java Style Guide (Official)](https://google.github.io/styleguide/javaguide.html)
* [Google Java Style Guide (Github)](https://github.com/google/styleguide)

