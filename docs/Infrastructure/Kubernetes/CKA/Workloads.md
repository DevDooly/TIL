# 2.1 워크로드 (Pod, Deployment, DaemonSet 등)

CKA 시험의 워크로드 영역에서는 파드를 생성하고 관리하는 다양한 컨트롤러들의 개념과 생성/스케일링/롤아웃 명령어를 숙지해야 합니다.

---

## 1. Pod (파드)
가장 작고 기본적인 배포 단위입니다. 보통 단독으로 생성하기보다는 Deployment 등을 통해 간접적으로 생성합니다.

*   **생성 (Imperative)**: `kubectl run my-pod --image=nginx`
*   **라벨(Label)과 함께 생성**: `kubectl run my-pod --image=nginx --labels="env=prod,tier=frontend"`
*   **멀티 컨테이너 파드**: 한 파드 안에 여러 컨테이너가 있을 때 로그를 보거나 접속하려면 `-c` 옵션이 필요합니다.
    *   로그: `kubectl logs my-pod -c container-name`
    *   접속: `kubectl exec -it my-pod -c container-name -- /bin/sh`

---

## 2. Deployment (디플로이먼트)
파드의 개수(ReplicaSet)를 유지하고, 무중단 배포(Rolling Update) 및 롤백을 관리합니다. CKA에서 가장 자주 다루는 리소스입니다.

### 2.1 생성 및 스케일링

*   **생성**: `kubectl create deployment my-deploy --image=nginx --replicas=3`
*   **스케일 아웃/인**: `kubectl scale deployment my-deploy --replicas=5`

### 2.2 롤아웃 (업데이트) 및 롤백
이미지 버전을 변경하여 새로운 버전으로 롤아웃합니다.

*   **이미지 업데이트**: `kubectl set image deployment/my-deploy nginx=nginx:1.19.1`
*   **롤아웃 상태 확인**: `kubectl rollout status deployment/my-deploy`
*   **히스토리 확인**: `kubectl rollout history deployment/my-deploy`
*   **이전 버전으로 롤백**: `kubectl rollout undo deployment/my-deploy`

---

## 3. DaemonSet (데몬셋)
클러스터의 **모든 워커 노드**에 파드가 하나씩(혹은 특정 노드들에만 하나씩) 실행되도록 보장합니다. 로그 수집기(Fluentd)나 모니터링 에이전트에 주로 사용됩니다.

*   *팁*: `kubectl create daemonset` 명령어는 존재하지 않습니다. Deployment의 YAML 뼈대를 만든 후, `kind: Deployment`를 `kind: DaemonSet`으로 변경하고 불필요한 필드(`replicas`, `strategy` 등)를 지우는 방식으로 만들어야 합니다.

---

## 4. Job & CronJob
단발성 작업이나 주기적인 스케줄링 작업을 실행합니다.

*   **Job 생성**: `kubectl create job my-job --image=busybox -- date`
*   **CronJob 생성**: `kubectl create cronjob my-cron --image=busybox --schedule="*/1 * * * *" -- date`
