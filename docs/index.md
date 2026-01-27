# TIL (Today I Learned)

TIL(Today I Learned) 기록이 쌓임에 따라 발생할 수 있는 분류의 모호함을 해결하고, 나중에 정보를 쉽게 찾을 수 있도록 저장소 구조를 재정의한다.

## 개요
기존의 파편화된 폴더 구조를 기술 스택과 도메인 중심으로 재편성하여 유지보수성을 높인다.

## 본문

### 1. 카테고리 분류 원칙
- **언어(Language)**: 특정 프로그래밍 언어 자체의 기능, 프레임워크, 라이브러리 (ex: Java, Python, Node.js)
- **웹(Web)**: 웹 개발 전반의 개념 및 프론트엔드/백엔드 기술 (ex: Web Concepts)
- **인프라(Infrastructure)**: 서버, 네트워크, 배포 및 운영 관련 기술 (ex: Linux, Docker, Network)
- **데이터(Data)**: 데이터 처리, 저장, 관리 및 빅데이터 기술 (ex: Database, FileSystem, Hadoop)
- **컴퓨터 과학(Computer Science)**: 전산학 기초 이론 및 아키텍처 (ex: OS, Design Pattern, Security, Architecture)
- **도구(Tools)**: 개발 생산성을 높이는 도구 및 서비스 (ex: Git, IDE, Markdown)
- **생활(Life)**: 커리어, 재테크, 마인드셋 등 개발 외적인 요소
- **아키텍처 쿡북(Architecture Cookbook)**: 외부 아키텍처 가이드 저장소 링크

### 2. 파일 명명 규칙 (Naming Convention)
- 공백 대신 언더바(`_`)나 하이픈(`-`)을 사용한다.
- 기술 명칭은 가급적 공식 명칭의 대소문자를 따른다.

### 3. 디렉토리 구조 예시

    .
    ├── Language/           # Java, Python, Node.js ...
    ├── Web/                # Web Concepts, Vue.js ...
    ├── Infrastructure/     # Linux, Docker, Message Broker ...
    ├── Data/               # Database, FileSystem ...
    ├── ComputerScience/    # OS, DesignPattern, Security, Architecture ...
    ├── Tools/              # Git, IDE ...
    └── Life/               # Career, RealEstate ...


## References
* [Google Technical Writing Style Guide](https://developers.google.com/style)
* [How to maintain a TIL repository](https://github.com/jbranchaud/til)

