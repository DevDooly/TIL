# Apache Maven: 자바 빌드 자동화 도구 가이드

**Maven**은 자바 기반 프로젝트의 빌드, 의존성 관리, 프로젝트 생명주기 관리 등을 자동화해주는 빌드 도구입니다. XML 기반의 `pom.xml` 파일을 사용하여 프로젝트의 구조와 설정을 정의합니다.

---

## 1. Maven 표준 디렉토리 구조

Maven은 "Convention over Configuration(설정보다 관습)" 원칙을 따르므로, 표준 구조를 지키는 것이 중요합니다.

* `src/main/java`: 자바 소스 코드
* `src/main/resources`: 자바 리소스 파일 (XML, Properties 등)
* `src/test/java`: 테스트 소스 코드
* `src/test/resources`: 테스트 리소스 파일
* `target`: 빌드 결과물이 생성되는 위치
* `pom.xml`: 프로젝트 정보 및 설정 파일

---

## 2. pom.xml 주요 태그 설명

`pom.xml`은 프로젝트 객체 모델(Project Object Model)의 약자로, 프로젝트의 모든 설정을 담고 있습니다.

### 2.1 프로젝트 식별 (GAV)

* **`<groupId>`**: 프로젝트를 생성한 조직이나 그룹의 고유 아이디 (보통 도메인 역순).
* **`<artifactId>`**: 프로젝트의 이름 (빌드 결과물 파일 이름의 기반).
* **`<version>`**: 프로젝트의 현재 버전 (예: `1.0.0-SNAPSHOT`).

### 2.2 설정 및 의존성

* **`<packaging>`**: 빌드 결과물의 형식 (`jar`, `war`, `pom` 등). 기본값은 `jar`.
* **`<properties>`**: `pom.xml` 내부에서 전역 변수처럼 사용할 값 정의 (예: 자바 버전, 라이브러리 버전).
* **`<dependencies>`**: 프로젝트에서 사용하는 외부 라이브러리 목록을 정의합니다.
    * **`<dependency>`**: 개별 라이브러리 설정.
    * **`<scope>`**: 라이브러리가 적용될 범위 (`compile`, `test`, `provided`, `runtime` 등).

### 2.3 빌드 및 플러그인

* **`<build>`**: 빌드 프로세스에 대한 상세 설정을 포함합니다.
    * **`<plugins>`**: 컴파일러 설정, 리소스 처리 등 빌드 단계에서 실행될 플러그인 정의.
* **`<repositories>`**: 라이브러리를 다운로드할 원격 저장소 설정 (기본은 Maven Central).

---

## 3. Maven 생명주기 (Lifecycle)

Maven은 정해진 순서대로 빌드 단계를 수행합니다.

1. **clean**: 이전 빌드 결과물(`target`) 삭제.
2. **validate**: 프로젝트 상태 확인 및 필요한 정보 로드.
3. **compile**: 소스 코드 컴파일.
4. **test**: 유닛 테스트 실행.
5. **package**: 컴파일된 코드를 `jar` 등 패키지로 압축.
6. **verify**: 패키지의 유효성 검사.
7. **install**: 로컬 저장소(`.m2`)에 패키지 설치 (다른 로컬 프로젝트에서 사용 가능).
8. **deploy**: 원격 저장소에 최종 패키지 배포.

---

## 4. 자주 사용하는 Maven 명령어

터미널에서 실행하는 주요 명령어들입니다.

```bash
# 1. 빌드 결과물 삭제 및 새로 패키징
mvn clean package

# 2. 테스트를 건너뛰고 설치
mvn install -DskipTests

# 3. 특정 프로파일 적용하여 컴파일
mvn compile -P production

# 4. 의존성 트리 확인 (라이브러리 충돌 해결 시 유용)
mvn dependency:tree
```

---

## 5. 요약
Maven은 정해진 규칙(표준 구조 및 생명주기)을 통해 프로젝트 관리를 일관되게 유지해 줍니다. 특히 `pom.xml`을 통한 체계적인 의존성 관리는 자바 생태계의 표준으로 자리 잡고 있습니다.
