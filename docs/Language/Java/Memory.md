# Java Memory Structure (JVM Runtime Data Areas)

Java 프로그램이 실행될 때 JVM(Java Virtual Machine)은 운영체제로부터 메모리를 할당받아 이를 여러 영역으로 나누어 관리합니다. 이를 **Runtime Data Areas**라고 합니다.

## 1. 주요 메모리 영역 (Runtime Data Areas)

JVM 메모리 구조는 크게 **Thread-Local(스레드 별로 생성)** 영역과 **Shared(모든 스레드가 공유)** 영역으로 나뉩니다.

### 1.1 Thread-Local (스레드별 독립 공간)
이 영역들은 각 스레드가 시작될 때 생성되고, 스레드가 종료되면 함께 소멸됩니다. 따라서 동기화 문제가 발생하지 않습니다.

*   **PC Register (Program Counter Register):**
    *   현재 실행 중인 JVM 명령의 주소를 저장합니다.
    *   CPU가 명령어를 어디까지 수행했는지 추적하는 역할을 합니다.
*   **JVM Stack (Stack Area):**
    *   메소드 호출 시마다 **Frame**이라는 단위로 쌓입니다.
    *   Frame 내부에는 **Local Variables(지역 변수)**, **Operand Stack(피연산자 스택)**, **Constant Pool Reference**가 포함됩니다.
    *   메소드가 종료되면 Frame은 스택에서 제거(Pop)됩니다.
    *   Primitive Type 변수와 Reference Type 변수의 주소값이 저장됩니다.
*   **Native Method Stack:**
    *   Java가 아닌 다른 언어(C, C++ 등)로 작성된 네이티브 코드를 실행하기 위한 스택입니다. (JNI 사용 시)

### 1.2 Shared (공유 공간)
모든 스레드가 공유하므로 **동기화(Synchronization)** 문제가 발생할 수 있으며, GC(Garbage Collection)의 대상이 됩니다.

*   **Heap Area (힙 영역):**
    *   `new` 키워드로 생성된 **객체(Instance)**와 **배열(Array)**이 저장되는 공간입니다.
    *   GC의 주요 대상입니다.
    *   효율적인 GC를 위해 Young Generation(Eden, Survivor)과 Old Generation으로 나뉩니다.
*   **Method Area (메소드 영역):**
    *   클래스 로더가 로드한 **클래스(Class) 정보**, **필드 정보**, **메소드 정보**, **Static 변수**, **상수(Constant Pool)** 등이 저장됩니다.
    *   Java 8부터는 **Metaspace**라는 이름으로 변경되어 Native Memory(OS 메모리) 영역을 사용하게 되었습니다. (PermGen 영역 제거됨)

## 2. Java 8 이후의 변화 (Metaspace)
Java 7까지 존재하던 **PermGen(Permanent Generation)** 영역이 Java 8부터 제거되고 **Metaspace**로 대체되었습니다.

*   **PermGen:** Heap 영역의 일부로, 크기가 제한적이어 `OutOfMemoryError: PermGen space` 오류가 자주 발생했습니다.
*   **Metaspace:** Native Memory(OS 관리 메모리)를 사용하므로, OS가 허용하는 한 유연하게 크기가 조정됩니다.

## 3. 요약 다이어그램 (JVM Runtime Data Areas)

```mermaid
graph TD
    subgraph Shared [Shared Area (GC Target)]
        Heap[Heap Area<br/>(Eden, Survivor, Old)]
        Method[Method Area / Metaspace<br/>(Class Info, Static Vars)]
    end

    subgraph Thread1 [Thread 1]
        Stack1[JVM Stack<br/>(Frames)]
        PC1[PC Register]
        Native1[Native Method Stack]
    end

    subgraph Thread2 [Thread 2]
        Stack2[JVM Stack<br/>(Frames)]
        PC2[PC Register]
        Native2[Native Method Stack]
    end

    Thread1 -.-> Shared
    Thread2 -.-> Shared
    
    style Shared fill:#f9f,stroke:#333,stroke-width:2px
    style Heap fill:#ff9,stroke:#333
    style Method fill:#9ff,stroke:#333
```
