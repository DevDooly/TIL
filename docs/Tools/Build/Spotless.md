# Spotless: 코드 스타일 자동화 도구

Spotless는 프로젝트의 코드 스타일을 일관되게 유지하고 관리하기 위한 강력한 포맷팅 도구입니다. 단순히 스타일을 검사하는 것에 그치지 않고, 설정된 규칙에 따라 코드를 자동으로 수정해 주는 기능을 제공합니다.

---

## 1. 핵심 기능

*   **다양한 언어 지원**: Java, Kotlin, Scala, Python, JavaScript, CSS, Markdown 등 광범위한 언어를 지원합니다.
*   **포맷터 통합**: Google Java Style, Palantir, Prettier, Eclipse Formatter 등 업계 표준 포맷팅 도구를 그대로 가져와 사용할 수 있습니다.
*   **멱등성(Idempotency)**: 동일한 규칙을 여러 번 적용해도 결과가 변하지 않음을 보장하여 빌드 안정성을 높입니다.
*   **빌드 도구 연동**: Gradle 및 Maven 플러그인을 통해 빌드 파이프라인(CI/CD)에 쉽게 통합할 수 있습니다.

---

## 2. 주요 설정 (Gradle 기준)

`build.gradle` 파일에 다음과 같이 설정하여 Java 프로젝트에 적용할 수 있습니다.

```gradle
plugins {
    id "com.diffplug.spotless" version "6.x.x"
}

spotless {
    java {
        target 'src/*/java/**/*.java' // 대상 파일 지정
        
        googleJavaFormat('1.17.0')     // Google Java Style 적용
        removeUnusedImports()          // 사용하지 않는 import 제거
        trimTrailingWhitespace()       // 줄 끝 공백 제거
        endWithNewline()               // 파일 끝 줄바꿈 추가
    }
}
```

---

## 3. 사용 방법

터미널에서 다음 명령어를 통해 코드 스타일을 관리합니다.

*   **`./gradlew spotlessCheck`**: 코드가 설정된 규칙을 준수하는지 확인합니다. 규칙 위반 시 빌드가 실패하므로 CI 환경에서 활용하기 적합합니다.
*   **`./gradlew spotlessApply`**: 잘못된 포맷을 설정된 규칙에 맞춰 **자동으로 수정**합니다. 개발자가 커밋하기 전에 실행하는 것이 권장됩니다.

---

## 4. 도입 효과

1.  **코드 리뷰 효율화**: "들여쓰기가 틀렸다"와 같은 소모적인 스타일 지적 대신 비즈니스 로직에 집중할 수 있습니다.
2.  **Git Diff 가독성 향상**: 팀원별로 다른 IDE 설정으로 인해 발생하는 불필요한 코드 변경을 방지하여 히스토리를 깔끔하게 유지합니다.
3.  **일관성 보장**: 프로젝트 전체에 걸쳐 하나의 통일된 스타일 가이드를 강제할 수 있습니다.

---

## 5. 추천 전략: Git Hook 활용

`Git Pre-commit hook`을 설정하여 커밋 시점에 자동으로 `spotlessApply`가 실행되도록 구성하면, 개발자가 신경 쓰지 않아도 항상 정돈된 코드가 커밋되는 환경을 구축할 수 있습니다.
