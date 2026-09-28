# 3.3 네트워크 정책 (NetworkPolicy)

NetworkPolicy 관점에서 Pod는 기본적으로 ingress·egress가 격리되지 않은 상태입니다. 실제 통신에는 CNI·라우팅·방화벽 등의 조건도 영향을 줍니다. **NetworkPolicy**는 특정 파드로 들어오거나(Ingress) 나가는(Egress) 트래픽을 IP 또는 라벨 셀렉터 기준으로 제한하는 방화벽 규칙입니다.

!!! important

    **NetworkPolicy를 지원하는 네트워크 구현**이 필요합니다. CNI가 있다는 사실만으로 정책 적용을 보장하지 않으므로 전후 통신을 확인합니다.

---

## 1. NetworkPolicy 핵심 문법 구조

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: test-network-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      role: db               # 1. 정책을 적용할 대상 파드
  policyTypes:
  - Ingress                  # 2. 이 예제는 ingress만 제한
  ingress:                   # 3. 들어오는 트래픽 허용 규칙 (화이트리스트)
  - from:
    - podSelector:           # 4. 허용할 출발지 파드
        matchLabels:
          role: frontend
    ports:
    - protocol: TCP
      port: 3306             # 5. 허용할 포트
```

---

## 2. AND와 OR 조건 구분

`from` 절 아래에 `podSelector`와 `namespaceSelector`를 작성할 때 하이픈(`-`)의 위치에 따라 완전히 다른 규칙이 됩니다.

### [OR 조건] 서로 다른 리스트 아이템 (`-`가 각각 있음)

선택한 namespace의 Pod **또는 정책과 같은 namespace**의 `role=monitoring` Pod를 허용합니다. 아래는 `spec` 아래에 넣는 발췌입니다.

```yaml
ingress:
- from:
  - namespaceSelector:
      matchLabels:
        project: internal
  - podSelector:
      matchLabels:
        role: monitoring
```

### [AND 조건] 하나의 리스트 아이템 (`-`가 하나만 있음)

`project=internal` namespace에 속하면서 **동시에** `role=frontend`인 Pod를 선택합니다. 아래는 `spec` 아래에 넣는 발췌입니다.

```yaml
ingress:
- from:
  - namespaceSelector:
      matchLabels:
        project: internal
    podSelector:
      matchLabels:
        role: frontend
```

---

## 3. 실전 필수 시나리오 2가지

### 📝 시나리오 1: 모든 인바운드 트래픽 기본 차단 (Default Deny All Ingress)

namespace의 모든 Pod를 ingress 격리 대상으로 만듭니다. 다른 정책이 허용한 트래픽은 계속 허용됩니다.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: prod
spec:
  podSelector: {} # 네임스페이스 내 전체 파드 선택
  policyTypes:
  - Ingress
```

### 📝 시나리오 2: 특정 백엔드 파드에 특정 프론트엔드 파드의 접근만 허용

`namespace: dev`에서 `app: backend` 라벨을 가진 파드에 같은 namespace의 `app: frontend` Pod가 TCP 80으로 접근하도록 허용합니다. 다른 정책의 허용 경로도 합쳐집니다.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: dev
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 80
```

---

## 4. 실전 검증 명령어

정책은 허용 규칙의 합집합으로 적용됩니다. 출발 파드의 egress와 도착 파드의 ingress가 모두 허용되어야 연결할 수 있습니다. egress를 격리했다면 DNS 질의에 필요한 UDP·TCP 53번 포트도 검토합니다.

정책 적용 전 backend Service의 selector·EndpointSlice·listen 포트와 통신을 확인합니다. 이후 허용/비허용 출발지에서 비교합니다. 테스트 이미지에는 curl이 있어야 합니다.

```bash
# 허용되어야 하는 파드에서 통신 테스트 (성공해야 함)
kubectl exec -it frontend-pod -n dev -- curl -m 3 http://backend-service:80

# 별도 허용 정책이 없는 다른 파드에서 테스트 (연결 실패 예상)
kubectl run test-curl --rm -i --restart=Never --image=curlimages/curl -n dev --command -- curl -m 3 http://backend-service:80
```

---

## 💡 CKA 시험 실전 팁

1. **공식 문서 검색어**: `networkpolicy`
2. 공식 문서의 "Declare Network Policy" 페이지에 나오는 풍부한 예제 YAML을 그대로 복사하여 필요한 라벨과 포트만 수정하세요.
3. 문제를 풀 때 다음 4가지를 체크리스트로 확인합니다:
    - [ ] 올바른 `namespace`에 정책을 만들었는가?
    - [ ] `podSelector`가 보호 대상 파드를 정확히 가리키는가?
    - [ ] `policyTypes`에 `Ingress` 또는 `Egress`를 누락하지 않았는가?
    - [ ] AND 조건(`-` 1개)인지 OR 조건(`-` 2개)인지 문제 지문을 확인했는가?

## 참고 자료

- [Kubernetes: Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
