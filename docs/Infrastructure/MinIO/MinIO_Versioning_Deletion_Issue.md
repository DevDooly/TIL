# MinIO: 버저닝(Versioning) 활성화 후 파일이 영구 삭제되지 않는 이슈

MinIO 버켓에 버저닝 기능을 활성화한 후, 기존 방식으로 파일을 삭제했음에도 불구하고 디스크 용량이 줄어들지 않거나 파일이 '삭제 마커(Delete Marker)' 상태로 남아있는 이슈와 해결 과정을 정리합니다.

확인일: 2026-09-07. 버전 보존은 버저닝의 정상 동작이며, 그 자체를 스토리지 누수라고 단정하지 않습니다. 사용 중인 MinIO 서버와 SDK/CLI 버전을 함께 기록합니다.

---

## 1. 이슈 배경 (Context)

* **상황**: 데이터 관리 정책에 따라 특정 디렉토리의 파일들을 삭제하려 함.
* **환경**: MinIO 클러스터, Bucket Versioning 활성 상태.
* **문제**: Java Client의 `removeObject` 또는 `mc rm` 명령어를 사용했으나, 파일이 실제로 삭제되지 않고 '이전 버전'으로 보관되거나 삭제 마커만 생성됨.

---

## 2. 원인 분석 (Why)

MinIO(및 S3 호환 스토리지)에서 버저닝이 활성화되면 삭제 동작이 다음과 같이 변경됩니다.

1. **단순 삭제 요청**: 특정 버전 ID를 명시하지 않고 삭제를 요청하면, 실제 데이터를 지우는 대신 **삭제 마커(Delete Marker)**라는 특별한 포인터를 생성합니다. 
    * 사용자 눈에는 파일이 삭제된 것처럼 보이지만, 실제 데이터는 여전히 디스크에 존재합니다.
2. **버전별 삭제**: 특정 버전만 제거하려면 해당 Version ID를 지정합니다. 객체 전체를 없애려면 보존된 모든 버전과 삭제 마커를 정리해야 합니다. 보존 기간·Object Lock·권한에 따라 삭제가 거절될 수 있습니다.

---

## 3. 해결 방법 (How)

디렉토리(Prefix) 내의 모든 파일과 그에 딸린 모든 버전들을 조회하여 하나씩 영구 삭제하는 로직을 적용했습니다.

### 3.1 Java Client를 이용한 조치
Java SDK의 `listObjects(...includeVersions(true))`로 버전별 대상을 확인합니다. 아래 코드 조각은 기본적으로 목록만 출력합니다. 삭제는 되돌릴 수 없으므로 대상 prefix·보존 정책·백업을 확인한 후 별도 실행 단계에서 수행합니다.

```java
// 모든 버전 정보를 가져와서 삭제 목록 구성
String prefix = "path/to/directory/";
boolean dryRun = true;
if (prefix.isBlank() || prefix.equals("/") || !prefix.endsWith("/")) {
    throw new IllegalArgumentException("명시적인 하위 prefix가 필요합니다.");
}
Iterable<Result<Item>> results = minioClient.listObjects(
    ListObjectsArgs.builder()
        .bucket("my-bucket")
        .prefix(prefix)
        .includeVersions(true) // 모든 버전 포함 필수!
        .recursive(true)
        .build()
);

for (Result<Item> result : results) {
    Item item = result.get();
    if (item.versionId() == null || item.versionId().isBlank()) {
        throw new IllegalStateException("Version ID가 없는 항목은 삭제하지 않습니다.");
    }
    System.out.printf("%s version=%s%n", item.objectName(), item.versionId());
    if (dryRun) {
        continue;
    }
    // 특정 파일의 특정 버전 ID를 명시하여 영구 삭제
    minioClient.removeObject(
        RemoveObjectArgs.builder()
            .bucket("my-bucket")
            .object(item.objectName())
            .versionId(item.versionId()) // Version ID 지정이 핵심
            .build()
    );
}
```

### 3.2 MinIO Client(mc)를 이용한 조치
CLI에서도 먼저 `--dry-run`으로 대상을 확인합니다. 설치한 `mc rm --help`에서 지원 옵션을 확인합니다.

```bash
# 조회 전용: 실제 삭제하지 않음
mc rm --recursive --versions --force --dry-run myminio/my-bucket/path/to/directory/
```

---

## 4. 결과 및 제언

* **확인**: 버전 목록을 다시 조회해 삭제 결과와 실패 항목을 확인합니다. 동시 쓰기가 있으면 목록과 삭제 사이에 새 버전이 생길 수 있으므로 prefix 단위 삭제를 원자적 작업으로 간주하지 않습니다. API 성공과 실제 디스크 사용량 변화도 각각 관찰합니다.
* **제언**: 
    * **Lifecycle**에서 현재 버전 만료, noncurrent version 만료, expired delete marker 정리를 구분합니다. 현재 버전의 Expiration만으로 이전 버전이 모두 제거되지는 않습니다. 필요한 보존 기간에 맞춰 정책을 검증합니다.
    * 수동 삭제 로직 작성 시 `includeVersions(true)` 옵션 사용 여부를 반드시 확인해야 합니다.

---

## 5. 관련 레퍼런스

* [MinIO Object Versioning Documentation](https://min.io/docs/minio/linux/administration/object-management/object-versioning.html)
* [MinIO mc rm 옵션](https://docs.min.io/aistor/reference/cli/mc-rm/) — 현재 AIStor 문서로 연결되므로 사용 중인 Community/AIStor 버전의 차이를 확인합니다.
* [AWS S3: Deleting object versions](https://docs.aws.amazon.com/AmazonS3/latest/userguide/DeletingObjectVersions.html)
