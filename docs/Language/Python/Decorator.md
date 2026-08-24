---
title: Python Decorator (데코레이터) 완벽 가이드
---

# 🐍 Python Decorator (데코레이터)

**데코레이터(Decorator)**는 기존 함수의 코드를 직접 수정하지 않고, **함수의 동작을 확장하거나 변경(횡단 관심사 분리)**할 수 있도록 지원하는 파이썬의 강력한 문법 기능입니다.

파이썬의 함수가 **일급 객체(First-Class Citizen)**이자 **클로저(Closure)**를 생성할 수 있다는 특성을 기반으로 작동합니다.

---

## 1. 데코레이터의 동작 원리

데코레이터 `@decorator_func`는 본질적으로 아래 코드의 문법적 설탕(Syntactic Sugar)입니다:

```python
target_function = decorator_func(target_function)
```

### 기본 구현 패턴
```python
import functools
import time

def timing_decorator(func):
    """함수의 실행 시간을 측정하는 데코레이터"""
    @functools.wraps(func)  # 원본 함수의 __name__, __doc__ 등 메타데이터 보존
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"⏱️ [{func.__name__}] 실행 시간: {end_time - start_time:.6f}초")
        return result
    return wrapper

@timing_decorator
def calculate_heavy_work(n: int) -> int:
    """1부터 n까지의 합을 계산"""
    return sum(i * i for i in range(n))

# 사용
result = calculate_heavy_work(1_000_000)
```

> [!NOTE]
> `@functools.wraps(func)`를 사용하지 않으면 데코레이팅된 함수의 이름(`__name__`)과 독스트링(`__doc__`)이 `wrapper`로 덮어씌워져 디버깅 및 문서화 도구에서 문제가 발생합니다.

---

## 2. 매개변수를 받는 데코레이터 (Decorator with Arguments)

데코레이터 자체에 설정값이나 파라미터를 넘겨주려면 **3중 중첩 함수(클로저 팩토리)** 구조를 사용합니다.

```python
import functools
import time

def retry(max_retries: int = 3, delay: float = 1.0):
    """실패 시 지정된 횟수만큼 재시도하는 데코레이터"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"⚠️ [{func.__name__}] 실패 ({attempt}/{max_retries}): {e}")
                    if attempt < max_retries:
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

@retry(max_retries=3, delay=0.5)
def unstable_network_call():
    import random
    if random.random() < 0.7:
        raise ConnectionError("네트워크 연결 실패")
    return "성공 데이터"
```

---

## 3. 클래스 기반 데코레이터 (Class-based Decorator)

상태(State)를 유지해야 하거나 복잡한 로직이 필요할 때 `__call__` 매직 메서드를 구현한 클래스로 데코레이터를 정의할 수 있습니다.

```python
import functools

class CallCounter:
    """함수의 호출 횟수를 기록하는 클래스 데코레이터"""
    def __init__(self, func):
        self.func = func
        self.count = 0
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"📊 [{self.func.__name__}] 누적 호출 횟수: {self.count}")
        return self.func(*args, **kwargs)

@CallCounter
def process_task(task_name: str):
    return f"완료: {task_name}"

process_task("Task 1")
process_task("Task 2")
```

---

## 4. 실무 활용 패턴 (Cross-Cutting Concerns)

1. **로깅 및 추적 (Logging & Tracing)**: 함수 진입/퇴출 로그 및 파라미터 기록
2. **성능 모니터링 & 프로파일링 (Profiling)**: 실행 소요 시간 계측 및 APM 전송
3. **인증 및 권한 인가 (Authentication & Authorization)**: 웹 프레임워크(FastAPI, Flask)의 세션/JWT 토큰 검증
4. **캐싱 (Memoization)**: `functools.lru_cache` 또는 Redis 캐싱 데코레이터
5. **트랜잭션 관리 (Transaction Management)**: DB 세션 자동 커밋/롤백 처리

---

## 5. References
* [Python Documentation - Decorators](https://docs.python.org/3/glossary.html#term-decorator)
* [PEP 318 – Decorators for Functions and Methods](https://peps.python.org/pep-0318/)
