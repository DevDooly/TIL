# Java/Spring Boot와 Python 연동 가이드

Java 애플리케이션에서 Python의 강력한 라이브러리(AI, 데이터 분석 등)를 활용해야 할 때 사용할 수 있는 주요 연동 전략 3가지를 소개합니다.

---

## 1. ProcessBuilder를 이용한 직접 호출

Java에서 시스템 명령어를 실행하여 Python 스크립트를 직접 구동하는 방식입니다. 별도의 서버 구성 없이 간단하게 연동할 때 사용합니다.

### 💻 Java 코드 예시
```java
public String executePython(String inputData) throws Exception {
    ProcessBuilder pb = new ProcessBuilder("python3", "script.py", inputData);
    Process process = pb.start();

    // 결과 읽기
    BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
    return reader.readLine();
}
```

* **장점**: 설정이 매우 단순함.
* **단점**: 매번 프로세스를 띄워야 하므로 오버헤드가 큼. 대량 요청 처리에 부적합.

---

## 2. HTTP API 연동 (가장 추천)

Python 측을 별도의 가벼운 웹 서버(FastAPI, Flask)로 띄우고, Spring Boot에서 `RestTemplate`이나 `WebClient`로 호출하는 방식입니다.

### 💻 Python (FastAPI) 코드 예시
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/process")
def process_data(data: str):
    # Python 특화 로직 수행
    return {"result": f"Processed {data}"}
```

### 💻 Java (Spring Boot) 호출 예시
```java
@Service
public class PythonApiService {
    private final WebClient webClient = WebClient.create("http://python-api:8000");

    public Mono<String> getResult(String data) {
        return webClient.get()
                .uri(uriBuilder -> uriBuilder.path("/process").queryParam("data", data).build())
                .retrieve()
                .bodyToMono(String.class);
    }
}
```

* **장점**: 확장성이 좋고(MSA), 각각 독립적인 배포 및 관리가 가능함. 가장 안정적인 방식.
* **단점**: 네트워크 오버헤드가 발생함.

---

## 3. gRPC 또는 메시지 큐(Kafka/RabbitMQ) 연동

실시간 고성능 처리가 필요하거나 대량의 데이터를 비동기로 처리해야 할 때 사용합니다.

* **gRPC**: 프로토콜 버퍼를 사용해 매우 빠른 바이너리 통신 수행.
* **Kafka**: Spring Boot가 데이터를 던져두면 Python 워커가 가져가서 처리하고 다시 결과를 던지는 파이프라인 구성.

---

## 4. 상황별 선택 가이드

| 상황 | 추천 방식 |
| :--- | :--- |
| **단발성, 간단한 계산** | **ProcessBuilder** |
| **지속적인 서비스, API 서버 형태** | **HTTP API (FastAPI)** |
| **대규모 데이터, AI 모델 추론** | **gRPC** 또는 **Kafka** |
| **함수 단위의 직접 공유** | **JNI/Jep** (난이도 높음, 비권장) |

---

## 5. 결론

현대적인 개발 환경에서는 **방법 2(HTTP API)** 방식을 가장 권장합니다. **FastAPI**는 파이썬에서 가장 빠르고 간결하게 API를 만들 수 있는 도구이며, Spring Boot와의 연동도 매우 직관적입니다. 

만약 파이썬 스크립트가 실행되는 환경과 자바 서버가 동일한 로컬 환경이라면 **ProcessBuilder**로 시작해 보시는 것도 좋은 출발점입니다.
