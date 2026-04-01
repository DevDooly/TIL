# 1.2 ETCD 백업(Backup) 및 복원(Restore)

ETCD는 클러스터의 모든 상태 정보가 저장되는 데이터베이스입니다. 장애 발생 시 클러스터를 복구하기 위해 반드시 숙지해야 하는 실전 기술입니다.

---

## 1. ETCD 백업 (Snapshot)

`etcdctl` 명령어를 사용하며, 세 가지 필수 옵션(`endpoints`, `cacert`, `cert`, `key`)을 정확히 입력해야 합니다.

```bash
# 공식 문서 예제 기반
ETCDCTL_API=3 etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  snapshot save /opt/snapshot-pre-boot.db
```
*💡 인증서 경로 팁: `describe pod etcd-master -n kube-system` 명령어로 실제 경로를 확인할 수 있습니다.*

---

## 2. ETCD 복원 (Restore)

복원 시에는 기존 데이터 디렉토리와 겹치지 않게 새로운 디렉토리(`--data-dir`)를 지정하는 것이 안전합니다.

### 2.1 스냅샷 복원 실행
```bash
ETCDCTL_API=3 etcdctl \
  --data-dir=/var/lib/etcd-from-backup \
  snapshot restore /opt/snapshot-pre-boot.db
```

### 2.2 정적 파드(Static Pod) 설정 변경
복원된 데이터 디렉토리를 실제 etcd 파드가 바라보게 하려면 `/etc/kubernetes/manifests/etcd.yaml` 파일을 수정해야 합니다.

1.   `volumes` 섹션의 `hostPath` 수정
2.   `volumeMounts` 섹션의 경로 확인
3.   수정 후 `kubelet`이 자동으로 파드를 재시작할 때까지 대기합니다.

---

## 3. 백업 확인 명령어
```bash
ETCDCTL_API=3 etcdctl --write-out=table snapshot status /opt/snapshot-pre-boot.db
```