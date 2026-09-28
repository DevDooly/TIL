# 4.2 StorageClass와 동적 프로비저닝

StorageClass는 provisioner와 스토리지 정책을 정의한다. 동적 생성에는 설치된 provisioner가 필요하다. `kubernetes.io/no-provisioner`는 동적 프로비저닝을 제공하지 않는다.

## 1. 기존 드라이버와 class 확인

```bash
kubectl get storageclass
kubectl get storageclass <class-name> -o yaml
kubectl get csidriver
```

CSI가 아닌 외부 provisioner도 있으므로 CSIDriver 목록만으로 전체 설치 여부를 판단하지 않는다. 제공된 환경과 controller 상태를 확인한다.

## 2. 동적 프로비저닝용 class

다음은 형식 예제다. `provisioner`와 필요한 `parameters`는 **실제로 설치한 드라이버**의 값으로 바꾼다.

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-storage
provisioner: csi.example.com # 예시: 실제 드라이버로 교체
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Delete
allowVolumeExpansion: true
```

확장·topology 지원 여부도 드라이버마다 다르다. [StorageClass 공식 문서](https://kubernetes.io/docs/concepts/storage/storage-classes/)

## 3. 정적 local 볼륨용 class

다음 class는 관리자가 local PV와 node affinity를 따로 준비할 때 사용한다. PVC를 만들었다고 새 디스크나 PV가 자동 생성되지 않는다.

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-storage
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
```

## 4. 바인딩 시점

| 모드 | 동작 | 확인할 점 |
| :--- | :--- | :--- |
| `Immediate` | PVC 생성 후 바인딩·프로비저닝 시작 | Pod 배치 조건을 반영하지 않아 zone 충돌이 생길 수 있음 |
| `WaitForFirstConsumer` | 소비 Pod의 스케줄링 조건을 고려해 바인딩·프로비저닝 | 소비 Pod, 사용 가능한 PV/드라이버, topology와 자원 조건 필요 |

`WaitForFirstConsumer` PVC는 소비 Pod가 없으면 Pending일 수 있다. Pod를 만들더라도 드라이버·PV·스케줄링 조건이 맞지 않으면 Bound가 되지 않는다. `spec.nodeName`으로 스케줄러를 우회하면 지연 바인딩이 진행되지 않을 수 있으므로 nodeSelector·affinity를 사용한다.

## 5. PVC와 소비 Pod 생성

아래는 2절의 **실제 드라이버로 교체한** `fast-storage`를 사용한다.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: dynamic-pvc
  namespace: default
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: fast-storage
  resources:
    requests:
      storage: 2Gi
```

1. provisioner와 class를 준비한다.
2. PVC를 생성한다.
3. 같은 namespace에 `claimName: dynamic-pvc`를 사용하는 Pod를 생성한다. [Pod 마운트 예제](Storage_PV_PVC.md)를 참고한다.
4. PVC·Pod 상태와 Events를 확인한다.

```bash
kubectl get pvc dynamic-pvc -n default
kubectl describe pvc dynamic-pvc -n default
kubectl get pods -n default -o wide
```

## 6. 기본 class와 볼륨 확장

기본 class는 `storageClassName`을 생략한 **PVC**에 적용된다. `storageClassName: ""`는 class 없는 PV를 요청하는 명시적 설정이다. 기본 class를 바꿀 때는 기존 설정도 확인한다.

```bash
kubectl get sc
kubectl patch storageclass <old-default> -p '{"metadata":{"annotations":{"storageclass.kubernetes.io/is-default-class":"false"}}}'
kubectl patch storageclass <new-default> -p '{"metadata":{"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
```

확장은 드라이버 지원과 `allowVolumeExpansion: true`를 확인한 뒤 PVC의 `spec.resources.requests.storage`를 **늘린다**. PV capacity를 먼저 직접 수정하지 않는다. PVC 이벤트와 컨테이너의 파일시스템 용량까지 확인하며 축소는 지원하지 않는다. [PVC 확장 절차](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#expanding-persistent-volumes-claims)
