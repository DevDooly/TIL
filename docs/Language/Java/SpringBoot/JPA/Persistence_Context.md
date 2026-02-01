# JPA Persistence Context (영속성 컨텍스트)

JPA(Java Persistence API)에서 가장 중요한 개념인 **영속성 컨텍스트(Persistence Context)**의 동작 원리와 핵심 기능(1차 캐시, 쓰기 지연, 변경 감지)을 설명합니다.

## 1. 영속성 컨텍스트란?

영속성 컨텍스트는 **"엔티티를 영구 저장하는 논리적인 환경"**을 의미합니다. 애플리케이션과 데이터베이스 사이에서 객체를 보관하는 가상의 계층 역할을 수행합니다.

`EntityManager`를 통해 영속성 컨텍스트에 접근하고 관리할 수 있습니다.

```java
EntityManager em = emf.createEntityManager();
```

## 2. 엔티티의 생명주기 (Entity LifeCycle)

*   **비영속 (New/Transient)**: 영속성 컨텍스트와 전혀 관계가 없는 새로운 상태
*   **영속 (Managed)**: 영속성 컨텍스트에 관리되는 상태 (`em.persist(entity)`)
*   **준영속 (Detached)**: 영속성 컨텍스트에 저장되었다가 분리된 상태 (`em.detach(entity)`)
*   **삭제 (Removed)**: 삭제된 상태 (`em.remove(entity)`)

## 3. 영속성 컨텍스트의 핵심 이점

### 3.1 1차 캐시 (First Level Cache)

영속성 컨텍스트는 내부에 캐시(Map<Key, Value>)를 가지고 있습니다.
*   **Key**: DB PK (Primary Key)
*   **Value**: 엔티티 객체

```java
// 1차 캐시에 저장됨
em.persist(member);

// 1차 캐시에서 조회 (DB 조회 X)
Member findMember = em.find(Member.class, "member1");
```
*   DB를 거치지 않고 메모리에서 바로 조회하므로 성능상 이점이 있습니다.
*   단, 트랜잭션 단위의 캐시이므로 트랜잭션이 끝나면 사라집니다 (OSIV 제외).

### 3.2 영속 엔티티의 동일성(Identity) 보장

같은 트랜잭션 안에서 조회한 엔티티는 동일한 참조값(주소)을 가집니다.

```java
Member a = em.find(Member.class, "member1");
Member b = em.find(Member.class, "member1");

System.out.println(a == b); // true
```

### 3.3 트랜잭션을 지원하는 쓰기 지연 (Transactional Write-Behind)

엔티티를 저장(`persist`)해도 즉시 INSERT SQL을 날리지 않습니다.
1.  1차 캐시에 저장하고, **쓰기 지연 SQL 저장소**에 쿼리를 쌓아둡니다.
2.  `transaction.commit()` 시점에 쌓여있던 SQL을 DB에 한 번에 보냅니다 (`flush`).

```java
em.persist(memberA);
em.persist(memberB);
// 여기까지 INSERT SQL 안 나감

transaction.commit(); 
// 커밋하는 순간 INSERT SQL 일괄 전송
```

### 3.4 변경 감지 (Dirty Checking)

JPA는 엔티티 수정 시 별도의 `update()`나 `save()` 메서드를 호출할 필요가 없습니다. 이를 **더티 체킹(Dirty Checking)**이라고 합니다.

*   **동작 원리**:
    1.  **스냅샷 생성**: JPA는 엔티티를 영속성 컨텍스트에 보관할 때, 최초 상태를 복사해서 저장해둡니다 (스냅샷).
    2.  **비교**: `flush()`가 호출되는 시점에 현재 엔티티의 상태와 스냅샷을 비교합니다.
    3.  **SQL 생성**: 변경된 내용이 있다면 UPDATE SQL을 생성하여 쓰기 지연 저장소에 보냅니다.
    4.  **반영**: 데이터베이스에 최종적으로 반영됩니다.

*   **핵심 조건**: 엔티티가 영속성 컨텍스트에 의해 관리되는 **영속(Managed) 상태**여야만 더티 체킹이 일어납니다. 준영속(Detached)이나 비영속(New) 상태의 객체는 값을 바꿔도 DB에 반영되지 않습니다.

*   **실무 팁 (@DynamicUpdate)**:
    - 기본적으로 JPA의 더티 체킹은 **모든 필드를 업데이트**하는 쿼리를 생성합니다 (쿼리 재사용성 및 데이터베이스 최적화 때문).
    - 만약 필드가 너무 많아 변경된 데이터만 동적으로 업데이트 쿼리를 만들고 싶다면 엔티티 클래스 상단에 `@DynamicUpdate`를 사용합니다.

```java
@Entity
@DynamicUpdate // 변경된 필드만 반영하고 싶을 때 사용
public class Member { ... }
```

### 3.5 지연 로딩 (Lazy Loading)

연관된 엔티티를 실제 사용할 때 조회하는 기능입니다. (프록시 객체 사용)

---

## 4. Flush (플러시)

영속성 컨텍스트의 변경 내용을 데이터베이스에 반영하는 작업을 말합니다.

### 플러시가 발생하는 시점
1.  `em.flush()` 직접 호출
2.  트랜잭션 커밋 시 자동 호출
3.  JPQL 쿼리 실행 시 자동 호출 (이전 변경 사항이 반영되어야 조회가 정확하므로)

> **주의**: 플러시는 영속성 컨텍스트를 비우는 것이 아니라, **변경 내용을 DB에 동기화**하는 작업입니다.

---

## 5. 요약

| 기능 | 설명 |
| :--- | :--- |
| **1차 캐시** | DB 조회 횟수를 줄여 성능 향상 |
| **동일성 보장** | `==` 비교가 `true`임 (객체 지향적인 개발 가능) |
| **쓰기 지연** | 버퍼링 기능으로 최적화 가능 (Batch Insert) |
| **변경 감지** | 객체 값만 바꾸면 DB 자동 업데이트 |
