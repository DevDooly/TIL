# Git Submodules (서브모듈)

Git 저장소 안에 또 다른 Git 저장소를 디렉토리로 포함시켜 관리하는 기능이다. 외부 라이브러리나 공통 모듈을 자신의 프로젝트에서 사용할 때 유용하다.

## 1. 서브모듈이 포함된 저장소 Clone 하기

서브모듈이 포함된 프로젝트를 처음 Clone 할 때는 `--recursive` 옵션을 사용해야 서브모듈의 내용까지 함께 받아온다.

```bash
git clone --recursive https://github.com/username/repo.git
```

만약 이미 Clone을 받았는데 서브모듈 폴더가 비어있다면, 다음 명령어로 초기화 및 업데이트를 수행한다.

```bash
git submodule update --init --recursive
```

---

## 2. 서브모듈 추가하기 (Add)

새로운 서브모듈을 프로젝트에 추가한다.

```bash
# git submodule add [저장소 URL] [디렉토리 경로]
git submodule add https://github.com/other/library.git libs/library
```
이 명령을 실행하면 `.gitmodules` 파일이 생성되며, 서브모듈 정보가 기록된다.

---

## 3. 서브모듈 업데이트 (Update)

서브모듈 리포지토리의 최신 변경 사항을 가져오려면 해당 디렉토리로 이동하여 `git pull`을 하거나, 프로젝트 루트에서 다음 명령어를 사용한다.

```bash
git submodule update --remote
```

---

## 4. 서브모듈 삭제하기 (Remove)

서브모듈은 단순히 디렉토리 삭제만으로는 완전히 제거되지 않는다.

1. `.gitmodules` 파일에서 해당 서브모듈 항목 삭제
2. `.git/config` 파일에서 해당 서브모듈 항목 삭제
3. `git rm --cached [서브모듈 경로]` 실행
4. `rm -rf .git/modules/[서브모듈 경로]` 실행
5. `rm -rf [서브모듈 디렉토리]` 실행

## References
* [Git Tools - Submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules)