# Java HttpClient · HttpRequest · HttpResponse 기반 JSON REST API 호출 예제

Java 11부터 표준 라이브러리에 포함된 `java.net.http.HttpClient`, `HttpRequest`, `HttpResponse`를 사용하면 별도의 HTTP 클라이언트 의존성 없이 REST API를 호출할 수 있다. 다만 JDK 표준 라이브러리는 JSON 파서를 내장하고 있지 않으므로, 실행 환경에 따라 Jackson·Gson 같은 라이브러리를 함께 쓰거나 단순 응답은 문자열·정규식으로 처리한다.

## 핵심 구성 요소와 동작 방식

| 클래스 | 역할 | 주요 설정 |
| :--- | :--- | :--- |
| `HttpClient` | 커넥션 풀과 프로토콜 버전, 연결 타임아웃을 관리하는 전송 주체 | `connectTimeout`, `version(HTTP_1_1 / HTTP_2)`, `followRedirects`. 스레드 안전하므로 매 요청마다 새로 만들지 않고 재사용한다. |
| `HttpRequest` | 요청 URI, HTTP 메서드, 헤더, 요청 본문(BodyPublisher), 응답 대기 타임아웃을 정의하는 불변 객체 | `uri`, `timeout`, `header("Content-Type", "application/json")`, `GET()`, `POST(BodyPublishers.ofString(...))` |
| `HttpResponse<T>` | 상태 코드, 응답 헤더, 변환된 응답 본문(BodyHandler 결과)을 담는 객체 | `statusCode()`, `headers()`, `body()`. `BodyHandlers.ofString(StandardCharsets.UTF_8)`로 JSON 문자열을 받는다. |

`HttpClient.send(...)`는 네트워크 오류나 타임아웃이 발생하면 `IOException`을 던지지만, **HTTP 상태 코드가 `400`, `404`, `500`이어도 예외를 던지지 않고 정상적으로 `HttpResponse`를 반환**한다. 따라서 JSON 파싱 전에 `response.statusCode()`가 `200~299` 범위인지 먼저 확인해야 한다.

## 1. 외부 의존성 없이 바로 실행 가능한 단일 파일 예제

아래 코드는 JDK 표준 라이브러리만 사용하여 로컬에 임시 JSON REST 서버(`HttpServer`)를 띄우고, `HttpClient`로 `GET` 조회와 `POST` 생성 요청을 보낸 뒤 JSON 응답을 받아 출력한다. JDK 17 이상(예제는 JDK 21 기준)에서 외부 서버나 Maven/Gradle 설정 없이 바로 컴파일해 동작을 확인할 수 있다.

```java
// 파일명: RestApiHttpClientExample.java
import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class RestApiHttpClientExample {

    private static final HttpClient CLIENT = HttpClient.newBuilder()
            .version(HttpClient.Version.HTTP_1_1)
            .connectTimeout(Duration.ofSeconds(5))
            .build();

    public static void main(String[] args) throws Exception {
        HttpServer server = startMockRestServer();
        int port = server.getAddress().getPort();
        String baseUrl = "http://127.0.0.1:" + port;

        try {
            // 1. GET 요청: 쿼리 파라미터 전달 및 JSON 응답 수신
            String encodedCategory = URLEncoder.encode("backend", StandardCharsets.UTF_8);
            HttpRequest getRequest = HttpRequest.newBuilder()
                    .uri(URI.create(baseUrl + "/api/items?category=" + encodedCategory + "&page=1"))
                    .timeout(Duration.ofSeconds(5))
                    .header("Accept", "application/json")
                    .GET()
                    .build();

            HttpResponse<String> getResponse = CLIENT.send(
                    getRequest,
                    HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8)
            );

            ensureSuccess(getResponse);
            String getJson = getResponse.body();
            System.out.println("[GET status] " + getResponse.statusCode());
            System.out.println("[GET body]   " + getJson);
            System.out.println("[GET total]  " + extractIntField(getJson, "total"));

            // 2. POST 요청: JSON 본문 전송 및 생성된 리소스 JSON 수신
            String requestBodyJson = """
                    {
                      "name": "wireless-keyboard",
                      "price": 89000
                    }
                    """.strip();

            HttpRequest postRequest = HttpRequest.newBuilder()
                    .uri(URI.create(baseUrl + "/api/items"))
                    .timeout(Duration.ofSeconds(5))
                    .header("Content-Type", "application/json; charset=UTF-8")
                    .header("Accept", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(requestBodyJson, StandardCharsets.UTF_8))
                    .build();

            HttpResponse<String> postResponse = CLIENT.send(
                    postRequest,
                    HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8)
            );

            ensureSuccess(postResponse);
            String postJson = postResponse.body();
            System.out.println("[POST status] " + postResponse.statusCode());
            System.out.println("[POST body]   " + postJson);
            System.out.println("[POST id]     " + extractStringField(postJson, "id"));
        } finally {
            server.stop(0);
        }
    }

    private static void ensureSuccess(HttpResponse<String> response) {
        int status = response.statusCode();
        if (status < 200 || status >= 300) {
            throw new IllegalStateException(
                    "HTTP 요청 실패: status=" + status + ", body=" + response.body()
            );
        }
    }

    private static int extractIntField(String json, String fieldName) {
        Pattern pattern = Pattern.compile("\"" + Pattern.quote(fieldName) + "\"\\s*:\\s*(-?\\d+)");
        Matcher matcher = pattern.matcher(json);
        if (!matcher.find()) {
            throw new IllegalArgumentException("숫자 필드를 찾을 수 없습니다: " + fieldName);
        }
        return Integer.parseInt(matcher.group(1));
    }

    private static String extractStringField(String json, String fieldName) {
        Pattern pattern = Pattern.compile("\"" + Pattern.quote(fieldName) + "\"\\s*:\\s*\"([^\"]*)\"");
        Matcher matcher = pattern.matcher(json);
        if (!matcher.find()) {
            throw new IllegalArgumentException("문자열 필드를 찾을 수 없습니다: " + fieldName);
        }
        return matcher.group(1);
    }

    private static HttpServer startMockRestServer() throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
        server.createContext("/api/items", exchange -> {
            String method = exchange.getRequestMethod();
            String responseJson;
            int statusCode;

            if ("GET".equalsIgnoreCase(method)) {
                statusCode = 200;
                responseJson = "{\"page\":1,\"total\":2,\"data\":[{\"id\":\"item-1\",\"name\":\"mouse\"},{\"id\":\"item-2\",\"name\":\"monitor\"}]}";
            } else if ("POST".equalsIgnoreCase(method)) {
                String reqBody = new String(exchange.getRequestBody().readAllBytes(), StandardCharsets.UTF_8);
                String name = extractStringField(reqBody, "name");
                int price = extractIntField(reqBody, "price");
                statusCode = 201;
                responseJson = "{\"id\":\"item-3\",\"name\":\"" + name + "\",\"price\":" + price + ",\"created\":true}";
            } else {
                statusCode = 405;
                responseJson = "{\"error\":\"Method Not Allowed\"}";
            }

            byte[] bytes = responseJson.getBytes(StandardCharsets.UTF_8);
            exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
            exchange.sendResponseHeaders(statusCode, bytes.length);
            try (OutputStream os = exchange.getResponseBody()) {
                os.write(bytes);
            }
        });
        server.start();
        return server;
    }
}
```

컴파일 후 실행하면 다음과 같이 출력된다.

```bash
javac -encoding UTF-8 RestApiHttpClientExample.java
java RestApiHttpClientExample
```

```text
[GET status] 200
[GET body]   {"page":1,"total":2,"data":[{"id":"item-1","name":"mouse"},{"id":"item-2","name":"monitor"}]}
[GET total]  2
[POST status] 201
[POST body]   {"id":"item-3","name":"wireless-keyboard","price":89000,"created":true}
[POST id]     item-3
```

정규식 추출 방식은 중첩 배열이나 이스케이프된 따옴표(`\"`)가 포함된 JSON에서는 깨질 수 있으므로, 외부 라이브러리를 사용할 수 없는 제한된 환경에서 최상위 단순 필드를 읽을 때만 제한적으로 사용한다.

## 2. 실무 환경: Jackson `ObjectMapper`와 `record`를 결합한 예제

실무 프로젝트에서는 Jackson(`com.fasterxml.jackson.core:jackson-databind`)의 `ObjectMapper`를 사용해 Java `record`와 JSON 문자열을 변환한다. 알 수 없는 필드가 응답에 추가되어도 역직렬화가 실패하지 않도록 `@JsonIgnoreProperties(ignoreUnknown = true)`를 함께 붙인다.

```java
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.List;
import java.util.concurrent.CompletableFuture;

public class JacksonRestApiClient {

    private final HttpClient httpClient;
    private final ObjectMapper objectMapper;
    private final String baseUrl;

    public JacksonRestApiClient(String baseUrl) {
        this.baseUrl = baseUrl;
        this.httpClient = HttpClient.newBuilder()
                .connectTimeout(Duration.ofSeconds(5))
                .build();
        this.objectMapper = new ObjectMapper();
    }

    @JsonIgnoreProperties(ignoreUnknown = true)
    public record ItemResponse(String id, String name, int price) {}

    public record CreateItemRequest(String name, int price) {}

    @JsonIgnoreProperties(ignoreUnknown = true)
    public record PageResponse<T>(int page, int totalPages, List<T> data) {}

    // 동기 GET: 페이지 응답 JSON을 제네릭 레코드로 역직렬화
    public PageResponse<ItemResponse> getItems(int page) throws IOException, InterruptedException {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/api/items?page=" + page))
                .timeout(Duration.ofSeconds(5))
                .header("Accept", "application/json")
                .GET()
                .build();

        HttpResponse<String> response = httpClient.send(
                request,
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8)
        );

        if (response.statusCode() < 200 || response.statusCode() >= 300) {
            throw new IllegalStateException("GET 실패: status=" + response.statusCode());
        }

        return objectMapper.readValue(
                response.body(),
                new TypeReference<PageResponse<ItemResponse>>() {}
        );
    }

    // 동기 POST: 요청 객체를 JSON으로 직렬화해 전송하고 생성 결과를 역직렬화
    public ItemResponse createItem(CreateItemRequest payload) throws IOException, InterruptedException {
        String requestJson = objectMapper.writeValueAsString(payload);

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/api/items"))
                .timeout(Duration.ofSeconds(5))
                .header("Content-Type", "application/json; charset=UTF-8")
                .header("Accept", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(requestJson, StandardCharsets.UTF_8))
                .build();

        HttpResponse<String> response = httpClient.send(
                request,
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8)
        );

        if (response.statusCode() != 200 && response.statusCode() != 201) {
            throw new IllegalStateException("POST 실패: status=" + response.statusCode());
        }

        return objectMapper.readValue(response.body(), ItemResponse.class);
    }

    // 비동기 GET: sendAsync와 CompletableFuture를 이용한 논블로킹 호출
    public CompletableFuture<ItemResponse> getItemAsync(String itemId) {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/api/items/" + itemId))
                .timeout(Duration.ofSeconds(5))
                .header("Accept", "application/json")
                .GET()
                .build();

        return httpClient.sendAsync(request, HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8))
                .thenApply(response -> {
                    if (response.statusCode() < 200 || response.statusCode() >= 300) {
                        throw new IllegalStateException("비동기 조회 실패: status=" + response.statusCode());
                    }
                    try {
                        return objectMapper.readValue(response.body(), ItemResponse.class);
                    } catch (IOException e) {
                        throw new java.io.UncheckedIOException(e);
                    }
                });
    }
}
```

## 3. 코딩테스트·배치에서 자주 쓰는 페이지네이션 JSON 집계 패턴

온라인 코딩테스트(HackerRank REST API 문항 등)나 외부 API 수집 작업에서는 `page=1`을 먼저 호출해 전체 페이지 수(`total_pages`)를 확인한 뒤, 마지막 페이지까지 순회하며 조건에 맞는 데이터를 집계하는 패턴이 자주 나온다. 온라인 저지 환경에는 보통 `com.google.gson.Gson`(`JsonParser`, `JsonObject`, `JsonArray`)이 기본 포함되므로 아래와 같이 작성할 수 있다.

```java
// Gson(com.google.gson.*)이 클래스패스에 있는 환경의 페이지 순회 예시 (발췌)
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;

public class PaginatedRestApiExample {

    private static final HttpClient CLIENT = HttpClient.newHttpClient();

    public static int sumPriceOverThreshold(String baseUrl, String category, int minPrice) throws Exception {
        String encodedCategory = URLEncoder.encode(category, StandardCharsets.UTF_8);
        int page = 1;
        int totalPages = 1;
        int sum = 0;

        while (page <= totalPages) {
            String url = baseUrl + "?category=" + encodedCategory + "&page=" + page;
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(url))
                    .header("Accept", "application/json")
                    .GET()
                    .build();

            HttpResponse<String> response = CLIENT.send(
                    request,
                    HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8)
            );

            JsonObject root = JsonParser.parseString(response.body()).getAsJsonObject();
            totalPages = root.get("total_pages").getAsInt();
            JsonArray data = root.getAsJsonArray("data");

            for (JsonElement element : data) {
                JsonObject item = element.getAsJsonObject();
                int price = item.get("price").getAsInt();
                if (price >= minPrice) {
                    sum += price;
                }
            }
            page++;
        }
        return sum;
    }
}
```

## 작성 시 주의할 점

- **쿼리 파라미터 URL 인코딩**: 검색어나 카테고리 이름에 공백(` `), 한글, `&`, `=` 같은 문자가 들어가면 `URI.create(...)`에서 `IllegalArgumentException`이 발생한다. 쿼리 파라미터 값은 `URLEncoder.encode(value, StandardCharsets.UTF_8)`로 인코딩한 뒤 URI 문자열에 결합한다.
- **`connectTimeout`과 요청별 `timeout` 분리**: `HttpClient.newBuilder().connectTimeout(...)`은 TCP/TLS 핸드셰이크 연결 시간만 제한한다. 서버가 연결만 맺고 응답 본문을 보내지 않는 현상(Read Timeout)을 막으려면 `HttpRequest.newBuilder().timeout(...)`도 함께 설정해야 한다.
- **인터럽트 상태 복원**: `client.send(...)`는 블로킹 호출이므로 `InterruptedException`을 던진다. 예외를 잡아서 별도 런타임 예외로 감싸 던질 때는 `Thread.currentThread().interrupt()`를 호출해 스레드의 인터럽트 플래그를 유지한다.

## 관련 문서

- [Java 11 주요 변경점 (Standard HTTP Client API)](Versions/Java11.md)
- [올리브영 HackerRank Java 코딩테스트 준비](HackerRank_Coding_Test_Preparation.md)
- [Java 문서 모음](README.md)
