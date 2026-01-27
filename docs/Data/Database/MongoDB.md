# MongoDB

**MongoDB**는 가장 널리 사용되는 오픈 소스 **문서 지향(Document-oriented) NoSQL 데이터베이스**입니다. RDBMS의 표(Table) 방식 대신 JSON과 유사한 형태의 동적 스키마형 문서(BSON)를 사용합니다.

## 1. 핵심 특징

*   **Schema-less:** 고정된 스키마가 없어 데이터 구조가 자유롭습니다. 한 컬렉션 내에서도 문서마다 다른 필드를 가질 수 있습니다.
*   **BSON (Binary JSON):** 데이터를 이진 형태의 JSON인 BSON 포맷으로 저장하여 효율적인 공간 사용과 빠른 속도를 제공합니다.
*   **Scalability:** 샤딩(Sharding)을 통해 여러 서버로 데이터를 분산하여 수평적 확장이 쉽습니다.
*   **High Availability:** 복제셋(Replica Set) 기능을 통해 노드 장애 시 자동으로 복구(Failover)되어 높은 가용성을 보장합니다.

## 2. 기본 용어 비교

| RDBMS | MongoDB | 설명 |
| :--- | :--- | :--- |
| Database | Database | 데이터베이스 |
| Table | **Collection** | 문서들의 집합 |
| Row | **Document** | 하나의 데이터 레코드 (BSON) |
| Column | **Field** | 데이터 항목 (Key-Value) |
| Join | **Embedding / Reference** | 데이터 간의 관계 설정 |

## 3. 설치 및 실행 (Mac 예시)

### 설치 (Homebrew 권장)
```bash
brew tap mongodb/brew
brew install mongodb-community
```

### 서버 실행
```bash
# 특정 데이터 디렉토리 지정하여 실행
mongod --dbpath ./data/db
```

### 클라이언트 접속
```bash
# 최신 버전은 mongosh 사용
mongosh
```