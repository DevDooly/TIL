# MinIO 수명 주기 관리 (Lifecycle / ILM)

MinIO의 수명 주기 관리(Information Lifecycle Management, ILM)는 버킷 내 객체의 보존 기간을 정의하여, 일정 기간이 지나면 자동으로 객체를 만료(삭제), 스토리지 계층 이동(티어링), 또는 임시 파트 정리를 수행하는 기능입니다. 특히 **버저닝(Versioning)**이 활성화된 환경에서 불필요한 스토리지 누수를 방지하기 위해 필수적입니다.

---

## 1. 핵심 개념

* **Expiration (만료/삭제)**: 지정된 기간(Days)이나 날짜가 경과한 객체를 자동으로 수명 주기 정책에 따라 만료 처리합니다.
* **Transition (계층화 / Tiering)**: 비용 절감을 위해 오래된 데이터를 저렴한 스토리지 계층(Warm/Cold Storage)으로 자동 이동시킵니다.
* **Noncurrent Version Expiration (과거 버전 만료)**: 최신 버전이 아닌 과거 버전(Noncurrent) 객체들만 타겟팅하여 영구 삭제합니다.
* **Delete Marker Expiration (삭제 마커 정리)**: 모든 과거 버전이 삭제되고 더 이상 참조할 데이터가 없는 고아(Orphaned) 삭제 마커를 정리합니다.
* **Abort Incomplete Multipart Uploads**: 업로드 도중 중단된 대용량 파일의 임시 파트를 지정 기간 후 정리하여 용량 낭비를 방지합니다.

---

## 2. Versioning 유무에 따른 Lifecycle 정책 동작 차이점 (중요)

버킷의 Versioning 활성화 여부에 따라 동일한 만료 정책이라도 내부 동작 방식이 완전히 다릅니다.

| 비교 항목 | Versioning 미활성화 (Off) | Versioning 활성화 (Enabled) |
| :--- | :--- | :--- |
| **객체 상태 구조** | 단일 최신 객체만 존재 (`VersionId: null`) | 최신 버전(Current) + 과거 버전들(Noncurrent) + Delete Marker |
| **`--expire-days` 만료 동작** | 지정 기간 경과 시 **객체가 즉시 영구 삭제**됨 | 지정 기간 경과 시 객체가 지워지지 않고 **Delete Marker가 생성**됨 (실제 원본 데이터는 Noncurrent로 보존되어 용량 차지) |
| **과거 버전(Noncurrent) 처리** | 과거 버전이 존재하지 않으므로 불필요 | **필수**: `--noncurrent-version-expiration-days`를 설정하지 않으면 과거 버전이 영구 보존되어 스토리지 누수 발생 |
| **Delete Marker 처리** | Delete Marker가 생성되지 않음 | **권장**: 과거 버전이 모두 정리된 후 남은 **Delete Marker 정리(`--expire-delete-marker`)** 필요 |
| **권장 ILM 정책 조합** | `--expire-days` 단독 설정 | `--expire-days` + `--noncurrent-version-expiration-days` + `--expire-delete-marker` |

> **⚠️ 주의 사항 (스토리지 누수 방지)**  
> Versioning 버킷에서 단순히 `--expire-days`만 적용하면, 만료 시점에 실제 파일이 삭제되는 것이 아니라 **Delete Marker만 추가**되어 이전 버전 데이터가 스토리지에 계속 남아있게 됩니다.  
> 반드시 **`--noncurrent-version-expiration-days`** 옵션을 함께 설정해야 과거 버전이 실제로 영구 삭제되어 용량이 회수됩니다.

---

## 3. MinIO Client (`mc`)를 이용한 정책 관리

`mc ilm` (Information Lifecycle Management) 및 `mc version` 명령어를 사용하여 수명 주기와 버저닝을 관리합니다.

### 3.1 버킷 Versioning 확인 및 설정

```bash
# Versioning 상태 확인
mc version info myminio/mybucket

# Versioning 활성화
mc version enable myminio/mybucket

# Versioning 일시정지 (기존 버전 유지, 신규 객체는 null 버전)
mc version suspend myminio/mybucket
```

### 3.2 Lifecycle 규칙 조회

```bash
# 버킷에 설정된 수명주기 규칙 목록 조회
mc ilm rule ls myminio/mybucket
# 또는 축약형
mc ilm ls myminio/mybucket
```

### 3.3 Lifecycle 규칙 추가 (`mc ilm rule add`)

#### 상황 A: Versioning 미사용 버킷 (단순 객체 만료)
객체 생성 후 30일이 지나면 영구 삭제:
```bash
mc ilm rule add --expire-days 30 myminio/mybucket
```

#### 상황 B: Versioning 활성화 버킷 (완결형 권장 설정)
* 현재 버전: 30일 경과 시 만료 (Delete Marker 생성)
* 과거 버전: 과거 버전(Noncurrent)으로 전환된 후 7일 뒤 영구 삭제
* 삭제 마커: 과거 버전이 모두 사라진 Delete Marker 자동 영구 삭제
* 미완료 멀티파트: 5일 이상 방치된 미완료 멀티파트 업로드 임시 데이터 정리

```bash
mc ilm rule add \
  --expire-days 30 \
  --noncurrent-version-expiration-days 7 \
  --expire-delete-marker \
  --abort-incomplete-multipart-upload-days 5 \
  myminio/mybucket
```

#### 상황 C: 최신 N개 버전 유지 및 이전 버전 만료
과거 버전 중 최신 3개 버전은 보존하고, 7일이 지난 그 이전 버전들만 삭제:
```bash
mc ilm rule add \
  --noncurrent-version-expiration-days 7 \
  --noncurrent-version-newer 3 \
  myminio/mybucket
```

#### 상황 D: 특정 접두사(Prefix) 또는 태그(Tags) 대상 정책
`logs/` 디렉터리 하위 객체만 14일 뒤 만료:
```bash
mc ilm rule add --prefix "logs/" --expire-days 14 myminio/mybucket
```

`temp=true` 태그가 설정된 객체만 1일 뒤 만료:
```bash
mc ilm rule add --tags "temp=true" --expire-days 1 myminio/mybucket
```

### 3.4 Lifecycle 규칙 삭제 (`mc ilm rule rm`)

```bash
# 1. 규칙 목록 조회를 통해 Rule ID 확인
mc ilm rule ls myminio/mybucket

# 2. 특정 Rule ID에 해당하는 규칙 삭제
mc ilm rule rm --id "<RULE_ID>" myminio/mybucket

# 3. 버킷 내 모든 수명주기 규칙 일괄 삭제
mc ilm rule rm --all --force myminio/mybucket
```

### 3.5 JSON 파일을 이용한 일괄 Export / Import

```bash
# 1. 기존 규칙을 JSON 파일로 내보내기
mc ilm rule export myminio/mybucket > lifecycle_rules.json

# 2. 파일 수정 후 버킷에 정책 가져오기
mc ilm rule import myminio/mybucket < lifecycle_rules.json
```

---

## 4. Java Client 사용 예제

`minio-java` 라이브러리를 사용하여 수명 주기 정책을 적용하는 예시입니다.

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

    // 과거 버전으로 전환된 지 7일 후 영구 삭제
    rules.add(new LifecycleRule(
            Status.ENABLED,
            null,
            new Expiration((Integer) null, null, null), // 최신 버전 유지
            new RuleFilter(""),                          // 버킷 전체 대상
            "ExpireNoncurrentVersionsRule",
            null,
            null,
            new NoncurrentVersionExpiration(7)           // 과거 버전 7일 후 삭제
    ));

    minioClient.setBucketLifecycle(
            SetBucketLifecycleArgs.builder()
                    .bucket(bucketName)
                    .config(new LifecycleConfiguration(rules))
                    .build()
    );
    
    System.out.println(bucketName + " 버킷에 수명 주기 정책이 성공적으로 적용되었습니다.");
}
```

---

## 5. 실무 운영 모범 사례 (Best Practices)

1. **미완료 멀티파트 업로드 자동 정리 필수화**:
   - 네트워크 단절이나 클라이언트 오류로 중단된 대용량 업로드 파트는 버킷에 은닉되어 스토리지를 지속 점유합니다. 모든 버킷에 `--abort-incomplete-multipart-upload-days 5~7` 설정을 기본 적용하는 것이 좋습니다.
2. **Delete Marker 정리 (`--expire-delete-marker`)**:
   - 과거 버전이 모두 삭제되더라도 Delete Marker 메타데이터가 남아있으면 불필요한 메타데이터 인덱스 부하를 유발합니다.
3. **스캐너 순회 주기 고려**:
   - MinIO ILM은 백그라운드 스캐너에 의해 비동기로 동작하므로 만료 조건 만족 즉시 삭제되는 것이 아니라 스캐너 순회 시점에 정리됩니다.
