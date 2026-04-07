# Caffeine Cache: 고성능 Java 로컬 캐시 가이드

**Caffeine**은 Java 8 이상을 위한 고성능 캐싱 라이브러리입니다. Google Guava 캐시를 영감으로 삼아 재설계되었으며, 현재 Java 생태계에서 가장 빠르고 효율적인 로컬 캐시로 평가받습니다.

---

## 1. Caffeine Cache의 핵심 특징

1.  **압도적 성능**: 인메모리 캐시 중 거의 이론적 한계에 가까운 속도를 제공합니다.
2.  **W-TinyLFU 알고리즘**: 기존의 LRU(Least Recently Used)나 LFU(Least Frequently Used)보다 진화된 알고리즘을 사용하여 캐시 적중률(Hit Rate)을 극대화합니다.
3.  **다양한 만료 정책**: 시간 기반, 크기 기반, 참조 기반 만료를 지원합니다.
4.  **통계 수집**: 캐시 적중률, 에러율 등 운영에 필요한 다양한 지표를 제공합니다.

---

## 2. 핵심 알고리즘: W-TinyLFU

대부분의 캐시는 **LRU**(최근에 안 쓴 것 삭제)를 사용하지만, Caffeine은 **W-TinyLFU**를 사용합니다.
*   **TinyLFU**: 적은 메모리로 각 항목의 접근 빈도를 추적합니다.
*   **Window**: 최근에 들어온 데이터가 바로 쫓겨나지 않도록 보호하는 구역을 둡니다.
*   **효과**: 빈도가 높으면서 최근성도 유지하는 데이터 위주로 캐시를 유지하여 성능을 높입니다.

---

## 3. 기본 사용법 (Java)

### 3.1 의존성 추가 (Gradle)
```gradle
dependencies {
    implementation 'com.github.ben-manes.caffeine:caffeine:3.1.8'
}
```

### 3.2 캐시 생성 예시
```java
Cache<String, DataObject> cache = Caffeine.newBuilder()
    .expireAfterWrite(Duration.ofMinutes(5)) // 쓰기 후 5분 뒤 만료
    .maximumSize(10_000)                    // 최대 1만 개 항목 유지
    .recordStats()                          // 통계 수집 활성화
    .build();

// 값 저장
cache.put("key1", dataObject);

// 값 조회 (없으면 null)
DataObject data = cache.getIfPresent("key1");

// 값 조회 (없으면 생성하여 반환 - 추천 방식)
DataObject data = cache.get("key2", k -> createData(k));
```

---

## 4. Spring Boot 연동

Spring Boot에서는 `@Cacheable` 추상화와 함께 사용하여 매우 간편하게 적용할 수 있습니다.

### 4.1 설정 (CacheManager)
```java
@Configuration
@EnableCaching
public class CacheConfig {
    @Bean
    public CacheManager cacheManager() {
        CaffeineCacheManager cacheManager = new CaffeineCacheManager("users", "products");
        cacheManager.setCaffeine(Caffeine.newBuilder()
                .expireAfterWrite(10, TimeUnit.MINUTES)
                .maximumSize(500));
        return cacheManager;
    }
}
```

### 4.2 서비스 적용
```java
@Service
public class UserService {
    @Cacheable(cacheNames = "users", key = "#id")
    public User getUserById(Long id) {
        // 실제 DB 조회 로직 (캐시 히트 시 실행 안 됨)
        return userRepository.findById(id).orElseThrow();
    }
}
```

---

## 5. 로컬 캐시 사용 시 주의사항

*   **메모리 관리**: 로컬 캐시는 JVM 힙(Heap) 메모리를 사용하므로 `maximumSize`를 적절히 설정하여 OOM(Out Of Memory)을 방지해야 합니다.
*   **데이터 일관성**: 분산 환경(여러 대의 서버)에서는 각 서버마다 캐시 내용이 다를 수 있습니다. 데이터의 엄격한 일관성이 중요하다면 Redis 같은 분산 캐시를 고려해야 합니다.

---

## 6. 결론
빠른 응답 속도가 중요하고 서버 간의 데이터 불일치가 큰 문제가 되지 않는 영역(예: 설정 정보, 빈번한 공통 코드 조회 등)에서 Caffeine은 가장 강력한 무기입니다.
