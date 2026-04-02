# TIL (Today I Learned)
> 배운 내용을 정리하는 저장소입니다.

---

## 🕒 최근 변경 사항 (Recent Changes)
<!-- RECENT_CHANGES_START -->
| 날짜 | 문서 | 설명 |
| :--- | :--- | :--- |
| 2026-04-02 17:14 | [index](docs/index.md) | feat: 전체 문서 목차 자동 생성 스크립트 추가 및 index.md 개편 |
| 2026-04-02 16:41 | [ThreadPoolTaskScheduler](docs/Language/Java/SpringBoot/ThreadPoolTaskScheduler.md) | docs: Spring ThreadPoolTaskScheduler 개념 및 설정 가이드 추... |
| 2026-04-01 16:38 | [IMDB vs IMDG](docs/Infrastructure/Hazelcast/IMDB_vs_IMDG.md) | docs: 인메모리 데이터베이스(IMDB) vs 인메모리 데이터 그리드(IMDG) 비교 가... |
| 2026-04-01 16:38 | [README](docs/Infrastructure/Hazelcast/README.md) | docs: 인메모리 데이터베이스(IMDB) vs 인메모리 데이터 그리드(IMDG) 비교 가... |
| 2026-04-01 16:37 | [README](docs/Infrastructure/Hazelcast/README.md) | docs: Hazelcast(IMDG) 섹션 신설 및 개요 문서 추가 |
| 2026-04-01 16:37 | [README](docs/Infrastructure/README.md) | docs: Hazelcast(IMDG) 섹션 신설 및 개요 문서 추가 |

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
- [**Tools**](#tools)
- [**Life**](#life)

---

## Language
* [**Overview**](docs/Language/README.md)
* **Java**
  * [**Overview**](docs/Language/Java/README.md)
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
    * [Spring Boot OAuth2 Implementation](docs/Language/Java/SpringBoot/OAuth2_Implementation.md)
    * [Spring Boot Introduction](docs/Language/Java/SpringBoot/SpringBoot_Intro.md)
    * [ThreadPoolTaskScheduler: Spring 작업 예약 및 스레드 풀 관리](docs/Language/Java/SpringBoot/ThreadPoolTaskScheduler.md)
    * **JPA**
      * [**Overview**](docs/Language/Java/SpringBoot/JPA/README.md)
      * [JPA Persistence Context (영속성 컨텍스트)](docs/Language/Java/SpringBoot/JPA/Persistence_Context.md)
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
  * [Yarn Berry (Yarn v2+)](docs/Language/NodeJs/Yarn%20Berry.md)
  * [Libuv](docs/Language/NodeJs/libuv.md)
* **Python**
  * [**Overview**](docs/Language/Python/README.md)
  * [client.py](docs/Language/Python/AIOHTTP%20vs%20Flask.md)
  * [Celery](docs/Language/Python/Celery.md)
  * [Comprehension](docs/Language/Python/Comprehension.md)
  * [Designing Modules in Python (모듈 설계)](docs/Language/Python/Designing%20Modules%20in%20Python.md)
  * [PyQt5](docs/Language/Python/PyQt5.md)
  * [Imports](docs/Language/Python/Refactoring.md)
  * [SQLAlchemy](docs/Language/Python/SQLAlchemy.md)
  * [Socket Programming](docs/Language/Python/Socket%20Programming.md)
  * [orjson](docs/Language/Python/orjson.md)
  * [Retry](docs/Language/Python/retry.md)
  * [Tokenizer](docs/Language/Python/tokenizer.md)
  * [MetaClass (메타클래스)](docs/Language/Python/%EB%A9%94%ED%83%80%ED%81%B4%EB%9E%98%EC%8A%A4.md)
  * [정적메소드 (@staticmethod, @classmethod)](docs/Language/Python/%EC%A0%95%EC%A0%81%EB%A9%94%EC%86%8C%EB%93%9C.md)
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
    * [RabbitMQ / Asynchronous consumer example](docs/Language/Python/pika/Asynchronous%20consumer%20example.md)
    * [BlockingConnection](docs/Language/Python/pika/BlockingConnection.md)
  * **sys**
    * [**Overview**](docs/Language/Python/sys/README.md)
    * [sys.setrecursionlimit(limit)](docs/Language/Python/sys/sys.setrecursionlimit.md)

## Web
* [**Overview**](docs/Web/README.md)
* **Concepts**
  * [Ajax 그리고 CSR, SSR](docs/Web/Concepts/Ajax%20%EA%B7%B8%EB%A6%AC%EA%B3%A0%20CSR%2C%20SSR.md)
  * [용어 #](docs/Web/Concepts/WebRTC.md)
  * [Using shadow DOM](docs/Web/Concepts/shadow%20DOM.md)
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
  * [Docker: No space left on device 해결 방법](docs/Infrastructure/Docker/no%20space%20left%20on%20device.md)
* **Hadoop**
  * [**Overview**](docs/Infrastructure/Hadoop/README.md)
  * [Hadoop NameNode High Availability (HA)](docs/Infrastructure/Hadoop/NameNode_HA.md)
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
  * [Single Quote vs Double Quote (Bash)](docs/Infrastructure/Linux/Single%20Quotation%20vs%20Double%20Quotation%20in%20bash.md)
  * [Stdin, Stdout, Stderr (표준 스트림)](docs/Infrastructure/Linux/Stdin%2C%20stdout%2C%20stderr.md)
  * [TL;DR (Too Long; Didn't Read)](docs/Infrastructure/Linux/TL%3BDR.md)
  * [Crontab (크론탭)](docs/Infrastructure/Linux/crontab.md)
  * **Tips**
    * [Mount OneDrive on Ubuntu](docs/Infrastructure/Linux/Tips/Mount%20OneDrive%20on%20Ubuntu.md)
* **MessageBroker**
  * [**Overview**](docs/Infrastructure/MessageBroker/README.md)
  * [AMQP (Advanced Message Queuing Protocol)](docs/Infrastructure/MessageBroker/AMQP.md)
  * [RabbitMQ vs Kafka](docs/Infrastructure/MessageBroker/RabbitMQ%20%EA%B7%B8%EB%A6%AC%EA%B3%A0%20Kafka.md)
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
    * [Editing RabbitMQ handle big message](docs/Infrastructure/MessageBroker/RabbitMQ/Editing%20RabbitMQ%20handle%20big%20message.md)
    * [설치](docs/Infrastructure/MessageBroker/RabbitMQ/%EC%84%A4%EC%B9%98.md)
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
* **Database**
  * [**Overview**](docs/Data/Database/README.md)
  * [이미지 저장 및 관리 전략](docs/Data/Database/Image_Storage_Management.md)
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
  * [LMDB (Lightning Memory-Mapped Database)](docs/ComputerScience/FileSystem/LMDB%20%28Sysmas%20Lightning%20Memory-mapped%20Database%29.md)
  * [대량의 이미지를 파일시스템에 저장할 때](docs/ComputerScience/FileSystem/%EB%8C%80%EB%9F%89%EC%9D%98%20%EC%9D%B4%EB%AF%B8%EC%A7%80%EB%A5%BC%20%ED%8C%8C%EC%9D%BC%EC%8B%9C%EC%8A%A4%ED%85%9C%EC%97%90%20%EC%A0%80%EC%9E%A5%ED%95%A0%20%EB%95%8C.md)
* **Math**
  * [**Overview**](docs/ComputerScience/Math/README.md)
  * [Fourier Transform (푸리에 변환)](docs/ComputerScience/Math/Fourier%20transform.md)
* **Network**
  * [**Overview**](docs/ComputerScience/Network/README.md)
  * [OSI 7 Layer (OSI 7 계층)](docs/ComputerScience/Network/OSI%207%20Layer.md)
  * [RPC (Remote Procedure Call)](docs/ComputerScience/Network/RPC.md)
  * [Socket (소켓)](docs/ComputerScience/Network/Socket.md)
  * [Subnetwork (서브넷)](docs/ComputerScience/Network/Subnetwork.md)
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
  * [Languages Supported by Github Flavored Markdown.md](docs/Tools/Markdown/Languages%20Supported%20by%20Github%20Flavored%20Markdown.md)
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

## Life
* [Development Trends](docs/Life/Trends.md)
* **Career**
  * [Reference Check(평판 조회)](docs/Life/Career/Reference%20Check.md)
* **Health**
  * [🦶 족저근막염 (Plantar Fasciitis) 가이드](docs/Life/Health/Plantar_Fasciitis.md)

## AI
* [**Overview**](docs/AI/README.md)
* [Gemini CLI](docs/AI/Gemini_CLI.md)
* [Ollama](docs/AI/Ollama.md)
* [🖥️ 현재 PC (Ubuntu) Ollama 설치 및 API 설정 가이드](docs/AI/Ollama_Local_Environment_Setup.md)
* [OpenClaw](docs/AI/OpenClaw.md)
* [OpenCode](docs/AI/OpenCode.md)
* [TurboQuant: 초거대 언어 모델(LLM) 최적화의 혁신](docs/AI/TurboQuant.md)
* [n8n (Nodemation)](docs/AI/n8n.md)

## History
* [**Overview**](docs/History/README.md)
* [🇹🇼 대만의 역사 (History of Taiwan)](docs/History/Taiwan.md)
* **Modern_Issues**
  * [미국-이란 갈등: 중동의 화약고 분석](docs/History/Modern_Issues/US_Iran_Conflict.md)

## RealEstate
* [**Overview**](docs/RealEstate/README.md)
* [📏 국민평형(전용 85㎡) 초과 시 달라지는 세금 및 규제](docs/RealEstate/Tax_85sqm_Rules.md)

## Templates
* [**Overview**](docs/Templates/README.md)
* [[양식] 기술 이슈 분석 및 리포트](docs/Templates/Issue_Report_Template.md)

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

<!-- TOC_END -->

