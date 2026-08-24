---
title: Engineering Troubleshooting Archive
---

# 🛠️ 실전 엔지니어링 트러블슈팅 아카이브

실무 및 대규모 시스템 운영 환경에서 발생한 **기술적 장애, 병목, 예기치 않은 동작에 대한 원인 분석과 해결 과정(Root Cause Analysis & Resolution)**을 기록한 공간입니다.

문제를 단순히 임기응변으로 때우는 것이 아니라, **내부 소스코드 분석, JVM/커널 레벨 동작 원리, 패킷/메모리 프로파일링**을 통해 근본 원인을 규명하고 최적화한 사례들입니다.

---

## ☕ 1. Java, JVM & Spring Ecosystem

| Problem & Symptom | Root Cause | Solution & Impact | Deep-Dive Article |
| :--- | :--- | :--- | :--- |
| **FTP/SFTP 가상 스레드 Pinning** | Commons-Net 내부 `synchronized` 블록으로 인한 OS 캐리어 스레드 고갈 | `ReentrantLock` 교체 및 전용 I/O 스레드 풀 분리 | [**분석 문서 보기**](../Language/Java/Virtual_Threads_FTP_Pinning.md) |
| **K8s 환경 Virtual Thread CPU 스로틀링** | K8s CPU CFS Quota와 대량 가상 스레드 생성 시 스케줄링 지연 충돌 | K8s 리소스 Limit 최적화 및 ForkJoinPool 병렬성 튜닝 | [**분석 문서 보기**](../Language/Java/Virtual_Threads_in_K8s.md) |
| **Kafka Consumer Pinning 이슈** | `KafkaConsumer`의 폴링 루프 내 동기화 락 경합 | 컨슈머 전용 단일 플랫폼 스레드 + 가상 스레드 핸들러 구조화 | [**분석 문서 보기**](../Language/Java/SpringBoot/Virtual_Thread_Pinning_Kafka.md) |
| **JDBI DB Blocking I/O Pinning** | DB 커넥션 풀 및 드라이버 소켓 동기화 락 | 하이브리드 스레드 풀 및 FetchSize 스트리밍 최적화 | [**분석 문서 보기**](../Language/Java/SpringBoot/JDBI_VT_Pinning_Solution.md) |
| **K8s Spring 프로파일 우선순위 이슈** | 환경 변수와 CLI 인자 간의 프로파일 덮어쓰기 순서 불일치 | `BeanPostProcessor` 및 설정 주입 우선순위 표준화 | [**분석 문서 보기**](../Language/Java/SpringBoot/Spring_Profile_Priority_in_K8s.md) |
| **로깅 설정 YAML to XML 전환 충돌** | 외부 SDK 내부 `logback.xml`과 Spring YAML 설정 충돌 | Logback XML 전환 및 JoranConfigurator 로딩 순서 제어 | [**분석 문서 보기**](../Language/Java/SpringBoot/Logging_Config_Migration_YAML_to_XML.md) |
| **SLF4J addKeyValue ECS 누락** | ECS JSON Encoder의 커스텀 MDC/KeyValue 직렬화 누락 | Composite Json Encoder 및 커스텀 프로바이더 구축 | [**분석 문서 보기**](../Language/Java/SpringBoot/Logging_ECS_KeyValue_Support.md) |

---

## 🎡 2. Distributed Messaging & Infrastructure

| Problem & Symptom | Root Cause | Solution & Impact | Deep-Dive Article |
| :--- | :--- | :--- | :--- |
| **Kafka RoundRobinPartitioner 불균형** | KAFKA-9965 버그로 인해 특정 파티션에만 레코드 집중 | Partitioner 업그레이드 및 파티션 키 할당 전략 수정 | [**분석 문서 보기**](../Infrastructure/MessageBroker/Kafka/Producer_Partitioner_Issue.md) |
| **Sticky Partitioner 배치 쏠림** | Sticky Partitioner와 `linger.ms` 지연 간의 불일치 | 배치 크기 및 링거 타임 최적화를 통한 고른 부하 분산 | [**분석 문서 보기**](../Infrastructure/MessageBroker/Kafka/Partitioner_Evolution_and_Imbalance.md) |
| **커스텀 파티셔너 abortOnNewBatch 이슈** | 새 배치가 생성될 때 파티션 순환이 중단되는 현상 | 파티셔너 내부 상태 추적 로직 및 락 메커니즘 수정 | [**분석 문서 보기**](../Infrastructure/MessageBroker/Kafka/AbortOnNewBatch_Issue.md) |
| **Consumer 종료 시 IllegalStateException** | 멀티스레드 환경에서 `wakeup()`과 `close()`의 호출 순서 꼬임 | 안전한 컨슈머 셧다운 훅(Graceful Shutdown) 구현 | [**분석 문서 보기**](../Infrastructure/MessageBroker/Kafka/Consumer_Safe_Shutdown.md) |
| **Hadoop/Tez 분산 작업 급격한 지연** | 특정 워커 노드의 네트워크 NIC 패킷 RX 드롭 에러 | 하드웨어 결함 노드 격리 및 네트워크 버퍼 튜닝 | [**분석 문서 보기**](../Infrastructure/Hadoop/Tez_Job_Slowness_Network_RX.md) |
| **대용량 파일 전송 후 용량 불일치** | Sparse File(희소 파일) 및 블록 크기 차이에 따른 rsync 계산 착오 | `--sparse` 옵션 적용 및 파일 체크섬 검증 자동화 | [**분석 문서 보기**](../Infrastructure/Linux/Large_File_Transfer.md) |
| **MinIO 버저닝 삭제 지연 & 스토리지 누수** | Delete Marker 생성 후 실제 이전 버전 데이터 미삭제 | VersionId 명시 삭제 및 Expiration Lifecycle Rule 정립 | [**분석 문서 보기**](MinIO_Versioning_Deletion_Issue.md) |

---

## 🗄️ 3. Database, Serialization & Data Processing

| Problem & Symptom | Root Cause | Solution & Impact | Deep-Dive Article |
| :--- | :--- | :--- | :--- |
| **Oracle LOB Segment 공간 부족 (ORA-01692)** | 대용량 LOB 컬럼 저장 시 테이블스페이스 자동 확장 한계 도달 | LOB 전용 테이블스페이스 분리 및 Chunk/Retention 최적화 | [**분석 문서 보기**](../Data/Database/Oracle_LOB_Segment.md) |
| **Avro 'result' 필드명 컴파일 에러** | 생성된 `hashCode()` 메서드의 내부 변수명과 필드명 충돌 | 스키마 명명 규칙 개정 및 커스텀 템플릿 컴파일러 패치 | [**분석 문서 보기**](Avro_HashCode_Field_Naming_Conflict.md) |

---

> [!TIP]
> 새로운 트러블슈팅 사례가 해결될 때마다 문제 원인과 함께 이 아카이브에 지속적으로 업데이트됩니다.
