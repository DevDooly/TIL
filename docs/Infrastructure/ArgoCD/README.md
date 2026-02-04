# ArgoCD

**ArgoCD**는 Kubernetes를 위한 **GitOps** 지속적 배포(Continuous Delivery) 도구입니다.
Git 저장소에 있는 매니페스트(Manifest) 파일(YAML, Helm Chart, Kustomize 등)을 Kubernetes 클러스터의 상태와 자동으로 동기화합니다.

## 💡 핵심 특징

### 1. GitOps 구현의 핵심
ArgoCD는 **"Git이 진실의 원천(Source of Truth)"**이라는 GitOps 원칙을 따릅니다. 클러스터의 상태를 변경하려면 `kubectl apply`를 직접 실행하는 것이 아니라, Git 저장소의 코드를 수정하고 커밋해야 합니다.

### 2. 자동 동기화 (Sync)
Git 저장소의 상태(Desired State)와 현재 Kubernetes 클러스터의 상태(Live State)를 지속적으로 감시하고 비교합니다. 차이가 발생하면(OutOfSync), 자동으로 또는 수동으로 동기화하여 일치시킵니다.

### 3. 시각화 및 모니터링
직관적인 웹 UI를 통해 애플리케이션의 배포 상태, 리소스 관계, 로그 등을 실시간으로 시각화하여 보여줍니다.

### 4. 다양한 설정 관리 도구 지원
- Kubernetes YAML
- Helm Charts
- Kustomize
- Jsonnet
- 그 외 커스텀 플러그인 지원

## 🚀 도입 효과

- **배포 자동화 및 일관성:** 사람이 수동으로 배포할 때 발생하는 실수를 줄이고, 어떤 환경이든 Git에 정의된 대로 일관성 있게 배포됩니다.
- **쉬운 롤백:** 배포에 문제가 생기면 `git revert` 만으로 이전 버전으로 되돌릴 수 있습니다. (ArgoCD가 변경된 커밋을 감지하여 다시 동기화함)
- **보안성 강화:** 개발자가 클러스터에 직접 접근할 권한(kubectl)을 줄 필요 없이, Git 권한만으로 배포를 제어할 수 있습니다.

---

이 문서는 ArgoCD 시리즈의 첫 번째 파트입니다. 이어지는 문서에서는 설치 방법, 사용 방법, 그리고 실전 예제에 대해 다룹니다.
