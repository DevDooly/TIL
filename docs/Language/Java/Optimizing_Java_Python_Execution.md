# Java-Python 실행 성능 최적화 가이드

Java에서 `ProcessBuilder`를 통해 Python을 실행할 때 속도가 느린 원인을 분석하고, 성능을 획기적으로 개선할 수 있는 아키텍처 패턴을 정리합니다.

---

## 1. 성능 저하의 주원인: 프로세스 기동 오버헤드

`ProcessBuilder`로 `python3 script.py`를 실행할 때마다 OS는 다음과 같은 작업을 반복합니다.

1. **OS Fork**: 새로운 프로세스 생성 및 메모리 할당.
2. **인터프리터 로드**: Python 실행 엔진 기동.
3. **라이브러리 임포트**: `import pandas`, `import torch` 등 무거운 라이브러리 로드 (**가장 큰 병목, 약 0.5s~2s 소요**).

멀티스레드에서 동시에 10번 호출하면 위 과정이 10번 독립적으로 발생하며 CPU와 메모리 자원을 급격히 소모합니다.

---

## 2. 최적화 전략 1: 영구 실행 워커 패턴 (Persistent Worker)

프로세스를 매번 종료하지 않고, 한 번 띄워놓은 뒤 **표준 입력(stdin)과 표준 출력(stdout)**을 통해 계속 대화하는 방식입니다.

### 💻 Python: 무한 루프 대기 스크립트
```python
import sys
import json

# 무거운 라이브러리를 최초 1회만 로드
import pandas as pd 

def process(data):
    # 비즈니스 로직
    return {"result": "success", "echo": data}

while True:
    # Java가 표준 입력으로 보낸 데이터를 읽음
    line = sys.stdin.readline()
    if not line: break
    
    input_data = json.loads(line)
    result = process(input_data)
    
    # 결과를 표준 출력으로 반환
    print(json.dumps(result), flush=True)
```

### 💻 Java: 프로세스 유지 및 스트림 통신
```java
public class PythonWorker {
    private Process process;
    private BufferedWriter writer;
    private BufferedReader reader;

    public void start() throws Exception {
        process = new ProcessBuilder("python3", "worker.py").start();
        writer = new BufferedWriter(new OutputStreamWriter(process.getOutputStream()));
        reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
    }

    public String sendRequest(String json) throws Exception {
        writer.write(json + "\n");
        writer.flush();
        return reader.readLine(); // 결과 수신
    }
}
```

---

## 3. 최적화 전략 2: FastAPI를 이용한 로컬 서버 (추천 ⭐)

Python 쪽을 가벼운 HTTP 서버(FastAPI)로 띄우고, Java에서 `WebClient`나 `RestTemplate`으로 호출하는 방식입니다.

* **장점**: 
    * 라이브러리가 메모리에 상주하여 응답 속도가 압도적으로 빠름 (ms 단위).
    * 동시성 처리를 Python 서버 내부에서 효율적으로 관리.
    * 운영 환경 배포 및 모니터링이 용이함.
* **단점**: 별도의 서버 포트를 관리해야 함.

---

## 4. 최적화 전략 3: JNI 기반의 Jep (Java Embedded Python)

Java 프로세스 내부(JVM)에 Python 인터프리터를 임베딩하여 직접 호출하는 방식입니다.

* **장점**: 데이터 복사(Serialization) 비용이 거의 없고 프로세스 기동 시간이 0에 수렴.
* **단점**: C-Extension 관련 라이브러리 충돌 가능성, 네이티브 설정이 복잡함.

---

## 5. 비교 및 결론

| 방식 | 기동 오버헤드 | 구현 난이도 | 데이터 전송 비용 | 추천 상황 |
| :--- | :--- | :--- | :--- | :--- |
| **ProcessBuilder** | **매우 높음** | 매우 낮음 | 보통 | 단발성, 아주 가끔 실행 |
| **Persistent Worker** | 낮음 | 보통 | 낮음 | 단순 연산 반복 처리 |
| **FastAPI (HTTP)** | **거의 없음** | 보통 | 보통 | **대부분의 MSA/웹 환경** |
| **Jep (Embedded)** | 없음 | 높음 | **매우 낮음** | 대용량 데이터, 초고성능 필요 |

### 💡 최종 가이드

1. 단순히 실행 시간이 문제라면 **전략 2(FastAPI)**를 가장 먼저 고려하세요. 가장 안정적이고 성능 개선 폭이 큽니다.
2. 네트워크 포트를 열 수 없는 폐쇄망의 특수 환경이라면 **전략 1(영구 워커)**을 사용하세요.
3. 멀티스레드 호출 시에는 Java 측에서 `ExecutorService`를 사용하여 **동시 실행 프로세스 개수를 CPU 코어 수 이내로 제한**하는 것이 필수입니다.
