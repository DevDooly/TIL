# 1.1 Kubeadm 클러스터 설치 및 업그레이드

CKA 시험에서는 `kubeadm`을 사용하여 새로운 노드를 클러스터에 추가하거나, 기존 클러스터의 버전을 업그레이드하는 과정이 빈번하게 출제됩니다.

---

## 1. 클러스터 설치 및 노드 조인 (Installation & Join)

### 1.1 컨트롤 플레인 초기화
```bash
kubeadm init --pod-network-cidr=192.168.0.0/16
```

### 1.2 노드 조인 (Worker Node Join)
컨트롤 플레인 초기화 후 출력되는 토큰 명령어를 복사하여 워커 노드에서 실행합니다.
```bash
kubeadm join <control-plane-host>:<port> --token <token> --discovery-token-ca-cert-hash sha256:<hash>
```
*💡 토큰을 잊어버린 경우:* `kubeadm token create --print-join-command`

---

## 2. 클러스터 업그레이드 (Upgrade)

시험에서는 주로 '마스터 노드를 먼저 업그레이드하고 워커 노드를 업그레이드하라'는 지시가 내려집니다.

### 2.1 마스터 노드 업그레이드 순서

1. **패키지 매니저 업데이트**: `apt update`
2. **kubeadm 업그레이드**: 
    ```bash
    apt-get install -y --allow-change-held-packages kubeadm=1.x.x-00
    ```

3. **업그레이드 계획 확인**: `kubeadm upgrade plan`
4. **업그레이드 적용**: `kubeadm upgrade apply v1.x.x`
5. **kubelet & kubectl 업그레이드**:
    ```bash
    apt-get install -y --allow-change-held-packages kubelet=1.x.x-00 kubectl=1.x.x-00
    systemctl daemon-reload
    systemctl restart kubelet
    ```

### 2.2 노드 비우기 (Drain & Uncordon)
업그레이드 전 노드에서 실행 중인 파드를 안전하게 옮겨야 합니다.
```bash
# 1. 노드를 스케줄링 불가능 상태로 만들고 파드 비우기
kubectl drain <node-name> --ignore-daemonsets --force

# 2. 작업 완료 후 다시 스케줄링 가능 상태로 복구
kubectl uncordon <node-name>
```
