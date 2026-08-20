# ArgoCD 사용 방법 및 운영 가이드

ArgoCD에서 애플리케이션을 선언적으로 배포하고, 동기화(Sync) 전략을 제어하며, 멀티테넌시(RBAC/Project)를 운영하는 실무 가이드입니다.

---

## 1. Application 생성 방법 (3가지 방식)

ArgoCD에서 배포의 기본 단위는 `Application` 커스텀 리소스(CRD)입니다.

### 방법 1: 선언적 YAML 파일 (Declarative - 실무 표준 권장)
GitOps 원칙에 맞추어 `Application` 자체를 코드로 작성하고 관리합니다.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: order-service-prod
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io # 앱 삭제 시 하위 K8s 리소스도 함께 삭제
spec:
  project: default
  source:
    repoURL: https://github.com/my-org/k8s-manifests.git
    targetRevision: main
    path: overlays/production
  destination:
    server: https://kubernetes.default.svc # 로컬 클러스터 (또는 원격 클러스터 API URL)
    namespace: prod-service
  syncPolicy:
    automated:
      prune: true      # Git에서 삭제된 리소스는 클러스터에서도 자동 제거
      selfHeal: true   # 클러스터에서 임의로 수정된 리소스를 Git 상태로 자동 강제 원복
    syncOptions:
      - CreateNamespace=true # 대상 네임스페이스가 없으면 자동 생성
      - ApplyOutOfSyncOnly=true # 변경된 리소스만 선별 적용하여 성능 최적화
```

적용 명령어:
```bash
kubectl apply -f application.yaml
```

---

### 방법 2: ArgoCD CLI 사용
터미널에서 스크립트나 명령어로 빠르게 애플리케이션을 생성합니다.

```bash
# 1. 로그인
argocd login <ARGOCD_SERVER_IP_OR_DOMAIN> --username admin --password <PASSWORD> --insecure

# 2. Application 생성
argocd app create order-service \
  --repo https://github.com/my-org/k8s-manifests.git \
  --path overlays/production \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace prod-service \
  --sync-policy auto \
  --auto-prune \
  --self-heal
```

---

### 방법 3: 웹 대시보드 UI
초보자나 디버깅 시 웹 UI(`http://<ARGOCD_SERVER>`)에서 **[+ NEW APP]** 버튼을 눌러 직관적으로 필드를 채워 생성할 수 있습니다.

---

## 2. 동기화(Sync) 정책 및 라이프사이클 제어

### 2.1 Sync Policy & Self-Healing
* **Manual (수동 동기화)**:
  * Git에 변경사항이 푸시되어도 `OutOfSync` 상태만 표시되고 배포되지 않습니다. 운영자가 웹 UI나 CLI에서 승인 후 배포해야 하는 프로덕션 환경에 적합합니다.
* **Automated (자동 동기화)**:
  * Git 커밋이 감지되면 즉시 배포를 수행합니다.
  * `prune: true`: Git에서 매니페스트 파일이 삭제되었을 때 실제 클러스터 리소스도 삭제합니다.
  * `selfHeal: true`: 누군가 `kubectl edit`이나 `kubectl delete`로 클러스터를 임의 조작하면, 즉시 감지하여 Git에 선언된 원래 상태로 되돌립니다.

---

### 2.2 Sync Waves (배포 순서 제어)

여러 Kubernetes 리소스(예: DB 마이그레이션 Job -> ConfigMap -> Service -> Deployment) 간에 **배포 순서(Order of Application)**를 지정해야 할 때 `argocd.argoproj.io/sync-wave` 어노테이션을 사용합니다.

```yaml
# 1단계: 네임스페이스 및 Secret 먼저 생성 (Wave: -1)
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
  annotations:
    argocd.argoproj.io/sync-wave: "-1"
---
# 2단계: DB 마이그레이션 Job 실행 (Wave: 0)
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migration-job
  annotations:
    argocd.argoproj.io/sync-wave: "0"
---
# 3단계: 애플리케이션 Deployment 기동 (Wave: 1)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-api
  annotations:
    argocd.argoproj.io/sync-wave: "1"
```

* **동작 원리**: 숫자가 낮은 Wave의 리소스가 정상 상태(Healthy)가 될 때까지 기다린 후 다음 Wave로 넘어갑니다.

---

### 2.3 Resource Hooks (배포 라이프사이클 훅)

배포 전후에 특정 작업(알림 전송, DB 스키마 체크, 헬스체크 등)을 수행할 때 사용합니다.

* `PreSync`: 배포(Sync)가 시작되기 전에 실행 (예: 백업, 사전 검증)
* `Sync`: 본 배포와 함께 실행
* `PostSync`: 모든 리소스가 성공적으로 배포된 후 실행 (예: 슬랙 배포 완료 알림, E2E 스모크 테스트)
* `SyncFail`: 동기화가 실패했을 때 실행 (예: 장애 알림 전송)

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: slack-notification-job
  annotations:
    argocd.argoproj.io/hook: PostSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded # 성공 시 Job Pod 자동 정리
```

---

## 3. 상태 모니터링 및 상태 코드 이해

ArgoCD는 두 가지 주요 축으로 애플리케이션 상태를 평가합니다.

| 상태 축 | 상태 값 | 설명 |
| :--- | :--- | :--- |
| **Sync Status** | `Synced` | Git 저장소의 매니페스트와 클러스터 리소스가 완전히 일치함 |
| | `OutOfSync` | Git 저장소에 새 커밋이 있거나 클러스터와 불일치함 |
| **Health Status** | `Healthy` | Pod가 정상 실행(Running/Ready) 중이고 서비스 엔드포인트 연결 완료 |
| | `Progressing` | 롤아웃 진행 중 (새 Pod 생성 및 트래픽 전환 중) |
| | `Degraded` | CrashLoopBackOff, ImagePullBackOff 등 Pod 장애 또는 배포 실패 |
| | `Missing` | 매니페스트에 선언되었으나 클러스터에 존재하지 않음 |

---

## 4. AppProject를 이용한 멀티테넌시 및 접근 제어

여러 개발팀이 하나의 ArgoCD를 공유할 때, 팀별로 배포 가능한 Git 저장소, 배포 대상 클러스터/네임스페이스, 리소스 종류를 격리 제한하기 위해 `AppProject`를 생성합니다.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: payment-team-project
  namespace: argocd
spec:
  description: "결제 플랫폼 팀 전용 프로젝트"
  # 접근 허용 Git 저장소
  sourceRepos:
    - "https://github.com/my-org/payment-manifests.git"
  # 배포 허용 대상 클러스터 및 네임스페이스
  destinations:
    - namespace: "payment-*"
      server: "https://kubernetes.default.svc"
  # 배포 금지 리소스 블랙리스트 (예: 클러스터 단위 리소스 생성 차단)
  clusterResourceBlacklist:
    - group: ""
      kind: Node
    - group: "rbac.authorization.k8s.io"
      kind: ClusterRoleBinding
```
