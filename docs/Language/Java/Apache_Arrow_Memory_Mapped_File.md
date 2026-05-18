# Apache Arrow를 이용한 Java-Python 고성능 데이터 공유 가이드

Apache Arrow의 `arrow-memory`를 사용하여 Java에서 대용량 데이터를 메모리 맵 파일(mmap)로 생성하고, Python에서 Zero-copy로 읽어 처리하는 상세 구현 방법을 설명합니다.

---

## 1. Maven 설정 (`pom.xml`)

Apache Arrow를 사용하기 위해 필요한 핵심 의존성입니다. 메모리 할당을 위해 `netty` 엔진을 명시적으로 추가해야 합니다.

```xml
<dependencies>
    <!-- Apache Arrow Core -->
    <dependency>
        <groupId>org.apache.arrow</groupId>
        <artifactId>arrow-vector</artifactId>
        <version>14.0.1</version>
    </dependency>

    <!-- Memory Allocator (Netty) -->
    <dependency>
        <groupId>org.apache.arrow</groupId>
        <artifactId>arrow-memory-netty</artifactId>
        <version>14.0.1</version>
        <scope>runtime</scope>
    </dependency>

    <!-- Arrow Format (IPC용) -->
    <dependency>
        <groupId>org.apache.arrow</groupId>
        <artifactId>arrow-format</artifactId>
        <version>14.0.1</version>
    </dependency>
</dependencies>
```

---

## 2. Java (Spring Boot) 구현

### 💻 Data Producer 클래스
`VectorSchemaRoot`를 생성하고 데이터를 채운 뒤, `ArrowFileWriter`를 통해 파일로 기록합니다.

```java
import org.apache.arrow.memory.BufferAllocator;
import org.apache.arrow.memory.RootAllocator;
import org.apache.arrow.vector.IntVector;
import org.apache.arrow.vector.VarCharVector;
import org.apache.arrow.vector.VectorSchemaRoot;
import org.apache.arrow.vector.ipc.ArrowFileWriter;
import org.apache.arrow.vector.types.pojo.ArrowType;
import org.apache.arrow.vector.types.pojo.Field;
import org.apache.arrow.vector.types.pojo.FieldType;
import org.apache.arrow.vector.types.pojo.Schema;

import java.io.File;
import java.io.FileOutputStream;
import java.nio.channels.FileChannel;
import java.util.Arrays;

public class ArrowDataProducer {

    public void createArrowFile(String filePath) throws Exception {
        // 1. 메모리 할당자 생성 (애플리케이션당 하나 권장)
        try (BufferAllocator allocator = new RootAllocator()) {
            
            // 2. 스키마 정의 (ID: Int, Name: String)
            Field idField = new Field("id", FieldType.nullable(new ArrowType.Int(32, true)), null);
            Field nameField = new Field("name", FieldType.nullable(new ArrowType.Utf8()), null);
            Schema schema = new Schema(Arrays.asList(idField, nameField));

            // 3. VectorSchemaRoot 생성 (컨테이너)
            try (VectorSchemaRoot root = VectorSchemaRoot.create(schema, allocator)) {
                IntVector idVector = (IntVector) root.getVector("id");
                VarCharVector nameVector = (VarCharVector) root.getVector("name");

                // 4. 데이터 채우기
                int rowCount = 1000;
                idVector.allocateNew(rowCount);
                nameVector.allocateNew(rowCount);

                for (int i = 0; i < rowCount; i++) {
                    idVector.set(i, i);
                    nameVector.set(i, ("User_" + i).getBytes());
                }
                root.setRowCount(rowCount);

                // 5. 파일 기록 (IPC File Format)
                File file = new File(filePath);
                try (FileOutputStream fos = new FileOutputStream(file);
                     ArrowFileWriter writer = new ArrowFileWriter(root, null, fos.getChannel())) {
                    writer.start();
                    writer.writeBatch();
                    writer.end();
                }
            }
        }
    }
}
```

---

## 3. Python 처리기 구현 (`processor.py`)

Python에서는 `pyarrow`를 사용하여 파일을 메모리 맵으로 엽니다. 이 과정에서 데이터 복사는 발생하지 않습니다.

```python
import sys
import pyarrow as pa
import pyarrow.ipc as ipc

def process_arrow_file(file_path):
    # 1. 파일을 메모리 맵으로 열기
    with pa.memory_map(file_path, 'r') as mmap:
        # 2. IPC 파일 스트림 읽기
        with ipc.open_file(mmap) as reader:
            # 3. 테이블 로드 (Zero-copy)
            table = reader.read_all()
            df = table.to_pandas()
            
            # 처리 결과 출력
            print(f"✅ 수신된 데이터 로우 수: {len(df)}")
            print(df.head())

if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_arrow_file(sys.argv[1])
```

---

## 4. Java에서 Python 호출 (Spring Boot 서비스)

```java
@Service
public class AnalysisService {

    public void analyzeData() {
        String filePath = "/tmp/data.arrow";
        ArrowDataProducer producer = new ArrowDataProducer();

        try {
            // 1. Arrow 파일 생성
            producer.createArrowFile(filePath);

            // 2. Python 호출
            ProcessBuilder pb = new ProcessBuilder("python3", "processor.py", filePath);
            pb.inheritIO();
            Process process = pb.start();

            int exitCode = process.waitFor();
            if (exitCode == 0) {
                System.out.println("분석 성공");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

---

## 5. 핵심 메모리 관리 팁

1. **RootAllocator**: Arrow는 JVM 힙(Heap)이 아닌 **Direct Memory(Off-heap)**를 사용합니다. 따라서 JVM 옵션에서 `-XX:MaxDirectMemorySize`를 충분히 확보해야 합니다.
2. **Resource Closing**: `allocator`, `root`, `writer`는 모두 `AutoCloseable`을 구현하므로 `try-with-resources` 구문을 사용하여 반드시 닫아줘야 메모리 누수를 방지할 수 있습니다.
3. **Netty Allocator**: `arrow-memory-netty`는 성능이 가장 뛰어나지만, 특정 환경에서 의존성 충돌이 날 경우 `arrow-memory-unsafe`를 대안으로 사용할 수 있습니다.
