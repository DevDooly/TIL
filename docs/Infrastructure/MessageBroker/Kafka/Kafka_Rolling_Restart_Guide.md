# Kafka Broker 롤링 재시작 가이드 (3대 HA 구성)

3대 HA(고가용성) 구성의 Kafka Broker에서 설정을 변경하거나 업그레이드를 수행할 때, 서비스 중단 없이 적용하기 위한 **롤링 재시작(Rolling Restart)** 절차를 설명합니다.

---

## 1. 롤링 재시작 전 필수 확인 사항 (Pre-requisites)

안전하고 무중단에 가까운 롤링 재시작을 위해 다음 사항들을 반드시 확인해야 합니다.

1.  **복제 계수 (Replication Factor) 확인:**
    *   모든 Topic의 복제 계수가 **최소 2 이상 (권장 3 이상)**이어야 합니다. 3대 Broker 구성이므로 3이 가장 이상적입니다.
    *   `kafka-topics.sh --bootstrap-server <broker_ip>:<port> --describe` 명령으로 각 Topic의 복제 계수를 확인할 수 있습니다.
2.  **`min.insync.replicas` 설정 확인:**
    *   각 Topic (또는 Broker 전체)에 설정된 `min.insync.replicas` 값은 **`(복제 계수 - 1)` 이상**으로 설정되어야 합니다. 예를 들어, 복제 계수가 3인 Topic에 `min.insync.replicas=2`로 설정되어 있다면, 한 대의 Broker가 중단되더라도 나머지 두 대의 복제본이 ISR에 남아 메시지 생산 및 소비가 중단되지 않습니다.
    *   `min.insync.replicas`가 너무 낮으면 데이터 안정성이 떨어지고, 너무 높으면 Broker 한 대만 중단되어도 Producer가 메시지를 보낼 수 없게 됩니다.
3.  **`unclean.leader.election.enable=false` 확인:**
    *   **필수적으로 `false` (기본값)를 유지해야 합니다.** 이 설정이 `true`이면 ISR에 없는 복제본도 Leader가 될 수 있어 **데이터 손실**의 위험이 매우 큽니다.
4.  **클러스터 건전성 확인:**
    *   재시작 전, 클러스터에 `Under-replicated Partitions` (복제본 수가 충분하지 않은 파티션)이나 기타 경고/에러가 없는지 반드시 확인해야 합니다.
    *   `kafka-topics.sh --bootstrap-server <broker_ip>:<port> --describe --under-replicated-partitions` 명령으로 확인할 수 있습니다.
    *   Zookeeper (또는 Kraft) 앙상블이 안정적으로 동작 중인지 확인합니다.

---

## 2. 롤링 재시작 절차 (Step-by-Step)

다음 절차를 따라 한 대씩 Broker를 재기동합니다. 이 과정에서 **모니터링이 매우 중요합니다.**

1.  **대상 Broker 선택:** 재기동할 첫 번째 Broker를 선택합니다. (예: `broker-1`)

2.  **Broker 중지:**
    *   `ssh`로 해당 Broker에 접속하여 Kafka 서비스를 안전하게 중지합니다.
    *   예시: `sudo systemctl stop kafka` 또는 `bin/kafka-server-stop.sh`

3.  **설정 변경:**
    *   Broker의 `server.properties` 파일에서 필요한 설정을 변경합니다. (예: `replica.fetch.max.bytes`를 2MB 이상으로 변경)

4.  **Broker 시작:**
    *   예시: `sudo systemctl start kafka` 또는 `bin/kafka-server-start.sh -daemon config/server.properties`

5.  **클러스터 안정화 대기 (가장 중요):**
    *   재시작된 Broker가 클러스터에 완전히 재참여하고, 해당 Broker가 Leader 또는 Follower로 담당하던 모든 파티션이 **ISR (In-Sync Replicas)에 다시 포함될 때까지 충분히 기다려야 합니다.**
    *   **모니터링 툴 (Prometheus/Grafana, Confluent Control Center 등)을 통해 `UnderReplicatedPartitions` 지표가 0이 되고, 모든 파티션이 Healthy 상태임을 확인하세요.**
    *   `kafka-topics.sh --bootstrap-server <broker_ip>:<port> --describe` 명령으로 각 파티션의 ISR 상태를 주기적으로 확인하는 것도 도움이 됩니다.

6.  **다음 Broker로 반복:**
    *   첫 번째 Broker가 완전히 안정화되고 클러스터 전체가 건강한 상태임을 확인한 후, 두 번째 Broker에 대해 1~5단계를 반복합니다.
    *   마찬가지로 두 번째 Broker도 안정화되면, 세 번째 Broker에 대해 반복합니다.

---

## 3. 롤링 재시작 중 발생할 수 있는 문제 및 고려사항

*   **일시적인 성능 저하 및 지연 시간 증가:** 한 대의 Broker가 중단되면 해당 Broker가 처리하던 부하가 다른 Broker로 분산됩니다. 이로 인해 클러스터 전체의 처리량(Throughput)이 감소하고 메시지 전송/수신 지연 시간이 일시적으로 늘어날 수 있습니다.
*   **Leader Election:** Broker 중단 시 해당 Broker가 Leader였던 파티션들은 다른 ISR Broker 중 하나를 새로운 Leader로 선출합니다. 이 과정에서 매우 짧은 지연이 발생할 수 있습니다.
*   **클라이언트 재연결:** 중단된 Broker와 연결되어 있던 Producer/Consumer 클라이언트는 자동으로 다른 Broker로 재연결을 시도합니다. 대부분의 Kafka 클라이언트는 재시도 로직을 내장하고 있어 자동으로 복구되지만, 일시적인 connection 에러가 발생할 수 있습니다.
*   **네트워크 파티셔닝 또는 추가 장애:** 롤링 재시작 중에 네트워크 문제, 또는 다른 Broker의 예상치 못한 장애 등이 발생하면 클러스터 전체의 서비스 중단으로 이어질 수 있습니다. 따라서 작업 중에는 클러스터 모니터링을 평소보다 강화해야 합니다.
*   **Zookeeper/Kraft Quorum:** 3대 Broker 클러스터에서 한 대가 중단되어도 2대의 Broker가 남아 Quorum을 유지하므로 Kafka 컨트롤러 기능에는 문제가 없습니다. 하지만 2대 이상이 동시에 중단되면 클러스터가 동작하지 않게 됩니다.

---

## 결론

Kafka Broker의 롤링 재시작은 클러스터 HA를 유지하면서 정적 설정을 변경하거나 업그레이드를 수행하는 표준적인 방법입니다. 핵심은 **사전 검증과 각 단계별 철저한 모니터링**입니다. 특히 `replica.fetch.max.bytes` 및 `min.insync.replicas` 설정을 충분히 이해하고 클러스터 상태를 확인한 후 진행해야 합니다.
