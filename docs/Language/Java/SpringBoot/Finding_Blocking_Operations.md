# Netty 환경에서 Blocking 코드/라이브러리를 찾는 방법

Spring WebFlux나 Netty 기반 애플리케이션에서 Event Loop가 차단되면 시스템 전체의 처리량이 급격히 떨어집니다. 이를 방지하기 위해 Blocking 지점을 찾아내는 기술적인 방법들을 정리합니다.

---

## 1. 흔한 Blocking API 패턴 (정적 분석)

먼저 코드나 의존성 목록에서 다음과 같은 API가 사용되고 있는지 확인해야 합니다.

### 1.1 데이터베이스 및 외부 호출

* **JDBC 기반 드라이버**: `spring-boot-starter-data-jpa`, `hibernate`, `mybatis` 등은 본질적으로 Blocking 방식입니다. (대안: R2DBC)
* **동기 HTTP 클라이언트**: `RestTemplate`, `Apache HttpClient`, `OkHttp` (대안: WebClient)
* **클라우드 SDK**: 구형 AWS SDK 등은 내부적으로 동기 호출을 수행하는 경우가 많습니다.

### 1.2 자바 표준 API

* **Thread.sleep()**: 절대 금지.
* **java.io**: `FileInputStream`, `FileOutputStream` 등 표준 I/O. (대안: java.nio 또는 전용 비동기 라이브러리)
* **CountDownLatch.await()**, **Future.get()**: 결과를 무한정 기다리는 작업.
* **synchronized 블록**: 락 경합이 심할 경우 가상 스레드 환경에서는 Pinning, Netty 환경에서는 스레드 점유 문제를 일으킵니다.

---

## 2. BlockHound를 이용한 자동 검출 (가장 확실한 방법)

**BlockHound**는 Java 에이전트로 동작하며, Event Loop 스레드에서 Blocking 호출이 발생하는 즉시 예외를 던져 개발자에게 알려주는 도구입니다.

### 2.1 의존성 추가

**Gradle**:
```gradle
dependencies {
    testImplementation 'io.projectreactor.tools:blockhound:1.0.8.RELEASE'
}
```

**Maven**:
```xml
<dependency>
    <groupId>io.projectreactor.tools</groupId>
    <artifactId>blockhound</artifactId>
    <version>1.0.8.RELEASE</version>
    <scope>test</scope>
</dependency>
```

### 2.2 설정
애플리케이션 시작 시점에 설치합니다.

```java
public static void main(String[] args) {
    BlockHound.install(); // 반드시 애플리케이션 실행 전 최상단에서 호출
    SpringApplication.run(MyApplication.class, args);
}
```

### 2.3 동작 방식
만약 `WebFlux` 로직 안에서 `Thread.sleep()`이나 `JDBC` 호출이 발생하면 다음과 같은 에러를 내뱉으며 프로세스를 중단시킵니다.
> `Blocking call! java.lang.Thread.sleep`

---

## 3. 스레드 덤프(Thread Dump) 분석

애플리케이션이 구동 중일 때 `jstack` 명령어를 통해 스레드의 상태를 확인합니다.

```bash
jstack <pid> > dump.txt
```

* **관찰 대상**: `reactor-http-nio-X` 또는 `nioEventLoopGroup-X-X` 이름을 가진 스레드들.
* **위험 징후**: 이 스레드들의 상태가 `RUNNABLE`이 아닌 **`WAITING`**, **`TIMED_WAITING`**, 또는 **`BLOCKED`** 상태로 특정 라이브러리 코드에 머물러 있다면 그곳이 바로 병목 지점입니다.

---

## 4. 로깅을 통한 추적 (Reactor Debug)

Reactor 라이브러리에서 제공하는 디버그 옵션을 활성화하면 Blocking 발생 지점의 스택 트레이스를 더 상세히 볼 수 있습니다.

```java
Hooks.onOperatorDebug();
```
*주의: 성능 오버헤드가 크므로 운영 환경이 아닌 개발 환경에서만 사용하세요.*

---

## 5. 요약: 찾는 순서

1. **Dependency 체크**: `starter-jdbc`, `jpa` 등이 포함되어 있는지 확인합니다.
2. **BlockHound 적용**: 로컬/테스트 환경에서 BlockHound를 켜고 비즈니스 로직을 수행해 봅니다.
3. **프로파일링**: `VisualVM`이나 `IntelliJ Profiler`를 통해 Netty 스레드가 유휴 시간 없이 실제로 "일을 하고 있는지" 아니면 "기다리고 있는지"를 모니터링합니다.

이 가이드를 통해 Netty의 성능을 100% 활용하지 못하게 방해하는 Blocking 지점들을 효율적으로 제거할 수 있습니다.
