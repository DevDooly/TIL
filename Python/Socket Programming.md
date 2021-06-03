# Socket Programming

## Introduce
Python의 소켓 모듈 은 Berkeley 소켓 API에 대한 인터페이스를 제공합니다.

## Socket API List
* socket()
* bind()
* listen()
* accept()
* connect()
* connect_ex()
* send()
* recv()
* close()

## Echo Server & Client Example
echo-server.py
```python echo-server.py
#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
```
echo-client.py
```python echo-client.py
import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    data = s.recv(1024)

print('Received', repr(data))
```

## TCP Socket
socket.socket ()을 사용하여 소켓 객체를 만들고 소켓 유형을 socket.SOCK_STREAM으로 지정합니다.</br>
기본 프로토콜은 TCP (Transmission Control Protocol)입니다.

## References
* https://realpython.com/python-sockets/
* https://en.wikipedia.org/wiki/Berkeley_sockets
* 
