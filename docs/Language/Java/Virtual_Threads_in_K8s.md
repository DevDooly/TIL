# Kubernetes에서 Virtual Thread 운영 시 확인할 것

가상 스레드를 쓰면 I/O를 기다리는 작업을 많이 다루기 쉬워진다. 다만 Pod의 CPU와 메모리, DB 연결 수는 그대로이므로 동시 요청이 늘어날 때 어디서 병목이 생기는지 살펴봐야 한다. CPU 계산 자체가 빨라지는 것은 아니다. [Virtual Thread 도입 가이드](https://docs.oracle.com/en/java/javase/25/core/virtual-threads.html)

## CPU와 scheduler

`jdk.virtualThreadScheduler.parallelism`은 정수로 설정한다. Pod의 CPU limit가 `500m`이라고 해서 이 값에 `0.5`를 넣을 수는 없다. 스케줄러 설정을 바꾸더라도 CPU 사용량이 제한을 넘으면 throttling은 발생한다.

JVM이 인식한 processor 수, 실제 CPU 사용량, throttling, runnable 작업 수와 p99 지연을 함께 본다. CPU-bound 작업의 동시성을 무제한으로 늘리면 대기만 늘 수 있다. [Java 21 가상 스레드 스케줄링](https://openjdk.org/jeps/444), [Kubernetes 리소스 제한](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)

## 메모리 예산

가상 스레드의 stack chunk는 Java heap에 들어간다. 이미 heap 예산에 포함되므로 `-Xmx` 바깥에 가상 스레드 스택용 공간을 따로 더하면 같은 메모리를 두 번 계산하게 된다.

Pod 메모리는 heap 외에도 metaspace, code cache, direct buffer, 플랫폼 스레드 stack과 기타 native 메모리 등을 포함한다. heap 안에서도 대기 중 요청 본문과 ThreadLocal 값이 누적될 수 있다. RSS와 heap·native 지표를 구분해 측정한다. [JEP 444 메모리 설명](https://openjdk.org/jeps/444)

## downstream과 종료

- DB connection 수, 외부 API 동시 호출 수, in-flight 요청 수에 상한을 둔다.
- Semaphore로 실행 수를 제한해도 기다리는 요청 수가 무한하면 메모리는 증가한다. 대기 한도·timeout·거절 정책을 함께 둔다.
- 종료 시 요청 유입을 중단하고 처리 중 작업을 정리한다. DB·Kafka·파일 작업의 완료와 재처리 범위를 정한다.
- `terminationGracePeriodSeconds`와 애플리케이션 종료 시간을 맞추고 강제 종료도 테스트한다.

## Pinning은 버전별로 확인

JDK 24에서는 monitor와 관련된 pinning 제약이 개선되었다. JDK 21–23에서 보던 증상이라도 업그레이드 후에는 달라질 수 있으므로, 실제 스택과 JFR 이벤트를 기준으로 판단한다. [진단 절차와 JDK별 옵션](Virtual_Threads_FTP_Pinning.md)

변경 전후를 비교할 때는 Pod 수, 리소스 제한, 입력, DB 크기를 맞춘다. 처리량만 보면 지연이나 메모리 증가를 놓칠 수 있으므로 p95/p99, 오류율, 큐 길이, RSS, GC, CPU throttling도 함께 확인한다.
