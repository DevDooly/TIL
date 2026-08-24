---
title: Cloud, DevOps & Infrastructure Architecture
---

# 🏗️ Infrastructure & Cloud Native

대규모 서비스를 무중단으로 안정적으로 운영하기 위한 **컨테이너 오케스트레이션(Kubernetes), GitOps & CI/CD(ArgoCD, Jenkins), 분산 메시징(Kafka, NATS), 오브젝트 스토리지(MinIO) 및 Linux 커널 튜닝**을 다룹니다.

---

## 📚 주요 기술 분야 및 문서

### 1. Distributed Streaming & Messaging
* **[Apache Kafka 심층 아키텍처](MessageBroker/Kafka/README.md)**:
  * **[Partitioner Evolution & Imbalance](MessageBroker/Kafka/Partitioner_Evolution_and_Imbalance.md)**: 최신 Kafka Partitioner 동작 원리 및 파티션 불균형 해결
  * **[Producer Partitioner Policy & Issue](MessageBroker/Kafka/Producer_Partitioner_Issue.md)**: RoundRobinPartitioner 버그(KAFKA-9965) 분석
  * **[Consumer Safe Shutdown](MessageBroker/Kafka/Consumer_Safe_Shutdown.md)**: 컨슈머 Graceful Shutdown 및 `IllegalStateException` 방지
  * **[Consumer Offset Control](MessageBroker/Kafka/Consumer_Offset_Control.md)**: 수동 커밋 및 정확한 1회 처리(Exactly-Once) 전략
  * **[Kafka Message Size Configuration](MessageBroker/Kafka/Kafka_Message_Size_Configuration.md)**: 대용량 메시지 전송을 위한 브로커/프로듀서/컨슈머 설정
* **[NATS](MessageBroker/NATS.md)**: 초경량 고성능 클라우드 네이티브 메시징 시스템
* **[AMQP Protocol](MessageBroker/AMQP.md)**: Advanced Message Queuing Protocol 구조 및 RabbitMQ 아키텍처

### 2. Container & Kubernetes Orchestration
* **[Kubernetes 핵심 개념](Kubernetes/README.md)**:
  * **[CKA (Certified Kubernetes Administrator) 핵심 가이드](Kubernetes/CKA/README.md)**: 클러스터 아키텍처, RBAC 권한 관리, 네트워크 정책
  * **[Operator Pattern](Kubernetes/Operator_Pattern.md)**: CRD와 컨트롤러를 이용한 K8s 자동화 패턴
* **[Docker 컨테이너화 가이드](Docker/README.md)**:
  * **[Docker Image Versioning Strategy](Docker/docker_image_versioning_strategy.md)**: 멀티 환경 배포를 위한 태깅 및 불변성 전략
  * **[Dockerfile 작성 가이드](Docker/dockerfile.md)**: 멀티 스테이지 빌드 및 이미지 크기 최적화

### 3. Continuous Integration & GitOps (CI/CD)
* **[ArgoCD GitOps 배포 자동화](ArgoCD/README.md)**: 선언적 GitOps 배포 아키텍처, K8s 매니페스트 동기화 및 롤백
  * **[ArgoCD 실전 예제](ArgoCD/Examples.md)**: 멀티 클러스터 배포 및 헬스 체크
* **[Jenkins 파이프라인 가이드](Jenkins/README.md)**:
  * **[Kubernetes 기반 Jenkins 설치](Jenkins/Installation_K8s.md)**: Dynamic Pod Agent 기반의 탄력적 빌드 환경 구축
  * **[Jenkinsfile 파이프라인 실전 예제](Jenkins/Examples.md)**: 선언적 파이프라인 작성법

### 4. Storage & Distributed Computing
* **[MinIO (S3-Compatible Object Storage)](MinIO/README.md)**:
  * **[MinIO Lifecycle Management](MinIO/Lifecycle.md)**: 데이터 보존 정책 및 자동 삭제 룰
  * **[MinIO Client (`mc`) CLI 활용](MinIO/MinIO_Client_mc.md)**: 미러링, 백업 및 버킷 정책 관리
  * **[MinIO Java Client 연동](MinIO/Java_Client_Examples.md)**: 멀티파트 업로드 및 사전 서명 URL(Presigned URL)
* **[Hadoop Ecosystem](Hadoop/README.md)**:
  * **[NameNode High Availability (HA)](Hadoop/NameNode_HA.md)**: QJM(Quorum Journal Manager) 기반 이중화
  * **[Tez Job Slowness (Network RX Issue)](Hadoop/Tez_Job_Slowness_Network_RX.md)**: 네트워크 패킷 손실로 인한 성능 저하 디버깅
* **[Hazelcast IMDG](Hazelcast/README.md)**: 인메모리 데이터 그리드 아키텍처 (IMDB vs IMDG)

### 5. Linux Kernel & System Administration
* **[Linux 운영 & 트러블슈팅](Linux/README.md)**:
  * **[대용량 파일 전송 가이드 (Large File Transfer)](Linux/Large_File_Transfer.md)**: `rsync`, `tar`, `netcat`을 이용한 고속 네트워크 전송 및 무결성 검증
  * **[Linux 초기 서버 세팅 & 보안](Linux/Initial_Setup.md)**: 방화벽, SSH 강화, 타임존 동기화
  * **[Fail2Ban](Linux/Fail2Ban.md)**: 무차별 대입 공격(Brute-force) 자동 차단
  * **[Logrotate](Linux/Logrotate.md)**: 대규모 로그 파일 로테이션 및 압축 관리
