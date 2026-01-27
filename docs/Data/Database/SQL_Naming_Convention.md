# SQL Naming Convention (SQL 명명 규칙)

데이터베이스 설계 시 일관된 이름을 사용하는 것은 가독성을 높이고 협업 시 발생할 수 있는 혼란을 줄이는 데 매우 중요합니다. 기본적으로 **snake_case** 규칙을 따르는 것을 권장합니다.

## 1. 데이터베이스(Database)
*   소문자를 사용하며 `snake_case`를 권장합니다.
*   예: `user_service_db`, `order_management`

## 2. 테이블(Table)
*   **단수형(Singular) 이름 사용:** `users` 보다는 `user`를 권장합니다. (객체 지향 모델과 매핑 시 유리)
*   소문자와 `snake_case`를 사용합니다.

```sql
CREATE TABLE user_profile (
    id BIGINT NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    ...
);
```

## 3. 컬럼(Column)
*   소문자와 `snake_case`를 사용합니다.
*   **기본 키 (Primary Key):** 단순하게 `id`로 지정하는 것이 가장 범용적입니다. (다른 테이블에서 참조 시 `user_id` 식으로 표현)
*   **외래 키 (Foreign Key):** `참조테이블명_id` 형식을 사용합니다. (예: `user_id`)
*   **날짜/시간:** `created_at`, `updated_at`, `deleted_at`과 같이 상태를 나타내는 이름을 사용합니다.

## 4. 제약 조건 (Constraints)
*   **기본 키:** `pk_테이블명` (예: `pk_user`)
*   **외래 키:** `fk_테이블명_참조테이블명` (예: `fk_order_user`)
*   **유니크 키:** `uk_테이블명_컬럼명` (예: `uk_user_email`)

## 참고
*   [SQL Naming Conventions Guide](https://www.sqlshack.com/learn-sql-naming-conventions/)