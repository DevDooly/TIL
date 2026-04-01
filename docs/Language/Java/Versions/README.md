# Java Versions History

Java는 지속적으로 발전하며 새로운 기능을 도입하고 있습니다. 특히 **LTS (Long-Term Support)** 버전은 안정성과 장기 지원을 보장하므로 실무에서 주로 사용됩니다.

## 📅 버전별 주요 변경 사항 요약

| 버전 | 출시일 | LTS | 주요 특징 |
| :---: | :---: | :---: | :--- |
| **Java 8** | 2014.03 | ✅ | **Lambda Expressions**, **Stream API**, Optional, 새로운 날짜/시간 API |
| **Java 9** | 2017.09 | | **Module System (Jigsaw)**, JShell, Factory Methods for Collections (`List.of`) |
| **Java 10** | 2018.03 | | **Local-Variable Type Inference (`var`)** |
| **Java 11** | 2018.09 | ✅ | **HTTP Client (Standard)**, String 메서드 추가(`isBlank`, `lines` 등), Oracle JDK 유료화 이슈 |
| **Java 12** | 2019.03 | | Switch Expressions (Preview) |
| **Java 13** | 2019.09 | | Text Blocks (Preview) |
| **Java 14** | 2020.03 | | **Switch Expressions (Standard)**, Records (Preview), NPE 메시지 개선 |
| **Java 15** | 2020.09 | | **Text Blocks (Standard)**, Hidden Classes |
| **Java 16** | 2021.03 | | **Records (Standard)**, Pattern Matching for instanceof |
| **Java 17** | 2021.09 | ✅ | **Sealed Classes**, Pattern Matching for switch (Preview), **Strong Encapsulation of JDK Internals** |
| **Java 21** | 2023.09 | ✅ | **Virtual Threads**, **Sequenced Collections**, Record Patterns |

---

## 🚀 변화가 컸던 주요 버전 (Major Milestones)

Java 역사에서 개발 패러다임을 바꿀 정도로 큰 변화가 있었던 버전들입니다.

### 1. Java 8 (The Beginning of Modern Java)
함수형 프로그래밍 개념이 도입되면서 Java 코드가 획기적으로 간결해지고 강력해졌습니다.

-   **핵심:** Lambda, Stream, Optional

### 2. Java 11 (The New LTS Standard)
Java 9의 모듈 시스템 도입 이후 안정화된 첫 LTS 버전입니다. 클라우드 네이티브 환경에 적합한 기능들이 대거 추가되었습니다.

-   **핵심:** `var` 키워드(10), 표준 HTTP Client, Docker 컨테이너 지원 개선

### 3. Java 17 (Records & Sealed Classes)
데이터 중심 프로그래밍을 위한 기능들이 완성되었습니다. Lombok 없이도 불변 객체를 쉽게 만들 수 있게 되었습니다.

-   **핵심:** Records, Sealed Classes, Text Blocks

### 4. Java 21 (Concurrency Revolution)
경량 스레드인 Virtual Thread의 도입으로 고성능 동시성 처리가 획기적으로 쉬워졌습니다.

-   **핵심:** Virtual Threads, Sequenced Collections
