# 📚 TIL 전체 문서 목차

모든 기술 지식을 한눈에 확인하고 바로 이동할 수 있습니다.

## 📁 Troubleshooting

* [🛠️ 실전 엔지니어링 트러블슈팅 아카이브](Troubleshooting/README.md)
    * [**분석 문서 보기**](Language/Java/Virtual_Threads_FTP_Pinning.md)
    * [**분석 문서 보기**](Language/Java/Virtual_Threads_in_K8s.md)
    * [**분석 문서 보기**](Language/Java/SpringBoot/Virtual_Thread_Pinning_Kafka.md)
    * [**분석 문서 보기**](Language/Java/SpringBoot/JDBI_VT_Pinning_Solution.md)
    * [**분석 문서 보기**](Language/Java/SpringBoot/Spring_Profile_Priority_in_K8s.md)
    * [**분석 문서 보기**](Language/Java/SpringBoot/Logging_Config_Migration_YAML_to_XML.md)
    * [**분석 문서 보기**](Language/Java/SpringBoot/Logging_ECS_KeyValue_Support.md)
    * [**분석 문서 보기**](Infrastructure/MessageBroker/Kafka/Producer_Partitioner_Issue.md)
    * [**분석 문서 보기**](Infrastructure/MessageBroker/Kafka/Partitioner_Evolution_and_Imbalance.md)
    * [**분석 문서 보기**](Infrastructure/MessageBroker/Kafka/AbortOnNewBatch_Issue.md)
    * [**분석 문서 보기**](Infrastructure/MessageBroker/Kafka/Consumer_Safe_Shutdown.md)
    * [**분석 문서 보기**](Infrastructure/Hadoop/Tez_Job_Slowness_Network_RX.md)
    * [**분석 문서 보기**](Infrastructure/Linux/Large_File_Transfer.md)
    * [**분석 문서 보기**](Troubleshooting/MinIO_Versioning_Deletion_Issue.md)
    * [**분석 문서 보기**](Data/Database/Oracle_LOB_Segment.md)
    * [**분석 문서 보기**](Troubleshooting/Avro_HashCode_Field_Naming_Conflict.md)

## 📁 Language

* [☕ Language & Runtime Ecosystem](Language/README.md)
    * **Java**
        * [☕ Java & JVM Ecosystem](Language/Java/README.md)
        * [Apache Arrow BufferAllocator 관리 및 멀티스레드 활용 가이드](Language/Java/Apache_Arrow_BufferAllocator_Management.md)
        * [Apache Arrow를 이용한 Java-Python 고성능 데이터 공유 가이드](Language/Java/Apache_Arrow_Memory_Mapped_File.md)
        * [Apache Arrow & mmap을 이용한 Zero-copy 데이터 공유](Language/Java/Apache_Arrow_with_mmap.md)
        * [Caffeine Cache: 고성능 Java 로컬 캐시 가이드](Language/Java/Caffeine_Cache.md)
        * [Java/Spring Boot: 현재 스레드가 가상 스레드인지 확인하는 방법](Language/Java/Check_Virtual_Thread.md)
        * [Java: Collections.emptyList() vs List.of() 비교](Language/Java/Collections.emptyList_vs_List.of.md)
        * [Java: Concatenated GZIP 스트림 압축 해제 (Unzip)](Language/Java/Concatenated_Gzip_Decompression.md)
        * [Java Effectively Final](Language/Java/Effectively_Final.md)
        * [Java Garbage Collection (GC)](Language/Java/Garbage_Collection.md)
        * [Google Java Style Guide](Language/Java/Google_Java_Style_Guide.md)
        * [Java와 Python의 대용량 데이터 교환: Apache Arrow & mmap](Language/Java/Java_Python_Shared_Memory_Arrow.md)
        * [Java Memory Structure (JVM Runtime Data Areas)](Language/Java/Memory.md)
        * [Java-Python 실행 성능 최적화 가이드](Language/Java/Optimizing_Java_Python_Execution.md)
        * [Java: Scoped Value - 가상 스레드 시대를 위한 새로운 데이터 공유 메커니즘](Language/Java/Scoped_Value.md)
        * [Java/Spring Boot와 Python 연동 가이드](Language/Java/Spring_Python_Integration.md)
        * [Java ThreadPoolExecutor와 거부 정책(Rejection Policy)](Language/Java/ThreadPoolExecutor.md)
        * [Java Virtual Threads: FTP/SFTP 사용 시 Pinning 이슈](Language/Java/Virtual_Threads_FTP_Pinning.md)
        * [K8s 환경에서의 Java Virtual Thread 사용 분석](Language/Java/Virtual_Threads_in_K8s.md)
        * **Versions**
            * [Java Versions History](Language/Java/Versions/README.md)
            * [Java 11: The Cloud Native LTS Standard](Language/Java/Versions/Java11.md)
            * [Java 17: Modernization and Productivity](Language/Java/Versions/Java17.md)
            * [Java 21: Next-Gen Concurrency and Performance](Language/Java/Versions/Java21.md)
            * [Java 25: Enhanced Stability and Modern Productivity](Language/Java/Versions/Java25.md)
            * [Java 8: Modern Java의 시작](Language/Java/Versions/Java8.md)
        * **Functional**
            * [Java Functional Programming](Language/Java/Functional/README.md)
            * [Functional Interfaces (함수형 인터페이스)](Language/Java/Functional/Functional_Interfaces.md)
            * [Lambda Expressions (람다 표현식)](Language/Java/Functional/Lambda.md)
            * [Optional](Language/Java/Functional/Optional.md)
            * [Stream API](Language/Java/Functional/Stream.md)
        * **SpringBoot**
            * [🍃 Spring Boot Framework](Language/Java/SpringBoot/README.md)
            * [Aspect-Oriented Programming (AOP)](Language/Java/SpringBoot/AOP.md)
            * [빈 후처리기 (BeanPostProcessor)](Language/Java/SpringBoot/BeanPostProcessor.md)
            * [Spring Bean Lifecycle](Language/Java/SpringBoot/Bean_Lifecycle.md)
            * [Dependency Injection (DI) & Inversion of Control (IoC)](Language/Java/SpringBoot/DI_IoC.md)
            * [Spring Boot: @EnableAutoConfiguration vs @ConfigurationPropertiesScan 비교](Language/Java/SpringBoot/EnableAutoConfiguration_vs_ConfigurationPropertiesScan.md)
            * [Netty 환경에서 Blocking 코드/라이브러리를 찾는 방법](Language/Java/SpringBoot/Finding_Blocking_Operations.md)
            * [JDBI & 가상 스레드: Pinning 이슈 해결을 위한 하이브리드 모델](Language/Java/SpringBoot/JDBI_VT_Pinning_Solution.md)
            * [Logback: LoggingEventCompositeJsonEncoder와 springProperty 활용 가이드](Language/Java/SpringBoot/Logback_JSON_Composite_Encoder.md)
            * [Spring Boot: 로깅 설정 YAML에서 XML로의 전환 (SDK 충돌 해결)](Language/Java/SpringBoot/Logging_Config_Migration_YAML_to_XML.md)
            * [Spring Boot: SLF4J addKeyValue를 ECS 로그에 포함하기 (대안 가이드)](Language/Java/SpringBoot/Logging_ECS_KeyValue_Support.md)
            * [Logback XML: logback-ecs-encoder를 이용한 정형 로깅 (ECS)](Language/Java/SpringBoot/Logging_ECS_XML_Encoder.md)
            * [Logstash Logback Encoder 사용 가이드](Language/Java/SpringBoot/Logstash_Logback_Encoder_Guide.md)
            * [Netflix Ribbon: 클라이언트 측 부하 분산(Load Balancing) 가이드](Language/Java/SpringBoot/Netflix_Ribbon_Guide.md)
            * [Spring Boot OAuth2 Implementation](Language/Java/SpringBoot/OAuth2_Implementation.md)
            * [Spring Cloud Gateway vs Netflix Zuul: 아키텍처 비교 및 선택 가이드](Language/Java/SpringBoot/SCG_vs_Zuul_Comparison.md)
            * [Spring Boot Introduction](Language/Java/SpringBoot/SpringBoot_Intro.md)
            * [Spring Cloud Gateway (SCG): 차세대 API Gateway 가이드](Language/Java/SpringBoot/Spring_Cloud_Gateway.md)
            * [Spring Cloud LoadBalancer: 현대적인 클라이언트 측 부하 분산 가이드](Language/Java/SpringBoot/Spring_Cloud_LoadBalancer.md)
            * [Spring Cloud Zuul: API Gateway 및 동적 라우팅 가이드](Language/Java/SpringBoot/Spring_Cloud_Zuul.md)
            * [Spring Data JPA: CrudRepository 가이드](Language/Java/SpringBoot/Spring_Data_JPA_CrudRepository.md)
            * [비교: 직접 쿼리 작성(JDBI/JDBC) vs Spring Data JPA (CrudRepository)](Language/Java/SpringBoot/Spring_Data_JPA_vs_JDBI.md)
            * [K8s 환경에서의 Spring 프로파일 및 설정 우선순위 이슈](Language/Java/SpringBoot/Spring_Profile_Priority_in_K8s.md)
            * [Spring Boot 3.4: 정형 로깅(Structured Logging) 및 ECS 연동](Language/Java/SpringBoot/Structured_Logging_SpringBoot_3_4.md)
            * [ThreadPoolTaskScheduler: Spring 작업 예약 및 스레드 풀 관리](Language/Java/SpringBoot/ThreadPoolTaskScheduler.md)
            * [Spring Boot: Tomcat vs Netty 비교 가이드](Language/Java/SpringBoot/Tomcat_vs_Netty.md)
            * [Java Virtual Thread: Kafka Consumer Pinning 이슈 분석](Language/Java/SpringBoot/Virtual_Thread_Pinning_Kafka.md)
            * **JPA**
                * [Spring Data JPA](Language/Java/SpringBoot/JPA/README.md)
                * [JPA Persistence Context (영속성 컨텍스트)](Language/Java/SpringBoot/JPA/Persistence_Context.md)
            * **Testing**
                * [Mockito: 단위 테스트를 위한 Mock 객체 활용 가이드](Language/Java/SpringBoot/Testing/Mockito_Guide.md)
            * **Web**
                * [Spring Web Development](Language/Java/SpringBoot/Web/README.md)
                * [Filter vs Interceptor](Language/Java/SpringBoot/Web/Filter_vs_Interceptor.md)
                * [Servlet vs Servlet Container](Language/Java/SpringBoot/Web/Servlet_vs_ServletContainer.md)
                * [Spring MVC (Model-View-Controller)](Language/Java/SpringBoot/Web/SpringMVC.md)
                * [Spring WebFlux (Reactive Stack)](Language/Java/SpringBoot/Web/SpringWebFlux.md)
    * **NodeJs**
        * [Node.js](Language/NodeJs/README.md)
        * [Yarn Berry (Yarn v2+)](Language/NodeJs/Yarn Berry.md)
        * [⚡ Libuv & Node.js 비동기 I/O 아키텍처](Language/NodeJs/libuv.md)
    * **Python**
        * [🐍 Python Engineering & Concurrency](Language/Python/README.md)
        * [client.py](Language/Python/AIOHTTP vs Flask.md)
        * [Stream](Language/Python/Asyncio_Streams.md)
        * [Python 스크립트 실행 가이드: `python3 main.py`](Language/Python/Basic_Execution_Guide.md)
        * [Celery](Language/Python/Celery.md)
        * [Comprehension](Language/Python/Comprehension.md)
        * [Anaconda vs Miniconda: 차이점과 환경 구축 가이드](Language/Python/Conda_Anaconda_Miniconda.md)
        * [🐍 Python Decorator (데코레이터)](Language/Python/Decorator.md)
        * [Designing Modules in Python (모듈 설계)](Language/Python/Designing Modules in Python.md)
        * [FastAPI의 동시성(Concurrency) 처리 메커니즘](Language/Python/FastAPI_Concurrency_Mechanism.md)
        * [Gunicorn vs Uvicorn: 개념과 운영 환경 구축 전략](Language/Python/Gunicorn_vs_Uvicorn.md)
        * [폐쇄망 환경 Python 3.12 설치 가이드 (최신 안정 버전)](Language/Python/Offline_Installation_Guide.md)
        * [오프라인 환경에서 `venv` 및 `pip` 패키지 설치 가이드](Language/Python/Offline_Venv_Pip_Guide.md)
        * [Imports](Language/Python/Refactoring.md)
        * [SQLAlchemy](Language/Python/SQLAlchemy.md)
        * [Python Web Server 실행 방식 비교: `python main.py` vs CLI Runner](Language/Python/Server_Execution_Methods.md)
        * [Socket Programming](Language/Python/Socket Programming.md)
        * [socketserver](Language/Python/SocketServer.md)
        * [orjson](Language/Python/orjson.md)
        * [Retry](Language/Python/retry.md)
        * [Tokenizer](Language/Python/tokenizer.md)
        * [venv vs Conda: 어떤 가상환경을 선택해야 할까?](Language/Python/venv_vs_Conda.md)
        * [MetaClass (메타클래스)](Language/Python/메타클래스.md)
        * [정적메소드 (@staticmethod, @classmethod)](Language/Python/정적메소드.md)
        * **pika**
            * [Pika](Language/Python/pika/README.md)
            * [RabbitMQ / Asynchronous consumer example](Language/Python/pika/Asynchronous consumer example.md)
            * [BlockingConnection](Language/Python/pika/BlockingConnection.md)
        * **Troubleshooting**
            * [Python_Reinstall_Server_Failure.md](Language/Python/Troubleshooting/Python_Reinstall_Server_Failure.md)

## 📁 Infrastructure

* [🏗️ Infrastructure & Cloud Native](Infrastructure/README.md)
    * **MessageBroker**
        * [Message Broker (메시지 브로커)](Infrastructure/MessageBroker/README.md)
        * [AMQP (Advanced Message Queuing Protocol)](Infrastructure/MessageBroker/AMQP.md)
        * [NATS (Neural Autonomic Transport System)](Infrastructure/MessageBroker/NATS.md)
        * [RabbitMQ vs Kafka](Infrastructure/MessageBroker/RabbitMQ 그리고 Kafka.md)
        * **Kafka**
            * [Apache Kafka](Infrastructure/MessageBroker/Kafka/README.md)
            * [Kafka: abortOnNewBatch 매커니즘과 파티션 쏠림 이슈](Infrastructure/MessageBroker/Kafka/AbortOnNewBatch_Issue.md)
            * [Kafka Consumer: 특정 Offset 재소비 (Seek API)](Infrastructure/MessageBroker/Kafka/Consumer_Offset_Control.md)
            * [Kafka: Consumer의 안전한 종료 (wakeup vs close)](Infrastructure/MessageBroker/Kafka/Consumer_Safe_Shutdown.md)
            * [Kafka 메시지 최대 사이즈 확장 가이드 (Broker 재기동 없이)](Infrastructure/MessageBroker/Kafka/Kafka_Message_Size_Configuration.md)
            * [Kafka Broker 롤링 재시작 가이드 (3대 HA 구성)](Infrastructure/MessageBroker/Kafka/Kafka_Rolling_Restart_Guide.md)
            * [Kafka 파티션 전략: 개수 산정과 증가 시 고려사항](Infrastructure/MessageBroker/Kafka/Partition_Strategy.md)
            * [Kafka 파티셔너의 진화와 불균형(Imbalance) 문제 해결](Infrastructure/MessageBroker/Kafka/Partitioner_Evolution_and_Imbalance.md)
            * [Kafka Producer: RoundRobinPartitioner 이슈 (KAFKA-9965)](Infrastructure/MessageBroker/Kafka/Producer_Partitioner_Issue.md)
            * [Kafka Producer: 파티셔너(Partitioner) 정책 및 설정](Infrastructure/MessageBroker/Kafka/Producer_Partitioner_Policy.md)
            * [Spring Kafka: 테스트 코드에서 단일 메시지 소비](Infrastructure/MessageBroker/Kafka/Spring_Kafka_Test.md)
    * **Jenkins**
        * [Jenkins (젠킨스)](Infrastructure/Jenkins/README.md)
        * [Jenkins 실전 사용 예시 (Pipeline)](Infrastructure/Jenkins/Examples.md)
        * [Jenkins 설치 가이드](Infrastructure/Jenkins/Installation_Docker_Linux.md)
        * [Jenkins 설치 가이드 (Kubernetes)](Infrastructure/Jenkins/Installation_K8s.md)
        * [Jenkins 사용 방법 및 실무 설정 가이드](Infrastructure/Jenkins/Usage.md)
    * **Docker**
        * [Docker](Infrastructure/Docker/README.md)
        * [Docker 이미지 버전 관리(Versioning) 전략](Infrastructure/Docker/docker_image_versioning_strategy.md)
        * [Dockerfile](Infrastructure/Docker/dockerfile.md)
        * [Docker: No space left on device 해결 방법](Infrastructure/Docker/no space left on device.md)
    * **Kubernetes**
        * [☸️ Kubernetes](Infrastructure/Kubernetes/README.md)
        * [🎡 Kubernetes Operator 패턴](Infrastructure/Kubernetes/Operator_Pattern.md)
        * **CKA**
            * [☸️ Kubernetes (CKA 준비)](Infrastructure/Kubernetes/CKA/README.md)
            * [0. CKA 시험 개요 및 팁 (Exam Overview & Tips)](Infrastructure/Kubernetes/CKA/CKA_Exam_Tips.md)
            * [1. 클러스터 아키텍처 및 컴포넌트](Infrastructure/Kubernetes/CKA/Cluster_Architecture.md)
            * [1.2 ETCD 백업(Backup) 및 복원(Restore)](Infrastructure/Kubernetes/CKA/ETCD_Backup_Restore.md)
            * [1.1 Kubeadm 클러스터 설치 및 업그레이드](Infrastructure/Kubernetes/CKA/Kubeadm_Install_Upgrade.md)
            * [1.3 RBAC (Role-Based Access Control)](Infrastructure/Kubernetes/CKA/RBAC_Authorization.md)
            * [2.3 리소스 제한 (Requests & Limits)](Infrastructure/Kubernetes/CKA/Resource_Limits.md)
            * [2.2 스케줄링 제어 (Scheduling)](Infrastructure/Kubernetes/CKA/Scheduling.md)
            * [2.1 워크로드 (Pod, Deployment, DaemonSet 등)](Infrastructure/Kubernetes/CKA/Workloads.md)
    * **Hadoop**
        * [Hadoop (Apache Hadoop)](Infrastructure/Hadoop/README.md)
        * [Hadoop NameNode High Availability (HA)](Infrastructure/Hadoop/NameNode_HA.md)
        * [Hadoop/Tez: 특정 노드 네트워크 RX Error로 인한 작업 지연 이슈](Infrastructure/Hadoop/Tez_Job_Slowness_Network_RX.md)
    * **OracleCloud**
        * [Oracle Cloud Free Tier (오라클 클라우드 프리티어)](Infrastructure/OracleCloud/README.md)
        * [HAProxy를 통한 Oracle DB 접속 지연 진단 가이드](Infrastructure/OracleCloud/HAProxy_Oracle_Latency_Diagnosis.md)
    * **Hazelcast**
        * [🌰 Hazelcast (IMDG)](Infrastructure/Hazelcast/README.md)
        * [인메모리 데이터베이스(IMDB) vs 인메모리 데이터 그리드(IMDG)](Infrastructure/Hazelcast/IMDB_vs_IMDG.md)
    * **MinIO**
        * [MinIO](Infrastructure/MinIO/README.md)
        * [MinIO Java Client 사용 예제](Infrastructure/MinIO/Java_Client_Examples.md)
        * [MinIO 수명 주기 관리 (Lifecycle / ILM)](Infrastructure/MinIO/Lifecycle.md)
        * [MinIO Client (mc) 설치 및 사용 가이드](Infrastructure/MinIO/MinIO_Client_mc.md)
        * [MinIO 버저닝 (Versioning)](Infrastructure/MinIO/Versioning.md)
    * **ArgoCD**
        * [ArgoCD](Infrastructure/ArgoCD/README.md)
        * [ArgoCD 실전 사용 예시 (App of Apps, Kustomize, ApplicationSet)](Infrastructure/ArgoCD/Examples.md)
        * [ArgoCD 설치 가이드](Infrastructure/ArgoCD/Installation.md)
        * [ArgoCD 사용 방법 및 운영 가이드](Infrastructure/ArgoCD/Usage.md)
    * **Linux**
        * [🐧 Linux Administration & Performance](Infrastructure/Linux/README.md)
        * [Fail2Ban](Infrastructure/Linux/Fail2Ban.md)
        * [Ubuntu Server 초기 셋팅 가이드](Infrastructure/Linux/Initial_Setup.md)
        * [대량 파일 전송 가이드 (rsync 활용)](Infrastructure/Linux/Large_File_Transfer.md)
        * [Logrotate (로그로테이트)](Infrastructure/Linux/Logrotate.md)
        * [POSIX (Portable Operating System Interface)](Infrastructure/Linux/POSIX.md)
        * [Stdin, Stdout, Stderr (표준 스트림)](Infrastructure/Linux/Stdin, stdout, stderr.md)
        * [TL;DR (Too Long; Didn't Read)](Infrastructure/Linux/TL;DR.md)
        * [Crontab (크론탭)](Infrastructure/Linux/crontab.md)

## 📁 Data

* [💾 Data Systems & Storage Architecture](Data/README.md)
* [ELK Stack](Data/ELK.md)
* [로그 수집기 비교: Logstash vs Fluentd vs Fluent-bit](Data/Log_Collectors_Comparison.md)
    * **Database**
        * [Database (데이터베이스)](Data/Database/README.md)
        * [이미지 저장 및 관리 전략](Data/Database/Image_Storage_Management.md)
        * [JDBI: @FetchSize 옵션과 가상 스레드(Virtual Thread) 최적화](Data/Database/JDBI_FetchSize_and_VirtualThreads.md)
        * [비관적 락(Pessimistic Lock) vs 낙관적 락(Optimistic Lock)](Data/Database/Locking_Strategy.md)
        * [MongoDB](Data/Database/MongoDB.md)
        * [Oracle LOB Segment 및 ORA-01692 에러 조치](Data/Database/Oracle_LOB_Segment.md)
        * [⚡ Redis (Remote Dictionary Server)](Data/Database/Redis.md)
        * [SQL Naming Convention (SQL 명명 규칙)](Data/Database/SQL_Naming_Convention.md)
        * [Fluentd](Data/Database/fluentd.md)

## 📁 AI

* [AI Tools & Agents](AI/README.md)
* [Antigravity CLI (agy) vs OpenCode (with Gemini) 비교 가이드](AI/AGY_vs_OpenCode_Comparison.md)
* [AI 코딩 에이전트 오케스트레이터: Orca vs Paseo](AI/AI_Coding_Agent_Orchestrators_Orca_Paseo.md)
* [Antigravity CLI - 자동 승인(Auto-Approve) 및 권한 설정 가이드](AI/Antigravity_CLI_Configuration.md)
* [Antigravity CLI (`agy`) 스킬 설치, 설정 및 활용 가이드](AI/Antigravity_CLI_Skills_Guide.md)
* [Claude CLI - 다중 모델(Multi-Model) 및 DeepSeek 연동 가이드 (Windows)](AI/Claude_CLI_DeepSeek_Setup.md)
* [Gemini CLI](AI/Gemini_CLI.md)
* [Ollama](AI/Ollama.md)
* [🖥️ 현재 PC (Ubuntu) Ollama 설치 및 API 설정 가이드](AI/Ollama_Local_Environment_Setup.md)
* [OpenClaw](AI/OpenClaw.md)
* [OpenCode](AI/OpenCode.md)
* [Paseo 설치 및 모바일 원격 제어 설정 가이드](AI/Paseo_Setup_and_Usage.md)
* [Qwen CLI - API Key 재등록 및 설정 가이드](AI/Qwen_CLI_Setup.md)
* [TurboQuant: 초거대 언어 모델(LLM) 최적화의 혁신](AI/TurboQuant.md)
* [n8n (Nodemation)](AI/n8n.md)

## 📁 LLM_Development

* [LLM Development Guide (LLM 개발 가이드)](LLM_Development/README.md)
* [Backend Development with LLM (백엔드 개발 시 LLM 활용 가이드)](LLM_Development/Backend_Development_Checklist.md)
* [Web Development with LLM (웹 개발 시 LLM 활용 가이드)](LLM_Development/Web_Development_Checklist.md)

## 📁 ComputerScience

* [🏛️ Computer Science & Fundamental Systems](ComputerScience/README.md)
    * **Security**
        * [Security (보안)](ComputerScience/Security/README.md)
        * [JWT (JSON Web Token) 및 인증 방식 비교](ComputerScience/Security/JWT.md)
        * [OAuth 2.0 (Open Authorization 2.0)](ComputerScience/Security/OAuth2.md)
        * [OIDC (OpenID Connect)](ComputerScience/Security/OIDC.md)
    * **DesignPattern**
        * [Design Pattern (디자인 패턴)](ComputerScience/DesignPattern/README.md)
        * [State Pattern (상태 패턴)](ComputerScience/DesignPattern/StatePattern.md)
    * **SoftwareEngineering**
        * [Behavior-Driven Development (BDD)](ComputerScience/SoftwareEngineering/BDD.md)
        * [소프트웨어 버저닝 (Software Versioning)](ComputerScience/SoftwareEngineering/Versioning.md)
    * **FileSystem**
        * [File System (파일 시스템)](ComputerScience/FileSystem/FileSystem.md)
        * [HDF5 (Hierarchical Data Format version 5)](ComputerScience/FileSystem/HDF5.md)
        * [LMDB (Lightning Memory-Mapped Database)](ComputerScience/FileSystem/LMDB (Sysmas Lightning Memory-mapped Database).md)
        * [대량의 이미지를 파일시스템에 저장할 때](ComputerScience/FileSystem/대량의 이미지를 파일시스템에 저장할 때.md)
    * **Architecture**
        * [Architecture (시스템 아키텍처)](ComputerScience/Architecture/README.md)
        * [고가용성 (High Availability, HA)](ComputerScience/Architecture/High_Availability.md)
        * [파이프라인 (Pipeline)](ComputerScience/Architecture/Pipeline.md)
    * **Network**
        * [Network (네트워크)](ComputerScience/Network/README.md)
        * [OSI 7 Layer (OSI 7 계층)](ComputerScience/Network/OSI 7 Layer.md)
        * [RPC (Remote Procedure Call)](ComputerScience/Network/RPC.md)
        * [Socket (소켓)](ComputerScience/Network/Socket.md)
        * [Subnetwork (서브넷)](ComputerScience/Network/Subnetwork.md)
        * **DNS**
            * [DNS와 NameServer: 개념 이해 및 리눅스 설정 가이드](ComputerScience/Network/DNS/DNS_and_NameServer.md)
    * **OperatingSystem**
        * [Endianness (엔디언)](ComputerScience/OperatingSystem/Endianness.md)

## 📁 Web

* [🌐 Web Technologies & Architecture](Web/README.md)
    * **Framework**
        * [Vuejs.md](Web/Framework/Vuejs.md)
    * **Concepts**
        * [Ajax 그리고 CSR, SSR.md](Web/Concepts/Ajax 그리고 CSR, SSR.md)
        * [OpenAPI vs Swagger: 개념 차이와 선택 가이드](Web/Concepts/OpenAPI_vs_Swagger.md)
        * [Scalar: 현대적이고 아름다운 API 문서화 도구 가이드](Web/Concepts/Scalar_UI.md)
        * [🌐 WebRTC (Web Real-Time Communication)](Web/Concepts/WebRTC.md)

## 📁 Tools

* [⚙️ Engineering & Build Tools](Tools/README.md)
    * **Build**
        * [Java 코드 포맷터 비교: google-java-format vs palantir-java-format](Tools/Build/Java_Code_Formatters_Comparison.md)
        * [Apache Maven: 자바 빌드 자동화 도구 가이드](Tools/Build/Maven.md)
        * [Maven Classifier와 Hive-JDBC Standalone 활용 가이드](Tools/Build/Maven_Classifier_and_Hive_JDBC.md)
        * [Maven Shade Plugin: Uber-JAR 생성 및 패키지 재배치](Tools/Build/Maven_Shade_Plugin.md)
        * [Spotless: 코드 스타일 자동화 도구](Tools/Build/Spotless.md)
    * **Github**
        * [GitHub Actions MkDocs 배포 실패 (Plugin Missing)](Tools/Github/Action_Deploy_Fail.md)
        * [GitHub 프로필 메인 페이지(Profile README) 꾸미기 가이드](Tools/Github/Profile_README_Guide.md)
    * **Git**
        * [Monorepo vs Polyrepo](Tools/Git/Monorepo_vs_Polyrepo.md)
        * [Git Remote Settings (원격 저장소 관리)](Tools/Git/Remote_Settings.md)
        * [Git Submodules (서브모듈)](Tools/Git/Submodules.md)
        * [Git Tag](Tools/Git/Tag.md)
        * [Git Tips](Tools/Git/Tips.md)
    * **OpenSource**
        * [FFmpeg](Tools/OpenSource/FFmpeg.md)
    * **Terminal**
        * [Terminal Tools](Tools/Terminal/README.md)
        * [Tmux (Terminal Multiplexer)](Tools/Terminal/Tmux.md)

## 📁 Templates

* [📋 문서 양식 (Templates)](Templates/README.md)
* [[양식] 기술 이슈 분석 및 리포트](Templates/Issue_Report_Template.md)
* [[양식] 신규 개발 정의 문서](Templates/New_Development_Definition_Template.md)

