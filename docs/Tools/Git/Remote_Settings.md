# Git Remote Settings (원격 저장소 관리)

Git 원격 저장소(Remote Repository)를 연결하고 관리하는 방법과 인증 방식(HTTPS vs SSH)을 변경하는 방법을 다룬다.

## 1. 기본 명령어

### 원격 저장소 확인
현재 연결된 원격 저장소의 목록과 URL을 확인한다.
```bash
git remote -v
```

### 원격 저장소 추가
새로운 원격 저장소를 `origin` 등의 이름으로 추가한다.
```bash
# git remote add [이름] [URL]
git remote add origin https://github.com/user/repo.git
```

### 원격 저장소 삭제
연결된 원격 저장소를 목록에서 제거한다.
```bash
git remote remove origin
```

---

## 2. HTTPS vs SSH 인증 방식 변경

서버에서 `git push`를 할 때마다 사용자 이름과 비밀번호(또는 Token)를 요구하는 경우, 원격 저장소 연결 방식이 **HTTPS**로 설정되어 있을 확률이 높다. 이를 **SSH** 방식으로 변경하면 인증 절차를 자동화할 수 있다.

### 차이점
- **HTTPS (`https://...`)**: 일반적인 웹 주소 사용. Push 시마다 인증 필요(Credential Helper 미사용 시).
- **SSH (`git@...`)**: SSH Key 쌍을 이용해 인증. 설정 후에는 비밀번호 입력 없이 사용 가능.

### 변경 방법 (HTTPS -> SSH)

1. **현재 설정 확인**
   ```bash
   git remote -v
   # origin  https://github.com/DevDooly/TIL.git (fetch)
   ```

2. **URL 변경**
   GitHub 저장소 페이지에서 SSH 주소를 복사한 후 아래 명령어를 실행한다.
   ```bash
   # git remote set-url [이름] [새로운 URL]
   git remote set-url origin git@github.com:DevDooly/TIL.git
   ```

3. **변경 확인**
   ```bash
   git remote -v
   # origin  git@github.com:DevDooly/TIL.git (fetch)
   ```

이제 `git push` 시 SSH 키를 통해 자동으로 인증된다.

## References
* [GitHub Docs - Managing remote repositories](https://docs.github.com/en/get-started/getting-started-with-git/managing-remote-repositories)