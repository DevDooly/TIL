# Hadoop NameNode High Availability (HA)

Hadoop 2.0부터 도입된 NameNode High Availability(HA)는 단일 실패 지점(SPOF, Single Point of Failure)이었던 기존 NameNode 아키텍처의 한계를 극복하기 위해 설계되었습니다.

## 1. 아키텍처 개요

HA 클러스터에서는 두 개의 NameNode가 존재합니다:
*   **Active NameNode:** 클라이언트의 모든 요청을 처리합니다.
*   **Standby NameNode:** Active 노드의 상태를 지속적으로 동기화하며, 장애 발생 시 즉시 Active 역할을 인계받을(Failover) 준비를 합니다.

이 두 노드 간의 상태 동기화를 위해 **Quorum Journal Manager (QJM)** 방식을 주로 사용합니다.

## 2. Quorum Journal Manager (QJM)

Active NameNode와 Standby NameNode는 **JournalNode** 그룹을 공유합니다.
*   Active 노드는 네임스페이스 변경 로그(EditLog)를 JournalNode 그룹에 씁니다.
*   Standby 노드는 JournalNode 그룹에서 이 로그를 지속적으로 읽어 자신의 상태를 동기화합니다.

### 왜 JournalNode는 홀수여야 하는가? (Quorum Algorithm)
분산 시스템의 합의 알고리즘(Paxos, Raft 등)에 기반하여, 데이터의 일관성을 보장하기 위해 **과반수(Majority)**의 동의가 필요합니다.

*   **쓰기 성공 조건:** 전체 N개의 JournalNode 중 `(N/2) + 1`개 이상의 노드에 성공적으로 써야 함.
*   **홀수 구성의 장점:**
    *   **3대 구성:** 1대 실패 허용 (2대 생존 시 동작)
    *   **4대 구성:** 1대 실패 허용 (3대 생존 시 동작, 2대 실패 시 과반수 미달로 중단)
    *   **결론:** 짝수(4대)로 구성해도 홀수(3대)와 허용 가능한 장애 노드 수(Fault Tolerance)가 동일하므로, 비용 효율성 측면에서 **홀수(3, 5, 7...)** 구성을 권장합니다.
    *   "Split-Brain" (두 NameNode가 동시에 Active가 되려는 상황) 방지를 위해서도 과반수 투표가 필수적입니다.

## 3. Zookeeper Failover Controller (ZKFC)

자동 장애 조치(Automatic Failover)를 위해 각 NameNode 머신에는 **ZKFC**라는 별도의 데몬이 실행됩니다.
*   **Health Monitoring:** 로컬 NameNode의 상태를 주기적으로 체크합니다.
*   **Session Management:** Zookeeper와 세션을 유지하며, Active Lock(znode)을 점유하려고 시도합니다.
*   **ZooKeeper의 역할:**
    *   Active NameNode가 응답하지 않으면 세션이 만료되고 Lock이 해제됩니다.
    *   Standby 측의 ZKFC가 이를 감지하고 Lock을 획득하여 자신의 NameNode를 Active로 승격시킵니다.

## 4. 참고 자료 및 모범 사례 (Best Practices)
*   **JournalNode 배치:** 각기 다른 물리적 머신 또는 랙(Rack)에 분산 배치하여 하드웨어 장애에 대비해야 합니다.
*   **Fencing:** Split-Brain 상황에서 기존 Active 노드가 멈추지 않고 오동작하여 데이터를 오염시키는 것을 막기 위해, SSH를 통해 기존 Active 노드를 강제 종료(Kill)하는 **STONITH (Shoot The Other Node In The Head)** 설정을 반드시 해야 합니다.
*   **Observer NameNode (Hadoop 3.0+):** 읽기 성능 향상을 위해 도입된 개념으로, Standby와 유사하지만 읽기 요청만을 처리하여 부하를 분산시킵니다. (HA 구성 원리는 유사함)

## 요약
NameNode의 안정성을 위해 Active/Standby 구성을 하며, 이들의 뇌(Brain) 역할을 하는 EditLog 공유 저장소로 **JournalNode**를 사용합니다. 데이터 무결성과 합의를 위해 JournalNode는 **홀수 개(최소 3개)**로 구성하는 것이 표준입니다.
