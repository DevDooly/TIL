# 5.2 컨트롤 플레인 트러블슈팅 (Control Plane Troubleshooting)

컨트롤 플레인 컴포넌트(`kube-apiserver`, `etcd`, `kube-scheduler`, `kube-controller-manager`)에 문제가 생기면 클러스터 전체가 마비되거나 신규 파드 스케줄링이 중단됩니다. 특히 API 서버가 다운되면 `kubectl` 명령어 자체가 동작하지 않으므로 저수준 런타임 도구를 활용한 진단법을 익혀야 합니다.

---

## 1. 정적 파드 (Static Pods)의 이해

kubeadm으로 구축된 클러스터에서 컨트롤 플레인 핵심 컴포넌트들은 **Static Pod**로 실행됩니다.

- **매니페스트 위치**: `/etc/kubernetes/manifests/`
  - `kube-apiserver.yaml`
  - `etcd.yaml`
  - `kube-controller-manager.yaml`
  - `kube-scheduler.yaml`
- **동작 방식**: 마스터 노드의 `kubelet` 데몬이 이 디렉터리를 실시간으로 감시하며, 파일이 수정되거나 추가되면 API 서버 없이도 직접 컨테이너를 생성/재시작합니다.

---

## 2. API 서버 다운 시 진단 절차 (`The connection was refused`)

`kubectl` 명령 실행 시 다음과 같은 에러가 발생한다면 API 서버가 기동하지 못하고 있는 상태입니다:
```text
The connection to the server 192.168.1.10:6443 was refused - did you specify the right host or port?
```

### 1단계: 마스터 노드로 SSH 접속
```bash
ssh controlplane
```

### 2단계: kubelet 데몬 상태 확인
Static Pod를 실행하는 주체는 `kubelet`이므로 kubelet이 죽어있다면 아무것도 뜨지 않습니다.
```bash
systemctl status kubelet
journalctl -u kubelet -n 50 --no-pager
```

### 3단계: 컨테이너 런타임 도구(`crictl`)로 실패한 컨테이너 추적
`kubectl`이 안 되므로 컨테이너 런타임 CLI인 **`crictl`**을 사용합니다.
```bash
# 실행 중이거나 비정상 종료된 apiserver 컨테이너 검색
sudo crictl ps -a | grep apiserver

# 가장 최근에 종료된 컨테이너 로그 확인 (에러 원인 직격!)
sudo crictl logs <container-id>
```

---

## 3. 컨트롤 플레인 빈출 장애 원인 BEST 3

### 1. 인증서 파일 경로 또는 파일명 오타

- **로그 메시지**: `cannot load certificate /etc/kubernetes/pki/apiserver-etcd-clien.crt: no such file or directory`
- **해결**: `/etc/kubernetes/manifests/kube-apiserver.yaml`을 열어 오타 수정. 저장하면 kubelet이 수초 내에 자동으로 다시 띄웁니다.

### 2. etcd 서버 주소/포트 불일치

- **로그 메시지**: `context deadline exceeded` 또는 `connection refused (port 2379)`
- **해결**: apiserver 매니페스트의 `--etcd-servers=https://127.0.0.1:2379` 설정과 etcd 매니페스트의 listen 포트가 일치하는지 확인.

### 3. Static Pod 매니페스트 경로 설정 누락

- **증상**: `/etc/kubernetes/manifests/`에 파일이 다 있는데 파드가 전혀 안 뜸.
- **원인**: `/var/lib/kubelet/config.yaml` 파일에서 `staticPodPath`가 누락되었거나 엉뚱한 경로로 지정됨.
- **해결**:
  ```yaml
  # /var/lib/kubelet/config.yaml
  staticPodPath: /etc/kubernetes/manifests
  ```
  수정 후 `systemctl restart kubelet` 실행.

---

## 4. 스케줄러 & 컨트롤러 매니저 장애 진단

API 서버는 살아있지만 파드를 만들어도 계속 `Pending` 상태로 머물고 이벤트에 아무것도 안 나온다면 `kube-scheduler`가 다운되었을 가능성이 큽니다.

```bash
# kube-system 네임스페이스의 시스템 파드 상태 확인
kubectl get pods -n kube-system

# 스케줄러 로그 확인
kubectl logs kube-scheduler-controlplane -n kube-system
```

---

## 💡 CKA 시험 실전 팁

1. 마스터 노드 컴포넌트 수정 시 **절대로 매니페스트 파일을 `/etc/kubernetes/manifests/` 디렉터리 안에 그대로 둔 채 백업하지 마세요.**
   - 잘못된 예: `cp kube-apiserver.yaml kube-apiserver.yaml.bak` $\rightarrow$ kubelet이 `.bak` 파일도 정적 파드로 인식하여 포트 충돌로 다운됩니다!
   - 올바른 예: 백업은 반드시 `/tmp/`나 홈 디렉터리로 복사해두세요 (`cp kube-apiserver.yaml /tmp/`).
2. YAML 수정 후 10~20초 정도 기다리거나, 급한 경우 `systemctl restart kubelet`을 실행하여 즉시 반영시킵니다.
