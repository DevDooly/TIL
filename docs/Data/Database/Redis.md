# Redis (Remote Dictionary Server)

**Redis**는 고성능 키-값(Key-Value) 구조의 비관계형(NoSQL) 데이터를 관리하기 위한 오픈 소스 **인메모리(In-Memory) 데이터 구조 저장소**입니다.

## 1. 주요 특징

*   **인메모리 (In-Memory):** 모든 데이터를 RAM에 저장하여 초당 수십만 건의 읽기/쓰기 성능을 제공합니다.
*   **다양한 데이터 구조 지원:** 단순 String뿐만 아니라 List, Set, Sorted Set, Hashes, Bitmaps, HyperLogLogs 등 다양한 데이터 타입을 지원합니다.
*   **영속성 (Persistence):** 메모리 기반이지만 데이터를 디스크에 저장(RDB, AOF)하여 서버 재시작 시 복구할 수 있는 기능을 제공합니다.
*   **싱글 스레드 (Single-Threaded):** 명령어 처리는 싱글 스레드로 수행되어 Race Condition(경합 상태)을 방지하며 원자성(Atomicity)을 보장합니다.

## 2. 주요 사용 사례

*   **캐싱 (Caching):** DB 부하를 줄이기 위해 자주 조회되는 데이터를 저장합니다.
*   **세션 관리 (Session Management):** 분산 서버 환경에서 사용자의 로그인 세션 정보를 공유할 때 사용합니다.
*   **실시간 순위표 (Leaderboard):** `Sorted Set`을 사용하여 점수 기반의 실시간 랭킹 시스템을 쉽게 구현합니다.
*   **메시지 브로커:** Pub/Sub 기능을 통해 간단한 메시지 큐 시스템으로 활용 가능합니다.

## 3. 요약

| 구분 | 설명 |
| :--- | :--- |
| **형태** | Key-Value NoSQL |
| **속도** | 매우 빠름 (In-Memory) |
| **휘발성** | 기본적으로 휘발성이지만 디스크 저장 옵션 존재 |
| **용도** | 캐시, 세션, 실시간 분석, 메시지 큐 등 |