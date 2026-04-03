# MinIO 수명 주기 관리 (Lifecycle Management)

MinIO의 수명 주기 관리 기능은 버킷 내 객체들의 보관 기간을 설정하여, 일정 시간이 지나면 자동으로 객체를 삭제하거나 다른 스토리지 계층으로 이동시키는 기능입니다. 특히 **버저닝(Versioning)**이 활성화된 버킷에서 불필요하게 누적되는 과거 버전들을 관리하는 데 필수적입니다.

## 1. 주요 기능

* **Expiration (삭제)**: 지정된 날짜나 기간이 지나면 객체를 자동으로 영구 삭제합니다.
* **Transition (이동)**: 비용 절감을 위해 오래된 데이터를 더 저렴한 스토리지 계층(Warm/Cold Storage)으로 이동시킵니다. (주로 원격 티어링 설정 필요)
* **Noncurrent Version Management**: 최신 버전이 아닌 과거 버전들만 타겟팅하여 삭제하거나 이동시킬 수 있습니다.

---

## 2. MinIO Client (mc)를 이용한 설정

`mc ilm` (Information Lifecycle Management) 명령어를 사용합니다.

### 2.1 수명 주기 규칙 생성 (삭제)

```bash
# test-bucket 내의 모든 객체를 생성 후 30일 뒤에 자동 삭제하는 규칙 추가
mc ilm rule add myminio/test-bucket --expire-days 30

# 특정 폴더(logs/) 하위 객체만 7일 뒤에 삭제
mc ilm rule add myminio/test-bucket --prefix "logs/" --expire-days 7
```

### 2.2 과거 버전(Noncurrent) 전용 규칙 생성

버저닝 환경에서 가장 많이 쓰이는 설정으로, 파일이 업데이트되어 "과거 버전"이 된 지 10일이 지나면 삭제하도록 설정합니다.

```bash
mc ilm rule add myminio/test-bucket --noncurrent-expire-days 10
```

### 2.3 설정된 규칙 확인 및 삭제

```bash
# 규칙 목록 확인
mc ilm rule list myminio/test-bucket

# 특정 ID를 가진 규칙 삭제
mc ilm rule rm myminio/test-bucket --id "규칙ID"
```

---

## 3. Java Client 사용 예제

`minio-java` 라이브러리를 사용하여 프로그램 방식으로 수명 주기 정책을 적용하는 방법입니다.

```java
import io.minio.SetBucketLifecycleArgs;
import io.minio.messages.LifecycleConfiguration;
import io.minio.messages.LifecycleRule;
import io.minio.messages.Expiration;
import io.minio.messages.NoncurrentVersionExpiration;
import io.minio.messages.RuleFilter;
import io.minio.messages.Status;

import java.util.LinkedList;
import java.util.List;

public void setBucketLifecycle(String bucketName) throws Exception {
    List<LifecycleRule> rules = new LinkedList<>();

    // 규칙 1: 과거 버전이 된 지 30일 후 자동 삭제
    rules.add(new LifecycleRule(
            Status.ENABLED,
            null,
            new Expiration((Integer) null, (ZonedDateTime) null, (Boolean) null), // 최신 버전은 유지
            new RuleFilter(""), // 버킷 전체 대상
            "DeleteOldVersionsRule",
            null,
            null,
            new NoncurrentVersionExpiration(30) // 과거 버전 유지 기간
    ));

    minioClient.setBucketLifecycle(
            SetBucketLifecycleArgs.builder()
                    .bucket(bucketName)
                    .config(new LifecycleConfiguration(rules))
                    .build()
    );
    
    System.out.println(bucketName + " 버킷에 수명 주기 정책이 적용되었습니다.");
}
```

---

## 4. 활용 팁

* **삭제 마커 정리**: `mc ilm rule add` 시 `--expire-delete-marker` 옵션을 사용하면 데이터는 없고 마커만 남은 유령 객체들을 자동으로 청소할 수 있습니다.
* **Prefix 활용**: 모든 파일을 지우기보다 `temp/`, `cache/` 와 같이 임시 성격의 경로에만 짧은 Expiration 주기를 부여하는 것이 효율적입니다.
