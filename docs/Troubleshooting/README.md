# 🛠️ 트러블슈팅 (Troubleshooting)

실무에서 발생한 기술적인 문제들과 그에 대한 원인 분석, 해결 과정을 정리한 공간입니다. 각 이슈의 상세 내용은 해당 기술 카테고리의 원본 문서를 연결합니다.

---

## ☕ Java & Spring

* **[Virtual Thread Pinning 이슈 (FTP/SFTP)](../Language/Java/Virtual_Threads_FTP_Pinning.md)**: 레거시 라이브러리의 `synchronized` 블록으로 인한 OS 스레드 고갈 문제.
* **[K8s 환경의 Virtual Thread 주의사항](../Language/Java/Virtual_Threads_in_K8s.md)**: CPU Throttling 및 메모리 팽창 이슈 분석.
* **[Kafka Consumer 가상 스레드 Pinning 이슈](../Language/Java/SpringBoot/Virtual_Thread_Pinning_Kafka.md)**: KafkaClient 내부 `synchronized` 블록으로 인한 캐리어 스레드 고갈 문제.
* **[JDBI 가상 스레드 Pinning 해결 패턴](../Language/Java/SpringBoot/JDBI_VT_Pinning_Solution.md)**: 하이브리드 스레드 모델을 이용한 DB Blocking I/O 최적화.
* **[K8s Spring 프로파일 우선순위 이슈](../Language/Java/SpringBoot/Spring_Profile_Priority_in_K8s.md)**: 환경 변수와 실행 인자 간의 설정 덮어쓰기 문제 및 `BeanPostProcessor`를 이용한 프로그래밍 방식의 해결책.


* **[로깅 설정 YAML to XML 전환 이슈](../Language/Java/SpringBoot/Logging_Config_Migration_YAML_to_XML.md)**: 외부 SDK의 `logback.xml`과 `application.yml` 설정 충돌 해결 사례.


* **[SLF4J addKeyValue를 ECS 로그에 포함하기](../Language/Java/SpringBoot/Logging_ECS_KeyValue_Support.md)**: 커스텀 키가 ECS JSON 로그에 나타나지 않는 문제 해결 및 대안 제시.










## 🎡 Infrastructure & Kafka

* **[Kafka RoundRobinPartitioner 불균형 (KAFKA-9965)](../Infrastructure/MessageBroker/Kafka/Producer_Partitioner_Issue.md)**: 특정 파티션으로 메시지가 쏠리는 버그 분석.

* **[Kafka 최신 버전 Offset 불균형 문제](../Infrastructure/MessageBroker/Kafka/Partitioner_Evolution_and_Imbalance.md)**: Sticky 전략과 배치 메커니즘 충돌 해결 방안.

* **[Hadoop/Tez 네트워크 RX 에러로 인한 작업 지연](../Infrastructure/Hadoop/Tez_Job_Slowness_Network_RX.md)**: 특정 노드의 하드웨어 결함으로 인한 전체 분산 처리 성능 저하.

* **[대량 파일 전송 용량 불일치 이슈](../Infrastructure/Linux/Large_File_Transfer.md#8-용량-불일치-트러블슈팅)**: rsync 복사 후 원본과 대상의 용량이 차이 나는 원인 분석.

* **[MinIO 버저닝 활성화 후 삭제 지연 이슈](../Troubleshooting/MinIO_Versioning_Deletion_Issue.md)**: 삭제 마커로 인해 파일이 영구 삭제되지 않는 문제 및 버전별 삭제 처리 방법.





## 🗄️ Database

* **[Oracle LOB Segment 공간 부족 (ORA-01692)](../Data/Database/Oracle_LOB_Segment.md)**: 대용량 데이터 저장 시 발생하는 LOB 세그먼트 오류 조치.
* **[Avro 필드명 'result' 사용 시 hashCode 충돌](../Troubleshooting/Avro_HashCode_Field_Naming_Conflict.md)**: Avro 자동 생성 코드의 지역 변수 이름 충돌 이슈 및 해결 방안.

---
*💡 새로운 이슈가 해결될 때마다 이 목차에 추가하여 지식을 공유합니다.*
