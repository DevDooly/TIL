# ArgoCD 설치 가이드

ArgoCD는 Kubernetes 클러스터 내부에서 실행되는 리소스이므로, **Helm**을 사용하거나 **Kubectl**로 매니페스트를 직접 적용하여 설치할 수 있습니다.

## 1. Kubectl을 이용한 설치 (빠른 시작)

가장 간단하게 공식 매니페스트를 적용하여 설치하는 방법입니다.

### 네임스페이스 생성
```bash
kubectl create namespace argocd
```

### 매니페스트 적용
```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```
이 명령어는 고가용성(HA)이 적용되지 않은 기본 설치입니다. 프로덕션 환경에서는 HA 버전을 사용하는 것이 좋습니다.

---

## 2. Helm을 이용한 설치 (권장)

설정을 커스터마이징하고 관리하기 편한 Helm 차트를 이용하는 방법입니다.

### Helm 리포지토리 추가
```bash
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
```

### 설치
```bash
helm install argocd argo/argo-cd --namespace argocd --create-namespace
```

### 커스텀 설정 (values.yaml)
`values.yaml`을 통해 인그레스(Ingress), 리소스 제한, 고가용성 등을 설정할 수 있습니다.

```yaml
# custom-values.yaml 예시
server:
  ingress:
    enabled: true
    hosts:
      - argocd.example.com
```

---

## 3. ArgoCD CLI 설치

ArgoCD를 커맨드 라인에서 제어하기 위한 CLI 도구입니다.

### Linux
```bash
curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd
rm argocd-linux-amd64
```

### Mac (Homebrew)
```bash
brew install argocd
```

---

## 4. 접속 및 초기 설정

### 초기 비밀번호 확인
설치 시 `admin` 계정의 초기 비밀번호가 Secret으로 생성됩니다.

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
```

### 포트 포워딩 (로컬 접속 시)
외부 접속 설정(Ingress/LoadBalancer)을 하지 않았다면 포트 포워딩으로 접속합니다.

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```
이제 브라우저에서 `https://localhost:8080` 으로 접속할 수 있습니다.
- **ID:** admin
- **Password:** 위에서 확인한 비밀번호
