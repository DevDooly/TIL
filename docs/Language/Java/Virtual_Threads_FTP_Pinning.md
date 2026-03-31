# Java Virtual Threads: FTP/SFTP 사용 시 Pinning 이슈

가상 스레드(Virtual Threads)는 I/O 바운드 작업에서 높은 효율을 보여주지만, 레거시 네트워크 라이브러리인 **FTP(Apache Commons Net)**나 **SFTP(JSch)**를 사용할 때는 **Thread Pinning** 현상으로 인해 성능이 급격히 저하될 수 있습니다.

---

## 1. Pinning 발생 원인 분석

### 1.1 Apache Commons Net (FTP)
*   **원인**: 이 라이브러리는 설계된 지 매우 오래되었으며, 내부적으로 소켓 통신을 처리할 때 `synchronized` 키워드를 사용하여 임계 구역을 관리합니다.
*   **현상**: 가상 스레드가 FTP 서버와 데이터를 주고받는 동안 `synchronized` 블록 안에서 블로킹 I/O가 발생하면, 실제 OS 스레드(Carrier Thread)를 반납하지 못하고 고정(Pinned)됩니다.

### 1.2 JSch (SFTP)
*   **원인**: SSH 통신을 담당하는 JSch는 내부 파이프 스트림(`PipedInputStream`) 및 채널 관리 로직에서 강한 동기화(`synchronized`)를 사용합니다.
*   **현상**: 대용량 파일 전송 시 가상 스레드가 계속해서 Carrier Thread를 점유하게 되어, 동시 전송 작업이 많아질수록 시스템의 사용 가능한 OS 스레드가 고갈됩니다.

---

## 2. 실전 트러블슈팅 사례

**상황**: Spring Boot에서 가상 스레드를 활성화하고 수백 개의 파일을 동시에 FTP로 업로드 시도.
*   **기대**: 가상 스레드이므로 수백 개의 업로드가 효율적으로 처리되어야 함.
*   **실제**: 업로드 속도가 현저히 느려지거나, 일부 요청이 타임아웃 발생. 다른 비즈니스 로직(API 호출 등)까지 함께 느려짐.
*   **진단**: `-Djdk.tracePinnedThreads=full` 옵션 확인 결과, `org.apache.commons.net.ftp.FTPClient` 내부 메서드에서 Pinning 발생 확인.

---

## 3. 해결 및 우회 전략

### 3.1 최신 라이브러리 업데이트 (Java 24+)
*   **Java 24 (JEP 491)**부터는 `synchronized` 블록 내에서의 Pinning 이슈가 대부분 해결될 예정입니다. 가급적 최신 JDK 버전을 유지하는 것이 장기적인 해결책입니다.

### 3.2 플랫폼 스레드 풀 활용 (Offloading)
라이브러리 자체를 수정할 수 없다면, Pinning이 발생하는 특정 작업만 **전통적인 플랫폼 스레드(Platform Threads)**에서 실행하도록 격리합니다.

```java
// FTP 전용 플랫폼 스레드 풀 생성
private final ExecutorService ftpExecutor = Executors.newFixedThreadPool(10);

public void uploadFile(byte[] data) {
    // 가상 스레드 내에서 호출하더라도, 실제 FTP 작업은 플랫폼 스레드에게 위임
    ftpExecutor.submit(() -> {
        FTPClient client = new FTPClient();
        client.connect("server");
        client.storeFile("remote-path", new ByteArrayInputStream(data));
        // ...
    });
}
```

### 3.3 가상 스레드 친화적 대안 라이브러리 검토
*   **sshj**: JSch의 현대적인 대안으로, 보다 나은 동시성 모델을 제공하려 노력하는 프로젝트입니다.
*   **NIO 기반 클라이언트**: Netty 등을 기반으로 한 비동기 FTP 클라이언트를 사용하면 가상 스레드 없이도 높은 성능을 낼 수 있습니다.

---

## 4. 요약
FTP/SFTP 작업은 전형적인 I/O 바운드 작업이라 가상 스레드와 궁합이 좋아 보이지만, **라이브러리 내부의 `synchronized` 구조**가 발목을 잡습니다. 
1.  **진단 옵션**으로 Pinning 여부를 먼저 확인하세요.
2.  해결되지 않는다면 **별도의 플랫폼 스레드 풀**로 FTP 작업만 격리하여 실행하는 것이 가장 현실적인 대안입니다.
