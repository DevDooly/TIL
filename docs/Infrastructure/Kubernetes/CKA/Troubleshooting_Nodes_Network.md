# 5.3 노드 및 네트워크 트러블슈팅

노드 상태를 확인하고, 영향을 받은 노드의 로그를 읽은 다음 원인을 수정한다. 노드가 Ready로 돌아온 뒤에도 애플리케이션 통신과 DNS가 복구되었는지 확인한다.

## 1. NotReady 노드 진단

`NotReady`는 kubelet이 정상 상태를 보고하지 못한다는 의미다. 기존 컨테이너가 계속 실행될 수도 있으므로 모든 파드가 중단되었다고 단정하지 않는다.

```bash
kubectl get nodes
kubectl describe node <node-name>
kubectl get pods -A -o wide --field-selector spec.nodeName=<node-name>
```

`Ready: False`와 `Ready: Unknown`, 마지막 상태 보고 시각, `MemoryPressure`, `DiskPressure`, `PIDPressure`와 관련 이벤트를 확인한다. `Unknown`이면 kubelet 중단뿐 아니라 노드와 API 서버 사이의 통신 문제도 살핀다.

### 로그 수집 → 원인 수정 → 필요한 서비스 재시작

대상 노드에 SSH로 접속해 상태와 로그를 먼저 수집한다. 아래 런타임 예시는 containerd이며, CRI-O 등 다른 런타임은 실제 서비스 이름을 사용한다.

```bash
ssh <node-name>
sudo systemctl status kubelet containerd --no-pager
sudo journalctl -u kubelet -n 100 --no-pager
sudo journalctl -u containerd -n 100 --no-pager
sudo crictl info
```

| 확인 결과 | 조치 |
| --- | --- |
| kubelet이 중지됨 | 중지 원인을 확인한 뒤 `sudo systemctl start kubelet` |
| kubelet 설정 오류 | 실제 설정 파일을 수정하고 kubelet 재시작 |
| systemd unit·drop-in 수정 | `daemon-reload` 후 해당 서비스 재시작 |
| cgroup 드라이버 불일치 | kubelet과 런타임의 설정·자동 감지 지원을 확인해 일치시킴. `systemd` 자체는 잘못된 값이 아님 |
| 인증서·kubeconfig 오류 | 경로·권한·유효기간·CA와 API 서버 주소 확인 |
| 디스크·메모리·PID 압박 | 사용량과 원인 프로세스·로그·이미지 등을 조사하고 용량 또는 워크로드 조정 |
| CRI 런타임 오류 | 런타임 로그와 설정을 먼저 확인하고 원인 수정 후 필요한 경우에만 재시작 |

`systemctl enable`은 부팅 시 자동 시작 설정이며 현재 장애 원인을 고치지 않는다. 모든 장애에서 런타임을 함께 재시작할 필요는 없다.

수정 후 베이스 노드로 돌아가 문제에서 지정한 kubectl 작업 호스트에 접속한다. 중첩 SSH를 피하고 다음을 확인한다.

```bash
kubectl wait --for=condition=Ready node/<node-name> --timeout=120s
kubectl get pods -A -o wide --field-selector spec.nodeName=<node-name>
```

## 2. DNS 장애 진단

먼저 실제 Service 이름과 네임스페이스를 확인한다. 짧은 이름 `my-service`는 보통 호출 파드의 네임스페이스에서 찾는다. 다른 네임스페이스라면 `my-service.<namespace>` 또는 클러스터 도메인을 포함한 이름을 사용한다.

### 2.1 파드의 DNS 설정과 질의 결과

```bash
kubectl exec <pod-name> -- cat /etc/resolv.conf
kubectl exec <pod-name> -- nslookup kubernetes.default
kubectl get pod <pod-name> -o yaml
```

컨테이너에 `nslookup`이 없다면 허용된 진단용 파드를 사용한다. 멀티 컨테이너 파드는 `-c`로 대상을 지정한다.

`dnsPolicy`, `dnsConfig`, `hostNetwork`와 `/etc/resolv.conf`를 함께 확인한다. NodeLocal DNSCache를 사용하는 클러스터는 nameserver가 kube-dns의 ClusterIP 대신 로컬 캐시 주소일 수 있다. `hostNetwork` 파드에서 클러스터 DNS가 필요하다면 `ClusterFirstWithHostNet` 설정을 확인한다.

### 2.2 CoreDNS와 kube-dns Service

```bash
kubectl get pods -n kube-system -l k8s-app=kube-dns -o wide
kubectl get svc kube-dns -n kube-system
kubectl get endpointslices -n kube-system -l kubernetes.io/service-name=kube-dns
kubectl logs -n kube-system -l k8s-app=kube-dns --tail=100
kubectl get configmap coredns -n kube-system -o yaml
```

DNS 파드의 Ready 상태, Service 주소와 EndpointSlice, Corefile의 문법·upstream 설정을 확인한다. 외부 도메인만 실패한다면 upstream 연결과 forward 설정을 살핀다.

Egress를 제한한 파드는 DNS 서버로의 UDP·TCP 53번 포트도 허용되어야 한다. 실제 DNS 경로와 적용된 NetworkPolicy를 확인한다.

## 3. CNI와 서비스 통신

`NetworkPluginNotReady`는 해당 노드의 CNI 초기화 문제를 조사할 단서다. 일부 노드에서만 발생할 수도 있다.

```bash
kubectl get daemonsets,pods -A -o wide
```

설치된 CNI의 실제 네임스페이스·파드를 선택해 Events와 로그를 읽는다. CNI가 항상 `kube-system`에 설치되는 것은 아니다. 문제가 있는 노드에서 런타임이 사용하는 CNI 설정·바이너리 경로도 확인한다. 흔히 사용하는 설정 경로는 `/etc/cni/net.d/`이다.

DNS 해석은 성공하는데 Service 접속이 실패하면 다음 순서로 범위를 좁힌다.

1. Service selector, port·targetPort와 EndpointSlice를 확인한다.
2. 대상 파드가 Ready이며 해당 포트에서 수신하는지 확인한다.
3. 출발·도착 파드에 적용되는 NetworkPolicy와 노드 네트워크를 확인한다.
4. 클러스터 구성에 따라 kube-proxy 또는 이를 대체하는 CNI의 서비스 처리 기능을 확인한다.

복구 후에는 같은 노드·다른 노드의 파드 통신, Service 접속과 DNS 질의를 다시 시험한다.

## 참고 자료

- [Kubernetes: Troubleshooting Clusters](https://kubernetes.io/docs/tasks/debug/debug-cluster/)
- [Kubernetes: Debugging DNS Resolution](https://kubernetes.io/docs/tasks/administer-cluster/dns-debugging-resolution/)
- [Kubernetes: NodeLocal DNSCache](https://kubernetes.io/docs/tasks/administer-cluster/nodelocaldns/)
- [서비스 진단](Services.md), [네트워크 정책](Network_Policy.md)
