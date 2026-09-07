# Java 25: 정식 기능과 Preview 구분

기준: JDK 25 GA 기능 상태, 확인일 2026-09-07. LTS 지원 기간과 배포판별 제공 기능은 벤더 정책을 별도로 확인한다.

## 주요 기능 상태

| 기능 | JDK 25 상태 | 적용 시 확인 |
| :--- | :--- | :--- |
| Scoped Values — JEP 506 | 정식 | scope 안의 값 바인딩. 참조한 객체 자체가 자동으로 불변이 되지는 않음 |
| Flexible Constructor Bodies — JEP 513 | 정식 | `super/this` 호출 전 안전한 검증·계산 및 제한된 필드 초기화 |
| Module Import Declarations — JEP 511 | 정식 | 모듈이 export한 패키지의 접근 가능한 타입. 내부 타입까지 모두 공개하지 않음 |
| Compact Source Files / Instance Main — JEP 512 | 정식 | 작은 프로그램의 진입점과 소스 구조 간소화 |
| Compact Object Headers — JEP 519 | 제품 기능 | **기본 비활성**, `-XX:+UseCompactObjectHeaders`로 활성화 |
| Structured Concurrency — JEP 505 | **다섯 번째 Preview** | `--enable-preview` 필요 |
| Primitive Types in Patterns — JEP 507 | **세 번째 Preview** | `--enable-preview` 필요 |
| Stable Values — JEP 502 | Preview | 정식 API로 취급하지 않음 |
| Vector API — JEP 508 | 열 번째 Incubator | 별도 incubator 모듈 |

상태와 옵션은 [Oracle JDK 25 릴리스 노트](https://www.oracle.com/java/technologies/javase/25-relnote-issues.html)를 기준으로 구분했다. 기존의 “Structured Concurrency Final/Stable” 안내는 잘못된 설명이었다.

## 기능별 오해

ScopedValue는 정해진 동적 범위에서 바인딩을 공유한다. 모든 ThreadLocal 사용을 그대로 대체할 수 있는 것은 아니다. 가변 객체를 넣으면 그 객체의 동시 접근 문제는 남는다. [ScopedValue API](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/ScopedValue.html)

유연한 생성자는 생성 중인 객체를 자유롭게 사용하는 기능이 아니다. 조기 생성 문맥의 제약 안에서 허용되는 필드 초기화가 있으므로, “인스턴스 필드 접근이 전부 금지”라고 설명하는 것도 부정확하다. [Java 25 생성자 규칙](https://docs.oracle.com/javase/specs/jls/se25/html/jls-8.html#jls-8.8.7)

Compact Object Headers는 정식 제품 옵션이 되었지만 기본값은 꺼져 있다. 활성화 전후의 heap, GC, 처리량을 직접 비교한다.

Structured Concurrency의 성공·실패·취소 정책은 사용하는 Joiner에 따라 달라진다. 이전 Preview 예제를 그대로 가져오지 말고 JDK 25 API로 컴파일한다. [StructuredTaskScope API](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/StructuredTaskScope.html)

## Preview 실습

JDK 25 도구로 해당 버전의 Preview 예제를 컴파일·실행한다. CI·테스트·운영 실행 옵션도 일치시켜야 한다.

```bash
javac --release 25 --enable-preview Main.java
java --enable-preview Main
```

운영 업그레이드는 JDK·Spring Boot·빌드 플러그인·agent·driver의 호환성을 확인하고 회귀 테스트로 판단한다. 이 문서는 기능 상태 정리이며 JDK 25 운영 적용 실적을 의미하지 않는다.
