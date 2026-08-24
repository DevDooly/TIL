---
title: Computer Science & Systems Engineering
---

# 🏛️ Computer Science & Fundamental Systems

소프트웨어의 확장성과 안정성을 지탱하는 **분산 시스템 아키텍처, 네트워크 프로토콜, 보안(인증/인가), 파일 시스템 및 소프트웨어 공학 원리**를 다룹니다.

---

## 📚 주요 기술 분야 및 문서

### 1. Architecture & Design Pattern
* **[Architecture Overview](Architecture/README.md)**: 시스템 아키텍처 원칙
  * **[High Availability (고가용성)](Architecture/High_Availability.md)**: 무중단 서비스를 위한 이중화 및 장애 복구 전략
  * **[Pipeline Architecture](Architecture/Pipeline.md)**: 데이터 파이프라인 패턴
* **[Design Pattern](DesignPattern/README.md)**:
  * **[State Pattern (상태 패턴)](DesignPattern/StatePattern.md)**: 상태 전이 캡슐화 및 OCP 준수

### 2. Network & Security Architecture
* **[Network Overview](Network/README.md)**:
  * **[OSI 7 Layer](Network/OSI%207%20Layer.md)**: 계층별 프로토콜 역할 및 패킷 흐름
  * **[RPC (Remote Procedure Call)](Network/RPC.md)**: gRPC / 분산 RPC 통신 메커니즘
  * **[Socket Communication](Network/Socket.md)**: 저수준 네트워크 소켓 통신 및 버퍼링
  * **[DNS and NameServer](Network/DNS/DNS_and_NameServer.md)**: 도메인 네임 해석 과정과 캐싱
  * **[Subnetwork & CIDR](Network/Subnetwork.md)**: 서브넷 마스킹 및 IP 라우팅
* **[Security Overview](Security/README.md)**:
  * **[JWT (JSON Web Token)](Security/JWT.md)**: 서명 구조, 검증 플로우 및 보안 취약점 대책
  * **[OAuth 2.0 Framework](Security/OAuth2.md)**: 인가 코드 그랜트(Authorization Code Grant) 플로우
  * **[OIDC (OpenID Connect)](Security/OIDC.md)**: OAuth2 기반의 신원 인증 표준 레이어

### 3. File System & Storage Mechanics
* **[File System Overview](FileSystem/FileSystem.md)**: 파일 시스템 레이아웃 및 블록 관리
* **[HDF5 (Hierarchical Data Format 5)](FileSystem/HDF5.md)**: 대용량 다차원 과학 데이터 저장 포맷
* **[LMDB (Lightning Memory-Mapped Database)](FileSystem/LMDB%20(Sysmas%20Lightning%20Memory-mapped%20Database).md)**: B+Tree 기반 초고속 mmap 임베디드 키-값 저장소
* **[대량의 이미지를 파일시스템에 저장할 때](FileSystem/대량의%20이미지를%20파일시스템에%20저장할%20때.md)**: 디렉토리 인덱스 병목 극복을 위한 샤딩 기법

### 4. Software Engineering & OS
* **[BDD (Behavior-Driven Development)](SoftwareEngineering/BDD.md)**: 사용자 행동 중심의 테스트 주도 개발 방법론
* **[Software Versioning Strategy](SoftwareEngineering/Versioning.md)**: Semantic Versioning(SemVer) 원칙
* **[Endianness (엔디안)](OperatingSystem/Endianness.md)**: Big-Endian vs Little-Endian 바이트 오더링
