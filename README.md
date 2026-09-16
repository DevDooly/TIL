# TIL · Today I Learned

백엔드 개발, 데이터 처리, 시스템 운영 과정에서 배운 내용을 기록하는 개인 기술 위키입니다. 개념과 사용법, 기술 비교, 문제 해결 과정을 정리합니다.

[위키에서 읽기](https://devdooly.github.io/TIL/) · [전체 문서](docs/Sitemap.md) · [최근 업데이트](docs/Recent_Changes.md) · [트러블슈팅](docs/Troubleshooting/README.md)

## 주제별 찾아보기

| 주제 | 문서 모음 |
| :--- | :--- |
| 언어와 백엔드 | [Java · Spring Boot](docs/Language/Java/README.md), [Python](docs/Language/Python/README.md), [Node.js](docs/Language/NodeJs/README.md) |
| 데이터 | [DB · SQL · 동시성 제어](docs/Data/Database/README.md), [로그 수집과 데이터 처리](docs/Data/README.md) |
| 인프라 | [Kafka · Kubernetes · Docker · Linux](docs/Infrastructure/README.md) |
| 컴퓨터 과학 | [아키텍처 · 네트워크 · 보안](docs/ComputerScience/README.md) |
| AI 활용 | [AI 도구와 에이전트](docs/AI/README.md), [LLM을 활용한 개발](docs/LLM_Development/README.md) |
| 웹과 개발 도구 | [웹 · API](docs/Web/README.md), [Git · 빌드 · 터미널](docs/Tools/README.md) |

## 주요 기록

- [비관적·낙관적 락과 동시성 제어](docs/Data/Database/Locking_Strategy.md): 락 전략의 차이와 SQL·JPA 적용 예시.
- [Virtual Thread의 FTP pinning 진단](docs/Language/Java/Virtual_Threads_FTP_Pinning.md): JDK 버전과 실행 경로에 따른 진단.
- [Kafka 파티셔너 불균형 분석](docs/Infrastructure/MessageBroker/Kafka/Producer_Partitioner_Issue.md): 원인과 수정 버전 확인.
- [LLM을 활용한 레거시 코드 개선](docs/LLM_Development/Legacy_Code_Improvement.md): 알고리즘·시간 처리·코딩 스타일 변경과 검증.

## 지식 추가와 수정

Gemini로 필요한 주제를 요청하고, 프로젝트 스킬로 작성·갱신·검증합니다.

작성과 수정에는 [문체 가이드](.agents/skills/til-natural-writing/SKILL.md)를 함께 적용해 반복적인 날짜·상투어를 줄이고, 구체적인 현상과 이유를 중심으로 설명합니다.

[새 지식 작성](.agents/skills/til-knowledge-write/SKILL.md) · [기존 문서 갱신](.agents/skills/til-knowledge-refresh/SKILL.md) · [문제 해결 기록](.agents/skills/til-troubleshooting/SKILL.md) · [문서 검증](.agents/skills/til-doc-verify/SKILL.md)

> 요청 예: “til-knowledge-refresh 스킬로 Virtual Thread 문서를 JDK 25 기준으로 확인하고 차이를 반영해줘.”

스킬이 자동으로 선택되지 않으면 해당 `SKILL.md`를 읽도록 요청합니다. 공통 규칙은 [프로젝트 지침](.gemini/GEMINI.md), 커밋과 게시 절차는 [Git 작업 가이드](.agents/skills/git-workflow/SKILL.md)를 참고합니다.

## 로컬에서 보기

Python 환경에 [필수 패키지](requirements.txt)를 설치한 뒤 미리보기를 실행합니다.

```bash
python -m pip install -r requirements.txt
python -m mkdocs serve
```

문서 검증에는 JDK 21 이상과 Git, Bash도 필요합니다. Windows에서는 Git Bash를 사용합니다. 전체 점검 명령은 [문서 검증 가이드](.agents/skills/til-doc-verify/SKILL.md)에 있습니다.

검토한 변경을 게시하려면 다음 명령을 실행합니다. 현재 작업 폴더의 모든 변경을 커밋하고, 생성 문서 갱신과 검증을 마친 뒤 push합니다.

```bash
PYTHON=python bash scripts/publish.sh "docs: 변경 내용"
```
