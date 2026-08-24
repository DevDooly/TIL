---
title: Resume - Backend & Systems Engineer
---

# 📄 Resume & Career Profile

## 👤 Profile

**대용량 분산 시스템 & 백엔드 엔지니어 (Senior Backend / Systems Engineer)**

> "복잡한 동시성 제어, 분산 메시징, 성능 병목 진단 및 클라우드 네이티브 아키텍처를 설계하고 구현합니다."

* 🌐 **Portfolio & Wiki**: [https://devdooly.github.io/TIL/](https://devdooly.github.io/TIL/)
* 💻 **GitHub**: [https://github.com/DevDooly](https://github.com/DevDooly)
* ✉️ **Contact**: devdooly@example.com *(필요 시 수정)*

---

## 🛠 Technical Skills

| Domain | Technologies & Libraries |
| :--- | :--- |
| **Backend & Concurrency** | **Java (8 ~ 21+)**, **Spring Boot 3.x**, **Virtual Threads (Loom)**, JPA/Hibernate, JDBI, Reactive (WebFlux), **Python 3.12**, FastAPI, Celery, Node.js (libuv) |
| **Data & Storage** | **Apache Kafka**, **RabbitMQ (AMQP)**, **Redis**, **Oracle Database**, **MinIO (S3-compatible)**, Apache Arrow (Zero-copy mmap), MongoDB, ElasticSearch |
| **DevOps & Cloud Native** | **Kubernetes (K8s)**, **Docker / Containerization**, **ArgoCD (GitOps)**, **Jenkins**, Linux (Kernel Tuning, Large File Transfer), Oracle Cloud |
| **AI & Productivity** | **AI Coding Agents (Antigravity CLI / agy)**, Multi-Agent Orchestration (Orca/Paseo), LLM Development Workflows, Offline/Air-gapped Package Distribution |
| **Build & Quality** | Maven (Multi-module, Shade Plugin, Classifier), Spotless, Google Java Format, Git (Monorepo, Submodules, GitFlow) |

---

## 💼 Core Competencies & Experience Highlights

### 1. High-Performance Concurrency & JVM Optimization
* **Virtual Threads (Project Loom) 실무 적용 및 Pinning 이슈 해결**:
  * Java 21 가상 스레드 환경에서 레거시 라이브러리의 `synchronized` 블록으로 인한 OS 캐리어 스레드 고갈(Pinning) 문제 진단 및 `ReentrantLock` 리팩토링.
  * DB Blocking I/O 구간에서 JDBI와 가상 스레드를 조화롭게 운용하기 위한 하이브리드 스레드 풀 모델 구축.
* **Java-Python 프로세스 간 Zero-Copy 공유 메모리 아키텍처**:
  * 대용량 데이터 처리 시 JSON/REST IPC의 직렬화 오버헤드를 극복하기 위해 **Apache Arrow IPC & mmap(Memory-Mapped Files)** 기반의 Zero-copy 데이터 파이프라인 구현, 데이터 처리 처리량 극대화.

### 2. Distributed Messaging & Stream Architecture
* **Apache Kafka 파티셔닝 전략 및 컨슈머 안정성 확보**:
  * Kafka Producer의 `DefaultPartitioner` 동작 방식(UniformStickyPartitioner) 변화에 따른 파티션 쏠림 이슈를 분석하고, 배치 크기와 링거 타임 튜닝을 통해 균등 분산 달성.
  * Graceful Shutdown 메커니즘을 적용하여 컨슈머 재시작 시 리밸런싱 지연 및 `IllegalStateException` 방지.
* **대용량 오브젝트 스토리지(MinIO) 운영 및 라이프사이클 최적화**:
  * S3 버저닝 활성화에 따른 Delete Marker 누적 및 용량 비대화 문제를 진단하고, 자동화된 라이프사이클 룰 및 배치 삭제 파이프라인 수립.

### 3. Cloud-Native CI/CD & Infrastructure Automation
* **Kubernetes 기반 GitOps (ArgoCD) & Jenkins 파이프라인 구축**:
  * 멀티 환경(Dev/Stage/Prod) 배포 파이프라인을 선언적 GitOps 방식으로 표준화.
  * K8s 환경에서 Spring Boot 어플리케이션의 CPU Throttling, JVM 메모리 튜닝(MaxRAMPercentage) 및 로깅 구조화(Spring Boot 3.4 Structured Logging & ECS 포맷) 적용.
* **폐쇄망(Air-Gapped) 환경 자동화 및 도구 구축**:
  * 외부 인터넷이 차단된 환경에서 Python 3.12, venv, pip 의존성 패키지 휠(wheel) 오프라인 빌드 및 사내 인프라 표준화.

---

## 🏆 Key Engineering Achievements & Troubleshooting

실제 서비스 및 시스템 구축 중 마주한 기술적 난제를 해결한 대표 사례입니다. (자세한 분석은 문서 링크 참조)

1. [**Java Virtual Threads: FTP Pinning 이슈 분석 및 개선**](Language/Java/Virtual_Threads_FTP_Pinning.md)
   - *문제*: FTP 대용량 파일 전송 중 가상 스레드가 캐리어 스레드를 점유(Pinning)하여 전체 서버 응답 불능 발생.
   - *해결*: JFR(Java Flight Recorder)로 Pinning 지점 검출 후 `synchronized` 블록을 `ReentrantLock` 및 전용 I/O 스레드 풀로 분리하여 처리량 400% 개선.

2. [**Kafka Producer Partitioner 진화 및 파티션 불균형 해결**](Infrastructure/MessageBroker/Kafka/Partitioner_Evolution_and_Imbalance.md)
   - *문제*: 프로듀서 버전 업그레이드 후 특정 파티션에만 트래픽이 쏠려 컨슈머 lag 급증.
   - *해결*: Sticky Partitioner의 batch flush 메커니즘 분석 및 파티셔너 정책 재조정으로 부하 분산 최적화.

3. [**MinIO 버저닝 환경 파일 영구 삭제 및 누수 해결**](Troubleshooting/MinIO_Versioning_Deletion_Issue.md)
   - *문제*: 버저닝 활성화된 버킷에서 객체 삭제 시 실제 스토리지가 반환되지 않는 현상.
   - *해결*: VersionId 명시 삭제 및 Expiration Lifecycle Rule 정립을 통한 스토리지 자원 회수.

4. [**Apache Avro 'result' 필드명 충돌 디버깅**](Troubleshooting/Avro_HashCode_Field_Naming_Conflict.md)
   - *문제*: 스키마 정의 필드명과 자동 생성된 `hashCode()` 로컬 변수명이 충돌하는 컴파일 에러.
   - *해결*: Avro 컴파일러 네이밍 전략 분석 및 스키마 명명 규칙 표준화.

---

## 🎓 Education & Certifications

* **Computer Science & Engineering** 학사
* **CKA (Certified Kubernetes Administrator)** *(해당 시 기재)*

---

## 📚 Open Source & Technical Writing

* **개인 엔지니어링 위키 & 포트폴리오 운영**: [https://devdooly.github.io/TIL/](https://devdooly.github.io/TIL/)
* 실무 지식 및 아키텍처 분석 문서 100+ 편 지속적 작성 및 공유.
