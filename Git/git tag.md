# Git Tag

특정 지점에 중요한 태그를 남겨 릴리즈 지점으로 표시한다

## 사용법

### 태그 조회

```bash
$ git tag
v1.0
v2.0
```

### 태그 붙이기

Git tag 는 Lightweight 태그와 Annotated 태그로 두 종류가 있다.

#### Annotated 태그

태그를 만든 사람의 이름, 이메일, 날짜와 메시지를 저장한다.

**사용방법**
```bash
$ git tag -a v1.0 -m "version 1.0"
$ git tag
v1.0
```

```-m``` 옵션으로 태그를 저장할 때 메시지를 함께 저장할 수 있다.
```git show``` ㅕㅇ령으로 정보를 확인할 수 있다.
```bash
$ git show v1.0
tav v1.0
Tagger: DevDooly <sunhongyi@gmail.com>
Date: Web Sep 1 15:09:07 2021 +0900

version v1.0

....
```

#### Lightweight 태그
파일에 커밋 체크섬을 저장한다.

**사용방법**
```bash
$ git tag v1.0-lw
$ git tag
v1.0
v1.0-lw
```
