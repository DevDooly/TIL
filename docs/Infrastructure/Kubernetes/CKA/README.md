# Kubernetes CKA 학습 목차

**CKA (Certified Kubernetes Administrator)** 준비에 필요한 Kubernetes 개념, 실습 명령과 트러블슈팅 절차를 모았다.

공식 출제 영역에 맞춰 문서를 묶었다. 아래 문서에서 다루지 않는 항목은 [보충 학습](#additional-topics)의 공식 문서를 함께 확인한다.

!!! tip "학습 순서"

    [CKA 2주 학습 계획](Study_Plan_2Weeks.md)은 Kubernetes 기초 경험이 있는 사람을 위한 복습 일정이다. 실습에 걸리는 시간에 맞춰 기간을 조정한다.

---

## 📌 CKA 시험 목차 (Table of Contents)

### 0. 시험 안내 및 전략

* **[0. 시험 개요 및 팁 (Exam Overview & Tips)](CKA_Exam_Tips.md)**: 시험 환경(PSI 브라우저), alias, vim 설정, 시간 관리 요령
* **[2주 학습 계획](Study_Plan_2Weeks.md)**: 14일 학습 체크리스트 및 실습 목표

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
* **[2.5 멀티 컨테이너 & 사이드카](Multi_Container_Pods.md)**: Init Container, Native Sidecar Container (1.29 베타, 1.33 정식)

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

## 예제를 실행하기 전에

- 명령은 Linux 실습 호스트의 Bash를 기준으로 한다. `<node-name>`, `<namespace>` 등의 자리표시자는 실제 값으로 바꾼다.
- 작업 호스트, kubeconfig와 네임스페이스를 먼저 확인한다. 예제에 생략된 네임스페이스는 문제 조건에 맞게 `-n`으로 지정한다.
- 같은 이름을 쓰는 대안 예제는 필요한 방식 하나를 선택한다. YAML의 `spec` 등 일부만 보여주는 예제는 완성된 리소스의 해당 위치에 넣는다.
- 리소스 생성 후에는 명령의 성공 여부뿐 아니라 상태·이벤트와 실제 동작을 확인한다.

<a id="additional-topics"></a>

## 보충 학습

[공식 CKA 출제 범위](https://training.linuxfoundation.org/certified-kubernetes-administrator-cka-program-changes/)에는 아래 주제도 포함된다. 이 목차의 문서만으로 전체 범위가 끝나는 것은 아니다.

- **클러스터 구성**: [HA 컨트롤 플레인](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/high-availability/), [컨테이너 런타임과 CRI](https://kubernetes.io/docs/setup/production-environment/container-runtimes/), CNI·CSI 확장 인터페이스의 역할
- **설치 도구**: [Helm 사용법](https://helm.sh/docs/intro/using_helm/), [Kustomize](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/)
- **확장**: [CRD](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)와 [Operator 패턴](../Operator_Pattern.md)
- **워크로드**: [Horizontal Pod Autoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
- **네트워킹**: [Gateway API 실습](https://gateway-api.sigs.k8s.io/guides/)
