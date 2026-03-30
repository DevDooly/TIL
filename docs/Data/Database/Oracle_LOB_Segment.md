# Oracle LOB Segment 및 ORA-01692 에러 조치

## 1. LOB (Large Object) Segment 란?

Oracle 데이터베이스에서 **LOB (Large Object)** 데이터 타입은 텍스트, 이미지, 동영상, 사운드 등 크기가 큰 비정형 데이터를 저장하기 위해 사용됩니다. 대표적으로 `CLOB`(대용량 문자열), `BLOB`(대용량 바이너리 데이터) 등이 있습니다.

LOB 데이터는 일반적인 테이블의 행(Row) 데이터와는 다른 방식으로 저장 및 관리됩니다.

### 1.1 LOB 데이터의 저장 구조
LOB 컬럼을 생성하면 Oracle은 내부적으로 다음 세 가지 요소를 생성합니다.

1. **LOB Locator (LOB 위치 지정자)**: 
    * 실제 테이블의 행(Row) 안에는 데이터 자체가 아니라, 데이터가 저장된 위치를 가리키는 **포인터(Locator)**만 저장됩니다.
2. **LOB Segment (LOB 세그먼트)**: 
    * 실제 대용량 데이터가 물리적으로 저장되는 독립된 공간입니다. (기본적으로 테이블과 분리되어 저장됨)
3. **LOB Index (LOB 인덱스)**: 
    * LOB Segment 내에서 데이터의 특정 위치를 빠르게 찾기 위해 시스템이 자동으로 생성하고 관리하는 인덱스입니다.

### 1.2 In-Row vs Out-of-Row

* **In-Row Storage**: LOB 데이터의 크기가 약 4,000 바이트(정확히는 3964 바이트) 이하일 경우, 별도의 LOB Segment를 쓰지 않고 일반 테이블 행(Row) 안에 직접 저장하여 성능을 높입니다. (기본 설정: `ENABLE STORAGE IN ROW`)
* **Out-of-Row Storage**: 데이터가 4,000 바이트를 초과하면, 행 안에는 Locator만 남기고 실제 데이터는 **LOB Segment**로 이동시켜 저장합니다.

---

## 2. ORA-01692 에러 원인 및 조치 방법

### 2.1 ORA-01692 에러란?
> `ORA-01692: unable to extend lob segment [소유자].[LOB세그먼트명] by [크기] in tablespace [테이블스페이스명]`

이 에러는 대용량 데이터(BLOB, CLOB 등)를 `INSERT` 하거나 `UPDATE` 할 때, **해당 LOB 세그먼트가 위치한 테이블스페이스(Tablespace)에 남은 여유 공간이 부족하여 세그먼트를 더 이상 확장(Extend)할 수 없을 때 발생**합니다.

### 2.2 원인 파악
주로 다음 세 가지 경우에 발생합니다.

1. **데이터 파일의 가득 참**: 테이블스페이스를 구성하는 데이터 파일(Datafile)의 물리적 용량이 꽉 찬 경우.
2. **Autoextend 설정 꺼짐**: 데이터 파일의 용량이 남아있어도 자동 확장(Autoextend)이 비활성화되어 있는 경우.
3. **Maxsize 도달**: 자동 확장이 켜져 있으나, 관리자가 설정한 최대 크기(Maxsize)에 도달한 경우.

### 2.3 해결 방법 (Troubleshooting)

이 문제를 해결하려면 테이블스페이스의 용량을 늘려주어야 합니다. DBA 권한(sysdba)으로 접근하여 다음 중 하나의 방법을 적용합니다.

#### 방법 1: 기존 데이터 파일 크기(Size) 늘리기
가장 간단한 방법으로, 꽉 찬 데이터 파일의 물리적 크기 자체를 리사이즈(Resize)합니다.

```sql
-- 데이터 파일 경로와 크기 확인
SELECT file_name, bytes/1024/1024 AS MB 
FROM dba_data_files 
WHERE tablespace_name = '문제가_발생한_테이블스페이스명';

-- 데이터 파일 크기 증가 (예: 10GB로 늘리기)
ALTER DATABASE DATAFILE '/오라클/경로/datafile01.dbf' RESIZE 10240M;
```

#### 방법 2: 기존 데이터 파일에 자동 확장(Autoextend) 설정하기
데이터가 찰 때마다 일정 크기씩 자동으로 늘어나도록 설정합니다.

```sql
-- 자동 확장 설정 (예: 100MB씩 증가, 최대 무제한)
ALTER DATABASE DATAFILE '/오라클/경로/datafile01.dbf' 
AUTOEXTEND ON NEXT 100M MAXSIZE UNLIMITED;
```

#### 방법 3: 테이블스페이스에 새로운 데이터 파일 추가 (권장)
기존 데이터 파일이 이미 너무 크거나 파일 시스템(디스크)의 제한에 걸렸다면, 새로운 데이터 파일을 생성하여 테이블스페이스에 추가하는 것이 가장 안전합니다.

```sql
-- 새로운 데이터 파일 추가 (예: 1GB 생성 후 100MB씩 자동 확장)
ALTER TABLESPACE 문제가_발생한_테이블스페이스명 
ADD DATAFILE '/오라클/경로/datafile02.dbf' 
SIZE 1024M 
AUTOEXTEND ON NEXT 100M MAXSIZE UNLIMITED;
```

### 💡 추가 팁: LOB 세그먼트 이름으로 소속 테이블 찾기
에러 메시지에 테이블 이름 대신 이상한 LOB 세그먼트 이름(`SYS_LOB...`)이 나와서 어떤 테이블에서 문제가 터졌는지 알기 어려울 때가 있습니다. 아래 쿼리로 테이블을 역추적할 수 있습니다.

```sql
SELECT table_name, column_name 
FROM dba_lobs 
WHERE segment_name = '에러에_나온_LOB세그먼트명';
```