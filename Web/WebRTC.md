<code>WebRTC (Web Real-Time Communication)</code>는 웹 브라우저 간에 플러그인의 도움 없이 서로 통신할 수 있도록 설계된 API이다. </br>
<code>W3C</code>에서 제시된 초안이며, 음성 통화, 영상 통화, P2P 파일 공유 등으로 활용될 수 있다.

# 용어 #
## Stun Server, Turn Server ##
### STUN ( Session Traversal Utilities for NAT ) ###
공재적 주소(Public Address)를 발견하거나 Peer 간의 직접 연결을 막는 등의 라우터의 제한을 결정하는 프로토콜.</br>
클라이언트는 인터넷을 통해 클라이언트의 공개 주소와 라우터의 NAT 뒤에 있는 클라이언트가 접근 가능한지 STUN 서버에 요청을 보냅니다.</br>


### NAT ( Network Address Translation ) ###
단말에 공개 IP 주소를 할당하기 위해 사용된다.</br>
라우터는 공개 IP 주소를 갖고 있고 모든 단말들은 라우터에 연결되어 있으며, 비공개 IP 주소 ( Private IP Address ) 를 갖고있다.</br>
요청은 단말의 비공개 주소로부터 라우터의 <code>공개 주소</code>와 <code>유일한 포트</code>를 기반으로 <code>번역</code>된다.</br></br>
어떠한 라우터들은 네트워크에 연결할수 있는 제한을 갖고 있습니다.</br>
따라서 STUN서버에 의해 공개 IP주소를 발견한다고 해도 모두가 연결을 할수 있다는 것은 아닙니다. 이를 위해 TURN이 필요합니다.</br>

### TURN ( Traversal Using Relays around NAT ###
몇몇의 라우터들은 Symmetric NAT이라고 불리우는 제한을 위한 NAT을 채용하고 있습니다.</br>
이 말은 peer 들이 오직 이전에 연결한 적 있는 연결들만 허용한다는 것입니다.</br></br>
TURN 은 연결된 모든 정보를 그 서버에 전달하는 것으로 Symmetric NAT 제한을 위회하는것을 의미합니다.</br>

* https://ko.wikipedia.org/wiki/WebRTC
* https://medium.com/@hyun.sang/webrtc-webrtc%EB%9E%80-43df68cbe511
* https://usinuniverse.bitbucket.io/blog/webrtc.html

# UDP Port Range #
## 브라우저 / 운영체제 별 포트범위 설정 ## 
### Chrome ###
#### WebRtcUdpPortRange 란 ####
WebRTC가 사용하는 로컬 UDP 포트 범위 제한
<pre>
Supported on:
Google Chrome (Linux, Mac, Windows) since version 54
Google Chrome OS (Google Chrome OS) since version 54
Google Chrome (Android) since version 54
</pre>
**Description**</br>
정책이 설정된 경우 WebRTC가 사용하는 UDP 포트 범위는 지정한 포트 간격(엔드포인트 포함)으로 제한됩니다.

정책이 설정되지 않았거나 빈 문자열 또는 유효하지 않은 포트 범위로 설정된 경우 WebRTC는 사용 가능한 로컬 UDP 포트를 사용하도록 허용됩니다.

**Supported features**</br>
* Dynamic Policy Refresh: No
* Per Profile: Yes
**Data type**</br>
<pre>
String
Windows:REG_SZ
Android:choice
</pre>

#### Windows registry location: ####
<pre>
Software\Policies\Google\Chrome\WebRtcUdpPortRange
</pre>

#### Mac/Linux preference name: ####
<pre>
WebRtcUdpPortRange
</pre>
#### Android restriction name: ####
<pre>
WebRtcUdpPortRange
</pre>
**Example value**</br>
<pre>
10000-11999
</pre>
* https://cloud.google.com/docs/chrome-enterprise/policies/?policy#WebRtcUdpPortRange
