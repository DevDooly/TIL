# 5.3 노드 및 네트워크 트러블슈팅 (Node & Network Troubleshooting)

워커 노드가 `NotReady` 상태에 빠지거나, 파드 간 또는 클러스터 내부 도메인(DNS) 통신이 실패하는 상황을 해결하는 절차를 정리합니다.

---

## 1. 워커 노드 NotReady 장애 해결

워커 노드가 `NotReady` 상태로 표시되면 해당 노드에 실행 중인 파드들이 정상 동작하지 않거나 스케줄링이 중단됩니다.

```bash
# 1. 노드 상태 및 조건(Conditions) 확인
kubectl get nodes
kubectl describe node <node-name>
```

`describe node` 출력의 `Conditions` 섹션을 확인합니다:

- `Ready: False` 또는 `Ready: Unknown`
- `MemoryPressure`, `DiskPressure`, `PIDPressure`가 `True`인지 확인

### 워커 노드 복구 3단계 절차
```bash
# 해당 노드로 SSH 접속
ssh <node-name>

# 1단계: kubelet 데몬 상태 확인
sudo systemctl status kubelet

# 만약 죽어있다면 시작 및 부팅 시 자동실행 등록
sudo systemctl daemon-reload
sudo systemctl restart kubelet
sudo systemctl enable kubelet

# 2단계: 여전히 실패한다면 journalctl로 시스템 로그 분석
sudo journalctl -u kubelet -n 50 --no-pager

# 3단계: 컨테이너 런타임(containerd) 상태 점검
sudo systemctl status containerd
sudo systemctl restart containerd
```

### 자주 발생하는 노드 장애 원인

1. **kubelet 서비스가 중지되어 있음**: `systemctl start kubelet`으로 해결.
2. **kubelet 설정 오타**: `/var/lib/kubelet/config.yaml` 파일 내의 오타 또는 잘못된 cgroup 드라이버(`cgroupDriver: systemd`).
3. **인증서 또는 kubelet.conf 누락**: `/etc/kubernetes/kubelet.conf` 경로가 잘못되었거나 클러스터 CA가 변경된 경우.

---

## 2. CoreDNS 및 클러스터 도메인 해석 장애

파드 내부에서 서비스 이름(예: `http://my-service`)으로 접속을 시도할 때 `Could not resolve host` 에러가 난다면 DNS 계층의 문제입니다.

### 2.1 CoreDNS 진단 순서
```bash
# 1. CoreDNS 파드가 정상 실행 중인지 확인
kubectl get pods -n kube-system -l k8s-app=kube-dns

# 2. CoreDNS 서비스의 ClusterIP 확인
kubectl get svc -n kube-system -l k8s-app=kube-dns

# 3. CoreDNS 로그 확인 (에러 및 재시작 원인 추적)
kubectl logs -n kube-system -l k8s-app=kube-dns
```

### 2.2 파드 내부 DNS 설정 점검
파드가 올바른 DNS 서버(kube-dns의 ClusterIP)를 바라보고 있는지 확인합니다.
```bash
# 파드 내부의 resolv.conf 확인
kubectl exec -it <pod-name> -- cat /etc/resolv.conf
# nameserver <kube-dns-cluster-ip> 가 적혀 있어야 함

# nslookup 도메인 질의 테스트
kubectl exec -it <pod-name> -- nslookup kubernetes.default
```

### 2.3 CoreDNS ConfigMap 점검
CoreDNS의 설정 파일은 ConfigMap으로 관리됩니다.
```bash
kubectl describe configmap coredns -n kube-system
```

- upstream DNS 서버 포워딩 설정(`/etc/resolv.conf`)이나 도메인 존 설정에 문법 오류가 없는지 점검합니다.

---

## 3. CNI 네트워크 플러그인 장애

모든 노드가 `NotReady`이고 `describe node`에서 `NetworkPluginNotReady` 메시지가 뜬다면 CNI(Calico, Flannel 등) 플러그인이 배포되지 않았거나 중단된 상태입니다.

```bash
# CNI 데몬셋 파드 상태 확인
kubectl get pods -n kube-system | grep -E "calico|flannel|weave|cilium"

# CNI 설정 파일 위치 확인
ls -l /etc/cni/net.d/
```

---

## 💡 CKA 시험 실전 팁

1. 노드 문제 해결 지시가 나오면 우선 **`ssh <node-name>`**으로 접속해야 합니다.
2. 접속 후 가장 빠른 1순위 조치는 **`systemctl status kubelet`**과 **`journalctl -u kubelet -e`**입니다.
3. 작업 완료 후 노드에서 빠져나와(`exit`) 마스터 노드에서 **`kubectl get nodes`**로 `Ready` 상태로 복구되었는지 반드시 확인하세요!
