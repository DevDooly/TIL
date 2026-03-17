# 1.3 RBAC (Role-Based Access Control)

RBAC은 '누가(Subject)', '어디서(Namespace)', '어떤 권한(Verb)'을 가지고 '어떤 자원(Resource)'에 접근할 수 있는지 결정합니다.

---

## 1. 핵심 리소스 구성

### 1.1 Role & ClusterRole (권한 정의)
*   **Role**: 특정 **네임스페이스** 내의 자원 권한 정의.
*   **ClusterRole**: 클러스터 **전체** 수준의 자원(Node, PV 등) 또는 모든 네임스페이스 권한 정의.

### 1.2 RoleBinding & ClusterRoleBinding (권한 부여)
*   사용자(User), 그룹(Group), 또는 서비스 어카운트(ServiceAccount)에 위에서 만든 Role을 연결합니다.

---

## 2. 실전 명령어 (Imperative)

시험에서는 YAML을 직접 쓰는 것보다 명령어로 생성하는 것이 훨씬 빠릅니다.

### 2.1 Role 생성
```bash
# default 네임스페이스에서 pod을 get, watch, list 할 수 있는 role 생성
kubectl create role pod-reader --verb=get,list,watch --resource=pods
```

### 2.2 RoleBinding 생성
```bash
# jane 이라는 사용자에게 pod-reader 권한 부여
kubectl create rolebinding jane-pod-reader --role=pod-reader --user=jane
```

### 2.3 권한 확인 (Can-I)
설정이 제대로 되었는지 테스트할 때 매우 유용합니다.
```bash
# 내가 현재 pod을 생성할 수 있는지 확인
kubectl auth can-i create pods

# 특정 사용자가 특정 네임스페이스에서 권한이 있는지 대역 확인
kubectl auth can-i list pods --as jane -n default
```
