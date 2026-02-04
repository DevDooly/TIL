# ArgoCD 실전 사용 예시 (App of Apps)

ArgoCD를 실무에서 사용할 때 가장 강력한 패턴 중 하나인 **App of Apps** 패턴과 **Helm Chart** 연동 예제를 다룹니다.

## 1. App of Apps 패턴

마이크로서비스 환경에서는 관리해야 할 애플리케이션이 수십 개가 될 수 있습니다. 이를 하나하나 UI에서 생성하는 것은 비효율적입니다.
**App of Apps** 패턴은 "다른 애플리케이션들을 생성하는 부모 애플리케이션"을 하나 만들어서, 전체 애플리케이션을 한 번에 관리하는 방식입니다.

### 구조

```text
root-app/
├── templates/
│   ├── guestbook-app.yaml
│   ├── backend-app.yaml
│   └── frontend-app.yaml
└── Chart.yaml
```

### Root Application YAML

부모 앱(`root-app`)은 Git 저장소의 특정 폴더를 바라보게 합니다. 그 폴더 안에는 자식 앱들을 정의한 YAML 파일들이 들어있습니다.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: root-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/my-org/argocd-apps.git
    targetRevision: HEAD
    path: apps  # 자식 앱들의 YAML이 모여있는 경로
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd # Application 리소스는 argocd 네임스페이스에 생성
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

이 `root-app` 하나만 ArgoCD에 등록하면, `apps` 폴더 안에 정의된 모든 애플리케이션이 자동으로 생성되고 동기화됩니다. 새로운 서비스를 추가할 때도 Git에 파일 하나만 추가하면 됩니다.

---

## 2. Helm Chart 배포 예제

ArgoCD는 Helm Chart를 직접 지원합니다. `values.yaml`을 Git에서 관리하여 환경별(Dev/Prod)로 다른 설정을 적용할 수 있습니다.

### Application 정의 (Helm)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-helm-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/my-org/my-charts.git
    targetRevision: HEAD
    path: charts/my-service
    helm:
      valueFiles:
        - values-prod.yaml # 프로덕션용 설정 파일 사용
  destination:
    server: https://kubernetes.default.svc
    namespace: my-service-ns
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### 외부 Helm Repository 사용 시

Git 저장소에 차트가 없고, Artifact Hub 같은 외부 차트 저장소를 사용할 때의 설정입니다.

```yaml
spec:
  source:
    repoURL: https://charts.bitnami.com/bitnami
    chart: nginx
    targetRevision: 15.0.0
    helm:
      parameters:
        - name: service.type
          value: LoadBalancer
```

---

## 3. Image Updater (추가 팁)

ArgoCD 자체는 Git의 변경만 감지합니다. Docker 이미지 태그가 변경되었을 때(예: `v1.0` -> `v1.1`) 자동으로 Git을 업데이트하고 배포하고 싶다면 **Argo CD Image Updater**를 함께 사용하는 것이 좋습니다.

이는 레지스트리를 모니터링하다가 새 이미지가 발견되면, ArgoCD Application의 파라미터를 자동으로 수정(Git Commit 또는 직접 수정)하여 배포를 트리거합니다.
