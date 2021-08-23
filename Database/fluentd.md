# Fluentd

Fluentd 는 데이터 소스(HTTP, TCP, ... )를 통해 데이터를 받아올 수 있는 로그 수집기다.</br>

## Event
Fluentd 가 읽어들인 데이터는 tag, time, recore 로 구성된 이벤트로 처리된다.

* tag: 이벹르를 어디로 보낼지 결정하기 위한 구분값
* time: 이벤트가 발생한 시간
* record: 데이터 (Json)

## Fluent-Bit
Fluentd forwarder 의 경량화 버전

## Refereces
 - https://www.fluentd.org/architecture
 - https://jonnung.dev/system/2018/04/06/fluentd-log-collector-part1/
