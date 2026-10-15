# fsGroup 환경에서 Java의 0700 디렉터리가 02700이 된 이유

Java에서 `0700`으로 디렉터리를 만들었는데 실제 권한이 `02700`이면, 부모 디렉터리의 SGID 비트부터 확인할 수 있다. Linux에서는 부모에 SGID가 있으면 새 하위 디렉터리에도 상속된다. 개인 Platform Lab의 readiness 초기화에서는 이 동작과 엄격한 권한 검사가 충돌했다.

이 사례는 Java 21·Linux K3s의 별도 합성 Pod에서 확인했다. 처음 실패한 canary 로그에는 일반 오류만 있었고, 이후 같은 이전 이미지와 설정으로 디렉터리 mode와 생성자 예외를 직접 재현했다. 수정 후보의 Linux CI와 수정 이미지의 격리 canary에 이어 실제 worker의 Ready 전환과 진행 기록을 쓴 프로세스의 준비 상태, 자료 보존을 확인했다. 유휴 worker 교체와 같은 ID의 읽기 전용 재시도까지 검증했지만 이전 컨테이너의 exit는 관측하지 못했다.

## 컨테이너 시작과 worker 준비를 구분하려 했다

상시 worker가 시작됐다는 것과 DB journal commit·소유권 확인을 마쳐 작업을 처리할 준비가 됐다는 것은 다르다. 이를 구분하려고 작업을 수행하는 스레드가 마지막 stage 경계에서 기록한 파일을 별도 Java exec probe로 검사하는 방식을 만들었다. 파일에는 PID/start ticks·Pod UID·source·진행 상태·만료 시점을 담고, 다른 process나 이전 실행의 파일은 거부하도록 했다.

진행 파일의 부모 디렉터리는 소유자가 worker UID이고 mode가 정확히 `0700`이어야 한다. 파일은 `0600`을 요구한다. 문제는 파일을 쓰기 전, 부모 디렉터리를 만드는 생성자에서 발생했다.

다음은 격리 Pod의 관련 설정을 발췌한 것이다. 실행할 수 있는 전체 manifest는 아니다.

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 10001
  runAsGroup: 10001
  fsGroup: 10001
volumes:
  - name: tmp
    emptyDir:
      sizeLimit: 100Mi
```

이 emptyDir을 `/tmp`에 마운트했다. `fsGroup`은 이를 지원하는 볼륨의 그룹 소유권·권한 관리에 관여하며 실제 적용 방식은 볼륨 종류와 드라이버에 따라 달라진다. 이 사례에서는 마운트한 부모 디렉터리에 SGID가 있는 것을 직접 관측했다. [Kubernetes security context](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)

## 첫 로그만으로는 원인을 알 수 없었다

첫 격리 canary는 첫 사례를 실행하기 전에 exit 1로 끝났다. 로그에서 확인한 내용은 다음과 같았다.

```json
{
  "failureCode": "CANARY_EXECUTION_FAILED",
  "passed": false,
  "cases": []
}
```

이 기록에는 예외 class나 stack이 없었다. 종료한 Pod의 emptyDir도 kubelet이 제거해 원래 디렉터리 mode를 사후에 읽을 수 없었다. 코드에서 SGID 상속을 의심할 수는 있었지만, 이 로그만으로 실제 예외 위치까지 확정할 수는 없었다.

실패한 결과와 Pod/Job/ConfigMap 선언·로그를 먼저 보관했다. 이후 종료한 테스트 Pod와 비활성 Job만 UID로 정리하고, 같은 namespace·quota·격리 네트워크 정책을 유지한 채 별도 진단을 실행했다. 진단에는 첫 이미지를 사용했다. writer는 기존 canary와 동일한 Java 소스에서 컴파일한 class 바이트를 다시 주입했고, probe는 이미지에 들어 있는 실제 class를 로드했다.

진단은 DB·lease·Kafka·S3에 연결하지 않고 새 emptyDir 안에서 생성자만 호출했다. 2026-10-15의 직접 관측 결과는 다음과 같았다.

| 관측 대상 | 결과 |
| --- | --- |
| process UID | 10001 |
| 부모 디렉터리 | SGID 있음, 진단 전후 권한 같음 |
| 새 디렉터리 | 요청한 mode는 0700, 관측한 mode는 02700 |
| 생성자 | `IllegalArgumentException`으로 거부 |
| 자체 stack | `RuntimeReadyProbe.privateDirectory` → `LocalRuntimeProgress.<init>` 경로 확인 |
| health record·권한 변경 | 진단 중 수행하지 않음 |

원본 진단 JSON의 mode 값 `1472`는 10진수이며, 8진수로 쓰면 `02700`이다. 기존 작업 7개·업무 SQL·전역 리소스 식별자를 보존했고, 같은 기존 객체 21개를 전후 전체 GET해 바이트가 같음을 비교했다. 이 결과는 별도 Pod에서 확인한 재현이며 첫 실패 컨테이너의 누락된 stack을 복원한 것은 아니다.

## 0700 요청이 SGID 상속을 막지는 않았다

기존 생성 코드는 다음과 같은 흐름이었다.

```java
// 기존 LocalRuntimeProgress 생성자 흐름 발췌
Files.createDirectory(
    directory,
    PosixFilePermissions.asFileAttribute(
        PosixFilePermissions.fromString("rwx------")));
RuntimeReadyProbe.privateDirectory(directory, expectedUid);
```

`Files.createDirectory`는 디렉터리 생성과 지정 속성의 적용을 원자적으로 수행하는 API다. 하지만 지정한 POSIX 권한이 Linux의 디렉터리 SGID 상속 규칙을 없애 주는 것은 아니다. [Java 21 Files.createDirectory](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/nio/file/Files.html#createDirectory(java.nio.file.Path,java.nio.file.attribute.FileAttribute...))

[Linux mkdir(2)](https://man7.org/linux/man-pages/man2/mkdir.2.html)는 부모 디렉터리에 SGID가 있으면 새 디렉터리에도 그 비트가 생긴다고 설명한다. 이번에는 owner의 `rwx`와 group/other의 권한 없음이 유지된 채 SGID 비트가 더해져 `02700`이 됐다. 검사는 특수 비트를 포함한 `mode & 07777`을 `0700`과 비교했으므로 거부가 발생했다.

여기서 `fsGroupChangePolicy: OnRootMismatch`로 바꾸는 것은 emptyDir의 해결책이 아니다. Kubernetes 문서는 이 정책이 emptyDir 같은 ephemeral 볼륨에는 적용되지 않는다고 명시한다. [fsGroupChangePolicy의 적용 범위](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/#configure-volume-permission-and-ownership-change-policy-for-pods)

## 이번에 새로 만든 inode만 교정했다

기존 디렉터리에 무조건 `chmod 700`을 하면 예상하지 못한 경로나 다른 파일을 조용히 수리할 수 있다. 수정은 디렉터리가 없었고 이번 `createDirectory` 호출이 성공한 경우에만 적용했다.

1. `NOFOLLOW_LINKS`로 실제 디렉터리인지 확인한다. owner가 예상 UID이고 `fileKey`가 있으며 mode가 `0700` 또는 `02700`인 경우만 허용한다.
2. `02700`이면 그 새 디렉터리의 SGID만 제거해 `0700`으로 맞춘다.
3. 다시 읽은 `fileKey`와 디렉터리 여부를 비교한다.
4. 기존의 엄격한 `privateDirectory` 검사를 그대로 수행한다.

수정 후 생성 흐름을 줄여 쓰면 다음과 같다. 검증 helper의 전체 구현은 [PR #43](https://github.com/DevDooly/devdooly-platform-lab/pull/43)에 있다.

```java
// 수정된 생성 흐름 발췌: 이미 존재한 경로는 교정 helper를 거치지 않는다.
if (!Files.exists(directory, LinkOption.NOFOLLOW_LINKS)) {
    Files.createDirectory(directory,
        PosixFilePermissions.asFileAttribute(
            PosixFilePermissions.fromString("rwx------")));
    clearNewDirectoryInheritedSetgid(directory, expectedUid);
}
RuntimeReadyProbe.privateDirectory(directory, expectedUid);
```

기존 `02700`·group-writable 디렉터리와 symlink는 여전히 거부한다. 부모 권한도 바꾸지 않는다. `unix:mode` 속성으로 특수 비트를 다루는 이 구현은 Linux worker 전용이며, 모든 파일시스템에서 쓸 수 있는 이식성 있는 Java 권한 유틸리티는 아니다.

## Linux 테스트와 수정 이미지의 격리 확인

[실제 Linux CI 실행 38746521878](https://github.com/DevDooly/devdooly-platform-lab/actions/runs/38746521878)은 수정 후보 `6a5305b670dd53f9b56a9638b64917575a232737`에서 API 180개·독립 Java 예제 20개, 총 200개의 JUnit을 실행했다. 실패·오류·skip은 모두 0이었다. 그중 writer suite 9개에는 다음 네 회귀가 포함됐다.

- SGID 부모 아래 새 디렉터리에서 상속을 재현하고, 수정 생성자가 자식만 `0700`으로 바꾸는지 확인한다.
- 기존 `02700` 디렉터리는 거부하고 권한을 그대로 두는지 확인한다.
- 기존 group-writable 디렉터리는 거부하고 권한을 그대로 두는지 확인한다.
- symlink를 거부하고 대상의 권한을 바꾸지 않는지 확인한다.

이전 Windows 실행에서는 POSIX 사례를 skip했으므로 해당 결과만으로 Linux 디렉터리 동작을 검증했다고 볼 수 없었다. Linux CI에서는 네 사례가 실제 실행됐다. 200개라는 합계에는 웹 검사나 미니 PC canary 사례를 더하지 않았다.

수정 PR은 직접 진단과 정리를 마친 뒤 main에 반영했다. 새 소스 `3e0d85be`의 Jenkins build 39에서도 JUnit 합계 200개와 필수 산출물·소스를 확인했다. 익명 registry와 K3s cache, 실제 OCI class를 대조한 뒤 수정 이미지로 별도 canary를 실행했다. 이때도 health class는 이미지에 실제 들어 있는 것을 사용했다.

수정 canary는 10개 사례를 통과했다. writer의 STARTING은 거부하고 READY는 허용했으며, 다른 source·시작 ticks·PID, 만료 record·잘못된 mode·손상 bytes와 terminal latch를 각각 확인했다. 종료한 자체 Pod와 Job은 UID로 정리했고 첫 실패 결과는 그대로 보존했다.

이 중 READY는 DB commit 없이 합성 callback을 호출한 파일 검사다. 만료는 과거 boot timestamp로 만든 record를 사용했으므로 240초를 실제로 기다리지 않았다. 시작 ticks 불일치도 실제 worker를 재시작한 결과가 아니다.

| 열 개 probe 실행의 관측값 | 실제 범위 또는 최대 |
| --- | ---: |
| 한 번의 wall time | 83.525~205.318ms |
| 마지막 생존 표본의 CPU 시간 | 30~130ms |
| RSS 표본 최대 | 약 40.789MiB |
| PSS 표본 최대 | 약 25.106MiB |

Java 21 child는 heap 8~16MiB·Serial GC·ActiveProcessorCount 1로 실행했다. CPU 시간은 마지막 생존 표본에서 읽은 하한이며 RSS/PSS는 4~9개 표본의 최대다. 최종 CPU 시간이나 lifetime peak, 운영 worker에 주기적으로 probe를 붙였을 때의 장기 비용은 아니다.

## 배포 전 관측을 먼저 시작했다

[PR #44](https://github.com/DevDooly/devdooly-platform-lab/pull/44)로 API·웹부터 바꾸고 당시 worker는 이전 소스로 유지했다. 배포 전 보존 검사 21/21과 API·웹 전환 뒤 25/25를 통과했고, 각 단계에서 같은 기존 객체 21개를 전체 GET해 비교했다.

worker-only [PR #45](https://github.com/DevDooly/devdooly-platform-lab/pull/45)를 반영하기 전에는 읽기 전용 watch가 실제 이전 worker를 읽었는지, 그 관측 process가 여전히 살아 있는지 확인했다. 이후 실제 NotReady→Ready를 관측했다. 이 watch 자체는 객체를 GET하거나 전체 SQL·리소스를 비교하지 않았다.

별도 after 검사는 보존 23/23과 기존 객체 21개의 전체 GET·바이트 비교를 통과했다. 같은 process의 source·식별자·소유 프로세스의 DB 진행 기록이 RUNNING인지·신선한 heartbeat를 대조하고 기존 작업 7개와 업무 SQL·리소스를 보존했다. after의 `readyTransitionObserved:false`는 그 검사에서 새 전환을 다시 관측하지 않았다는 뜻이며, 앞선 watch의 성공과 모순되지 않는다.

## 유휴 worker를 교체한 뒤 같은 작업을 다시 제출했다

후속 검사 10/10에서는 내부 명령으로 고정 V1 입력 12개를 접수해 성공 7·실패 3·중복 2·대기 0을 확인했다. 실제 승인 정책에는 다음 허용까지 30초가 부과됐으며 전체 작업은 8개가 됐다. 작업이 끝나 슬롯이 빈 상태에서 이전 worker UID와 grace 300초를 지정해 한 번 교체하고, 새 Pod의 NotReady→Ready를 다시 관측했다.

이전 worker의 exit는 `UNOBSERVED`였다. 새 Pod의 복구가 관측됐다는 것과 이전 컨테이너가 exit 0/143 또는 SIGTERM으로 정상 종료했다는 것은 다른 근거가 필요하다. 이번 기록은 grace 300초를 지정한 유휴 worker 교체와 복구까지 다룬다.

그다음 실제 ACL을 확인한 RO credential로 같은 ID를 재시도했다. read만 허용하고 write·owner·createBucket을 허용하지 않은 조건에서 성공했으며, 받아들여진 새 S3 write나 승인 정책 재부과는 없었다. 접수 전 기존 객체 21개, 접수 뒤 24개, RO 재시도 뒤 같은 24개를 전체 GET해 검증했다. 최종 Kafka offset·log end는 각각 8, lag는 0이고 슬롯은 비었다. 전체 8개 작업이 COMPLETED·EXPORTED였다. 테스트 뒤에는 자체 RO 키와 Secret만 회수하는 3/3 검사도 통과했다.

HTTP PUT 시도 횟수나 다른 새 ID의 실제 운영 cooldown 거부는 계측하지 않았다. 운영 worker의 진행 중 작업이나 호스트를 중단하는 복구 경계, 장기간 주기적인 probe 비용은 후속으로 남는다.

readiness 실패는 컨테이너를 강제로 재시작시키는 신호가 아니다. 이 worker는 public Service 트래픽을 받지 않으므로 Ready 상태만으로 Kafka 소비를 멈추거나 lease를 해제한다고 기대해서도 안 된다. 마지막 stage의 신선도 검사와 외부 시스템의 지속적인 건강 검사는 별개의 조건이다. [Kubernetes probe의 역할](https://kubernetes.io/docs/concepts/workloads/pods/probes/)

관련 TIL: [Pod 문제 진단과 probe 구분](../Infrastructure/Kubernetes/CKA/Troubleshooting_Pods.md), [Java 데몬의 K8s 리소스 산정](../Language/Java/Java_Resource_Sizing_in_K8s.md)
