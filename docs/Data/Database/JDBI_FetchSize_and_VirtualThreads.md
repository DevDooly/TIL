# JDBI FetchSize: 드라이버 힌트와 결과 보관량 구분

대량 조회에서 fetch size를 줄였는데도 메모리 사용량이 그대로일 수 있다. JDBC의 `setFetchSize`와 JDBI 3의 `@FetchSize`는 한 번에 가져올 행 수를 드라이버에 알려주는 힌트다. 기본값과 실제 데이터를 가져오는 방식은 드라이버마다 다르며, 애플리케이션이 결과를 얼마나 오래 보관하는지는 별개다. [JDBC Statement API](https://docs.oracle.com/en/java/javase/21/docs/api/java.sql/java/sql/Statement.html#setFetchSize(int)), [JDBI Query API](https://jdbi.org/releases/3.54.0/apidocs/org/jdbi/v3/core/statement/Query.html)

## Fetch와 보관은 다른 단계다

`@FetchSize(1000)`을 붙여도 반환형이 `List<User>`이면 최종적으로 모든 결과를 메모리에 보관한다. 메모리 부담을 줄이려면 다음 두 조건을 함께 확인한다.

1. 드라이버가 서버 커서나 부분 fetch를 실제로 사용한다.
2. 애플리케이션이 스트림이나 이터레이터에서 읽은 결과를 처리한 뒤 전체 목록으로 다시 모으지 않는다.

예를 들어 pgJDBC의 cursor 기반 fetch는 auto-commit 해제, forward-only 결과, 양수 fetch size 등의 조건이 있다. Java `Stream`만 사용한다고 네트워크 스트리밍이 보장되지는 않는다. [pgJDBC 결과 처리 문서](https://jdbc.postgresql.org/documentation/query/)

## JDBI에서 자원 수명을 맞추기

아래 코드는 이미 구성된 `Jdbi jdbi`로 결과를 한 행씩 처리하는 예제다. SQL과 커서 사용 조건은 연결할 DB에 맞춰 조정한다.

```java
jdbi.useTransaction(handle -> {
    try (var rows = handle.createQuery(
            "select id from users where status = :status order by id")
            .bind("status", "ACTIVE")
            .setFetchSize(500)
            .mapTo(Long.class)
            .stream()) {
        rows.forEach(id -> {
            // 한 행씩 처리한다. 전체 List로 다시 수집하지 않는다.
            System.out.println(id);
        });
    }
});
```

stream을 handle/transaction 범위 밖으로 반환하거나 다른 스레드로 전달하지 않는다. 대용량·장시간 조회는 connection과 transaction을 오래 점유하므로, 업무 요건에 따라 keyset pagination과 짧은 트랜잭션도 비교한다. [JDBI 매뉴얼](https://jdbi.org/releases/3.54.0/)

## Virtual Thread와의 관계

FetchSize는 동시 쿼리 수를 제한하는 장치가 아니다. 가상 스레드를 많이 생성할 수 있어도 connection pool, in-flight 요청 수와 대기 시간에는 한도가 필요하다.

적절한 fetch size는 행 크기와 동시 조회 수에 따라 달라진다. 예제의 500을 시작점으로 삼더라도 결과 보관량, 네트워크 왕복 시간, GC, 연결 점유 시간을 보며 조정해야 한다. `@MaxRows`는 바이트 단위 메모리 한도가 아니고, `@QueryTimeout`만으로 모든 네트워크 대기가 취소되는 것도 아니다.

Pinning 여부는 driver/JDK 버전과 stack으로 진단하고, 필요할 때만 [제한된 실행기 격리](../../Language/Java/SpringBoot/JDBI_VT_Pinning_Solution.md)를 비교한다.
