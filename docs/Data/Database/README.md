# Database (데이터베이스)

데이터를 효율적으로 저장하고 관리하기 위한 데이터베이스 시스템, 최적화 및 동시성 제어 전략을 정리합니다.

## 목차

1. **[SQL Naming Convention](SQL_Naming_Convention.md)**: SQL 설계 시 권장되는 명명 규칙
2. **[Locking Strategy](Locking_Strategy.md)**: 동시성 제어를 위한 비관적/낙관적 락 전략 (원리, JPA/SQL 예시, 분산 락 고려)
3. **[JDBI FetchSize & Virtual Threads](JDBI_FetchSize_and_VirtualThreads.md)**: 대용량 데이터 스트리밍 조회 시 메모리 및 가상 스레드 최적화
4. **[Oracle LOB Segment](Oracle_LOB_Segment.md)**: Oracle 대용량 데이터(LOB) 세그먼트 관리 및 튜닝
5. **[Redis](Redis.md)**: 고성능 인메모리 Key-Value 저장소
6. **[MongoDB](MongoDB.md)**: 문서 지향 NoSQL 데이터베이스
7. **[Fluentd](fluentd.md)**: 통합 데이터 수집기 (Log Collector)
8. **[Image Storage Management](Image_Storage_Management.md)**: 효율적인 이미지 저장 및 관리 전략
