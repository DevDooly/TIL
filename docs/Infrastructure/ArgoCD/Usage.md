# ArgoCD 사용 방법

ArgoCD에서 애플리케이션을 배포하고 관리하는 기본적인 방법을 다룹니다.

## 1. Application 생성하기

ArgoCD에서 관리하는 배포 단위인 `Application`을 생성하는 방법입니다.

### 방법 A: 웹 UI 사용
1. 좌측 상단 **[+ NEW APP]** 버튼 클릭.
2. **General:**
   - Application Name: 앱 이름 (예: `guestbook`)
   - Project: `default`
   - Sync Policy: `Automatic` (권장) 또는 `Manual`
3. **Source:**
   - Repository URL: Git 저장소 주소 (예: `https://github.com/argoproj/argocd-example-apps.git`)
   - Revision: `HEAD` (또는 브랜치명)
   - Path: 배포할 매니페스트가 있는 경로 (예: `guestbook`)
4. **Destination:**
   - Cluster URL: `https://kubernetes.default.svc` (ArgoCD가 설치된 동일 클러스터)
   - Namespace: 배포될 네임스페이스 (예: `default`)
5. 상단 **[CREATE]** 클릭.

### 방법 B: YAML 파일 사용 (Declarative)
GitOps 원칙에 따라 Application 자체도 코드로 관리하는 것이 좋습니다.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: guestbook
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/argoproj/argocd-example-apps.git
    targetRevision: HEAD
    path: guestbook
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true    # Git에 없는 리소스는 클러스터에서 삭제
      selfHeal: true # 클러스터에서 임의로 변경된 내용을 Git 상태로 복구
```
```bash
kubectl apply -f application.yaml
```

---

## 2. 동기화 (Sync) 이해하기

### Sync Status
- **Synced:** Git과 클러스터 상태가 일치함.
- **OutOfSync:** Git에 변경 사항이 있거나, 클러스터 상태가 변경되어 불일치함.

### Sync Policy
- **Manual (수동):** 사용자가 직접 [SYNC] 버튼을 눌러야 배포됩니다. 운영 환경에서 승인 절차가 필요할 때 유용합니다.
- **Automatic (자동):** Git에 커밋이 발생하면 ArgoCD가 감지하고 즉시 배포합니다.
  - `prune: true`: Git에서 파일이 삭제되면 클러스터 리소스도 삭제합니다. (기본값은 false)
  - `selfHeal: true`: 누군가 `kubectl edit`으로 리소스를 수정하면, 즉시 Git에 정의된 상태로 되돌립니다.

---

## 3. 리소스 상태 확인

- **Health Status:**
  - `Healthy`: Pod가 정상 실행 중이고 서비스 연결이 완료됨.
  - `Progressing`: 배포 진행 중 (예: 새 Pod 생성 중).
  - `Degraded`: 배포 실패 또는 오류 발생.
  - `Missing`: 리소스가 클러스터에 존재하지 않음.

UI에서 각 리소스 아이콘을 클릭하면 상세 로그와 YAML 설정, 이벤트 등을 확인할 수 있어 디버깅에 매우 유용합니다.
