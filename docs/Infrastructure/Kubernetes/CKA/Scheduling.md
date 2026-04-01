# 2.2 스케줄링 제어 (Scheduling)

특정 파드를 원하는 노드에 배치하거나(Affinity), 반대로 특정 파드가 특정 노드에 배치되지 못하게 막는(Taint) 설정은 CKA 시험의 단골 문제입니다.

---

## 1. Node Selector (가장 단순한 방법)
파드가 특정 라벨이 붙은 노드에만 스케줄링되도록 합니다.

**1. 노드에 라벨 추가**
```bash
kubectl label nodes node01 disktype=ssd
```

**2. 파드 YAML에 적용**
```yaml
spec:
  containers:
  - name: nginx
    image: nginx
  nodeSelector:
    disktype: ssd
```

---

## 2. Node Affinity & Anti-Affinity (상세한 제어)
Node Selector보다 유연한 조건(In, NotIn, Exists 등)과 선호도(반드시 지켜야 함 vs 가능하면 지킴)를 설정할 수 있습니다.

*   `requiredDuringSchedulingIgnoredDuringExecution`: **반드시** 조건을 만족하는 노드에만 배치 (Hard).
*   `preferredDuringSchedulingIgnoredDuringExecution`: 조건을 만족하는 노드를 **선호**하지만, 없으면 다른 곳에 배치 (Soft).

**예제 (disktype이 ssd 또는 nvme인 노드에만 배치):**
```yaml
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: disktype
            operator: In
            values:
            - ssd
            - nvme
```

---

## 3. Taints and Tolerations (오염과 용인)
노드에 '오염(Taint)'을 묻혀두면, 이를 '용인(Toleration)'할 수 있는 파드만 해당 노드에 스케줄링될 수 있습니다. **주로 마스터 노드에 일반 파드가 배포되지 않게 막는 데 사용됩니다.**

### 3.1 노드에 Taint 설정 / 해제
```bash
# Taint 설정 (key=value:effect)
kubectl taint nodes node01 app=blue:NoSchedule

# Taint 해제 (끝에 '-' 추가)
kubectl taint nodes node01 app=blue:NoSchedule-
```

*   **NoSchedule**: Toleration이 없으면 스케줄링하지 않음 (기존 파드는 놔둠).
*   **NoExecute**: Toleration이 없으면 스케줄링 안 함 + 기존에 돌고 있던 파드도 쫓아냄.

### 3.2 파드에 Toleration 설정
`node01`에 설정된 `app=blue:NoSchedule` Taint를 무시하고 배치될 수 있게 합니다.
```yaml
spec:
  tolerations:
  - key: "app"
    operator: "Equal"
    value: "blue"
    effect: "NoSchedule"
```
