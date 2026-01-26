# 비관적 락(Pessimistic Lock) vs 낙관적 락(Optimistic Lock)

데이터베이스에서 동일한 데이터에 대해 여러 트랜잭션이 동시에 접근할 때, 데이터의 일관성을 유지하기 위해 사용하는 동시성 제어 전략이다.

## 1. 비관적 락 (Pessimistic Lock)
데이터 충돌이 발생할 것이라고 '비관적'으로 가정하고, 데이터를 읽는 시점에 미리 락을 걸어 다른 사용자의 접근을 차단하는 방식이다.

- **특징**: 
  - 데이터베이스 수준의 락(Exclusive Lock, Shared Lock)을 사용한다.
  - 트랜잭션이 완료될 때까지 다른 트랜잭션은 대기해야 하므로 데이터 정합성이 강력하게 보장된다.
- **사용 사례**: 
  - 데이터 수정이 빈번하여 충돌 가능성이 높은 경우.
  - 재고 관리, 금융 거래 등 데이터 무결성이 최우선인 시스템.
- **장단점**:
  - 장점: 충돌이 발생하기 전에 차단하므로 데이터 정합성이 높다.
  - 단점: 성능 저하의 원인이 될 수 있으며, 데드락(Deadlock)이 발생할 위험이 있다.

## 2. 낙관적 락 (Optimistic Lock)
데이터 충돌이 거의 발생하지 않을 것이라고 '낙관적'으로 가정하는 방식이다. DB 레벨의 락 대신 어플리케이션 레벨에서 버전 관리 기능을 사용한다.

- **특징**:
  - 데이터를 읽을 때 락을 걸지 않고, 수정 시점에 데이터가 변경되었는지 확인한다.
  - 주로 `version` 컬럼이나 `timestamp`를 활용하여 비교한다.
- **사용 사례**: 
  - 데이터 충돌 발생 확률이 낮은 경우.
  - 읽기 작업이 많고 수정 작업이 적은 시스템.
- **장단점**:
  - 장점: DB 락을 잡지 않으므로 성능상 이점이 있고 확장성이 좋다.
  - 단점: 충돌 발생 시 어플리케이션에서 롤백이나 재시도 로직을 직접 구현해야 한다.

## 3. 비교 요약
| 구분 | 비관적 락 (Pessimistic) | 낙관적 락 (Optimistic) |
| :--- | :--- | :--- |
| **락 시점** | 데이터 조회 시 (SELECT FOR UPDATE) | 데이터 수정 시 (UPDATE) |
| **제어 주체** | 데이터베이스 (DB) | 어플리케이션 (Code) |
| **충돌 대응** | 발생 전 예방 (Blocking) | 발생 후 처리 (Rollback/Retry) |
| **성능** | 비교적 낮음 | 비교적 높음 |

## References
* [SQLAlchemy - Transactions and Connection Management](https://docs.sqlalchemy.org/en/14/core/connections.html)
* [Database Concurrency Control - Wikipedia](https://en.wikipedia.org/wiki/Concurrency_control)

