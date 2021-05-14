# Logrotate

많은 수의 로그 파일을 생성하는 시스템을 쉽게 관리 할 수 있도록 설계되었습니다.  
로그 파일의 자동 회전, 압축, 제거 및 메일 링을 허용합니다.  

## 옵션 ##
<pre>
-d, --debug
    디버그 모드를 사용한다. -v 옵션을 의미합니다.
    디버그 모드에서는 로그 또는 logrotate 상태 파일이 변경되지 않습니다.

-f , --force
    logrotate 구성 파일에 새 항목을 추가한 후 또는 이전 로그 파일이 수동으로 제거 된 경우 새 파일이 생성되고 로깅이 올바르게 계속 될 때 유용합니다.

-m , --mail <command>
    로그를 메일링 할 때 사용할 명령을 logrotate 에게 알려줍니다.
    이 명령은 1) 메시지 제목 및 2) 수신자의 두 가지 인수를 허용해야합니다.
    그런 다음 명령은 표준 입력에서 메시지를 읽고 수신자에게 메일을 보내야합니다.
    기본 메일 명령은 /bin/mail -s 입니다.

-s, --state <statefile>
    지시 logrotate에 다른 상태 파일을 사용할 수 있습니다.
    이는 logrotate가 다양한 로그 파일 세트에 대해 다른 사용자로 실행되는 경우 유용합니다.
    기본 상태 파일은 /var/lib/logrotate.status 입니다.

--usage
    간단한 사용법 메시지를 인쇄합니다.

--? , --help
    - help 메시지를 출력합니다.

-v , --verbose
    상세 모드를 켭니다.
</pre>

## 설정 ##
* rotate 30(숫자)  : log파일 30개 이상 되면 삭제
* maxage 30(숫자) : 30일 이산된 로그 파일 삭제
* size : 지정한 용량이 되면 로그로테이트를 실행한다. 10k, 10M 이런식으로 지정한다.
* create : [권한 유저 그룹] 으로 rotation된 로그파일 생성
* notifempty : log 내용이 없으면 rotation 하지 않는다.
* ifempty : 로그파일이 비어있는 경우에도 로테이트한다.
* monthly : 월 단위로 로테이트 한다.
* daily : 월 단위로 로테이트 한다.
* weekly : 월 단위로 로테이트 한다.
* compress : rotate 된 로그 gzip 압축
* nocompress : 압축을 원치 않는다.
* mail admin@mail : 로테이트 설정에 의해 보관주기가 끝난 파일을 메일로 발송한다.
* mailfirst admin@mail : 로테이트시 신규파일 이전의 로그를 메일로 발송한다.
* nomail : 메일로 통보받지 않음.
* errors admin@mail : 로테이트 실행시 에러가 발생하면 이메일로 통보한다.
* prerotate-endscript : 사이의 명령어를 로그파일 처리전에 실행한다.
* postrotate-endscript : 사이의 명령어를 로그파일 처리후에 실행한다.
* extension : 로테이트 후 생성되는 파일의 확정자를 지정한다.
* copytruncate : 이옵션을 넣지 않으면 현재 사용중인 로그를 다른이름으로 move하고 새로운 파일을 생성한다.

## docker ##
docker container log 삭제하기.</br>
아래 명령어 순서대로 실행한다.</br>

1. <code> $ vi /etc/logrotate.d/docker-container </code>
<syntaxhighlight lang="YAML">
/var/lib/docker/containers/*/*.log {
  rotate 7
  daily
  compress
  missingok
  delaycompress
  copytruncate
}
</syntaxhighlight>

2. <code> $ logrotate -fv /etc/logrotate.d/docker-container </code>
