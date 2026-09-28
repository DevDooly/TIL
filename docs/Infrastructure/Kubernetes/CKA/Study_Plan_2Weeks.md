# CKA 2주 학습 계획

기본적인 Linux·kubectl 사용 경험이 있는 사람이 하루 1~2시간씩 복습하는 14일 계획이다. 처음 배우는 주제나 복구 실습이 오래 걸리면 기간을 늘린다. 개념 확인 → 실습 → 결과 검증·오답 기록 순서로 진행하며, 모의고사 날은 풀이 2시간 외에 복습 시간을 따로 확보한다.

시험 시간·허용 자료·작업 호스트 지침은 [0. 시험 개요 및 팁](CKA_Exam_Tips.md)을 따른다. 문서 번호는 [CKA 목차](README.md)와 같으며 일자별로 필요한 내용을 묶었다.

## 1주차: 구성과 리소스 관리

### Day 1. 시험 환경과 클러스터 구성

관련 문서: [0. 시험 개요 및 팁](CKA_Exam_Tips.md), [1. 클러스터 아키텍처](Cluster_Architecture.md), [1.1 설치 및 업그레이드](Kubeadm_Install_Upgrade.md)

- [ ] 지정 호스트로 SSH 접속하고 hostname·context·namespace를 확인한다.
- [ ] 기존 alias·자동완성과 `--dry-run=client -o yaml`을 사용해 본다.
- [ ] 런타임·패키지 준비 → init → kubeconfig → CNI → 워커 join → Ready 확인 순서로 실습한다.
- [ ] CRI·CNI·CSI 역할과 추가 컨트롤 플레인의 HA 조건을 구분한다.

### Day 2. 백업·복원과 업그레이드

관련 문서: [1.1 설치 및 업그레이드](Kubeadm_Install_Upgrade.md), [1.2 etcd 백업 및 복원](ETCD_Backup_Restore.md)

- [ ] 변경 전에 etcd snapshot을 저장하고 상태를 확인한다.
- [ ] 단일 멤버 실습에서 API server·etcd 중지 → 새 경로 복원 → 설정 확인 → etcd·API server 재기동 → 리소스 검증을 진행한다.
- [ ] 첫 컨트롤 플레인: kubeadm 갱신 → `upgrade plan` → `upgrade apply` → drain → kubelet 갱신·재시작 → Ready 확인 → uncordon.
- [ ] 추가 컨트롤 플레인과 워커: kubeadm 갱신 → `upgrade node` → drain → kubelet 갱신·재시작 → Ready 확인 → uncordon.
- [ ] 첫 컨트롤 플레인 → 나머지 컨트롤 플레인 → 워커 순서와 목표 버전의 패키지 저장소를 확인한다.

### Day 3. 권한·워크로드·설정

관련 문서: [1.3 RBAC](RBAC_Authorization.md), [2.1 워크로드](Workloads.md), [2.4 ConfigMap과 Secret](ConfigMaps_Secrets.md)

- [ ] namespace·ServiceAccount → Role → RoleBinding → `auth can-i` 순서로 검증한다.
- [ ] Deployment 생성 → 이미지 변경 → rollout 확인 → rollback을 실습한다.
- [ ] ConfigMap·Secret을 먼저 만든 뒤 Pod의 env·volume으로 연결한다.
- [ ] 환경변수와 볼륨 마운트의 갱신 방식 차이를 확인한다.

### Day 4. 스케줄링·리소스·사이드카

관련 문서: [2.2 스케줄링](Scheduling.md), [2.3 리소스 제한](Resource_Limits.md), [2.5 멀티 컨테이너](Multi_Container_Pods.md)

- [ ] nodeSelector·required/preferred affinity와 taint/toleration을 구분한다.
- [ ] request·limit·LimitRange를 적용하고 Pending·OOMKilled를 비교한다.
- [ ] 일반 init container의 완료와 native sidecar의 시작 조건을 구분한다.
- [ ] 공유 로그 파일을 먼저 준비하고 `logs -c`로 확인한다.

### Day 5. Service·Ingress·Gateway API

관련 문서: [3.1 Service](Services.md), [3.2 Ingress](Ingress.md)

- [ ] 실제 listen 포트·라벨을 확인한 뒤 Service를 만든다.
- [ ] selector·targetPort·EndpointSlice·실제 요청 순서로 검증한다.
- [ ] IngressClass와 controller를 확인한 뒤 host/path 규칙을 적용한다.
- [ ] [Gateway API 가이드](https://gateway-api.sigs.k8s.io/guides/)로 GatewayClass → Gateway → HTTPRoute의 연결과 상태 조건을 확인한다.

### Day 6. NetworkPolicy

관련 문서: [3.3 NetworkPolicy](Network_Policy.md)

- [ ] 정책 적용 전 Service가 정상 통신하는지 확인한다.
- [ ] CNI의 정책 지원 여부와 대상 namespace·Pod 라벨을 확인한다.
- [ ] ingress·egress, selector의 AND/OR, 여러 정책의 허용 규칙 합집합을 구분한다.
- [ ] 허용·비허용 출발지에서 각각 테스트하고 DNS 차단과 목적지 포트 차단을 구분한다.

### Day 7. PV·PVC·StorageClass

관련 문서: [4.1 PV와 PVC](Storage_PV_PVC.md), [4.2 StorageClass](Storage_StorageClass.md)

- [ ] 정적 구성은 PV → PVC → 소비 Pod 순서로 연결한다.
- [ ] 동적 구성은 provisioner → StorageClass → PVC → 소비 Pod를 확인한다.
- [ ] `WaitForFirstConsumer`는 소비 Pod의 스케줄링 조건까지 준비한 뒤 바인딩을 확인한다.
- [ ] accessModes·class·용량·node affinity·회수 정책과 확장 조건을 확인한다.

## 2주차: 장애 진단과 모의고사

### Day 8. Pod 진단과 보충 범위

관련 문서: [5.1 Pod 트러블슈팅](Troubleshooting_Pods.md), [목차의 보충 학습](README.md#additional-topics)

- [ ] Pending·ImagePullBackOff·CrashLoopBackOff의 상태·Events·현재/이전 로그를 확인한다.
- [ ] startup·readiness·liveness probe의 영향을 구분한다.
- [ ] 관리되는 Pod는 Deployment 등 상위 리소스의 template을 수정한다.
- [ ] HPA, Helm·Kustomize, CRD·Operator 중 부족한 주제를 별도 실습한다. 하루에 끝내기 어렵다면 이 구간을 연장한다.

### Day 9. 컨트롤 플레인 진단

관련 문서: [5.2 컨트롤 플레인 트러블슈팅](Troubleshooting_Cluster.md)

- [ ] endpoint·접속 설정 → kubelet·런타임 → 컨테이너 로그 → manifest 순서로 확인한다.
- [ ] manifest를 감시 디렉터리 밖에 백업하고 경로·인자·인증서 오류를 수정한다.
- [ ] kubelet의 변경 감지 후 API·시스템 Pod·워크로드를 검증한다.

### Day 10. 노드·DNS·CNI 진단

관련 문서: [5.3 노드와 네트워크 트러블슈팅](Troubleshooting_Nodes_Network.md)

- [ ] Node Conditions와 이벤트를 읽고 해당 노드로 접속한다.
- [ ] kubelet·런타임 로그와 설정을 확인한 뒤 필요한 수정·재시작만 한다.
- [ ] Pod DNS 설정 → DNS Service·EndpointSlice → CoreDNS 로그 → CNI·정책 순서로 범위를 좁힌다.
- [ ] 복구 후 Ready와 실제 통신을 확인한다.

### Day 11. 첫 모의고사

관련 문서: [Killer.sh 활용](Killer_sh_Strategy.md)

- [ ] 복습할 시간을 확보한 뒤 첫 세션을 활성화한다.
- [ ] 2시간 동안 해설을 보지 않고 허용 자료를 사용해 푼다.
- [ ] 호스트·namespace 확인과 적용 후 검증에 걸린 시간을 기록한다.

### Day 12. 오답과 데이터 추출

관련 문서: [JSONPath 치트시트](JSONPath_Cheatsheet.md)

- [ ] 실패한 명령·잘못 읽은 조건·누락한 검증을 구분하고 다시 푼다.
- [ ] JSONPath·custom-columns·정렬 결과를 지정 파일에 저장하고 확인한다.
- [ ] 접근 기간 안에 필요한 재실습을 마친다. 세션의 36시간은 연속으로 흐른다.

### Day 13. 두 번째 모의고사

관련 문서: [Killer.sh 활용](Killer_sh_Strategy.md)

- [ ] 두 번째 세션의 문제 세트와 사용 가능 시간을 확인한다.
- [ ] 다시 2시간을 측정하고 새 문제에도 같은 작업·검증 절차를 적용한다.
- [ ] 남은 취약 유형을 실습한다. 특정 유형 세 개의 고정 배점을 가정하지 않는다.

### Day 14. 최종 복습과 응시 준비

관련 문서: [0. 시험 개요 및 팁](CKA_Exam_Tips.md), [응시 체크리스트](Killer_sh_Strategy.md)

- [ ] 공식 신분증·시스템 검사·시험 공간 요건을 확인한다.
- [ ] 자주 틀린 명령과 업그레이드·복원 순서를 다시 설명해 본다.
- [ ] 허용 문서 위치와 작업 호스트 이동 방법을 확인한다.
- [ ] 시험 예약 시간과 접속 절차를 확인한다.
