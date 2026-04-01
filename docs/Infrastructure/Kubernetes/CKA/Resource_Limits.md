# 2.3 리소스 제한 (Requests & Limits)

클러스터의 자원(CPU, Memory)을 안정적으로 운영하기 위해 파드가 사용할 리소스의 최소 요구량과 최대 제한량을 설정합니다.

---

## 1. Requests와 Limits의 차이

파드 내부의 컨테이너 스펙(spec)에 정의합니다.

* **Requests (요청량)**: 
    * 컨테이너가 실행되기 위해 **최소한으로 보장받아야 하는 자원량**.
    * 스케줄러는 노드의 남은 자원이 Requests보다 클 때만 해당 파드를 배치합니다. (예약의 개념)
* **Limits (제한량)**:
    * 컨테이너가 사용할 수 있는 **최대 자원량**.
    * **CPU**: 한도를 넘게 쓰려고 하면 스로틀링(Throttling)이 발생하여 느려집니다. (파드가 죽지는 않음)
    * **Memory**: 한도를 넘게 쓰면 **OOMKilled** (Out Of Memory Killed) 에러가 발생하며 파드가 강제 종료(재시작)됩니다.

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
