# Git 원격 주소 변경 (HTTPS 인증 문제 해결)

서버에서 `git push`를 할 때마다 사용자 이름(Username)과 비밀번호(Password)를 요구하는 경우, 원격 저장소 연결 방식이 **HTTPS**로 설정되어 있을 확률이 높다. 이를 **SSH** 방식으로 변경하면 매번 인증 정보를 입력하지 않아도 된다.

## 1. 차이점 이해 (HTTPS vs SSH)

### HTTPS (`https://github.com/User/Repo.git`)
- 일반적인 웹 주소를 사용한다.
- `push` 할 때마다 인증이 필요하다.
- GitHub 정책 변경으로 비밀번호 대신 **Personal Access Token (PAT)**을 입력해야 한다.
- `credential helper`를 설정하지 않으면 매번 입력해야 해서 번거롭다.

### SSH (`git@github.com:User/Repo.git`)
- 서버에 생성된 SSH Key(공개키/비공개키)를 사용하여 인증한다.
- 한 번 설정해두면 비밀번호 입력 없이 자동으로 인증된다.
- **기존에 잘 작동하던 프로젝트는 이 방식을 사용 중일 가능성이 크다.**

## 2. 해결 방법 (Remote URL 변경)

현재 연결된 주소를 확인하고, HTTPS 주소를 SSH 주소로 변경한다.

### 2-1. 현재 설정 확인
```bash
git remote -v

# 출력 예시 (HTTPS로 설정된 경우)
# origin  [https://github.com/DevDooly/TIL.git](https://github.com/DevDooly/TIL.git) (fetch)
# origin  [https://github.com/DevDooly/TIL.git](https://github.com/DevDooly/TIL.git) (push)
```

### 2-2. 주소 변경 (HTTPS -> SSH)

GitHub 저장소 페이지에서 Code 버튼을 누르고 SSH 탭의 주소를 복사하거나, 아래 명령어를 입력한다.

```bash
# git remote set-url origin [SSH 주소]
git remote set-url origin git@github.com:DevDooly/TIL.git
```

### 2-3. 변경 확인

```bash
git remote -v

# 출력 예시 (성공)
# origin  git@github.com:DevDooly/TIL.git (fetch)
# origin  git@github.com:DevDooly/TIL.git (push)
```

이제 git push를 실행하면 계정 정보를 묻지 않고 정상적으로 수행된다.

## References
* [How to maintain a TIL repository](https://github.com/jbranchaud/til)
* [GitHub Docs - Switching remote URLs from HTTPS to SSH](https://docs.github.com/en/get-started/getting-started-with-git/managing-remote-repositories%23switching-remote-urls-from-https-to-ssh&hl=ko-KR)
