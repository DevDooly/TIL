# 파이프라인 (Pipeline)

## 1. 개요
파이프라인(Pipeline)은 데이터 처리의 단계(Step)들이 연쇄적으로 이어져 있는 구조를 말한다. 한 단계의 출력(Output)이 다음 단계의 입력(Input)으로 곧바로 연결되는 형태를 가지며, 이를 통해 **효율성**과 **자동화**를 달성할 수 있다.

## 2. 핵심 원리
*   **분할 정복(Divide and Conquer)**: 복잡한 작업을 작고 독립적인 단계들로 나눈다.
*   **병렬 처리(Parallelism)**: 각 단계가 독립적으로 수행될 수 있다면, 서로 다른 데이터를 동시에 처리하여 처리량(Throughput)을 높일 수 있다.
*   **스트리밍(Streaming)**: 데이터 전체가 처리되기를 기다리지 않고, 처리된 조각을 즉시 다음 단계로 넘긴다.

## 3. 파이프라인의 종류

### 3.1. 소프트웨어 파이프라인 (Unix Pipes)
가장 고전적이고 직관적인 형태이다. 유닉스(Unix) 계열 운영체제에서 `|` (파이프) 기호를 사용하여 프로그램들을 연결한다.
```bash
# 예시: 로그 파일에서 'Error'가 포함된 라인을 찾아, 개수를 세기
cat application.log | grep "Error" | wc -l
```
*   `cat`: 파일 읽기
*   `grep`: 필터링 (Transformation)
*   `wc`: 집계 (Aggregation)

### 3.2. 데이터 파이프라인 (Data Pipeline / ETL)
데이터 엔지니어링 분야에서 다양한 소스의 데이터를 수집, 변환하여 저장소로 옮기는 과정을 말한다.
*   **ETL (Extract, Transform, Load)**: 추출 -> 변환 -> 적재의 전통적인 방식.
*   **ELT (Extract, Load, Transform)**: 일단 데이터를 적재(Data Lake 등)한 후, 필요에 따라 변환하는 방식.
*   **도구**: Apache Airflow, Kafka Connect, AWS Glue 등.

### 3.3. CI/CD 파이프라인 (DevOps)
소프트웨어 개발 프로세스를 자동화한 파이프라인이다. 코드가 작성되어 배포되기까지의 과정을 단계별로 정의한다.
1.  **Build**: 코드 컴파일 및 패키징
2.  **Test**: 단위 테스트, 통합 테스트 자동 수행
3.  **Deploy**: 스테이징 또는 프로덕션 환경에 배포
*   **도구**: Jenkins, GitHub Actions, GitLab CI 등.

### 3.4. 명령어 파이프라인 (Instruction Pipeline)
컴퓨터 아키텍처(CPU) 수준에서의 파이프라인이다. 하나의 명령어를 처리하는 과정을 `Fetch -> Decode -> Execute -> Write-back` 등의 단계로 나누어, 동시에 여러 명령어를 겹쳐서 실행함으로써 CPU 성능을 극대화한다.

## 4. 파이프라인 패턴

### 4.1. Fan-out (확산)
하나의 입력이 여러 개의 파이프라인으로 분기되는 형태이다.
*   예: 결제 완료 이벤트가 발생하면 -> 1) 사용자에게 메일 발송, 2) 배송 시스템에 요청, 3) 통계 데이터 저장.

### 4.2. Fan-in (수렴)
여러 경로에서 처리된 데이터가 하나의 단계로 모이는 형태이다.
*   예: 여러 서버의 로그를 하나의 중앙 로그 저장소(ELK 등)로 수집.

## 5. 결론
파이프라인 아키텍처를 적용하면 **작업의 흐름이 명확**해지고 모듈화가 잘 되어 **유지보수와 확장**이 용이해진다. 하지만 단계가 많아질수록 복잡도가 증가하고 추적(Debugging)이 어려워질 수 있으므로, 적절한 모니터링과 오케스트레이션 도구의 도입이 필요하다.

### References
* [Wikipedia - Pipeline (computing)](https://en.wikipedia.org/wiki/Pipeline_(computing))
* [Wikipedia - Xargs](https://ko.wikipedia.org/wiki/Xargs)
