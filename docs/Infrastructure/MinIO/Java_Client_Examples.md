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

버저닝이 활성화된 버킷에서 단순히 `RemoveObjectArgs`를 이름만 주어 호출하면, 파일이 실제로 삭제되지 않고 **삭제 마커(Delete Marker)**가 추가됩니다. 
특정 버전을 완전히 영구 삭제(Hard Delete)하려면 **`versionId`**를 반드시 명시해야 합니다.

### 2.1 단일 객체 특정 버전 영구 삭제

```java
import io.minio.RemoveObjectArgs;

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

### 2.2 여러 객체/버전 일괄 영구 삭제 (RemoveObjects)

여러 개의 버전을 한 번에 영구 삭제할 때는 `RemoveObjectsArgs`와 `DeleteObject` 객체를 사용합니다.

```java
import io.minio.RemoveObjectsArgs;
import io.minio.Result;
import io.minio.messages.DeleteError;
import io.minio.messages.DeleteObject;

import java.util.LinkedList;
import java.util.List;

public void deleteMultipleVersions(String bucketName) throws Exception {
    List<DeleteObject> objectsToDelete = new LinkedList<>();
    
    // 삭제할 객체와 그 특정 버전 ID를 리스트에 추가
    objectsToDelete.add(new DeleteObject("sample.txt", "version-id-1"));
    objectsToDelete.add(new DeleteObject("sample.txt", "version-id-2"));
    objectsToDelete.add(new DeleteObject("image.png", "version-id-3"));

    Iterable<Result<DeleteError>> results = minioClient.removeObjects(
            RemoveObjectsArgs.builder()
                    .bucket(bucketName)
                    .objects(objectsToDelete)
                    .build()
    );

    // 에러 확인 (removeObjects는 Lazy 실행이므로 Iteration 시점에 삭제가 수행됨)
    for (Result<DeleteError> result : results) {
        DeleteError error = result.get();
        System.out.println("삭제 실패: " + error.objectName() + " / 이유: " + error.message());
    }
}
```

---

## 3. 기타 유용한 기능 (버저닝 관련)

### 3.1 객체의 모든 버전 목록 조회 (List Versions)

버저닝이 활성화된 버킷에서 삭제 마커를 포함한 파일의 모든 히스토리(버전들)를 조회하는 방법입니다. `ListObjectsArgs`에서 `includeVersions(true)`를 설정해야 합니다.

```java
import io.minio.ListObjectsArgs;
import io.minio.Result;
import io.minio.messages.Item;

public void listAllVersions(String bucketName, String objectPrefix) throws Exception {
    Iterable<Result<Item>> results = minioClient.listObjects(
            ListObjectsArgs.builder()
                    .bucket(bucketName)
                    .prefix(objectPrefix) // 특정 파일명이나 폴더 경로
                    .includeVersions(true) // 핵심: 모든 버전을 가져옴
                    .build()
    );

    for (Result<Item> result : results) {
        Item item = result.get();
        System.out.println("파일명: " + item.objectName());
        System.out.println("버전 ID: " + item.versionId());
        System.out.println("최신 여부: " + item.isLatest());
        System.out.println("삭제 마커 여부: " + item.isDeleteMarker());
        System.out.println("크기: " + item.size());
        System.out.println("-------------------------");
    }
}
```

### 3.2 임시 다운로드 링크 생성 (Presigned URL)

특정 버전의 파일을 외부 사용자가 웹 브라우저 등에서 다운로드할 수 있도록 한시적으로 유효한 URL을 생성합니다.

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
                    .versionId(versionId) // 특정 버전을 지정하여 다운로드 링크 생성
                    .expiry(1, TimeUnit.HOURS) // 1시간 동안만 유효
                    .build()
    );
}
```
