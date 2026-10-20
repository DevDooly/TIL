# Java 버전 관리 도구 `jenv`와 `JEP`(JDK Enhancement Proposal) 정리

Java 개발 환경에서 `jev`로 자주 오기하거나 검색하는 대상은 로컬 다중 JDK 버전을 전환하는 CLI 도구인 **`jenv`(Java Environment Manager)**와 OpenJDK의 공식 기능 제안 문서인 **`JEP`(JDK Enhancement Proposal)** 두 가지다.

## 1. `jenv`: 로컬 다중 JDK 버전 전환 도구

한 개발 장비에 JDK 17과 JDK 21처럼 여러 버전의 JDK가 함께 설치되어 있을 때, 프로젝트 디렉터리나 터미널 세션마다 `PATH`와 `JAVA_HOME`을 수동으로 고치는 작업은 번거롭고 실수하기 쉽다. `jenv`는 Python의 `pyenv`, Node.js의 `nvm`처럼 **이미 시스템에 설치된 여러 JDK 경로를 등록해 두고 전역(Global)·폴더(Local)·현재 셸(Shell) 단위로 Java 버전을 전환**한다.

### 동작 원리 (Shim 방식과 버전 우선순위)

`jenv`는 `~/.jenv/shims` 디렉터리를 `PATH`의 가장 앞에 배치한다. 사용자가 터미널에서 `java`, `javac`, `jar` 같은 명령을 실행하면 실제 JDK 바이너리 대신 `jenv`의 심(Shim) 실행 파일이 먼저 호출된다. 심은 다음 우선순위에 따라 실행할 JDK 버전을 결정하고 해당 경로의 바이너리로 실행을 넘긴다.

1. **`shell` (`JENV_VERSION` 환경 변수)**: 현재 터미널 세션에만 임시로 지정한 버전 (`jenv shell 21.0`)
2. **`local` (`.java-version` 파일)**: 현재 작업 디렉터리(또는 상위 디렉터리)에 있는 `.java-version` 파일에 적힌 버전 (`jenv local 17.0`)
3. **`global` (`~/.jenv/version` 파일)**: 위 두 설정이 없을 때 사용하는 사용자 기본 버전 (`jenv global 21.0`)

### 설치 및 초기 설정 (Linux / macOS)

`jenv`는 JDK를 직접 다운로드해 주지 않으므로, 먼저 패키지 매니저(`apt`, `brew`)나 수동 설치로 필요한 JDK가 설치되어 있어야 한다.

```bash
# 1. jenv 클론 (macOS Homebrew 환경이라면 brew install jenv 가능)
git clone https://github.com/jenv/jenv.git ~/.jenv

# 2. 사용하는 셸 설정 파일(~/.bashrc 또는 ~/.zshrc)에 PATH와 초기화 스크립트 추가
echo 'export PATH="$HOME/.jenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(jenv init -)"' >> ~/.bashrc
source ~/.bashrc
```

초기화 직후에는 반드시 **`export` 플러그인을 활성화**해야 한다. 기본적으로 `jenv`는 `java` 실행 경로만 가로채고 `JAVA_HOME` 환경 변수는 바꾸지 않기 때문에, `export` 플러그인이 꺼져 있으면 Maven, Gradle이나 `JAVA_HOME`을 직접 읽는 스크립트가 엉뚱한 JDK를 바라보게 된다.

```bash
# 셸 프롬프트 전환 시 JAVA_HOME을 자동으로 갱신하는 export 플러그인 활성화
jenv enable-plugin export

# 새 셸 세션에 반영한 뒤 설정 상태 점검
exec "$SHELL" -l
jenv doctor
```

### JDK 등록과 버전 전환 명령어

시스템에 설치된 JDK 루트 디렉터리(`bin/java`의 상위 경로)를 `jenv add`로 등록한 뒤 사용한다.

```bash
# Linux (Ubuntu OpenJDK 경로 예시)
jenv add /usr/lib/jvm/java-17-openjdk-amd64
jenv add /usr/lib/jvm/java-21-openjdk-amd64

# macOS (설치된 JDK 경로 예시)
# jenv add "$(/usr/libexec/java_home -v 21)"

# 등록된 버전 목록과 현재 선택된 버전(*) 확인
jenv versions

# 1) 시스템 전역 기본 버전을 21로 설정
jenv global 21.0

# 2) 특정 프로젝트 폴더에서만 JDK 17을 쓰도록 고정 (.java-version 파일 생성)
cd ~/workspace/legacy-service
jenv local 17.0

# 3) 현재 열린 터미널 창에서만 일시적으로 JDK 21 사용
jenv shell 21.0
```

`.java-version` 파일은 Git 저장소에 커밋해 팀원들과 프로젝트의 대상 JDK 버전을 맞추는 용도로도 사용할 수 있다.

### `jenv` 사용 시 주의할 점

- **비대화형(Non-interactive) 셸에서의 `JAVA_HOME`**: `jenv`의 `export` 플러그인은 셸 프롬프트 훅(`PROMPT_COMMAND` 또는 `precmd`)을 통해 `JAVA_HOME`을 갱신한다. 따라서 CI 스크립트나 IDE 외부 실행기처럼 프롬프트가 렌더링되지 않는 비대화형 셸에서는 `jenv local`이 있어도 `JAVA_HOME`이 즉시 세팅되지 않을 수 있다. 스크립트 안에서 `JAVA_HOME`이 필요할 때는 `export JAVA_HOME="$(jenv javahome)"`을 명시적으로 호출한다.
- **새 JDK 바이너리 추가 후 `rehash`**: 플러그인을 추가했거나 JDK 내부 실행 파일 구성을 바꾼 뒤에는 `jenv rehash`를 실행해 심 목록을 갱신한다.

## 2. Java 버전 관리 도구 비교 (`jenv` vs `SDKMAN!` vs `update-java-alternatives`)

상황에 따라 `jenv` 대신 JDK 설치까지 지원하는 도구(`SDKMAN!`)나 OS 기본 명령을 쓰는 편이 나을 수 있다.

| 구분 | `jenv` | `SDKMAN!` (`sdk`) | `update-java-alternatives` |
| :--- | :--- | :--- | :--- |
| **JDK 다운로드·설치** | 미지원 (이미 설치된 JDK 경로만 등록) | 지원 (Temurin, Corretto, GraalVM 등 목록에서 바로 설치) | 미지원 (`apt` 등으로 먼저 설치 필요) |
| **디렉터리별 자동 전환** | 기본 지원 (`.java-version` 파일 감지) | 지원 (`.sdkmanrc` 생성 및 `sdkman_auto_env=true` 설정 시) | 미지원 (시스템 전체 `/usr/bin/java` 링크 변경) |
| **권한 요구 사항** | 사용자 권한 (`~/.jenv`) | 사용자 권한 (`~/.sdkman`) | `root` (`sudo`) 권한 필요 |
| **적합한 환경** | 사내 정책이나 OS 패키지로 설치된 JDK들을 폴더별로 빠르게 전환할 때 | 다양한 벤더의 JDK와 Gradle·Maven·Kotlin 버전까지 한 번에 설치·관리할 때 | 단일 서버나 컨테이너에서 시스템 기본 JDK 버전을 고정할 때 |

## 3. `JEP` (JDK Enhancement Proposal)

`JEP`는 OpenJDK 커뮤니티에서 **Java 언어 문법, 표준 라이브러리 API, JVM 내부 아키텍처의 중요한 변경 사항을 제안하고 설계 근거를 기록하는 공식 문서**다. 각 제안에는 고유 번호가 부여되며, 기능이 왜 필요한지(Motivation), 어떻게 동작하는지(Description), 어떤 대안을 검토했는지(Alternatives), 어떤 위험과 가정이 있는지(Risks and Assumptions)를 담는다.

### 기능 도입 단계: Incubator · Preview · Standard

새로운 기능이 JEP를 통해 JDK에 들어올 때는 호환성 문제를 줄이기 위해 단계를 거친다(JEP 12).

| 단계 | 특징 | 컴파일·실행 조건 |
| :--- | :--- | :--- |
| **Incubator (인큐베이터)** | 아직 표준 패키지(`java.*`)에 넣기 전 `jdk.incubator.*` 모듈에서 API 설계를 실험하는 단계. 버전이 올라가면서 시그니처가 크게 바뀔 수 있다. | `--add-modules jdk.incubator.<모듈명>` 필요 |
| **Preview (프리뷰)** | 언어 문법이나 `java.*` 표준 API 형태는 갖췄으나 정식 확정 전 실사용 피드백을 수집하는 단계. | 컴파일·실행 모두 `--enable-preview` 필요 (`javac --release N --enable-preview`) |
| **Standard (정식 표준)** | 피드백 반영을 마치고 영구(Permanent) 기능으로 확정된 단계. | 별도 플래그 없이 기본 사용 가능 |

예를 들어 표준 HTTP Client API는 Java 9에서 **JEP 110(Incubator)**으로 처음 도입되어 실험을 거친 뒤, Java 11에서 **JEP 321(Standard)**을 통해 `java.net.http.HttpClient`로 정식 승격되었다.

### 자주 참고하는 주요 JEP 목록

실무에서 버전 업그레이드나 성능 진단을 할 때 자주 찾아보는 대표 JEP는 다음과 같다.

| JEP 번호 | 대상 버전 | 핵심 내용 | 관련 내부 문서 |
| :--- | :--- | :--- | :--- |
| **JEP 321** | Java 11 | HTTP Client (Standard): `HttpClient`, `HttpRequest`, `HttpResponse` 표준화 및 HTTP/2·비동기 지원 | [HttpClient JSON REST API 예제](HttpClient_REST_API_JSON_Example.md), [Java 11](Versions/Java11.md) |
| **JEP 395** | Java 16 | Records: 불변 데이터 운반 객체(`record`) 정식 도입 | [Java 17](Versions/Java17.md) |
| **JEP 444** | Java 21 | Virtual Threads: 경량 가상 스레드 정식 도입 | [Java 21](Versions/Java21.md), [K8s 환경 Virtual Threads 분석](Virtual_Threads_in_K8s.md) |
| **JEP 491** | Java 24 | Synchronize Virtual Threads without Pinning: `synchronized` 블록 내 가상 스레드 피닝(Pinning) 해소 | [Virtual Threads: FTP Pinning 진단](Virtual_Threads_FTP_Pinning.md), [Java 25](Versions/Java25.md) |

## 관련 문서 및 참고 자료

- 내부 문서
  - [Java 버전별 변경점 요약](Versions/README.md)
  - [Java 문서 모음](README.md)
- 외부 공식 자료
  - [jenv 공식 저장소 및 문서 (GitHub)](https://github.com/jenv/jenv)
  - [OpenJDK JEP 0: JEP Index](https://openjdk.org/jeps/0)
  - [OpenJDK JEP 1: JDK Enhancement-Proposal & Roadmap Process](https://openjdk.org/jeps/1)
  - [OpenJDK JEP 12: Preview Features](https://openjdk.org/jeps/12)
