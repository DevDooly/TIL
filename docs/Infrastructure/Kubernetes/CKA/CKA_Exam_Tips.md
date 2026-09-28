# 0. CKA 시험 개요 및 팁

CKA는 터미널에서 Kubernetes 관리 작업을 수행하는 실습 시험이다. 문제에 지정된 작업 호스트·클러스터·namespace와 결과 저장 경로를 먼저 확인하고, 변경 후 실제 상태까지 검증한다.

## 1. 시험 환경과 허용 자료

- 시험 시간은 **2시간**, 합격 기준은 **66% 이상**이다. 문항 수와 개별 배점은 시험 화면을 따른다. [Linux Foundation FAQ](https://docs.linuxfoundation.org/tc-docs/certification/faq-cka-ckad-cks)
- 문제의 안내 상자에 지정된 **호스트로 SSH 접속**해서 작업한다. 완료 후 `exit`으로 `base`에 돌아온다. 중첩 SSH는 지원하지 않으며 `base`를 재부팅하지 않는다.
- 지정 호스트의 `kubectl`과 `k` alias·자동완성이 준비되어 있는지 확인한다. `base`에 같은 도구가 있다고 가정하지 않는다. context 전환 명령이 제공되면 실행하고 현재 context·namespace도 확인한다. [공식 기술 지침](https://docs.linuxfoundation.org/tc-docs/certification/tips-cka-and-ckad)
- VM 안의 브라우저에서 Kubernetes 문서·블로그, Helm 문서, CKA용 Gateway API 문서와 문제의 Quick Reference 자료를 사용할 수 있다. 허용 문서 내부 검색은 가능하지만 외부 검색 결과는 열지 않는다. 응시 전 [허용 자료 목록](https://docs.linuxfoundation.org/tc-docs/certification/certification-resources-allowed)을 다시 확인한다.

학습 문서에 연결한 모든 외부 사이트가 시험에서도 허용되는 것은 아니다. 시험 Kubernetes 버전은 공식 FAQ와 접속한 환경의 `kubectl version`으로 확인한다.

## 2. 문제를 시작하는 순서

```bash
# base에서 문제에 지정된 호스트로 이동한다.
ssh <task-host>

# 접속한 호스트에서 확인한다.
hostname
kubectl config current-context

# 문제에서 context 전환을 지시한 경우에 실행한다.
kubectl config use-context <required-context>
kubectl get namespaces
```

조회·수정 명령에는 문제에서 요구한 `-n <namespace>`를 붙인다. 노드의 systemd·패키지를 수정하는 문제라면 그 노드가 실제 작업 호스트인지도 확인한다. 다른 호스트로 이동할 때는 먼저 `exit`으로 base에 돌아온다.

## 3. 터미널 설정

이미 설정되어 있는 항목은 그대로 사용한다. 다음은 Bash에서 필요한 경우 추가하는 예다.

```bash
source <(kubectl completion bash)
alias k=kubectl
complete -F __start_kubectl k
export do="--dry-run=client -o yaml"

# 클러스터에 생성하지 않고 YAML 뼈대 저장
k run nginx --image=nginx $do > pod.yaml
```

YAML 편집용 `~/.vimrc` 설정:

```vim
set ts=2 sw=2 sts=2 et
```

원격 Linux 터미널의 복사·붙여넣기는 `Ctrl+Shift+C` / `Ctrl+Shift+V`를 사용한다. 환경별 단축키는 시험 UI 안내를 우선한다.

## 4. 풀이와 검증

1. 문제의 요구사항과 기존 리소스를 조회한다.
2. 명령형 생성 또는 공식 YAML 예제로 변경 내용을 준비한다.
3. 이름·namespace·selector·포트·파일 경로를 확인하고 적용한다.
4. `get`, `describe`, `rollout status`, 실제 통신 등 요구사항에 맞는 방법으로 검증한다.
5. 파일 저장 문제는 지정 경로의 내용을 확인한다. 완료하면 SSH 세션에서 나온다.

배점과 예상 소요 시간으로 풀이 순서를 정한다. 특정 문제가 반드시 출제된다고 전제하거나 외운 배점을 기준으로 시간을 배분하지 않는다.

## 관련 문서

- [CKA 2주 학습 계획](Study_Plan_2Weeks.md)
- [JSONPath와 명령형 명령 치트시트](JSONPath_Cheatsheet.md)
- [Killer.sh 활용과 응시 준비](Killer_sh_Strategy.md)
