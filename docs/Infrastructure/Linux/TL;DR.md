# TL;DR (Too Long; Didn't Read)

**tldr-pages**는 복잡하고 긴 `man` 페이지 대신, 자주 사용하는 옵션과 실용적인 예제 위주로 명령어를 요약해 주는 커뮤니티 프로젝트입니다.

## 1. 설치

```bash
# Node.js (npm)
npm install -g tldr

# macOS (Homebrew)
brew install tldr

# Python (pip)
pip install tldr
```

## 2. 사용법

```bash
# tar 명령어 사용법 보기
tldr tar

# git checkout 예제 보기
tldr git checkout
```

## 3. 예시 출력 (tar)
```text
  tar

  Archiving utility.
  Often combined with a compression method, such as gzip or bzip2.

  - Create an archive from files:
    tar cf target.tar file1 file2 file3

  - Create a gzipped archive:
    tar czf target.tar.gz file1 file2 file3

  - Extract a (compressed) archive into the current directory:
    tar xf source.tar[.gz|.bz2|.xz]
```

## 참고
*   [tldr-pages 공식 사이트](https://tldr.sh/)