# Behavior-Driven Development (BDD)

**BDD (Behavior-Driven Development, 행동 주도 개발)**는 **TDD (Test-Driven Development)**에서 파생된 소프트웨어 개발 방법론으로, 개발자, QA, 그리고 비즈니스 관계자(기획자 등) 간의 협업과 소통을 강조합니다.

소프트웨어의 **행동(Behavior)**과 **사용자 시나리오**에 초점을 맞추어 테스트 케이스를 작성하며, 이를 통해 기술적인 구현 세부 사항보다는 **"이 기능이 사용자의 어떤 요구사항을 해결해 주는가?"**에 집중하게 합니다.

---

## 1. TDD vs BDD

| 특징 | TDD (Test-Driven Development) | BDD (Behavior-Driven Development) |
| :--- | :--- | :--- |
| **관점** | 기능 구현의 정확성 (구현 검증) | 사용자의 행동 및 비즈니스 요구사항 (행위 검증) |
| **테스트 언어** | 프로그래밍 언어 (코드 중심) | 자연어에 가까운 언어 (Gherkin 등) |
| **주요 대상** | 개발자 | 개발자, 기획자, QA 등 모든 이해관계자 |
| **테스트 단위** | 유닛(Unit) 테스트 중심 | 인수(Acceptance) 테스트, 통합 테스트 중심 |

> **TDD가 "올바르게 만들고 있는가?(Are we building the product right?)"**를 묻는다면,  
> **BDD는 "올바른 제품을 만들고 있는가?(Are we building the right product?)"**를 묻습니다.

---

## 2. 기본 패턴 (Given-When-Then)

BDD는 **Given-When-Then**이라는 구조화된 패턴을 사용하여 시나리오를 작성합니다. 이 패턴은 비전문가도 쉽게 이해할 수 있는 **유비쿼터스 언어(Ubiquitous Language)**를 사용하는 것을 권장합니다.

### 구조 설명

- **Feature (기능):** 테스트할 기능이나 시스템의 동작을 정의합니다.
- **Scenario (시나리오):** 특정 상황에서의 구체적인 행동 흐름을 설명합니다.
- **Given (주어진 환경):** 시나리오가 시작되기 전의 초기 상태나 조건을 명시합니다. (준비)
- **When (행위):** 사용자가 시스템에 가하는 행동이나 이벤트를 명시합니다. (실행)
- **Then (기대 결과):** 행동의 결과로 인해 변경된 상태나 기대되는 출력을 명시합니다. (검증)

### 예시 (로그인 기능)

```gherkin
Feature: 사용자 로그인

  Scenario: 유효한 자격 증명으로 로그인 성공
    Given 사용자가 로그인 페이지에 접속해 있다
    And 사용자는 유효한 아이디 "user1"과 비밀번호 "password123"을 가지고 있다
    When 사용자가 아이디와 비밀번호를 입력하고 로그인 버튼을 클릭한다
    Then "로그인 성공" 메시지가 표시되어야 한다
    And 메인 페이지로 리다이렉트 되어야 한다
```

---

## 3. Java 코드 예시 (JUnit + Mockito)

BDD 스타일은 실제 코드 작성 시에도 적용될 수 있습니다. `Mockito`나 `BDDMockito` 라이브러리를 사용하면 BDD 스타일의 테스트 코드를 쉽게 작성할 수 있습니다.

```java
import static org.mockito.BDDMockito.*;
import static org.assertj.core.api.Assertions.*;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class AuthServiceTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private AuthService authService;

    @Test
    void login_Success() {
        // Given (준비)
        User user = new User("devdooly", "1234");
        given(userRepository.findByUsername("devdooly"))
            .willReturn(Optional.of(user));

        // When (실행)
        boolean result = authService.login("devdooly", "1234");

        // Then (검증)
        then(userRepository).should(times(1)).findByUsername("devdooly");
        assertThat(result).isTrue();
    }
}
```

## 4. 관련 도구 (Tools)

- **Cucumber:** Gherkin 문법을 지원하는 가장 대표적인 BDD 프레임워크. (Java, JS, Ruby 등 지원)
- **JBehave:** Java 기반의 BDD 프레임워크.
- **SpecFlow:** .NET용 BDD 프레임워크.
- **Jest / Jasmine:** JavaScript 생태계에서는 테스트 블록(`describe`, `it`) 자체가 BDD 스타일을 따름.

---

## References
- [Cucumber - BDD](https://cucumber.io/docs/bdd/)
- [Martin Fowler - GivenWhenThen](https://martinfowler.com/bliki/GivenWhenThen.html)