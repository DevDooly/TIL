# Git Tips

## Git Aliases
터미널에서 작업시간을 절약하기 위한 별칭 만들기.  
가장 자주 사용되는 명령어에 별칭을 지정할 수 있다. (ex.`checkout`, `commit`, `branch`)

```bash
git config --global alias.co checkout
git config --global alias.ci commit
git config --global alias.br branch
```

`~/.gitconfig` 파일을 수정해 별칭을 더 추가할 수 있다.
```scripts
[alias]
    co = checkout
    ci = commit
    br = brach
```

`git checkout master` 대신 `git co master` 로 사용 가능

## 터미널에서 Repository 상태 보기

[`git-prompt.sh`](https://github.com/git/git/blob/master/contrib/completion/git-prompt.sh) 를 사용한다.  
Linux를 사용중이라면 이미 있을 수 있다. ( `/etc/bash_completion,d/` )

## Command Line 에서 Commit 비교하기

다른 커밋 간에 동일한 파일을 비교하려면 아래와 같이 사용한다.
```bash
$ git diff $start_commit..$end_commit -- path/to/file
```

두 커밋을 비교한다면 아래와 같이 사용한다.
```bash
$ git diff $start_commit..$end_commit
```

### Meld ( diff 시각화 툴 )
Meld는 시각적 비교 미 병합 도구이다.  
현 지점에서는 git diff 을 대체해서 사용할 수 있다.

**공식사이트 : https://meldmerge.org/**

#### Meld 구성하기
```bash
$ git config --global diff.tool git-meld
```

#### diff 에서 사용하기
```bash
$ git difftool $start_commit..$end_commit -- path/to/file
# or
$ git difftool $start_commit..$end_commit
```

## 커밋되지 않은 변경 사항 숨기기
```bash
$ git stash
```
stash 한 내용 돌리고, stash list 에서 삭제하기
```bash
$ git stash pop
```
불필요한 stash 스택 지우기
```bash
$ git stash drop
```

## 명령 자동 완성
[완료 스크립트](https://github.com/git/git/tree/master/contrib/completion)를 사용하여 `bash`, `tcsh`나 `zsh` 에서 명령을 빠르게 생성할 수 있습니다.  
`git pull`을 사용하는 경우 `git p` 다음 `Tab`을 사용하여 다음을 표시해준다.
```bash
pack-objects   -- create packed archive of objects
pack-redundant -- find redundant pack files
pack-refs      -- pack heads and tags for efficient repository access
parse-remote   -- routines to help parsing remote repository access parameters
patch-id       -- compute unique ID for a patch
prune          -- prune all unreachable objects from the object database
prune-packed   -- remove extra objects that are already in pack files
pull           -- fetch from and merge with another repository or local branch
push           -- update remote refs along with associated objects
```

사용 가능한 모든 명령을 표시하려면 `git` + `Tab` 을 사용한다.

## Common Terminology

### Pull Request vs Merge Request
기본적으로 이 두 용어는 **브랜치의 변경 사항을 다른 브랜치(주로 main/master)에 병합해달라고 요청하는 것**으로, 본질적으로 동일한 개념이다.

- **Pull Request (PR):** GitHub, Bitbucket 등에서 사용하는 용어. "내 변경 사항을 당신의 저장소로 당겨가세요(Pull)"라는 의미.
- **Merge Request (MR):** GitLab에서 사용하는 용어. "내 변경 사항을 병합(Merge)해주세요"라는 의미.

## References
* https://about.gitlab.com/blog/2020/04/07/15-git-tips-improve-workflow/

