# Pipeline

데이터 처리 단계의 출력이 다음 단계의 입력으로 이어지는 형태로 연결된 구조를 가리킨다. 이렇게 연결된 데이터 처리 단계는 한 여러 단계가 서로 동시에, 또는 병렬적으로 수행될 수 있어 효율성의 향상을 꾀할 수 있다. 각 단계 사이의 입출력을 중계하기 위해 버퍼가 사용될 수 있다.

대표적인 파이프라인 구조는 다음과 같은 것들이 있다.

* 명령어 파이프라인: 같은 CPU 회로 안에서 여러 명령어들이 단계적으로 수행되는 것을 가리킨다. 각 명령어는 다시 페치, 디코딩, 연산 등의 세부 주기로 나뉘어 각 파이프라인 단계에 의해 수행된다.
* 그래픽스 파이프라인: 대부분의 그래픽 카드는 그래픽 처리 과정을 3차원 사영, 윈도 클리핑, 셰이딩, 렌더링 등으로 나누어 각각의 하부 모듈에서 병렬적으로 수행한다.
* 소프트웨어 파이프라인: 한 소프트웨어의 출력이 자동으로 다른 소프트웨어의 입력으로 연결될 경우 이를 소프트웨어 파이프라인이라고 한다. 유닉스 계열 운영체제에서 사용되는 파이프가 대표적이다.

개발에 있어서는 주로 소프트웨어 파이프라인을 얘기한다.

리눅스에서는 xargs 를 사용하여 실행한 명령어의 결과를 다음 명령어의 입력값으로 사용하기도 한다.

example
```
$ ls *.txt | xargs rm
$ find .mtime +30 | xargs mv -i {} {}.bak
```

### References
* https://ko.wikipedia.org/wiki/%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8_(%EC%BB%B4%ED%93%A8%ED%8C%85)
* https://ko.wikipedia.org/wiki/Xargs
