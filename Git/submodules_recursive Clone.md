# Options: Recursive

## Introduce
**Section 9.1: submodule 이 존재하는 git 저장소를 clone 하기**

submodule이 존재하는 저장소를 clone 할 때 초기화 후 업데이트 하는 과정이 필요합니다.

### Usage
<pre>
$ git clone --recursive https://github.com/username/repo.git
</pre>

위 명령어를 사용하면 submodule 들을 적절한 위치에 clone 한다. (submodule 의 submodule도 동일하게 진행)

**아래 명령어와 같은 의미를 지닌다.**
<pre>
$ git submodule update --init --recursive
</pre>

## References
* https://books.goalkicker.com/GitBook/
