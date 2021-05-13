# SQL Naming Conventions
기본적으로 snake_case 를 따른다.
## Create Database
```
CREATE DATABASE 'database_name';
```

## Create Table
### Table Name
```
CREATE TABLE table_name {
    column_name column_type,
    column_name column_type,
    ...
);
```

**예시**
```
CREATE TABLE city (
    id int  NOT NULL IDENTITY(1, 1),
    city_name char(128)  NOT NULL,
    lat decimal(9,6)  NOT NULL,
    long decimal(9,6)  NOT NULL,
    country_id int  NOT NULL,
    CONSTRAINT city_pk PRIMARY KEY  (id)
);
```

### Column Name
* 기본 키 / Primary Key
  * 일반적으로 기본 키는 하나만 있어야 한다.
  * id 로 지정하는것이 가장 좋다.
  * 의미있는 방식으로 PK 제약 조건의 이름을 지정해야합니다. 예를 들어 데이터베이스에서 호출 테이블 의 PK 이름은 call_pk입니다.  
  ~~( 설명이 부족함.. 추후 수정해야 함)~~  
  https://docs.microsoft.com/ko-kr/sql/relational-databases/indexes/clustered-and-nonclustered-indexes-described?view=sql-server-ver15

## References
* https://www.sqlshack.com/learn-sql-naming-conventions/
