# Dockerfile

Docker는 Dockerfile에서 지침을 읽어 이미지를 자동으로 빌드 할 수 있습니다. 

Dockerfile은 사용자가 이미지를 어셈블하기 위해 명령 줄에서 호출 할 수있는 모든 명령이 포함 된 텍스트 문서입니다. 

Docker 빌드를 사용하면 여러 명령 줄 지침을 연속적으로 실행하는 자동화 된 빌드를 만들 수 있습니다.

## Usage
```shell
$ docker build .
```
build 는 cli 가 아닌, Docker 데몬에 의해 실행된다.

Docker 데몬은 Dockerfile 을 실행하기 전, Dockerfile 의 유효성 검사를 수행하고 구문이 잘못된 경우 오류를 반환한다.
```shell
$ docker build -t test/myapp .
 [internal] load build definition from Dockerfile                       0.1s
 => transferring dockerfile: 60B                                        0.0s
 [internal] load .dockerignore                                          0.1s
 => transferring context: 2B                                            0.0s
```

## Format
```Dockerfile
# Comment
INSTRUCTION arguments
```
명령어가 대소문자를 구분하지는 않지만, 구분하기 위해 대문자를 사용한다.

**Dockerfile은 FROM 명령어로 시작한다.**
```Dockerfile
FROM ImageName
# Comment
RUN echo 'we are running some # of cool things'
```

### FROM
```Dockerfile
FROM [--platform=<platform>] <image> [AS <name>]
```
Or
```Dockerfile
FROM [--platform=<platform>] <image>[:<tag>] [AS <name>]
```
Or
```Dockerfile
FROM [--platform=<platform>] <image>[@<digest>] [AS <name>]
```
