# Java와 Python의 대용량 데이터 교환: Apache Arrow & mmap

Java(Spring Boot)와 Python 간에 대용량 데이터를 효율적으로 주고받기 위해 공유 메모리(mmap)와 Apache Arrow 포맷을 활용하는 방법을 정리합니다.

---

## 1. 배경: 왜 이 방식이 필요한가?

* **성능 병목**: REST API(JSON)나 gRPC는 데이터를 보낼 때 직렬화(Serialization)하고 받을 때 역직렬화하는 비용이 매우 큽니다. 데이터가 GB 단위라면 이 과정에서 시스템이 멈출 수 있습니다.
* **Zero-Copy**: Apache Arrow와 mmap을 사용하면 데이터를 복사하거나 변환하지 않고, 메모리 주소값만 참조하여 즉시 읽을 수 있습니다.

---

## 2. 주요 구성 요소

### 📦 Apache Arrow

* 언어에 무관한 **Columnar Memory Format**.
* Java에서 메모리에 적재한 구조 그대로 Python(Pandas)에서 즉시 읽을 수 있는 규격을 제공합니다.

### 📂 mmap (Memory-mapped File)

* 프로세스 간 공유 메모리 역할을 하는 파일 매핑 기술입니다.
* OS 수준에서 관리되므로 매우 빠르고 안정적입니다.

---

## 3. 구현 단계 (Workflow)

### Step 1: Java에서 데이터 준비 및 저장
Java에서 데이터를 생성하여 `.arrow` 파일로 기록합니다.

```java
// Maven 의존성: arrow-vector, arrow-memory-netty
BufferAllocator allocator = new RootAllocator();
// 스키마 정의 및 데이터 로드 (생략)
VectorSchemaRoot root = VectorSchemaRoot.create(schema, allocator);

File file = new File("data.arrow");
try (FileOutputStream fos = new FileOutputStream(file);
     ArrowFileWriter writer = new ArrowFileWriter(root, null, fos.getChannel())) {
    writer.start();
    writer.writeBatch();
    writer.end();
}
```

### Step 2: Java에서 Python 프로세스 호출
데이터가 준비되면 Java는 `ProcessBuilder`를 사용하여 Python 스크립트를 실행합니다. 이때 생성한 `.arrow` 파일의 경로를 인자로 전달합니다.

```java
public void callPythonProcessor(String arrowFilePath) throws Exception {
    // 1. 실행할 명령어 구성 (python3 script.py path/to/data.arrow)
    ProcessBuilder pb = new ProcessBuilder("python3", "processor.py", arrowFilePath);
    pb.inheritIO(); // Python의 로그를 Java 콘솔에서 바로 확인 가능

    // 2. 프로세스 실행
    Process process = pb.start();

    // 3. 작업 완료 대기 (필요 시 타임아웃 설정 권장)
    int exitCode = process.waitFor();
    
    if (exitCode == 0) {
        System.out.println("Python 처리 완료. 결과를 읽습니다.");
        // 결과 파일 또는 mmap 업데이트된 내용을 읽는 로직 수행
    } else {
        System.err.println("Python 처리 중 에러 발생. Exit Code: " + exitCode);
    }
}
```

### Step 3: Python에서 데이터 읽기 (Zero-Copy)
Python은 전달받은 경로를 통해 메모리 맵으로 파일을 엽니다.

```python
import sys
import pyarrow as pa
import pyarrow.ipc as ipc

def main(file_path):
    # 파일을 메모리 매핑으로 열기
    with pa.memory_map(file_path, 'r') as mmap:
        # IPC 포맷으로 데이터 로드
        table = ipc.open_file(mmap).read_all()
        df = table.to_pandas()
        
        # 처리 로직 수행 (예: AI 모델 추론 등)
        print(f"데이터 {len(df)}건 처리 중...")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
```

---

## 4. 성능 비교 및 고려사항

| 방식 | 특징 | 추천 상황 |
| :--- | :--- | :--- |
| **JSON/REST** | 구현이 쉬움, 데이터가 작음 | 수 MB 이하의 일반적인 API |
| **Apache Arrow + mmap** | **가장 빠름**, 복사 없음 | **수백 MB ~ 수 GB 단위 데이터 처리** |
| **gRPC/Protobuf** | 타입 안전, 네트워크 통신 | 서버 간 통신이 필요한 경우 |

### ⚠️ 주의사항

1. **동기화**: Java가 쓰는 동안 Python이 읽지 않도록 파일 락(Lock)이나 프로세스 실행 순서를 제어해야 합니다.
2. **메모리 관리**: Java의 `RootAllocator`에서 할당한 메모리는 명시적으로 `close()`해줘야 메모리 누수를 방지할 수 있습니다.
3. **버전 호환성**: Java와 Python이 사용하는 Apache Arrow 라이브러리 버전을 가급적 일치시키는 것이 좋습니다.

---

## 5. 결론

Spring Boot에서 수집한 대량의 데이터를 Python의 AI 모델이나 데이터 분석 라이브러리(Pandas, Scikit-learn)로 전달할 때 **Apache Arrow + mmap** 조합은 성능 면에서 타의 추종을 불허하는 최적의 솔루션입니다.
