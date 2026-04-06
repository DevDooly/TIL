# Mockito: 단위 테스트를 위한 Mock 객체 활용 가이드

Spring Boot 환경에서 단위 테스트(Unit Test)를 작성할 때, 의존성을 가진 외부 객체를 실제 객체 대신 가짜 객체(Mock)로 대체하여 테스트 대상 로직에만 집중할 수 있도록 돕는 **Mockito** 라이브러리의 활용법을 정리합니다.

---

## 1. Mockito란?

**Mockito**는 Java용 오픈소스 Mocking 프레임워크입니다. 테스트 대상 클래스가 의존하고 있는 다른 클래스(예: 데이터베이스, 외부 API 등)의 동작을 가상으로 정의(Stubbing)하여, 독립적인 단위 테스트를 가능하게 합니다.

Spring Boot 2.x/3.x에서는 `spring-boot-starter-test`에 기본 포함되어 있어 별도 설정 없이 바로 사용할 수 있습니다.

---

## 2. 핵심 어노테이션 (Annotations)

JUnit 5와 함께 사용할 때 가장 많이 쓰이는 3가지 어노테이션입니다.

* **`@Mock`**: 가짜 객체를 생성합니다. 실제 로직은 실행되지 않으며, 모든 메소드 호출에 대해 기본값(null, 0 등)을 반환합니다.
* **`@Spy`**: 실제 객체의 기능을 유지하면서 특정 메소드만 Mocking하고 싶을 때 사용합니다. (Partial Mocking)
* **`@InjectMocks`**: 생성된 `@Mock` 또는 `@Spy` 객체들을 테스트 대상 객체의 필드에 자동으로 주입해줍니다.

---

## 3. 기본 사용법 및 예시 코드

### 3.1 서비스 계층 단위 테스트 구조

```java
@ExtendWith(MockitoExtension.class) // JUnit 5에서 Mockito 사용 선언
class UserServiceTest {

    @Mock
    private UserRepository userRepository; // 가짜 레포지토리

    @InjectMocks
    private UserService userService; // 가짜 레포지토리가 주입된 서비스

    @Test
    void 유저_조회_성공_테스트() {
        // 1. Given: Mock 객체의 동작 정의 (Stubbing)
        User mockUser = new User(1L, "Rudy");
        when(userRepository.findById(1L)).thenReturn(Optional.of(mockUser));

        // 2. When: 실제 테스트 대상 로직 실행
        User foundUser = userService.getUserById(1L);

        // 3. Then: 검증
        assertThat(foundUser.getName()).isEqualTo("Rudy");
        verify(userRepository, times(1)).findById(1L); // 메소드 호출 횟수 검증
    }
}
```

---

## 4. 주요 기능 상세

### 4.1 Stubbing (동작 정의)

* `when(...).thenReturn(...)`: 특정 파라미터로 호출 시 결과값 반환.
* `when(...).thenThrow(...)`: 예외 발생 상황 시뮬레이션.
* `any()`, `anyInt()`, `anyString()`: 구체적인 값이 아닌 인자 매처(Argument Matcher) 사용.

### 4.2 Verification (호출 검증)

* `verify(mock, times(n)).method(...)`: n번 호출되었는지 확인.
* `verify(mock, never()).method(...)`: 한 번도 호출되지 않았는지 확인.
* `verifyNoInteractions(mock)`: 해당 객체와 아무런 상호작용이 없었는지 확인.

---

## 5. @SpringBootTest vs @MockBean

* **`@SpringBootTest` + `@MockBean`**: 스프링 컨텍스트를 전체 로드하여 통합 테스트 성격이 강함. 스프링 빈으로 등록된 객체를 Mock으로 교체하고 싶을 때 사용.
* **`@ExtendWith(MockitoExtension.class)` + `@Mock`**: 스프링 컨텍스트 없이 순수 Java 객체로 테스트. **실행 속도가 매우 빠름.**

---

## 6. 결론

Mockito를 잘 활용하면 복잡한 인프라(DB, 외부 API) 의존성 없이도 핵심 비즈니스 로직을 빠르고 정확하게 검증할 수 있습니다. 가능한 한 스프링 컨텍스트를 사용하지 않는 순수 Mockito 테스트를 지향하는 것이 테스트 효율성 면에서 유리합니다.
