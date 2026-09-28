# Kubernetes Java 데몬 리소스 산정: CPU, JVM, Virtual Thread

Java 서비스의 처리량은 CPU 시간, JVM의 병렬 처리 규모, 처리 중 요청 수, 메모리와 외부 시스템 용량이 함께 결정한다. `limits.cpu`와 `-XX:ActiveProcessorCount`를 같은 숫자로 맞추는 것만으로 리소스 산정이 끝나지는 않는다. 먼저 자동 인식값을 확인하고, 같은 부하에서 지연·throttling·메모리·대기열을 비교해 조정한다.

Linux 컨테이너의 **HotSpot JDK 25**를 기준으로 설명한다. JDK 21–23의 가상 스레드 pinning 차이는 별도로 표시한다. Kubernetes 예제는 컨테이너별 resources를 사용하며, Pod 수준 리소스 제한·CPU Manager·노드 정책을 사용한다면 실제 적용된 cgroup도 확인한다.

## 1. 서로 다른 제한을 먼저 구분한다

| 설정 | 제어하는 것 | 함께 확인할 값 |
| :--- | :--- | :--- |
| `requests.cpu` | 스케줄링 시 필요한 CPU와 경합 시 CPU 배분의 기준 | 평상시 CPU 사용량, 노드 경합, HPA 기준 |
| `limits.cpu` | cgroup이 사용할 수 있는 CPU 시간의 상한 | 짧은 구간의 throttling, p95/p99, 기동 시간 |
| `-XX:ActiveProcessorCount=N` | JVM이 사용하는 가용 프로세서 수를 정수 `N`으로 재정의 | `availableProcessors()`, GC와 CPU 수 기반 풀 |
| `jdk.virtualThreadScheduler.parallelism` | 가상 스레드 스케줄러의 목표 병렬도 | 실행 대기 가상 스레드, carrier 사용량 |
| 애플리케이션 동시성 제한 | 동시에 받아 두거나 실행할 요청·작업 수 | in-flight, 큐 길이, timeout, 거절 수 |
| `requests.memory` / `limits.memory` | 메모리 스케줄링 기준 / 컨테이너 메모리 상한 | heap 외 메모리까지 포함한 실제 사용량 |
| `-Xmx` | Java heap의 최대 크기 | GC 후 살아 있는 객체, 할당률, GC 지연 |

CPU request와 limit의 단위는 CPU이며 `1000m = 1 CPU`, `500m = 0.5 CPU`다. CPU 제한은 throttling으로, 메모리 제한은 메모리 회수와 OOM kill로 나타날 수 있다. `requests.memory`가 JVM heap 크기를 정하지는 않는다. [Kubernetes 리소스 관리](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)

## 2. CPU limit은 코어 개수보다 CPU 시간으로 이해한다

일반적인 공유 CPU 환경에서 `limits.cpu: "1"`은 특정 코어 하나를 전용으로 받는 설정이 아니다. 여러 스레드가 여러 CPU에서 실행되어도 같은 cgroup의 CPU 시간 예산을 함께 소비한다.

예를 들어 quota period가 100ms이고 quota가 50ms이면 `500m`에 해당한다. 여러 스레드가 동시에 실행하면 합산 CPU 시간을 더 빨리 소진할 수 있다. 남은 주기 동안 throttling되면 분 단위 평균 CPU는 낮아도 짧은 요청의 지연은 늘어날 수 있다. 실제 period와 quota는 환경에서 읽는다. [Linux cgroup v2의 `cpu.max`](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html#cpu)

`requests.cpu: 500m`, `limits.cpu: "2"`이면 스케줄링은 0.5 CPU 요청을 기준으로 하지만, 여유가 있을 때 최대 2 CPU까지 사용할 수 있다. 모든 Pod가 동시에 limit만큼 CPU를 필요로 할 때도 그 용량을 확보했다는 뜻은 아니다. 반대로 request만 있고 limit이 없다면 노드의 가용 자원을 더 사용할 수 있으나 경합 시 성능은 달라진다.

### CPU limit을 둘지 판단하는 기준

- **공유 클러스터에서 사용량 상한이 필요함**: limit을 두고 부하·기동 시 throttling을 측정한다. 평균 사용량에 너무 가깝게 잡으면 JIT·GC·순간 부하를 처리할 여유가 줄어든다.
- **지연이 중요하고 운영 정책이 허용함**: CPU limit을 생략하는 후보도 비교한다. 적절한 request, 노드 용량, 애플리케이션 동시성 상한은 유지한다. LimitRange나 admission 정책이 limit을 추가하는지도 확인한다.
- **CPU 격리가 필요함**: CPU Manager의 `static` 정책과 Guaranteed Pod, 정수 CPU request 등의 조건을 검토한다. `request = limit`만 설정했다고 전용 CPU가 생기지는 않는다. [CPU Manager 정책](https://kubernetes.io/docs/tasks/administer-cluster/cpu-management-policies/)

CPU limit 생략이나 `request = limit`을 모든 서비스의 기본 정답으로 삼지 않는다. request를 낮추면 스케줄러가 더 많은 Pod를 같은 노드에 배치할 수 있고, request를 높이면 비용·배치 가능성·HPA 동작도 바뀐다.

컨테이너별 resources로 Guaranteed QoS를 구성하려면 sidecar를 포함한 모든 컨테이너에 CPU·메모리 request와 limit을 지정하고 각각 같게 맞추는 조건도 충족해야 한다. CPU 값만 같게 두는 것으로는 충분하지 않다. [Pod QoS 조건](https://kubernetes.io/docs/concepts/workloads/pods/pod-qos/)

## 3. `ActiveProcessorCount`는 언제 지정하는가

정확한 옵션 이름은 **`-XX:ActiveProcessorCount`**다. JVM이 가용 CPU 수를 바탕으로 정하는 GC 스레드 수와 ForkJoinPool 등의 기본값에 영향을 준다. 애플리케이션과 라이브러리가 `Runtime.getRuntime().availableProcessors()`로 풀 크기를 정한다면 그 값도 달라진다. 명시적으로 크기를 정한 풀까지 일괄 재설정하지는 않는다. [JDK 25 Java 명령](https://docs.oracle.com/en/java/javase/25/docs/specs/man/java.html#advanced-runtime-options-for-java)

이 옵션은 cgroup quota, cpuset, Kubernetes request/limit을 변경하지 않는다. `limits.cpu: "1"`에 `ActiveProcessorCount=8`을 주어도 8 CPU의 실행 시간을 얻지 못한다. `ActiveProcessorCount=1` 역시 프로세스 전체를 OS 스레드 하나로 제한하지 않는다.

### 자동 인식값과 소수 CPU

HotSpot은 컨테이너 인식이 정상 동작하면 CPU affinity와 quota 등을 반영한다. JDK 25의 quota 계산은 `ceil(quota / period)`이며, OS가 허용한 CPU 수로 다시 제한한다. 다음은 별도 override가 없고 충분한 CPU affinity가 허용된 경우의 예다.

| CPU request | CPU limit | 예상 `availableProcessors()` | 해석 |
| :--- | :--- | :--- | :--- |
| `250m` | `500m` | `1` | JVM은 정수 1을 보지만 실제 시간 예산은 0.5 CPU |
| `500m` | `"1"` | `1` | request와 limit의 역할이 다름 |
| `500m` | `1500m` | `2` | 올림된 2가 2 CPU 시간 보장을 뜻하지 않음 |
| `"1"` | `"2"` | `2` | CPU 경합 시 지속적으로 2 CPU를 쓰지 못할 수 있음 |
| `500m` | 없음 | affinity가 허용한 CPU 수 | request만 보고 1로 정해지지 않음 |

계산 근거는 [JDK 25 `CgroupUtil::processor_count`](https://github.com/openjdk/jdk/blob/jdk-25%2B36/src/hotspot/os/linux/cgroupUtil_linux.cpp)다. 부모 cgroup의 제한, CPU Manager, JVM 패치 버전·컨테이너 인식 상태에 따라 실제 결과를 확인해야 한다. 특히 최근 HotSpot은 CPU shares/weight를 가용 CPU 수의 상한으로 사용하지 않는다. 오래된 JDK의 request 기반 계산 설명을 그대로 적용하지 않는다. [JDK-8281181](https://bugs.openjdk.org/browse/JDK-8281181)

### 설정 순서

1. **처음에는 생략한다.** 실제 앱의 `availableProcessors()`, GC 종류, 생성된 풀 크기를 기록한다.
2. **CPU limit이 없고 JVM이 노드의 큰 CPU 수를 인식한다면** 서비스에 맞는 작은 정수 후보를 비교한다. GC·라이브러리 풀이 지나치게 커졌는지가 판단 근거다.
3. **소수 CPU limit에서는** 자동 인식값을 출발점으로 둔다. `500m`에 `0.5`를 넣을 수 없으며, `1`과 `2`의 비교도 실제 지연·throttling·GC 결과가 있을 때 의미가 있다.
4. **가상 스레드 스케줄러만 조정하려면** 해당 parallelism을 별도로 비교한다. JVM 전체 CPU 인식값을 바꾸면 GC와 다른 풀도 영향을 받는다.
5. **리소스나 노드 풀을 바꾼 뒤에는** 다시 측정한다. 기존에 생성된 풀과 heap 설정이 새 제한에 맞춰 모두 자동 변경된다고 가정하지 않는다.

가용 CPU 수가 달라지면 자동 선택되는 GC나 GC 병렬도도 달라질 수 있다. `UseG1GC`, `UseSerialGC`, `ParallelGCThreads`, `ConcGCThreads` 등 실제 플래그를 확인하고 CPU 옵션 하나의 효과로 오해하지 않는다.

## 4. Virtual Thread의 병렬도와 요청 수를 따로 관리한다

가상 스레드가 Java 코드를 실행할 때는 carrier라고 부르는 플랫폼 스레드에 올라간다. 지원되는 블로킹 I/O에서 대기할 때는 carrier를 반납할 수 있어 많은 요청을 적은 플랫폼 스레드로 처리할 수 있다. CPU를 사용하는 압축·암호화·JSON 변환·연산 작업은 계속 CPU 시간을 소비한다.

| 항목 | 의미 | 동시 요청 수와의 관계 |
| :--- | :--- | :--- |
| `jdk.virtualThreadScheduler.parallelism` | 기본값은 가용 프로세서 수인 목표 병렬도 | 대기 중인 가상 스레드 수를 제한하지 않음 |
| `jdk.virtualThreadScheduler.maxPoolSize` | 일부 carrier 블로킹을 보상할 때 늘어나는 플랫폼 스레드 수의 상한 | 가상 스레드 생성 수나 요청 수의 상한이 아님 |
| `ForkJoinPool.commonPool()` | parallel stream과 일부 비동기 작업에 쓰이는 별도 풀 | VT 스케줄러와 별개로 CPU를 경쟁함 |
| `newVirtualThreadPerTaskExecutor()` | 작업마다 가상 스레드를 생성하는 실행기 | 제출량에 대한 별도 제한이 필요함 |

JDK 25 구현에서 `maxPoolSize` 미지정 시 기본값은 `max(parallelism, 256)`이다. 일부 블로킹 보상과 pinning은 동작이 다르므로 이 값을 높이는 것을 pinning 해결책으로 쓰지 않는다. [JDK 25 스케줄러 구현](https://github.com/openjdk/jdk/blob/jdk-25%2B36/src/java.base/share/classes/java/lang/VirtualThread.java), [JEP 444 스케줄링](https://openjdk.org/jeps/444)

`-XX:ActiveProcessorCount=2`를 쓰면 기본 VT parallelism도 보통 2에서 시작한다. `-Djdk.virtualThreadScheduler.parallelism=4`를 별도로 주면 VT 스케줄러의 목표 병렬도는 4가 되지만, CPU quota와 DB 연결 수는 그대로다. 먼저 기본값을 측정하고 변경할 이유가 있을 때 한 설정씩 비교한다.

### 가상 스레드로 전환할 때 확인할 코드

- **유입 상한**: HTTP 요청, 메시지 prefetch, batch 크기와 executor 제출량을 제한한다. 처리 중 요청과 대기 중 요청을 모두 세며, 대기 시간·timeout·거절 또는 소비 중단 정책을 정한다.
- **외부 시스템별 상한**: DB connection pool, 외부 HTTP 연결 풀, FTP/SFTP 세션 수를 따로 관리한다. Semaphore로 실행 수만 제한하면 대기 가상 스레드는 계속 늘 수 있다.
- **CPU 작업**: CPU를 오래 점유하는 작업의 동시성을 제한한다. 별도 실행기로 분리해도 같은 컨테이너의 CPU 시간은 공유하며, 강한 격리가 필요하면 별도 서비스나 워커로 분리한다.
- **실제 실행기**: VT 안에서 호출한 `CompletableFuture.supplyAsync()`가 자동으로 VT 실행기를 쓰지는 않는다. 명시적인 executor가 없는 async 메서드는 JDK 기본 비동기 실행기를 사용한다. 기존 `@Async`, parallel stream, 라이브러리 풀을 확인한다. [CompletableFuture 실행 정책](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/CompletableFuture.html)
- **ThreadLocal**: 플랫폼 스레드 풀에서 소수만 존재하던 버퍼·캐시를 요청별 VT마다 만들면 heap 사용이 커진다. 외부 연결 같은 비싼 자원은 별도 풀로 관리한다.

가상 스레드를 고정 풀로 재사용하기보다 보호하려는 자원의 동시성에 상한을 둔다. [JEP 444의 풀과 ThreadLocal 안내](https://openjdk.org/jeps/444)

### Pinning과 일반적인 대기를 구분한다

JDK 21–23에서는 `synchronized` 안의 블로킹이 carrier를 붙잡는 pinning을 일으킬 수 있다. JDK 24부터 JEP 491이 이 제약을 개선했으며 JDK 25에도 포함된다. native/foreign 코드가 Java로 돌아와 블로킹하는 경로 등은 별도로 확인한다. `synchronized`가 개선되어도 락 경합과 작업 직렬화 자체는 남는다.

JDK 24 이상에서는 `jdk.tracePinnedThreads`가 제거되어 지정해도 효과가 없다. JFR의 `jdk.VirtualThreadPinned` 이벤트, 스레드 덤프와 실제 호출 스택으로 판단한다. [JEP 491](https://openjdk.org/jeps/491), [저장소의 pinning 진단 절차](Virtual_Threads_FTP_Pinning.md)

## 5. CPU·동시성·외부 연결 수를 계산하는 순서

다음 수치는 계산을 설명하기 위한 가정이다. 운영값은 대표적인 요청 구성과 데이터 크기로 측정한다.

### CPU는 요청당 CPU 시간으로 출발한다

```text
필요한 평균 CPU ≈ 초당 처리량 × 요청당 CPU 시간(초) + 백그라운드 CPU
확보할 CPU 후보 ≈ 필요한 평균 CPU / 목표 사용 비율

Pod당 200건/초 × 0.003 CPU초/건 + 0.1 CPU = 0.7 CPU
목표 사용 비율을 70%로 가정하면 0.7 / 0.7 = 1 CPU
```

응답 시간 150ms 중 DB 대기가 147ms라면 150ms 전체를 CPU 시간으로 계산하지 않는다. 컨테이너 전체 CPU를 처리 건수로 나눴다면 이미 포함된 GC·백그라운드 비용을 다시 더하지 않는다. 심하게 throttling된 측정값은 처리하지 못한 수요를 보여주지 못하므로 제한을 바꾼 비교도 필요하다.

이 예에서는 CPU request 1을 후보로 두고, 순간 부하·기동에 필요한 limit과 replica 수를 시험한다. CPU 모델, 아키텍처, JIT warm-up, 캐시 적중률, GC와 APM 유무가 바뀌면 요청당 CPU 비용도 다시 잰다.

### 처리 중 요청 수는 대기 시간이 길어지면 증가한다

안정된 구간의 평균에는 Little's Law를 적용할 수 있다.

```text
평균 처리 중 요청 수 ≈ 초당 처리량 × 평균 체류 시간

200건/초 × 0.15초 = 30건
200건/초 × 2초 = 400건
```

외부 시스템이 느려져 체류 시간이 2초가 되면 같은 유입에도 훨씬 많은 요청을 메모리에 보관한다. 두 번째 계산은 같은 처리량을 유지할 수 있다는 가정이며, 실제 과부하에서는 대기열이 계속 증가할 수 있다. 평균 계산값을 곧바로 최대 동시성으로 쓰지 말고 burst·tail latency·timeout·요청 크기를 반영해 부하 시험한다.

### 외부 연결 예산은 최대 Pod 수로 계산한다

```text
최대 동시 연결 후보
  = 동시에 살아 있는 앱 Pod 수 × Pod당 connection pool 상한
  + 다른 서비스·운영 도구의 연결 수
```

HPA `maxReplicas`뿐 아니라 rollout의 추가 Pod, 종료 중이지만 아직 연결을 가진 Pod도 포함한다. 가령 12개 Pod가 살아 있고 pool 상한이 20이면 앱 연결만 최대 240개다. DB가 허용할 수 없는 수라면 Pod 수·pool 크기·처리 동시성을 함께 조정한다. 연결을 늘려도 DB 처리량이 늘지 않는 구간에서는 대기와 경합만 커질 수 있다.

많은 연결을 여는 서비스는 파일 디스크립터, 소켓·포트, 프록시와 외부 서비스의 연결·요청 제한도 확인한다. 가상 스레드가 저렴해져도 연결마다 쓰는 자원과 네트워크·디스크 처리 용량은 따로 남는다.

## 6. 메모리는 heap과 컨테이너 전체를 함께 산정한다

```text
컨테이너 메모리 예산
  = 최대 heap 예산
  + metaspace·code cache·GC native 구조
  + direct buffer·JNI·APM 등 native 메모리
  + carrier를 포함한 플랫폼 스레드 stack
  + 같은 컨테이너의 다른 프로세스·cgroup에 계산되는 파일/소켓 메모리
  + 피크 변동을 위한 여유
```

가상 스레드의 stack chunk는 **heap 안에** 저장된다. VT 수에 `-Xss`를 곱한 값을 native 메모리로 다시 더하지 않는다. 다만 대기 중인 요청 객체, 본문, ThreadLocal, stack chunk는 heap을 유지하므로 VT가 많아지면 heap과 GC 비용은 커질 수 있다. [JEP 444 메모리 설명](https://openjdk.org/jeps/444)

### `-Xmx`와 `MaxRAMPercentage`

`-Xmx`는 heap 상한을 직접 정하고, `-XX:MaxRAMPercentage`는 JVM이 heap 산정에 사용하는 가용 메모리에 대한 비율이다. 컨테이너 인식이 정상이고 다른 override가 없다면 메모리 limit이 이 산정에 반영된다. memory request 기준 비율로 해석하지 않는다.

둘을 무심코 함께 지정하지 말고, 실제 `MaxHeapSize`를 확인한다. `-Xmx`를 명시했다면 그 heap 상한을 기준으로 검증한다. 비율만 높여 limit 대부분을 heap에 주면 native 메모리나 파일 처리 여유가 부족해질 수 있다. `-Xms = -Xmx` 역시 기동·상주 메모리와 GC 특성을 측정한 뒤 선택한다. [JDK 25 heap 옵션](https://docs.oracle.com/en/java/javase/25/docs/specs/man/java.html#advanced-garbage-collection-options-for-java)

예를 들어 `limits.memory: 2Gi`, `-Xmx1024m`이면 나머지 약 1Gi를 heap 밖 사용량과 여유로 남긴다. 이것이 충분한지는 APM·direct buffer·클래스 수·플랫폼 스레드 수·파일 처리량에 달려 있다. 부하에서 측정한 상주 사용량과 변동을 바탕으로 memory request도 정한다.

### 놓치기 쉬운 메모리와 저장 공간

- Java 프로세스의 RSS, cgroup 전체 사용량, `container_memory_working_set_bytes`, JVM heap used는 서로 다른 값이다. working set 하나를 OOM까지 남은 정확한 메모리로 해석하지 않는다.
- `emptyDir.medium: Memory`에 쓴 데이터는 메모리를 사용한다. 큰 임시 파일·heap dump를 넣는다면 크기 제한과 메모리 예산을 함께 잡는다. 디스크 기반 `emptyDir`은 ephemeral storage 사용량과 노드 디스크 용량도 확인한다. [Kubernetes 볼륨](https://kubernetes.io/docs/concepts/storage/volumes/#emptydir)
- sidecar는 자기 컨테이너의 resources를 가진다. 앱 heap은 앱 컨테이너의 제한으로 산정하고, 배치 용량은 sidecar와 Pod overhead까지 합쳐 본다. Pod 수준 제한이 있으면 공유되는 상한도 추가로 확인한다.
- Java `OutOfMemoryError`와 컨테이너 `OOMKilled`를 구분한다. 종료 코드 137만으로 원인을 확정하지 않고 Pod 종료 사유·이벤트와 JVM 로그를 대조한다. OS가 프로세스를 종료하면 JVM heap dump가 남지 않을 수 있다.

## 7. 설정 예제와 Java 데몬의 생명주기

아래는 Deployment의 `spec.template.spec`에 넣을 **PodSpec 발췌**다. 이미지·요청량·건강 상태 확인 방식은 실제 서비스에 맞춘다. CPU request 1, limit 2와 memory request 1536Mi, limit 2Gi는 앞 계산에서 시작할 시험 후보이며 공통 권장값이 아니다.

```yaml
terminationGracePeriodSeconds: 60
containers:
  - name: app
    image: registry.example.com/team/java-worker:validated
    resources:
      requests:
        cpu: "1"
        memory: 1536Mi
      limits:
        cpu: "2"
        memory: 2Gi
    env:
      - name: JAVA_TOOL_OPTIONS
        value: >-
          -Xms256m -Xmx1024m
          -Xlog:gc*,safepoint:stdout:time,uptime,level,tags
```

처음에는 `ActiveProcessorCount`와 VT scheduler 옵션을 생략해 자동 인식값을 측정한다. 이미지의 시작 스크립트가 다른 JVM 옵션을 추가하는지도 확인한다. 일반적인 `JAVA_OPTS` 변수는 JVM이 자동으로 읽는 표준 변수가 아니므로 시작 스크립트에서 실제 사용하는지 확인해야 한다.

### Spring Boot와 백그라운드 워커

Spring Boot 3.5에서 가상 스레드를 사용하는 예는 다음과 같다.

```yaml
spring:
  threads:
    virtual:
      enabled: true
  main:
    keep-alive: true
```

가상 스레드는 daemon thread다. 웹 서버 등 JVM을 유지할 non-daemon thread가 없고 `main`까지 끝나면 진행 중 VT가 있어도 JVM이 종료될 수 있다. 장시간 도는 Spring Boot 워커에는 `spring.main.keep-alive`를 검토하고, 일반 Java 프로그램은 main의 대기·작업 join·종료 절차를 명시한다. 유한 작업을 끝내고 종료해야 하는 Job에는 상주 설정을 그대로 복사하지 않는다. [Spring Boot 3.5 가상 스레드](https://docs.spring.io/spring-boot/3.5/reference/features/spring-application.html#features.spring-application.virtual-threads)

Boot의 자동 설정 실행기가 VT 방식으로 바뀌면 기존 pooling 속성으로 작업 수를 제한하지 못할 수 있다. 사용자 정의 Executor와 스케줄러, 메시지 리스너의 concurrency·prefetch는 각 구현을 확인한다. VT 활성화만으로 모든 스레드가 VT로 바뀌지는 않는다. [Spring Boot 작업 실행과 스케줄링](https://docs.spring.io/spring-boot/3.5/reference/features/task-execution-and-scheduling.html)

### 기동·건강 상태·종료

- 애플리케이션은 컨테이너의 주 프로세스로 실행하고, 셸을 거친다면 `exec java ...` 등으로 종료 신호가 전달되게 한다. 컨테이너 안에서 `nohup`이나 `&`로 분리하지 않는다.
- `startupProbe`는 JIT·클래스 로딩을 포함한 기동 시간을 반영한다. readiness는 요청을 받을 준비 상태, liveness는 재시작으로 복구할 수 있는 상태를 나타내도록 설계한다. 외부 DB 지연마다 liveness가 실패하면 재시작이 몰릴 수 있다. [Kubernetes probe](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)
- readiness가 내려가도 메시지 브로커 소비가 자동으로 멈추지는 않는다. 워커는 신규 poll·작업 제출을 중단하고, 진행 중 작업의 완료·ack/commit·재처리 기준을 정한다.
- `preStop` 실행 시간도 종료 유예 시간에 포함된다. 신호 전달·작업 정리·프레임워크 종료 단계가 전체 `terminationGracePeriodSeconds` 안에 들어오게 하고, 강제 종료 후 중복 처리도 시험한다. [Pod 종료 절차](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination-flow)

## 8. 실제 적용값과 병목을 확인한다

### 앱 프로세스에서 가용 CPU와 heap 기록

다음 코드는 JDK 21 이상에서 실행할 수 있는 진단 예제다. 앱 기동 코드에서도 같은 값을 로그·메트릭으로 기록할 수 있다. 단독 실행 결과는 그 진단 JVM의 값이므로, 앱을 진단할 때는 같은 옵션을 사용하거나 앱 내부에서 기록한다.

```java
import java.util.concurrent.ForkJoinPool;

public class ResourceSnapshot {
    public static void main(String[] args) {
        Runtime runtime = Runtime.getRuntime();
        System.out.println("availableProcessors=" + runtime.availableProcessors());
        System.out.println("maxHeapMiB=" + runtime.maxMemory() / (1024 * 1024));
        System.out.println("commonPoolParallelism=" + ForkJoinPool.commonPool().getParallelism());
        System.out.println("configuredVtParallelism="
                + System.getProperty("jdk.virtualThreadScheduler.parallelism", "default"));
    }
}
```

`configuredVtParallelism=default`는 속성을 명시하지 않았다는 뜻이다. 실행 중 목표 병렬도와 carrier 수는 JDK 24 이상에서 `VirtualThreadSchedulerMXBean`의 `getParallelism()`, `getPoolSize()`, `getMountedVirtualThreadCount()`, `getQueuedVirtualThreadCount()`로 볼 수 있다. queued 값은 스케줄러에서 실행을 기다리는 VT의 추정치이며, I/O를 기다리며 park된 모든 요청 수를 뜻하지 않는다. [JDK 25 관리 API](https://docs.oracle.com/en/java/javase/25/docs/api/jdk.management/jdk/management/VirtualThreadSchedulerMXBean.html)

### Kubernetes와 JVM 진단 명령

아래 Bash 예제는 context·namespace·Pod·컨테이너 이름을 바꿔 사용한다. `jcmd`는 대상 JVM과 호환되는 JDK 도구, 같은 사용자와 attach 가능한 환경이 필요하다. 여기서는 Java 프로세스가 PID 1이라고 가정하며 다르면 확인한 PID로 바꾼다.

```bash
kubectl --context my-cluster -n app-namespace get pod my-pod -o yaml
kubectl --context my-cluster -n app-namespace top pod my-pod --containers

kubectl --context my-cluster -n app-namespace exec my-pod -c app -- jcmd 1 VM.flags -all
kubectl --context my-cluster -n app-namespace exec my-pod -c app -- jcmd 1 GC.heap_info

# 별도 JVM을 시작하여 cgroup 인식 상태를 확인한다.
kubectl --context my-cluster -n app-namespace exec my-pod -c app -- \
  java -XshowSettings:system -version

# JDK 25의 VT 스케줄러 상태. 지원 명령은 jcmd 1 help로 확인한다.
kubectl --context my-cluster -n app-namespace exec my-pod -c app -- \
  jcmd 1 Thread.vthread_scheduler
```

Pod YAML에는 admission·LimitRange 적용 후 설정이 나타난다. `VM.flags`에서 `ActiveProcessorCount`, `MaxHeapSize`, GC 관련 플래그를 확인한다. `ActiveProcessorCount=-1`이면 자동 계산을 사용한다는 뜻이므로 실제 가용 CPU 수는 앱의 로그와 함께 본다. 새로 실행한 `java -version`은 앱 명령줄 옵션이나 기존 풀 상태를 그대로 재현하지 않는다. `kubectl top`의 평균값만으로 짧은 throttling이나 피크를 판단하지 않는다.

별도 JVM도 같은 컨테이너의 CPU·메모리 예산을 소비하며 `JAVA_TOOL_OPTIONS` 등 환경변수를 상속한다. 메모리 여유가 없는 운영 Pod에서는 추가 JVM을 띄우지 않고 동일 설정의 검증 Pod에서 확인한다.

Linux cgroup v2에서는 해당 컨테이너의 `cpu.max`, `cpu.stat`, `cpuset.cpus.effective`, `memory.current`, `memory.max`, `memory.events`도 확인한다. `/sys/fs/cgroup` 마운트와 `/proc/self/cgroup`에 따라 경로가 달라지며 cgroup v1은 파일 구조가 다르다. [cgroup v2 인터페이스](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html)

NMT가 필요하면 시험 환경에서 JVM 시작 시 `-XX:NativeMemoryTracking=summary`를 추가하고 다음처럼 비교한다. 측정 비용이 있으며, NMT는 third-party native 할당 등 전체 RSS를 모두 추적하지 않는다. reserved·committed와 실제 상주 메모리를 구분한다. [Native Memory Tracking](https://docs.oracle.com/en/java/javase/25/vm/native-memory-tracking.html)

```bash
kubectl --context my-cluster -n app-namespace exec my-pod -c app -- \
  jcmd 1 VM.native_memory baseline
# 대표 부하를 가한 뒤 같은 JVM의 증가량을 확인한다.
kubectl --context my-cluster -n app-namespace exec my-pod -c app -- \
  jcmd 1 VM.native_memory summary.diff scale=MB
```

가상 스레드까지 포함한 스택은 `jcmd 1 Thread.dump_to_file -format=json /tmp/threads.json`으로 남길 수 있다. 쓰기 권한·용량·수집 경로를 마련하고, 기존 파일과 겹치지 않는 이름을 사용한다. JFR·덤프 수집 자체의 비용도 고려한다. [JDK 25 jcmd](https://docs.oracle.com/en/java/javase/25/docs/specs/man/jcmd.html)

### 함께 볼 지표

| 관측 | 가능한 원인 | 다음 확인 |
| :--- | :--- | :--- |
| p99 증가와 CPU throttling 증가 | quota 소진, 기동·GC·CPU 작업의 순간 수요 | limit 후보 비교, 요청당 CPU 시간, runnable 작업 |
| CPU가 낮고 in-flight·heap이 증가 | 외부 I/O 지연, 무제한 유입, timeout 부족 | 연결 풀 대기·외부 지연·요청 크기·ThreadLocal |
| CPU가 높고 처리량은 정체 | CPU 포화, GC 비용, 락 경합 | CPU 프로파일·GC·스택·처리 동시성 |
| heap 여유가 있는데 `OOMKilled` | native/direct 메모리, 파일·tmpfs 등 | cgroup 메모리·NMT·버퍼·플랫폼 스레드 수 |
| Pod 증가 후 DB가 더 느려짐 | 전체 연결·쿼리 동시성 증가 | 최대 Pod 수를 반영한 DB 예산 |
| 낮은 트래픽에서도 워커가 정상 종료 | non-daemon thread가 남지 않음 | main·스케줄러·keep-alive·종료 로그 |

cAdvisor 기반 Prometheus 환경에서는 다음처럼 확인할 수 있다. exporter와 수집 설정에 따라 지표·label이 다르며, 여러 클러스터를 수집하면 cluster label 조건도 추가한다.

```promql
# app 컨테이너의 CPU 사용량. 결과 0.5는 0.5 CPU에 해당한다.
sum by (pod) (
  rate(container_cpu_usage_seconds_total{namespace="app-namespace", container="app"}[5m])
)

# quota가 적용된 주기 중 throttling이 발생한 주기의 비율(%)
100 * sum by (pod) (
  rate(container_cpu_cfs_throttled_periods_total{namespace="app-namespace", container="app"}[5m])
) / sum by (pod) (
  rate(container_cpu_cfs_periods_total{namespace="app-namespace", container="app"}[5m])
)
```

두 번째 값은 잃어버린 CPU 시간이나 실패 요청의 비율이 아니다. quota가 없거나 분모가 0인 시계열은 해석에서 제외하고, 더 짧은 구간의 지연·throttled seconds·GC·노드 CPU 경합도 함께 본다. [cAdvisor 지표 정의](https://github.com/google/cadvisor/blob/master/docs/storage/prometheus.md)

## 9. HPA와 부하 시험으로 산정값을 검증한다

CPU `averageUtilization` 기반 HPA는 **request에 대한 실제 CPU 사용량 비율**을 사용한다. request가 `500m`이면 목표 70%는 평균 `350m` 사용에 해당한다. limit이 `"2"`라고 해서 1.4 CPU가 기준이 되지는 않는다. 같은 사용량에서도 request 변경은 HPA 동작을 바꾼다.

VT 서비스는 외부 I/O 대기로 CPU가 낮은 상태에서도 포화될 수 있다. HTTP in-flight·대기 시간, 메시지 backlog·가장 오래된 메시지의 나이 등 해당 작업의 병목을 나타내는 지표를 검토한다. sidecar가 CPU 지표를 왜곡하면 앱 컨테이너를 지정하는 `ContainerResource` 지표도 선택지다. 확장이 DB·외부 API의 처리 한계를 넘어서는 경우에는 동시성·유입 제한이 먼저 필요하다. [Kubernetes HPA](https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/)

다음 조건을 같은 입력·데이터·외부 시스템 조건에서 비교한다.

1. **정상 부하와 피크**: p95/p99, 오류율, CPU·throttling, heap·컨테이너 메모리, GC, 연결 풀 대기와 in-flight를 기록한다.
2. **기동과 확장**: warm-up, 캐시가 비어 있는 새 Pod, 필요한 노드 확보 시간까지 본다. HPA가 반응하기 전의 유입을 감당할 여유도 정한다.
3. **외부 지연과 실패**: DB/API 응답 지연, timeout과 재시도로 요청·메모리가 무한히 쌓이지 않는지 확인한다.
4. **노드 경합과 일부 Pod 손실**: request만큼의 용량 가정이 현실적인지, 남은 Pod로 부하가 몰려도 기준을 만족하는지 본다.
5. **rollout과 종료**: 최대 동시 Pod의 외부 연결 수, drain, ack/commit, 강제 종료 후 재처리를 확인한다.

결과에는 이미지·JDK 버전, request/limit, 실제 가용 CPU 수, `ActiveProcessorCount`, VT parallelism, heap 상한, 동시성·연결 풀 상한을 함께 남긴다. 설정을 하나씩 바꾸어 성능·비용·오류율이 어떻게 변했는지 비교하면 다음 배포에서도 같은 판단을 재사용할 수 있다.

## 관련 문서

- [Kubernetes에서 Virtual Thread 운영 시 확인할 것](Virtual_Threads_in_K8s.md)
- [ThreadPoolExecutor와 작업 거부 정책](ThreadPoolExecutor.md)
- [JDK 25 이미지 선택과 Kubernetes 점검 스크립트](JDK25_Docker_Base_Image_Selection.md)
- [Java 메모리 구조](Memory.md)
