# Java 11: The Cloud Native LTS Standard

Java 11은 Java 8 이후 출시된 첫 번째 **LTS (Long-Term Support)** 버전으로, 모듈 시스템(Java 9) 도입 이후의 안정성과 클라우드 환경에 최적화된 기능들을 제공합니다.

## 1. Local-Variable Type Inference (`var`)

Java 10에서 처음 도입되어 Java 11에서 표준이 된 기능입니다. 컴파일러가 변수의 타입을 추론하게 하여 코드를 간결하게 만듭니다.

```java
// 기존
String message = "Hello, Java 11";
List<String> list = new ArrayList<>();

// var 사용
var message = "Hello, Java 11"; // String으로 추론
var list = new ArrayList<String>(); // ArrayList<String>으로 추론
```
- **주의:** 지역 변수에만 사용할 수 있으며, 가독성을 해치지 않는 선에서 사용하는 것이 권장됩니다.

---

## 2. Standard HTTP Client API

Java 9에서 인큐베이팅 프로젝트로 시작되어 Java 11에서 표준 API로 승격되었습니다. 기존의 `HttpURLConnection`을 대체하며, 비동기 처리 및 HTTP/2를 지원합니다.

```java
HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.github.com/"))
    .build();

// 동기 방식
HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
System.out.println(response.body());

// 비동기 방식
client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
    .thenApply(HttpResponse::body)
    .thenAccept(System::println);
```

---

## 3. String & File API 개선

문자열 처리를 위한 유용한 메서드들이 추가되었습니다.

- **String:**
  - `isBlank()`: 공백 문자열인지 확인
  - `lines()`: 줄 단위로 분리하여 스트림 반환
  - `strip()`: 앞뒤 공백 제거 (Unicode 공백 포함)
  - `repeat(n)`: 문자열 n번 반복
- **Files:**
  - `writeString()`: 파일에 문자열 쓰기
  - `readString()`: 파일에서 문자열 읽기

---

## 4. Single-File Source Code 실행

컴파일 과정(`javac`) 없이 소스 코드 파일 하나를 바로 실행할 수 있게 되었습니다. 간단한 스크립트 작성 시 유용합니다.

```bash
# HelloWorld.java 파일을 바로 실행
java HelloWorld.java
```

---

## 5. ZGC & Epsilon GC 도입

- **ZGC (Z Garbage Collector):** 대용량 메모리(TB 단위)에서도 일시 정지 시간(Pause Time)을 10ms 이하로 유지하도록 설계된 저지연 GC입니다. (Java 11에서는 실험적 도입)
- **Epsilon GC:** "아무것도 하지 않는" GC입니다. 성능 테스트나 수명이 매우 짧은 애플리케이션에 사용됩니다.
