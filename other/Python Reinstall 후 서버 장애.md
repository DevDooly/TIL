### 잘못된 선택...

테스트를 한답시고 python 을 제거한 뒤 재설치 함.


#### 사용한 명령어
```
sudo apt remove python3
sudo apt install python3
sudo apt update
sudo reboot
```

이후...

위키가 접속되지 않았다...

로컬에서 접속을 해보니 특정 메시지와 함께 로그인 실패함

**세션을 접속할 수 없습니다.**

Ctrl + Alt + f1 을 사용하여 터미널 환경으로 접속하고 아래 명령어를 수행 함.

```
sudo apt-get update && sudo apt-get install ubuntu-desktop
sudo apt-get install --reinstall ubuntu-desktop
sudo reboot
```

정상적으로 진행되지 않았다.

**문제 :: 인터넷이 연결되지 않음**

현재 해결이 불가하여 다른 방법을 찾고있다...
