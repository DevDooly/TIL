# LLM Development Guide (LLM 개발 가이드)

AI 및 LLM(Large Language Model)을 활용하여 소프트웨어를 개발할 때 필요한 필수적인 요소들과 주의사항, 그리고 효과적인 개발 프로세스를 정리합니다.

## 📌 개요

LLM 기반 개발은 기존의 확정적(Deterministic) 프로그래밍과는 다른 접근 방식이 필요합니다. 모델의 확률적 특성을 이해하고, 이를 제어하며 품질을 유지하기 위한 체계적인 가이드라인을 제공하는 것이 이 섹션의 목적입니다.

## 🏗️ 주요 내용

이 섹션은 LLM을 활용한 개발 여정의 각 단계별 필수 지식과 체크리스트를 다룹니다.

### 📝 개발 단계별 가이드

- **[AI 명령 설계(Prompting · Context · Harness) 방법론 및 주기적 운영 가이드](AI_Command_and_Prompting_Methodology.md)**: AI에게 명확하게 명령을 내리는 5대 원칙, Before/After 사례 카탈로그, 그리고 지시 패턴을 주기적으로 규칙·스킬(`SKILL.md`)로 승격하는 운영 체계
- **[레거시 코드 개선과 검증 기록](Legacy_Code_Improvement.md)**: LLM을 활용한 알고리즘·시간 처리·코딩 스타일 개선의 검증 절차
- **[UTC 구간 계산의 AI 제안 검증](UTC_Window_Analysis_Case.md)**: 독립 oracle·시간대 회귀·실제 JMH 측정을 연결한 공개 합성 사례
- **[Web Development Checklist](Web_Development_Checklist.md)**: 프론트엔드 UI/UX, 클라이언트 로직 개발 시 고려사항
- **[Backend Development Checklist](Backend_Development_Checklist.md)**: 서버 로직, DB 설계, 보안 및 테스트 가이드

### 📚 핵심 주제 (예정)

1. **LLM 개발 시 주의 사항 (Precautions)**
    - 할루시네이션(Hallucination) 관리
    - 보안 및 데이터 프라이버시 (API 키, 민감 정보 노출 방지)
    - 비용 및 토큰 관리 전략

2. **확인 및 검증 사항 (Checklist)**
    - 출력 형식의 일관성 (Structured Output)
    - 프롬프트 엔지니어링 최적화
    - 테스트 및 평가 지표 (RAG 평가 등)

3. **권장 개발 단계 (Development Stages)**
    - 요구사항 분석 및 모델 선정
    - 프롬프트 프로토타이핑 및 실험
    - 시스템 통합 및 최적화 (RAG, Agentic Workflow)
    - 모니터링 및 피드백 루프 구축

4. **필수 요소 (Essential Elements)**
    - 에이전트 워크플로우 설계
    - 도구 사용(Tool Use/Function Calling) 최적화
    - 컨텍스트 관리 전략

## 🚀 시작하기

오른쪽 내비게이션 또는 아래 상세 문서를 통해 각 단계별 가이드를 확인하세요.
