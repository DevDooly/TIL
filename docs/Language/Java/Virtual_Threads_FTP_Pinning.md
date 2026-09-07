# Virtual Thread: FTP 처리의 Pinning 진단

확인 기준: JDK 21 / 24 이후 동작 구분, 2026-09-07. FTP와 SFTP는 다른 프로토콜·라이브러리이므로 같은 내부 구현으로 취급하지 않는다.

## 증상과 원인 가설

파일 전송 지연이나 요청 정지는 pinning, 서버 응답 지연, 연결 부족, 파일 I/O, 애플리케이션 lock 경합으로 발생할 수 있다. Commons Net이라는 라이브러리 이름만으로 모든 실행 경로가 pinning을 일으킨다고 단정하지 않는다.

실무 분석 기록에는 JDK와 라이브러리 버전, 전송 모드, 동시 연결 수, 파일 크기, timeout, 재현 조건과 실제 stack을 함께 남긴다. 이 문서만으로 특정 운영 장애의 원인이 확인되었다고 볼 수 없다.

## JDK별 진단

| 기준 | 확인 사항 |
| :--- | :--- |
| JDK 21–23 | monitor를 잡은 채 blocking하는 경로 확인. `-Djdk.tracePinnedThreads=full`과 JFR 활용 |
| JDK 24 이후 | JEP 491로 monitor 관련 pinning 개선. native/foreign 호출 등 남는 경로 확인 |
| 공통 | JFR 이벤트 지속 시간과 전송 지연·CPU·lock 대기 시점을 대조 |

JDK 24에서 `jdk.tracePinnedThreads` 속성은 제거되었다. 이후 버전에서도 동일 옵션을 핵심 진단법으로 안내하면 안 된다. [JEP 491](https://openjdk.org/jeps/491), [JDK 21 진단](https://docs.oracle.com/en/java/javase/21/core/virtual-threads.html), [JDK 25 진단](https://docs.oracle.com/en/java/javase/25/core/virtual-threads.html)

기록된 JFR 파일의 pinning 이벤트는 다음과 같이 확인한다. 이벤트가 없다고 모든 blocking 문제가 없다는 뜻은 아니며 recording 설정과 threshold도 확인한다.

```bash
jfr print --events jdk.VirtualThreadPinned recording.jfr
```

## 개선 선택

1. 증상이 재현되는 driver/library/JDK 조합을 고정한다.
2. 실제 수정이 포함된 버전으로 변경하고 동일 입력으로 비교한다.
3. 애플리케이션 lock 범위를 줄일 수 있는지 검토한다. lock을 통째로 제거하기 전에 공유 상태의 불변식을 확인한다.
4. 업그레이드가 어렵다면 확인된 경로만 [제한된 플랫폼 실행기](SpringBoot/JDBI_VT_Pinning_Solution.md)로 격리한다.

`synchronized`를 `ReentrantLock`으로 바꿔도 lock을 잡은 채 전송하면 작업 간 직렬화는 그대로다. Pinning 감소와 업무 처리 병렬화는 별도로 측정한다.

## FTP 예제에서 빠뜨리기 쉬운 것

- 연결·로그인 실패와 `storeFile`의 boolean 반환값 검사
- 입력 스트림과 FTP 연결의 정상·실패 경로 정리
- connection/data/socket timeout과 재시도 한도
- 임시 이름으로 업로드 후 완료 처리, 부분 업로드의 재처리 정책
- 실행 수뿐 아니라 대기 큐의 상한

FTP API별 반환값과 자원 수명은 사용하는 버전의 공식 문서를 확인한다. [FTPClient API](https://commons.apache.org/proper/commons-net/apidocs/org/apache/commons/net/ftp/FTPClient.html)

처리량 개선을 기록할 때는 전후 시간, bytes, 동시 연결 수, 오류율과 측정 환경을 함께 남긴다. 근거 없는 개선율을 사례의 결과로 쓰지 않는다.
