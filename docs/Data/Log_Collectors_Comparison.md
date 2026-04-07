# 로그 수집기 비교: Logstash vs Fluentd vs Fluent-bit

데이터 파이프라인의 핵심인 로그 수집기 3종을 비교하고, 특히 경량화와 성능이 중요한 환경에서 Fluent-bit이 왜 선호되는지 분석합니다.

---

## 1. 도구별 핵심 특징 및 차이점

| 구분 | Logstash | Fluentd | Fluent-bit |
| :--- | :--- | :--- | :--- |
| **개발 언어** | JRuby (Java 기반) | C & Ruby | **C (순수 C)** |
| **메모리 사용량** | 약 1GB+ (매우 높음) | 약 40MB ~ 100MB | **약 1MB ~ 10MB (초경량)** |
| **플러그인** | 200개 이상 (매우 풍부) | 1,000개 이상 (방대함) | 약 100개 내외 (필수 위주) |
| **주요 용도** | 복잡한 데이터 변환/가공 | 범용 로그 수집 레이어 | **컨테이너/Edge/Cloud 전용** |
| **운영 주체** | Elastic (ELK Stack) | Treasure Data (CNCF) | Treasure Data (CNCF) |

---

## 2. 왜 Fluent-bit을 선택해야 하는가? (선택의 이유)

현대적인 아키텍처(Kubernetes, Microservices)에서 Fluent-bit이 더 좋은 이유는 명확합니다.

### 2.1 압도적인 리소스 효율성

* **Zero Dependency**: Java나 Ruby 런타임이 필요 없는 순수 C로 작성되었습니다.
* **저사양 환경 최적화**: 메모리 사용량이 Logstash 대비 1/100 수준입니다. 이는 수백 개의 Pod가 떠 있는 K8s 환경에서 **Node의 리소스 낭비를 최소화**해줍니다.

### 2.2 클라우드 네이티브 및 컨테이너 최적화

* Docker, Kubernetes 메타데이터를 자동으로 수집하고 태그를 붙이는 기능이 매우 강력합니다.
* **Sidecar 또는 DaemonSet**으로 배포하기에 가장 이상적인 크기를 가집니다.

### 2.3 성능 (High Throughput)

* C 언어로 작성된 엔진은 높은 처리량(Throughput)을 보장하며, 복잡한 비즈니스 로직 가공보다 **빠른 전달과 라우팅**에 집중되어 있어 지연 시간(Latency)이 짧습니다.

### 2.4 Fluentd와의 완벽한 공생

* Fluent-bit은 Fluentd와 같은 에코시스템에 속해 있습니다.
* 각 노드에서 경량인 **Fluent-bit이 로그를 수집(Aggregator)**하여 중앙의 **Fluentd로 전달(Processor)**하는 계층형 구조(Tiered Architecture)를 쉽게 구축할 수 있습니다.

---

## 3. 요약 및 권장 환경

* **Logstash**: 이미 ELK 스택을 풀세트로 사용 중이며, 매우 복잡한 데이터 변환(Filter) 로직이 중앙 서버에서 필요한 경우.
* **Fluentd**: 다양한 소스로부터 데이터를 받아 정제하고, 방대한 플러그인 생태계가 필요한 범용 Aggregator로 사용 시.
* **Fluent-bit (Best Choice)**: **Kubernetes 환경**, 컨테이너 기반 마이크로서비스, 또는 리소스 사용량이 민감한 클라우드 인프라의 로그 수집기로 가장 적합.

---

## 4. 결론
가장 중요한 것은 **"인프라 자원을 로그 수집에 얼마나 할당할 것인가?"**입니다. Fluent-bit은 비즈니스 로직에 쓰여야 할 소중한 CPU와 메모리를 로그 수집기가 과하게 점유하는 것을 막아주는 가장 스마트한 선택입니다.
