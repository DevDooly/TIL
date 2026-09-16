# Virtual Thread: FTP 처리의 Pinning 진단

가상 스레드에서 FTP 전송이 느려지면 먼저 어디서 기다리는지 살펴봐야 한다. Pinning 진단 방법은 JDK 21–23과 24 이후가 다르다. FTP와 SFTP도 사용하는 프로토콜과 라이브러리가 달라 각각의 호출 경로를 확인해야 한다.

## 증상과 원인 가설

전송 지연은 서버 응답, 연결 부족, 파일 I/O, 애플리케이션의 락 경합에서도 생긴다. Commons Net을 사용한다는 사실만으로 pinning을 원인으로 잡으면 이런 병목을 놓칠 수 있다.

원인을 좁힐 때는 JDK·라이브러리 버전과 스택을 함께 본다. 전송 모드, 동시 연결 수, 파일 크기, 타임아웃을 기록해 두면 같은 조건으로 재현하기 쉽다.

## JDK별 진단

| 기준 | 확인 사항 |
| :--- | :--- |
| JDK 21–23 | monitor를 잡은 채 blocking하는 경로 확인. `-Djdk.tracePinnedThreads=full`과 JFR 활용 |
| JDK 24 이후 | JEP 491로 monitor 관련 pinning 개선. native/foreign 호출 등 남는 경로 확인 |
| 공통 | JFR 이벤트 지속 시간과 전송 지연·CPU·lock 대기 시점을 대조 |

JDK 24부터는 `jdk.tracePinnedThreads` 속성이 제거되었으므로 JDK 21에서 쓰던 옵션을 그대로 사용할 수 없다. [JEP 491](https://openjdk.org/jeps/491), [JDK 21 진단](https://docs.oracle.com/en/java/javase/21/core/virtual-threads.html), [JDK 25 진단](https://docs.oracle.com/en/java/javase/25/core/virtual-threads.html)

JFR 파일에서 pinning 이벤트만 보려면 다음 명령을 사용한다. 이벤트가 보이지 않을 때는 기록 설정과 임계값도 확인한다. 다른 이유로 블로킹된 작업은 이 이벤트에 나타나지 않을 수 있다.

```bash
jfr print --events jdk.VirtualThreadPinned recording.jfr
```

## 원인을 확인한 뒤 바꿀 것

1. 증상이 재현되는 driver/library/JDK 조합을 고정한다.
2. 실제 수정이 포함된 버전으로 변경하고 동일 입력으로 비교한다.
3. 애플리케이션 lock 범위를 줄일 수 있는지 검토한다. lock을 통째로 제거하기 전에 공유 상태의 불변식을 확인한다.
4. 업그레이드가 어렵다면 확인된 경로만 [제한된 플랫폼 실행기](SpringBoot/JDBI_VT_Pinning_Solution.md)로 격리한다.

`synchronized`를 `ReentrantLock`으로 바꿔도 lock을 잡은 채 전송하면 작업 간 직렬화는 그대로다. Pinning이 줄어도 전송 처리량이 그대로일 수 있는 이유다.

## FTP 예제에서 빠뜨리기 쉬운 것

- 연결·로그인 실패와 `storeFile`의 boolean 반환값 검사
- 입력 스트림과 FTP 연결의 정상·실패 경로 정리
- connection/data/socket timeout과 재시도 한도
- 임시 이름으로 업로드 후 완료 처리, 부분 업로드의 재처리 정책
- 실행 수뿐 아니라 대기 큐의 상한

FTP API별 반환값과 자원 수명은 사용하는 버전의 공식 문서를 확인한다. [FTPClient API](https://commons.apache.org/proper/commons-net/apidocs/org/apache/commons/net/ftp/FTPClient.html)

변경 효과는 같은 파일과 동시 연결 수로 비교한다. 전송 시간과 바이트 수뿐 아니라 오류율도 함께 보면, 단순히 요청을 더 많이 보내서 얻은 처리량인지 구분할 수 있다.
