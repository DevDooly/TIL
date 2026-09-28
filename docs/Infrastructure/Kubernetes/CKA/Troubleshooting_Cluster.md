# 5.2 컨트롤 플레인 트러블슈팅

API 서버가 응답하지 않으면 `kubectl`만으로 진단하기 어렵다. 접속 설정을 확인한 뒤 대상 노드의 kubelet과 컨테이너 런타임 로그를 읽는다.

## 1. 정적 파드의 동작

kubeadm 클러스터의 API 서버, 스케줄러, 컨트롤러 매니저는 보통 `/etc/kubernetes/manifests/`의 매니페스트로 실행된다. 로컬 etcd를 사용하는 구성에는 `etcd.yaml`도 있다. 외부 etcd 구성은 별도로 확인한다.

컨트롤 플레인 노드의 kubelet이 `staticPodPath`를 주기적으로 검사해 정적 파드를 관리한다. API 서버 없이도 실행할 수 있으며, kubelet이 잠시 중지되어도 이미 실행 중인 컨테이너가 즉시 모두 종료되는 것은 아니다.

!!! warning "백업은 감시 디렉터리 밖에 저장"

    kubelet은 점으로 시작하는 파일을 제외하고 확장자와 관계없이 디렉터리의 파일을 읽는다. `kube-apiserver.yaml.bak`도 읽힐 수 있다. 같은 이름의 정적 파드 정의가 둘이면 동작이 정의되지 않아 이전 설정이 반영되는 등의 문제가 생길 수 있다.

    백업은 홈 디렉터리 등 `staticPodPath` 밖에 저장한다.

## 2. API 서버 접속 실패 진단

```text
The connection to the server 192.168.1.10:6443 was refused - did you specify the right host or port?
```

이 메시지는 지정한 주소·포트로 연결하지 못했다는 뜻이다. API 서버 중단 외에도 잘못된 kubeconfig, 엔드포인트·로드밸런서 또는 네트워크 문제를 확인해야 한다.

### 1단계: 현재 작업 위치와 접속 설정 확인

```bash
hostname
kubectl config current-context
kubectl config view --minify
```

문제가 지정한 호스트·클러스터와 일치하는지 확인한다. 필요한 경우 베이스 노드로 `exit`한 뒤 대상 컨트롤 플레인으로 SSH 접속한다. 시험에서는 중첩 SSH를 피한다.

### 2단계: kubelet 상태와 로그 확인

대상 노드에서 실행한다.

```bash
sudo systemctl status kubelet --no-pager
sudo journalctl -u kubelet -n 100 --no-pager
```

로그의 설정 파일 경로, 인증서, 런타임 연결 오류를 확인한다. 원인을 확인하기 전에 서비스를 반복 재시작하지 않는다.

### 3단계: 런타임에서 컨테이너와 로그 확인

`crictl`은 노드의 CRI 런타임 소켓을 사용하도록 설정되어 있어야 한다. `/etc/crictl.yaml`과 실제 런타임 엔드포인트를 확인한다.

```bash
sudo crictl ps -a
sudo crictl logs <container-id>
```

최근에 종료된 API 서버와 etcd 컨테이너를 각각 확인한다. 컨테이너 생성 전 오류는 kubelet 또는 런타임 로그에만 있을 수 있다.

## 3. 로그에 따른 수정

### 인증서 경로·마운트 오류

`cannot load certificate ... no such file or directory`이면 매니페스트의 인자와 volumeMounts·hostPath를 비교한다. 컨테이너 내부 경로와 호스트 경로를 구분하고 파일 존재 여부·권한도 확인한다.

### etcd 접속 실패

`context deadline exceeded`나 `connection refused`이면 API 서버의 `--etcd-servers`, etcd의 listen 주소·포트, 실제 실행 상태를 비교한다. TLS 인증서·CA 불일치와 네트워크 문제도 로그로 구분한다. `127.0.0.1:2379`는 같은 노드의 로컬 etcd를 쓰는 구성에 해당한다.

### 정적 파드 경로 오류

실제로 사용하는 kubelet 설정 파일의 `staticPodPath`를 확인한다. kubeadm의 일반적인 설정 예시는 다음과 같다.

```yaml
# /var/lib/kubelet/config.yaml의 일부
staticPodPath: /etc/kubernetes/manifests
```

정적 파드 매니페스트만 바꾸었다면 kubelet의 다음 검사와 컨테이너 재생성을 기다리며 로그를 확인한다. kubelet 설정 파일을 바꾸었다면 `sudo systemctl restart kubelet`으로 다시 읽게 한다. systemd unit이나 drop-in을 변경한 경우에는 먼저 `sudo systemctl daemon-reload`가 필요하다.

## 4. 스케줄러와 컨트롤러 매니저

API 서버는 응답하지만 새 파드가 배치되지 않으면 스케줄러를, 원하는 수의 파드가 생성되지 않으면 소유 컨트롤러와 컨트롤러 매니저를 확인한다. Pending에는 리소스·PVC·스케줄링 조건 등 여러 원인이 있으므로 이벤트도 함께 읽는다.

```bash
kubectl get pods -n kube-system -o wide
kubectl logs -n kube-system <scheduler-pod-name>
kubectl logs -n kube-system <controller-manager-pod-name>
```

HA 구성이라면 리더 선출 상태도 확인한다. 실제 파드 이름은 조회 결과에서 선택한다.

## 5. 복구 확인

```bash
kubectl get --raw='/readyz?verbose'
kubectl get nodes
kubectl get pods -n kube-system -o wide
```

API 서버 응답뿐 아니라 정적 파드 상태와 로그, 대상 워크로드의 생성·스케줄링·Ready 상태까지 확인한다. etcd 데이터 복구가 필요한 경우에는 [ETCD 백업 및 복원](ETCD_Backup_Restore.md)의 중지·복원·재기동 순서를 따른다.

## 참고 자료

- [Kubernetes: Static Pods](https://kubernetes.io/docs/tasks/configure-pod-container/static-pod/)
- [Kubernetes: Troubleshooting Clusters](https://kubernetes.io/docs/tasks/debug/debug-cluster/)
- [Kubernetes: Debugging Kubernetes nodes with crictl](https://kubernetes.io/docs/tasks/debug/debug-cluster/crictl/)
