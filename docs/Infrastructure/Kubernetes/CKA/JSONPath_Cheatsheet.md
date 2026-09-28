# 부록: JSONPath 및 명령형 커맨드 치트시트

클러스터 리소스에서 필요한 정보를 추출하고 지정된 파일에 저장하는 예제입니다. `kubectl`의 `-o jsonpath`와 `custom-columns`, `--sort-by`를 사용해 필요한 필드를 추출하고 결과를 검증합니다. 아래 셸 예제는 Bash 기준입니다.

---

## 1. JSONPath 핵심 문법 요약

| 문법 | 설명 | 예시 |
| :--- | :--- | :--- |
| `$` | 루트 오브젝트 | `$` |
| `.` | 하위 프로퍼티 접근 | `.metadata.name` |
| `[]` | 배열 인덱스 접근 | `.items[0]` |
| `[*]` | 배열의 모든 원소 순회 | `.items[*].metadata.name` |
| `?()` | 조건 필터 표현식 | `[?(@.type=="InternalIP")]` |
| `\n` | 줄바꿈 추가 | `{"\n"}` |

---

## 2. JSONPath 실전 예제

### 2.1 모든 노드의 이름과 내부 IP 추출

```bash
# 단일 노드 또는 모든 노드의 Internal IP
kubectl get nodes -o jsonpath='{.items[*].status.addresses[?(@.type=="InternalIP")].address}'

# 줄바꿈과 함께 출력
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.addresses[?(@.type=="InternalIP")].address}{"\n"}{end}'
```

### 2.2 특정 네임스페이스의 모든 파드 이름 추출

```bash
kubectl get pods -n kube-system -o jsonpath='{.items[*].metadata.name}'
```

### 2.3 특정 파드의 컨테이너 이미지 목록 추출

```bash
kubectl get pod my-pod -o jsonpath='{.spec.containers[*].image}'
```

### 2.4 파드가 실행 중인 노드 이름 추출

```bash
kubectl get pod my-pod -o jsonpath='{.spec.nodeName}'
```

---

## 3. 정렬 (`--sort-by`) 활용

특정 필드를 기준으로 오름차순 정렬하여 출력합니다.

```bash
# 생성 시간(CreationTimestamp) 기준으로 파드 정렬
kubectl get pods --sort-by=.metadata.creationTimestamp

# 노드 이름 기준으로 정렬
kubectl get nodes --sort-by=.metadata.name
```

---

## 4. 커스텀 컬럼 (`-o custom-columns`)

원하는 헤더 이름과 필드를 표 형태로 깔끔하게 표시합니다.

```bash
kubectl get pods -o custom-columns=NAME:.metadata.name,NODE:.spec.nodeName,STATUS:.status.phase
```

---

## 5. 실전 명령형(Imperative) 커맨드 치트키

YAML 뼈대를 빠르게 생성하는 단축 명령어 모음입니다.

```bash
export do="--dry-run=client -o yaml"

# 1. Pod YAML 생성
kubectl run nginx --image=nginx $do > pod.yaml

# 2. Deployment 생성
kubectl create deployment web --image=nginx --replicas=3 $do > deploy.yaml

# 3. Service 생성 (ClusterIP)
kubectl create service clusterip web --tcp=80:80 $do > svc.yaml

# 4. ConfigMap 생성
kubectl create cm my-config --from-literal=key1=value1 $do > cm.yaml

# 5. Job & CronJob 생성
kubectl create job my-job --image=busybox $do -- date > job.yaml
kubectl create cronjob my-cron --image=busybox --schedule="*/5 * * * *" $do -- date > cronjob.yaml

# 6. ServiceAccount 생성
kubectl create sa my-sa -n dev $do > sa.yaml
```

위 명령은 YAML 파일만 생성합니다. 리소스를 배포하려면 파일을 확인하고 `kubectl apply -f <파일명>`을 실행합니다. `dev` 네임스페이스가 없다면 ServiceAccount를 적용하기 전에 생성합니다. `kubectl expose deployment`는 기존 Deployment가 필요하므로 이 예제에서는 독립적인 `create service`를 사용했습니다.

---

## 💡 CKA 시험 실전 팁

1. JSONPath 경로가 잘 기억나지 않으면 우선 **`-o yaml`**이나 **`-o json`**으로 출력한 뒤 구조를 확인하세요:

    ```bash
    kubectl get node <node-name> -o yaml | grep -A 5 addresses
    ```

2. 파일로 저장하라는 요구가 있을 때는 끝에 **`> /opt/result.txt`** 리다이렉트를 붙인 후, 반드시 **`cat /opt/result.txt`**로 결과를 육안 검증하세요.

## 참고 자료

- [Kubernetes: JSONPath Support](https://kubernetes.io/docs/reference/kubectl/jsonpath/)
