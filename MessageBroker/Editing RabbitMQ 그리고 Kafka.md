# Editing RabbitMQ 그리고 Kafka

컴퓨터의 기본적인 자료구조인 큐(queue)를 활용한 메시지 브로커 소프트웨어.

메시지를 생산하는 생산자(Producer)가 메시지를 큐에 저장해 두면, 메시지를 수신하는 소비자(Consumer)가 메시지를 가져와 처리하는 Publish/Subscribe 방식의 메시지 전달 브로커이다.

쉽게 설명해 요청을 큐에 저장해두고, 선입선출 방식으로 요청을 처리한다.


||RabbitMQ|Kafka|비고|
|------|---|---|---|
|성능(msg/sec)|20,000|100,000|RabbitMQ 도 충분히 빠르나 차이가 있다.|
|개발언어|Erlang|Scala(JVM)||
|고가용성|지원|지원||
|페더레이션 큐|지원|미지원||
|설계방식|소비자 중심|생산자 중심||
|메시지 손실 방지|미지원|파일로 보관</br>(Ack, Offset Commit)||


관리 UI
공식 지원
미지원 (오픈소스 사용)





## Tutorials
* https://www.rabbitmq.com/getstarted.html 
* https://kafka.apache.org/quickstart
