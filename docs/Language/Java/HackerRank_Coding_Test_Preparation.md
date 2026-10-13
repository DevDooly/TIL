---
title: 올리브영 HackerRank Java 코딩테스트 준비
---

# 올리브영 HackerRank Java 코딩테스트 준비

HackerRank에서 Java 코딩테스트를 준비할 때는 자료구조를 선택하고, 제한 시간 안에 구현과 검증을 마치는 연습부터 한다. 실무에서 익숙한 Java도 온라인 편집기의 함수 형식과 입력 조건에 맞춰 작성하는 연습이 필요하다.

올리브영의 공개 후기와 HackerRank 공식 안내를 바탕으로 연습 순서를 정리했다. 회사의 실제 시험 시간·문항 수·자료 사용 범위는 응시 초청과 시험 안내에서 확인한다. 아래 7일 일정과 90분 모의시험은 학습용으로 잡은 분량이다.

## 공개 후기에서 참고할 내용

| 자료 | 작성자가 설명한 경험 | 준비에 참고할 부분 |
| :--- | :--- | :--- |
| [2025년 경력 채용 관련 글](https://www.teamblind.com/kr/post/올리브영-경력직-채용-프로세스-궁금해-buw6olii) | 사전코테 링크 수령. 댓글에서 HackerRank와 영어 지문 경험 언급 | 익명 경험이며 세부 직무와 시험 시간은 불명확하다. 영어 지문을 읽고 온라인 편집기를 사용하는 연습에 참고한다. |
| [2025년 Java 준비 기록](https://velog.io/@evielee/코테-JAVA로-코딩테스트-벼락치기) | 당시 Software Engineer 코테의 허용 언어가 Java·C#이었다고 기록 | 작성자는 문법·자료구조·구현·탐색을 복습했다. 경력 전형인지는 확인되지 않는다. |
| [2023년 응시 후기](https://velog.io/@nayu1105/CJ-올리브영-코딩테스트-후기) | 당시 3시간·3문제, 오픈북·카메라 없음. 풀이 방향을 알아도 구현 시간이 부족했던 경험 | 웹캠이 필요한 응시 안내와 조건이 다르다. 제한 시간 안에 구현을 완성하는 연습의 필요성을 참고한다. |

과거 응시자의 체감 난이도와 풀이 수만으로 현재 전형의 난이도나 합격 기준을 정할 수는 없다. 공개 후기의 시험 조건은 해당 시점의 경험이며, 실제 응시에서는 받은 안내가 우선이다.

검색에 나오는 AI 과제 도입도 전형 범위를 함께 봐야 한다. 올리브영의 2026년 7월 21일 발표는 7월 20일~8월 9일 접수한 **AI-First Track**의 Cofa-Probe 과제 전형을 설명한다. HackerRank 시험에서 검색·번역기·외부 IDE·AI를 사용할 수 있는지는 해당 시험 규정으로 확인한다. [올리브영 공식 발표](https://corp.oliveyoung.com/ko/newsroom/press/134)

## Java로 먼저 점검할 부분

연습은 문자열·배열·해시·정렬부터 시작하고, 스택·큐와 BFS, 구간 처리와 우선순위 큐로 넓힌다. 같은 입력을 중복 순회하는 부분을 찾아 시간복잡도를 설명하고, 샘플 밖의 경계 조건도 확인한다.

- `HashMap`, `HashSet`: 빈도 집계, 중복 확인, 빠른 조회
- `ArrayDeque`: 스택·큐와 BFS의 대기 노드 관리
- `Arrays.sort`, `List.sort`, `PriorityQueue`: 정렬과 우선순위에 따른 처리
- 수치와 문자열: 합계·곱셈의 `long` 처리, 문자열의 `.equals()` 비교
- 경계 조건: 허용된 최소·최대 입력, 중복 값, 답이 없는 경우, 인덱스 범위

합계가 `int` 범위를 넘는 경우는 [A Very Big Sum](https://www.hackerrank.com/challenges/a-very-big-sum/problem)으로 확인할 수 있다. 실무에서 사용하는 JDK와 시험의 허용 버전이 같다고 가정하지 않고, 제공된 함수 이름·인자·반환형에 맞춰 구현한다. 회사는 시험의 허용 언어를 제한할 수 있으며, 버전과 실행 제한은 시험 화면의 Execution Environment에서 확인할 수 있다. [HackerRank 공식 언어 안내](https://candidatesupport.hackerrank.com/articles/2200226909)

## 하루 두 시간 기준 7일 연습 계획

다음 문제는 HackerRank에 공개된 연습문제다. 올리브영 시험의 출제 목록을 뜻하지 않는다.

| 일정 | 연습 내용 | 문제와 완료 목표 |
| :--- | :--- | :--- |
| 1일차 | 환경 적응과 현재 수준 점검 | [A Very Big Sum](https://www.hackerrank.com/challenges/a-very-big-sum/problem), [Two Strings](https://www.hackerrank.com/challenges/two-strings/problem), [Balanced Brackets](https://www.hackerrank.com/challenges/balanced-brackets/problem). 각각 15·25·40분을 잡고 남은 시간에 복기한다. |
| 2일차 | 해시와 빈도 관리 | [Frequency Queries](https://www.hackerrank.com/challenges/frequency-queries/problem). 반복 조회에서 매번 전체 데이터를 순회하는 부분을 찾아 개선한다. |
| 3일차 | 정렬과 탐색 | [Mark and Toys](https://www.hackerrank.com/challenges/mark-and-toys/problem), [Pairs](https://www.hackerrank.com/challenges/pairs/problem). 풀이 전에 예상 시간복잡도를 적는다. |
| 4일차 | BFS와 방문 처리 | [BFS Shortest Reach](https://www.hackerrank.com/challenges/bfsshortreach/problem). 인접 리스트·큐·방문 배열을 직접 구성한다. |
| 5일차 | 구간 처리와 우선순위 큐 | [Subarray Division](https://www.hackerrank.com/challenges/the-birthday-bar/problem), [Jesse and Cookies](https://www.hackerrank.com/challenges/jesse-and-cookies/problem). |
| 6일차 | 제한 시간 모의시험 | 처음 보는 공개 문제로 연습용 90분·3문제를 진행한다. 검색·AI 없이 풀고 이후 30분 복기한다. |
| 7일차 | 오답 재풀이와 응시 준비 | 틀린 문제를 해설 없이 다시 구현하고 웹캠·브라우저·저장·제출 절차를 확인한다. |

3일 이하로 남았다면 현재 수준 점검, 해시·정렬·스택과 오답, 모의시험·환경 점검 순서로 압축한다. 새 유형을 많이 늘리기보다 접근할 수 있는 문제를 끝까지 완성하는 데 시간을 쓴다.

## 문제를 풀고 복기하는 방법

1. 입력 제약을 읽고 데이터 크기와 허용되는 값을 적는다.
2. 가장 단순한 풀이와 예상 시간·공간복잡도를 생각한다.
3. 반복 탐색을 줄일 자료구조나 정렬 방법을 고른다.
4. 제공된 함수 형식에 맞춰 구현한다.
5. 샘플과 직접 만든 경계 테스트를 실행한다.

문제마다 소요 시간, 힌트 사용 여부, 막힌 부분, 실패한 입력, 최종 시간복잡도를 남긴다. 풀이 설계가 막혔는지, Java API 사용에서 지체했는지, 구현 후 경계 조건을 놓쳤는지를 구분하면 다음 연습 대상을 정하기 쉽다. 해설을 본 문제는 다음 날 해설 없이 다시 구현한다.

샘플 통과 뒤에도 허용 입력 범위의 양 끝과 답이 없는 경우를 확인한다. HackerRank의 숨겨진 테스트는 샘플에 없는 경계 조건 등을 확인하므로 샘플 통과만으로 구현 검증이 끝나지는 않는다. [HackerRank 공식 테스트 안내](https://candidatesupport.hackerrank.com/articles/2859650598-frequently-asked-questions-during-the-test)

## HackerRank 응시 환경 점검

### Java 버전과 제공 코드

시험에서 선택 가능한 Java 버전과 함수 형식을 먼저 확인한다. 제공된 입출력 코드를 사용하는 문제는 지정된 함수와 반환형을 유지한다. 버전별 언어 기능이나 API를 사용할 때는 해당 실행 환경에서 지원하는지 확인한다. [공식 언어 안내](https://candidatesupport.hackerrank.com/articles/2200226909)

### 연습 화면과 답안 저장

Sample Test에서 편집기, 코드 실행, 사용자 입력 테스트, 답안 저장·제출을 미리 사용해 본다. 본시험의 최종 시작은 응시 준비가 끝난 뒤 진행한다. `Run Code`와 답안 저장은 별도 동작이며, 구간별 시간 제한이 있는 시험은 종료된 구간으로 돌아가지 못할 수 있다. [응시 전 안내](https://candidatesupport.hackerrank.com/articles/6145743949-frequently-asked-questions-before-the-test), [실행과 저장 안내](https://candidatesupport.hackerrank.com/articles/2859650598-frequently-asked-questions-during-the-test)

### 웹캠과 시험 규정

지원서와 같은 실제 이름을 입력하고, 웹캠이 작동하는 PC에서 조명·전원·네트워크를 점검한다. 웹캠 촬영 방식과 자료 사용 범위는 회사의 초청 메일과 시험 안내를 따른다. [HackerRank 공식 응시 전 안내](https://candidatesupport.hackerrank.com/articles/6145743949-frequently-asked-questions-before-the-test)

문제별로 실패 원인을 직접 설명할 수 있도록 연습하고, 검색과 AI를 사용한 복기는 제한 시간 풀이가 끝난 뒤 진행한다.

## 관련 문서

- [Java 문서 모음](README.md)
- [Java 버전별 변경점](Versions/README.md)
- [Java 함수형 프로그래밍](Functional/README.md)
