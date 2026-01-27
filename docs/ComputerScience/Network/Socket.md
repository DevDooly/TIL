# Socket (소켓)

**네트워크 소켓(Network Socket)**은 컴퓨터 네트워크를 경유하는 프로세스 간 통신의 종착점(Endpoint)입니다. 프로그램이 네트워크를 통해 데이터를 주고받기 위해서는 소켓을 생성하고 이를 통해 데이터를 입출력해야 합니다.

## 1. 소켓의 정의
*   오늘날 대부분의 통신은 인터넷 프로토콜(IP)을 기반으로 하므로 보통 **인터넷 소켓**을 의미합니다.
*   소켓은 IP 주소와 포트 번호의 조합으로 식별됩니다.

## 2. 소켓의 구성 요소 (5-Tuple)
네트워크 상에서 특정 통신 세션을 유니크하게 식별하기 위해 다음 5가지 요소가 사용됩니다.
1.  **Protocol**: (TCP, UDP, Raw IP)
2.  **Local IP Address**: 내 컴퓨터의 주소
3.  **Local Port**: 내 컴퓨터의 프로세스 포트
4.  **Remote IP Address**: 상대방 컴퓨터의 주소
5.  **Remote Port**: 상대방 컴퓨터의 프로세스 포트

## 3. 소켓의 종류

### TCP 소켓 (Stream Sockets)
*   **연결 지향 (Connection-oriented):** 데이터를 주고받기 전에 연결을 설정합니다.
*   **신뢰성 보장:** 데이터가 순서대로, 유실 없이 전달됨을 보장합니다.
*   **용도:** 웹 브라우징(HTTP), 파일 전송(FTP) 등.

### UDP 소켓 (Datagram Sockets)
*   **비연결 지향 (Connectionless):** 연결 설정 없이 데이터를 바로 보냅니다.
*   **속도 중심:** 신뢰성보다는 빠른 전송을 목적으로 합니다.
*   **용도:** 스트리밍, 온라인 게임, DNS 등.

## 4. 소켓 통신 흐름 (TCP 기준)

1.  **Server**: `socket()` 생성 -> `bind()` 주소 할당 -> `listen()` 대기 -> `accept()` 연결 승인
2.  **Client**: `socket()` 생성 -> `connect()` 연결 요청
3.  **Data Transfer**: `send()`, `recv()` (또는 `read()`, `write()`)를 통해 데이터 교환
4.  **Close**: `close()` 통신 종료

## 참고
*   [Wikipedia - Network Socket](https://ko.wikipedia.org/wiki/%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC_%EC%86%8C%EC%BC%93)
*   [RFC 147](https://datatracker.ietf.org/doc/html/rfc147)