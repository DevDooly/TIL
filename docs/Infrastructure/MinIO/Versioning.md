# MinIO 버저닝 (Versioning)

MinIO의 버저닝(Versioning) 기능은 동일한 객체(파일)에 대해 여러 버전을 유지할 수 있게 해주는 데이터 보호 및 관리 기능입니다. Amazon S3의 버저닝 스펙과 완벽히 호환됩니다.

---

## 1. 버저닝의 주요 이점

* **실수 복구**: 사용자가 실수로 객체를 덮어쓰거나 삭제하더라도 이전 버전을 즉시 복원할 수 있습니다.
* **랜섬웨어 및 변조 방지**: 악의적인 공격으로 데이터가 변조되거나 암호화되더라도, 변경 전 버전을 살려낼 수 있습니다.
* **변경 이력 추적 및 감사**: 파일의 변경 과정을 시간에 따라 추적하고 보관해야 하는 규정 준수(Compliance) 요구사항을 충족합니다.

---

## 2. 작동 방식 및 상태 (Status)

버저닝은 **버킷(Bucket)** 단위로 활성화(Enabled)하거나 일시 정지(Suspended)할 수 있습니다. 기본 상태는 비활성화(`Off`)입니다.

| 상태 | 설명 |
| :--- | :--- |
| **Off** (기본) | 버전 관리가 꺼져 있으며, 덮어쓰기 시 기존 데이터가 즉시 대체됩니다. |
| **Enabled** | 모든 생성, 수정, 삭제 작업마다 고유한 Version ID가 부여되어 관리됩니다. |
| **Suspended** | 버전 관리를 일시 정지합니다. 기존 버전은 유지되나 신규 객체는 `VersionId: null`로 저장됩니다. |

### 2.1 파일 덮어쓰기 (Overwrite)
* 버저닝이 **비활성화**된 상태에서 같은 이름의 파일을 업로드하면 기존 파일은 사라지고 새 파일로 덮어씌워집니다.
* 버저닝이 **활성화**된 상태에서 같은 이름의 파일을 업로드하면, 기존 파일은 지워지지 않고 **과거 버전(Noncurrent Version)**으로 남게 되며, 새로 업로드된 파일이 고유 Version ID와 함께 **최신 버전(Current / Latest Version)**이 됩니다.

### 2.2 파일 삭제와 삭제 마커 (Delete Marker)
* 버저닝 활성화 상태에서 일반적인 삭제 요청(`mc rm` 또는 S3 DELETE)을 보내면, 실제 데이터가 삭제되지 않고 **삭제 마커(Delete Marker)**라는 특별한 0바이트 객체가 최신 버전으로 추가됩니다.
* 사용자가 해당 객체를 조회(GET)하면 삭제 마커를 만나 `404 Not Found`가 반환되어 삭제된 것처럼 보입니다.
* 영구 삭제를 원할 경우, 삭제 요청 시 대상 객체의 **특정 Version ID**를 명시해야 합니다.

---

## 3. MinIO Client (`mc`)를 이용한 버저닝 관리

```bash
# 1. 버킷 버저닝 상태 확인
mc version info myminio/mybucket

# 2. 버킷 버저닝 활성화
mc version enable myminio/mybucket

# 3. 버킷 버저닝 일시 정지
mc version suspend myminio/mybucket

# 4. 특정 객체의 모든 버전 목록 조회
mc ls --versions myminio/mybucket/

# 5. 특정 버전의 객체 영구 삭제 (Version ID 명시)
mc rm --version-id "<VERSION_ID>" myminio/mybucket/file.txt
```

---

## 4. 수명 주기 관리(Lifecycle)와의 연계

버저닝이 켜진 버킷은 객체가 수정되거나 삭제될 때마다 버전이 계속 쌓여 **스토리지 사용량이 지속적으로 증가**합니다.

이를 해결하기 위해 반드시 [수명 주기 관리 (Lifecycle)](Lifecycle.md) 정책을 함께 설정해야 합니다:
- **`--noncurrent-version-expiration-days`**: 과거 버전이 된 지 N일이 지난 객체를 영구 삭제
- **`--expire-delete-marker`**: 연결된 원본 데이터가 없는 고아 삭제 마커 자동 정리
