# etcd 백업과 복원: etcdctl과 etcdutl 구분

확인 기준: etcd 3.6 공식 문서, 2026-09-07. CKA 실습에서도 먼저 제공된 etcd/tool 버전과 클러스터 구성을 확인한다.

## 도구의 역할

| 작업 | 도구 |
| :--- | :--- |
| 실행 중인 etcd에서 snapshot 저장 | `etcdctl snapshot save` |
| snapshot 파일 상태 확인 | `etcdutl snapshot status` |
| snapshot으로 새 data directory 생성 | `etcdutl snapshot restore` |

`etcdctl snapshot status/restore`는 3.6에서 제거되었다. 구버전 예제를 그대로 암기하지 않는다. [etcd 3.6 변경 사항](https://etcd.io/blog/2025/announcing-etcd-3.6/)

```bash
etcdctl version
etcdutl version
etcdutl snapshot restore --help
```

## 백업과 상태 확인

다음은 kubeadm에서 자주 사용하는 경로를 가정한 예다. `endpoints`·`cacert`·`cert`·`key` 네 항목은 실제 static Pod manifest와 인증 설정에 맞춘다.

```bash
etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/healthcheck-client.crt \
  --key=/etc/kubernetes/pki/etcd/healthcheck-client.key \
  snapshot save /opt/snapshot-pre-restore.db

etcdutl --write-out=table snapshot status /opt/snapshot-pre-restore.db
```

snapshot은 Kubernetes Secret 등 민감한 상태를 포함할 수 있으므로 공개 저장소에 올리지 않는다. 파일 생성 성공과 복구 가능성은 다르다. 격리된 실습 환경에서 복원까지 확인한다. [Kubernetes etcd 운영 문서](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/)

## 단일 멤버 실습의 복원 절차

아래는 **단일 멤버 kubeadm 실습용 흐름**이다. 운영 HA 클러스터에는 멤버별 복원과 quorum 계획이 필요하다.

1. snapshot과 기존 etcd manifest를 보관한다. manifest 백업은 kubelet이 감시하는 manifests 디렉터리 **밖**에 둔다.
2. API server와 etcd를 해당 클러스터의 종료 절차에 따라 중지하고 실제 종료를 확인한다.
3. 기존 데이터를 덮어쓰지 않는 새 디렉터리로 복원한다.
4. 복원 시 멤버 이름·peer URL과 manifest의 설정을 맞춘다.
5. etcd volume의 hostPath가 복원 경로를 보도록 수정하고 컨테이너의 mountPath와 `--data-dir`도 일치시키거나 기존 매핑을 유지한다.
6. etcd와 API server를 복구한 뒤 endpoint 상태, 노드·리소스 조회와 실제 리소스 생성·변경을 확인한다.

복원 명령의 형식은 다음과 같다. 이름과 주소는 예시이며 실제 manifest 값으로 바꾼다.

```bash
ETCD_NAME=control-plane
PEER_URL=https://192.0.2.10:2380

etcdutl snapshot restore /opt/snapshot-pre-restore.db \
  --data-dir=/var/lib/etcd-restored \
  --name="$ETCD_NAME" \
  --initial-cluster="$ETCD_NAME=$PEER_URL" \
  --initial-advertise-peer-urls="$PEER_URL" \
  --initial-cluster-token=restore-lab-20260907 \
  --bump-revision=1000000000 \
  --mark-compacted
```

Kubernetes controller의 watch/cache가 과거 revision으로 돌아간 상태를 계속 사용하지 않도록 etcd 공식 복원 가이드는 revision bump와 compaction 표시를 함께 설명한다. 위 10억은 예시이며 snapshot 이후 변경량을 충분히 넘는 값인지 판단해야 한다. flag 지원 여부도 사용하는 `etcdutl`에서 확인한다. [etcd 3.6 재해 복구](https://etcd.io/docs/v3.6/op-guide/recovery/)

TLS 인증은 실행 중인 endpoint에서 백업할 때 사용한다. `etcdutl` 복원은 로컬 파일 작업이므로 백업 명령의 client 인증 옵션을 그대로 붙이지 않는다. 실제 클러스터 복원 실습 결과는 환경·소요 시간·확인한 리소스와 함께 별도로 기록한다.
