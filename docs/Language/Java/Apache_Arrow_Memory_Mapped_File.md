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

### 💻 Data Consumer 클래스
기록된 `.arrow` 파일을 `ArrowFileReader`를 통해 읽어 Java 객체(Vector)로 복원합니다.

```java
import org.apache.arrow.memory.BufferAllocator;
import org.apache.arrow.memory.RootAllocator;
import org.apache.arrow.vector.IntVector;
import org.apache.arrow.vector.VarCharVector;
import org.apache.arrow.vector.VectorSchemaRoot;
import org.apache.arrow.vector.ipc.ArrowFileReader;

import java.io.File;
import java.io.FileInputStream;
import java.nio.charset.StandardCharsets;

public class ArrowDataConsumer {

    public void readArrowFile(String filePath) throws Exception {
        File file = new File(filePath);
        
        try (BufferAllocator allocator = new RootAllocator();
             FileInputStream fis = new FileInputStream(file);
             ArrowFileReader reader = new ArrowFileReader(fis.getChannel(), allocator)) {

            // 1. VectorSchemaRoot 로드 (스키마 정보 포함)
            VectorSchemaRoot root = reader.getVectorSchemaRoot();
            
            // 2. 모든 레코드 배치(Record Batch) 순회
            while (reader.loadNextBatch()) {
                int rowCount = root.getRowCount();
                IntVector idVector = (IntVector) root.getVector("id");
                VarCharVector nameVector = (VarCharVector) root.getVector("name");

                for (int i = 0; i < rowCount; i++) {
                    int id = idVector.get(i);
                    String name = new String(nameVector.get(i), StandardCharsets.UTF_8);
                    System.out.println("ID: " + id + ", Name: " + name);
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

## 6. 트러블슈팅: FlatBuffers 버전 충돌

### ⚠️ `FlatBufferBuilder.createString` 에러
`ArrowFileWriter.write` 호출 시 `NoSuchMethodError: ... FlatBufferBuilder.createString(CharSequence)` 에러가 발생한다면, 이는 Arrow와 FlatBuffers 라이브러리 간의 버전 불일치 때문입니다.

* **원인**: Apache Arrow 18.x 버전은 내부적으로 **FlatBuffers 24.3.25** 버전에 의존합니다. 프로젝트의 다른 라이브러리나 명시적 선언으로 인해 25.x 이상의 최신 FlatBuffers가 로드되면 메서드 시그니처가 달라 에러가 발생합니다.
* **해결**: `pom.xml`에서 FlatBuffers 버전을 **24.3.25**로 강제 고정하세요.

```xml
<dependency>
    <groupId>com.google.flatbuffers</groupId>
    <artifactId>flatbuffers-java</artifactId>
    <version>24.3.25</version>
</dependency>
```

### 💡 기타 팁

1. **Direct Memory**: Arrow는 JVM Heap이 아닌 Off-heap을 사용하므로 `-XX:MaxDirectMemorySize` 설정을 잊지 마세요.
2. **Resource Closing**: `allocator`, `root` 등은 반드시 `try-with-resources`로 닫아야 합니다.

