# FFmpeg

## Installation
```
git clone https://git.ffmpeg.org/ffmpeg.git ffmpeg
```

## Generic options
```shell
-i [input]
입력 파일을 지정한다.

-vcodec [codec], -acodec [codec] 또는 -c:v [codec], -c:a [codec]
비디오 코덱, 오디오 코덱을 지정한다. 사용할 수 있는 코덱은 ffmpeg -encoders 로 확인할 수 있다. copy로 지정하면 기존 스트림을 인코딩 하지 않고(direct stream) 복사한다.

-vf [filter], -af [filter]
비디오, 오디오에 필터를 적용한다. 리사이즈를 하거나 스피드를 바꾸거나 ass, srt 자막을 입히는 등의 처리를 할 수 있다. 자세한 것은 ffmpeg의 필터 문서를 참고하자. 참고로 자막을 입히는 건 폰트 때문에 윈도에서는 환경변수를 지정해 줘야 한다.

-b:v [bitrate], -b:a [bitrate]
비디오, 오디오의 비트레이트를 지정한다.

-crf [quality]
비트레이트 대신 화질 기준으로 인코딩할 때 쓰는 옵션. 0-51, 0은 무손실, 디폴트는 23

-y
파일을 덮어쓸 일이 있어도 물어보지 않는다.

-re
인코딩 속도를 1x(실시간)으로 제한한다. 로컬 파일을 ffserver로 스트리밍 시 실시간으로 feed를 전송하기 위해서 필요하다.

-f [container]
출력 포맷을 지정한다. 따로 적지않으면 파일명에 맞춰서 해준다.

-t [time]
지정된 시간 (초 단위)만큼 인코딩한다.

-ss [time]
지정된 시간 (초 단위)만큼 건너뛰고 인코딩한다. hh:mm:ss 방식으로도 표기가 가능하다.
```

## References
* https://www.ffmpeg.org/
