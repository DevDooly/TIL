# 👨‍💻 Dooly | Backend & Systems Engineering Portfolio & Tech Wiki

> **대용량 분산 시스템, 고성능 동시성 제어 및 클라우드 네이티브 아키텍처를 다루는 엔지니어링 포트폴리오 & 기술 위키입니다.**

🌐 **Live Portfolio & Wiki**: [https://devdooly.github.io/TIL/](https://devdooly.github.io/TIL/)

![Build Status](https://github.com/DevDooly/TIL/actions/workflows/ci.yml/badge.svg)
![Last Commit](https://img.shields.io/github/last-commit/DevDooly/TIL)
![License](https://img.shields.io/github/license/DevDooly/TIL)

---

## 🛠 Tech Stack Overview

### Core Backend & Concurrency
![Java](https://img.shields.io/badge/Java_21+-ED8B00?style=flat-square&logo=openjdk&logoColor=white)
![Spring Boot](https://img.shields.io/badge/Spring_Boot_3.x-6DB33F?style=flat-square&logo=springboot&logoColor=white)
![Python](https://img.shields.io/badge/Python_3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=nodedotjs&logoColor=white)

### Distributed Messaging & Storage
![Apache Kafka](https://img.shields.io/badge/Apache_Kafka-231F20?style=flat-square&logo=apachekafka&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-FF6600?style=flat-square&logo=rabbitmq&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white)
![MinIO](https://img.shields.io/badge/MinIO-C72C48?style=flat-square&logo=minio&logoColor=white)
![Oracle](https://img.shields.io/badge/Oracle_DB-F80000?style=flat-square&logo=oracle&logoColor=white)
![Apache Arrow](https://img.shields.io/badge/Apache_Arrow-E10079?style=flat-square&logo=apachearrow&logoColor=white)

### Cloud Native & DevOps
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![ArgoCD](https://img.shields.io/badge/ArgoCD-EF7B4D?style=flat-square&logo=argo&logoColor=white)
![Jenkins](https://img.shields.io/badge/Jenkins-D24939?style=flat-square&logo=jenkins&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black)

---

## 🎯 Key Highlights & Architecture Showcase

* 📄 **[온라인 이력서 (Resume)](docs/Resume.md)**: 경력 요약, 프로젝트 수행 이력 및 핵심 역량 맵
* 🛠️ **[실전 트러블슈팅 아카이브 (Troubleshooting)](docs/Troubleshooting/README.md)**: 
  * Java 21 가상 스레드(Virtual Threads) Pinning 이슈 해결 (FTP, JDBI, Kafka)
  * Apache Kafka Partitioner 쏠림 버그 및 셧다운 훅 안정화
  * Java-Python 간 Apache Arrow mmap 기반 Zero-Copy 데이터 공유
  * MinIO 버저닝 삭제 지연 및 스토리지 누수 해결
* 🧠 **[AI 개발 환경 & 에이전트 오케스트레이션](docs/AI/README.md)**:
  * Antigravity CLI(agy) 스킬 확장 및 자동화
  * Multi-Agent Orchestrator(Orca, Paseo) 아키텍처 비교

---

## 🕒 최근 변경 사항 (Recent Changes)

<!-- RECENT_CHANGES_START -->
| 날짜 | 문서 | 설명 |
| :--- | :--- | :--- |
| 2026-08-24 19:58 | [Architecture Cookbook](docs/Architecture_Cookbook.md) | feat: 위키를 개인 포트폴리오 및 이력서 홈페이지로 전면 개편 |
| 2026-08-24 19:58 | [Fourier transform](docs/ComputerScience/Math/Fourier transform.md) | feat: 위키를 개인 포트폴리오 및 이력서 홈페이지로 전면 개편 |
| 2026-08-24 19:58 | [Redis](docs/Data/Database/Redis.md) | feat: 위키를 개인 포트폴리오 및 이력서 홈페이지로 전면 개편 |
| 2026-08-24 19:58 | [US Iran Conflict](docs/History/Modern_Issues/US_Iran_Conflict.md) | feat: 위키를 개인 포트폴리오 및 이력서 홈페이지로 전면 개편 |
| 2026-08-24 19:58 | [Taiwan](docs/History/Taiwan.md) | feat: 위키를 개인 포트폴리오 및 이력서 홈페이지로 전면 개편 |
| 2026-08-24 19:58 | [Single Quotation vs Double Quotation in bash](docs/Infrastructure/Linux/Single Quotation vs Double Quotation in bash.md) | feat: 위키를 개인 포트폴리오 및 이력서 홈페이지로 전면 개편 |

<!-- RECENT_CHANGES_END -->

[👉 전체 변경 로그 보기](docs/Recent_Changes.md)

---

## 📂 카테고리별 목차 (Table of Contents)

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
  * [Apache Arrow BufferAllocator 관리 및 멀티스레드 활용 가이드](docs/Language/Java/Apache_Arrow_BufferAllocator_Management.md)
  * [Apache Arrow를 이용한 Java-Python 고성능 데이터 공유 가이드](docs/Language/Java/Apache_Arrow_Memory_Mapped_File.md)
  * [Apache Arrow & mmap을 이용한 Zero-copy 데이터 공유](docs/Language/Java/Apache_Arrow_with_mmap.md)
  * [Caffeine Cache: 고성능 Java 로컬 캐시 가이드](docs/Language/Java/Caffeine_Cache.md)
  * [Java/Spring Boot: 현재 스레드가 가상 스레드인지 확인하는 방법](docs/Language/Java/Check_Virtual_Thread.md)
  * [Java: Collections.emptyList() vs List.of() 비교](docs/Language/Java/Collections.emptyList_vs_List.of.md)
  * [Java: Concatenated GZIP 스트림 압축 해제 (Unzip)](docs/Language/Java/Concatenated_Gzip_Decompression.md)
  * [Java Effectively Final](docs/Language/Java/Effectively_Final.md)
  * [Java Garbage Collection (GC)](docs/Language/Java/Garbage_Collection.md)
  * [Google Java Style Guide](docs/Language/Java/Google_Java_Style_Guide.md)
  * [Java와 Python의 대용량 데이터 교환: Apache Arrow & mmap](docs/Language/Java/Java_Python_Shared_Memory_Arrow.md)
  * [Java Memory Structure (JVM Runtime Data Areas)](docs/Language/Java/Memory.md)
  * [Java-Python 실행 성능 최적화 가이드](docs/Language/Java/Optimizing_Java_Python_Execution.md)
  * [Java: Scoped Value - 가상 스레드 시대를 위한 새로운 데이터 공유 메커니즘](docs/Language/Java/Scoped_Value.md)
  * [Java/Spring Boot와 Python 연동 가이드](docs/Language/Java/Spring_Python_Integration.md)
  * [Java ThreadPoolExecutor와 거부 정책(Rejection Policy)](docs/Language/Java/ThreadPoolExecutor.md)
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
    * [Spring Boot: @EnableAutoConfiguration vs @ConfigurationPropertiesScan 비교](docs/Language/Java/SpringBoot/EnableAutoConfiguration_vs_ConfigurationPropertiesScan.md)
    * [Netty 환경에서 Blocking 코드/라이브러리를 찾는 방법](docs/Language/Java/SpringBoot/Finding_Blocking_Operations.md)
    * [JDBI & 가상 스레드: Pinning 이슈 해결을 위한 하이브리드 모델](docs/Language/Java/SpringBoot/JDBI_VT_Pinning_Solution.md)
    * [Logback: LoggingEventCompositeJsonEncoder와 springProperty 활용 가이드](docs/Language/Java/SpringBoot/Logback_JSON_Composite_Encoder.md)
    * [Spring Boot: 로깅 설정 YAML에서 XML로의 전환 (SDK 충돌 해결)](docs/Language/Java/SpringBoot/Logging_Config_Migration_YAML_to_XML.md)
    * [Spring Boot: SLF4J addKeyValue를 ECS 로그에 포함하기 (대안 가이드)](docs/Language/Java/SpringBoot/Logging_ECS_KeyValue_Support.md)
    * [Logback XML: logback-ecs-encoder를 이용한 정형 로깅 (ECS)](docs/Language/Java/SpringBoot/Logging_ECS_XML_Encoder.md)
    * [Logstash Logback Encoder 사용 가이드](docs/Language/Java/SpringBoot/Logstash_Logback_Encoder_Guide.md)
    * [Netflix Ribbon: 클라이언트 측 부하 분산(Load Balancing) 가이드](docs/Language/Java/SpringBoot/Netflix_Ribbon_Guide.md)
    * [Spring Boot OAuth2 Implementation](docs/Language/Java/SpringBoot/OAuth2_Implementation.md)
    * [Spring Cloud Gateway vs Netflix Zuul: 아키텍처 비교 및 선택 가이드](docs/Language/Java/SpringBoot/SCG_vs_Zuul_Comparison.md)
    * [Spring Boot Introduction](docs/Language/Java/SpringBoot/SpringBoot_Intro.md)
    * [Spring Cloud Gateway (SCG): 차세대 API Gateway 가이드](docs/Language/Java/SpringBoot/Spring_Cloud_Gateway.md)
    * [Spring Cloud LoadBalancer: 현대적인 클라이언트 측 부하 분산 가이드](docs/Language/Java/SpringBoot/Spring_Cloud_LoadBalancer.md)
    * [Spring Cloud Zuul: API Gateway 및 동적 라우팅 가이드](docs/Language/Java/SpringBoot/Spring_Cloud_Zuul.md)
    * [Spring Data JPA: CrudRepository 가이드](docs/Language/Java/SpringBoot/Spring_Data_JPA_CrudRepository.md)
    * [비교: 직접 쿼리 작성(JDBI/JDBC) vs Spring Data JPA (CrudRepository)](docs/Language/Java/SpringBoot/Spring_Data_JPA_vs_JDBI.md)
    * [K8s 환경에서의 Spring 프로파일 및 설정 우선순위 이슈](docs/Language/Java/SpringBoot/Spring_Profile_Priority_in_K8s.md)
    * [Spring Boot 3.4: 정형 로깅(Structured Logging) 및 ECS 연동](docs/Language/Java/SpringBoot/Structured_Logging_SpringBoot_3_4.md)
    * [ThreadPoolTaskScheduler: Spring 작업 예약 및 스레드 풀 관리](docs/Language/Java/SpringBoot/ThreadPoolTaskScheduler.md)
    * [Spring Boot: Tomcat vs Netty 비교 가이드](docs/Language/Java/SpringBoot/Tomcat_vs_Netty.md)
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
    * [Java 25: Enhanced Stability and Modern Productivity](docs/Language/Java/Versions/Java25.md)
    * [Java 8: Modern Java의 시작](docs/Language/Java/Versions/Java8.md)
* **NodeJs**
  * [**Overview**](docs/Language/NodeJs/README.md)
  * [Yarn Berry (Yarn v2+)](docs/Language/NodeJs/Yarn Berry.md)
  * [⚡ Libuv & Node.js 비동기 I/O 아키텍처](docs/Language/NodeJs/libuv.md)
* **Python**
  * [**Overview**](docs/Language/Python/README.md)
  * [client.py](docs/Language/Python/AIOHTTP vs Flask.md)
  * [Stream](docs/Language/Python/Asyncio_Streams.md)
  * [Python 스크립트 실행 가이드: `python3 main.py`](docs/Language/Python/Basic_Execution_Guide.md)
  * [Celery](docs/Language/Python/Celery.md)
  * [Comprehension](docs/Language/Python/Comprehension.md)
  * [Anaconda vs Miniconda: 차이점과 환경 구축 가이드](docs/Language/Python/Conda_Anaconda_Miniconda.md)
  * [🐍 Python Decorator (데코레이터)](docs/Language/Python/Decorator.md)
  * [Designing Modules in Python (모듈 설계)](docs/Language/Python/Designing Modules in Python.md)
  * [FastAPI의 동시성(Concurrency) 처리 메커니즘](docs/Language/Python/FastAPI_Concurrency_Mechanism.md)
  * [Gunicorn vs Uvicorn: 개념과 운영 환경 구축 전략](docs/Language/Python/Gunicorn_vs_Uvicorn.md)
  * [폐쇄망 환경 Python 3.12 설치 가이드 (최신 안정 버전)](docs/Language/Python/Offline_Installation_Guide.md)
  * [오프라인 환경에서 `venv` 및 `pip` 패키지 설치 가이드](docs/Language/Python/Offline_Venv_Pip_Guide.md)
  * [Imports](docs/Language/Python/Refactoring.md)
  * [SQLAlchemy](docs/Language/Python/SQLAlchemy.md)
  * [Python Web Server 실행 방식 비교: `python main.py` vs CLI Runner](docs/Language/Python/Server_Execution_Methods.md)
  * [Socket Programming](docs/Language/Python/Socket Programming.md)
  * [socketserver](docs/Language/Python/SocketServer.md)
  * [orjson](docs/Language/Python/orjson.md)
  * [Retry](docs/Language/Python/retry.md)
  * [Tokenizer](docs/Language/Python/tokenizer.md)
  * [venv vs Conda: 어떤 가상환경을 선택해야 할까?](docs/Language/Python/venv_vs_Conda.md)
  * [MetaClass (메타클래스)](docs/Language/Python/메타클래스.md)
  * [정적메소드 (@staticmethod, @classmethod)](docs/Language/Python/정적메소드.md)
  * **Troubleshooting**
    * [Python Reinstall Server Failure](docs/Language/Python/Troubleshooting/Python_Reinstall_Server_Failure.md)
  * **pika**
    * [**Overview**](docs/Language/Python/pika/README.md)
    * [RabbitMQ / Asynchronous consumer example](docs/Language/Python/pika/Asynchronous consumer example.md)
    * [BlockingConnection](docs/Language/Python/pika/BlockingConnection.md)

## Web
* [**Overview**](docs/Web/README.md)
* **Concepts**
  * [Ajax 그리고 CSR, SSR](docs/Web/Concepts/Ajax 그리고 CSR, SSR.md)
  * [OpenAPI vs Swagger: 개념 차이와 선택 가이드](docs/Web/Concepts/OpenAPI_vs_Swagger.md)
  * [Scalar: 현대적이고 아름다운 API 문서화 도구 가이드](docs/Web/Concepts/Scalar_UI.md)
  * [🌐 WebRTC (Web Real-Time Communication)](docs/Web/Concepts/WebRTC.md)
* **Framework**
  * [Vuejs](docs/Web/Framework/Vuejs.md)

## Infrastructure
* [**Overview**](docs/Infrastructure/README.md)
* **ArgoCD**
  * [**Overview**](docs/Infrastructure/ArgoCD/README.md)
  * [ArgoCD 실전 사용 예시 (App of Apps, Kustomize, ApplicationSet)](docs/Infrastructure/ArgoCD/Examples.md)
  * [ArgoCD 설치 가이드](docs/Infrastructure/ArgoCD/Installation.md)
  * [ArgoCD 사용 방법 및 운영 가이드](docs/Infrastructure/ArgoCD/Usage.md)
* **Docker**
  * [**Overview**](docs/Infrastructure/Docker/README.md)
  * [Docker 이미지 버전 관리(Versioning) 전략](docs/Infrastructure/Docker/docker_image_versioning_strategy.md)
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
  * [Jenkins 실전 사용 예시 (Pipeline)](docs/Infrastructure/Jenkins/Examples.md)
  * [Jenkins 설치 가이드](docs/Infrastructure/Jenkins/Installation_Docker_Linux.md)
  * [Jenkins 설치 가이드 (Kubernetes)](docs/Infrastructure/Jenkins/Installation_K8s.md)
  * [Jenkins 사용 방법 및 실무 설정 가이드](docs/Infrastructure/Jenkins/Usage.md)
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
  * [Stdin, Stdout, Stderr (표준 스트림)](docs/Infrastructure/Linux/Stdin, stdout, stderr.md)
  * [TL;DR (Too Long; Didn't Read)](docs/Infrastructure/Linux/TL;DR.md)
  * [Crontab (크론탭)](docs/Infrastructure/Linux/crontab.md)
* **MessageBroker**
  * [**Overview**](docs/Infrastructure/MessageBroker/README.md)
  * [AMQP (Advanced Message Queuing Protocol)](docs/Infrastructure/MessageBroker/AMQP.md)
  * [NATS (Neural Autonomic Transport System)](docs/Infrastructure/MessageBroker/NATS.md)
  * [RabbitMQ vs Kafka](docs/Infrastructure/MessageBroker/RabbitMQ 그리고 Kafka.md)
  * **Kafka**
    * [**Overview**](docs/Infrastructure/MessageBroker/Kafka/README.md)
    * [Kafka: abortOnNewBatch 매커니즘과 파티션 쏠림 이슈](docs/Infrastructure/MessageBroker/Kafka/AbortOnNewBatch_Issue.md)
    * [Kafka Consumer: 특정 Offset 재소비 (Seek API)](docs/Infrastructure/MessageBroker/Kafka/Consumer_Offset_Control.md)
    * [Kafka: Consumer의 안전한 종료 (wakeup vs close)](docs/Infrastructure/MessageBroker/Kafka/Consumer_Safe_Shutdown.md)
    * [Kafka 메시지 최대 사이즈 확장 가이드 (Broker 재기동 없이)](docs/Infrastructure/MessageBroker/Kafka/Kafka_Message_Size_Configuration.md)
    * [Kafka Broker 롤링 재시작 가이드 (3대 HA 구성)](docs/Infrastructure/MessageBroker/Kafka/Kafka_Rolling_Restart_Guide.md)
    * [Kafka 파티션 전략: 개수 산정과 증가 시 고려사항](docs/Infrastructure/MessageBroker/Kafka/Partition_Strategy.md)
    * [Kafka 파티셔너의 진화와 불균형(Imbalance) 문제 해결](docs/Infrastructure/MessageBroker/Kafka/Partitioner_Evolution_and_Imbalance.md)
    * [Kafka Producer: RoundRobinPartitioner 이슈 (KAFKA-9965)](docs/Infrastructure/MessageBroker/Kafka/Producer_Partitioner_Issue.md)
    * [Kafka Producer: 파티셔너(Partitioner) 정책 및 설정](docs/Infrastructure/MessageBroker/Kafka/Producer_Partitioner_Policy.md)
    * [Spring Kafka: 테스트 코드에서 단일 메시지 소비](docs/Infrastructure/MessageBroker/Kafka/Spring_Kafka_Test.md)
* **MinIO**
  * [**Overview**](docs/Infrastructure/MinIO/README.md)
  * [MinIO Java Client 사용 예제](docs/Infrastructure/MinIO/Java_Client_Examples.md)
  * [MinIO 수명 주기 관리 (Lifecycle / ILM)](docs/Infrastructure/MinIO/Lifecycle.md)
  * [MinIO Client (mc) 설치 및 사용 가이드](docs/Infrastructure/MinIO/MinIO_Client_mc.md)
  * [MinIO 버저닝 (Versioning)](docs/Infrastructure/MinIO/Versioning.md)
* **OracleCloud**
  * [**Overview**](docs/Infrastructure/OracleCloud/README.md)
  * [HAProxy를 통한 Oracle DB 접속 지연 진단 가이드](docs/Infrastructure/OracleCloud/HAProxy_Oracle_Latency_Diagnosis.md)

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
  * [⚡ Redis (Remote Dictionary Server)](docs/Data/Database/Redis.md)
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
  * [**분석 문서 보기**](docs/Language/Java/Virtual_Threads_FTP_Pinning.md)
  * [**분석 문서 보기**](docs/Language/Java/Virtual_Threads_in_K8s.md)
  * [**분석 문서 보기**](docs/Language/Java/SpringBoot/Virtual_Thread_Pinning_Kafka.md)
  * [**분석 문서 보기**](docs/Language/Java/SpringBoot/JDBI_VT_Pinning_Solution.md)
  * [**분석 문서 보기**](docs/Language/Java/SpringBoot/Spring_Profile_Priority_in_K8s.md)
  * [**분석 문서 보기**](docs/Language/Java/SpringBoot/Logging_Config_Migration_YAML_to_XML.md)
  * [**분석 문서 보기**](docs/Language/Java/SpringBoot/Logging_ECS_KeyValue_Support.md)
  * [**분석 문서 보기**](docs/Infrastructure/MessageBroker/Kafka/Producer_Partitioner_Issue.md)
  * [**분석 문서 보기**](docs/Infrastructure/MessageBroker/Kafka/Partitioner_Evolution_and_Imbalance.md)
  * [**분석 문서 보기**](docs/Infrastructure/MessageBroker/Kafka/AbortOnNewBatch_Issue.md)
  * [**분석 문서 보기**](docs/Infrastructure/MessageBroker/Kafka/Consumer_Safe_Shutdown.md)
  * [**분석 문서 보기**](docs/Infrastructure/Hadoop/Tez_Job_Slowness_Network_RX.md)
  * [**분석 문서 보기**](docs/Infrastructure/Linux/Large_File_Transfer.md)
  * [**분석 문서 보기**](docs/Troubleshooting/MinIO_Versioning_Deletion_Issue.md)
  * [**분석 문서 보기**](docs/Data/Database/Oracle_LOB_Segment.md)
  * [**분석 문서 보기**](docs/Troubleshooting/Avro_HashCode_Field_Naming_Conflict.md)

## AI
* [**Overview**](docs/AI/README.md)
* [Antigravity CLI (agy) vs OpenCode (with Gemini) 비교 가이드](docs/AI/AGY_vs_OpenCode_Comparison.md)
* [AI 코딩 에이전트 오케스트레이터: Orca vs Paseo](docs/AI/AI_Coding_Agent_Orchestrators_Orca_Paseo.md)
* [Antigravity CLI - 자동 승인(Auto-Approve) 및 권한 설정 가이드](docs/AI/Antigravity_CLI_Configuration.md)
* [Antigravity CLI (`agy`) 스킬 설치, 설정 및 활용 가이드](docs/AI/Antigravity_CLI_Skills_Guide.md)
* [Claude CLI - 다중 모델(Multi-Model) 및 DeepSeek 연동 가이드 (Windows)](docs/AI/Claude_CLI_DeepSeek_Setup.md)
* [Gemini CLI](docs/AI/Gemini_CLI.md)
* [Ollama](docs/AI/Ollama.md)
* [🖥️ 현재 PC (Ubuntu) Ollama 설치 및 API 설정 가이드](docs/AI/Ollama_Local_Environment_Setup.md)
* [OpenClaw](docs/AI/OpenClaw.md)
* [OpenCode](docs/AI/OpenCode.md)
* [Paseo 설치 및 모바일 원격 제어 설정 가이드](docs/AI/Paseo_Setup_and_Usage.md)
* [Qwen CLI - API Key 재등록 및 설정 가이드](docs/AI/Qwen_CLI_Setup.md)
* [TurboQuant: 초거대 언어 모델(LLM) 최적화의 혁신](docs/AI/TurboQuant.md)
* [n8n (Nodemation)](docs/AI/n8n.md)

## Tools
* [**Overview**](docs/Tools/README.md)
* **Build**
  * [Java 코드 포맷터 비교: google-java-format vs palantir-java-format](docs/Tools/Build/Java_Code_Formatters_Comparison.md)
  * [Apache Maven: 자바 빌드 자동화 도구 가이드](docs/Tools/Build/Maven.md)
  * [Maven Classifier와 Hive-JDBC Standalone 활용 가이드](docs/Tools/Build/Maven_Classifier_and_Hive_JDBC.md)
  * [Maven Shade Plugin: Uber-JAR 생성 및 패키지 재배치](docs/Tools/Build/Maven_Shade_Plugin.md)
  * [Spotless: 코드 스타일 자동화 도구](docs/Tools/Build/Spotless.md)
* **Git**
  * [Monorepo vs Polyrepo](docs/Tools/Git/Monorepo_vs_Polyrepo.md)
  * [Git Remote Settings (원격 저장소 관리)](docs/Tools/Git/Remote_Settings.md)
  * [Git Submodules (서브모듈)](docs/Tools/Git/Submodules.md)
  * [Git Tag](docs/Tools/Git/Tag.md)
  * [Git Tips](docs/Tools/Git/Tips.md)
* **Github**
  * [GitHub Actions MkDocs 배포 실패 (Plugin Missing)](docs/Tools/Github/Action_Deploy_Fail.md)
  * [GitHub 프로필 메인 페이지(Profile README) 꾸미기 가이드](docs/Tools/Github/Profile_README_Guide.md)
* **OpenSource**
  * [FFmpeg](docs/Tools/OpenSource/FFmpeg.md)
* **Terminal**
  * [**Overview**](docs/Tools/Terminal/README.md)
  * [Tmux (Terminal Multiplexer)](docs/Tools/Terminal/Tmux.md)

## Templates
* [**Overview**](docs/Templates/README.md)
* [[양식] 기술 이슈 분석 및 리포트](docs/Templates/Issue_Report_Template.md)
* [[양식] 신규 개발 정의 문서](docs/Templates/New_Development_Definition_Template.md)

## LLM_Development
* [**Overview**](docs/LLM_Development/README.md)
* [Backend Development with LLM (백엔드 개발 시 LLM 활용 가이드)](docs/LLM_Development/Backend_Development_Checklist.md)
* [Web Development with LLM (웹 개발 시 LLM 활용 가이드)](docs/LLM_Development/Web_Development_Checklist.md)

<!-- TOC_END -->

---

## ⚙️ 관리 및 자동화 스크립트

* `python3 scripts/update_recent_changes.py`: Git 커밋 로그를 기반으로 최근 변경 사항(`docs/Recent_Changes.md`) 및 README 자동 동기화
* `python3 scripts/generate_sitemap.py`: 전체 문서 계층 구조를 반영한 `docs/Sitemap.md` 자동 생성
* `python3 scripts/validate_pages.py`: 모든 `.pages` 파일의 경로 유효성 자동 검증