# socketserver

socketserver 모듈은 네트워크 서버 작성 작업을 단순화합니다.

## Default Class

```python
class socketserver.TCPServer(server_address, RequestHandlerClass, bind_and_activate=True)
```
클라이언트와 서버 간에 연속적인 데이터 스트림을 제공하는 인터넷 TCP 프로토콜을 사용합니다.
bind_and_activate가 참이면, 생성자는 자동으로 server_bind()와 server_activate()를 호출하려고 시도합니다.
다른 매개 변수는 BaseServer 베이스 클래스로 전달됩니다.

```python
class socketserver.UDPServer(server_address, RequestHandlerClass, bind_and_activate=True)
```
순서가 잘못되거나 전송 중 손실될 수 있는 이산적 정보 패킷인 데이터 그램을 사용합니다. 매개 변수는 TCPServer와 같습니다.

```python
class socketserver.UnixStreamServer(server_address, RequestHandlerClass, bind_and_activate=True)
class socketserver.UnixDatagramServer(server_address, RequestHandlerClass, bind_and_activate=True)
```
TCP와 UDP 클래스와 비슷하지만, 유닉스 도메인 소켓을 사용하는 자주 사용되지 않는 클래스입니다; 유닉스 이외의 플랫폼에서는 사용할 수 없습니다. 매개 변수는 TCPServer와 같습니다.

이 네 가지 클래스는 동기적으로 (synchronously) 요청을 처리합니다

**위 요청을 시작하기 전에 각 요청을 완료해야 합니다.**

1. BaseRequestHandler 클래스를 서브 클래싱하고 handle() 메서드를 재정의하여 요청 처리기 클래스를 만들어야 합니다. (이 메서드는 들어오는 요청을 처리합니다.)
2. 서버 주소와 요청 처리기 클래스를 전달하여 서버 클래스 중 하나를 인스턴스 화해야 합니다. (with 문에서 서버를 사용하는 것이 좋습니다.)
3. 서버 객체의 handle_request()나 serve_forever() 메서드를 호출하여 하나 이상의 요청을 처리합니다.
4. (with 문을 사용하지 않았다면) server_close()를 호출하여 소켓을 닫습니다.

## References
* https://docs.python.org/ko/3/library/socketserver.html
