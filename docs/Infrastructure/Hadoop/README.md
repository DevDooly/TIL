# Hadoop (Apache Hadoop)

**Apache Hadoop**은 대량의 데이터를 분산 환경에서 저장하고 처리할 수 있는 오픈 소스 프레임워크입니다. Google의 GFS(Google File System)와 MapReduce 논문에서 영감을 받아 개발되었습니다.

## 1. 핵심 구성 요소

### 1.1 HDFS (Hadoop Distributed File System)
*   **분산 파일 시스템:** 데이터를 여러 노드(서버)에 쪼개서 저장합니다.
*   **특징:** 데이터를 블록 단위(기본 128MB)로 나누고 복제(Replication, 기본 3개)하여 저장하므로, 특정 노드가 고장 나도 데이터 손실을 방지합니다.

### 1.2 MapReduce (맵리듀스)
*   **분산 처리 모델:** 데이터를 처리하는 로직을 Map(쪼개서 처리)과 Reduce(결과 취합) 단계로 나누어 수행합니다.
*   **단점:** 디스크 기반으로 동작하여 속도가 느린 편이라, 최근에는 **Apache Spark**와 같은 인메모리 처리 엔진이 많이 사용됩니다.

### 1.3 YARN (Yet Another Resource Negotiator)
*   **리소스 관리자:** 클러스터 내의 컴퓨팅 리소스(CPU, RAM)를 관리하고 애플리케이션에 할당하는 스케줄러 역할을 합니다.

## 2. 참고
*   [Apache Hadoop 공식 사이트](https://hadoop.apache.org/)
*   [Hadoop Documentation](https://hadoop.apache.org/docs/stable/)