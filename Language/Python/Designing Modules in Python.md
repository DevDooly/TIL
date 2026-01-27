# Python 모듈 디자인

## 인터페이스 디자인
모듈의 특정 함수를 사용할때는 함수의 매개변수만 알고있으면 되기 때문에 디자인을 정확히 해야한다.
<pre>
# sms.py:
class SmsClient:
    def __init__(self, url, username, password):
        self.username = username
        self.password = password
    def send_sms(phone_number, message):
        # TODO - write code to send sms
        pass
</pre>
위 처럼 send_sms 를 사용할때는 phone_number, message 두 매개변수 외에는 알 필요가 없다.

**실제 사용 예시**  
<pre>
# In orders.py
from django.conf import settings
from sms import SmsClient
sms_client = SmsClient(settings.sms_url, settings.sms_username, settings.sms_password)
....
sms_client.send_sms(phone_number, message)
</pre>
하지만 위 방법대로 사용하면 두가지 문제가 있다.

1. orders.py 에서 SmsClient 객체가 어떻게 구성되는지 알 필요가 없다.
  이는 orders.py 가 사용되는 모든 소스에서 설정값을 입력해야함을 의미한다.
2. 나중에 생성자가 바뀐다면 SmsClient 가 사용되는 모든 소스를 수정해야 한다.

**해결방법**  
SmsClient 모듈에서 객체를 만드는 것.
<pre>
# In sms.py:
from django.conf import settings
class SmsClient:
    def __init__(self, url, username, password):
        self.username = username
        self.password = password
    def send_sms(phone_number, message):
        # TODO - write code to send sms
        pass
sms_client = SmsClient(settings.sms_url, settings.sms_username, settings.sms_password)
</pre>
<pre>
# orders.py
from sms import sms_client
...
# when you need to send an sms
sms_client.send_sms(phone_number, message)
</pre>

## 예외처리 ##
**예외처리예시 - Status Codes**
<pre>
def _validate_phone_number (self, phone_number) :
    if not phone_number:
        InvalidPhoneNumberError ( "Empty phone number")
    phone_number = phone_number.strip ()
    if (len (phone_number)> 10) :
        InvalidPhoneNumberError ( "Phone number too long")
    # TODO 더 많은 예외처리 추가
def _validate_message (self, message) :
    if not message:
        raise InvalidMessageError ("Empty message")
    if (len (message)> 140) :
        raise InvalidMessageError ( "Message too long")
def send_sms (self, phone_number, message) :
    self._validate_phone_number (phone_number)
    self._validate_message (message)
    access_token = self._get_access_token ()
    status_code, response = _make_http_request (access_token, phone_number, message)
    if (status_code == 400) :
        # 워터 텔이 입력이 잘못되었음을 알려줍니다.
        # 가능하다면 오류 메시지를 읽어야합니다.
        # 적절한 오류로 변환하십시오.
        # 그냥 일반적인 BadInputError를 발생시킵니다.
        raise BadInputError (response.error_message) 발생
     elif (status_code in (300, 301, 302, 401, 403)) :
         # 이 상태 코드는 무언가 잘못되었음을 나타냅니다.
         # 모듈의 로직과 함께. 다시 시도해도 도움이되지 않습니다.
         # 동일한 상태 코드를 계속 받게됩니다.
         # 3xx는 리디렉션이며 잘못된 URL을 나타냅니다.
         # 401, 403은 access_token이 잘못된 것과 관련이 있습니다.
         # 클라이언트가 재 시도하는 것을 원하지 않으므로 RuntimeError를 발생시킵니다.
         raise RuntimeError (response.error_message)
      elif (status_code> 500) :
         # Watertel의 문제
         # 이것은 우리가 통제 할 수 없는 일이며 아마도 재시도하면 도움이 될 것입니다.
         # SmsException을 발생시켜 이를 나타냅니다.
         raise SmsException (response.error_message)
</pre>

**예외처리예시 - Exceptions**
<pre>
def _make_http_request(access_token, phone_number, message):
    try:
        data = {"message": message, "phone": phone_number, "priority": self.priority}
        url = "%s?accessToken=%s" % (self.url, access_token)
        r = requests.post(url, json=data)
        return (r.status_code, r.json())
    except ConnectTimeout:
        raise SmsException("Connection timeout trying to send SMS")
</pre>
**더 자세한 내용은 출처를 참고하거나, 추후 내용을 추가하겠음..**  
## References 
* https://hashedin.com/blog/designing-modules-in-python-ebook/
