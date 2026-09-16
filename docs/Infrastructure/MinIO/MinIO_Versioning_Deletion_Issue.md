# MinIO: 버저닝(Versioning) 활성화 후 파일이 영구 삭제되지 않는 이슈

버저닝을 켠 버킷에서 파일을 지웠는데도 디스크 사용량이 그대로일 수 있다. Java Client의 `removeObject`나 `mc rm`으로 삭제해도 이전 버전이 남기 때문이다. 파일이 안 보이는 상태와 저장된 데이터가 모두 지워진 상태를 구분해서 봐야 한다.

## 삭제했는데 용량이 줄지 않는 이유

버전 ID 없이 삭제를 요청하면 MinIO는 기존 데이터를 지우는 대신 삭제 마커(Delete Marker)를 만든다. 일반 조회에서는 객체가 사라진 것처럼 보이지만, 이전 버전은 여전히 보관되어 있다. 버저닝이 켜진 버킷의 정상 동작이다.

특정 버전을 영구 삭제하려면 그 버전의 ID를 지정해야 한다. 객체를 완전히 없애려면 남아 있는 모든 버전과 삭제 마커를 정리한다. 다만 보존 기간, Object Lock, 권한 때문에 삭제가 거절될 수 있다.

## Java Client로 버전별 대상 확인하기

Prefix 안의 모든 버전을 조회한 뒤 삭제할 대상을 정한다. SDK의 `listObjects(...includeVersions(true))`를 사용하면 버전 정보를 함께 얻을 수 있다. 사용하는 MinIO 서버와 SDK 버전도 확인해 둔다.

아래 코드는 구성된 `minioClient`를 사용하는 코드 조각이며, `dryRun = true` 상태에서는 목록만 출력한다. 삭제로 전환하기 전에 prefix, 보존 정책, 백업을 확인한다. 특정 버전을 영구 삭제하면 되돌릴 수 없다.

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

## mc로 대상 확인하기

CLI에서도 먼저 `--dry-run`으로 범위를 확인한다. 설치된 버전이 옵션을 지원하는지는 `mc rm --help`에서 확인할 수 있다.

```bash
# 조회 전용: 실제 삭제하지 않음
mc rm --recursive --versions --force --dry-run myminio/my-bucket/path/to/directory/
```

## 삭제 후 확인할 것

버전 목록을 다시 조회해 남은 항목과 실패한 요청을 확인한다. 동시에 파일을 쓰는 작업이 있으면 조회와 삭제 사이에 새 버전이 생길 수 있어, prefix 전체가 한 번에 삭제된다고 볼 수는 없다. API 응답과 실제 디스크 사용량도 각각 확인한다.

주기적으로 정리할 데이터라면 [Lifecycle 정책](Lifecycle.md)을 사용하는 방법도 있다. 현재 버전의 만료, 이전 버전의 만료, 만료된 삭제 마커 정리는 서로 다른 설정이다. 현재 버전의 Expiration만 설정하면 이전 버전이 남을 수 있으므로 필요한 보존 기간에 맞춰 확인한다.

## 참고 자료

- [MinIO Object Versioning Documentation](https://min.io/docs/minio/linux/administration/object-management/object-versioning.html)
- [MinIO mc rm 옵션](https://docs.min.io/aistor/reference/cli/mc-rm/): AIStor 문서이므로 Community 버전을 사용한다면 지원 옵션을 비교한다.
- [AWS S3: Deleting object versions](https://docs.aws.amazon.com/AmazonS3/latest/userguide/DeletingObjectVersions.html)
