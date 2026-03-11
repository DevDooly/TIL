# MinIO Java Client 사용 예제

Java에서 `minio-java` 라이브러리를 사용하여 MinIO 스토리지와 상호작용하는 방법, 특히 **버저닝(Versioning)이 활성화된 버킷**에서의 객체 제어 방법을 다룹니다.

## 의존성 추가 (Maven/Gradle)

```xml
<!-- pom.xml -->
<dependency>
    <groupId>io.minio</groupId>
    <artifactId>minio</artifactId>
    <version>8.5.7</version> <!-- 최신 버전 사용 권장 -->
</dependency>
```

```gradle
// build.gradle
implementation 'io.minio:minio:8.5.7'
```

---

## 1. MinioClient 초기화

```java
import io.minio.MinioClient;

public class MinioService {
    private final MinioClient minioClient;

    public MinioService() {
        this.minioClient = MinioClient.builder()
                .endpoint("http://localhost:9000")
                .credentials("YOUR_ACCESS_KEY", "YOUR_SECRET_KEY")
                .build();
    }
}
```

---

## 2. 버저닝 환경에서의 객체 삭제 (Remove Objects)

버저닝이 활성화된 버킷에서 객체를 삭제할 때는 두 가지 시나리오가 있습니다.

### 2.1 일반 삭제 (Delete Marker 추가)
`versionId`를 지정하지 않고 호출하면, 실제 데이터가 삭제되는 대신 **삭제 마커(Delete Marker)**가 최신 버전으로 쌓입니다.

```java
import io.minio.RemoveObjectArgs;

public void deleteObject(String bucketName, String objectName) throws Exception {
    minioClient.removeObject(
            RemoveObjectArgs.builder()
                    .bucket(bucketName)
                    .object(objectName)
                    .build()
    );
    System.out.println(objectName + " 객체에 삭제 마커가 추가되었습니다.");
}
```

### 2.2 특정 버전 영구 삭제 (Hard Delete)
특정 버전의 데이터를 물리적으로 완전히 삭제하려면 **`versionId`**를 명시해야 합니다.

```java
public void deleteSpecificVersion(String bucketName, String objectName, String versionId) throws Exception {
    minioClient.removeObject(
            RemoveObjectArgs.builder()
                    .bucket(bucketName)
                    .object(objectName)
                    .versionId(versionId) // 영구 삭제를 위해 버전 ID 명시
                    .build()
    );
    System.out.println("버전 " + versionId + " 객체가 영구 삭제되었습니다.");
}
```

### 2.3 여러 객체/버전 일괄 영구 삭제

```java
import io.minio.RemoveObjectsArgs;
import io.minio.Result;
import io.minio.messages.DeleteError;
import io.minio.messages.DeleteObject;
import java.util.LinkedList;
import java.util.List;

public void deleteMultipleVersions(String bucketName, List<DeleteObject> objectsToDelete) throws Exception {
    Iterable<Result<DeleteError>> results = minioClient.removeObjects(
            RemoveObjectsArgs.builder()
                    .bucket(bucketName)
                    .objects(objectsToDelete)
                    .build()
    );

    for (Result<DeleteError> result : results) {
        DeleteError error = result.get();
        System.out.println("삭제 실패: " + error.objectName() + " / " + error.message());
    }
}
```

---

## 3. 기타 유용한 기능 (버저닝 관련)

### 3.1 특정 객체의 모든 버전 목록 조회

```java
import io.minio.ListObjectsArgs;
import io.minio.Result;
import io.minio.messages.Item;

public void listObjectVersions(String bucketName, String objectName) throws Exception {
    Iterable<Result<Item>> results = minioClient.listObjects(
            ListObjectsArgs.builder()
                    .bucket(bucketName)
                    .prefix(objectName) // 특정 파일명 지정
                    .includeVersions(true) 
                    .build()
    );

    for (Result<Item> result : results) {
        Item item = result.get();
        if (item.objectName().equals(objectName)) {
            System.out.println("버전 ID: " + item.versionId());
            System.out.println("최신 여부: " + item.isLatest());
            System.out.println("삭제 마커 여부: " + item.isDeleteMarker());
            System.out.println("-------------------------");
        }
    }
}
```

### 3.2 임시 다운로드 링크 생성 (Presigned URL)

```java
import io.minio.GetPresignedObjectUrlArgs;
import io.minio.http.Method;
import java.util.concurrent.TimeUnit;

public String generatePresignedUrl(String bucketName, String objectName, String versionId) throws Exception {
    return minioClient.getPresignedObjectUrl(
            GetPresignedObjectUrlArgs.builder()
                    .method(Method.GET)
                    .bucket(bucketName)
                    .object(objectName)
                    .versionId(versionId) // null 이면 최신 버전, 명시하면 특정 버전
                    .expiry(1, TimeUnit.HOURS)
                    .build()
    );
}
```