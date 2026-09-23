# 2.5 멀티 컨테이너 파드 & 네이티브 사이드카 (Multi-Container Pods)

하나의 파드(Pod) 내부에는 여러 개의 컨테이너가 공존할 수 있으며, 이들은 **동일한 네트워크 네임스페이스(IP, 포트)와 스토리지 볼륨을 공유**합니다. CKA 시험에서는 전통적인 Init 컨테이너, 공유 볼륨 로깅 패턴뿐만 아니라 **Kubernetes 1.29+에서 정식 지원(GA)된 Native Sidecar Container**가 중요 출제 포인트로 다루어집니다.

---

## 1. Init 컨테이너 (초기화 컨테이너)

- **동작 특성**: 메인 애플리케이션 컨테이너가 시작되기 **전에** 순차적으로 실행되어 완료(Exit 0)되어야 합니다.
- **용도**: DB 준비 대기, 외부 설정 다운로드, 파일 권한 변경 등.
- Init 컨테이너가 실패하면 파드는 재시작 정책에 따라 계속 재시도하며 메인 컨테이너는 실행되지 않습니다.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: init-demo
spec:
  initContainers:
  - name: wait-for-service
    image: busybox:1.28
    command: ['sh', '-c', 'until nslookup mydb; do echo waiting for mydb; sleep 2; done;']
  containers:
  - name: main-app
    image: busybox:1.28
    command: ['sh', '-c', 'echo The app is running! && sleep 3600']
```

---

## 2. 최신 핵심: Native Sidecar Containers (K8s 1.29+)

> [!IMPORTANT]
> Kubernetes 1.28에 도입되어 1.29부터 기본 활성화된 네이티브 사이드카 기능입니다. `initContainers` 배열 안에 정의하되, **`restartPolicy: Always`**를 명시하면 메인 컨테이너와 함께 파드가 종료될 때까지 백그라운드에서 상시 실행됩니다.

- **차이점**: 기존 사이드카는 일반 `containers`에 넣어 메인보다 늦게 뜨거나 일찍 종료되는 문제가 있었으나, 네이티브 사이드카는 메인 컨테이너 시작 전 먼저 기동되어 파드 수명 주기 내내 유지됩니다.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: native-sidecar-pod
spec:
  initContainers:
  - name: log-agent
    image: busybox:1.28
    # restartPolicy: Always 설정으로 네이티브 사이드카로 동작
    restartPolicy: Always
    command: ['sh', '-c', 'tail -F /var/log/app.log']
    volumeMounts:
    - name: shared-logs
      mountPath: /var/log
  containers:
  - name: app
    image: busybox:1.28
    command: ['sh', '-c', 'while true; do echo "$(date) - Ping" >> /var/log/app.log; sleep 1; done']
    volumeMounts:
    - name: shared-logs
      mountPath: /var/log
  volumes:
  - name: shared-logs
    emptyDir: {}
```

---

## 3. 볼륨 공유를 통한 멀티 컨테이너 로깅 (Adapter/Sidecar 패턴)

메인 컨테이너가 로그를 파일에 기록하면, 사이드카 컨테이너가 `emptyDir` 볼륨으로 해당 파일을 읽어 표준 출력(stdout)으로 스트리밍하는 전통적인 CKA 빈출 패턴입니다.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: shared-volume-pod
spec:
  containers:
  - name: app
    image: busybox
    command: ["/bin/sh", "-c", "while true; do date >> /var/log/app.log; sleep 1; done"]
    volumeMounts:
    - name: log-dir
      mountPath: /var/log
  - name: sidecar
    image: busybox
    command: ["/bin/sh", "-c", "tail -n+1 -f /var/log/app.log"]
    volumeMounts:
    - name: log-dir
      mountPath: /var/log
  volumes:
  - name: log-dir
    emptyDir: {}
```

---

## 4. 멀티 컨테이너 파드 관리 명령어

컨테이너가 여러 개인 파드는 명령 실행 시 반드시 컨테이너 이름(`-c`)을 지정해야 합니다.

```bash
# 특정 컨테이너 로그 확인
kubectl logs <pod-name> -c <container-name>

# 특정 컨테이너 내부 셸 접속
kubectl exec -it <pod-name> -c <container-name> -- /bin/sh

# 이전 컨테이너 실행 로그 확인 (Crash 된 경우)
kubectl logs <pod-name> -c <container-name> --previous
```

---

## 💡 CKA 시험 실전 팁

1. 문제 지문에서 "메인 컨테이너가 시작되기 전에 특정 작업을 수행하라" $\rightarrow$ **`initContainers`**
2. "사이드카 컨테이너로 로그 에이전트를 구성하라" $\rightarrow$ **`emptyDir` 볼륨 공유** 또는 **`restartPolicy: Always`**
3. 문제에서 특정 컨테이너를 지정하여 로그를 추출하라는 지시가 나오면 `kubectl logs <pod> -c <container> > /opt/output.txt` 형태로 리다이렉트합니다.
