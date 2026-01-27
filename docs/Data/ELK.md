# ELK Stack

**ELK Stack**은 Elasticsearch, Logstash, Kibana 세 가지 오픈소스 프로젝트의 약자로, 다양한 소스로부터 데이터를 수집하여 실시간으로 검색, 분석 및 시각화할 수 있는 강력한 데이터 플랫폼입니다. 최근에는 가벼운 데이터 수집기인 Beats가 추가되어 **Elastic Stack**이라고도 불립니다.

## 1. 구성 요소

### 1.1 Elasticsearch
*   **역할:** 분산형 검색 및 분석 엔진
*   **특징:**
    *   JSON 기반의 문서 지향(Document-oriented) 저장소입니다.
    *   Lucene 라이브러리를 기반으로 하며, 실시간(Near Real-Time) 검색 성능이 매우 뛰어납니다.
    *   정형, 비정형 데이터 모두 처리가 가능합니다.

### 1.2 Logstash
*   **역할:** 데이터 처리 파이프라인 (ETL 도구)
*   **특징:**
    *   입력(Input) -> 필터(Filter) -> 출력(Output)의 단계를 거칩니다.
    *   다양한 소스(로그, 웹 앱 등)에서 데이터를 수집하고, 원하는 형태로 가공하여 Elasticsearch 등으로 전달합니다.

### 1.3 Kibana
*   **역할:** 데이터 시각화 및 관리 도구
*   **특징:**
    *   Elasticsearch에 저장된 데이터를 그래프, 차트, 지도 등으로 시각화합니다.
    *   로그 분석 대시보드를 구성하거나 Elastic Stack 전체의 상태를 모니터링하는 인터페이스 역할을 합니다.

### 1.4 Beats (추가 구성품)
*   **역할:** 경량 데이터 수집기 (Shipper)
*   **특징:**
    *   서버에 에이전트로 설치되어 파일(Filebeat), 메트릭(Metricbeat) 등을 Logstash나 Elasticsearch로 전송합니다.
    *   리소스 사용량이 매우 적어 수집용으로 최적화되어 있습니다.

## 2. 데이터 흐름 (Workflow)

1.  **수집 (Beats):** 각 서버에서 로그 또는 상태 데이터를 수집합니다.
2.  **가공 (Logstash):** 수집된 데이터를 통합하고 형식을 변환(Parsing)합니다.
3.  **색인/저장 (Elasticsearch):** 가공된 데이터를 검색 가능하도록 저장합니다.
4.  **시각화 (Kibana):** 저장된 데이터를 대시보드를 통해 분석합니다.

## 참고
*   [Elastic 공식 홈페이지](https://www.elastic.co/kr/elastic-stack)