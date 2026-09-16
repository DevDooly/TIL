# Kafka 메시지 크기 제한: Producer·Topic·Consumer 구분

Kafka에서 큰 메시지가 거절되면 producer 설정만 바꿔서는 해결되지 않을 수 있다. Producer, topic, consumer가 제한하는 대상이 서로 다르기 때문이다. 아래는 Kafka 3.9 Java client와 broker 설정을 기준으로 설명한다.

## 설정 이름과 적용 범위

| 위치 | 설정 | 범위 |
| :--- | :--- | :--- |
| Producer | `max.request.size` | producer 요청 제한. 압축 전 record batch 크기에도 실질적인 상한 |
| Broker | `message.max.bytes` | 수용할 record batch 크기의 기본값. 압축 사용 시 압축 후 기준 |
| Topic | `max.message.bytes` | 해당 토픽의 record batch 제한 override |
| Consumer | `max.partition.fetch.bytes` | 파티션별 fetch 응답 예산 |
| Consumer | `fetch.max.bytes` | fetch 응답 전체 예산 |
| Broker 복제 | `replica.fetch.max.bytes` | 파티션별 replica fetch 예산 |
| Broker 복제 | `replica.fetch.response.max.bytes` | replica fetch 응답 전체 예산 |

메시지 본문 크기와 직렬화한 레코드·배치·요청 크기를 구분해서 봐야 한다. Consumer의 전체 fetch 예산은 `fetch.max.bytes`이며, 토픽의 `max.message.bytes`와 브로커의 `message.max.bytes`는 이름이 비슷해 혼동하기 쉽다. [Producer 설정](https://kafka.apache.org/39/configuration/producer-configs/), [Consumer 설정](https://kafka.apache.org/39/configuration/consumer-configs/), [Broker 설정](https://kafka.apache.org/39/configuration/broker-configs/)

## Fetch 크기는 절대적인 차단선이 아니다

Kafka 3.9의 consumer/replica fetch에는 **첫 번째 비어 있지 않은 파티션의 첫 배치가 한도를 넘어도 반환하는 예외**가 있다. 큰 배치 하나 때문에 처리가 계속 멈추는 것을 막기 위한 동작이다. 그래서 replica fetch 한도가 1 MiB이고 배치가 2 MiB라는 이유만으로 복제가 반드시 실패하지는 않는다.

이 예외와 동시에 진행되는 여러 fetch를 고려하면 실제 메모리 사용량은 설정값보다 커질 수 있다. 프로세스의 메모리와 네트워크 여유도 함께 확인해야 한다. [Consumer 설정](https://kafka.apache.org/39/configuration/consumer-configs/), [Replica fetch 설정](https://kafka.apache.org/39/configuration/broker-configs/#replica.fetch.max.bytes)

## 2 MiB payload 실험용 구성

아래의 3 MiB는 직렬화·키·헤더를 위한 여유를 둔 **실험 시작값**이다. 실제 최대 레코드와 배치 크기를 측정해 정한다. 압축률이 낮은 입력도 포함한다.

Producer의 기존 설정에 추가한다.

```properties
max.request.size=3145728
```

Consumer의 기존 설정에 추가한다.

```properties
max.partition.fetch.bytes=3145728
fetch.max.bytes=52428800
```

토픽 설정을 확인한 후 필요한 토픽에만 변경한다. 다음은 로컬 테스트 브로커용 Bash 예제다. 운영에서는 주소·인증 설정과 기존 override 값을 먼저 기록한다.

```bash
kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type topics --entity-name large-events --describe

kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type topics --entity-name large-events \
  --alter --add-config max.message.bytes=3145728

kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type topics --entity-name large-events --describe
```

## 동적 변경과 검증

Kafka 3.9에서 `message.max.bytes`는 `cluster-wide` 동적 설정이어서 토픽 override 외에도 재시작 없이 바꿀 수 있는 방법이 있다. 반면 `replica.fetch.max.bytes`는 `read-only` 설정이다. 실제 적용 방식은 사용하는 Kafka 버전과 배포 도구에서 확인한다. [Broker 설정과 Update Mode](https://kafka.apache.org/39/configuration/broker-configs/)

1. 한도 직전·직후 payload를 보내 성공/실패의 경계를 확인한다.
2. 수신 내용의 길이와 checksum을 검증한다.
3. ISR, under-replicated partitions, lag, broker/client 메모리와 오류를 관찰한다.
4. producer 재시도와 consumer 재시작도 포함한다.
5. 되돌릴 때는 원래 override로 복원한다. override가 원래 없었다면 삭제해 상속값으로 되돌린다.

큰 바이너리를 지속적으로 보낸다면 객체 저장소에 본문을 두고 Kafka에 참조·크기·checksum을 싣는 설계도 비교한다. 이 경우 객체와 이벤트의 수명·재처리·접근 제어가 추가 과제가 된다.
