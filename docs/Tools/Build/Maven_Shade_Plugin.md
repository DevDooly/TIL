# Maven Shade Plugin: Uber-JAR 생성 및 패키지 재배치

Maven 프로젝트 빌드 시 의존성을 포함한 단일 실행 파일을 만들고, 의존성 충돌을 해결하기 위한 핵심 도구인 Maven Shade Plugin에 대해 정리합니다.

---

## 1. 개요

**Maven Shade Plugin**은 모든 의존 라이브러리를 포함하는 **Uber-JAR**(Fat JAR)를 생성하는 플러그인입니다. 단순히 파일들을 묶는 것을 넘어, 패키지 이름을 변경하여 충돌을 방지하는 기능을 제공합니다.

---

## 2. 핵심 기능

### 📦 1) Uber-JAR (Fat JAR) 생성

* 프로젝트가 의존하는 모든 라이브러리의 클래스 파일들을 하나의 JAR 파일로 병합합니다.
* 배포 시 단일 파일만 옮기면 되므로 관리가 매우 편리합니다.

### 🔄 2) 패키지 재배치 (Relocation)

* **배경**: 내 프로젝트와 의존 라이브러리가 동일한 라이브러리의 서로 다른 버전을 사용할 때 충돌 발생.
* **해결**: 특정 라이브러리의 패키지 경로를 빌드 시점에 강제로 변경(Shadowing)합니다.
    * 예: `com.google.gson` → `shaded.com.google.gson`
* 이를 통해 런타임에 클래스 로더가 서로 다른 버전의 클래스를 명확히 구분하게 합니다.

### 🛠️ 3) 리소스 변환 (Resource Transformation)

* 여러 JAR를 합칠 때 `META-INF/` 아래의 중복된 설정 파일들을 적절히 처리합니다.
* **ManifestResourceTransformer**: 실행 가능한 JAR의 메인 클래스를 지정.
* **ServicesResourceTransformer**: `META-INF/services` 파일들을 병합(SPI 지원).

---

## 3. 설정 방법 (`pom.xml`)

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-shade-plugin</artifactId>
    <version>3.5.0</version>
    <executions>
        <execution>
            <phase>package</phase>
            <goals>
                <goal>shade</goal>
            </goals>
            <configuration>
                <relocations>
                    <relocation>
                        <pattern>org.apache.http</pattern>
                        <shadedPattern>myproject.shaded.http</shadedPattern>
                    </relocation>
                </relocations>
                <transformers>
                    <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
                        <mainClass>com.example.App</mainClass>
                    </transformer>
                </transformers>
            </configuration>
        </execution>
    </executions>
</plugin>
```

---

## 4. 선택 가이드 (언제 무엇을 쓸까?)

| 플러그인 | 특징 | 추천 상황 |
| :--- | :--- | :--- |
| **Shade Plugin** | 패키지 재배치, 리소스 병합 가능 | **의존성 충돌 해결이 필요한 대규모 라이브러리/앱** |
| **Assembly Plugin** | 단순 파일/디렉토리 구조 보존 병합 | 간단한 번들링, 소스 코드 배포 |
| **Spring Boot Plugin** | Nested JAR 구조 (JAR 내 JAR) | **Spring Boot 기반 애플리케이션** |

---

## 5. 주의사항

1. **빌드 시간**: 모든 의존성을 풀어서 다시 압축하므로 빌드 시간이 늘어날 수 있습니다.
2. **라이선스**: 라이브러리를 Shading할 때 해당 라이브러리의 라이선스 규정을 준수해야 합니다.
3. **Reflective Access**: 리플렉션을 사용하여 클래스를 찾는 코드가 있다면, 패키지 재배치 시 해당 코드가 깨질 수 있으므로 주의가 필요합니다.
