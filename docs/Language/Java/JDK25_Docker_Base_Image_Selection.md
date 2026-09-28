# JDK 25 Docker Base 이미지 선택과 업그레이드 검증

`openjdk:22-oraclelinux9`에서 JDK 25로 전환하면 JDK 24의 JEP 491에 포함된 monitor 관련 가상 스레드 pinning 개선을 사용할 수 있다. JDK 25는 2025년 9월 출시된 LTS 버전이며, 배포판의 업데이트 정책과 컨테이너의 기반 OS를 함께 선택해야 한다.

Kubernetes에서 일반적인 Java 서비스를 옮긴다면 **`eclipse-temurin:25-jdk-noble`로 먼저 검증**하는 것을 권한다. glibc 환경과 JDK 진단 도구를 유지하면서 전환하고, 런타임에 JDK 도구가 필요 없다고 확인되면 `25-jre-noble`로 줄인다. RPM 패키지 운영을 유지해야 하는 경우에는 Corretto AL2023, 조직의 UBI 표준이 있는 경우에는 Temurin UBI 10을 검토한다.

노드가 Amazon Linux나 RHEL이라는 이유로 컨테이너도 같은 배포판을 쓸 필요는 없다. 컨테이너는 자체 사용자 공간을 포함하고 호스트 커널을 공유한다. 이미지의 OS·CPU 아키텍처, 커널·런타임 호환성과 애플리케이션의 네이티브 의존성을 확인한다. [Kubernetes 컨테이너 개념](https://kubernetes.io/docs/concepts/containers/)

## 1. 기존 이미지에서 바뀌는 것

`openjdk:22-oraclelinux9`의 `oraclelinux9`는 기반 OS를 가리킨다. 이 이미지에 들어 있는 Java는 `jdk.java.net` 계열의 GPLv2 with Classpath Exception(GPLv2+CPE) OpenJDK 빌드다. Oracle JDK에 적용하는 NFTC와는 배포 라이선스가 다르다.

기존 [Dockerfile](https://github.com/docker-library/openjdk/blob/29413b7a4a8cfec0a856961829befe652d37bb7e/22/jdk/oraclelinux9/Dockerfile)을 보면 기반 이미지는 `oraclelinux:9-slim`, 패키지 관리자는 `microdnf`, `JAVA_HOME`은 `/usr/java/openjdk-22`다. 같은 Oracle Linux 9을 사용해도 full/slim 구성과 JDK 설치 경로, CA 인증서 연결 방식이 달라질 수 있다.

Docker Hub의 [`library/openjdk`는 deprecated 상태](https://hub.docker.com/_/openjdk)이며, 계속 갱신하는 대상으로 안내하는 것은 Early Access 빌드다. 기존 22 태그를 가져올 수 있다는 사실만으로 보안 업데이트가 유지된다고 판단할 수 없다. 운영용 업그레이드는 유지보수 중인 배포판의 JDK 25 이미지로 진행한다.

## 2. 이미지별 선택 조건

아래 태그는 2026년 9월 28일 레지스트리의 manifest를 조회해 확인했다. 태그가 가리키는 패치 버전과 digest는 이후 달라질 수 있다.

| 후보 이미지 | 기반 OS / libc | 패키지 관리자 | 선택 조건과 변경점 |
| :--- | :--- | :--- | :--- |
| `amazoncorretto:25-al2023` | Amazon Linux 2023 / glibc | `dnf` | RPM 기반 운영을 이어갈 후보. OL9과 패키지 저장소·버전이 다르므로 설치 목록을 다시 확인한다. |
| `eclipse-temurin:25-jdk-noble` | Ubuntu 24.04 / glibc | `apt-get` | OS 의존성이 적거나 Ubuntu를 표준으로 쓰는 환경. RPM 설치 명령을 바꿔야 한다. |
| `eclipse-temurin:25-jdk-ubi10-minimal` | Red Hat UBI 10 Minimal / glibc | `microdnf` | UBI가 필요한 환경. OL9에서 OS 주 버전까지 바뀌며 CPU 요구 사항도 확인해야 한다. |
| `container-registry.oracle.com/java/jdk-no-fee-term:25-oraclelinux9` | Oracle Linux 9 / glibc | `dnf` | OL9 유지와 Oracle JDK 지원이 필요한 환경. NFTC 조건과 이후 업데이트 계획을 확인한다. |
| `bellsoft/liberica-openjdk-alpine-musl:25` | Alpine Linux / musl | `apk` | 크기를 줄이는 것이 중요하고 네이티브 라이브러리의 musl 호환성을 검증할 수 있는 환경. |

### RPM 계열이어도 패키지 호환성은 따로 확인한다

Corretto의 [JDK 25 Dockerfile](https://github.com/corretto/corretto-docker/blob/main/25/jdk/al2023/Dockerfile)은 `amazonlinux:2023`과 `dnf`를 사용한다. 그러나 AL2023은 여러 Fedora 버전 등의 구성 요소를 바탕으로 독자적인 릴리스 주기를 갖는다. OL9의 저장소 설정, RPM 파일, 패키지 이름과 옵션을 그대로 가져올 수 있다는 보장은 없다. [AL2023과 Fedora의 관계](https://docs.aws.amazon.com/linux/al2023/ug/relationship-to-fedora.html)

Temurin JDK 25의 UBI 이미지는 **UBI 10으로 제공된다**. `eclipse-temurin:25-jdk-ubi9-minimal`은 공식 제공 태그가 아니며, 레지스트리 조회에서도 `not found`를 반환했다. UBI 10의 x86 이미지에는 x86-64-v3를 지원하는 CPU가 필요하므로, 기존 x86-64-v2 노드에 그대로 배포할 수 없다. [Temurin 25 출시 안내](https://adoptium.net/news/2025/09/eclipse-temurin-25-available), [RHEL 10 지원 아키텍처](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/10.0_release_notes/architectures)

UBI에는 RHEL 패키지의 일부를 제공하는 전용 저장소가 포함된다. 필요한 패키지가 그 저장소에 있는지 확인해야 하며, `microdnf`를 쓴다는 이유만으로 OL9 환경과 같다고 볼 수 없다. [UBI 구성과 저장소](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/building_running_and_managing_containers/types-of-container-images)

### Alpine은 저장소 이름까지 구분한다

BellSoft의 [`liberica-openjdk-alpine`](https://github.com/bell-sw/Liberica/blob/master/docker/repos/liberica-openjdk-alpine/README.md)은 glibc를 추가한 Alpine 이미지다. musl 기반 후보는 [`liberica-openjdk-alpine-musl`](https://github.com/bell-sw/Liberica/blob/master/docker/repos/liberica-openjdk-alpine-musl/25/Dockerfile)이다. JNI 라이브러리와 APM 에이전트가 요구하는 libc를 확인한 뒤 선택한다.

이미지 크기는 JDK/JRE 구성, 아키텍처, 추가 패키지, 압축 여부에 따라 달라진다. 전환 전후의 같은 아키텍처 이미지로 비교하며, 경량화가 필요하면 배포판 변경 외에 JRE 또는 `jlink`로 만든 런타임도 검토한다. 운영 진단에 쓰는 `jcmd`, `jfr` 등의 도구가 필요한지도 함께 판단한다.

## 3. 라이선스와 업데이트를 구분한다

Oracle Linux, Oracle OpenJDK, Oracle JDK는 각각 다른 배포 대상이다. Oracle Linux는 무료로 사용·배포·업데이트할 수 있고 유료 지원은 별도다. Java의 라이선스는 OS 이름이 아니라 포함된 JDK 배포판에서 확인한다. [Oracle Linux 배포·업데이트 정책](https://blogs.oracle.com/cloud-infrastructure/oracle-linux-provides-a-stable-free-rhel-compatible-alternative-to-centos-with-support-included-in-oracle-cloud)

### Oracle JDK 25의 NFTC 적용 범위

Oracle의 [Java 라이선스 FAQ](https://www.oracle.com/java/technologies/javase/jdk-faqs.html)는 Oracle JDK 25 업데이트를 **2028년 9월까지 NFTC로 제공할 계획**이라고 안내한다. NFTC 조건을 충족하면 상용 운영에도 무료로 사용할 수 있다. 이후 JDK 25 업데이트에는 OTN을 적용할 계획이므로, 그 시점에 배포판 전환·다음 LTS 업그레이드·구독 여부를 판단해야 한다.

이미 NFTC로 받은 릴리스는 받은 당시의 조건으로 계속 사용할 수 있다. 해당 날짜가 지났다는 이유만으로 기존 설치본이 자동 유료화되는 구조는 아니다. 다만 구버전을 고정해 두면 이후 보안 패치를 받지 못한다. JDK 17도 17.0.12까지의 NFTC 릴리스와 17.0.13 이후 업데이트의 조건을 구분한다.

NFTC에는 재배포 조건도 있다. 고객에게 JDK가 포함된 컨테이너를 전달하는 경우에는 SaaS처럼 내부 서버에서 실행하는 경우와 함께 취급하지 말고, [NFTC 원문](https://www.oracle.com/downloads/licenses/no-fee-license.html)의 배포 조건을 확인한다.

Oracle JDK 25의 OL9 이미지는 공식 [Oracle 실습 문서](https://luna.oracle.com/lab/268ea851-2f09-43e6-8d70-40a10cb4de03/steps)에서 안내하는 `java/jdk-no-fee-term:25-oraclelinux9` 경로로 조회할 수 있다. 직접 빌드할 때 참고할 [Oracle의 OL9용 Dockerfile](https://github.com/oracle/docker-images/blob/main/OracleJava/25/Dockerfile.ol9)도 제공된다. 채택할 때는 정확한 저장소·태그와 해당 배포본의 라이선스를 함께 확인한다.

### GPL 배포판의 무료 사용과 지원 기간

Temurin·Corretto·Liberica의 OpenJDK는 GPLv2+CPE로 제공된다. 상용 애플리케이션에 사용할 수 있지만, 이미지에 포함된 OS 패키지와 제3자 구성 요소의 라이선스, JDK 재배포 시 의무는 별도로 남는다. 무료 사용이 무기한 업데이트나 유료 기술 지원까지 뜻하지는 않는다. [Temurin 이미지 라이선스](https://hub.docker.com/_/eclipse-temurin), [Corretto FAQ](https://aws.amazon.com/corretto/faqs/), [BellSoft의 GPLv2+CPE 설명](https://bell-sw.com/blog/gplv2-classpath-exception-the-intricacies-of-open-source-licensing/)

Temurin의 커뮤니티 지원 일정과 Corretto의 분기별 업데이트 계획은 각 공급자의 정책을 따른다. JDK 보안 릴리스, 배포판 바이너리 출시, OS 패치, 컨테이너 재빌드 시점은 다를 수 있다. 선정한 태그의 실제 JDK 버전과 OS 패치 상태를 확인하고, 지원 계약이 필요하면 별도로 검토한다. [Temurin 지원 정책](https://adoptium.net/support/), [Corretto 업데이트 정책](https://aws.amazon.com/corretto/faqs/)

## 4. Dockerfile 전환 예제

아래 예제는 실행 가능한 JAR 하나를 `target/app.jar`로 준비한 경우다. 실제 빌드 산출물은 `JAR_FILE`로 지정한다. 공식 태그와 빌드 정의는 확인했지만, 이 예제의 이미지 빌드와 서비스 실행은 별도 검증이 필요하다.

### Corretto 25 / Amazon Linux 2023

```dockerfile
FROM amazoncorretto:25-al2023

RUN dnf install -y tzdata && dnf clean all

WORKDIR /app
ARG JAR_FILE=target/app.jar
COPY --chmod=0444 ${JAR_FILE} /app/app.jar

USER 10001:10001
CMD ["java", "-jar", "/app/app.jar"]
```

기존 `microdnf` 또는 `dnf` 명령은 설치 대상 패키지별로 확인한 뒤 바꾼다. 위의 `tzdata` 한 패키지 예제가 전체 Dockerfile의 호환성을 보장하지는 않는다.

### Temurin 25 / Ubuntu Noble

```dockerfile
FROM eclipse-temurin:25-jdk-noble

WORKDIR /app
ARG JAR_FILE=target/app.jar
COPY --chmod=0444 ${JAR_FILE} /app/app.jar

USER 10001:10001
CMD ["java", "-jar", "/app/app.jar"]
```

Temurin은 CA 인증서를 처리하는 기본 entrypoint가 있어 `CMD`로 Java 명령을 전달한다. 사내 CA를 추가한다면 `USE_SYSTEM_CA_CERTS` 설정과 비루트 실행 시 truststore 처리도 확인한다. [Temurin 인증서 처리 안내](https://hub.docker.com/_/eclipse-temurin)

두 예제 모두 숫자 UID/GID로 실행한다. 애플리케이션이 쓰는 업로드·로그·캐시 디렉터리와 볼륨에는 해당 UID의 쓰기 권한을 부여해야 한다. `/app`과 JAR은 읽기 전용으로 두고, 사용자 이름 조회가 필요한 라이브러리는 계정 등록 여부도 확인한다.

## 5. 태그를 확인하고 같은 조건으로 검증한다

먼저 레지스트리에서 태그와 대상 아키텍처를 확인한다. 다음 명령은 Docker Buildx가 필요하며, manifest 조회에는 실행 중인 Docker Engine이 필요하지 않다.

```bash
docker buildx imagetools inspect amazoncorretto:25-al2023
docker buildx imagetools inspect eclipse-temurin:25-jdk-noble
docker buildx imagetools inspect eclipse-temurin:25-jdk-ubi10-minimal
docker buildx imagetools inspect container-registry.oracle.com/java/jdk-no-fee-term:25-oraclelinux9
```

태그는 가변이므로 운영에서 재현성을 확보하려면 `이미지:태그@sha256:실제_digest`로 검증한 베이스를 고정한다. digest를 고정한 뒤에는 새 패치가 나올 때 digest를 갱신하고 다시 빌드·배포하는 절차도 필요하다. [Docker 이미지 버전 고정과 재빌드](https://docs.docker.com/build/building/best-practices/)

Docker Engine이 실행 중인 검증 환경에서, 선택한 Dockerfile과 서비스 산출물로 다음을 실행한다.

```bash
docker build --pull --build-arg JAR_FILE=target/app.jar -t app:jdk25 .
docker run --rm --entrypoint java app:jdk25 -version
docker run --rm --entrypoint sh app:jdk25 -c 'cat /etc/os-release; id'
docker run --rm app:jdk25
```

버전 확인과 기동만으로 업그레이드 검증이 끝나지는 않는다.

1. **JDK 호환성**: 사용 중인 Spring Boot, 빌드 도구, JDBC 드라이버, 바이트코드 처리 라이브러리, APM 에이전트가 JDK 25를 지원하는지 확인한다. 이전 JDK의 Preview 기능을 썼다면 소스·컴파일·실행 옵션을 함께 검토한다.
2. **OS 의존성**: JNI, 인증서, DNS, 타임존, 로케일, 폰트, 실행 스크립트와 파일 권한을 점검한다. `JAVA_HOME`의 기존 절대 경로를 사용하는 설정도 찾는다.
3. **서비스 동작**: 같은 CPU·메모리 제한과 같은 부하에서 FTP/SFTP·DB·HTTP 연동, 오류율, 처리량, 지연 시간을 비교한다.
4. **배포와 복구**: 검증한 새 애플리케이션 이미지와 이전 이미지의 digest를 남기고, 일부 인스턴스에 먼저 적용해 되돌릴 수 있는지 확인한다.

## 6. JDK 25에서 pinning을 판단하는 방법

JEP 491은 `synchronized` 구간에서 블로킹하거나 monitor를 기다릴 때 가상 스레드가 캐리어에서 내려올 수 있도록 개선했다. 이 효과는 여기서 비교한 HotSpot 기반 JDK 25 배포판에 공통으로 적용된다. `synchronized`를 사용한다는 이유만으로 pinning 회피용 락 교체를 할 필요는 줄지만, 공유 락으로 인한 작업 직렬화와 연결 풀 부족은 별도의 병목으로 남는다. [JEP 491](https://openjdk.org/jeps/491)

native/foreign 호출이 Java로 되돌아온 뒤 블로킹하는 경로 등에는 pinning이 남을 수 있다. JDK 24부터 `jdk.tracePinnedThreads` 속성은 제거되어 `-Djdk.tracePinnedThreads=full`을 지정해도 효과가 없다. JFR의 `jdk.VirtualThreadPinned` 이벤트로 남은 경로를 확인한다.

```bash
# 60초 동안 같은 재현 부하를 넣고, 기록이 끝난 뒤 파일을 읽는다.
java -XX:StartFlightRecording=filename=/tmp/vt-check.jfr,settings=profile,duration=60s -jar app.jar

# 컨테이너에서는 별도 셸에서 실행하거나 파일을 꺼내 분석한다.
jfr print --events jdk.VirtualThreadPinned /tmp/vt-check.jfr
```

`jdk.VirtualThreadPinned`의 기본 임계값은 20ms다. 이벤트가 없을 때도 기록 설정과 임계값을 확인하고, native 코드 내부의 블로킹 등 이 이벤트만으로 확인하기 어려운 경로는 스레드 덤프·프로파일링과 대조한다. 업그레이드 효과는 실제 지연·오류율과 함께 판단한다. [JDK 25 Virtual Threads 진단](https://docs.oracle.com/en/java/javase/25/core/virtual-threads.html)

## 7. Kubernetes 상황별 추천

| 상황 | 먼저 검증할 이미지 | 선택 이유와 조건 |
| :--- | :--- | :--- |
| 일반적인 Spring Boot/JAR 서비스의 첫 JDK 25 전환 | `eclipse-temurin:25-jdk-noble` | glibc 기반. `jcmd` 등 진단 도구를 확보한 상태에서 호환성과 부하를 확인한다. |
| 빌드와 실행을 분리했고 운영 컨테이너에 JDK 도구가 필요 없음 | `eclipse-temurin:25-jre-noble` | 런타임 구성을 줄인다. 에이전트·동적 컴파일·장애 진단 도구 의존성을 먼저 확인한다. |
| OpenShift 또는 조직에서 UBI를 표준으로 사용 | `eclipse-temurin:25-jdk-ubi10-minimal` | 모든 대상 노드의 CPU 요구 사항과 UBI 저장소 패키지를 검증한다. OpenShift가 허용하는 UID/GID 범위도 맞춘다. |
| 오래된 x86 노드 또는 CPU 세대를 파악하지 못함 | `eclipse-temurin:25-jdk-noble` | UBI 10의 x86-64-v3 조건을 확인하기 전에는 Noble부터 기동 시험한다. Noble도 해당 노드에서 직접 확인한다. |
| amd64·arm64 노드가 섞임 | Noble의 JDK 또는 JRE | 두 아키텍처용 베이스와 최종 앱 이미지를 모두 제공한다. JNI/APM도 각 아키텍처에서 검증한다. |
| 이미지 크기가 중요하고 musl 검증을 마침 | `eclipse-temurin:25-jre-alpine` | 네이티브 라이브러리·DNS·폰트·인증서를 포함한 서비스 테스트 통과 후 선택한다. |
| 기존 RPM 패키지·Amazon Linux 운영 절차 의존성이 큼 | `amazoncorretto:25-al2023` | `dnf` 기반 후보. EKS 사용 자체가 이 이미지를 선택해야 하는 이유는 아니다. |
| Oracle Linux 9 유지 또는 Oracle JDK 지원 계약이 필수 | `container-registry.oracle.com/java/jdk-no-fee-term:25-oraclelinux9` | OS와 계약 조건을 우선하고, 앞 절의 업데이트·라이선스 계획을 적용한다. |

Noble의 `25-jdk-noble`·`25-jre-noble`, Alpine의 `25-jdk-alpine`·`25-jre-alpine`은 조회한 manifest에서 Linux amd64와 arm64를 제공했다. 실제 배포할 태그와 최종 앱 이미지의 manifest도 확인한다. 혼합 아키텍처 클러스터에서는 여러 아키텍처를 묶은 image index의 digest와 특정 아키텍처의 digest를 구분해야 한다. 특정 아키텍처 이미지만 빌드했다면 Pod의 스케줄링도 그 아키텍처로 제한한다. [Temurin 공식 태그와 Dockerfile](https://github.com/docker-library/official-images/blob/master/library/eclipse-temurin)

### Temurin 적용 전에 확인할 Pod 설정

- **실행 사용자와 쓰기 경로**: 숫자 UID/GID 또는 플랫폼이 배정한 UID로 실행한다. 읽기 전용 root filesystem을 쓰면 `/tmp`에 쓰기 가능한 볼륨을 두고, 업로드·캐시·JFR·heap dump 경로의 권한과 용량도 확인한다. `emptyDir`은 Pod 삭제 시 사라지므로 보존해야 하는 진단 파일은 따로 수집한다.
- **CA와 시작 명령**: Kubernetes의 `command`는 이미지의 `ENTRYPOINT`를 대체한다. Temurin의 CA 처리를 사용할 때는 기본 entrypoint를 유지하고 실행 인자는 `args`로 전달한다. `USE_SYSTEM_CA_CERTS`와 `/certificates`를 쓴다면 비루트 환경에서 생성하는 truststore와 `/tmp` 쓰기 권한을 확인한다. 기존 Helm chart의 `command`도 살펴본다.
- **메모리와 CPU**: 실제 적용된 requests/limits와 JVM이 인식하는 cgroup 값을 대조한다. heap 외에 metaspace, direct buffer, 스레드 stack, 에이전트의 native 메모리를 남긴다. `-Xmx`와 `MaxRAMPercentage`를 함께 지정했다면 실제 최대 heap을 확인하며, 모든 서비스에 같은 비율을 적용하지 않는다.
- **준비 상태와 종료**: `startupProbe`·`readinessProbe`를 새 기동 시간에 맞추고, SIGTERM을 받은 뒤 `terminationGracePeriodSeconds` 안에 요청·파일·메시지 처리를 마치는지 확인한다. 이미지 기동 성공만으로 DB·FTP·TLS 연동이나 graceful shutdown이 검증되지는 않는다.

[Kubernetes 보안 컨텍스트](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/), [command와 args](https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/), [리소스 제한](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/), [Temurin CA 처리](https://hub.docker.com/_/eclipse-temurin)

## 8. Kubernetes 점검 스크립트

저장소의 [`scripts/check_temurin_k8s.py`](https://github.com/DevDooly/TIL/blob/main/scripts/check_temurin_k8s.py)는 Python 3.10 이상과 `kubectl`을 사용한다. Docker Engine, `jq`, 추가 Python 패키지는 필요 없다. **스크립트는 조회와 로컬 파일 생성만 수행한다.** 생성한 Job은 아래 명령으로 별도 실행한다.

### 기존 설정 조회

예제의 context, namespace, Deployment와 컨테이너 이름은 실제 환경에 맞게 바꾼다. `--context`를 명시해야 하므로 현재 선택된 클러스터가 바뀌어도 다른 클러스터를 묵시적으로 조회하지 않는다.

```bash
python scripts/check_temurin_k8s.py \
  --context my-cluster --namespace app-namespace \
  --workload deployment/my-app --container app
```

스크립트는 다음을 출력한다.

- 노드 OS·아키텍처·Ready 상태·cordon 여부·커널·컨테이너 런타임
- workload의 `nodeSelector`에 해당하는 노드와 추가 스케줄링 확인 필요 여부
- 실행 UID/GID, `runAsNonRoot`, 읽기 전용 rootfs와 `/tmp` 마운트
- Temurin entrypoint를 덮어쓰는 `command`, 사용자 지정 `JAVA_HOME`·JVM 옵션 유무
- CPU·메모리 requests/limits, startup/readiness probe 유무

Secret 리소스는 조회하지 않고 환경변수 값과 시작 명령 내용도 출력하지 않는다. admission webhook이나 LimitRange가 변경한 Pod 설정은 실제 실행 중인 `--workload pod/실제-pod-이름`으로도 확인한다. `envFrom`으로 주입되는 실제 값은 이 조회로 확인되지 않으므로 별도로 점검한다. `--container`는 sidecar가 있는 경우 필수다.

`--node-selector nodepool=java`처럼 `key=value` 조건을 추가할 수 있다. workload의 `nodeSelector`와 교집합으로 적용하며 서로 충돌하면 중단한다. affinity·taint·리소스까지 계산하는 스케줄러 시뮬레이션은 아니므로, 목록에 있다고 실제 배치가 가능한 것은 아니다.

외부에서 받은 JSON으로도 점검할 수 있다. JSON은 기존에 실행한 `kubectl get nodes -o json`과 `kubectl get deployment/my-app -o json`의 결과를 사용한다.

```bash
python scripts/check_temurin_k8s.py \
  --nodes-json nodes.json --workload-json deployment.json --container app
```

종료 코드 `0`은 보고서 생성 성공, `2`는 인자·조회·입력·파일 생성 오류다. `CHECK`·`WARN`이 남아 있거나 보고서 생성에 성공했다고 해서 이미지 호환성 검증을 통과한 것은 아니다.

### 대상 노드마다 베이스 이미지 기동 시험

같은 명령에 `--emit-probes`를 추가하면 Ready 상태이고 cordon되지 않은 Linux 노드마다 진단 Job을 생성할 명세를 저장한다. 출력 파일이 이미 있으면 덮어쓰지 않는다.

```bash
python scripts/check_temurin_k8s.py \
  --context my-cluster --namespace app-namespace \
  --workload deployment/my-app --container app \
  --node-selector nodepool=java \
  --image eclipse-temurin:25-jdk-noble \
  --emit-probes temurin-noble-jobs.json
```

`nodepool=java`는 예시다. 실제 노드 풀 label로 바꾸거나, workload의 `nodeSelector`만 사용하려면 생략한다. UBI 10을 비교할 때는 `--image eclipse-temurin:25-jdk-ubi10-minimal`과 다른 출력 파일명을 지정한다. 운영에서 사용할 정확한 패치 태그나 digest, 사내 미러 경로도 지정할 수 있다.

생성한 Job은 다음 조건으로 실행된다.

- 기본 UID/GID `10001`, 비루트, 읽기 전용 rootfs, capability 제거, `RuntimeDefault` seccomp
- 쓰기 가능한 `/tmp`용 `emptyDir`과 서비스 계정 토큰 자동 마운트 비활성화
- Job당 CPU `100m`/`500m`, 메모리 `128Mi`/`512Mi`의 request/limit
- 원래 `nodeSelector`·node affinity·tolerations·RuntimeClass를 유지하고, 각 노드에 대한 affinity 추가
- 재시도 없음, 최대 실행 시간 180초, 종료 후 1시간 뒤 Job·Pod 자동 정리

OpenShift 등에서 UID/GID 범위가 정해져 있다면 `--uid`와 `--gid`로 허용된 값을 지정한다. 앱의 ServiceAccount, 환경변수, 볼륨, imagePullSecrets는 복사하지 않는다. 사내 이미지 인증이 필요하면 **진단 namespace에 있는** Secret 이름을 `--pull-secret registry-credentials`로 지정한다. pod affinity·anti-affinity·topology spread, 앱 label 기반 NetworkPolicy, 앱 인증서와 사용자 JVM 옵션도 자동 복제하지 않는다.

아래 명령은 Bash 기준이다. 파일의 namespace·이미지·대상 노드·Job 수를 확인하고 실행한다. 모든 Job이 함께 생성되므로 큰 노드 풀은 `--node-selector`로 범위를 나눌 수 있다.

```bash
CHECK_ID=$(python -c 'import json; print(json.load(open("temurin-noble-jobs.json"))["items"][0]["metadata"]["labels"]["til.dev/check-id"])')

kubectl --context my-cluster --namespace app-namespace create -f temurin-noble-jobs.json
kubectl --context my-cluster --namespace app-namespace wait \
  --for=condition=complete job -l "til.dev/check-id=$CHECK_ID" --timeout=240s

kubectl --context my-cluster --namespace app-namespace get pods \
  -l "til.dev/check-id=$CHECK_ID" -o wide
kubectl --context my-cluster --namespace app-namespace logs \
  -l "til.dev/check-id=$CHECK_ID" -c check --prefix --tail=-1

# 결과를 확인한 뒤 이번 파일에 포함된 Job만 정리한다.
kubectl --context my-cluster --namespace app-namespace delete -f temurin-noble-jobs.json
```

**생성한 모든 Job의 `Complete` 상태와 모든 대상 노드의 `TIL_TEMURIN_PROBE_OK` 로그**를 확인한다. 로그에는 OS, 아키텍처, UID, `/tmp` 쓰기 결과, JVM 버전과 cgroup CPU·메모리 인식값, 진단 도구 유무가 나온다. UBI 10의 CPU 명령어 조건, 이미지 아키텍처·pull 문제, 비루트 기동 문제를 찾는 데 사용할 수 있다.

`wait`가 실패하거나 시간이 초과되면 같은 context·namespace에서 Job과 Pod의 상태·이벤트를 확인한다. Pod가 생성되지 않았다면 `kubectl --context my-cluster --namespace app-namespace describe job 실제-job-이름`으로 admission 거부 등을 찾는다. Pod가 있다면 같은 명령의 `job`을 `pod`로 바꿔 taint/affinity 불일치, 자원 부족, `ImagePullBackOff`를 확인하고, JVM 기동 오류는 컨테이너 로그로 확인한다. Pending·권한 오류·생성 대상에서 빠진 노드는 통과로 집계하지 않는다. [노드 배치 제약](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/), [Job 종료 후 정리](https://kubernetes.io/docs/concepts/workloads/controllers/ttlafterfinished/)

이 시험은 **Temurin 베이스 이미지의 기동 확인**이다. 샘플 자원 제한으로 출력한 heap·processor 값은 실제 앱 Pod의 값과 다를 수 있다. 이후 Temurin으로 빌드한 최종 애플리케이션 이미지를 실제 보안 설정·볼륨·CA·리소스 제한으로 staging에 배포해 JNI/APM, 외부 연동, 부하, 종료를 확인한다. autoscaling으로 추가될 노드 풀과 다른 아키텍처도 검증 범위에 포함한다.

## 관련 문서

- [Virtual Thread: FTP 처리의 Pinning 진단](Virtual_Threads_FTP_Pinning.md)
- [JDBI와 Virtual Thread: Bounded Executor 격리](SpringBoot/JDBI_VT_Pinning_Solution.md)
- [Java 25 주요 기능 및 정식/Preview 구분](Versions/Java25.md)
- [Kubernetes에서 Virtual Thread 운영 시 확인할 것](Virtual_Threads_in_K8s.md)
