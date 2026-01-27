# AMQP (Advanced Message Queuing Protocol)

**AMQP**는 메시지 지향 미들웨어(Message Oriented Middleware)를 위한 개방형 표준 응용 계층 프로토콜입니다. 클라이언트와 메시지 브로커(미들웨어) 간의 통신을 정의합니다.

## 1. 주요 특징
*   **플랫폼 독립적:** 서로 다른 언어나 운영체제 간에도 메시지를 주고받을 수 있습니다.
*   **신뢰성:** 메시지 전달 보장(Ack), 트랜잭션 등을 지원하여 금융권 등 신뢰성이 중요한 시스템에서 많이 사용됩니다.
*   **표준화:** RabbitMQ, ActiveMQ 등 다양한 브로커들이 이 표준을 따릅니다.

## 2. 구성 요소 (AMQP 모델)
*   **Exchange:** 생산자(Publisher)가 보낸 메시지를 받아서 규칙(Binding)에 따라 큐(Queue)로 라우팅하는 우체국 역할을 합니다.
*   **Queue:** 메시지가 소비되기 전까지 보관되는 버퍼입니다.
*   **Binding:** Exchange와 Queue를 연결하는 규칙입니다.