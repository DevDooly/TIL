---
title: Engineering Troubleshooting Archive
---

# 트러블슈팅과 기술 검증 기록

실무에서 접한 문제, 공개 이슈 분석, 재현·운영 가이드를 함께 모은다. 문서의 예제나 공식 버그 설명을 곧바로 개인의 운영 성과로 해석하지 않는다. 개별 사례는 적용 버전·재현 조건·검증 결과를 함께 기록한다.

## Java · JVM · Spring

| 문서 | 확인할 내용 |
| :--- | :--- |
| [FTP 처리와 Virtual Thread](../Language/Java/Virtual_Threads_FTP_Pinning.md) | JDK별 pinning 진단과 FTP 오류 처리 |
| [Kubernetes의 Virtual Thread](../Language/Java/Virtual_Threads_in_K8s.md) | CPU quota, heap/native 메모리, downstream 제한 |
| [Kafka Consumer pinning](../Language/Java/SpringBoot/Virtual_Thread_Pinning_Kafka.md) | 실제 stack과 consumer 소유권 |
| [JDBI 실행기 격리](../Language/Java/SpringBoot/JDBI_VT_Pinning_Solution.md) | bounded queue, 거절과 transaction 경계 |
| [JDBI FetchSize](../Data/Database/JDBI_FetchSize_and_VirtualThreads.md) | driver 힌트와 결과 보관량의 차이 |
| [연결된 GZIP 해제](../Language/Java/Concatenated_Gzip_Decompression.md) | 멤버 처리, 크기 제한과 손상 입력 |
| [K8s Spring 프로파일](../Language/Java/SpringBoot/Spring_Profile_Priority_in_K8s.md) | 설정 우선순위 분석 |
| [로깅 YAML/XML 전환](../Language/Java/SpringBoot/Logging_Config_Migration_YAML_to_XML.md) | 설정 파일과 로딩 경로 |
| [SLF4J key-value와 ECS](../Language/Java/SpringBoot/Logging_ECS_KeyValue_Support.md) | 구조화 로그 필드 확인 |

## Kafka · 인프라

| 문서 | 확인할 내용 |
| :--- | :--- |
| [RoundRobin 불균형](../Infrastructure/MessageBroker/Kafka/Producer_Partitioner_Issue.md) | client 이중 호출 버그와 패치 버전 |
| [파티셔너 변화](../Infrastructure/MessageBroker/Kafka/Partitioner_Evolution_and_Imbalance.md) | 건수·bytes·lag 분포를 구분한 측정 |
| [abortOnNewBatch](../Infrastructure/MessageBroker/Kafka/AbortOnNewBatch_Issue.md) | 패치 전 내부 호출 흐름 |
| [Consumer 종료](../Infrastructure/MessageBroker/Kafka/Consumer_Safe_Shutdown.md) | wakeup, close, 완료 offset |
| [메시지 크기 설정](../Infrastructure/MessageBroker/Kafka/Kafka_Message_Size_Configuration.md) | producer/topic/consumer 설정과 fetch 예외 |
| [Hadoop/Tez RX 오류](../Infrastructure/Hadoop/Tez_Job_Slowness_Network_RX.md) | 네트워크 지표와 작업 지연 분석 |
| [대용량 파일 전송](../Infrastructure/Linux/Large_File_Transfer.md) | 파일 크기와 디스크 사용량 비교 |
| [MinIO 버전별 삭제](MinIO_Versioning_Deletion_Issue.md) | delete marker와 보존된 객체 버전 |
| [etcd 백업과 복원](../Infrastructure/Kubernetes/CKA/ETCD_Backup_Restore.md) | etcdctl/etcdutl과 복원 검증 |

## 데이터 · 개발 과정

| 문서 | 확인할 내용 |
| :--- | :--- |
| [Oracle LOB 공간](../Data/Database/Oracle_LOB_Segment.md) | LOB segment와 tablespace 확인 |
| [Avro result 충돌](Avro_HashCode_Field_Naming_Conflict.md) | 생성기 버전과 필드/지역 변수 참조 |
| [LLM을 활용한 레거시 개선](../LLM_Development/Legacy_Code_Improvement.md) | 알고리즘·시간 로직·스타일 변경의 검증 기록 |
