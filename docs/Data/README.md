---
title: Data Engineering & Storage Systems
---

# 💾 Data Systems & Storage Architecture

대용량 데이터의 안정적인 저장, 트랜잭션 무결성, 고속 캐싱 및 실시간 로그 파이프라인 구축을 위한 **데이터베이스, 분산 캐시, 락킹 전략 및 로그 수집 아키텍처**를 다룹니다.

---

## 📚 주요 기술 문서 목차

### 1. Database Architecture & Optimization

* **[Database 종합 가이드](Database/README.md)**: RDBMS 및 NoSQL 데이터 저장소 아키텍처
* **[Redis 캐싱 & 데이터 구조](Database/Redis.md)**: 인메모리 데이터 구조, 캐싱 패턴(Cache-Aside) 및 분산 락
* **[Locking Strategy (동시성 제어)](Database/Locking_Strategy.md)**: 낙관적 락(Optimistic Lock) vs 비관적 락(Pessimistic Lock) 트레이드오프
* **[Oracle LOB Segment 관리 및 트러블슈팅](Database/Oracle_LOB_Segment.md)**: 대용량 바이너리 저장 시 ORA-01692 공간 부족 해결
* **[JDBI FetchSize & Virtual Threads](Database/JDBI_FetchSize_and_VirtualThreads.md)**: 대량 조회 시 메모리 OutOfMemory 방지 스트리밍
* **[MongoDB](Database/MongoDB.md)**: 도큐먼트 지향 NoSQL 및 인덱싱 전략
* **[SQL Naming Convention](Database/SQL_Naming_Convention.md)**: 테이블 및 컬럼 표준 명명 규칙

### 2. Logging, Metrics & Telemetry

* **[ELK Stack (Elasticsearch, Logstash, Kibana)](ELK.md)**: 분산 로그 수집 및 대시보드 시각화
* **[Log Collectors Comparison](Log_Collectors_Comparison.md)**: Fluentd, Logstash, Vector, Fluent Bit 성능 및 리소스 비교 분석
* **[Fluentd](Database/fluentd.md)**: 플러그인 기반 로그 포워딩 파이프라인

### 3. Data Serialization

* **[Avro result 필드와 hashCode 지역 변수 충돌](Avro_HashCode_Field_Naming_Conflict.md)**: Java 코드 생성기의 필드 참조 문제와 검증 방법

### 4. Lakehouse 실측 사례 및 파이프라인 설계

* **[Java Avro 저장부터 Spark Iceberg(Parquet) 변환·Trino 조회까지의 파이프라인 설계 및 챕터별 진행 계획](Avro_Spark_Iceberg_Trino_Pipeline_Plan.md)**: Avro 수집 파일에서 Iceberg(Parquet) 테이블 적재 및 Trino 조회까지 5개 챕터로 나누어 구현·검증하는 실행 로드맵과 예제 코드
* **[[Chapter 1] Avro 스키마 설계 및 Spark·Trino 로컬 레이크하우스 공통 인프라 구성](Avro_Iceberg_Trino_Ch1_Schema_and_Infra.md)**: Java·Spark·Iceberg·Trino 간 데이터 타입 매핑, `order_event.avsc` 설계 원칙, Docker Compose(PostgreSQL JDBC 카탈로그 + 공유 볼륨) 구성 및 연동 검증
* **[[Chapter 2] Java에서 Apache Avro로 `.avro` 컨테이너 파일 생성 및 검증](Avro_Iceberg_Trino_Ch2_Java_Avro_Writer.md)**: `.avro` Object Container File 바이너리 구조, `GenericRecord` vs `SpecificRecord` 비교, `DataFileWriter`(Snappy 압축·`appendTo`) 및 `DataFileReader` 검증 예제
* **[[Chapter 3] Apache Spark로 Avro 파일을 읽어 Iceberg(Parquet) 테이블로 변환·적재](Avro_Iceberg_Trino_Ch3_Spark_Avro_to_Iceberg.md)**: `spark-avro` + `iceberg-spark-runtime` 변환 흐름, 히든 파티셔닝(`days(event_time)`) DDL, `append()` 및 `MERGE INTO` 멱등 적재, 물리 Parquet·매니페스트 파일 구조 검증
* **[[Chapter 4] Trino에서 Iceberg 카탈로그 연결 및 Parquet 데이터·메타데이터 교차 검증](Avro_Iceberg_Trino_Ch4_Trino_Query_and_Metadata.md)**: 무중단 스냅샷 조회 원리, 히든 파티션 프루닝 확인, `$files`·`$partitions`·`$snapshots` 메타데이터 테이블 교차 검증 및 연동 트러블슈팅
* **[[Chapter 5] 운영 고도화 — 스키마 진화(Schema Evolution), 소파일 Compaction, 스냅샷 만료](Avro_Iceberg_Trino_Ch5_Schema_Evolution_and_Maintenance.md)**: 기존 Parquet 파일 재작성 없는 신규 컬럼(`payment_method`) 전파, `rewrite_data_files`(`binpack`/`sort`) Compaction, `expire_snapshots`·`remove_orphan_files` 운영 절차
* **[Iceberg snapshot 만료와 공유 파일 보존](Iceberg_Snapshot_Expiration_Lab.md)**: 새 합성 warehouse에서 만료 대상·공유 파일·객체 GET·Spark/Trino 조회 범위를 분리해 확인한 개인 Lab 사례
