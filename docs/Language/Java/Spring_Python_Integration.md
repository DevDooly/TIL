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

## 6. 수행 시간이 긴 로직 처리 전략 (Long-Running Tasks)

Python 로직(AI 모델 추론, 대량 데이터 처리 등)이 수 초에서 수 분 이상 소요될 경우, 기존의 **동기식(Synchronous) 방식**은 심각한 문제를 야기할 수 있습니다.

### ⚠️ 동기 호출 시 발생하는 문제

* **스레드 차단(Thread Blocking)**: Spring Boot의 Tomcat 스레드가 Python 작업이 끝날 때까지 대기 상태가 되어, 동시 접속자가 많아질 경우 서버 전체가 응답 불능 상태에 빠질 수 있습니다.
* **타임아웃 관리 어려움**: 네트워크나 프로세스 수준의 타임아웃 설정을 정교하게 관리하지 않으면, 좀비 프로세스가 생성되거나 연결이 강제로 끊길 수 있습니다.
* **리소스 고갈**: 요청마다 프로세스를 생성하거나 긴 시간 스레드를 점유하는 것은 메모리와 CPU에 큰 부담을 줍니다.

### ✅ 권장 해결 방안

#### A. Spring `@Async`를 이용한 비동기 호출
가장 간단한 방법으로, Spring의 스레드 풀을 사용하여 호출 자체를 비동기로 만듭니다.

* **방식**: 클라이언트는 즉시 응답(202 Accepted)을 받고, 작업은 백그라운드에서 진행됩니다.
* **코드 예시**:
    ```java
    @Async
    public CompletableFuture<String> runLongPythonTask(String data) {
        // ProcessBuilder 또는 WebClient 호출 로직
        return CompletableFuture.completedFuture(result);
    }
    ```

#### B. 비동기 작업 큐 (Python Side) + Polling/Webhook
Python 서버(FastAPI/Flask) 내부에 **Celery**나 **RQ** 같은 작업 큐를 도입합니다.

* **흐름**: Spring -> Python API (작업 등록) -> 즉시 Task ID 반환 -> Python 워커가 백그라운드 처리 -> Spring에서 상태 확인(Polling) 또는 Python이 결과 알림(Webhook).

#### C. 메시지 큐(Message Queue) 도입 (가장 견고한 방식)
Spring Boot와 Python 사이에 RabbitMQ, Kafka, Redis Pub/Sub 등을 둡니다.

* **장점**: 두 서비스 간의 결합도가 가장 낮으며, Python 워커를 자유롭게 확장(Scale-out)할 수 있습니다.
* **구조**: `[Spring Boot] --(Job)--> [RabbitMQ] --(Process)--> [Python Worker]`

---

## 7. 결론 및 요약

| 상황 | 추천 방식 | 비고 |
| :--- | :--- | :--- |
| **짧은 작업 (1~2초 내)** | **HTTP API (FastAPI)** | 가장 직관적이고 표준적임 |
| **긴 작업 (5초 이상)** | **비동기 큐 (Celery/RabbitMQ)** | 시스템 안정성을 위해 필수 |
| **단발성/단순 실행** | **ProcessBuilder** | 오버헤드 주의 |

단순히 "동작하는 것"이 목표라면 직접 호출도 가능하지만, **운영 환경과 확장성**을 고려한다면 **FastAPI를 이용한 HTTP API 방식**이나 **메시지 큐를 통한 비동기 처리**를 강력히 권장합니다.
