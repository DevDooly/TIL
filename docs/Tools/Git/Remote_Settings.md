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

이제 `git push` 시 SSH 키를 통해 자동으로 인증된다. (단, 로컬에 생성된 SSH Public Key가 GitHub 계정에 등록되어 있어야 한다.)

---

## 3. 인증 자동화 상세 방법 (Seamless Push)

매번 비밀번호(Token)를 입력하지 않고 편리하게 Push하기 위한 두 가지 핵심 방법을 정리한다.

### 3.1 SSH 인증 설정 (가장 추천)
원격 저장소 URL이 `git@github.com:...` 형식일 때 사용한다.

1. **SSH 키 생성** (이미 있다면 건너뜀):
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   # 엔터를 계속 눌러 기본 경로에 저장
   ```

2. **Public Key 복사**:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

3. **GitHub 등록**:
   - GitHub 설정(Settings) -> **SSH and GPG keys** -> **New SSH key** 클릭.
   - 복사한 내용을 붙여넣고 저장.

### 3.2 HTTPS 방식에서 Credential Helper 사용
이미 `https://...` URL을 사용 중이고 형식을 바꾸고 싶지 않을 때 사용한다.

* **인증 정보 메모리에 임시 저장** (기본 15분):
  ```bash
  git config --global credential.helper cache
  ```

* **인증 정보 파일에 영구 저장** (보안상 주의):
  ```bash
  git config --global credential.helper store
  ```

  * 한 번 로그인(Token 입력)하면 이후부터는 묻지 않는다. 정보는 `~/.git-credentials` 파일에 평문으로 저장된다.

### 3.3 GitHub CLI 활용 (가장 현대적인 방법)
GitHub 공식 CLI 도구인 `gh`를 설치하면 로그인 한 번으로 모든 인증이 해결된다.
```bash
gh auth login
# 안내에 따라 브라우저 인증 완료
```

---

## 4. 활용 팁: 프로필 페이지 업데이트
GitHub Profile 전용 저장소(자신의 ID와 동일한 이름)와 같이 빈번하게 Push가 발생하는 프로젝트의 경우, 위 인증 설정을 해두면 별도의 입력 없이 로컬 마크다운 수정 후 즉시 반영이 가능하여 작업 생산성이 비약적으로 향상된다.

## References

* [GitHub Docs - Managing remote repositories](https://docs.github.com/en/get-started/getting-started-with-git/managing-remote-repositories)
