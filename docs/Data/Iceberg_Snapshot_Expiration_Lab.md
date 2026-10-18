# Iceberg snapshot 만료와 공유 data 파일 보존을 따로 검증하기

스냅샷 하나를 만료한다고 그 스냅샷에서 보이던 파일을 모두 지울 수는 없다. 남겨 둔 다른 스냅샷이 같은 파일을 참조할 수 있기 때문이다. 개인 Platform Lab에서는 만료할 스냅샷과 삭제되어야 할 파일을 먼저 구분한 뒤, 남은 데이터의 조회와 객체 저장소의 응답을 각각 대조했다.

[만료 전후 화면 보기](https://devdooly.github.io/devdooly-platform-lab/#snapshot-expiration) · [실행 근거와 원본 요약](https://github.com/DevDooly/devdooly-platform-lab/blob/main/docs/evidence/cloud-iceberg-expiration/README.md) · [고정 실행 소스](https://github.com/DevDooly/devdooly-platform-lab/tree/482d3ca4b564282feceb31f392c6a981302a7c2d/infra/cloud-lakehouse-expiration)

GitHub hosted runner에서 새 합성 warehouse만 사용한 실험이다. Spark 4.1.1·Iceberg 1.11.0·Trino 483·Garage 2.4.1과 PostgreSQL JDBC catalog를 사용했다. 회사 자료나 기존 운영 warehouse, 미니 PC에는 접속하지 않았다. 아래 S1–S4와 a1·a2·b1·a3는 관계를 설명하는 별칭이며 실제 snapshot ID나 객체 key가 아니다.

## 만료할 snapshot과 지울 파일의 범위가 달랐다

Iceberg의 `expire_snapshots`는 오래된 스냅샷과 그 스냅샷만 필요로 하는 파일을 정리한다. 만료하지 않은 스냅샷에 여전히 필요한 파일은 남긴다. `retain_last`는 최근 조상 스냅샷을 보존하는 조건이며, tag나 branch가 참조하는 스냅샷도 보호한다. [Iceberg 1.11.0 procedure 설명](https://iceberg.apache.org/docs/1.11.0/spark-procedures/#expire_snapshots)

공유가 실제로 생기는 작은 입력을 만들었다. 먼저 6행을 append하고 6행을 더 넣어 12행으로 만든 뒤 compaction을 수행했다. 그다음 첫 스냅샷 S1에 tag를 붙이고 새 6행을 append해 현재 상태를 18행으로 만들었다.

| 스냅샷 | 생성 작업 | 현재 참조하는 data 파일 | 만료 후 기대 |
| --- | --- | --- | --- |
| S1 | 첫 append, 6행 | a1 | tag로 보존 |
| S2 | 두 번째 append, 12행 | a1·a2 | 이 스냅샷만 만료 |
| S3 | compaction, 12행 | b1 | 최근 두 스냅샷 중 하나로 보존 |
| S4 | 세 번째 append, 18행 | b1·a3 | current로 보존 |

S2가 없어져도 a1은 S1에 필요하다. b1은 S3와 S4가 공유하며 a3는 current인 S4에 필요하다. 이 구성에서 다른 보존 스냅샷이 필요로 하지 않는 data 파일은 a2 하나다. compaction이 이전 파일의 즉시 삭제를 뜻하지 않는다는 점도 이 참조 관계에서 드러난다.

## 삭제 호출 전에 기대값을 고정했다

기존 source를 바꾸지 않은 append·compaction 흐름에 tag와 마지막 append를 덧붙였다. 만료 직전에는 snapshot 4개, tag와 current, 파일 참조, 객체 집합과 bytes를 수집했다. 새 테이블의 writer는 이 Spark 실행 하나였고 Trino와 사후 reader는 아직 시작하지 않은 상태였다.

사전 검사는 스냅샷이 예상한 네 단계로 이어지는지, S1 tag가 유지되는지, a2만 보존 참조에서 벗어나는지 확인했다. 이 조건이 맞은 뒤 S3의 실제 commit 시각을 `older_than`에 넣고 `retain_last=2`로 `expire_snapshots`를 한 번 호출했다. 시각 기준만 적용하는 대신 tag와 최근 두 스냅샷을 함께 보호해 S2 하나만 만료하도록 구성했다.

호출 반환만으로 완료 처리하지 않았다. 이후 snapshot·참조·파일 집합과 행을 다시 검사했다. 호출 결과가 불명확하면 자동으로 만료를 반복하지 않는 실행기이며, 이번 정상 결과가 metadata commit과 객체 삭제의 원자성을 증명하는 것은 아니다. [실제 호출과 후검사 소스](https://github.com/DevDooly/devdooly-platform-lab/blob/482d3ca4b564282feceb31f392c6a981302a7c2d/infra/cloud-lakehouse-expiration/bootstrap_expiration.py)

## 객체 25개에서 23개로 줄었다는 말의 내부를 확인했다

[실행 39140688897](https://github.com/DevDooly/devdooly-platform-lab/actions/runs/39140688897)은 `COMPLETE / PASSED / VERIFIED`로 끝났다. 2026-10-18 15:31:51 UTC의 공개 요약에는 만료한 snapshot 1개와 보존한 snapshot 3개가 기록됐다. 한국 시각으로는 10월 19일의 실행이다.

| 비교 항목 | 실제 결과 |
| --- | --- |
| Snapshot | 4개 → 3개, S2만 만료 |
| 삭제된 객체 | data 1개·manifest 1개·manifest list 1개 |
| 기존 객체 보존 | 22개, 전체 bytes 대조 |
| 새 객체 | metadata JSON 1개 |
| 사후 전체 객체 | 23개 |

객체 수는 `25 − 3 + 1 = 23`이다. 두 개 줄었다고 data 파일 두 개가 삭제된 것은 아니다. 공개 요약의 `protectedObjectCount=22`와 `oldSurvivorObjectCount=22`는 보호 대상과 실제 생존 대조를 각각 표현하는 값이므로 두 수를 더하지 않는다. manifest·manifest list를 data 파일이나 물리 블록과 같은 단위로 세지도 않는다. [같은 실행의 원본 summary](https://github.com/DevDooly/devdooly-platform-lab/blob/main/docs/evidence/cloud-iceberg-expiration/summary.json)

a2는 만료 전에 GET으로 읽은 같은 key를 만료 뒤 다시 조회해 `NoSuchKey`와 HTTP 404를 확인했다. procedure의 삭제 counter와 사후 전체 객체 대조도 함께 통과했다. LIST에 이름이 안 보이는 것, 권한 오류 403, timeout을 삭제 성공으로 해석하지 않았다. 남아야 할 a1·b1·a3와 Silver 객체는 생존 객체의 전체 bytes 대조에 포함됐다.

## Spark와 Trino가 확인한 내용도 구분했다

파일이 남아 있다는 사실과 테이블을 올바르게 읽을 수 있다는 사실은 각각 확인해야 했다. Spark에서는 tag가 가리키는 S1과 보존한 이전 스냅샷 S3, current S4를 실제 snapshot ID로 읽어 고정 입력의 전체 값·순서와 비교했다.

| Spark의 행 대조 | 결과 |
| --- | --- |
| tag가 가리키는 S1 | 6행 |
| 보존한 이전 스냅샷 S3 | 12행 |
| current S4 | 18행 |
| 기존 Silver 결과 | 12행, 내용 유지 |

이후 Trino에서 실행한 SELECT는 네 개다. version, current Bronze 18행, `sensor_value`의 DOUBLE schema, Silver 12행을 조회했다. **Trino가 tag나 과거 스냅샷을 조회한 시험은 아니다.** 사후 reader에서는 JDBC metadata pointer와 warehouse 전체 객체 bytes가 후속 조회 전후에도 같은지 대조하고 a2의 `NoSuchKey`도 다시 확인했다. [조회·보존·종료를 연결한 실행기](https://github.com/DevDooly/devdooly-platform-lab/blob/482d3ca4b564282feceb31f392c6a981302a7c2d/infra/cloud-lakehouse-expiration/run_expiration.py)

과거 metadata JSON을 보존했다고 S2를 복원할 수 있는 것은 아니다. S2가 필요로 했던 a2는 삭제됐다. 만료된 스냅샷은 time travel 대상에서 빠지며, 남아 있는 metadata 파일만으로 삭제한 data를 되살릴 수 없다. [Iceberg 1.11.0 maintenance](https://iceberg.apache.org/docs/1.11.0/maintenance/#expire-snapshots)

## 종료 확인과 공간 회수는 다른 결과였다

Spark·Trino·Python reader의 정상 종료와 initializer·소유한 bound 컨테이너의 stop을 확인했다. 이 실행의 정리는 소유 컨테이너 종료까지이며 volume은 삭제하지 않았다. 공개 요약의 `volumesDeleted`와 `physicalStorageGcVerified`는 false다.

따라서 이번 결과는 새 warehouse의 snapshot 만료·선택 객체 삭제·공유 데이터와 조회 결과 보존에 대한 증거다. Garage 물리 블록 GC나 실제 디스크 공간 회수량은 측정하지 않았고, 운영 보존 계획기의 KEEP·`applyEnabled:false`도 그대로 유지했다. metadata commit 직후 장애·부분 삭제 복구, 운영 warehouse 적용, 장기간 가용성이나 성능 SLA는 별도의 검증이 필요하다.

공개 화면의 전후 값도 이 저장된 실행 기록이다. 토글을 눌러도 만료를 다시 수행하지 않는다. snapshot 수, 객체 집합, 객체 GET, 행 조회, 프로세스 종료를 다른 검사로 연결했기 때문에 “만료가 성공했다”는 한 문장보다 무엇을 지우고 무엇을 지켰는지 구체적으로 설명할 수 있었다.
