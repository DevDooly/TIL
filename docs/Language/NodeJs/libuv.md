---
title: Libuv 아키텍처 및 Node.js 이벤트 루프(Event Loop) 심층 분석
---

# ⚡ Libuv & Node.js 비동기 I/O 아키텍처

**libuv**는 Node.js의 핵심 비동기 I/O 엔진으로, 크로스 플랫폼(Linux, Windows, macOS) 비동기 알림 및 멀티스레드 작업을 추상화하는 고성능 C 라이브러리입니다.

Node.js 자체는 **단일 메인 스레드(Single-Threaded Event Loop)**로 동작하지만, libuv 덕분에 논블로킹(Non-blocking) I/O와 무거운 백그라운드 작업을 효율적으로 처리할 수 있습니다.

---

## 1. Libuv 아키텍처 구조

```mermaid
graph TD
    NodeApp[Node.js Javascript Engine / V8]
    NodeBindings[Node.js C++ Bindings]
    Libuv[Libuv Core]
    
    NodeApp --> NodeBindings
    NodeBindings --> Libuv
    
    subgraph Libuv Engine
        EventLoop[Event Loop (Single Thread)]
        ThreadPool[Thread Pool (Default: 4 Threads)]
    end
    
    Libuv --> EventLoop
    Libuv --> ThreadPool
    
    EventLoop -->|Non-blocking OS I/O| OSKernel[OS Kernel: epoll / kqueue / IOCP]
    ThreadPool -->|Blocking Operations| FS_DNS[File System, DNS, Crypto, Compression]
```

* **논블로킹 네트워크 I/O**: OS 커널 레벨의 이벤트 통지 메커니즘(`epoll` on Linux, `kqueue` on macOS, `IOCP` on Windows)을 직접 활용하여 스레드 낭비 없이 수만 개의 동시 소켓을 처리합니다.
* **스레드 풀(Thread Pool)**: OS 커널에서 완전한 논블로킹을 지원하지 않거나 동기 블로킹 방식으로만 작동하는 작업(파일 I/O, DNS 조회, 암호화 crypto, 압축 zlib)은 내부 스레드 풀(`UV_THREADPOOL_SIZE`, 기본 4개)로 위임하여 처리합니다.

---

## 2. Node.js 이벤트 루프의 6개 Phase

이벤트 루프는 매 틱(Tick)마다 정의된 6개의 단계를 순서대로 순회하며 큐에 쌓인 콜백을 실행합니다:

```mermaid
flowchart TD
    Start((Start / Next Tick)) --> Timers[1. Timers Phase: setTimeout, setInterval]
    Timers --> Pending[2. Pending Callbacks: OS 시스템 작업 콜백]
    Pending --> Idle[3. Idle, Prepare: 내부용]
    Idle --> Poll[4. Poll Phase: I/O 이벤트 대기 및 실행]
    Poll --> Check[5. Check Phase: setImmediate]
    Check --> Close[6. Close Callbacks: socket.on('close')]
    Close --> NextTick{큐에 남은 작업?}
    NextTick -->|Yes| Timers
    NextTick -->|No| Exit((Process Exit))
```

### 각 단계별 역할

| Phase | 설명 | 대상 작업 |
| :--- | :--- | :--- |
| **1. Timers** | 타이머 만료 시간이 도래한 콜백을 실행합니다. | `setTimeout()`, `setInterval()` |
| **2. Pending Callbacks** | 이전 루프 반복에서 지연된 I/O 콜백(예: 특정 TCP 오류 등)을 실행합니다. | 시스템 레벨 I/O 에러/알림 |
| **3. Idle, Prepare** | Node.js 내부적인 관리를 위해서만 사용됩니다. | libuv 내부 동작 |
| **4. Poll** | 새로운 I/O 이벤트를 조회하고 블로킹 대기(timeout 계산)하며, I/O 관련 콜백을 실행합니다. | 파일 읽기 완료, 수신 데이터 처리 등 |
| **5. Check** | Poll 단계가 완료된 직후 실행되는 콜백을 처리합니다. | `setImmediate()` |
| **6. Close Callbacks** | 연결이 갑자기 닫히거나 리소스가 해제될 때의 콜백을 실행합니다. | `socket.on('close', ...)` |

---

## 3. 마이크로태스크(Microtask) 우선순위

이벤트 루프의 각 Phase 사이마다 **Microtask Queue**가 항상 최우선으로 비워집니다.

1. **`process.nextTick()` 큐**: 다른 모든 비동기 큐보다 가장 먼저 실행됩니다 (최고 우선순위).
2. **`Promise` 큐 (`Promise.resolve()`, `async/await`)**: `nextTick` 바로 다음에 실행됩니다.

```javascript
setTimeout(() => console.log('1. setTimeout (Timers)'), 0);
setImmediate(() => console.log('2. setImmediate (Check)'));
process.nextTick(() => console.log('3. process.nextTick (Microtask)'));
Promise.resolve().then(() => console.log('4. Promise (Microtask)'));

// 출력 순서:
// 3. process.nextTick (Microtask)
// 4. Promise (Microtask)
// 1. setTimeout (Timers)
// 2. setImmediate (Check)
```

---

## 4. 실무 성능 최적화 팁

1. **스레드 풀 크기 튜닝 (`UV_THREADPOOL_SIZE`)**:
   대용량 파일 읽기/쓰기나 암호화 연산(`crypto.pbkdf2`, `bcrypt`)이 많은 서버인 경우 환경 변수로 스레드 풀 크기를 확장(기본 4 → CPU 코어 수 고려 16~32)해야 이벤트 루프 병목을 막을 수 있습니다:
   ```bash
   UV_THREADPOOL_SIZE=16 node server.js
   ```
2. **메인 스레드 블로킹 금지 (Don't Block the Event Loop)**:
   정규표현식 ReDoS 공격, 대용량 동기 JSON 파싱, 동기 파일 I/O(`fs.readFileSync`)는 전체 이벤트 루프를 멈추게 하므로 반드시 비동기 또는 Worker Threads를 활용해야 합니다.

---

## 5. References
* [libuv Design Overview](http://docs.libuv.org/en/v1.x/design.html)
* [Node.js Event Loop, Timers, and process.nextTick() Guide](https://nodejs.org/en/docs/guides/event-loop-timers-and-nexttick/)
