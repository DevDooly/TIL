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

**더 자세한 내용은 출처를 참고하거나, 추후 내용을 추가하겠음..**  
## References 
* https://hashedin.com/blog/designing-modules-in-python-ebook/
