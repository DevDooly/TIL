---
title: Redis 아키텍처, 핵심 데이터 구조 및 실무 캐싱 전략
---

# ⚡ Redis (Remote Dictionary Server)

**Redis (Remote Dictionary Server)**는 초당 수십만 건의 빠른 I/O 처리가 가능한 오픈소스 **인메모리(In-Memory) 키-값(Key-Value) 데이터 구조 저장소**입니다.

주로 고성능 캐싱(Caching), 분산 세션 저장소, 실시간 랭킹 시스템, 분산 락(Distributed Lock) 및 메시징 큐(Pub/Sub, Streams)에 널리 활용됩니다.

---

## 1. Redis의 핵심 아키텍처 특징

1. **인메모리(In-Memory) 기반**: 모든 데이터를 RAM에 적재하여 마이크로초(µs) 단위의 초저지연 읽기/쓰기 성능을 제공합니다.
2. **단일 스레드(Single-Threaded) 명령 처리**:
   * 핵심 명령 실행 루프는 싱글 스레드로 동작하여 동시성 제어에 따른 Lock 경합이나 Race Condition 없이 원자적(Atomic) 연산을 보장합니다.
   * 네트워크 I/O 및 백그라운드 디스크 동기화는 별도의 멀티스레드(Redis 6.0+)로 처리됩니다.
3. **영속성(Persistence) 지원**:
   * **RDB (Redis Database Snapshot)**: 특정 시점의 메모리 스냅샷을 디스크 바이너리 파일(`.rdb`)로 덤프 (빠른 복구, 최근 데이터 유실 가능성 존재).
   * **AOF (Append Only File)**: 모든 쓰기/수정 명령어를 실시간 로그 파일에 기록 (데이터 유실 최소화, 파일 크기 증가 시 AOF Rewrite 수행).

---

## 2. 주요 데이터 구조 및 활용 사례

```mermaid
mindmap
  root((Redis Data Types))
    Strings
      JSON Cache / Token
      Atomic Counter (INCR / DECR)
      Bitmaps (출석 체크)
    Hashes
      사용자 프로필 (Field-Value)
      세션 데이터 관리
    Lists
      LPUSH / RPOP 큐
      최신 N개 피드 타임라인
    Sets
      SADD / SINTER 태그 시스템
      고유 방문자(UV) 수집
    Sorted Sets (ZSet)
      실시간 랭킹 (Leaderboard)
      Rate Limiter (시간 기반 윈도우)
    Streams
      Kafka 스타일 분산 이벤트 로그
      Consumer Group 지원
```

| 데이터 타입 | 주요 명령어 | 실무 활용 사례 |
| :--- | :--- | :--- |
| **String** | `SET`, `GET`, `INCR`, `SETNX`, `EXPIRE` | 세션/토큰 캐싱, 원자적 방문자 수 카운터, 분산 락 기본 구현 |
| **Hash** | `HSET`, `HGET`, `HGETALL`, `HINCRBY` | 객체 단위 사용자 정보, 장바구니 상품 목록 |
| **List** | `LPUSH`, `RPUSH`, `LPOP`, `BRPOP` | 선입선출(FIFO) 작업 큐, 최근 활동 로그 스트림 |
| **Set** | `SADD`, `SMEMBERS`, `SINTER`, `SISMEMBER` | 중복 없는 태그 목록, 친구 목록 공통 교집합 조회 |
| **Sorted Set** | `ZADD`, `ZRANGE`, `ZREVRANGEBYSCORE` | 실시간 점수 순위표(Leaderboard), 슬라이딩 윈도우 처리율 제한기 |
| **Stream** | `XADD`, `XREADGROUP`, `XACK` | 이벤트 소싱, 멀티 컨슈머 분산 메시징 |

---

## 3. 실무 캐싱 아키텍처 패턴

```mermaid
flowchart TD
    subgraph Pattern1 [Cache-Aside 패턴 (Lazy Loading)]
        App1[Application] -->|1. 캐시 조회| Redis1[(Redis Cache)]
        Redis1 -->|2. Cache Hit| App1
        Redis1 -.->|Cache Miss| DB1[(Primary DB)]
        App1 -->|3. DB 직접 조회| DB1
        App1 -->|4. 조회 데이터 캐시에 저장| Redis1
    end

    subgraph Pattern2 [Write-Through / Write-Behind 패턴]
        App2[Application] -->|1. 쓰기 요청| Redis2[(Redis Cache)]
        Redis2 -->|2-a. 동기 저장 (Write-Through)| DB2[(Primary DB)]
        Redis2 -.->|2-b. 비동기 배치 저장 (Write-Behind)| DB2
    end
```

### 1) Cache-Aside (Look-Aside)
* **장점**: 캐시가 죽더라도 DB를 통해 서비스 지속 가능, 실제로 요청된 데이터만 캐싱되어 메모리 효율적.
* **단점**: Cache Miss 시 DB 조회 및 캐시 갱신으로 인한 응답 지연 발생.

### 2) 캐시 스탬피드(Cache Stampede) 방지
* TTL이 만료되는 순간 동일 키에 대한 대량의 동시 요청이 DB로 몰려 장애가 발생하는 현상.
* **해결책**:
  * **Jitter (만료 시간에 무작위 오차 추가)**: `TTL = base_ttl + random(0, 60)`
  * **Mutex Lock (분산 락)**: Cache Miss 시 락을 획득한 단 1개의 스레드만 DB를 조회하고 나머지는 대기.

---

## 4. 운영 시 핵심 주의사항 & Best Practices

> [!CAUTION]
> **운영 환경에서 `KEYS *` 명령어 절대 사용 금지**
> 싱글 스레드 특성상 수백만 개의 키가 존재할 때 `KEYS *`를 실행하면 전체 서버가 멈추는(Hang) 심각한 장애가 발생합니다. 대신 반드시 `SCAN` 명령어를 사용해야 합니다.

1. **메모리 퇴거 정책 (Maxmemory-policy)**:
   * `allkeys-lru` / `volatile-lru`: 가장 오랫동안 참조되지 않은 키부터 삭제 (일반 캐시 환경 권장).
   * `noeviction`: 메모리가 꽉 차면 쓰기 명령 시 에러 반환 (데이터 유실이 절대 불가한 경우).
2. **Big Key 모니터링**:
   * 하나의 키에 수만~수십만 개의 요소가 들어있는 List/Set/Hash는 삭제(`DEL`) 시에도 O(N) 시간이 소요되어 서버를 블로킹합니다. `UNLINK`(비동기 삭제)를 사용해야 합니다.
3. **분산 락 (Distributed Lock)**:
   * 단일 인스턴스는 `SET key value NX PX 30000` 방식을 적용하고, 분산 클러스터 환경에서는 **Redlock 알고리즘** 또는 **Redisson** 라이브러리를 활용합니다.

---

## 5. References
* [Redis Documentation](https://redis.io/docs/)
* [Redis Best Practices - Memory and Latency Optimization](https://redis.io/docs/management/optimization/)