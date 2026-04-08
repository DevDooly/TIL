# TIL (Today I Learned)
> 배운 내용을 정리하는 저장소입니다.

---

## 🕒 최근 변경 사항 (Recent Changes)

<!-- RECENT_CHANGES_START -->
| 날짜 | 문서 | 설명 |
| :--- | :--- | :--- |
| 2026-04-08 10:50 | [Logstash Logback Encoder Guide](docs/Language/Java/SpringBoot/Logstash_Logback_Encoder_Guide.md) | docs: Logstash Logback Encoder 사용 가이드 및 SLF4J 2.0 ...  |
| 2026-04-08 10:48 | [ECS Logging KeyValuePairs](docs/Language/Java/SpringBoot/ECS_Logging_KeyValuePairs.md) | fix: ECS 로깅 addKeyValue 미지원 사실 확인 및 대안(MDC, Logsta...  |
| 2026-04-08 10:48 | [Logging ECS KeyValue Support](docs/Language/Java/SpringBoot/Logging_ECS_KeyValue_Support.md) | fix: ECS 로깅 addKeyValue 미지원 사실 확인 및 대안(MDC, Logsta...  |
| 2026-04-07 15:19 | [JDBI VT Pinning Solution](docs/Language/Java/SpringBoot/JDBI_VT_Pinning_Solution.md) | docs: JDBI 가상 스레드 Pinning 해결을 위한 하이브리드 모델 가이드 추가 |
| 2026-04-07 14:51 | [JDBI FetchSize and VirtualThreads](docs/Data/Database/JDBI_FetchSize_and_VirtualThreads.md) | docs: JDBI @FetchSize 옵션 설명 및 가상 스레드 시너지 가이드 추가 |
| 2026-04-07 13:25 | [Caffeine Cache](docs/Language/Java/Caffeine_Cache.md) | fix: 최근 변경 사항 중복 제거 로직 추가 및 스크립트 고도화 |

<!-- RECENT_CHANGES_END -->

[👉 전체 변경 로그 보기](docs/Recent_Changes.md)

---

## 목차 (Table of Contents)

<!-- TOC_START -->
### 📂 Categories
- [**Language**](#language)
- [**Web**](#web)
- [**Infrastructure**](#infrastructure)
- [**Data**](#data)
- [**ComputerScience**](#computerscience)
- [**Troubleshooting**](#troubleshooting)
- [**AI**](#ai)
- [**Tools**](#tools)
- [**History**](#history)
- [**Travel**](#travel)
- [**RealEstate**](#realestate)
- [**Templates**](#templates)

---

## Language
* [**Overview**](docs/Language/README.md)
* **Java**
  * [**Overview**](docs/Language/Java/README.md)
  * [Caffeine Cache: 고성능 Java 로컬 캐시 가이드](docs/Language/Java/Caffeine_Cache.md)
  * [Java Garbage Collection (GC)](docs/Language/Java/Garbage_Collection.md)
  * [Google Java Style Guide](docs/Language/Java/Google_Java_Style_Guide.md)
  * [Java Memory Structure (JVM Runtime Data Areas)](docs/Language/Java/Memory.md)
  * [Java Virtual Threads: FTP/SFTP 사용 시 Pinning 이슈](docs/Language/Java/Virtual_Threads_FTP_Pinning.md)
  * [K8s 환경에서의 Java Virtual Thread 사용 분석](docs/Language/Java/Virtual_Threads_in_K8s.md)
  * **Functional**
    * [**Overview**](docs/Language/Java/Functional/README.md)
    * [Functional Interfaces (함수형 인터페이스)](docs/Language/Java/Functional/Functional_Interfaces.md)
    * [Lambda Expressions (람다 표현식)](docs/Language/Java/Functional/Lambda.md)
    * [Optional](docs/Language/Java/Functional/Optional.md)
    * [Stream API](docs/Language/Java/Functional/Stream.md)
  * **SpringBoot**
    * [**Overview**](docs/Language/Java/SpringBoot/README.md)
    * [Aspect-Oriented Programming (AOP)](docs/Language/Java/SpringBoot/AOP.md)
    * [빈 후처리기 (BeanPostProcessor)](docs/Language/Java/SpringBoot/BeanPostProcessor.md)
    * [Spring Bean Lifecycle](docs/Language/Java/SpringBoot/Bean_Lifecycle.md)
    * [Dependency Injection (DI) & Inversion of Control (IoC)](docs/Language/Java/SpringBoot/DI_IoC.md)
    * [JDBI & 가상 스레드: Pinning 이슈 해결을 위한 하이브리드 모델](docs/Language/Java/SpringBoot/JDBI_VT_Pinning_Solution.md)
    * [Spring Boot: 로깅 설정 YAML에서 XML로의 전환 (SDK 충돌 해결)](docs/Language/Java/SpringBoot/Logging_Config_Migration_YAML_to_XML.md)
    * [Spring Boot: SLF4J addKeyValue를 ECS 로그에 포함하기 (대안 가이드)](docs/Language/Java/SpringBoot/Logging_ECS_KeyValue_Support.md)
    * [Logback XML: logback-ecs-encoder를 이용한 정형 로깅 (ECS)](docs/Language/Java/SpringBoot/Logging_ECS_XML_Encoder.md)
    * [Logstash Logback Encoder 사용 가이드](docs/Language/Java/SpringBoot/Logstash_Logback_Encoder_Guide.md)
    * [Spring Boot OAuth2 Implementation](docs/Language/Java/SpringBoot/OAuth2_Implementation.md)
    * [Spring Boot Introduction](docs/Language/Java/SpringBoot/SpringBoot_Intro.md)
    * [K8s 환경에서의 Spring 프로파일 및 설정 우선순위 이슈](docs/Language/Java/SpringBoot/Spring_Profile_Priority_in_K8s.md)
    * [Spring Boot 3.4: 정형 로깅(Structured Logging) 및 ECS 연동](docs/Language/Java/SpringBoot/Structured_Logging_SpringBoot_3_4.md)
    * [ThreadPoolTaskScheduler: Spring 작업 예약 및 스레드 풀 관리](docs/Language/Java/SpringBoot/ThreadPoolTaskScheduler.md)
    * [Java Virtual Thread: Kafka Consumer Pinning 이슈 분석](docs/Language/Java/SpringBoot/Virtual_Thread_Pinning_Kafka.md)
    * **JPA**
      * [**Overview**](docs/Language/Java/SpringBoot/JPA/README.md)
      * [JPA Persistence Context (영속성 컨텍스트)](docs/Language/Java/SpringBoot/JPA/Persistence_Context.md)
    * **Testing**
      * [Mockito: 단위 테스트를 위한 Mock 객체 활용 가이드](docs/Language/Java/SpringBoot/Testing/Mockito_Guide.md)
    * **Web**
      * [**Overview**](docs/Language/Java/SpringBoot/Web/README.md)
      * [Filter vs Interceptor](docs/Language/Java/SpringBoot/Web/Filter_vs_Interceptor.md)
      * [Servlet vs Servlet Container](docs/Language/Java/SpringBoot/Web/Servlet_vs_ServletContainer.md)
      * [Spring MVC (Model-View-Controller)](docs/Language/Java/SpringBoot/Web/SpringMVC.md)
      * [Spring WebFlux (Reactive Stack)](docs/Language/Java/SpringBoot/Web/SpringWebFlux.md)
  * **Versions**
    * [**Overview**](docs/Language/Java/Versions/README.md)
    * [Java 11: The Cloud Native LTS Standard](docs/Language/Java/Versions/Java11.md)
    * [Java 17: Modernization and Productivity](docs/Language/Java/Versions/Java17.md)
    * [Java 21: Next-Gen Concurrency and Performance](docs/Language/Java/Versions/Java21.md)
    * [Java 8: Modern Java의 시작](docs/Language/Java/Versions/Java8.md)
* **NodeJs**
  * [**Overview**](docs/Language/NodeJs/README.md)
  * [Yarn Berry (Yarn v2+)](docs/Language/NodeJs/Yarn Berry.md)
  * [Libuv](docs/Language/NodeJs/libuv.md)
* **Python**
  * [**Overview**](docs/Language/Python/README.md)
  * [client.py](docs/Language/Python/AIOHTTP vs Flask.md)
  * [Celery](docs/Language/Python/Celery.md)
  * [Comprehension](docs/Language/Python/Comprehension.md)
  * [Designing Modules in Python (모듈 설계)](docs/Language/Python/Designing Modules in Python.md)
  * [PyQt5](docs/Language/Python/PyQt5.md)
  * [Imports](docs/Language/Python/Refactoring.md)
  * [SQLAlchemy](docs/Language/Python/SQLAlchemy.md)
  * [Socket Programming](docs/Language/Python/Socket Programming.md)
  * [orjson](docs/Language/Python/orjson.md)
  * [Retry](docs/Language/Python/retry.md)
  * [Tokenizer](docs/Language/Python/tokenizer.md)
  * [MetaClass (메타클래스)](docs/Language/Python/메타클래스.md)
  * [정적메소드 (@staticmethod, @classmethod)](docs/Language/Python/정적메소드.md)
  * **Lib**
    * [asyncio](docs/Language/Python/Lib/asyncio.md)
    * [socketserver](docs/Language/Python/Lib/socketserver.md)
    * **asyncio**
      * [Stream](docs/Language/Python/Lib/asyncio/streams.md)
  * **Library**
    * [Keras](docs/Language/Python/Library/Keras.md)
  * **PyQt5**
    * **Custom**
  * **PySide6**
    * [**Overview**](docs/Language/Python/PySide6/README.md)
  * **Study**
    * [Decorator](docs/Language/Python/Study/Decorator.md)
    * [Python Study](docs/Language/Python/Study/READMD.md)
  * **Troubleshooting**
    * [Python Reinstall Server Failure](docs/Language/Python/Troubleshooting/Python_Reinstall_Server_Failure.md)
  * **pika**
    * [**Overview**](docs/Language/Python/pika/README.md)
    * [RabbitMQ / Asynchronous consumer example](docs/Language/Python/pika/Asynchronous consumer example.md)
    * [BlockingConnection](docs/Language/Python/pika/BlockingConnection.md)
  * **sys**
    * [**Overview**](docs/Language/Python/sys/README.md)
    * [sys.setrecursionlimit(limit)](docs/Language/Python/sys/sys.setrecursionlimit.md)

## Web
* [**Overview**](docs/Web/README.md)
* **Concepts**
  * [Ajax 그리고 CSR, SSR](docs/Web/Concepts/Ajax 그리고 CSR, SSR.md)
  * [용어 #](docs/Web/Concepts/WebRTC.md)
  * [Using shadow DOM](docs/Web/Concepts/shadow DOM.md)
* **Framework**
  * [Chart.js #](docs/Web/Framework/ChartJs.md)
  * [Electron](docs/Web/Framework/Electron.md)
  * [Vuejs](docs/Web/Framework/Vuejs.md)

## Infrastructure
* [**Overview**](docs/Infrastructure/README.md)
* **ArgoCD**
  * [**Overview**](docs/Infrastructure/ArgoCD/README.md)
  * [ArgoCD 실전 사용 예시 (App of Apps)](docs/Infrastructure/ArgoCD/Examples.md)
  * [ArgoCD 설치 가이드](docs/Infrastructure/ArgoCD/Installation.md)
  * [ArgoCD 사용 방법](docs/Infrastructure/ArgoCD/Usage.md)
* **Docker**
  * [**Overview**](docs/Infrastructure/Docker/README.md)
  * [Dockerfile](docs/Infrastructure/Docker/dockerfile.md)
  * [Docker: No space left on device 해결 방법](docs/Infrastructure/Docker/no space left on device.md)
* **Hadoop**
  * [**Overview**](docs/Infrastructure/Hadoop/README.md)
  * [Hadoop NameNode High Availability (HA)](docs/Infrastructure/Hadoop/NameNode_HA.md)
  * [Hadoop/Tez: 특정 노드 네트워크 RX Error로 인한 작업 지연 이슈](docs/Infrastructure/Hadoop/Tez_Job_Slowness_Network_RX.md)
* **Hazelcast**
  * [**Overview**](docs/Infrastructure/Hazelcast/README.md)
  * [인메모리 데이터베이스(IMDB) vs 인메모리 데이터 그리드(IMDG)](docs/Infrastructure/Hazelcast/IMDB_vs_IMDG.md)
* **Jenkins**
  * [**Overview**](docs/Infrastructure/Jenkins/README.md)
  * [Jenkins 사용 예시 (Pipeline)](docs/Infrastructure/Jenkins/Examples.md)
  * [Jenkins 설치 가이드](docs/Infrastructure/Jenkins/Installation_Docker_Linux.md)
  * [Jenkins 설치 가이드 (Kubernetes)](docs/Infrastructure/Jenkins/Installation_K8s.md)
  * [Jenkins 사용 방법](docs/Infrastructure/Jenkins/Usage.md)
* **Kubernetes**
  * [**Overview**](docs/Infrastructure/Kubernetes/README.md)
  * [🎡 Kubernetes Operator 패턴](docs/Infrastructure/Kubernetes/Operator_Pattern.md)
  * **CKA**
    * [**Overview**](docs/Infrastructure/Kubernetes/CKA/README.md)
    * [0. CKA 시험 개요 및 팁 (Exam Overview & Tips)](docs/Infrastructure/Kubernetes/CKA/CKA_Exam_Tips.md)
    * [1. 클러스터 아키텍처 및 컴포넌트](docs/Infrastructure/Kubernetes/CKA/Cluster_Architecture.md)
    * [1.2 ETCD 백업(Backup) 및 복원(Restore)](docs/Infrastructure/Kubernetes/CKA/ETCD_Backup_Restore.md)
    * [1.1 Kubeadm 클러스터 설치 및 업그레이드](docs/Infrastructure/Kubernetes/CKA/Kubeadm_Install_Upgrade.md)
    * [1.3 RBAC (Role-Based Access Control)](docs/Infrastructure/Kubernetes/CKA/RBAC_Authorization.md)
    * [2.3 리소스 제한 (Requests & Limits)](docs/Infrastructure/Kubernetes/CKA/Resource_Limits.md)
    * [2.2 스케줄링 제어 (Scheduling)](docs/Infrastructure/Kubernetes/CKA/Scheduling.md)
    * [2.1 워크로드 (Pod, Deployment, DaemonSet 등)](docs/Infrastructure/Kubernetes/CKA/Workloads.md)
* **Linux**
  * [**Overview**](docs/Infrastructure/Linux/README.md)
  * [Fail2Ban](docs/Infrastructure/Linux/Fail2Ban.md)
  * [Ubuntu Server 초기 셋팅 가이드](docs/Infrastructure/Linux/Initial_Setup.md)
  * [대량 파일 전송 가이드 (rsync 활용)](docs/Infrastructure/Linux/Large_File_Transfer.md)
  * [Logrotate (로그로테이트)](docs/Infrastructure/Linux/Logrotate.md)
  * [POSIX (Portable Operating System Interface)](docs/Infrastructure/Linux/POSIX.md)
  * [Single Quote vs Double Quote (Bash)](docs/Infrastructure/Linux/Single Quotation vs Double Quotation in bash.md)
  * [Stdin, Stdout, Stderr (표준 스트림)](docs/Infrastructure/Linux/Stdin, stdout, stderr.md)
  * [TL;DR (Too Long; Didn't Read)](docs/Infrastructure/Linux/TL;DR.md)
  * [Crontab (크론탭)](docs/Infrastructure/Linux/crontab.md)
  * **Tips**
    * [Mount OneDrive on Ubuntu](docs/Infrastructure/Linux/Tips/Mount OneDrive on Ubuntu.md)
* **MessageBroker**
  * [**Overview**](docs/Infrastructure/MessageBroker/README.md)
  * [AMQP (Advanced Message Queuing Protocol)](docs/Infrastructure/MessageBroker/AMQP.md)
  * [RabbitMQ vs Kafka](docs/Infrastructure/MessageBroker/RabbitMQ 그리고 Kafka.md)
  * **Kafka**
    * [**Overview**](docs/Infrastructure/MessageBroker/Kafka/README.md)
    * [Kafka Consumer: 특정 Offset 재소비 (Seek API)](docs/Infrastructure/MessageBroker/Kafka/Consumer_Offset_Control.md)
    * [Kafka 파티션 전략: 개수 산정과 증가 시 고려사항](docs/Infrastructure/MessageBroker/Kafka/Partition_Strategy.md)
    * [Kafka 파티셔너의 진화와 불균형(Imbalance) 문제 해결](docs/Infrastructure/MessageBroker/Kafka/Partitioner_Evolution_and_Imbalance.md)
    * [Kafka Producer: RoundRobinPartitioner 이슈 (KAFKA-9965)](docs/Infrastructure/MessageBroker/Kafka/Producer_Partitioner_Issue.md)
    * [Kafka Producer: 파티셔너(Partitioner) 정책 및 설정](docs/Infrastructure/MessageBroker/Kafka/Producer_Partitioner_Policy.md)
    * [Spring Kafka: 테스트 코드에서 단일 메시지 소비](docs/Infrastructure/MessageBroker/Kafka/Spring_Kafka_Test.md)
  * **RabbitMQ**
    * [**Overview**](docs/Infrastructure/MessageBroker/RabbitMQ/README.md)
    * [Editing RabbitMQ handle big message](docs/Infrastructure/MessageBroker/RabbitMQ/Editing RabbitMQ handle big message.md)
    * [설치](docs/Infrastructure/MessageBroker/RabbitMQ/설치.md)
    * **test**
* **MinIO**
  * [**Overview**](docs/Infrastructure/MinIO/README.md)
  * [MinIO Java Client 사용 예제](docs/Infrastructure/MinIO/Java_Client_Examples.md)
  * [MinIO 수명 주기 관리 (Lifecycle Management)](docs/Infrastructure/MinIO/Lifecycle.md)
  * [MinIO Client (mc) 설치 및 사용 가이드](docs/Infrastructure/MinIO/MinIO_Client_mc.md)
  * [MinIO 버저닝 (Versioning)](docs/Infrastructure/MinIO/Versioning.md)
* **OracleCloud**
  * [**Overview**](docs/Infrastructure/OracleCloud/README.md)

## Data
* [**Overview**](docs/Data/README.md)
* [ELK Stack](docs/Data/ELK.md)
* [로그 수집기 비교: Logstash vs Fluentd vs Fluent-bit](docs/Data/Log_Collectors_Comparison.md)
* **Database**
  * [**Overview**](docs/Data/Database/README.md)
  * [이미지 저장 및 관리 전략](docs/Data/Database/Image_Storage_Management.md)
  * [JDBI: @FetchSize 옵션과 가상 스레드(Virtual Thread) 최적화](docs/Data/Database/JDBI_FetchSize_and_VirtualThreads.md)
  * [비관적 락(Pessimistic Lock) vs 낙관적 락(Optimistic Lock)](docs/Data/Database/Locking_Strategy.md)
  * [MongoDB](docs/Data/Database/MongoDB.md)
  * [Oracle LOB Segment 및 ORA-01692 에러 조치](docs/Data/Database/Oracle_LOB_Segment.md)
  * [Redis (Remote Dictionary Server)](docs/Data/Database/Redis.md)
  * [SQL Naming Convention (SQL 명명 규칙)](docs/Data/Database/SQL_Naming_Convention.md)
  * [Fluentd](docs/Data/Database/fluentd.md)

## ComputerScience
* [**Overview**](docs/ComputerScience/README.md)
* **Architecture**
  * [**Overview**](docs/ComputerScience/Architecture/README.md)
  * [고가용성 (High Availability, HA)](docs/ComputerScience/Architecture/High_Availability.md)
  * [파이프라인 (Pipeline)](docs/ComputerScience/Architecture/Pipeline.md)
* **DesignPattern**
  * [**Overview**](docs/ComputerScience/DesignPattern/README.md)
  * [State Pattern (상태 패턴)](docs/ComputerScience/DesignPattern/StatePattern.md)
* **FileSystem**
  * [File System (파일 시스템)](docs/ComputerScience/FileSystem/FileSystem.md)
  * [HDF5 (Hierarchical Data Format version 5)](docs/ComputerScience/FileSystem/HDF5.md)
  * [LMDB (Lightning Memory-Mapped Database)](docs/ComputerScience/FileSystem/LMDB (Sysmas Lightning Memory-mapped Database).md)
  * [대량의 이미지를 파일시스템에 저장할 때](docs/ComputerScience/FileSystem/대량의 이미지를 파일시스템에 저장할 때.md)
* **Math**
  * [**Overview**](docs/ComputerScience/Math/README.md)
  * [Fourier Transform (푸리에 변환)](docs/ComputerScience/Math/Fourier transform.md)
* **Network**
  * [**Overview**](docs/ComputerScience/Network/README.md)
  * [OSI 7 Layer (OSI 7 계층)](docs/ComputerScience/Network/OSI 7 Layer.md)
  * [RPC (Remote Procedure Call)](docs/ComputerScience/Network/RPC.md)
  * [Socket (소켓)](docs/ComputerScience/Network/Socket.md)
  * [Subnetwork (서브넷)](docs/ComputerScience/Network/Subnetwork.md)
  * **DNS**
    * [DNS와 NameServer: 개념 이해 및 리눅스 설정 가이드](docs/ComputerScience/Network/DNS/DNS_and_NameServer.md)
* **OperatingSystem**
  * [Endianness (엔디언)](docs/ComputerScience/OperatingSystem/Endianness.md)
* **Security**
  * [**Overview**](docs/ComputerScience/Security/README.md)
  * [JWT (JSON Web Token) 및 인증 방식 비교](docs/ComputerScience/Security/JWT.md)
  * [OAuth 2.0 (Open Authorization 2.0)](docs/ComputerScience/Security/OAuth2.md)
  * [OIDC (OpenID Connect)](docs/ComputerScience/Security/OIDC.md)
* **SoftwareEngineering**
  * [Behavior-Driven Development (BDD)](docs/ComputerScience/SoftwareEngineering/BDD.md)
  * [소프트웨어 버저닝 (Software Versioning)](docs/ComputerScience/SoftwareEngineering/Versioning.md)

## Troubleshooting
* [**Overview**](docs/Troubleshooting/README.md)
  * [Virtual Thread Pinning 이슈 (FTP/SFTP)](docs/Language/Java/Virtual_Threads_FTP_Pinning.md)
  * [K8s 환경의 Virtual Thread 주의사항](docs/Language/Java/Virtual_Threads_in_K8s.md)
  * [Kafka Consumer 가상 스레드 Pinning 이슈](docs/Language/Java/SpringBoot/Virtual_Thread_Pinning_Kafka.md)
  * [JDBI 가상 스레드 Pinning 해결 패턴](docs/Language/Java/SpringBoot/JDBI_VT_Pinning_Solution.md)
  * [K8s Spring 프로파일 우선순위 이슈](docs/Language/Java/SpringBoot/Spring_Profile_Priority_in_K8s.md)
  * [로깅 설정 YAML to XML 전환 이슈](docs/Language/Java/SpringBoot/Logging_Config_Migration_YAML_to_XML.md)
  * [SLF4J addKeyValue를 ECS 로그에 포함하기](docs/Language/Java/SpringBoot/Logging_ECS_KeyValue_Support.md)
  * [Kafka RoundRobinPartitioner 불균형 (KAFKA-9965)](docs/Infrastructure/MessageBroker/Kafka/Producer_Partitioner_Issue.md)
  * [Kafka 최신 버전 Offset 불균형 문제](docs/Infrastructure/MessageBroker/Kafka/Partitioner_Evolution_and_Imbalance.md)
  * [Hadoop/Tez 네트워크 RX 에러로 인한 작업 지연](docs/Infrastructure/Hadoop/Tez_Job_Slowness_Network_RX.md)
  * [MinIO 버저닝 활성화 후 삭제 지연 이슈](docs/Troubleshooting/MinIO_Versioning_Deletion_Issue.md)
  * [Oracle LOB Segment 공간 부족 (ORA-01692)](docs/Data/Database/Oracle_LOB_Segment.md)
  * [Avro 필드명 'result' 사용 시 hashCode 충돌](docs/Troubleshooting/Avro_HashCode_Field_Naming_Conflict.md)

## AI
* [**Overview**](docs/AI/README.md)
* [Gemini CLI](docs/AI/Gemini_CLI.md)
* [Ollama](docs/AI/Ollama.md)
* [🖥️ 현재 PC (Ubuntu) Ollama 설치 및 API 설정 가이드](docs/AI/Ollama_Local_Environment_Setup.md)
* [OpenClaw](docs/AI/OpenClaw.md)
* [OpenCode](docs/AI/OpenCode.md)
* [TurboQuant: 초거대 언어 모델(LLM) 최적화의 혁신](docs/AI/TurboQuant.md)
* [n8n (Nodemation)](docs/AI/n8n.md)

## Tools
* [**Overview**](docs/Tools/README.md)
* **Git**
  * [Monorepo vs Polyrepo](docs/Tools/Git/Monorepo_vs_Polyrepo.md)
  * [Git Remote Settings (원격 저장소 관리)](docs/Tools/Git/Remote_Settings.md)
  * [Git Submodules (서브모듈)](docs/Tools/Git/Submodules.md)
  * [Git Tag](docs/Tools/Git/Tag.md)
  * [Git Tips](docs/Tools/Git/Tips.md)
* **Github**
  * [GitHub Actions MkDocs 배포 실패 (Plugin Missing)](docs/Tools/Github/Action_Deploy_Fail.md)
* **IDE**
  * [Intellij](docs/Tools/IDE/Intellij.md)
* **Markdown**
  * [Languages Supported by Github Flavored Markdown.md](docs/Tools/Markdown/Languages Supported by Github Flavored Markdown.md)
* **OpenSource**
  * [FFmpeg](docs/Tools/OpenSource/FFmpeg.md)
* **Productivity**
  * [Impress.js](docs/Tools/Productivity/Impress.js.md)
  * [Qlib](docs/Tools/Productivity/Qlib.md)
  * [Slidev](docs/Tools/Productivity/Slidev.md)
  * [sentry](docs/Tools/Productivity/sentry.md)
  * [zapier](docs/Tools/Productivity/zapier.md)
  * **ReadtheDocs**
    * [**Overview**](docs/Tools/Productivity/ReadtheDocs/README.md)
* **Terminal**
  * [**Overview**](docs/Tools/Terminal/README.md)
  * [Tmux (Terminal Multiplexer)](docs/Tools/Terminal/Tmux.md)

## History
* [**Overview**](docs/History/README.md)
* [🇹🇼 대만의 역사 (History of Taiwan)](docs/History/Taiwan.md)
* **Modern_Issues**
  * [미국-이란 갈등: 중동의 화약고 분석](docs/History/Modern_Issues/US_Iran_Conflict.md)

## Travel
* [**Overview**](docs/Travel/README.md)
* **Central_Europe**
  * [🇭🇺 부다페스트, 헝가리 (Budapest): 도나우의 진주 (7-9일차)](docs/Travel/Central_Europe/Budapest.md)
  * [🏰 중부 유럽의 봄: 제국의 흔적을 걷는 10일간의 여정](docs/Travel/Central_Europe/Overview.md)
  * [🇨🇿 프라하, 체코 (Prague): 중세 보헤미아의 낭만 (1-3일차)](docs/Travel/Central_Europe/Prague.md)
  * [🇦🇹 잘츠부르크, 오스트리아 (Salzburg): 알프스의 풍경과 모차르트 (3-5일차)](docs/Travel/Central_Europe/Salzburg.md)
  * [🇦🇹 비엔나, 오스트리아 (Vienna): 합스부르크의 영광과 예술 (5-7일차)](docs/Travel/Central_Europe/Vienna.md)
* **Taiwan**
  * [**Overview**](docs/Travel/Taiwan/README.md)
  * [🥃 카발란 증류소 (Kavalan Distillery)](docs/Travel/Taiwan/Kavalan_Distillery.md)
  * [💡 대만 여행 팁 (Travel Tips)](docs/Travel/Taiwan/Tips.md)

## RealEstate
* [**Overview**](docs/RealEstate/README.md)
* [📏 국민평형(전용 85㎡) 초과 시 달라지는 세금 및 규제](docs/RealEstate/Tax_85sqm_Rules.md)

## Templates
* [**Overview**](docs/Templates/README.md)
* [[양식] 기술 이슈 분석 및 리포트](docs/Templates/Issue_Report_Template.md)

## Life
* [Development Trends](docs/Life/Trends.md)
* **Career**
  * [Reference Check(평판 조회)](docs/Life/Career/Reference Check.md)
* **Health**
  * [🦶 족저근막염 (Plantar Fasciitis) 가이드](docs/Life/Health/Plantar_Fasciitis.md)

<!-- TOC_END -->