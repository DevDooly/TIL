# 🛠️ 트러블슈팅 (Troubleshooting)

실무에서 발생한 기술적인 문제들과 그에 대한 원인 분석, 해결 과정을 정리한 공간입니다. 각 이슈의 상세 내용은 해당 기술 카테고리의 원본 문서를 연결합니다.

---

## ☕ Java & Spring

*   **[Virtual Thread Pinning 이슈 (FTP/SFTP)](../Language/Java/Virtual_Threads_FTP_Pinning.md)**: 레거시 라이브러리의 `synchronized` 블록으로 인한 OS 스레드 고갈 문제.
*   **[K8s 환경의 Virtual Thread 주의사항](../Language/Java/Virtual_Threads_in_K8s.md)**: CPU Throttling 및 메모리 팽창 이슈 분석.
*   **[K8s Spring 프로파일 우선순위 이슈](../Language/Java/SpringBoot/Spring_Profile_Priority_in_K8s.md)**: 환경 변수와 실행 인자 간의 설정 덮어쓰기 문제 해결.

## 🎡 Infrastructure & Kafka

*   **[Kafka RoundRobinPartitioner 불균형 (KAFKA-9965)](../Infrastructure/MessageBroker/Kafka/Producer_Partitioner_Issue.md)**: 특정 파티션으로 메시지가 쏠리는 버그 분석.
*   **[Kafka 최신 버전 Offset 불균형 문제](../Infrastructure/MessageBroker/Kafka/Partitioner_Evolution_and_Imbalance.md)**: Sticky 전략과 배치 메커니즘 충돌 해결 방안.
*   **[대량 파일 전송 용량 불일치 이슈](../Infrastructure/Linux/Large_File_Transfer.md#8-용량-불일치-트러블슈팅)**: rsync 복사 후 원본과 대상의 용량이 차이 나는 원인 분석.

## 🗄️ Database

*   **[Oracle LOB Segment 공간 부족 (ORA-01692)](../Data/Database/Oracle_LOB_Segment.md)**: 대용량 데이터 저장 시 발생하는 LOB 세그먼트 오류 조치.

---
*💡 새로운 이슈가 해결될 때마다 이 목차에 추가하여 지식을 공유합니다.*
