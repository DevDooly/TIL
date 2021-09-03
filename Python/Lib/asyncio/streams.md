# Stream
* Source Code: https://github.com/python/cpython/tree/3.9/Lib/asyncio/streams.py

스트림은 네트워크 연결로 작업하기 위해, async/await에서 사용할 수 있는 고수준 프리미티브<sup>[1](#primitive)</sup> 입니다. 

스트림은 콜백이나 저수준 프로토콜과 트랜스포트를 사용하지 않고 데이터를 송수신할 수 있게 합니다.

## 예시
**TCP 클라이언트**
```python
import asyncio

async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888)

    print(f'Send: {message!r}')
    writer.write(message.encode())
    await writer.drain()

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()
    await writer.wait_closed()

asyncio.run(tcp_echo_client('Hello World!'))
```

---

<a name="primitive">[1] Primitive</a> : 
컴퓨터 프로그래밍 언어에서 프리미티브는 이용가능한 가장 단순한 요소들이다.<br>
프리미티브는 주어진 기계(machine)의 프로그래머에게 이용가능한 가장 작은 처리(processing)의 단위이거나 언어에서 표현의 원자 요소가 될 수 있다.
