# 1.3 RBAC (Role-Based Access Control)

RBAC은 **'누가(Subject)'**, **'어디서(Namespace)'**, **'어떤 권한(Verb)'**을 가지고 **'어떤 자원(Resource)'**에 접근할 수 있는지 결정하는 쿠버네티스의 핵심 보안 메커니즘입니다.

---

## 1. 핵심 리소스 구성

### 1.1 Role & ClusterRole (권한의 "내용" 정의)

* **Role**: **특정 네임스페이스** 내에 존재하는 자원(Pod, Service, Secret 등)에 대한 권한을 정의합니다.
* **ClusterRole**: **클러스터 전체** 수준의 자원(Node, PV 등)에 대한 권한을 정의하거나, 모든 네임스페이스에 걸쳐 특정 자원에 접근할 수 있는 권한을 정의합니다.

### 1.2 RoleBinding & ClusterRoleBinding (권한 "부여")

* 만들어진 Role이나 ClusterRole을 실제 **사용자(User)**, **그룹(Group)**, 또는 **서비스 어카운트(ServiceAccount)**에 연결(Bind)해 주는 역할입니다.

---

## 2. CKA 실전 시나리오 및 예제 (명령어 위주)

CKA 시험에서는 YAML 파일을 처음부터 작성하면 시간이 부족합니다. 반드시 `kubectl create` 명령어를 활용하여 뼈대를 만들거나 즉시 생성해야 합니다.

### 📝 시나리오 1: 특정 네임스페이스의 사용자 권한 부여
**요구사항**: `dev` 네임스페이스에서 사용자 `john`이 Pod를 조회(get, list, watch)만 할 수 있도록 설정하시오.

1. **Role 생성**: `dev` 네임스페이스에 `pod-reader`라는 Role을 만듭니다.
    ```bash
    kubectl create role pod-reader --verb=get,list,watch --resource=pods -n dev
    ```

2. **RoleBinding 생성**: 방금 만든 `pod-reader` Role을 사용자 `john`에게 연결합니다.
    ```bash
    kubectl create rolebinding john-pod-reader --role=pod-reader --user=john -n dev
    ```

3. **검증 (Can-I)**: `john`의 권한으로 조회가 가능한지 확인합니다.
    ```bash
    # 성공해야 함 (yes)
    kubectl auth can-i get pods --as john -n dev
    
    # 실패해야 함 (no) - 삭제 권한은 주지 않았으므로
    kubectl auth can-i delete pods --as john -n dev
    ```

### 📝 시나리오 2: 서비스 어카운트(ServiceAccount)에 권한 부여
**요구사항**: `app-team` 네임스페이스에 `backend-sa`라는 서비스 어카운트를 만들고, 이 계정이 Deployment를 생성, 삭제, 수정할 수 있는 권한을 부여하시오.

1. **ServiceAccount 생성**:
    ```bash
    kubectl create sa backend-sa -n app-team
    ```

2. **Role 생성**: (복수 자원 지정 가능)
    ```bash
    kubectl create role deploy-admin --verb=create,delete,update,patch --resource=deployments -n app-team
    ```

3. **RoleBinding 생성**: 이번에는 `--user`가 아닌 `--serviceaccount`를 사용합니다. (형식: `네임스페이스:SA이름`)
    ```bash
    kubectl create rolebinding backend-sa-binding --role=deploy-admin --serviceaccount=app-team:backend-sa -n app-team
    ```

### 📝 시나리오 3: 클러스터 전체 권한 부여 (ClusterRole)
**요구사항**: 사용자 `admin-user`가 클러스터 내의 모든 노드(Node) 목록을 조회할 수 있도록 설정하시오. (Node는 네임스페이스에 속하지 않는 클러스터 자원입니다.)

1. **ClusterRole 생성**: (`-n` 옵션이 들어가지 않습니다)
    ```bash
    kubectl create clusterrole node-viewer --verb=get,list,watch --resource=nodes
    ```

2. **ClusterRoleBinding 생성**:
    ```bash
    kubectl create clusterrolebinding admin-node-binding --clusterrole=node-viewer --user=admin-user
    ```

---

## 3. 꿀팁: 여러 자원에 여러 권한 한 번에 주기

명령어 한 줄로 다양한 조합을 만들 수 있습니다.
```bash
# Services 와 ConfigMaps 에 대해 모든 권한(*) 부여
kubectl create role full-access --verb=* --resource=services,configmaps -n default
```