# JDK 25 Docker Base 이미지 선택과 업그레이드 검증

`openjdk:22-oraclelinux9`에서 JDK 25로 전환하면 JDK 24의 JEP 491에 포함된 monitor 관련 가상 스레드 pinning 개선을 사용할 수 있다. JDK 25는 2025년 9월 출시된 LTS 버전이며, 배포판의 업데이트 정책과 컨테이너의 기반 OS를 함께 선택해야 한다.

기존 RPM 패키지 작업을 유지하려면 **`amazoncorretto:25-al2023`을 우선 검증할 후보**로 잡을 수 있다. OS 패키지 의존성이 적거나 Ubuntu 운영 경험이 있다면 **`eclipse-temurin:25-jdk-noble`**도 후보가 된다. 실제 Dockerfile과 네이티브 라이브러리를 확인한 뒤 결정하며, Oracle Linux 9 유지가 필수인 경우는 별도로 다룬다.

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

## 관련 문서

- [Virtual Thread: FTP 처리의 Pinning 진단](Virtual_Threads_FTP_Pinning.md)
- [JDBI와 Virtual Thread: Bounded Executor 격리](SpringBoot/JDBI_VT_Pinning_Solution.md)
- [Java 25 주요 기능 및 정식/Preview 구분](Versions/Java25.md)
