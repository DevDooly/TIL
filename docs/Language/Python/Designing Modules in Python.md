# Designing Modules in Python (모듈 설계)

좋은 Python 모듈을 설계하기 위한 인터페이스 정의 및 예외 처리 패턴을 정리합니다.

## 1. 인터페이스 디자인 (Interface Design)
사용자가 모듈 내부의 복잡한 구현 내용을 알 필요 없이, **최소한의 정보만으로 기능을 사용할 수 있도록** 추상화해야 합니다.

### Bad Case
사용자가 객체 생성에 필요한 모든 의존성을 직접 주입해야 하는 경우:
```python
# orders.py (사용자 코드)
from django.conf import settings
from sms import SmsClient

# 사용자가 settings에서 url, id, pw를 다 꺼내와야 함 (불편, 결합도 증가)
sms_client = SmsClient(settings.sms_url, settings.sms_username, settings.sms_password)
sms_client.send_sms(phone_number, message)
```

### Good Case
모듈 내부에서 설정을 처리하고, 미리 생성된 객체(Instance)를 노출하는 경우:
```python
# sms.py (모듈 코드)
from django.conf import settings

class SmsClient:
    def __init__(self, url, username, password):
        ...

# 모듈 로드 시점에 미리 생성
default_client = SmsClient(settings.sms_url, settings.sms_username, settings.sms_password)
```

```python
# orders.py (사용자 코드)
from sms import default_client

# 사용자는 send_sms만 호출하면 됨
default_client.send_sms(phone_number, message)
```

## 2. 예외 처리 (Error Handling)
적절한 커스텀 예외를 정의하고, 내부 구현에서 발생한 저수준 예외(HTTP Error 등)를 **의미 있는 고수준 예외**로 변환하여 던져야 합니다.

### 예시 패턴
```python
class SmsException(Exception):
    """SMS 모듈의 기본 예외"""
    pass

class BadInputError(SmsException):
    """입력값이 잘못됨"""
    pass

def send_sms(self, phone_number, message):
    try:
        response = requests.post(...)
        
        if response.status_code == 400:
            raise BadInputError("Invalid phone number")
        elif response.status_code >= 500:
            raise SmsException("Server error")
            
    except requests.ConnectTimeout:
        # requests 라이브러리의 예외를 모듈 전용 예외로 감싸서 던짐
        raise SmsException("Connection timeout")
```

## 참고
* [Designing Modules in Python (HashedIn)](https://hashedin.com/blog/designing-modules-in-python-ebook/)