# Editing RabbitMQ handle big message

## RabbitMQ 로 큰 메시지 처리하기.

메시지큐 크기 제한 : 512Mib
```
%% Max message size is hard limited to 512 MiB.
%% If user configures a greater rabbit.max_message_size,
%% this value is used instead.
-define(MAX_MSG_SIZE, 536870912).
```
* 출처 : https://github.com/rabbitmq/rabbitmq-common/blob/master/include/rabbit.hrl#L255

### Sending Images from sender to recieverin rabbitmq Python with Pika Part 8
* https://www.youtube.com/watch?v=QkorTB0ldwE
