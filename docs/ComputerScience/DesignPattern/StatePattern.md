# State Pattern (상태 패턴)

**상태 패턴(State Pattern)**은 객체의 내부 상태에 따라 스스로 행동을 변경할 수 있게 하는 행동 디자인 패턴입니다. 객체 내부에 상태를 나타내는 클래스들을 별도로 캡슐화하고, 상태가 전환될 때 행동도 같이 전환되도록 구현합니다.

## 1. 사용 목적
*   객체의 상태에 따라 동작이 달라져야 하고, 상태가 런타임에 동적으로 바뀔 때 유용합니다.
*   거대한 `if-else` 또는 `switch` 문으로 상태를 분기하는 코드를 제거하여 유지보수성을 높일 수 있습니다.
*   각 상태 로직을 독립된 클래스로 분리하므로 새로운 상태 추가가 쉽습니다(OCP 원칙).

## 2. 구조
*   **Context (문맥):** 클라이언트가 사용하는 인터페이스를 정의하고, 현재 상태(State 객체)를 유지합니다.
*   **State (상태 인터페이스):** 상태별 동작을 정의하는 공통 인터페이스입니다.
*   **ConcreteState (구체적 상태):** State 인터페이스를 구현하며, 각 상태별 실제 동작을 정의합니다.

## 3. 예제 코드 (Java)

아래 예제는 문자열을 출력할 때 대문자 상태와 소문자 상태를 번갈아 가며 동작하는 간단한 상태 머신입니다.

```java
// 1. State Interface
interface Statelike {
    void writeName(StateContext context, String name);
}

// 2. Concrete State (소문자 상태)
class StateLowerCase implements Statelike {
    @Override
    public void writeName(final StateContext context, final String name) {
        System.out.println(name.toLowerCase()); // 동작: 소문자 출력
        context.setState(new StateMultipleUpperCase()); // 상태 전환 -> 대문자 상태로
    }
}

// 2. Concrete State (대문자 상태)
class StateMultipleUpperCase implements Statelike {
    private int count = 0;

    @Override
    public void writeName(final StateContext context, final String name) {
        System.out.println(name.toUpperCase()); // 동작: 대문자 출력
        // 두 번 출력한 뒤에 다시 소문자 상태로 전환
        if(++count > 1) {
            context.setState(new StateLowerCase());
        }
    }
}

// 3. Context
class StateContext {
    private Statelike myState;

    StateContext() {
        setState(new StateLowerCase()); // 초기 상태 설정
    }

    void setState(final Statelike newState) {
        myState = newState;
    }

    public void writeName(final String name) {
        myState.writeName(this, name); // 현재 상태 객체에 행동 위임
    }
}

// 4. Usage
public class DemoOfClientState {
    public static void main(String[] args) {
        final StateContext sc = new StateContext();

        sc.writeName("Monday");    // monday (소문자 상태 -> 대문자 전환)
        sc.writeName("Tuesday");   // TUESDAY (대문자 상태 1회)
        sc.writeName("Wednesday"); // WEDNESDAY (대문자 상태 2회 -> 소문자 전환)
        sc.writeName("Thursday");  // thursday (소문자 상태 -> 대문자 전환)
        sc.writeName("Friday");    // FRIDAY
        sc.writeName("Saturday");  // SATURDAY
        sc.writeName("Sunday");    // sunday
    }
}
```

## 4. 장단점
*   **장점:** 상태별 로직을 분리하여 코드가 깔끔해지고, 새로운 상태 추가 시 기존 코드를 수정할 필요가 적습니다.
*   **단점:** 상태가 적을 때는 클래스 개수가 불필요하게 늘어나 복잡해질 수 있습니다.