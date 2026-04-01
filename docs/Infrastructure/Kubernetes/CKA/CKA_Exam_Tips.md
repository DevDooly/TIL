# 0. CKA 시험 개요 및 팁 (Exam Overview & Tips)

CKA 시험은 이론보다는 **실습(Performance-based)** 위주의 시험입니다. 실제 터미널 환경에서 문제를 해결해야 하므로, 시간 관리와 정확한 명령어 사용이 합격의 핵심입니다.

---

## 1. 시험 환경 및 유의사항

*   **플랫폼**: Killer.sh와 유사한 원격 데스크톱(Remote Desktop) 환경에서 진행됩니다.
*   **브라우저 탭**: 시험 중에는 공식 문서(kubernetes.io/docs) 탭 하나만 추가로 띄울 수 있습니다.
*   **컨텍스트(Context)**: 문제마다 작업해야 할 클러스터가 다를 수 있습니다. 문제 상단에 제공되는 `kubectl config use-context ...` 명령어를 **반드시** 먼저 실행해야 합니다.

---

## 2. 터미널 생산성 향상 (필수 설정)

시험 시작 직후, 시간을 아끼기 위해 아래 설정들을 터미널에 적용하는 것을 권장합니다.

### 2.1 kubectl Alias 및 자동완성
```bash
source <(kubectl completion bash) # bash-completion 패키지가 설치되어 있음
alias k=kubectl
complete -F __start_kubectl k
```

### 2.2 자주 쓰는 환경변수
```bash
export do="--dry-run=client -o yaml"
# 사용 예: k run nginx --image=nginx $do > pod.yaml
```

### 2.3 Vim 설정 (`~/.vimrc`)
YAML 파일을 편집할 때 들여쓰기 오류를 방지하기 위한 최소한의 설정입니다.
```vim
set ts=2 sw=2 sts=2 et
```

---

## 3. 실전 문제 풀이 팁

1.   **Dry-run 활용**: YAML 파일을 처음부터 작성하지 마세요. `kubectl ... --dry-run=client -o yaml > file.yaml` 명령어로 뼈대를 만들고 수정하는 것이 훨씬 빠르고 정확합니다.
2.   **시간 관리**: 배점이 높고 쉬운 문제(예: ETCD 백업, 가벼운 트러블슈팅)부터 먼저 푸세요. 모르는 문제는 `flag` 표시를 하고 과감히 넘어갑니다.
3.   **공식 문서 검색 키워드**: 검색창에 `pv pvc`, `network policy`, `ingress` 등 핵심 키워드를 입력하여 예제 코드를 빠르게 찾는 연습이 필요합니다.
