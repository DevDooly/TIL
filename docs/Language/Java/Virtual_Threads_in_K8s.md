# Kubernetes에서 Virtual Thread 운영 시 확인할 것

기준: JDK 21과 24 이후 차이를 구분, 2026-09-07.

가상 스레드는 I/O를 기다리는 많은 작업을 표현하는 데 유용하다. CPU 계산 자체를 빠르게 하거나 같은 Pod에서 수십 배 처리량을 보장하지는 않는다. [Virtual Thread 도입 가이드](https://docs.oracle.com/en/java/javase/25/core/virtual-threads.html)

## CPU와 scheduler

`jdk.virtualThreadScheduler.parallelism`은 정수 병렬성 설정이다. `500m`처럼 소수 CPU quota를 가진 Pod의 limit와 기계적으로 맞출 수 없고, 값을 맞춘다고 CPU throttling이 사라지지도 않는다.

JVM이 인식한 processor 수, 실제 CPU 사용량, throttling, runnable 작업 수와 p99 지연을 함께 본다. CPU-bound 작업의 동시성을 무제한으로 늘리면 대기만 늘 수 있다. [Java 21 가상 스레드 스케줄링](https://openjdk.org/jeps/444), [Kubernetes 리소스 제한](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)

## 메모리 예산

가상 스레드 stack chunk는 Java heap에 있다. 따라서 `-Xmx` 바깥에 “가상 스레드 stack용 20–30%”를 따로 더하는 설명은 이중 계산이다.

Pod 메모리는 heap 외에도 metaspace, code cache, direct buffer, 플랫폼 스레드 stack과 기타 native 메모리 등을 포함한다. heap 안에서도 대기 중 요청 본문과 ThreadLocal 값이 누적될 수 있다. RSS와 heap·native 지표를 구분해 측정한다. [JEP 444 메모리 설명](https://openjdk.org/jeps/444)

## downstream과 종료

- DB connection 수, 외부 API 동시 호출 수, in-flight 요청 수에 상한을 둔다.
- Semaphore로 실행 수를 제한해도 기다리는 요청 수가 무한하면 메모리는 증가한다. 대기 한도·timeout·거절 정책을 함께 둔다.
- 종료 시 요청 유입을 중단하고 처리 중 작업을 정리한다. DB·Kafka·파일 작업의 완료와 재처리 범위를 정한다.
- `terminationGracePeriodSeconds`와 애플리케이션 종료 시간을 맞추고 강제 종료도 테스트한다.

## Pinning은 버전별로 확인

JDK 21–23의 monitor 관련 제약과 JDK 24 이후 개선을 구분한다. 라이브러리 이름이나 `synchronized` 존재만으로 원인을 확정하지 않는다. [진단 절차와 JDK별 옵션](Virtual_Threads_FTP_Pinning.md)

검증 시 Pod 수·limit·입력·DB 크기를 고정하고 처리량, p95/p99, 오류율, 큐 길이, RSS, GC, CPU throttling을 함께 기록한다. 개선율과 비용 절감은 측정 결과가 있을 때만 적는다.
