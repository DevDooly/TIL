# 1. 클러스터 아키텍처 및 컴포넌트

Kubernetes 클러스터는 시스템을 관리하는 **Control Plane (Master Node)**과 실제 컨테이너가 실행되는 **Worker Node**로 구성됩니다.

---

## 1. 컨트롤 플레인 컴포넌트 (Control Plane Components)

클러스터 전체에 대한 결정(예: 스케줄링)을 내리고 클러스터 이벤트를 감지 및 대응합니다.

### 1.1 kube-apiserver

* **역할**: Kubernetes API를 노출하는 컨트롤 플레인의 프론트엔드입니다. 모든 컴포넌트 간의 통신은 API 서버를 거칩니다.
* **특징**: 수평적으로 확장 가능하도록 설계되었습니다.

### 1.2 etcd

* **역할**: 모든 클러스터 데이터를 담는 **Key-Value 저장소**입니다. (클러스터의 '뇌' 역할)
* **중요**: CKA 시험에서 백업 및 복원 문제가 반드시 출제되는 핵심 컴포넌트입니다.

### 1.3 kube-scheduler

* **역할**: 새로운 Pod가 생성될 때, 어느 노드에 배치할지 결정합니다.
* **결정 기준**: 리소스 요구사항, 정책, 하드웨어/소프트웨어 제약 등.

### 1.4 kube-controller-manager

* **역할**: 클러스터의 상태를 관찰하며, 원하는 상태(Desired State)와 현재 상태(Current State)를 일치시키는 다양한 컨트롤러를 실행합니다.
* **예**: Node Controller, Replication Controller, Endpoint Controller 등.

---

## 2. 노드 컴포넌트 (Node Components)

모든 노드에서 실행되며 런타임 환경을 유지하고 Pod를 관리합니다.

### 2.1 kubelet

* **역할**: 클러스터의 각 노드에서 실행되는 에이전트입니다. Pod 내의 컨테이너들이 정상적으로 실행되고 있는지 관리합니다.
* **중요**: 노드가 `NotReady` 상태일 때 가장 먼저 점검해야 할 컴포넌트입니다.

### 2.2 kube-proxy

* **역할**: 각 노드에서 실행되는 네트워크 프록시로, 서비스(Service) 개념을 구현합니다.
* **동작**: 노드에 네트워크 규칙을 유지하여 내부/외부 통신이 가능하게 합니다.

### 2.3 Container Runtime (CRI)

* **역할**: 컨테이너 실행을 직접 담당하는 소프트웨어입니다.
* **예**: Docker(현재는 containerd를 주로 사용), CRI-O 등.

---

## 3. 핵심 아키텍처 요약도

```mermaid
graph LR
    subgraph Control Plane
        API[kube-apiserver]
        ETCD[(etcd)]
        SCH[kube-scheduler]
        CM[kube-controller-manager]
        API --- ETCD
        API --- SCH
        API --- CM
    end

    subgraph Worker Node
        KLT[kubelet]
        KPR[kube-proxy]
        CRT[Container Runtime]
        KLT --- CRT
    end

    User(사용자/kubectl) --> API
    KLT --- API
```
