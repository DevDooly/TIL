# Spring Boot: @EnableAutoConfiguration vs @ConfigurationPropertiesScan 비교

Spring Boot에서 애플리케이션의 설정을 다루는 데 중요한 역할을 하는 `@EnableAutoConfiguration`과 `@ConfigurationPropertiesScan` 어노테이션은 그 목적과 작동 방식에 명확한 차이가 있습니다. 이 문서에서는 두 어노테이션의 용도, 차이점, 그리고 언제 사용해야 하는지에 대해 비교 설명합니다.

---

## 1. `@EnableAutoConfiguration`

### 1.1. 용도

*   **Spring Boot의 "마법" 핵심:** 클래스패스에 존재하는 JAR 파일, 개발자가 정의한 빈(Bean), 또는 다양한 프로퍼티(Properties) 설정 등을 기반으로 Spring 애플리케이션 컨텍스트를 **자동으로 구성**하는 역할을 합니다.
*   **보일러플레이트 코드 제거:** 개발자가 직접 수많은 `@Configuration` 클래스를 정의하지 않아도, 필요한 빈들을 자동으로 등록하여 애플리케이션을 빠르게 실행할 수 있도록 돕습니다.

### 1.2. 작동 방식

*   애플리케이션 시작 시 클래스패스를 스캔하여 모든 `META-INF/spring.factories` 파일을 찾습니다.
*   이 파일들에는 `@AutoConfiguration`으로 어노테이션된 클래스들이 나열되어 있습니다.
*   각 `AutoConfiguration` 클래스에는 `@ConditionalOnClass`, `@ConditionalOnMissingBean`, `@ConditionalOnProperty` 등 다양한 `@ConditionalOn...` 어노테이션이 붙어 있습니다.
*   이 조건들이 충족될 경우에만 해당 `AutoConfiguration`이 활성화되어 특정 빈들을 애플리케이션 컨텍스트에 등록합니다.
*   예를 들어, `spring-webmvc`가 클래스패스에 있으면 웹 서버를 자동으로 구성하고, `spring-data-jpa`가 있으면 JPA 관련 빈들을 구성합니다.

### 1.3. 사용 시점

*   대부분의 Spring Boot 애플리케이션에서는 메인 애플리케이션 클래스에 붙는 `@SpringBootApplication` 어노테이션 내부에 `@EnableAutoConfiguration`이 이미 포함되어 있습니다.
*   따라서 일반적인 경우에는 개발자가 이 어노테이션을 직접 명시할 필요는 거의 없습니다.
*   특정 자동 구성을 제외하고 싶을 때 (`@SpringBootApplication(exclude = {DataSourceAutoConfiguration.class})`) 명시적으로 사용하기도 합니다.

---

## 2. `@ConfigurationPropertiesScan`

### 2.1. 용도

*   **타입 안전한 외부 설정 바인딩:** 외부 설정 파일(`application.properties`, `application.yml`), 환경 변수, 커맨드 라인 인자 등에 정의된 설정 값들을 타입 안전한(type-safe) Java 객체로 바인딩하여 Spring 빈으로 등록하는 역할을 합니다.
*   **커스텀 설정 관리 간소화:** 개발자가 직접 정의한 `@ConfigurationProperties` 클래스들을 자동으로 스캔하고 빈으로 등록하여, 일일이 `@Bean`으로 선언하는 번거로움을 줄여줍니다.

### 2.2. 작동 방식

*   어노테이션이 붙은 `@ConfigurationProperties` 클래스를 찾기 위해 지정된 패키지(`basePackages`) 또는 메인 애플리케이션 클래스가 있는 패키지 및 하위 패키지들을 스캔합니다.
*   스캔된 `@ConfigurationProperties` 클래스를 Spring 빈으로 등록하고, 해당 클래스의 필드에 외부 설정 값을 주입(바인딩)합니다.

### 2.3. 사용 시점

*   애플리케이션에 **특정 목적의 커스텀 설정 프로퍼티 객체를 여러 개 정의**하고, 이를 Spring Boot가 자동으로 찾아서 등록해주기를 원할 때 사용합니다.
*   주로 메인 애플리케이션 클래스(`@SpringBootApplication`와 함께) 또는 별도의 `@Configuration` 클래스에 붙여 사용합니다.

### 2.4. 코드 예시

```java
// application.yml (외부 설정 파일)
my:
  app:
    name: My Awesome App
    version: 1.0.0
    enabled-features:
      - featureA
      - featureB
```

```java
// MyProperties.java (@ConfigurationProperties 클래스)
package com.example.config;

import java.util.List;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component; // 또는 @ConfigurationPropertiesScan이 스캔하는 패키지에 위치

@Component // 또는 @ConfigurationPropertiesScan으로 스캔
@ConfigurationProperties(prefix = "my.app")
public class MyProperties {
    private String name;
    private String version;
    private List<String> enabledFeatures;

    // Getter, Setter, toString... (Lombok으로 생성 가능)
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getVersion() { return version; }
    public void setVersion(String version) { this.version = version; }
    public List<String> getEnabledFeatures() { return enabledFeatures; }
    public void setEnabledFeatures(List<String> enabledFeatures) { this.enabledFeatures = enabledFeatures; }
}
```

```java
// MainApplication.java (메인 애플리케이션 클래스)
package com.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.ConfigurationPropertiesScan;
import org.springframework.context.ApplicationContext;

@SpringBootApplication
@ConfigurationPropertiesScan("com.example.config") // MyProperties가 위치한 패키지를 스캔
public class MainApplication {
    public static void main(String[] args) {
        ApplicationContext context = SpringApplication.run(MainApplication.class, args);
        MyProperties myProperties = context.getBean(MyProperties.class);
        System.out.println("App Name: " + myProperties.getName());
        System.out.println("App Version: " + myProperties.getVersion());
        System.out.println("Enabled Features: " + myProperties.getEnabledFeatures());
    }
}
```

---

## 3. 주요 차이점 비교

| 특징 | `@EnableAutoConfiguration` | `@ConfigurationPropertiesScan` |
| :--- | :--- | :--- |
| **목적** | 클래스패스/빈/프로퍼티 기반으로 **자동 구성 활성화** | `@ConfigurationProperties` 빈 **자동 등록 및 외부 설정 바인딩** |
| **도입 버전** | Spring Boot 1.0 (일반적으로 `@SpringBootApplication`에 포함) | **Spring Boot 2.2** |
| **작동 방식** | `META-INF/spring.factories`의 `@AutoConfiguration` 클래스 조건부 스캔 및 빈 등록 | `@ConfigurationProperties` 어노테이션이 붙은 클래스를 지정된 패키지에서 스캔하여 빈 등록 및 값 바인딩 |
| **영향 범위** | 애플리케이션의 전반적인 기능 (웹 서버, DB 연결, 메시징, 데이터 등) | 애플리케이션의 **커스텀 설정 값** 관리 |
| **사용 빈도** | `@SpringBootApplication` 덕분에 직접 명시할 일은 드a | 커스텀 설정 객체 (`@ConfigurationProperties`)를 사용할 때 유용 |

---

## 4. 용도 및 사용 시점

*   **`@EnableAutoConfiguration`:**
    *   **거의 항상 사용됩니다.** (명시적으로 사용하기보다는 `@SpringBootApplication`을 통해 암묵적으로 포함됨)
    *   Spring Boot의 핵심적인 "마법"을 제공하며, 개발자의 수고를 덜어주는 가장 중요한 기능입니다.
    *   애플리케이션의 기본적인 동작과 외부 라이브러리 통합을 자동화하는 데 사용됩니다.

*   **`@ConfigurationPropertiesScan`:**
    *   애플리케이션에 **도메인 특화된 커스텀 설정 프로퍼티 객체를 여러 개 정의**할 때 사용합니다.
    *   이 어노테이션이 없다면, 각 `@ConfigurationProperties` 클래스를 `@Component`로 선언하거나, `@EnableConfigurationProperties({MyProperties.class, OtherProperties.class})`와 같이 일일이 나열해야 합니다.
    *   `@ConfigurationPropertiesScan`을 사용하면 지정된 패키지(기본값은 메인 애플리케이션 클래스가 있는 패키지)만 스캔하도록 하여, 명시적으로 모든 커스텀 설정 빈을 등록할 필요 없이 코드를 깔끔하게 유지할 수 있습니다.

---

## 결론

두 어노테이션은 Spring Boot 애플리케이션의 설정을 다루지만, 그 초점이 다릅니다. `@EnableAutoConfiguration`은 **프레임워크 수준의 자동 구성**을 위한 것이고, `@ConfigurationPropertiesScan`은 **애플리케이션 개발자가 정의한 커스텀 설정**을 편리하게 관리하고 바인딩하기 위한 것입니다. 둘 다 현대적인 Spring Boot 애플리케이션 개발에 필수적인 도구입니다.
