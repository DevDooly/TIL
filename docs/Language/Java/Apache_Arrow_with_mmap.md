# Apache Arrow & mmap을 이용한 Zero-copy 데이터 공유

Apache Arrow의 열 지향 포맷과 OS의 `mmap` 기술을 결합하여, Java에서 생성한 대용량 데이터를 Python에서 메모리 복사 없이(Zero-copy) 즉시 읽어 처리하는 방법을 정리합니다.

---

## 1. 동작 원리

1. **Java**: 데이터를 Apache Arrow IPC 포맷으로 파일(또는 RAM 디스크)에 기록합니다.
2. **OS**: `mmap`은 디스크의 파일을 프로세스의 가상 메모리 주소 공간에 직접 매핑합니다.
3. **Python**: `pyarrow.memory_map`을 통해 파일의 내용을 메모리에 올리는 과정 없이 주소값만 참조하여 즉시 읽습니다.

> **💡 팁**: 리눅스 환경이라면 `/dev/shm` (공유 메모리 영역) 경로를 사용하여 물리적 디스크 I/O 조차 발생하지 않는 초고속 통신이 가능합니다.

---

## 2. Java: Arrow IPC 파일 생성 (Producer)

Java에서는 `ArrowFileWriter`를 사용하여 데이터를 저장합니다.

```java
import org.apache.arrow.memory.BufferAllocator;
import org.apache.arrow.memory.RootAllocator;
import org.apache.arrow.vector.IntVector;
import org.apache.arrow.vector.VectorSchemaRoot;
import org.apache.arrow.vector.ipc.ArrowFileWriter;
import org.apache.arrow.vector.types.pojo.ArrowType;
import org.apache.arrow.vector.types.pojo.Field;
import org.apache.arrow.vector.types.pojo.Schema;

import java.io.FileOutputStream;
import java.nio.channels.FileChannel;
import java.nio.file.Paths;
import java.util.Collections;

public class MmapArrowProducer {
    private static final BufferAllocator allocator = new RootAllocator();

    public void writeToMmap(String filePath) throws Exception {
        // 1. 스키마 정의
        Schema schema = new Schema(Collections.singletonList(
            Field.nullable("data", new ArrowType.Int(32, true))
        ));

        // 2. 데이터 생성 및 파일 쓰기
        try (VectorSchemaRoot root = VectorSchemaRoot.create(schema, allocator);
             FileOutputStream fos = new FileOutputStream(filePath);
             ArrowFileWriter writer = new ArrowFileWriter(root, null, fos.getChannel())) {
            
            IntVector vector = (IntVector) root.getVector("data");
            vector.allocateNew(1_000_000); // 100만 건

            for (int i = 0; i < 1_000_000; i++) {
                vector.set(i, i);
            }
            root.setRowCount(1_000_000);

            writer.start();
            writer.writeBatch();
            writer.end();
            
            System.out.println("✅ Arrow IPC 파일 생성 완료: " + filePath);
        }
    }
}
```

---

## 3. Python: mmap을 이용한 데이터 읽기 (Consumer)

Python의 `pyarrow` 라이브러리는 `mmap`을 기본적으로 지원하며, 이를 통해 수 GB의 데이터도 0.1초 내에 로드할 수 있습니다.

```python
import pyarrow as pa
import pyarrow.ipc as ipc
import time

def read_from_mmap(file_path):
    start_time = time.time()

    # 1. mmap으로 파일 열기 (Zero-copy)
    with pa.memory_map(file_path, 'r') as source:
        # 2. Arrow IPC 파일 스트림 읽기
        with ipc.open_file(source) as reader:
            table = reader.read_all()
            
            # 3. Pandas로 변환 (복사 거의 없음)
            df = table.to_pandas()
            
            print(f"✅ 데이터 로드 완료 (소요시간: {time.time() - start_time:.4f}s)")
            print(f"📊 로우 수: {len(df)}")
            print(df.head())

if __name__ == "__main__":
    read_from_mmap("data.arrow")
```

---

## 4. 성능 최적화 가이드

### 🚀 `/dev/shm` 활용 (Linux 전용)
파일 경로를 `/dev/shm/data.arrow`와 같이 설정하면, 데이터가 디스크가 아닌 **RAM**에 저장됩니다. 

* **장점**: 디스크 속도 제한을 무시하며, 프로세스 종료 시 자동으로 메모리에서 해제됩니다.
* **용도**: Java와 Python이 동일한 서버 내에서 작동할 때 최상의 속도를 보장합니다.

### 🛠️ JVM 옵션
메모리 매핑 및 Direct Memory 효율을 위해 다음 옵션을 권장합니다.

* `-XX:MaxDirectMemorySize=4G` (처리할 데이터 크기보다 넉넉하게 설정)
* `--add-opens=java.base/java.nio=ALL-UNNAMED` (Arrow 내부 최적화 허용)

---

## 5. 요약: 왜 이 조합인가?

| 비교 항목 | 일반 파일 (CSV/JSON) | Apache Arrow + mmap |
| :--- | :--- | :--- |
| **파싱 비용** | 텍스트 분석으로 매우 비쌈 | **없음** (메모리 주소 직접 참조) |
| **메모리 복사** | 힙(Heap) 메모리로 데이터 복사 발생 | **Zero-copy** (OS 수준 매핑) |
| **대용량 처리** | 메모리 부족 위험 | 데이터가 커도 가상 메모리 활용으로 안전 |

이 방식은 특히 **Java(Spring Boot)에서 수집한 실시간 로그/센서 데이터를 Python AI 모델로 전달**할 때 전 세계적으로 가장 많이 쓰이는 고성능 아키텍처입니다.
