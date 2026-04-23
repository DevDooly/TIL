# Spring Data JPA: CrudRepository 가이드

**CrudRepository**는 Spring Data JPA에서 제공하는 인터페이스로, 기본적인 CRUD(Create, Read, Update, Delete) 기능을 추상화하여 제공합니다. 개발자는 인터페이스 선언만으로 데이터베이스 조작 로직을 완성할 수 있습니다.

---

## 1. CrudRepository란?

Spring Data 프로젝트의 공통 인터페이스인 `Repository`를 상속받아, 실제 서비스 구축에 필요한 가장 기본적인 메서드들을 정의해 둔 인터페이스입니다.

### 계층 구조

* `Repository<T, ID>`: 마커 인터페이스.
* **`CrudRepository<T, ID>`**: 기본 CRUD 기능 제공.
* `PagingAndSortingRepository<T, ID>`: 페이징 및 정렬 기능 추가.
* `JpaRepository<T, ID>`: JPA 특화 기능(Flush, 배치 삭제 등) 추가.

---

## 2. 주요 메서드 설명

| 메서드 | 설명 |
| :--- | :--- |
| `<S extends T> S save(S entity)` | 엔티티 저장 및 수정 (ID 존재 여부에 따라 결정) |
| `Optional<T> findById(ID id)` | ID를 통한 단건 조회 |
| `Iterable<T> findAll()` | 모든 엔티티 조회 |
| `long count()` | 전체 엔티티 개수 반환 |
| `void deleteById(ID id)` | ID를 통한 삭제 |
| `void delete(T entity)` | 엔티티 객체를 통한 삭제 |
| `boolean existsById(ID id)` | 해당 ID 존재 여부 확인 |

---

## 3. 사용 방법

### 3.1 Entity 정의
```java
@Entity
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String name;
    private String email;
    
    // Getter, Setter, Constructor...
}
```

### 3.2 Repository 생성
인터페이스를 만들고 `CrudRepository<엔티티타입, ID타입>`를 상속받습니다.

```java
@Repository
public interface UserRepository extends CrudRepository<User, Long> {
    // 기본적인 CRUD 메서드는 이미 포함되어 있음
    
    // 추가적인 쿼리 메서드 정의 가능
    List<User> findByName(String name);
}
```

### 3.3 서비스에서 사용
```java
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;

    public User createUser(String name, String email) {
        User user = new User(name, email);
        return userRepository.save(user); // 저장
    }

    public Optional<User> getUser(Long id) {
        return userRepository.findById(id); // 조회
    }
}
```

---

## 4. CrudRepository vs JpaRepository

실무에서는 `CrudRepository`보다 기능이 더 많은 **`JpaRepository`**를 주로 사용합니다.

* **CrudRepository**: 순수하게 CRUD 기능만 필요할 때 사용. (범용적)
* **JpaRepository**: 페이징, 정렬, 배치 처리, Flush 등 JPA 고유 기능이 필요할 때 사용. 

---

## 5. 결론

`CrudRepository`는 데이터 접근 계층을 추상화하여 **반복적인 코드 작성을 획기적으로 줄여줍니다.** SQL 중심의 개발에서 객체 중심의 개발로 전환하게 해주는 Spring Data JPA의 핵심 도구입니다.
