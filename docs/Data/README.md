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
