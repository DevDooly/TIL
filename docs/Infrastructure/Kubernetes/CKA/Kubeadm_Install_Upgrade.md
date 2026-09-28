# 1.1 Kubeadm 클러스터 설치 및 업그레이드

kubeadm 작업은 **명령을 실행할 노드**와 **목표 버전**을 먼저 확인한다. 아래 패키지 예제는 Debian/Ubuntu 계열이며, 대상 환경의 저장소와 패키지 버전으로 바꿔 사용한다.

## 1. 설치와 노드 조인

1. 컨테이너 런타임·CRI 소켓, 네트워크와 필요한 포트, kubelet의 cgroup 설정을 준비한다. kubeadm 설치 지침에 맞춰 swap을 처리하고 패키지를 설치한다.
2. 첫 컨트롤 플레인에서 `kubeadm init`을 실행한다. Pod CIDR은 CNI와 맞추고 노드·Service 네트워크와 겹치지 않게 정한다.
3. 관리자 kubeconfig를 준비한다.
4. 선택한 CNI를 설치하고 시스템 Pod를 확인한다.
5. 워커에서 join 명령을 실행한 뒤 노드가 `Ready`인지 확인한다.

[클러스터 생성 공식 절차](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)

```bash
# 첫 컨트롤 플레인: CIDR은 사용하는 CNI에 맞춘다.
sudo kubeadm init --pod-network-cidr=192.168.0.0/16

# kubectl을 사용할 일반 사용자 계정에서 실행한다.
mkdir -p "$HOME/.kube"
sudo cp /etc/kubernetes/admin.conf "$HOME/.kube/config"
sudo chown "$(id -u):$(id -g)" "$HOME/.kube/config"

# CNI 설치 후 조인 명령이 다시 필요할 때 실행한다.
sudo kubeadm token create --print-join-command
```

출력된 `kubeadm join ...`은 **추가할 워커 노드**에서 `sudo`로 실행한다. 추가 컨트롤 플레인은 `--control-plane`과 인증서·안정적인 API endpoint를 포함한 [HA 구성 절차](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/high-availability/)를 따른다.

## 2. 업그레이드 전 확인

- 현재 버전·노드 상태와 목표 버전을 확인한다. minor 버전을 건너뛰지 않고 목표 버전의 kubeadm 문서와 version skew 정책을 따른다.
- [etcd 백업](ETCD_Backup_Restore.md)과 필요한 애플리케이션 데이터를 보관한다.
- 목표 minor 버전의 `pkgs.k8s.io` 저장소를 설정하고 `apt-cache madison kubeadm`으로 **정확한 패키지 버전**을 확인한다. 예전 `-00` 접미사를 고정해서 쓰지 않는다.
- 노드를 한 대씩 처리한다. drain 전에 다른 노드의 수용 용량과 PodDisruptionBudget(PDB)을 확인한다.

[컨트롤 플레인 업그레이드](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/), [버전 호환 정책](https://kubernetes.io/releases/version-skew-policy/)

## 3. 노드 역할별 순서

| 작업 대상 | kubeadm 단계 | 이후 공통 단계 |
| :--- | :--- | :--- |
| 첫 컨트롤 플레인 | kubeadm 갱신 → `upgrade plan` → `upgrade apply <목표 버전>` | drain → kubelet 갱신 → 재시작·확인 → uncordon |
| 추가 컨트롤 플레인 | kubeadm 갱신 → `upgrade node` | drain → kubelet 갱신 → 재시작·확인 → uncordon |
| 워커 | 컨트롤 플레인 완료 후 kubeadm 갱신 → `upgrade node` | drain → kubelet 갱신 → 재시작·확인 → uncordon |

`kubectl`도 API server와 호환되는 버전으로 갱신한다. **drain은 kubelet을 minor 업그레이드하기 전에 완료**해야 한다. 계획에 따라 drain을 더 일찍 할 수 있지만, kubeadm과 kubelet 패키지 갱신을 한 단계로 묶지 않는다. drain은 Static Pod와 DaemonSet Pod를 모두 중지하는 명령이 아니다.

### 3.1 첫 컨트롤 플레인: kubeadm 갱신과 apply

다음 변수는 형식 예시다. 실행 전에 목표 Kubernetes 버전과 패키지 조회 결과의 전체 문자열로 교체한다.

```bash
sudo apt-get update
apt-cache madison kubeadm

# 조회 결과를 확인한 뒤 실제 버전으로 설정한다.
TARGET_VERSION='v1.Y.Z'
PKG_VERSION='1.Y.Z-1.1'

sudo apt-mark unhold kubeadm
sudo apt-get install -y kubeadm="$PKG_VERSION"
sudo apt-mark hold kubeadm
kubeadm version

sudo kubeadm upgrade plan
sudo kubeadm upgrade apply "$TARGET_VERSION"
```

### 3.2 추가 컨트롤 플레인과 워커: node 실행

각 대상 노드에서 목표 버전의 kubeadm 패키지를 갱신한 다음 실행한다. `upgrade apply`는 첫 컨트롤 플레인에서만 실행한다.

```bash
sudo kubeadm upgrade node
```

워커에서는 로컬 kubelet 설정을 갱신한다. 해당 노드의 kubectl도 version skew를 맞춘다. [Linux 워커 업그레이드](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/upgrading-linux-nodes/)

### 3.3 관리자 터미널에서 drain

```bash
# 관리자 kubeconfig가 있는 터미널에서 실행한다.
kubectl drain <node-name> --ignore-daemonsets
```

성공하기 전에는 kubelet 갱신으로 넘어가지 않는다. PDB, 관리 컨트롤러가 없는 Pod, `emptyDir` 데이터 등 실패 원인을 먼저 확인한다. `--force`는 관리 컨트롤러가 없는 Pod 등의 삭제를 허용하며 PDB를 우회하지 않는다. `--delete-emptydir-data`는 임시 데이터 삭제를 허용하므로 필요한 경우에만 사용한다. [drain 옵션](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_drain/)

### 3.4 대상 노드에서 kubelet 갱신과 재시작

새 SSH 세션에서는 변수를 다시 설정한다. 다음은 kubelet·kubectl이 설치된 노드의 예다. kubectl을 설치하지 않은 워커라면 kubelet만 갱신할 수 있다.

```bash
PKG_VERSION='1.Y.Z-1.1' # 조회한 실제 버전으로 교체
sudo apt-mark unhold kubelet kubectl
sudo apt-get install -y kubelet="$PKG_VERSION" kubectl="$PKG_VERSION"
sudo apt-mark hold kubelet kubectl

sudo systemctl daemon-reload
sudo systemctl restart kubelet
sudo systemctl status kubelet --no-pager
```

실패하면 `journalctl -u kubelet`으로 원인을 해결한다. 실패 상태에서 uncordon하거나 다음 노드로 넘어가지 않는다.

### 3.5 관리자 터미널에서 확인과 uncordon

```bash
kubectl get nodes -o wide
kubectl wait --for=condition=Ready node/<node-name> --timeout=180s
kubectl uncordon <node-name>
kubectl get pods -A -o wide
```

kubelet 버전, 시스템 Pod, 기존 워크로드를 확인한 뒤 다음 노드로 진행한다. 일부 컨트롤 플레인만 갱신한 상태에서 전체 완료로 판단하지 않는다.
