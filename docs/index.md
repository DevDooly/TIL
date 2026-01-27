# TIL (Today I Learned)

TIL(Today I Learned) 기록이 쌓임에 따라 발생할 수 있는 분류의 모호함을 해결하고, 나중에 정보를 쉽게 찾을 수 있도록 저장소 구조를 재정의한다.

## 개요
기존의 파편화된 폴더 구조를 기술 스택과 도메인 중심으로 재편성하여 유지보수성을 높인다.

## 본문

### 1. 카테고리 분류 원칙
- **언어(Language)**: 특정 프로그래밍 언어 자체의 기능, 프레임워크, 라이브러리 (ex: Java, Python, Node.js)
- **웹(Web)**: 웹 개발 전반의 개념 및 프론트엔드/백엔드 기술 (ex: Web Concepts)
- **인프라(Infrastructure)**: 서버, 네트워크, 배포 및 운영 관련 기술 (ex: Linux, Docker, Network)
- **데이터(Data)**: 데이터 처리, 저장, 관리 및 빅데이터 기술 (ex: Database, FileSystem, Hadoop)
- **컴퓨터 과학(Computer Science)**: 전산학 기초 이론 및 아키텍처 (ex: OS, Design Pattern, Security, Architecture)
- **도구(Tools)**: 개발 생산성을 높이는 도구 및 서비스 (ex: Git, IDE, Markdown)
- **생활(Life)**: 커리어, 재테크, 마인드셋 등 개발 외적인 요소
- **아키텍처 쿡북(Architecture Cookbook)**: 외부 아키텍처 가이드 저장소 링크

### 2. 파일 명명 규칙 (Naming Convention)
- 공백 대신 언더바(`_`)나 하이픈(`-`)을 사용한다.
- 기술 명칭은 가급적 공식 명칭의 대소문자를 따른다.

### 3. 디렉토리 구조 예시

    .
    ├── Language/           # Java, Python, Node.js ...
    ├── Web/                # Web Concepts, Vue.js ...
    ├── Infrastructure/     # Linux, Docker, Message Broker ...
    ├── Data/               # Database, FileSystem ...
    ├── ComputerScience/    # OS, DesignPattern, Security, Architecture ...
    ├── Tools/              # Git, IDE ...
    └── Life/               # Career, RealEstate ...


## References
* [Google Technical Writing Style Guide](https://developers.google.com/style)
* [How to maintain a TIL repository](https://github.com/jbranchaud/til)

---

## 목차 (Table of Contents)

### 📂 1. Language (언어 및 프레임워크)
- [**Java**](#java)
- [**Python**](#python)
- [**Node.js**](#nodejs)

### 📂 2. Web (웹 개발)
- [**Web Concepts**](#web-concepts)

### 📂 3. Infrastructure (인프라 및 데브옵스)
- [**Linux**](#linux)
- [**Docker**](#docker)
- [**Network**](#network)
- [**Message Broker**](#message-broker)

### 📂 4. Data (데이터 엔지니어링)
- [**Database**](#database)
- [**FileSystem**](#filesystem)
- [**Hadoop**](#hadoop)

### 📂 5. Computer Science (CS 기초)
- [**Operating System**](#operating-system)
- [**Design Pattern**](#design-pattern)
- [**Security & Auth**](#security--auth)
- [**Architecture**](#architecture)

### 📂 6. Tools (개발 도구)
- [**Git**](#git)
- [**IDE**](#ide)
- [**Productivity**](#productivity)

### 📂 7. Life (생활 및 커리어)
- [**Career**](#career)
- [**Real Estate**](#real-estate)
- [**Mindset**](#mindset)

### 📂 8. Architecture Cookbook (External)
- [**GitHub Repository**](https://github.com/DevDooly/architecture-cookbook)

---

## Language

### Java
* [Google Java Style Guide](Language/Java/Google_Java_Style_Guide.md)
<!-- * [Spring](Language/Java/Spring.md) --> (File missing)

### Python
* [Python Overview](Language/Python.md)
* [Decorator](Language/Python/Study/Decorator.md)
* [Comprehension](Language/Python/Comprehension.md)
* [Asyncio](Language/Python/Lib/asyncio.md)
* [Celery](Language/Python/Celery.md)
* [PyQt5](Language/Python/PyQt5.md)
* [SQLAlchemy](Language/Python/SQLAlchemy.md)
* [Refactoring](Language/Python/Refactoring.md)
* [Keras](Language/Python/Library/Keras.md)
* [문제 해결: Python Reinstall 후 서버 장애](Language/Python/Troubleshooting/Python_Reinstall_Server_Failure.md)

### Node.js
* [Node.js Overview](Language/NodeJs.md)
* [libuv](Language/NodeJs/libuv.md)
* [Yarn Berry](Language/NodeJs/Yarn%20Berry.md)

---

## Web
### Web Concepts
* [Ajax 그리고 CSR, SSR](Web/Concepts/Ajax%20그리고%20CSR,%20SSR.md)
* [Shadow DOM](Web/Concepts/shadow%20DOM.md)
* [WebRTC](Web/Concepts/WebRTC.md)
* [Electron](Web/Framework/Electron.md)
* [Vue.js](Web/Framework/Vuejs.md)

---

## Infrastructure
### Linux
* [Linux Overview](Infrastructure/Linux/README.md)
* [Crontab](Infrastructure/Linux/crontab.md)
* [Logrotate](Infrastructure/Linux/Logrotate.md)
* [Stdin, stdout, stderr](Infrastructure/Linux/Stdin,%20stdout,%20stderr.md)
* [POSIX](Infrastructure/Linux/POSIX.md)
* [Mount OneDrive on Ubuntu](Infrastructure/Linux/Tips/Mount%20OneDrive%20on%20Ubuntu.md)

### Docker
* [Docker Overview](Infrastructure/Docker/README.md)
* [Dockerfile](Infrastructure/Docker/dockerfile.md)
* [Troubleshooting: No space left on device](Infrastructure/Docker/no%20space%20left%20on%20device.md)

<!-- ### Network (Directory missing)
* [Network Overview](Infrastructure/Network.md)
* [OSI 7 Layer](Infrastructure/Network/OSI%207%20Layer.md)
* [Socket](Infrastructure/Network/Socket.md)
* [RPC](Infrastructure/Network/RPC.md) -->

### Message Broker
* [RabbitMQ](Infrastructure/MessageBroker/RabbitMQ/README.md)
* [RabbitMQ 그리고 Kafka](Infrastructure/MessageBroker/RabbitMQ%20그리고%20Kafka.md)
* [AMQP](Infrastructure/MessageBroker/AMQP.md)

---

## Data
### Database
* [SQL Naming Convention](Data/Database/SQL_Naming_Convention.md)
* [Redis](Data/Database/Redis.md)
* [MongoDB](Data/Database/MongoDB.md)
* [이미지 저장 및 관리](Data/Database/Image_Storage_Management.md)
* [ELK Stack](Data/ELK.md)

### FileSystem
<!-- * [FileSystem](Data/FileSystem.md) --> (Moved to CS)
* [HDF5](ComputerScience/FileSystem/HDF5.md)

### Hadoop
<!-- * [Hadoop](Data/Hadoop.md) --> (Directory missing)

---

## Computer Science
### Operating System
<!-- * [OS Overview](ComputerScience/OperatingSystem.md) --> (File missing)
<!-- * [프로세스 제어 블록](ComputerScience/OperatingSystem/Process_Control_Block.md) --> (File missing)
* [Endianness](ComputerScience/OperatingSystem/Endianness.md)

### Design Pattern
* [State Pattern](ComputerScience/DesignPattern/StatePattern.md)

### Security & Auth
* [JWT](ComputerScience/Security/JWT.md)
* [OIDC](ComputerScience/Security/OIDC.md)
<!-- * [Bug Bounty](ComputerScience/Security/BugBounty.md) --> (File missing)

### Architecture
* [High Availability (고가용성)](ComputerScience/Architecture/High_Availability.md)
* [Pipeline](ComputerScience/Architecture/Pipeline.md)

---

## Tools
### Git
* [Git Tips](Tools/Git/Tips.md)
* [Tag](Tools/Git/Tag.md)
* [Pull Request vs Merge Request](Tools/Git/Pull%20Request%20vs%20Merge%20Request.md)

### IDE
* [Intellij](Tools/IDE/Intellij.md)

### Productivity
* [FFmpeg](Tools/OpenSource/FFmpeg.md)
* [Zapier](Tools/Productivity/zapier.md)
* [Markdown Languages](Tools/Markdown/Languages%20Supported%20by%20Github%20Flavored%20Markdown.md)
* [BDD](Tools/Methodology/BDD.md)

---

## Life
### Career
* [Reference Check](Life/Career/Reference%20Check.md)

<!-- ### Real Estate (Directory missing)
* [LTV, DTI, DSR](Life/RealEstate/LTV,%20DTI,%20DSR.md)
* [종부세](Life/RealEstate/종부세.md) -->

### Mindset
<!-- * [Mindset](Life/Mindset.md) --> (File missing)
