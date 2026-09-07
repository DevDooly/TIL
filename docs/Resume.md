---
title: Backend Engineer - Career Profile
---

# Backend Engineer · 공개 경력 요약

업데이트: 2026-09-07. 이 페이지는 확인된 업무 경험을 요약한다. 위키의 모든 학습 문서가 실무 적용 기술을 의미하지는 않는다.

## 주요 업무

미리비트에서 Java·Spring Boot 기반 프로젝트를 지속적으로 개발하고 유지보수하고 있다. 데이터 처리 로직과 프로젝트 구조를 개선하고, Kafka 관련 버그 분석·수정 및 버전 업그레이드 업무를 수행했다.

Kubernetes와 MinIO 환경에서 서비스를 운영하며 Helm chart 작성과 배포 작업을 진행하고 있다.

## 문제 해결과 개발 방식

- 레거시 코드 분석에 LLM을 적극 활용해 반도체 수율 개선을 지원하는 수학적 로직의 계산 복잡도를 낮추고 시간 동기화 관련 오류를 수정했다.
- 프로젝트의 구현 방식과 코딩 스타일을 일관되게 정리했다.
- Virtual Thread 적용 과정의 pinning 이슈를 해결한 경험이 있다. 관련 문서에서는 JDK·라이브러리 버전과 진단 근거를 구분한다.

세부 알고리즘의 전후 복잡도, 성능 수치와 운영 지표는 측정 조건을 확인한 뒤 보완한다. 공개 근거가 없는 처리량 개선율은 기재하지 않는다.

## 관련 기록

- [LLM을 활용한 레거시 개선과 검증 기록](LLM_Development/Legacy_Code_Improvement.md)
- [Kafka 파티셔너 불균형 진단](Infrastructure/MessageBroker/Kafka/Producer_Partitioner_Issue.md)
- [Consumer의 종료와 처리 완료 offset](Infrastructure/MessageBroker/Kafka/Consumer_Safe_Shutdown.md)
- [Virtual Thread pinning 진단](Language/Java/Virtual_Threads_FTP_Pinning.md)
- [트러블슈팅 문서 모음](Troubleshooting/README.md)

## 학습

**CKA 준비 중**이다. Kubernetes 운영·장애 대응과 복원 실습을 학습 기록으로 정리한다. Apache Arrow, GitOps, AI 도구 등 위키의 다른 주제는 각 문서의 적용 범위를 확인한다.

- [GitHub](https://github.com/DevDooly)
- [TIL Wiki](https://devdooly.github.io/TIL/)
