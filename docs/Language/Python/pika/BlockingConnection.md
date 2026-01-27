# BlockingConnection

BlockingConnection 모듈은 Pika의 핵심 드라이버인 AMQP 위에 차단 체계를 구현합니다.  
대부분의 비동기식 예상이 제거되지만 AMQP 프로토콜의 비동기식 RPC 특성에 충실하려고 시도하여 서버에서 보낸 RPC 명령을 지원합니다.

```python
classpika.adapters.blocking_connection.BlockingConnection(parameters=None, _impl_class=None)[source]
```
BlockingConnection은 예상 응답이 반환될 때까지 차단하는 메서드를 제공하는 Pika의 비동기 코어 위에 레이어를 만듭니다.  
RabbitMQ에서 응용 프로그램에 대한 Basic.Deliver 및 Basic.Return 호출의 비동기 특성으로 인해 `basic_consume`을 사용하여 RabbitMQ에서 메시지를 수신하거나 알림을 받고 싶은 경우 계속 전달 스타일의 비동기 메서드를 구현할 수 있습니다.  
basic_publish 사용 시 배달 실패.
