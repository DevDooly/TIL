# 2.3 리소스 제한 (Requests & Limits)

클러스터의 자원(CPU, Memory)을 안정적으로 운영하기 위해 파드가 사용할 리소스의 최소 요구량과 최대 제한량을 설정합니다.

---

## 1. Requests와 Limits의 차이

파드 내부의 컨테이너 스펙(spec)에 정의합니다.

* **Requests (요청량)**:
    * 스케줄링에 사용하는 **자원 요청량**. CPU 경합 시 배분에도 영향을 주며 실제 사용량 상한은 아닙니다.
    * 스케줄러는 실제 순간 사용량이 아니라 노드 allocatable과 이미 배치된 파드들의 requests로 수용 가능성을 판단합니다.
* **Limits (제한량)**:
    * 컨테이너가 사용할 수 있는 **최대 자원량**.
    * **CPU**: 한도를 넘게 쓰려고 하면 스로틀링(Throttling)이 발생하여 느려집니다. (파드가 죽지는 않음)
    * **Memory**: 메모리 압력으로 컨테이너 프로세스가 **OOMKilled**될 수 있습니다. 재시작 여부는 restartPolicy 등에 따르며 Pod 전체가 항상 삭제되는 것은 아닙니다.

---

## 2. YAML 적용 예제

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: resource-demo
spec:
  containers:
  - name: my-app
    image: nginx
    resources:
      requests:
        memory: "256Mi"
        cpu: "250m" # 0.25 코어
      limits:
        memory: "512Mi"
        cpu: "500m" # 0.5 코어
```

---

## 3. LimitRange (네임스페이스 기본값 설정)

개발자가 파드를 만들 때 `requests`나 `limits`를 적지 않고 배포하는 경우를 대비해, 특정 네임스페이스에 **기본 할당량 및 제한 범위(최소/최대)**를 강제하는 정책입니다.

```yaml
# limit-range.yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: mem-limit-range
  namespace: default
spec:
  limits:
  - default: # 파드 생성 시 limits를 적지 않으면 이 값이 기본 적용됨
      memory: 512Mi
    defaultRequest: # 파드 생성 시 requests를 적지 않으면 이 값이 기본 적용됨
      memory: 256Mi
    type: Container
```

LimitRange는 생성 시 기본값과 제한을 적용합니다. 새로 만들거나 수정해도 기존 파드의 requests·limits를 소급 변경하지 않습니다. 위 예제는 기본 메모리 값만 설정하며 최소·최대 범위까지 제한하려면 `min`·`max`를 별도로 지정합니다. 네임스페이스 전체의 자원 합계 제한은 ResourceQuota를 사용합니다.

## 참고 자료

- [Kubernetes: Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- [Kubernetes: Limit Ranges](https://kubernetes.io/docs/concepts/policy/limit-range/)
