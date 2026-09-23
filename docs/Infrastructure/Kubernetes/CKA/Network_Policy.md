# 3.3 네트워크 정책 (NetworkPolicy)

쿠버네티스는 기본적으로 **모든 파드 간의 네트워크 통신이 제한 없이 열려 있습니다(Default Allow)**. **NetworkPolicy**는 특정 파드로 들어오거나(Ingress) 나가는(Egress) 트래픽을 IP 또는 라벨 셀렉터 기준으로 제한하는 방화벽 규칙입니다.

> [!IMPORTANT]
> CKA 시험에서 **단골 출제되며 배점도 매우 높고 가장 실수가 잦은 영역**입니다. CNI 플러그인(Calico, Cilium 등)이 설치되어 있어야 실제로 패킷이 차단됩니다.

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
  - Ingress                  # 2. 적용할 트래픽 방향 (Ingress 또는 Egress)
  - Egress
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

## 2. ⚠️ 시험 최대 함정: AND vs OR 조건 구분

`from` 절 아래에 `podSelector`와 `namespaceSelector`를 작성할 때 하이픈(`-`)의 위치에 따라 완전히 다른 규칙이 됩니다.

### [OR 조건] 서로 다른 리스트 아이템 (`-`가 각각 있음)
특정 네임스페이스의 파드 **또는** 특정 라벨의 파드로부터의 접근 허용
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
`project=internal` 네임스페이스에 속해 있으면서 **동시에** `role=frontend` 라벨을 가진 파드만 허용
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
네임스페이스 내의 모든 파드가 들어오는 트래픽을 받지 못하도록 격리합니다.
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
`namespace: dev`에서 `app: backend` 라벨을 가진 파드에 오직 `app: frontend` 파드가 80 포트로 접근하는 것만 허용:
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

네트워크 정책을 적용한 후 실제로 차단/허용되는지 반드시 테스트해야 합니다.
```bash
# 허용되어야 하는 파드에서 통신 테스트 (성공해야 함)
kubectl exec -it frontend-pod -n dev -- curl -m 3 http://backend-service:80

# 차단되어야 하는 다른 파드에서 테스트 (타임아웃 발생해야 함)
kubectl run test-curl --rm -it --image=curlimages/curl -n dev -- curl -m 3 http://backend-service:80
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
