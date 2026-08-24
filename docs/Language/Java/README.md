---
title: Java & Spring Engineering
---

# ☕ Java & JVM Ecosystem

엔터프라이즈 환경의 대규모 트래픽 처리와 안정적인 서비스 운영을 위한 **Java, JVM 내부 메커니즘, 가상 스레드(Virtual Threads), Spring Boot 및 고성능 메모리 공유 기법**을 다룹니다.

---

## 📚 주요 기술 문서 목차

### 1. JVM Internals & Memory Management
* **[Java Memory Structure](Memory.md)**: JVM Runtime Data Areas (Stack, Heap, Metaspace, Direct Memory) 심층 분석
* **[Garbage Collection (GC)](Garbage_Collection.md)**: Generational GC 원리, ZGC/G1GC 튜닝 및 GC 동작 메커니즘
* **[ThreadPoolExecutor & Rejection Policy](ThreadPoolExecutor.md)**: 스레드 풀 생성 전략 및 과부하 시 작업 거부 정책

### 2. Modern Java & Concurrency (Java 21+)
* **[Java Virtual Threads: FTP Pinning 이슈](Virtual_Threads_FTP_Pinning.md)**: `synchronized` 블록으로 인한 OS 캐리어 스레드 고갈 원인 및 락 리팩토링
* **[K8s 환경 Virtual Threads 분석](Virtual_Threads_in_K8s.md)**: 컨테이너 CPU 쿼터와 ForkJoinPool 병렬성 충돌 해결
* **[Check Virtual Thread](Check_Virtual_Thread.md)**: 런타임에 현재 스레드가 가상 스레드인지 확인하는 방법
* **[Scoped Value](Scoped_Value.md)**: ThreadLocal의 한계를 극복하는 가상 스레드 시대의 불변 데이터 공유 메커니즘

### 3. High-Performance & Data Exchange
* **[Apache Arrow & mmap을 이용한 Zero-Copy 데이터 공유](Apache_Arrow_with_mmap.md)**: IPC 오버헤드 없는 프로세스 간 고속 데이터 전달
* **[Java-Python Shared Memory with Arrow](Java_Python_Shared_Memory_Arrow.md)**: Java 백엔드와 Python ML/분석 프로세스 간 대용량 데이터 연동
* **[Apache Arrow Memory Mapped File 가이드](Apache_Arrow_Memory_Mapped_File.md)**: 실전 코드 예제 및 메모리 해제 라이프사이클
* **[Apache Arrow BufferAllocator 관리](Apache_Arrow_BufferAllocator_Management.md)**: 멀티스레드 환경에서의 Direct Buffer 메모리 누수 방지
* **[Concatenated GZIP 스트림 압축 해제](Concatenated_Gzip_Decompression.md)**: 다중 블록 연결 GZIP 스트림 고속 언패킹 기법
* **[Caffeine Cache](Caffeine_Cache.md)**: W-TinyLFU 알고리즘 기반 초고성능 로컬 캐시 활용법

### 4. Spring Boot Framework
* **[Spring Boot 종합 가이드](SpringBoot/README.md)**: Spring Boot 핵심 개념 및 아키텍처
* **[Spring Web (MVC vs WebFlux)](SpringBoot/Web/README.md)**: 서블릿 컨테이너 기반 동기 모델과 Reactive 이벤트 루프 모델 비교
* **[Spring Boot 3.4 Structured Logging](SpringBoot/Structured_Logging_SpringBoot_3_4.md)**: ECS 포맷 JSON 정형 로깅 및 관찰 가능성(Observability)
* **[JDBI Virtual Thread Pinning Solution](SpringBoot/JDBI_VT_Pinning_Solution.md)**: DB 블로킹 I/O 구간 전용 하이브리드 스레드 풀 설계
* **[Spring Data JPA vs JDBI](SpringBoot/Spring_Data_JPA_vs_JDBI.md)**: ORM 생산성과 SQL 직관성/성능 간의 트레이드오프 분석

### 5. Functional & Language Core
* **[Java Functional Programming](Functional/README.md)**: Lambda, Stream API, Optional, 표준 함수형 인터페이스
* **[Effectively Final](Effectively_Final.md)**: 람다/익명 클래스 내 변수 캡처링 제약과 원리
* **[Collections.emptyList() vs List.of()](Collections.emptyList_vs_List.of.md)**: 불변 컬렉션 인스턴스 생성 시 메모리 및 불변성 차이
* **[Google Java Style Guide](Google_Java_Style_Guide.md)**: 사내 표준 코드 품질 유지를 위한 구글 자바 스타일 가이드

### 6. Java Version Release Notes
* **[Java Versions Overview](Versions/README.md)**: Java 8부터 최신 LTS(Java 11, 17, 21, 25)까지의 주요 변경점
