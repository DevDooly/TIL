# HAProxy를 통한 Oracle DB 접속 지연 진단 가이드

HAProxy를 통해 Oracle DB에 접속할 때 직접 접속하는 것보다 속도 저하가 발생하는 경우, HAProxy 또는 관련 인프라에서 지연이 발생하고 있을 수 있습니다. 이 가이드는 HAProxy를 포함한 시스템 전반에서 지연의 원인을 체계적으로 진단하는 방법을 제공합니다.

---

## 1. HAProxy 통계 페이지 및 로그 확인 (1순위)

HAProxy는 자체적으로 상세한 통계 페이지와 로그를 제공하며, 이는 지연의 원인을 파악하는 데 가장 중요한 첫 번째 정보원입니다.

### 1.1. HAProxy Statistics Page 활용

HAProxy 통계 페이지는 실시간으로 HAProxy의 성능 지표를 모니터링할 수 있는 강력한 도구입니다.

**활성화 예시 (`haproxy.cfg`)**

```ini
listen stats
    bind *:8080                     # 통계 페이지 접속 포트 (예: http://your-haproxy-ip:8080/haproxy_stats)
    mode http                       # 통계 페이지는 HTTP 모드로 동작
    stats enable                    # 통계 페이지 활성화
    stats uri /haproxy_stats        # 통계 페이지 접속 URI
    stats realm HAPROXY\ Statistics # 인증 메시지 (팝업창에 표시)
    stats auth user:password        # 접속 사용자명 및 비밀번호 (보안을 위해 반드시 설정)
    stats refresh 5s                # 5초마다 자동 새로고침
```

**확인할 주요 지표:**

*   **`qcur` (Queue Current):** 현재 HAProxy 내부 큐에서 대기 중인 요청 수. 이 값이 지속적으로 높으면 HAProxy 자체가 병목이거나, 백엔드 DB가 HAProxy의 처리 속도를 따라가지 못함을 의미합니다.
*   **`c_con` (Connections Current):** 현재 HAProxy와 클라이언트 간의 활성 연결 수.
*   **`s_con` (Connections Current):** 현재 HAProxy와 서버(DB) 간의 활성 연결 수.
*   **`qtime` (Queue Time):** 요청이 HAProxy 큐에서 대기한 시간 (밀리초). 높으면 HAProxy가 요청을 백엔드로 보내지 못하고 있음을 나타냅니다.
*   **`c_time` (Connect Time):** HAProxy가 백엔드 서버에 연결하는 데 걸린 시간 (밀리초). 높으면 HAProxy -> DB 간 네트워크 문제 또는 DB 자체의 연결 처리 지연을 의심할 수 있습니다.
*   **`r_time` (Response Time):** HAProxy가 백엔드 서버로부터 첫 번째 응답 바이트를 받는 데 걸린 시간 (밀리초). DB 쿼리 처리 시간과 HAProxy -> DB 간 네트워크 지연을 포함합니다.
*   **`tt_time` (Total Session Time):** 클라이언트 요청부터 응답 완료까지 전체 세션 시간.
*   **`status` (Health Check Status):** 백엔드 DB의 헬스 체크 상태를 확인하여 DB가 정상적으로 응답하고 있는지 봅니다.
*   **`bin` (Bytes In) / `bout` (Bytes Out):** 트래픽 양을 확인하여 예상치 못한 트래픽 급증 여부를 확인합니다.

### 1.2. HAProxy 로그 확인

HAProxy 로그는 각 연결의 세부 정보를 제공하므로 지연이 발생한 특정 요청의 패턴을 파악하는 데 유용합니다.

**로그 설정 예시 (`haproxy.cfg`)**

```ini
global
    log /dev/log    local0 notice  # syslog로 로그를 보냄 (OS 설정 필요)
    # log global                   # syslog를 사용하는 경우
    # log 127.0.0.1:514 local0 info  # 원격 syslog 서버를 사용하는 경우

defaults
    mode tcp                       # Oracle DB는 TCP 모드로 설정
    log global
    # 타임아웃 설정 (아래 2.1. 참고)
    timeout connect 10s            # HAProxy가 백엔드에 연결 시도 시 타임아웃
    timeout client  60s            # 클라이언트가 HAProxy에 연결 유지 시 타임아웃
    timeout server  60s            # HAProxy가 백엔드로부터 응답 대기 시 타임아웃
    timeout queue   1m             # 큐 대기 타임아웃
```

**확인할 로그 내용:**

*   **`c_time`, `s_time`, `t_total` 필드:** 로그 라인에 포함된 이 필드들을 통해 특정 세션의 연결, 응답, 전체 처리 시간을 파악할 수 있습니다. (예시: `queue=0, connect=1, reuse=0, total=1`)
*   **오류 메시지:** `timeout`, `connection refused`, `connection reset` 등의 오류 메시지를 통해 어떤 단계에서 문제가 발생하는지 단서를 얻습니다.

---

## 2. HAProxy 설정 파일(`haproxy.cfg`) 검토

HAProxy 설정은 성능에 직접적인 영향을 미칩니다. 다음 설정들을 중심으로 검토하세요.

### 2.1. 핵심 타임아웃 설정

*   **`timeout connect <time>`:** HAProxy가 백엔드 서버에 TCP 연결을 설정하는 데 기다리는 최대 시간. 이 값이 너무 낮으면 백엔드 DB의 연결 부하가 높을 때 `Connection refused`가 발생할 수 있습니다.
*   **`timeout client <time>`:** 클라이언트와 HAProxy 간의 비활성(idle) 연결을 유지하는 최대 시간.
*   **`timeout server <time>`:** HAProxy와 백엔드 서버 간의 비활성(idle) 연결을 유지하는 최대 시간. DB 쿼리 특성(장시간 쿼리)을 고려하여 적절히 설정해야 합니다. 너무 짧으면 장시간 쿼리가 중간에 끊길 수 있습니다.
*   **`timeout queue <time>`:** 요청이 HAProxy 내부 큐에서 대기할 수 있는 최대 시간. 큐가 가득 찼을 때 이 시간이 지나면 요청은 드롭됩니다.

### 2.2. 모드 및 밸런싱

*   **`mode tcp`:** Oracle DB는 TCP 기반이므로 반드시 `mode tcp`로 설정되어 있어야 합니다. `mode http`로 설정되어 있다면 불필요한 오버헤드가 발생합니다.
*   **`balance` 알고리즘:** `leastconn`, `roundrobin` 등 여러 알고리즘이 있습니다. `leastconn`은 현재 연결 수가 가장 적은 서버로 요청을 보내 DB 부하 분산에 적합합니다. `roundrobin`은 연결 수와 관계없이 순환 방식으로 분산합니다.
*   **`option tcp-keepalive`:** 비활성 연결을 주기적으로 확인하여 연결을 유지하고, 다시 연결하는 오버헤드를 줄입니다. DB 연결에 유리합니다.

### 2.3. 연결 및 세션 관리

*   **`maxconn` (Global), `maxconn` (Frontend/Backend/Server):** HAProxy 전체 또는 특정 백엔드 서버에 대한 최대 동시 연결 수 제한. 이 제한에 도달하면 `qcur` 값이 증가하고 클라이언트는 연결 지연 또는 오류를 겪을 수 있습니다.
*   **`stick-table` / `stick on` (Session Persistence):** Oracle RAC (Real Application Clusters) 등 세션 지속성이 중요한 환경에서는 클라이언트 IP 또는 쿠키 기반의 세션 지속성 설정을 검토해야 합니다. 잘못 설정하면 매번 새로운 연결이 발생하거나 세션이 끊길 수 있습니다.
*   **SSL/TLS Offloading:** HAProxy가 SSL/TLS 암복호화를 처리하는 경우 (DB도 SSL/TLS를 사용하는 경우) CPU 부하가 증가하여 지연의 원인이 될 수 있습니다. HAProxy 서버의 CPU 사용률을 확인해야 합니다.

---

## 3. 네트워크 수준 진단

HAProxy와 DB 백엔드 간, 또는 클라이언트와 HAProxy 간의 네트워크 문제를 확인합니다.

*   **지연 측정 (`ping`, `traceroute`):**
    *   **클라이언트 -> HAProxy 서버:** 이 구간의 네트워크 지연 확인.
    *   **HAProxy 서버 -> DB 서버:** 이 구간의 네트워크 지연 확인.
    *   **직접 접속하는 클라이언트 -> DB 서버:** 비교를 위한 기준치.
    *   각 구간별 평균 왕복 시간(RTT)을 비교하여 어떤 구간에서 지연이 발생하는지 확인합니다.
*   **패킷 캡처 (`tcpdump`, Wireshark):**
    *   HAProxy 서버와 DB 서버 양쪽에서 `tcpdump`를 사용하여 패킷을 캡처합니다.
    *   특히 TCP 3-way handshake 시간, 데이터 전송 시간, 재전송(retransmissions) 발생 여부, TCP Window Size 관련 문제 등을 분석하여 정확한 네트워크 병목 지점을 찾을 수 있습니다.
    *   SSL/TLS가 적용된 경우, 암복호화 과정에서의 추가 오버헤드도 확인 대상입니다.
*   **방화벽 / 보안 그룹:**
    *   HAProxy와 DB 사이에 있는 방화벽이나 보안 그룹 규칙이 불필요한 지연을 유발하거나 특정 포트/프로토콜에 대해 트래픽 제한을 걸고 있지는 않은지 확인합니다.
*   **NIC (Network Interface Card) 상태:**
    *   HAProxy 서버 및 DB 서버의 네트워크 인터페이스 오류 (CRC 에러, Dropped packets 등)를 `ethtool -S <interface>` 명령 등으로 확인합니다.

---

## 4. HAProxy 서버의 시스템 리소스 확인

HAProxy가 실행되는 서버 자체의 리소스 부족이 지연을 유발할 수 있습니다.

*   **CPU 사용률:** `top`, `htop`, `sar` 명령으로 CPU 사용률을 확인합니다. HAProxy 프로세스가 CPU를 많이 사용한다면 암복호화 (SSL/TLS Offloading) 또는 복잡한 ACL 규칙 등이 원인일 수 있습니다.
*   **메모리 사용률:** 메모리 부족으로 스왑(Swap)이 발생하면 성능이 급격히 저하됩니다.
*   **디스크 I/O:** `iostat` 등으로 HAProxy 서버의 디스크 I/O를 확인합니다. HAProxy 자체는 디스크 I/O가 많지 않지만, 로그가 과도하게 쌓이거나 다른 프로세스가 디스크를 많이 사용하는 경우 영향을 줄 수 있습니다.
*   **파일 디스크립터 제한 (`ulimit -n`):** 동시 연결이 많을 때 파일 디스크립터 제한에 도달하면 새로운 연결을 받지 못하거나 오류가 발생할 수 있습니다.

---

## 5. Oracle DB 백엔드 상태 확인

HAProxy 통계와 네트워크 진단에서 특별한 문제가 발견되지 않는다면, Oracle DB 백엔드 자체의 지연일 가능성이 높습니다.

*   **DB 부하:**
    *   DB 서버의 CPU, 메모리, 디스크 I/O 사용률을 확인합니다.
    *   액티브 세션 수, 대기 이벤트 (Wait Events) 등 DB 성능 지표를 확인하여 DB가 정상적인 속도로 쿼리를 처리하고 있는지 봅니다.
*   **DB 커넥션 풀:**
    *   HAProxy를 통해 들어오는 연결을 DB가 어떻게 처리하고 있는지 확인합니다. DB 커넥션 풀이 너무 작거나 설정이 부적절하면 연결 요청이 대기하거나 거부될 수 있습니다.

---

## 6. 체계적인 진단 흐름

1.  **HAProxy 통계 페이지를 최우선으로 확인:** `qtime`, `c_time`, `r_time` 지표를 통해 지연이 HAProxy 내부 큐에서 발생하는지, 백엔드 연결 시 발생하는지, 아니면 백엔드 응답 자체에서 발생하는지 1차적으로 파악합니다.
2.  **HAProxy 로그 상세 분석:** 특정 지연 세션의 로그를 분석하여 정확한 타임아웃이나 오류 패턴을 찾아냅니다.
3.  **네트워크 진단:** `ping`, `traceroute`, `tcpdump`를 사용하여 HAProxy 서버와 DB 서버 간의 네트워크 지연 여부를 확인합니다.
4.  **HAProxy 설정 검토:** 통계와 로그에서 얻은 단서를 바탕으로 `haproxy.cfg`의 `timeout` 값, `maxconn`, 헬스 체크 설정 등을 조정합니다.
5.  **HAProxy 서버 리소스 모니터링:** HAProxy 서버 자체의 CPU, 메모리, 네트워크 트래픽을 모니터링하여 리소스 병목이 없는지 확인합니다.
6.  **Oracle DB 성능 확인:** 위 단계에서 문제가 발견되지 않으면 DB 자체의 성능 문제를 조사합니다.

이러한 단계들을 체계적으로 밟아가면 HAProxy를 통한 Oracle DB 접속 지연의 원인을 정확히 파악하고 해결책을 마련할 수 있을 것입니다.
