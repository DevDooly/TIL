📂 경로: Architecture/TIL_Structure_Guide.md

# TIL 저장소 구조 개선 가이드

TIL(Today I Learned) 기록이 쌓임에 따라 발생할 수 있는 분류의 모호함을 해결하고, 나중에 정보를 쉽게 찾을 수 있도록 저장소 구조를 재정의한다.

## 개요
기존의 파편화된 폴더 구조를 기술 스택과 도메인 중심으로 재편성하여 유지보수성을 높인다.

## 본문

### 1. 카테고리 분류 원칙
- **언어(Language)**: 특정 프로그래밍 언어 자체의 기능이나 표준 라이브러리 (ex: Python, JavaScript)
- **도구(Tools)**: 업무 효율을 높이는 도구나 설정법 (ex: Docker, Git, IDE)
- **컴퓨터 과학(CS)**: 언어와 상관없는 핵심 이론 (ex: Network, OS, Database)
- **기타(Others)**: 기술 외적인 학습 내용 (ex: 부동산, 마음가짐)

### 2. 파일 명명 규칙 (Naming Convention)
- 공백 대신 언더바(`_`)나 하이픈(`-`)을 사용한다.
- 기술 명칭은 가급적 공식 명칭의 대소문자를 따른다.

### 3. 디렉토리 구조 예시

    .
    ├── Python/             # Python 문법, 전용 라이브러리
    ├── Database/           # SQL, NoSQL, Naming Convention
    ├── Infrastructure/     # Docker, Linux, Network
    ├── CS/                 # OS, DesignPattern, DataStructure
    └── Mindset/            # 회고, 습관 개선 등

## References
* [Google Technical Writing Style Guide](https://developers.google.com/style)
* [How to maintain a TIL repository](https://github.com/jbranchaud/til)
