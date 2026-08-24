---
title: Engineering & Productivity Tools
---

# ⚙️ Engineering & Build Tools

개발 생산성, 빌드 자동화, 코드 품질 유지 및 협업 효율성을 극대화하기 위한 **빌드 도구(Maven/Spotless), 버전 관리(Git/GitHub), 터미널 환경(Tmux) 및 유틸리티**를 정리한 공간입니다.

---

## 📚 주요 기술 문서 목차

### 1. Build & Code Quality Automation
* **[Apache Maven 자바 빌드 가이드](Build/Maven.md)**: 빌드 라이프사이클, 플러그인 설정 및 멀티 모듈 관리
* **[Maven Shade Plugin](Build/Maven_Shade_Plugin.md)**: Uber-JAR 생성 및 의존성 충돌 해결(Package Relocation)
* **[Maven Classifier와 Hive-JDBC](Build/Maven_Classifier_and_Hive_JDBC.md)**: 특정 플랫폼/환경 의존성 분류자 활용법
* **[Spotless 코드 스타일 자동화](Build/Spotless.md)**: CI/CD 파이프라인 연동 및 자동 포맷팅 적용
* **[Java Code Formatters Comparison](Build/Java_Code_Formatters_Comparison.md)**: Google Java Format vs Palantir Java Format 비교 분석

### 2. Git & Version Control
* **[Monorepo vs Polyrepo](Git/Monorepo_vs_Polyrepo.md)**: 대규모 코드베이스 아키텍처 비교 및 선택 전략
* **[Git Remote Settings](Git/Remote_Settings.md)**: 다중 원격 저장소 관리 및 업스트림 동기화
* **[Git Submodules](Git/Submodules.md)**: 서브모듈 추가, 업데이트 및 관리 전략
* **[Git Tag](Git/Tag.md)**: 릴리즈 태깅 및 배포 버전 관리
* **[Git Tips & Tricks](Git/Tips.md)**: Cherry-pick, Stash, Rebase 등 실무 유용한 명령어 모음
* **[GitHub Actions Deploy Fail 트러블슈팅](Github/Action_Deploy_Fail.md)**: CI/CD 배포 실패 디버깅

### 3. Terminal & Open Source Utilities
* **[Tmux (Terminal Multiplexer)](Terminal/Tmux.md)**: 세션 유지, 윈도우/패널 분할 및 단축키 활용
* **[FFmpeg](OpenSource/FFmpeg.md)**: 미디어 트랜스코딩, 스트림 추출 및 변환 명령어
