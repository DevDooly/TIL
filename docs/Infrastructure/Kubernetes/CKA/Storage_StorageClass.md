# 4.2 StorageClass & 동적 프로비저닝 (Dynamic Provisioning)

**StorageClass**는 관리자가 수동으로 PV를 미리 만들어두지 않아도, 사용자가 PVC를 요청했을 때 백엔드 스토리지(클라우드 디스크, 로컬 볼륨 등)에 **PV를 자동으로 생성(동적 프로비저닝)**해주는 쿠버네티스 리소스입니다.

---

## 1. StorageClass 핵심 필드

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-storage
provisioner: kubernetes.io/no-provisioner  # 프로비저너 종류 (클라우드 드라이버 또는 CSI)
volumeBindingMode: WaitForFirstConsumer    # 볼륨 바인딩 시점
reclaimPolicy: Delete                      # 기본 회수 정책
allowVolumeExpansion: true                 # 볼륨 크기 동적 확장 허용 여부
```

---

## 2. ⚠️ volumeBindingMode의 중요성: Immediate vs WaitForFirstConsumer

| 모드 | 동작 방식 | 주요 사용 처 |
| :--- | :--- | :--- |
| **`Immediate`** (기본값) | PVC가 생성되는 즉시 볼륨과 PV가 프로비저닝되고 바인딩됩니다. | 클라우드 네트워크 스토리지 (EBS 등) |
| **`WaitForFirstConsumer`** | PVC 생성 시 대기하고 있다가, **해당 PVC를 사용하는 파드가 특정 노드에 실제로 스케줄링될 때** 해당 노드의 위치(Topology/Zone)에 맞춰 볼륨을 생성합니다. | 로컬 볼륨, 가용영역(AZ) 종속 디스크 |

> [!NOTE]
> CKA 시험에서 PVC를 만들었는데 파드가 뜨기 전까지 PVC가 `Pending` 상태로 유지되는 경우가 있습니다. 만약 StorageClass의 `volumeBindingMode`가 `WaitForFirstConsumer`라면 이는 정상 동작이며, 파드를 배포하면 즉시 `Bound`로 전환됩니다.

---

## 3. 기본 StorageClass 지정 (Default StorageClass)

클러스터에 여러 StorageClass가 있을 때, PVC에서 `storageClassName`을 명시하지 않아도 자동으로 사용될 기본 스토리지를 지정할 수 있습니다.

```bash
# 기본 StorageClass 확인 (* 표시 여부)
kubectl get sc

# 특정 StorageClass를 기본값으로 지정
kubectl patch storageclass local-storage -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'

# 기본값 해제
kubectl patch storageclass local-storage -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"false"}}}'
```

---

## 4. 동적 프로비저닝을 사용하는 PVC 예제

관리자가 PV를 만들지 않아도, 아래 PVC를 배포하면 `fast-storage` 프로비저너가 알아서 PV를 생성하고 바인딩합니다.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: dynamic-pvc
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: fast-storage
  resources:
    requests:
      storage: 2Gi
```

---

## 💡 CKA 시험 실전 팁

1. **공식 문서 검색어**: `storageclass`
2. 문제에서 "StorageClass를 생성하고 볼륨 바인딩 모드를 WaitForFirstConsumer로 설정하라"는 요구사항이 나오면 공식 문서의 StorageClass 예제에서 `volumeBindingMode` 옵션을 정확히 복사합니다.
3. PVC의 용량을 늘리라는(Volume Expansion) 문제가 나오면:
   - 해당 StorageClass에 `allowVolumeExpansion: true`가 설정되어 있는지 확인
   - `kubectl edit pvc <pvc-name>`에서 `resources.requests.storage`를 원하는 크기로 수정
