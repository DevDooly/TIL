# JDK 25 Docker Base 이미지 선택: Virtual Thread Pinning 해결 및 마이그레이션

Java 21~23의 가상 스레드(Virtual Threads) 환경에서 `synchronized` 블록 내 I/O 블로킹 작업으로 인해 발생하던 **스레드 고정(Pinning) 및 캐리어 스레드 풀 고갈 이슈**는 **JDK 24의 JEP 491 (Synchronize Virtual Threads without Pinning)**을 통해 근본적으로 해결되었습니다. 

차기 LTS 버전인 **JDK 25**를 프로덕션에 도입하여 Pinning 문제를 해결할 때, 기존 `openjdk:22-oraclelinux9` 이미지를 대체할 최적의 Docker Base 이미지 선정 기준과 벤더별 특징을 정리합니다.

---

## 1. 배경: 공식 `openjdk` 이미지의 지원 중단(Deprecation)

Docker Hub의 공식 `library/openjdk` 리포지토리는 공식적으로 **사용 중단(Deprecated)**되었습니다. 

따라서 JDK 21, 24, 25 등 최신 버전을 컨테이너 환경에서 운영하려면 Oracle, Eclipse Adoptium, Amazon 등 **공식 OpenJDK 공급사가 직접 관리하는 컨테이너 레지스트리 이미지를 사용하는 것이 표준**입니다.

---

## 2. Docker Base 이미지 후보 4선 비교

기존 베이스 OS가 `oraclelinux9` (RHEL 9 계열, `glibc`, `dnf/rpm`)이었던 환경을 기준으로 각 대안의 호환성과 특징을 비교합니다.

### ① [강력 추천 1순위] Oracle 공식 JDK 25 (`container-registry.oracle.com/java/jdk:25`)

- **기반 OS**: **Oracle Linux 9 (`glibc`, `dnf/microdnf`)**
- **기존 환경과의 호환성**: **100% 동일 (변경점 제로)**
- **특징**:
  - 기존 `openjdk:22-oraclelinux9`의 직계 후속 이미지입니다.
  - OS 베이스(Oracle Linux 9)와 패키지 매니저(`dnf`)가 완전히 동일하므로, `Dockerfile` 내 기존 OS 패키지 설치 스크립트(`dnf install`), glibc 의존 C 라이브러리, 타임존/로케일 설정을 **수정 없이 그대로 유지**할 수 있습니다.
  - [Oracle No-Fee Terms and Conditions (NFTC)](https://www.oracle.com/downloads/licenses/no-fee-license.html) 라이선스에 따라 상용 프로덕션 환경에서도 무료로 이용 가능합니다. (LTS 출시 후 최소 3년간 무료 보안 패치 제공)

### ② [업계 표준] Eclipse Temurin 25 (`eclipse-temurin:25-jdk-ubi9-minimal` / `eclipse-temurin:25-jdk`)

- **기반 OS**: Red Hat UBI 9 Minimal 또는 Ubuntu 24.04 (`noble`)
- **기존 환경과의 호환성**: 높음 (`ubi9-minimal` 태그 사용 시 RHEL 생태계 유지)
- **특징**:
  - Eclipse Foundation(Adoptium) 주도의 가장 대표적인 글로벌 오픈소스 OpenJDK 배포판입니다.
  - Oracle Linux와 유사한 RHEL/RPM 계열 환경을 원하면 **`eclipse-temurin:25-jdk-ubi9-minimal`** 태그를 사용하여 불필요한 패키지를 줄인 경량 컨테이너를 구성할 수 있습니다.
  - 런타임 전용 경량화가 필요할 경우 JRE 전용 이미지(`eclipse-temurin:25-jre-...`)도 제공됩니다.

### ③ [AWS 인프라 최적화] Amazon Corretto 25 (`amazoncorretto:25-al2023`)

- **기반 OS**: Amazon Linux 2023 (`glibc`, `dnf`)
- **기존 환경과의 호환성**: 높음 (RPM/dnf 패키지 구조 호환)
- **특징**:
  - AWS 인프라(EKS, ECS, EC2)에서 실행되는 워크로드에 가장 권장되는 이미지입니다.
  - Amazon Linux 2023 기반이므로 기존 Oracle Linux 9과 동일하게 `dnf` 패키지 관리자와 `glibc`를 사용하여 마이그레이션이 수월합니다.
  - AWS 외부(온프레미스, 타 클라우드)에서도 라이선스 제약 없이 전액 무료로 사용 가능합니다.

### ④ [경량화 / Spring Boot 최적화] BellSoft Liberica JDK 25 (`bellsoft/liberica-openjdk-alpine:25`)

- **기반 OS**: Alpine Linux (`musl libc`, `apk`)
- **기존 환경과의 호환성**: 보통 (musl libc 호환성 확인 필요)
- **특징**:
  - Spring Boot 공식 레퍼런스이자 Paketo Cloud Native Buildpacks의 기본 JDK 배포판입니다.
  - 이미지 크기(~200MB 이하)를 극대화하여 줄이고 싶을 때 적합합니다.
  - 단, Alpine은 `musl libc`를 사용하므로 JNI 기반 네이티브 라이브러리(암호화 모듈, 일부 DB/네트워크 C 바인딩 등)가 포함된 경우 비호환 문제가 생길 수 있어 사전 테스트가 필수적입니다.

---

## 3. 한눈에 보는 비교 매트릭스

| 항목 | ① Oracle 공식 JDK 25 | ② Eclipse Temurin 25 | ③ Amazon Corretto 25 | ④ BellSoft Liberica (Alpine) |
| :--- | :--- | :--- | :--- | :--- |
| **대표 이미지 태그** | `container-registry.oracle.com/java/jdk:25` | `eclipse-temurin:25-jdk-ubi9-minimal` | `amazoncorretto:25-al2023` | `bellsoft/liberica-openjdk-alpine:25` |
| **기반 OS** | **Oracle Linux 9** | Red Hat UBI 9 Minimal | Amazon Linux 2023 | Alpine Linux |
| **C 표준 라이브러리** | `glibc` | `glibc` | `glibc` | `musl libc` |
| **패키지 관리자** | `dnf` / `microdnf` | `microdnf` | `dnf` | `apk` |
| **라이선스** | Oracle NFTC (무료) | GPL v2 with CE (오픈소스) | GPL v2 with CE (오픈소스) | GPL v2 with CE (오픈소스) |
| **이미지 크기** | 약 450~500 MB | 약 380~420 MB | 약 400~450 MB | **약 180~220 MB (초경량)** |
| **마이그레이션 비용** | **최저 (Dockerfile 수정 없음)** | 낮음 | 낮음 | 보통 (musl 검증 필요) |
| **권장 시나리오** | **기존 OL9 설정 완벽 보존** | 범용 오픈소스 표준 채택 | AWS 인프라 환경 | 이미지 최소화 / Spring 친화 |

---

## 4. Dockerfile 마이그레이션 예제

기존 `openjdk:22-oraclelinux9`에서 1순위 권장안인 Oracle 공식 JDK 25로 전환하는 예시입니다.

```dockerfile
# [기존]
# FROM openjdk:22-oraclelinux9

# [변경 후] Oracle 공식 레지스트리 JDK 25 이미지 적용
FROM container-registry.oracle.com/java/jdk:25

# 기존 dnf 패키지 설치 명령어 변경 없이 그대로 동작
RUN dnf install -y tzdata && dnf clean all

WORKDIR /app
COPY target/*.jar app.jar

# 컨테이너 실행
ENTRYPOINT ["java", "-jar", "app.jar"]
```

---

## 5. JDK 25 전환 후 Pinning 진단 시 주의사항

1. **JEP 491 효과**: 애플리케이션 및 서드파티 라이브러리 내의 `synchronized` 블록으로 인한 Pinning은 코드 수정 없이 JDK 25 런타임 교체만으로 즉시 해결됩니다.
2. **진단 플래그 제거**: JDK 21~23에서 사용하던 `-Djdk.tracePinnedThreads=full` 플래그는 **JDK 24부터 제거**되었습니다.
3. **JFR(Java Flight Recorder) 활용**: C/C++ 네이티브 메서드(JNI)나 Foreign Function 호출로 인한 잔여 Pinning을 모니터링하려면 JFR 이벤트를 활용합니다.
   ```bash
   # JFR 기록과 함께 실행
   java -XX:StartFlightRecording=filename=vt-check.jfr,settings=profile -jar app.jar

   # Pinning 이벤트 조회
   jfr print --events jdk.VirtualThreadPinned vt-check.jfr
   ```

---

## 🔗 관련 문서

- [Virtual Thread: FTP 처리의 Pinning 진단](Virtual_Threads_FTP_Pinning.md)
- [JDBI와 Virtual Thread: Bounded Executor 격리](SpringBoot/JDBI_VT_Pinning_Solution.md)
- [Java 25 주요 기능 및 정식/Preview 구분](Versions/Java25.md)
