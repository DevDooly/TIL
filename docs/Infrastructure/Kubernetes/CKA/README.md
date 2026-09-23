# ☸️ Kubernetes (CKA 준비)

이 섹션은 **CKA (Certified Kubernetes Administrator)** 시험 준비를 위해 Kubernetes의 핵심 개념과 실습 명령어, 트러블슈팅 방법들을 정리하는 공간입니다. 

실제 CKA 시험의 공식 도메인(출제 영역)에 맞추어 목차를 구성했습니다.

> [!TIP]
> 2주간 하루 1~2시간씩 단기 집중하여 자격증을 취득할 수 있도록 정리된 **[📅 CKA 2주 단기 완성 로드맵](Study_Plan_2Weeks.md)**을 먼저 확인하세요!

---

## 📌 CKA 시험 목차 (Table of Contents)

### 0. 시험 안내 및 전략

* **[0. 시험 개요 및 팁 (Exam Overview & Tips)](CKA_Exam_Tips.md)**: 시험 환경(PSI 브라우저), alias, vim 설정, 시간 관리 요령
* **[📅 2주 단기 완성 로드맵 (하루 1~2시간)](Study_Plan_2Weeks.md)**: 14일차 일일 학습 체크리스트 및 실습 목표

### 1. 클러스터 아키텍처, 설치 및 구성 (Cluster Architecture, Installation & Configuration) - 25%

* **[1. 클러스터 아키텍처 및 컴포넌트](Cluster_Architecture.md)**: Control Plane & Worker Node 컴포넌트 역할
* **[1.1 Kubeadm 클러스터 설치 및 업그레이드](Kubeadm_Install_Upgrade.md)**: 클러스터 초기화(init), 워커 조인(join), drain/uncordon 및 버전 업그레이드
* **[1.2 ETCD 백업 및 복원](ETCD_Backup_Restore.md)**: etcd 3.6 기준 `etcdctl`(백업)과 `etcdutl`(복원) 분리 운영 실습
* **[1.3 RBAC (Role-Based Access Control)](RBAC_Authorization.md)**: Role, ClusterRole, RoleBinding 및 `can-i` 권한 검증

### 2. 워크로드 및 스케줄링 (Workloads & Scheduling) - 15%

* **[2.1 워크로드 (Pod, Deployment, DaemonSet 등)](Workloads.md)**: 파드 생성, 디플로이먼트 롤아웃/롤백/스케일링
* **[2.2 스케줄링 제어 (Scheduling)](Scheduling.md)**: nodeSelector, Node Affinity, Taints & Tolerations
* **[2.3 리소스 제한 (Requests & Limits)](Resource_Limits.md)**: requests/limits, OOMKilled, LimitRange
* **[2.4 설정 관리 (ConfigMaps & Secrets)](ConfigMaps_Secrets.md)**: ENV 주입, envFrom, Volume 마운트
* **[2.5 멀티 컨테이너 & 사이드카](Multi_Container_Pods.md)**: Init Container, K8s 1.29+ Native Sidecar Container

### 3. 서비스 및 네트워킹 (Services & Networking) - 20%

* **[3.1 서비스 네트워킹 (Services)](Services.md)**: ClusterIP, NodePort, LoadBalancer, 포트포워딩 및 엔드포인트
* **[3.2 인그레스 라우팅 (Ingress)](Ingress.md)**: Ingress Controller, Ingress 리소스 호스트/경로 라우팅
* **[3.3 네트워크 정책 (NetworkPolicy)](Network_Policy.md)**: podSelector, namespaceSelector, Ingress/Egress 트래픽 격리

### 4. 스토리지 (Storage) - 10%

* **[4.1 PV & PVC 스토리지 (Persistent Volumes & Claims)](Storage_PV_PVC.md)**: PV, PVC 바인딩, AccessModes, ReclaimPolicy, Pod 마운트
* **[4.2 StorageClass & 동적 프로비저닝](Storage_StorageClass.md)**: 프로비저너, volumeBindingMode(WaitForFirstConsumer)

### 5. 트러블슈팅 (Troubleshooting) - 30%

* **[5.1 파드 트러블슈팅 (Pod & Application)](Troubleshooting_Pods.md)**: CrashLoopBackOff, ImagePullBackOff, Pending, Probe 오류
* **[5.2 컨트롤 플레인 트러블슈팅 (Control Plane)](Troubleshooting_Cluster.md)**: Static Pods, kube-apiserver 로그 분석, 복구 절차
* **[5.3 노드 및 네트워크 트러블슈팅 (Node & Network)](Troubleshooting_Nodes_Network.md)**: Worker Node NotReady, kubelet systemd, CoreDNS 장애

### 6. 부록 (Appendix)

* **[부록: JSONPath 및 명령형 치트시트](JSONPath_Cheatsheet.md)**: jsonpath 필터링, custom-columns, --sort-by, 필수 단축키
* **[부록: Killer.sh 모의고사 공략 및 시험 체크리스트](Killer_sh_Strategy.md)**: 2회 세션 활용법, 타임어택 전략, 응시 환경 체크리스트
