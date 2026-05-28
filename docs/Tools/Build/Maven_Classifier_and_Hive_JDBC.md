# Maven Classifier와 Hive-JDBC Standalone 활용 가이드

Maven의 `classifier` 개념을 이해하고, 특히 의존성 충돌이 심한 `hive-jdbc`를 안정적으로 사용하는 방법을 정리합니다.

---

## 1. Maven Classifier란?

**Classifier**는 동일한 `GAV`(GroupId, ArtifactId, Version) 좌표를 가진 아티팩트 내에서 서로 다른 구성이나 용도를 가진 파일을 구분하기 위해 사용되는 식별자입니다.

### 📂 구성 형식
`artifactId-version-classifier.jar`

### 💡 주요 용도

* **자매품 제공**: `sources`(소스 코드), `javadoc`(문서)
* **환경별 최적화**: `linux-x86_64`, `windows-x86_64` (Native 라이브러리 등)
* **의존성 통합**: `standalone`, `all`, `shaded` (모든 의존성을 포함한 Fat JAR)

---

## 2. Hive-JDBC와 Standalone Classifier

Hive를 Java 애플리케이션에 연동할 때 가장 큰 문제는 **Hadoop 에코시스템의 방대한 의존성**입니다.

### ⚠️ 일반적인 연동 시 문제점
`hive-jdbc`를 일반적인 방식으로 추가하면 Hadoop, Zookeeper, Guava, Jetty 등 수십 개의 라이브러리가 함께 로드됩니다. 이 과정에서 프로젝트의 기존 라이브러리와 버전이 겹쳐 `NoSuchMethodError`나 `ClassNotFoundException`이 빈번하게 발생합니다.

### ✅ 해결책: `standalone` 사용
Hive 측에서는 이러한 의존성 지옥을 해결하기 위해 필요한 모든 클래스를 하나로 묶고 패키지 경로를 재배치(Shading)한 **Standalone** 버전을 제공합니다.

### 💻 설정 방법 (`pom.xml`)
```xml
<dependency>
    <groupId>org.apache.hive</groupId>
    <artifactId>hive-jdbc</artifactId>
    <version>3.1.3</version>
    <!-- 핵심 설정: standalone 변종을 사용함 -->
    <classifier>standalone</classifier>
</dependency>
```

---

## 3. 실무 적용 팁

1. **의존성 청소**: `standalone`을 적용했다면, 기존에 Hive 연결을 위해 추가했던 다른 Hadoop 관련 의존성들을 과감히 제거하세요. Standalone JAR 하나가 모든 역할을 대신합니다.
2. **버전 매칭**: Hive 서버의 버전과 JDBC 드라이버의 버전을 가급적 일치시키는 것이 정신 건강에 이롭습니다.
3. **Excluded Dependencies**: 만약 `standalone` 내부에 포함된 특정 라이브러리가 여전히 문제를 일으킨다면, `<exclusions>`를 통해 명시적으로 제외해야 할 수도 있습니다.

---

## 4. 요약

* **Classifier**는 동일 버전의 아티팩트 중 특수 목적(소스, 통합본 등) 파일을 찾을 때 사용한다.
* **hive-jdbc:standalone**은 의존성 충돌을 방지하기 위해 모든 필요 라이브러리를 내장한 Uber-JAR이다.
* Hadoop/Hive 연동 시 발생하는 대부분의 라이브러리 충돌은 `standalone` 분류자 하나로 해결 가능하다.
