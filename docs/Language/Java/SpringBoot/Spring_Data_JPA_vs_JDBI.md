# 비교: 직접 쿼리 작성(JDBI/JDBC) vs Spring Data JPA (CrudRepository)

전통적인 방식인 SQL을 직접 제어하는 방식과 Spring Data JPA의 추상화된 방식의 차이점을 분석합니다.

---

## 1. 개발 패러다임의 차이

| 구분 | 직접 쿼리 작성 방식 (JDBI, JDBC 등) | Spring Data JPA (CrudRepository) |
| :--- | :--- | :--- |
| **중심 사상** | **데이터 중심 (SQL 중심)** | **객체 중심 (Entity 중심)** |
| **쿼리 제어** | 개발자가 SQL을 직접 작성 (`@SqlUpdate`, `@SqlQuery`) | 프레임워크가 SQL을 자동 생성 및 실행 |
| **변경 감지** | 변경 사항을 수동으로 `Update` 쿼리로 실행 | 객체의 상태가 변하면 트랜잭션 종료 시 자동 반영 (Dirty Check) |
| **패러다임 불일치** | 개발자가 수동으로 매핑 처리 | 프레임워크가 객체와 테이블 간의 불일치 해결 |

---

## 2. 장단점 상세 비교

### 2.1 직접 쿼리 방식 (JDBI 등)

* **장점**:
    * **세밀한 최적화**: 특정 DB에 최적화된 복잡한 쿼리를 작성하기 유리합니다.
    * **직관성**: 어떤 SQL이 실행되는지 명확히 알 수 있습니다.
    * **학습 곡선**: SQL만 잘 안다면 러닝 커브가 낮습니다.
* **단점**:
    * **반복 작업**: 기본적인 CRUD 작업도 모두 쿼리를 작성해야 합니다. (생산성 저하)
    * **유지보수**: 테이블 스키마가 변하면 관련 SQL을 모두 찾아 수정해야 합니다.

### 2.2 Spring Data JPA (CrudRepository)

* **장점**:
    * **높은 생산성**: 인터페이스 정의만으로 CRUD가 완성됩니다.
    * **객체 지향적**: 데이터베이스를 마치 자바 컬렉션처럼 다룰 수 있습니다.
    * **유지보수 용이**: 엔티티 클래스만 수정하면 관련 SQL 처리가 자동으로 맞춰집니다.
* **단점**:
    * **학습 곡선**: 영속성 컨텍스트, 지연 로딩 등 JPA 내부 동작 원리를 이해해야 합니다.
    * **성능 위험**: 의도치 않은 대량 쿼리(N+1 문제)가 발생할 위험이 있습니다.

---

## 3. 코드 비교

### 직접 쿼리 방식 (JDBI 예시)
```java
@Repository
public interface UserJdbiRepo {
    @SqlUpdate("INSERT INTO users (name, email) VALUES (:name, :email)")
    void insert(@BindBean User user);

    @SqlQuery("SELECT * FROM users WHERE id = :id")
    User findById(@Bind("id") Long id);
}
```

### Spring Data JPA 방식
```java
@Repository
public interface UserJpaRepo extends CrudRepository<User, Long> {
    // 아무것도 작성하지 않아도 save(), findById() 제공됨
}
```

---

## 4. 어떤 상황에서 무엇을 써야 하나?

### 직접 쿼리 방식이 유리한 경우

* 데이터베이스 성능이 극도로 중요하여 **SQL 튜닝이 필수적**인 대규모 트래픽 서비스.
* 이미 복잡한 레거시 DB 스키마가 존재하여 ORM 매핑이 어려운 경우.
* 단순 통계 쿼리 등 조회 위주의 작업이 많은 경우.

### CrudRepository(JPA)가 유리한 경우

* **빠른 개발 속도**가 필요한 신규 프로젝트.
* 비즈니스 로직이 복잡하여 **객체 지향적인 설계**가 중요한 도메인 중심 서비스.
* 표준적인 CRUD 작업이 전체 로직의 대부분을 차지하는 경우.

---

## 5. 결론

기존에 사용하신 **JDBI 방식은 "SQL의 힘"**을 빌리는 것이고, **`CrudRepository` 방식은 "Spring의 생산성"**을 빌리는 것입니다. 최근에는 생산성을 위해 JPA를 기본으로 사용하되, 복잡한 쿼리만 Querydsl이나 JDBI를 섞어서 사용하는 **하이브리드 방식**이 가장 많이 쓰입니다.
