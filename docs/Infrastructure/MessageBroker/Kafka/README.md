# Apache Kafka

Kafka는 실시간 데이터 파이프라인 및 스트리밍 애플리케이션을 구축하기 위한 분산 이벤트 스트리밍 플랫폼입니다.

## 📌 학습 로드맵

1. **Kafka 개요 및 핵심 개념**: Topic, Partition, Offset의 이해
   - [파티션(Partition) 전략 및 개수 산정](Partition_Strategy.md)
2. **설치 및 환경 구성**: Docker를 이용한 Kafka 기동
3. **Kafka Producer (Java)**: 효율적인 메시지 발행 전략
   - [파티셔너(Partitioner) 정책 및 설정](Producer_Partitioner_Policy.md)
   - [RoundRobinPartitioner 이슈 (KAFKA-9965)](Producer_Partitioner_Issue.md)
   - [파티셔너의 진화와 불균형(Imbalance) 문제 해결](Partitioner_Evolution_and_Imbalance.md)
4. **Kafka Consumer (Java)**: [특정 Offset 재소비 및 제어](Consumer_Offset_Control.md)
5. **Spring Kafka**: 스프링 프레임워크와의 연동
   - [테스트 코드에서 단일 메시지 소비 예제](Spring_Kafka_Test.md)
6. **운영 및 트러블슈팅**: Lag 모니터링 및 성능 최적화
