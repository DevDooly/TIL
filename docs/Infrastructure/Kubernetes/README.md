# ☸️ Kubernetes (CKA 준비)

이 섹션은 **CKA (Certified Kubernetes Administrator)** 시험 준비를 위해 Kubernetes의 핵심 개념과 실습 명령어, 트러블슈팅 방법들을 정리하는 공간입니다. 

실제 CKA 시험의 공식 도메인(출제 영역)에 맞추어 목차를 구성했습니다. 앞으로 이 목차를 기반으로 하위 문서들을 하나씩 채워나갈 예정입니다.

---

## 📌 CKA 시험 목차 (Table of Contents)

### 0. 시험 개요 및 팁 (Exam Overview & Tips)

* CKA 시험 환경 및 유의사항
* 필수 `kubectl` 단축어(Alias) 및 자동완성 설정
* Vim 에디터 설정 팁

### 1. 클러스터 아키텍처, 설치 및 구성 (Cluster Architecture, Installation & Configuration) - 25%

* Kubernetes 컴포넌트 아키텍처 (kube-apiserver, etcd, kubelet 등)
* `kubeadm`을 이용한 클러스터 설치 및 업그레이드
* ETCD 백업(Backup) 및 복원(Restore)
* RBAC (Role-Based Access Control)을 이용한 권한 제어

### 2. 워크로드 및 스케줄링 (Workloads & Scheduling) - 15%

* Pod, ReplicaSet, Deployment의 이해 및 스케일링
* DaemonSet, StatefulSet, Job, CronJob
* 스케줄링 제어 1: Node Selector, Node Affinity
* 스케줄링 제어 2: Taints and Tolerations
* 리소스 제한 (Requests & Limits) 및 LimitRange

### 3. 서비스 및 네트워킹 (Services & Networking) - 20%

* 네트워크 기본 개념 (Pod Network, CNI)
* Service (ClusterIP, NodePort, LoadBalancer)
* Ingress 리소스 설정 및 Ingress Controller
* Network Policy (네트워크 정책)를 이용한 파드 간 통신 제어
* CoreDNS 디버깅

### 4. 스토리지 (Storage) - 10%

* Volume 개념 및 emptyDir, hostPath
* Persistent Volume (PV) 및 Persistent Volume Claim (PVC)
* StorageClass (동적 프로비저닝)

### 5. 트러블슈팅 (Troubleshooting) - 30%

* 클러스터 및 노드 장애 해결 (kubelet 상태 확인 등)
* 컨트롤 플레인 장애 해결
* 애플리케이션(Pod) 장애 해결 및 로그 확인 (`kubectl logs`, `describe`)
* 네트워크 장애 해결

---
*💡 이 목차는 시험 준비 과정에서 필요에 따라 자유롭게 수정 및 확장될 수 있습니다.*
