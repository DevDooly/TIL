# Java 코드 포맷터 비교: google-java-format vs palantir-java-format

Java 프로젝트의 코드 스타일 일관성을 유지하기 위한 자동 포맷터로 `google-java-format`과 `palantir-java-format`이 가장 많이 추천됩니다. 이 두 포맷터의 특징과 차이점, 그리고 다른 대안들을 알아보고 Maven 프로젝트에서의 사용법을 정리합니다.

---

## 1. 주요 포맷터 비교

### 1.1. `google-java-format`

*   **철학:** **"코드 스타일에 대한 논쟁을 멈춰라."**
    *   매우 독단적(Opinionated)이며, 설정을 거의 제공하지 않습니다. 목표는 모든 Java 프로젝트에서 절대적인 코드 스타일 일관성을 유지하는 것입니다.
*   **주요 스타일 특징:**
    *   **들여쓰기: 2칸 공백 (Tabs not allowed)**
    *   **줄 길이 제한: 100자**
    *   메서드 체이닝 등 긴 줄은 가독성을 위해 여러 줄로 나누는 경향이 강합니다.
    *   AOSP (Android Open Source Project) 스타일 변형도 지원합니다.
*   **장점:**
    *   설정이 거의 필요 없어 도입이 매우 간편합니다.
    *   팀 내에서 포맷팅 스타일에 대한 모든 논쟁을 원천 차단할 수 있습니다.
    *   Google의 표준이라는 점에서 신뢰도가 높습니다.
*   **단점:**
    *   **설정이 불가능합니다.** 만약 2칸 들여쓰기나 100자 줄 제한이 마음에 들지 않아도 변경할 수 없습니다.

### 1.2. `palantir-java-format`

*   **철학:** **`google-java-format` 기반의 합리적인 변형.**
    *   `google-java-format`의 포크(fork) 버전입니다. Google 스타일을 대부분 따르지만, 개발자들이 가장 많이 선호하는 몇 가지 중요한 차이점을 뒀습니다.
*   **주요 스타일 특징 (Google 포맷과의 차이점):**
    *   **들여쓰기: 4칸 공백** (이 포맷터를 선택하는 가장 큰 이유)
    *   줄 바꿈 휴리스틱이 약간 달라, 경우에 따라 조금 더 간결한 코드를 생성하기도 합니다.
*   **장점:**
    *   "Google 스타일이지만 들여쓰기는 4칸"이라는, 많은 Java 개발자에게 익숙한 스타일을 제공합니다.
    *   여전히 매우 일관된 스타일을 강제하므로 논쟁의 여지가 적습니다.
*   **단점:**
    *   `google-java-format`에 비해 인지도는 낮습니다.
    *   마찬가지로 설정의 유연성은 거의 없습니다.

### 1.3. 다른 대안: `Eclipse Java Formatter`

*   **철학:** **"최고의 유연성."**
    *   Eclipse IDE에 내장된 포맷터로, 거의 모든 스타일을 XML 설정을 통해 커스터마이징할 수 있습니다.
*   **장점:**
    *   **최고의 유연성:** 기존 프로젝트의 복잡한 스타일 가이드를 그대로 따르거나, 팀의 고유한 스타일을 정의할 수 있습니다.
    *   IDE(Eclipse)에서 사용하는 포맷팅 규칙을 XML로 export하여 빌드 과정에 그대로 적용할 수 있어 일관성 유지가 용이합니다.
*   **단점:**
    *   **설정의 복잡성:** XML 설정 파일이 복잡하고 관리하기 어렵습니다.
    *   어떤 설정을 사용할지에 대한 팀 내 논쟁이 다시 시작될 수 있습니다.

> #### Checkstyle은 포맷터가 아닙니다
> `Checkstyle`은 코드 스타일 규칙을 **검사(Check)**하고 위반 사항을 보고하는 정적 분석 도구입니다. 코드를 자동으로 수정해주는 포맷터와는 역할이 다릅니다. 보통 포맷터가 처리하지 못하는 네이밍 컨벤션, 클래스 설계 규칙 등을 강제하기 위해 포맷터와 **함께** 사용됩니다.

---

## 2. 추천: 어떤 포맷터를 선택해야 할까?

| 특징 | `google-java-format` | `palantir-java-format` | `Eclipse Formatter` |
| :--- | :--- | :--- | :--- |
| **들여쓰기** | 2칸 공백 | **4칸 공백** | 설정 가능 |
| **설정 유연성**| 거의 없음 | 거의 없음 | **매우 높음** |
| **철학** | 절대적 일관성, 논쟁 종결 | Google 스타일 + 4칸 | 완전한 커스터마이징 |
| **적합한 환경**| 새로운 프로젝트, 일관성 최우선 | 4칸 들여쓰기를 선호하는 팀 | 기존 스타일 유지가 중요한 레거시 프로젝트 |

*   **새로운 프로젝트를 시작하고, 스타일 논쟁 없이 일관성을 최우선으로 한다면?**
    *   ➡️ **`google-java-format`** (2칸) 또는 **`palantir-java-format`** (4칸)을 추천합니다. 팀의 들여쓰기 선호도에 따라 선택하세요.
*   **기존에 복잡한 스타일 가이드가 있거나, 특정 스타일을 반드시 따라야 한다면?**
    *   ➡️ **`Eclipse Java Formatter`**가 유일한 대안입니다.

---

## 3. Maven에서 사용법 (Spotless 플러그인 활용)

`spotless-maven-plugin`은 다양한 포맷터를 통합하여 실행할 수 있게 해주는 메타 플러그인입니다. 이를 사용하여 Maven 프로젝트에 포맷터를 적용하는 것이 가장 일반적입니다.

### 3.1. `pom.xml`에 Spotless 플러그인 추가

```xml
<build>
    <plugins>
        <plugin>
            <groupId>com.diffplug.spotless</groupId>
            <artifactId>spotless-maven-plugin</artifactId>
            <version>2.27.2</version> <!-- 최신 버전 사용 권장 -->
            <configuration>
                <!-- 아래에 원하는 포맷터 설정을 추가 -->
            </configuration>
        </plugin>
    </plugins>
</build>
```

### 3.2. 포맷터별 설정

#### A. `google-java-format` 사용 시

```xml
<configuration>
    <java>
        <googleJavaFormat>
            <version>1.15.0</version> <!-- 포맷터 버전 지정 -->
            <style>GOOGLE</style> <!-- 또는 AOSP -->
        </googleJavaFormat>
        <licenseHeader>
            <content>/* (C) $YEAR */</content>  <!-- (선택) 라이선스 헤더 자동 추가 -->
        </licenseHeader>
    </java>
</configuration>
```

#### B. `palantir-java-format` 사용 시

```xml
<configuration>
    <java>
        <palantirJavaFormat>
            <version>2.20.0</version> <!-- 포맷터 버전 지정 -->
            <style>PALANTIR</style>
        </palantirJavaFormat>
    </java>
</configuration>
```

#### C. `Eclipse Java Formatter` 사용 시

```xml
<configuration>
    <java>
        <eclipse>
            <version>4.21.0</version> <!-- 이클립스 포맷터 버전 지정 -->
            <file>${project.basedir}/eclipse-formatter.xml</file> <!-- XML 설정 파일 경로 -->
        </eclipse>
    </java>
</configuration>
```

### 3.3. 실행 명령어

*   **스타일 검사:**
    ```bash
    mvn spotless:check
    ```
    (코드 스타일이 맞지 않으면 빌드가 실패합니다. CI/CD 파이프라인에 통합하기 좋습니다.)

*   **스타일 자동 수정:**
    ```bash
    mvn spotless:apply
    ```
    (잘못된 포맷을 가진 파일을 자동으로 수정해줍니다. 커밋 전에 실행하는 것이 좋습니다.)
