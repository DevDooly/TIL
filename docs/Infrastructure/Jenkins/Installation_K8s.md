# Jenkins 설치 가이드 (Kubernetes)

Kubernetes 환경에서 Jenkins를 설치하는 가장 표준적이고 권장되는 방법은 **Helm Chart**를 사용하는 것입니다.

## 1. Helm을 이용한 설치 (권장)

### 사전 준비
- Kubernetes 클러스터가 구축되어 있어야 합니다.
- `kubectl`이 설치 및 설정되어 있어야 합니다.
- `helm`이 설치되어 있어야 합니다.

### Jenkins Helm 리포지토리 추가

```bash
helm repo add jenkins https://charts.jenkins.io
helm repo update
```

### 설치 (기본 설정)

```bash
helm install jenkins jenkins/jenkins
```

위 명령어를 실행하면 `jenkins`라는 릴리스 이름으로 기본 설정의 Jenkins가 설치됩니다.

### 커스텀 설정 (values.yaml)

프로덕션 환경에서는 영구 볼륨(Persistence Volume), 서비스 타입(Service Type), 리소스 제한 등을 설정하기 위해 `values.yaml`을 수정해야 합니다.

1. **기본 설정 파일 다운로드:**
   ```bash
   helm show values jenkins/jenkins > jenkins-values.yaml
   ```

2. **`jenkins-values.yaml` 수정:**
   - **ServiceType:** 기본값은 `ClusterIP`입니다. 외부 접속을 위해 `LoadBalancer` 또는 `NodePort`로 변경하거나 Ingress를 설정합니다.
   - **Persistence:** 스토리지 클래스(StorageClass)와 크기를 환경에 맞게 조정합니다.
   - **AdminPassword:** 초기 관리자 비밀번호를 지정할 수 있습니다.

3. **커스텀 설정으로 설치:**
   ```bash
   helm install jenkins jenkins/jenkins -f jenkins-values.yaml
   ```

---

## 2. 설치 확인 및 접속

### Pod 상태 확인
```bash
kubectl get pods -w
```
`Running` 상태가 될 때까지 기다립니다.

### 관리자 비밀번호 확인
Helm 차트로 설치 시 자동으로 생성된 비밀번호는 다음 명령어로 확인할 수 있습니다.

```bash
kubectl exec --namespace default -it svc/jenkins -c jenkins -- /bin/cat /run/secrets/additional/chart-admin-password && echo
```
(설치 시 네임스페이스나 서비스 이름을 변경했다면 그에 맞게 수정해주세요.)

### 접속
설정한 Service Type에 따라 접속 방법이 다릅니다.

- **LoadBalancer:** `kubectl get svc jenkins`로 확인된 `EXTERNAL-IP`와 포트(8080)로 접속.
- **NodePort:** 노드 IP와 할당된 NodePort로 접속.
- **Port-Forwarding (테스트용):**
  ```bash
  kubectl port-forward svc/jenkins 8080:8080
  ```
  `http://localhost:8080` 접속.

---

## 3. Kubernetes Plugin 설정

Kubernetes 위에 설치된 Jenkins의 가장 큰 장점은 **동적 에이전트 프로비저닝**입니다.
`Kubernetes Plugin`을 설정하면 빌드가 요청될 때마다 자동으로 Pod를 생성하여 빌드를 수행하고, 완료되면 Pod를 삭제합니다.

1. Jenkins 관리 -> 플러그인 관리 -> `Kubernetes` 플러그인 설치 확인.
2. Jenkins 관리 -> 노드 관리 -> Configure Clouds 이동.
3. Kubernetes 클러스터 정보 및 Pod 템플릿 설정.
