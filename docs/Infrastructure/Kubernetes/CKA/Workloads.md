# 2.1 워크로드 (Pod, Deployment, DaemonSet 등)

CKA 시험의 워크로드 영역에서는 파드를 생성하고 관리하는 다양한 컨트롤러들의 개념과 생성/스케일링/롤아웃 명령어를 숙지해야 합니다.

---

## 1. Pod (파드)

가장 작고 기본적인 배포 단위입니다. 보통 단독으로 생성하기보다는 Deployment 등을 통해 간접적으로 생성합니다.

* **생성 (Imperative)**: `kubectl run my-pod --image=nginx`
* **라벨(Label)과 함께 생성**: `kubectl run my-pod --image=nginx --labels="env=prod,tier=frontend"`
* **멀티 컨테이너 파드**: `-c` 옵션으로 로그·접속 대상을 명확히 지정합니다. 생략하면 기본 컨테이너가 선택될 수 있습니다.
    * 로그: `kubectl logs my-pod -c container-name`
    * 접속: `kubectl exec -it my-pod -c container-name -- /bin/sh`

---

## 2. Deployment (디플로이먼트)

ReplicaSet을 통해 원하는 파드 수를 유지하고 RollingUpdate·Recreate 배포와 롤백을 관리합니다. 무중단 여부는 readiness, replica 수와 업데이트 전략에 달려 있습니다.

### 2.1 생성 및 스케일링

* **생성**: `kubectl create deployment my-deploy --image=nginx --replicas=3`
* **스케일 아웃/인**: `kubectl scale deployment my-deploy --replicas=5`

### 2.2 롤아웃 (업데이트) 및 롤백

이미지 버전을 변경하여 새로운 버전으로 롤아웃합니다.

* **이미지 업데이트**: `kubectl set image deployment/my-deploy nginx=<target-image>`
* **롤아웃 상태 확인**: `kubectl rollout status deployment/my-deploy`
* **히스토리 확인**: `kubectl rollout history deployment/my-deploy`
* **이전 버전으로 롤백**: `kubectl rollout undo deployment/my-deploy`

---

## 3. DaemonSet (데몬셋)

nodeSelector·affinity·taint/toleration 등 조건을 만족하는 **대상 노드마다** 파드를 실행합니다. 컨트롤 플레인도 조건을 만족하면 대상이 됩니다. 로그 수집기(Fluentd)나 모니터링 에이전트에 주로 사용됩니다.

* *팁*: `kubectl create daemonset` 명령어는 존재하지 않습니다. Deployment의 YAML 뼈대를 만든 후, `kind: Deployment`를 `kind: DaemonSet`으로 변경하고 불필요한 필드(`replicas`, `strategy` 등)를 지우는 방식이나 공식 DaemonSet 예제를 사용할 수 있습니다. `spec.selector.matchLabels`와 Pod template의 라벨도 일치해야 합니다.

---

## 4. Job & CronJob

단발성 작업이나 주기적인 스케줄링 작업을 실행합니다.

* **Job 생성**: `kubectl create job my-job --image=busybox -- date`
* **CronJob 생성**: `kubectl create cronjob my-cron --image=busybox --schedule="*/1 * * * *" -- date`

## 참고 자료

- [Kubernetes: Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Kubernetes: DaemonSet](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/)
