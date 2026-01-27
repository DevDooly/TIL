# 이미지 저장 및 관리 전략

웹 애플리케이션에서 대량의 이미지를 저장하고 효율적으로 관리하는 것은 시스템 성능과 비용에 큰 영향을 미칩니다.

## 1. 이미지를 DB에 직접 저장하지 않는 이유

많은 관계형 데이터베이스(RDBMS)가 BLOB 타입을 통해 이미지 바이너리를 저장할 수 있지만, 일반적으로 권장되지 않습니다.

*   **성능 저하:** DB는 인덱싱과 트랜잭션 처리에 최적화되어 있지, 큰 바이너리 덩어리(Blob)를 스트리밍하는 데는 비효율적입니다.
*   **백업 및 복구 부담:** 데이터베이스 파일 크기가 기하급수적으로 커져 백업 시간이 오래 걸리고 관리가 어려워집니다.
*   **캐싱의 어려움:** 파일 시스템이나 Object Storage에 저장하면 CDN(Content Delivery Network)을 통한 캐싱이 매우 쉽지만, DB는 그렇지 않습니다.

## 2. 권장되는 저장 전략

### 2.1 파일 경로 저장 방식
이미지 파일 자체는 서버의 **파일 시스템**이나 **오브젝트 스토리지(S3 등)**에 저장하고, 데이터베이스에는 해당 파일의 **URL 또는 경로(Path)**만 저장합니다.

### 2.2 디렉토리 계층화
하나의 디렉토리에 수만 개의 파일을 몰아넣으면 OS 수준에서 성능 저하가 발생합니다. 파일명의 해시값을 따서 디렉토리를 분산하는 것이 좋습니다.
*   예: `abcde123.jpg` -> `/a/b/abcde123.jpg`

## 3. 다양한 저장소 비교

| 방식 | 설명 |
| :--- | :--- |
| **File System** | 서버 로컬 디스크에 저장. 구현이 쉽지만 서버 확장(Scale-out) 시 동기화 문제 발생. |
| **Object Storage (S3)** | 현대적 표준. 고가용성, 무한 확장성, CDN 연동이 쉬움. |
| **LMDB / HDF5** | AI/데이터 분석용. 수백만 개의 작은 이미지나 대규모 데이터셋을 빠르게 읽어야 할 때 사용. |

## 참고
*   [The best database for storing images might not be a database at all](https://blog.couchbase.com/the-best-database-for-storing-images-might-not-be-a-database-at-all/)
*   [Three Ways of Storing and Accessing Lots of Images in Python](https://realpython.com/storing-images-in-python/)