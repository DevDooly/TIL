# MinIO: 버저닝(Versioning) 활성화 후 파일이 영구 삭제되지 않는 이슈

MinIO 버켓에 버저닝 기능을 활성화한 후, 기존 방식으로 파일을 삭제했음에도 불구하고 디스크 용량이 줄어들지 않거나 파일이 '삭제 마커(Delete Marker)' 상태로 남아있는 이슈와 해결 과정을 정리합니다.

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
2. **영구 삭제 조건**: 데이터를 물리적으로 삭제하려면 **모든 버전(Version ID)을 각각 명시하여 삭제**해야 합니다.

---

## 3. 해결 방법 (How)

디렉토리(Prefix) 내의 모든 파일과 그에 딸린 모든 버전들을 조회하여 하나씩 영구 삭제하는 로직을 적용했습니다.

### 3.1 Java Client를 이용한 조치
단순히 `removeObject`를 호출하는 것이 아니라, `listObjectVersions`를 통해 모든 버전을 긁어온 뒤 삭제해야 합니다.

```java
// 모든 버전 정보를 가져와서 삭제 목록 구성
Iterable<Result<Item>> results = minioClient.listObjects(
    ListObjectsArgs.builder()
        .bucket("my-bucket")
        .prefix("path/to/directory/")
        .includeVersions(true) // 모든 버전 포함 필수!
        .recursive(true)
        .build()
);

for (Result<Item> result : results) {
    Item item = result.get();
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
터미널에서 즉시 처리해야 할 경우 `--versions` 옵션을 사용합니다.

```bash
# 특정 경로 하위의 모든 버전과 삭제 마커를 강제 삭제
mc rm --recursive --versions --force myminio/my-bucket/path/to/directory/
```

---

## 4. 결과 및 제언

* **결과**: 삭제 마커를 포함한 모든 데이터 조각이 물리적으로 제거되어 디스크 공간이 확보됨.
* **제언**: 
    * 버저닝이 필요한 버켓이라면 **Lifecycle(생명주기)** 정책을 설정하여 '삭제 마커'나 '오래된 버전'이 일정 기간 후 자동으로 영구 삭제되도록 구성하는 것이 운영상 안전합니다.
    * 수동 삭제 로직 작성 시 `includeVersions(true)` 옵션 사용 여부를 반드시 확인해야 합니다.

---

## 5. 관련 레퍼런스

* [MinIO Object Versioning Documentation](https://min.io/docs/minio/linux/administration/object-management/object-versioning.html)
* [AWS S3: Deleting object versions](https://docs.aws.amazon.com/AmazonS3/latest/userguide/DeletingObjectVersions.html)
