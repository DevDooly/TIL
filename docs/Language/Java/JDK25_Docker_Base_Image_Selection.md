# JDK 25 Docker Base 이미지 선택: Virtual Thread Pinning 해결 및 마이그레이션

Java 21~23의 가상 스레드(Virtual Threads) 환경에서 `synchronized` 블록 내 I/O 블로킹 작업으로 인해 발생하던 **스레드 고정(Pinning) 및 캐리어 스레드 풀 고갈 이슈**는 **JDK 24의 JEP 491 (Synchronize Virtual Threads without Pinning)**을 통해 근본적으로 해결되었습니다. 

차기 LTS 버전인 **JDK 25**를 프로덕션에 도입하여 Pinning 문제를 해결할 때, 기존 `openjdk:22-oraclelinux9` 이미지를 대체할 최적의 Docker Base 이미지 선정 기준과 **Oracle 이미지의 라이선스·업데이트 리스크**를 상세히 분석하고 최적 대안을 정리합니다.

---

## 1. ⚠️ Oracle Linux / Oracle JDK 기반 이미지의 치명적 리스크 분석

기존에 `openjdk:*-oraclelinux9`을 사용했거나 Oracle 공식 컨테이너 레지스트리를 검토할 때, **프로덕션 환경에서는 다음과 같은 중대한 위험 요소를 반드시 고려**해야 합니다.

### ① NFTC 라이선스의 '시한부 무료' 함정과 라이선스 변경 리스크

- Oracle은 JDK 17부터 [Oracle No-Fee Terms and Conditions (NFTC)](https://www.oracle.com/downloads/licenses/no-fee-license.html)를 통해 상용 무료를 표방했으나, 이는 **"차기 LTS 릴리스 후 1년까지만 무료"**라는 시한부 조건입니다.
- **실제 사례**: JDK 17은 JDK 21이 출시(2023년 9월)된 후 1년이 지난 **2024년 9월에 NFTC 무료 기간이 공식 종료**되었으며, 이후 배포되는 보안 패치는 다시 유료 라이선스(OTN) 대상으로 전환되었습니다.
- 기업에서 컨테이너 이미지를 한 번 배포한 후 장기 운영하다가 무료 기간 만료 시점을 놓치면, Oracle의 강력한 **라이선스 감사(Audit) 및 막대한 위약금/소급 과금 리스크**에 직면하게 됩니다.
- 2023년 Oracle이 발표한 '전사 직원 수(Employee Metric)' 기준 과금제 등 예측 불가능한 라이선스 정책 변경 이력 때문에 엔터프라이즈 환경에서는 Oracle 공식 이미지 채택을 극도로 기피하는 추세입니다.

### ② OpenJDK 컨테이너 이미지 업데이트 지연 및 사실상 방치 문제

- Docker Hub 공식 `library/openjdk`의 `oraclelinux` 태그는 이미 **지원 중단(Deprecated)**되었습니다.
- Oracle Container Registry(`container-registry.oracle.com`)의 커뮤니티용 OpenJDK 이미지는 릴리스 후 6개월만 유지보수되며, 신규 버전 출시 시 기존 버전의 보안 패치 컨테이너 빌드가 매우 불규칙하거나 중단되는 사례가 빈번합니다.
- 결과적으로 CVE 보안 취약점이 발견되어도 적시에 패치된 베이스 이미지를 공급받기 어렵습니다.

> [!CAUTION]
> **결론**: 기존 `Dockerfile` 설정을 바꾸지 않으려고 Oracle 공식 이미지를 그대로 쓰는 것은 **"시한폭탄 같은 라이선스 감사 위험과 보안 패치 중단"**을 떠안는 위험한 선택입니다. 프로덕션 환경에서는 반드시 **GPL v2 with Classpath Exception (GPL v2 + CE)** 라이선스를 따르는 검증된 오픈소스 OpenJDK 배포판으로 전환해야 합니다.

---

## 2. 권장 Docker Base 이미지 후보 비교

기존 베이스 OS가 `oraclelinux9` (RHEL 9 계열, `glibc`, `dnf/rpm`)이었던 환경을 기준으로, **라이선스 리스크가 전혀 없으면서 OS 패키지 호환성을 보존할 수 있는 대안**을 추천 순위별로 정리합니다.

### ① [강력 추천 1순위] Eclipse Temurin 25 with UBI 9 Minimal (`eclipse-temurin:25-jdk-ubi9-minimal`)

- **기반 OS**: **Red Hat Universal Base Image 9 Minimal (`ubi9-minimal`, `glibc`, `microdnf`)**
- **라이선스**: **GPL v2 with CE (완전 무료, 상용 제약 제로, 라이선스 감사 위험 없음)**
- **특징**:
  - Eclipse Foundation(Adoptium 프로젝트)에서 빌드하며, 전 세계 엔터프라이즈에서 가장 널리 쓰이는 **사실상의 업계 표준(De Facto Standard)**입니다.
  - Red Hat의 공식 UBI 9 기반 태그(`ubi9-minimal`)를 사용하므로, **기존 Oracle Linux 9과 동일한 RHEL 9 계열 패키지 생태계 및 glibc 환경**을 완벽하게 유지합니다.
  - `microdnf` 명령어로 기존 RPM 패키지를 설치할 수 있어 Dockerfile 수정이 최소화됩니다.
  - 범용적인 Debian/Ubuntu 환경을 선호한다면 `eclipse-temurin:25-jdk` (Ubuntu noble 기반)도 훌륭한 선택입니다.

### ② [강력 추천 2순위] Amazon Corretto 25 (`amazoncorretto:25-al2023`)

- **기반 OS**: **Amazon Linux 2023 (`al2023`, `glibc`, `dnf`)**
- **라이선스**: **GPL v2 with CE (완전 무료, 상용 제약 제로)**
- **특징**:
  - AWS가 직접 빌드하고 장기 지원(LTS)을 보장하는 프로덕션급 OpenJDK입니다.
  - Amazon Linux 2023은 Fedora/RHEL 기반이므로 **기존 Oracle Linux 9과 마찬가지로 `dnf` 패키지 관리자와 `glibc`**를 기본 제공합니다. 기존 Dockerfile의 `dnf install` 명령어를 단 한 줄도 고치지 않고 그대로 사용할 수 있습니다.
  - AWS 환경(EKS, ECS, EC2)뿐만 아니라 온프레미스 및 타 클라우드에서도 아무런 제약 없이 무료로 사용할 수 있습니다.

### ③ [경량화 / Spring 친화] BellSoft Liberica JDK 25 (`bellsoft/liberica-openjdk-alpine:25`)

- **기반 OS**: Alpine Linux (`musl libc`, `apk`)
- **라이선스**: **GPL v2 with CE (완전 무료)**
- **특징**:
  - Spring Boot 공식 레퍼런스이자 Paketo Buildpacks의 기본 JDK 배포판입니다.
  - 이미지 크기(~200MB)를 극도로 줄이고 싶을 때 최적입니다.
  - **주의**: Alpine의 `musl libc` 특성상 JNI 기반 네이티브 라이브러리(C 바인딩, 특정 암호화/압축 모듈) 사용 시 호환성 검증이 선행되어야 합니다.

### ④ [⚠️ 운영 비추천 / 임시 테스트용] Oracle 공식 JDK 25 (`container-registry.oracle.com/java/jdk:25`)

- **기반 OS**: Oracle Linux 9 (`glibc`, `dnf`)
- **라이선스**: **Oracle NFTC (차기 LTS 출시 1년 후 유료 전환)**
- **평가**:
  - OS와 JDK가 기존 환경과 100% 동일하여 로컬 검증이나 임시 테스트에는 유용할 수 있으나, **앞서 언급한 NFTC 라이선스 만료 및 업데이트 지연 리스크로 인해 프로덕션 배포에는 권장하지 않습니다.**

---

## 3. 한눈에 보는 비교 매트릭스

| 항목 | ① Eclipse Temurin 25 (UBI 9) | ② Amazon Corretto 25 (AL2023) | ③ BellSoft Liberica (Alpine) | ④ Oracle 공식 JDK 25 |
| :--- | :--- | :--- | :--- | :--- |
| **추천 등급** | **[1순위] 엔터프라이즈 표준** | **[2순위] AWS / dnf 호환 표준** | [3순위] 이미지 경량화 | **[비추천] 라이선스 리스크** |
| **대표 태그** | `eclipse-temurin:25-jdk-ubi9-minimal` | `amazoncorretto:25-al2023` | `bellsoft/liberica-openjdk-alpine:25` | `container-registry.oracle.com/java/jdk:25` |
| **기반 OS** | **Red Hat UBI 9 Minimal** | **Amazon Linux 2023** | Alpine Linux | Oracle Linux 9 |
| **C 표준 라이브러리** | `glibc` | `glibc` | `musl libc` | `glibc` |
| **패키지 관리자** | `microdnf` | `dnf` | `apk` | `dnf` |
| **라이선스** | **GPL v2 with CE (평생 무료)** | **GPL v2 with CE (평생 무료)** | **GPL v2 with CE (평생 무료)** | **NFTC (시한부 무료 $\rightarrow$ 유료)** |
| **라이선스 감사 리스크** | **없음 (0%)** | **없음 (0%)** | **없음 (0%)** | **높음 (유료 전환 위험)** |
| **보안 패치 주기** | 분기별 정기 CPU 즉각 반영 | 분기별 정기 CPU 즉각 반영 | 정기 반영 | 불규칙 / 지연 가능성 |
| **기존 OL9 호환성** | **매우 높음 (RHEL 9 계열)** | **매우 높음 (dnf 완벽 호환)** | 보통 (musl 호환성 점검) | 동일 |

---

## 4. 권장 Dockerfile 마이그레이션 예제

기존 `openjdk:22-oraclelinux9`의 RHEL/RPM 생태계를 안전하게 계승하는 2가지 모범 예시입니다.

### 방법 A: [1순위] Eclipse Temurin (Red Hat UBI 9 Minimal 기반)
```dockerfile
# Eclipse Temurin 공식 UBI 9 Minimal 이미지 채택
FROM eclipse-temurin:25-jdk-ubi9-minimal

# microdnf를 사용해 필요한 패키지 설치 (RHEL 계열 RPM 패키지 호환)
USER root
RUN microdnf install -y tzdata && microdnf clean all

WORKDIR /app
COPY target/*.jar app.jar

# 보안 강화를 위한 비루트 실행
USER 1001
ENTRYPOINT ["java", "-jar", "app.jar"]
```

### 방법 B: [2순위] Amazon Corretto (Amazon Linux 2023 기반 - 기존 dnf 명령어 100% 유지)
```dockerfile
# Amazon Corretto 공식 AL2023 이미지 채택
FROM amazoncorretto:25-al2023

# 기존 Oracle Linux에서 사용하던 dnf 명령어를 수정 없이 그대로 사용 가능
RUN dnf install -y tzdata && dnf clean all

WORKDIR /app
COPY target/*.jar app.jar

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
