# JDBI FetchSize: 드라이버 힌트와 결과 보관량 구분

기준: JDBC / JDBI 3 API, 2026-09-07.

`setFetchSize`와 JDBI의 `@FetchSize`는 결과를 가져오는 행 수에 대한 **드라이버 힌트**다. 모든 JDBC 드라이버의 기본값이 10이거나, 설정값대로 정확히 네트워크 왕복이 나뉜다고 일반화할 수 없다. [JDBC Statement API](https://docs.oracle.com/en/java/javase/21/docs/api/java.sql/java/sql/Statement.html#setFetchSize(int)), [JDBI Query API](https://jdbi.org/releases/3.54.0/apidocs/org/jdbi/v3/core/statement/Query.html)

## Fetch와 보관은 다른 단계다

`@FetchSize(1000)`을 붙여도 반환형이 `List<User>`이면 최종적으로 모든 결과를 메모리에 보관한다. 메모리 부담을 줄이려면 다음 두 조건을 함께 확인한다.

1. driver가 서버 cursor/부분 fetch를 실제 사용한다.
2. 애플리케이션도 stream/iterator를 소비하면서 처리하고 전체 결과를 다시 모으지 않는다.

예를 들어 pgJDBC의 cursor 기반 fetch는 auto-commit 해제, forward-only 결과, 양수 fetch size 등의 조건이 있다. Java `Stream`만 사용한다고 네트워크 스트리밍이 보장되지는 않는다. [pgJDBC 결과 처리 문서](https://jdbc.postgresql.org/documentation/query/)

## JDBI에서 자원 수명을 맞추기

아래는 이미 구성한 `Jdbi jdbi`를 사용하는 코드 조각이다. SQL과 driver의 cursor 조건은 해당 DB에 맞춰야 한다.

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

측정할 항목은 행 너비, 동시 조회 수, 결과 보관량, 왕복 지연, GC와 connection 점유 시간이다. 500이나 1000을 모든 시스템의 권장값으로 정하지 않는다. `@MaxRows`·`@QueryTimeout`도 byte 단위 메모리 상한이나 모든 네트워크 대기의 확실한 취소를 보장하지 않는다.

Pinning 여부는 driver/JDK 버전과 stack으로 진단하고, 필요할 때만 [제한된 실행기 격리](../../Language/Java/SpringBoot/JDBI_VT_Pinning_Solution.md)를 비교한다.
