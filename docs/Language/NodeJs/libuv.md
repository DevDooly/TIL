# Libuv

**libuv**는 Node.js의 이벤트 루프(Event Loop)와 비동기 I/O를 담당하는 멀티 플랫폼 C 라이브러리입니다.

## 1. 역할
Node.js는 싱글 스레드 기반이지만, 비동기 작업을 처리할 수 있는 이유는 바로 libuv 덕분입니다.
*   **이벤트 루프 관리:** `setTimeout`, `process.nextTick` 등의 스케줄링을 담당합니다.
*   **비동기 I/O:** 파일 시스템, DNS, 네트워크 소켓 등의 작업을 OS 커널(epoll, kqueue, IOCP)에 위임하거나, 스레드 풀(Thread Pool)을 이용하여 백그라운드에서 처리합니다.

## 2. 특징
*   **Full-featured event loop:** 고성능 이벤트 루프 제공
*   **Cross-platform:** Windows(IOCP), Linux(epoll), macOS(kqueue) 등 다양한 OS의 비동기 알림 메커니즘을 추상화하여 동일한 API로 제공합니다.

## 참고
*   [libuv 공식 문서](http://docs.libuv.org/)