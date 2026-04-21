# Scalar: 현대적이고 아름다운 API 문서화 도구 가이드

**Scalar**는 OpenAPI 사양을 시각화해주는 차세대 API 참조(Reference) 도구입니다. Swagger UI의 강력한 대안으로 부상하고 있으며, 특히 개발자 경험(DX)을 극대화한 UI/UX가 특징입니다.

---

## 1. Scalar의 주요 특징

* **현대적인 디자인**: 기본적으로 다크 모드를 지원하며, 군더더기 없고 깔끔한 3단 레이아웃을 제공합니다.
* **다양한 코드 스니펫**: 70개 이상의 프로그래밍 언어 및 라이브러리(JavaScript, Python, Java, Go 등)에 대한 요청 예제 코드를 즉시 생성해 줍니다.
* **통합 검색**: 문서 전체를 빠르게 검색할 수 있는 강력한 검색 기능을 내장하고 있습니다.
* **고성능**: 대규모 OpenAPI 사양 파일도 지연 없이 빠르게 렌더링합니다.
* **무료 및 오픈 소스**: 누구나 무료로 사용할 수 있으며 커스터마이징이 용이합니다.

---

## 2. Swagger UI vs Scalar 비교

| 기능 | Swagger UI | Scalar |
| :--- | :--- | :--- |
| **UI/UX** | 전통적, 세로 나열 방식 | 현대적, 3단 구성 레이아웃 |
| **코드 예제** | 제한적 (curl 위주) | **매우 풍부 (70+ 언어 지원)** |
| **테스트(Try it)** | 강력함 | 강력함 (인터페이스가 더 깔끔함) |
| **커스터마이징** | 다소 복잡함 | 테마 시스템으로 매우 쉬움 |

---

## 3. Spring Boot 연동 방법 (springdoc-openapi)

Spring Boot 프로젝트에서 기존의 Swagger 대신 Scalar를 사용하는 것은 매우 간단합니다.

### 3.1 의존성 추가 (Gradle)
기존 `springdoc-openapi-ui` 대신 또는 함께 사용할 수 있는 라이브러리들이 있으나, 가장 간단한 방법은 공식 Scalar CDN이나 전용 의존성을 활용하는 것입니다. (최근에는 `scalar-spring-boot` 라이브러리가 출시되었습니다.)

```gradle
dependencies {
    implementation 'io.github.scalar:scalar-spring-boot-starter:1.0.0'
}
```

### 3.2 기본 접속 주소
설정 후 애플리케이션을 실행하면 보통 다음 주소에서 Scalar UI를 확인할 수 있습니다.

* **주소**: `http://localhost:8080/scalar`

---

## 4. 다양한 환경에서의 사용법

### 4.1 HTML/CDN 방식 (가장 빠름)
별도의 백엔드 연동 없이도 정적 HTML 파일 하나만으로 OpenAPI 문서를 Scalar로 렌더링할 수 있습니다.

```html
<!doctype html>
<html>
  <head>
    <title>Scalar API Reference</title>
    <meta charset="utf-8" />
  </head>
  <body>
    <!-- OpenAPI JSON 주소를 넣어주기만 하면 끝! -->
    <script
      id="api-reference"
      data-url="https://api.example.com/v1/openapi.json"></script>
    <script src="https://cdn.jsdelivr.net/npm/@scalar/api-reference"></script>
  </body>
</html>
```

### 4.2 주요 설정 옵션

* **Theme**: `purple`, `moon`, `blueplanet` 등 다양한 테마 제공.
* **Layout**: `modern` (3단) 또는 `classic` (Swagger와 유사) 선택 가능.

---

## 5. 결론
내부 개발자용 문서로는 Swagger UI도 충분하지만, **외부 고객에게 제공하거나 팀 내 개발자 경험을 한 단계 높이고 싶다면 Scalar가 최선의 선택**입니다. 특히 풍부한 클라이언트 코드 스니펫 기능은 프론트엔드나 앱 개발자와의 협업 효율을 비약적으로 상승시켜 줍니다.
