---
title: Java 코딩테스트 1일차부터 5일차 연습문제와 풀이
---

# Java 코딩테스트 1일차부터 5일차 연습문제와 풀이

HackerRank에 접속하지 않고 1~5일차 학습 주제를 연습할 수 있도록 자체 문제 9개를 구성했다. 각 문제의 조건과 예시를 읽고 먼저 구현한 뒤, 접힌 **정답과 Java 풀이 펼치기** 영역에서 풀이 방법·코드·복잡도·경계 조건을 확인한다.

기존 계획의 공개 문제와 같은 자료구조·알고리즘을 연습하되 상황·입력 조건·예시·함수 계약을 새로 구성했다. 원문은 표의 참고 링크에서 볼 수 있으며, 아래 클래스와 반환형은 이 페이지의 연습용 계약이다.

[준비 계획과 응시 안내](HackerRank_Coding_Test_Preparation.md) · [Java 문서 모음](README.md)

| 일차 | 이 페이지의 연습문제 | 대응하는 공개 학습 주제 |
| :--- | :--- | :--- |
| 1일차 | [01 정산 조정액 합계](#exercise-01) | [A Very Big Sum](https://www.hackerrank.com/challenges/a-very-big-sum/problem) |
| 1일차 | [02 공통 문자가 있는 태그](#exercise-02) | [Two Strings](https://www.hackerrank.com/challenges/two-strings/problem) |
| 1일차 | [03 설정 문자열의 괄호 검사](#exercise-03) | [Balanced Brackets](https://www.hackerrank.com/challenges/balanced-brackets/problem) |
| 2일차 | [04 장비 알림의 발생 횟수 조회](#exercise-04) | [Frequency Queries](https://www.hackerrank.com/challenges/frequency-queries/problem) |
| 3일차 | [05 실습용 센서 구매하기](#exercise-05) | [Mark and Toys](https://www.hackerrank.com/challenges/mark-and-toys/problem) |
| 3일차 | [06 일정 간격으로 떨어진 측정값 찾기](#exercise-06) | [Pairs](https://www.hackerrank.com/challenges/pairs/problem) |
| 4일차 | [07 창고 구역 사이의 최소 이동 횟수](#exercise-07) | [BFS Shortest Reach](https://www.hackerrank.com/challenges/bfsshortreach/problem) |
| 5일차 | [08 연속 측정 구간의 합 확인하기](#exercise-08) | [Subarray Division](https://www.hackerrank.com/challenges/the-birthday-bar/problem) |
| 5일차 | [09 보정 모듈의 점수 끌어올리기](#exercise-09) | [Jesse and Cookies](https://www.hackerrank.com/challenges/jesse-and-cookies/problem) |

## 풀이 코드 실행 방법

각 정답에는 외부 라이브러리 없이 실행할 수 있는 `Exercise01`~`Exercise09` 클래스와 예시용 `main`이 있다. 클래스 이름과 같은 파일명으로 저장한다. 예를 들어 01번 코드는 `Exercise01.java`에 저장하고 다음과 같이 실행한다.

```sh
javac -encoding UTF-8 Exercise01.java
java Exercise01
```

풀이 코드는 Java 8 문법과 표준 라이브러리를 사용한다. 입력은 각 `main`의 배열·문자열을 바꿔 확인할 수 있으며, 표준 입력을 읽는 코드는 포함하지 않는다. 함수는 문제에 명시한 유효 입력을 받는다고 가정한다.

## 1일차 큰 정수와 문자열과 스택

<a id="exercise-01"></a>

### 01. 정산 조정액 합계

**연습 주제:** 큰 정수의 합계, `int`와 `long`의 범위.

#### 문제

정산 시스템은 금액이 늘어나면 양수, 줄어들면 음수인 조정액을 기록한다. 하루 동안 기록한 조정액을 모두 더해 최종 변동 금액을 구하라. 각각의 조정액과 전체 합계는 `int` 범위를 넘을 수 있다.

#### 제약과 함수 계약

- `0 ≤ adjustments.length ≤ 100,000`
- 각 조정액은 `-1,000,000,000,000` 이상 `1,000,000,000,000` 이하이다.
- 입력 배열은 `null`이 아니다. 입력 배열을 수정하지 않는다.
- `public static long total(long[] adjustments)`를 구현한다.
- 반환값은 모든 조정액의 합이다. 기록이 없으면 `0`을 반환한다.

#### 예시 1

| 항목 | 값 |
| --- | --- |
| 입력 | `[2400000000, 1700000000, -600000000]` |
| 반환값 | `3500000000` |

양수와 음수를 그대로 더한다. 결과가 `int`의 최댓값을 넘으므로 합계 변수도 `long`이어야 한다.

#### 예시 2

| 항목 | 값 |
| --- | --- |
| 입력 | `[]` |
| 반환값 | `0` |

??? success "정답과 Java 풀이 펼치기"

    **접근:** 합계 변수를 `long`의 `0L`로 초기화하고 배열을 한 번 순회한다. 이 문제의 최대 절댓값 합은 `100,000 × 10^12 = 10^17`이므로 `long` 범위 안에 들어간다. `int`로 계산한 뒤 마지막에 `long`으로 변환하면 앞선 오버플로를 복구할 수 없다.

    ```java
    public class Exercise01 {
        public static long total(long[] adjustments) {
            long total = 0L;
            for (long adjustment : adjustments) {
                total += adjustment;
            }
            return total;
        }

        public static void main(String[] args) {
            System.out.println(total(new long[] {
                2_400_000_000L, 1_700_000_000L, -600_000_000L
            }));
            System.out.println(total(new long[0]));
        }
    }
    ```

    실행 시 `3500000000`, `0`이 각각 한 줄에 출력된다.

    **복잡도:** 배열 길이가 `n`일 때 시간 `O(n)`, 입력 배열을 제외한 추가 공간 `O(1)`.

    **직접 확인할 경계조건:** 빈 배열, 음수만 있는 배열, 합이 `0`인 배열, `int` 범위를 넘는 합계. 테스트 데이터의 큰 정수 리터럴에도 `L`을 붙인다.

<a id="exercise-02"></a>

### 02. 공통 문자가 있는 태그

**연습 주제:** 존재 여부를 저장하는 집합, 고정 크기 배열.

#### 문제

두 개의 장비 태그가 문자열로 주어진다. 두 태그에 공통으로 등장하는 영문 소문자가 하나라도 있으면 `true`, 없으면 `false`를 반환하라. 문자 위치와 등장 횟수는 관계없으며, 문자열이 비어 있을 수도 있다.

#### 제약과 함수 계약

- 각 문자열의 길이는 `0` 이상 `100,000` 이하이다.
- 문자는 영문 소문자 `a`부터 `z`까지만 사용한다.
- 두 문자열은 `null`이 아니다.
- `public static boolean hasCommonCharacter(String first, String second)`를 구현한다.
- 공통 문자가 존재하면 `true`, 존재하지 않으면 `false`를 반환한다.

#### 예시 1

| 항목 | 값 |
| --- | --- |
| `first` | `"orbit"` |
| `second` | `"voice"` |
| 반환값 | `true` |

`o` 또는 `i`가 두 문자열에 모두 등장한다. 같은 위치에 있을 필요는 없다.

#### 예시 2

| 항목 | 값 |
| --- | --- |
| `first` | `""` |
| `second` | `"signal"` |
| 반환값 | `false` |

??? success "정답과 Java 풀이 펼치기"

    **접근:** 가능한 문자가 26개뿐이므로 첫 문자열의 문자 존재 여부를 `boolean[26]`에 기록한다. 두 번째 문자열을 순회하다가 기록된 문자를 만나면 즉시 `true`를 반환한다. 문자열 두 개의 모든 문자 조합을 비교하는 이중 반복문은 필요 없다.

    ```java
    public class Exercise02 {
        public static boolean hasCommonCharacter(String first, String second) {
            boolean[] present = new boolean[26];
            for (int i = 0; i < first.length(); i++) {
                present[first.charAt(i) - 'a'] = true;
            }
            for (int i = 0; i < second.length(); i++) {
                if (present[second.charAt(i) - 'a']) {
                    return true;
                }
            }
            return false;
        }

        public static void main(String[] args) {
            System.out.println(hasCommonCharacter("orbit", "voice"));
            System.out.println(hasCommonCharacter("", "signal"));
        }
    }
    ```

    실행 시 `true`, `false`가 각각 한 줄에 출력된다.

    **복잡도:** 두 문자열 길이가 각각 `n`, `m`이면 시간 `O(n + m)`, 추가 공간 `O(1)`. 배열의 크기는 입력 길이와 무관하게 26이다.

    **직접 확인할 경계조건:** 두 문자열 모두 비어 있음, 한쪽만 비어 있음, 같은 문자만 반복됨, 공통 문자가 마지막에 등장함, 공통 문자가 전혀 없음. 대문자나 한글까지 지원해야 한다면 현재의 배열 인덱스 규칙을 그대로 사용할 수 없다.

<a id="exercise-03"></a>

### 03. 설정 문자열의 괄호 검사

**연습 주제:** 스택, 괄호의 중첩 순서.

#### 문제

간소화된 설정 문자열에는 `(`, `)`, `[`, `]`, `{`, `}`만 들어 있다. 모든 여는 괄호가 같은 종류의 닫는 괄호와 올바른 순서로 짝지어지면 `true`를 반환하라. 아직 닫히지 않은 괄호 중 가장 최근에 열린 괄호부터 닫혀야 한다. 빈 문자열은 올바른 문자열로 취급한다.

#### 제약과 함수 계약

- `0 ≤ text.length() ≤ 200,000`
- 문자는 `()[]{}` 여섯 종류뿐이다.
- 문자열은 `null`이 아니다.
- `public static boolean isBalanced(String text)`를 구현한다.
- 괄호의 종류와 중첩 순서가 모두 맞으면 `true`, 그렇지 않으면 `false`를 반환한다.

#### 예시 1

| 항목 | 값 |
| --- | --- |
| 입력 | `"{[()()]()}"` |
| 반환값 | `true` |

각 닫는 괄호가 가장 최근의 여는 괄호를 닫는다. 문자열 끝에서 열린 괄호가 남지 않는다.

#### 예시 2

| 항목 | 값 |
| --- | --- |
| 입력 | `"[({)]}"` |
| 반환값 | `false` |

`)`가 등장하는 시점에 가장 최근에 열린 괄호는 `{`이므로 잘못된 순서이다. 괄호 개수가 같다는 사실만으로는 충분하지 않다.

??? success "정답과 Java 풀이 펼치기"

    **접근:** 여는 괄호를 스택에 넣고, 닫는 괄호를 만나면 스택의 맨 위와 비교한다. 스택이 비어 있거나 종류가 다르면 실패한다. 순회가 끝났을 때 스택이 비어 있어야 성공이다. 여기서는 문자 배열과 `size`로 스택을 구현한다.

    ```java
    public class Exercise03 {
        public static boolean isBalanced(String text) {
            char[] stack = new char[text.length()];
            int size = 0;

            for (int i = 0; i < text.length(); i++) {
                char current = text.charAt(i);
                if (current == '(' || current == '[' || current == '{') {
                    stack[size++] = current;
                    continue;
                }

                if (size == 0) {
                    return false;
                }
                char expected;
                if (current == ')') {
                    expected = '(';
                } else if (current == ']') {
                    expected = '[';
                } else {
                    expected = '{';
                }
                if (stack[--size] != expected) {
                    return false;
                }
            }
            return size == 0;
        }

        public static void main(String[] args) {
            System.out.println(isBalanced("{[()()]()}"));
            System.out.println(isBalanced("[({)]}"));
        }
    }
    ```

    실행 시 `true`, `false`가 각각 한 줄에 출력된다.

    **복잡도:** 문자열 길이가 `n`일 때 시간 `O(n)`, 추가 공간 `O(n)`. 최대 `n`개의 여는 괄호가 스택에 쌓일 수 있다.

    **직접 확인할 경계조건:** 빈 문자열, 닫는 괄호로 시작하는 문자열, 여는 괄호만 있는 문자열, 정상 괄호 뒤에 닫는 괄호가 하나 더 있는 문자열, 깊게 중첩된 괄호. 재귀를 사용하지 않으므로 입력 길이만큼 호출 스택을 소비하지 않는다.

## 2일차 해시 맵과 빈도 관리

<a id="exercise-04"></a>

### 04. 장비 알림의 발생 횟수 조회

**연습 주제:** 해시 맵 두 개로 값의 빈도와 빈도의 개수를 함께 관리하기.

#### 문제

장비 알림 번호를 중복 저장할 수 있는 기록함이 처음에는 비어 있다. 다음 연산들을 주어진 순서대로 처리하라.

| 연산 | 의미 |
| --- | --- |
| `[1, x]` | 알림 번호 `x`를 한 번 추가한다. |
| `[2, x]` | 알림 번호 `x`를 한 번 제거한다. 없으면 아무것도 하지 않는다. |
| `[3, f]` | 현재 정확히 `f`번 기록된 알림 번호가 하나라도 있는지 조회한다. |

조회 연산의 결과만 모아 순서대로 반환한다. 서로 다른 번호 여러 개의 발생 횟수를 합쳐서 판단하지 않는다. 기록함에 없는 번호는 조회 대상이 아니다.

#### 제약과 함수 계약

- 연산 수는 `0` 이상 `200,000` 이하이다.
- 각 연산은 길이가 2인 배열이며, 첫 번째 값은 `1`, `2`, `3` 중 하나이다.
- 알림 번호 `x`는 `1` 이상 `1,000,000,000` 이하의 정수이다. 조회 빈도 `f`는 `1` 이상 `200,000` 이하의 정수이다.
- 입력 배열과 각 연산은 `null`이 아니다. 입력 배열을 수정하지 않는다.
- `public static List<Integer> processQueries(int[][] operations)`를 구현한다.
- 반환 리스트에는 `[3, f]` 연산의 결과만 담는다. 조건을 만족하는 번호가 있으면 `1`, 없으면 `0`을 담는다. 조회 연산이 없으면 빈 리스트를 반환한다.

#### 예시 1

| 항목 | 값 |
| --- | --- |
| 입력 | `[[1, 7], [1, 7], [1, 9], [3, 2], [2, 7], [3, 2], [3, 1]]` |
| 반환값 | `[1, 0, 1]` |

첫 조회에서 `7`은 두 번 기록되어 있다. `7`을 한 번 제거하면 `7`과 `9`가 각각 한 번씩 기록되어 있으므로, 두 번 기록된 번호는 없고 한 번 기록된 번호는 있다.

#### 예시 2

| 항목 | 값 |
| --- | --- |
| 입력 | `[[2, 4], [3, 1], [1, 4], [2, 4], [3, 1]]` |
| 반환값 | `[0, 0]` |

처음의 제거 연산은 무시한다. 나중에 `4`를 추가했다가 제거한 뒤에도 기록함은 비어 있으므로 두 조회 모두 `0`이다.

??? success "정답과 Java 풀이 펼치기"

    **접근:** `counts`는 `알림 번호 → 발생 횟수`, `population`은 `발생 횟수 → 그 횟수를 가진 알림 번호의 개수`를 저장한다. 번호 하나의 횟수가 바뀌면 이전 횟수의 개수를 하나 줄이고 새 횟수의 개수를 하나 늘린다. 조회할 때는 `population`에서 바로 확인한다. 발생 횟수가 0이 된 번호는 `counts`에서 제거하고, `population`에는 양의 빈도만 저장한다. 해당 빈도를 가진 번호가 0개가 되면 그 빈도 항목도 제거한다.

    ```java
    import java.util.ArrayList;
    import java.util.HashMap;
    import java.util.List;
    import java.util.Map;

    public class Exercise04 {
        public static List<Integer> processQueries(int[][] operations) {
            Map<Integer, Integer> counts = new HashMap<>();
            Map<Integer, Integer> population = new HashMap<>();
            List<Integer> answers = new ArrayList<>();

            for (int[] operation : operations) {
                int type = operation[0];
                int argument = operation[1];

                if (type == 3) {
                    answers.add(population.getOrDefault(argument, 0) > 0 ? 1 : 0);
                    continue;
                }

                int oldCount = counts.getOrDefault(argument, 0);
                if (type == 2 && oldCount == 0) {
                    continue;
                }

                int newCount = type == 1 ? oldCount + 1 : oldCount - 1;
                changePopulation(population, oldCount, -1);
                if (newCount == 0) {
                    counts.remove(argument);
                } else {
                    counts.put(argument, newCount);
                    changePopulation(population, newCount, 1);
                }
            }
            return answers;
        }

        private static void changePopulation(
                Map<Integer, Integer> population, int frequency, int delta) {
            if (frequency == 0) {
                return;
            }
            int newPopulation = population.getOrDefault(frequency, 0) + delta;
            if (newPopulation == 0) {
                population.remove(frequency);
            } else {
                population.put(frequency, newPopulation);
            }
        }

        public static void main(String[] args) {
            System.out.println(processQueries(new int[][] {
                {1, 7}, {1, 7}, {1, 9}, {3, 2},
                {2, 7}, {3, 2}, {3, 1}
            }));
            System.out.println(processQueries(new int[][] {
                {2, 4}, {3, 1}, {1, 4}, {2, 4}, {3, 1}
            }));
        }
    }
    ```

    실행 시 `[1, 0, 1]`, `[0, 0]`이 각각 한 줄에 출력된다.

    **복잡도:** 연산 수가 `q`이면 해시 맵 연산이 평균 `O(1)`이라는 가정에서 전체 기대 시간은 `O(q)`이다. 동시에 저장되는 서로 다른 알림 번호 수의 최댓값이 `d`, 조회 연산 수가 `r`이면 결과 리스트를 포함한 추가 공간은 `O(d + r)`이다. 서로 다른 양의 발생 횟수의 개수는 `d`를 넘지 않는다.

    **직접 확인할 경계조건:** 빈 연산 배열, 조회만 있는 경우, 없는 번호를 반복 제거, 마지막 한 개를 제거, 서로 다른 여러 번호가 같은 횟수를 갖는 경우, 연산 수보다 큰 빈도 조회. 조회마다 `counts.values()` 전체를 순회하면 연산 수와 번호 수가 모두 클 때 느려질 수 있다.

## 3일차 정렬과 두 포인터

<a id="exercise-05"></a>

### 05. 실습용 센서 구매하기

#### 문제

메이커 모임에서 실습용 센서를 구매하려고 한다. 구매 후보 목록에는 센서마다 가격이 하나씩 적혀 있으며, 각 센서는 한 번만 구매할 수 있다. 가격이 같은 센서도 서로 다른 물품으로 취급한다.

주어진 예산을 넘지 않으면서 구매할 수 있는 센서 개수의 최댓값을 반환하라. 센서의 성능이나 종류는 고려하지 않는다.

#### 제약과 함수 계약

- 센서 개수 `n`은 `0` 이상 `100,000` 이하이다.
- 각 가격은 `1` 이상 `1,000,000,000,000` 이하이다.
- 예산은 `0` 이상 `1,000,000,000,000,000` 이하이다.
- 가격 배열은 `null`이 아니며, 같은 가격이 여러 번 등장할 수 있다.
- 호출자가 전달한 가격 배열의 내용과 순서를 변경하면 안 된다.
- 함수: `public static int maxItems(long[] prices, long budget)`
- 반환값: 총가격이 `budget` 이하인 구매 조합 중 가장 많은 물품의 개수다. 구매하지 못하면 `0`을 반환한다.

#### 예제

| 구분 | 가격 목록 | 예산 | 반환값 |
| --- | --- | ---: | ---: |
| 예제 1 | `[27, 13, 45, 13, 8]` | `50` | `3` |
| 예제 2 | `[5, 12]` | `0` | `0` |

예제 1에서는 가격이 `8`, `13`, `13`인 센서 세 개를 구매할 수 있다. 총가격은 `34`다. 가장 저렴한 네 개의 총가격도 `61`이므로 네 개를 구매하는 방법은 없다.

??? success "정답과 Java 풀이 펼치기"

    **접근**

    같은 개수의 물품을 살 때는 가격이 낮은 물품부터 선택하는 조합이 총가격을 가장 작게 만든다. 따라서 가격을 오름차순으로 정렬한 뒤, 남은 예산으로 살 수 있는 동안 하나씩 구매하면 된다.

    현재 가격이 남은 예산보다 크다면 이후 가격도 모두 더 크거나 같으므로 탐색을 끝낼 수 있다. 원본 배열을 보존하기 위해 복사본을 정렬한다. 가격과 남은 예산은 `long`으로 계산한다.

    **완전한 Java 코드**

    ```java
    import java.util.Arrays;

    public class Exercise05 {
        public static int maxItems(long[] prices, long budget) {
            long[] sorted = Arrays.copyOf(prices, prices.length);
            Arrays.sort(sorted);

            long remaining = budget;
            int count = 0;

            for (long price : sorted) {
                if (price > remaining) {
                    break;
                }
                remaining -= price;
                count++;
            }

            return count;
        }

        public static void main(String[] args) {
            System.out.println(maxItems(new long[] {27, 13, 45, 13, 8}, 50));
            System.out.println(maxItems(new long[] {5, 12}, 0));
        }
    }
    ```

    예제 실행 시 기대 출력:

    ```text
    3
    0
    ```

    **복잡도**

    - 시간: 정렬 `O(n log n)`, 순회 `O(n)`으로 전체 `O(n log n)`이다.
    - 추가 공간: 배열 복사에 `O(n)`을 사용한다.

    **경계 조건**

    - 빈 목록이면 `0`을 반환한다.
    - 예산이 `0`이거나 가장 저렴한 물품도 살 수 없으면 `0`이다.
    - 가격이 같은 물품도 각각 하나씩 구매할 수 있다.
    - 가격이 남은 예산과 정확히 같으면 해당 물품을 구매한다.
    - 예산과 가격이 `int` 범위를 넘을 수 있으므로 `long`을 사용한다.

<a id="exercise-06"></a>

### 06. 일정 간격으로 떨어진 측정값 찾기

#### 문제

가상의 센서에서 얻은 정수 측정값 목록이 있다. 목록의 측정값은 모두 서로 다르다. 이 중 두 값을 골랐을 때, 큰 값에서 작은 값을 뺀 차이가 정확히 `k`가 되는 값 쌍의 개수를 구하라.

두 값의 순서만 바뀐 경우는 같은 쌍이다. 예를 들어 `(3, 9)`와 `(9, 3)`은 한 쌍으로 센다. 하나의 값이 여러 쌍에 포함되는 것은 허용한다.

#### 제약과 함수 계약

- 값의 개수 `n`은 `0` 이상 `200,000` 이하이다.
- 각 값은 `0` 이상 `1,000,000,000,000` 이하이다.
- `k`는 `1` 이상 `1,000,000,000,000` 이하이다.
- 배열은 `null`이 아니며, 모든 원소가 서로 다르다.
- 호출자가 전달한 배열의 내용과 순서를 변경하면 안 된다.
- 함수: `public static long countPairs(long[] values, long k)`
- 반환값: 차이가 `k`인 서로 다른 값 쌍의 개수다. 해당하는 쌍이 없으면 `0`을 반환한다.

#### 예제

| 구분 | 값 목록 | `k` | 반환값 |
| --- | --- | ---: | ---: |
| 예제 1 | `[24, 9, 18, 3, 15]` | `6` | `3` |
| 예제 2 | `[0, 1000000000000]` | `1000000000000` | `1` |

예제 1의 쌍은 `(3, 9)`, `(9, 15)`, `(18, 24)`이다. 값 `9`는 두 쌍에 포함되지만, 각각 다른 두 값을 고른 결과이므로 두 쌍 모두 센다.

??? success "정답과 Java 풀이 펼치기"

    **접근**

    복사한 배열을 오름차순으로 정렬하고, 작은 값을 가리키는 `left`와 큰 값을 가리키는 `right`를 둔다.

    - 두 값의 차이가 `k`보다 작으면 더 큰 값이 필요하므로 `right`를 이동한다.
    - 차이가 `k`보다 크면 작은 값을 키워야 하므로 `left`를 이동한다.
    - 차이가 정확히 `k`이면 개수를 늘리고 두 포인터를 모두 이동한다.

    모든 값이 서로 다르므로 차이가 일치한 작은 값이나 큰 값으로 같은 차이의 다른 쌍을 만들 수 없다. 두 포인터를 이동한 뒤에도 값 하나가 다른 쌍의 반대쪽 값으로 다시 사용될 수 있다. 두 포인터가 같은 원소를 가리키면 `right`를 한 칸 이동한다.

    **완전한 Java 코드**

    ```java
    import java.util.Arrays;

    public class Exercise06 {
        public static long countPairs(long[] values, long k) {
            long[] sorted = Arrays.copyOf(values, values.length);
            Arrays.sort(sorted);

            int left = 0;
            int right = 1;
            long count = 0;

            while (right < sorted.length) {
                if (left == right) {
                    right++;
                    continue;
                }

                long difference = sorted[right] - sorted[left];
                if (difference < k) {
                    right++;
                } else if (difference > k) {
                    left++;
                } else {
                    count++;
                    left++;
                    right++;
                }
            }

            return count;
        }

        public static void main(String[] args) {
            System.out.println(countPairs(new long[] {24, 9, 18, 3, 15}, 6));
            System.out.println(countPairs(
                    new long[] {0, 1_000_000_000_000L}, 1_000_000_000_000L));
        }
    }
    ```

    예제 실행 시 기대 출력:

    ```text
    3
    1
    ```

    **복잡도**

    - 시간: 정렬 `O(n log n)`, 두 포인터 순회 `O(n)`으로 전체 `O(n log n)`이다.
    - 추가 공간: 배열 복사에 `O(n)`을 사용한다.

    **경계 조건**

    - 값이 없거나 하나뿐이면 쌍을 만들 수 없으므로 `0`이다.
    - 두 값의 차이가 `k`보다 크거나 작기만 하면 `0`이다.
    - 입력 순서는 결과에 영향을 주지 않는다.
    - `k`는 양수이므로 같은 원소를 두 번 선택할 수 없다.
    - 큰 측정값과 차이 계산에 `long`을 사용한다. 반환형도 함수 계약에 따라 `long`이다.

## 4일차 너비 우선 탐색

<a id="exercise-07"></a>

### 07. 창고 구역 사이의 최소 이동 횟수

#### 문제

한 물류 창고에는 `1`부터 `n`까지 번호가 붙은 구역이 있다. 통로 하나는 두 구역을 연결하며, 양방향으로 이동할 수 있다. 어느 통로든 한 번 지나는 비용은 이동 `1`회로 같다.

시작 구역에서 각 구역까지 가는 데 필요한 최소 이동 횟수를 구하라. 이동할 수 없는 구역은 `-1`로 표시한다. 같은 통로가 목록에 여러 번 등장하거나, 한 구역에서 자기 자신으로 연결되는 통로가 있어도 결과를 올바르게 계산해야 한다.

#### 제약과 함수 계약

- 구역 수 `n`은 `1` 이상 `200,000` 이하이다.
- 통로 수 `m`은 `0` 이상 `200,000` 이하이다.
- `edges`는 `null`이 아니며, 각 원소는 두 정점 번호를 담은 길이 `2`의 배열이다.
- 모든 정점 번호와 시작점 `start`는 `1` 이상 `n` 이하이다.
- 중복 간선과 자기 자신으로 연결되는 간선을 허용한다.
- 함수: `public static int[] distances(int n, int[][] edges, int start)`
- 반환값은 길이가 `n + 1`인 배열이다. 인덱스 `v`에는 구역 `v`까지의 최소 이동 횟수를 저장한다.
- 사용하지 않는 인덱스 `0`은 `-1`, 시작점의 거리는 `0`, 도달할 수 없는 구역의 거리는 `-1`이다.

#### 예제

| 구분 | `n` | 통로 목록 | 시작점 | 반환 배열 |
| --- | ---: | --- | ---: | --- |
| 예제 1 | `7` | `[[1,2], [1,4], [2,3], [4,5], [5,3], [6,7]]` | `1` | `[-1, 0, 1, 2, 1, 2, -1, -1]` |
| 예제 2 | `4` | `[[2,2], [2,3], [2,3]]` | `2` | `[-1, -1, 0, 1, -1]` |

예제 1에서 `3`번 구역은 `1 → 2 → 3`으로 이동하면 두 번 만에 도착한다. `6`, `7`번 구역은 시작점과 연결되어 있지 않는다. 예제 2에서 자기 자신으로 가는 통로와 중복 통로는 최소 거리를 바꾸지 않는다.

??? success "정답과 Java 풀이 펼치기"

    **접근**

    모든 통로의 이동 비용이 같으므로 너비 우선 탐색(BFS)을 사용한다. 시작점에서 가까운 구역부터 큐에서 꺼내며, 아직 발견하지 않은 이웃의 거리를 `현재 거리 + 1`로 기록한다.

    구역을 큐에 넣을 때 거리를 기록하면 방문 여부도 함께 관리할 수 있다. 같은 구역을 다시 큐에 넣지 않으므로 중복 간선이나 자기 자신으로 가는 간선이 있어도 반복 탐색하지 않는다. 정점 수가 크므로 모든 구역 쌍을 저장하는 인접 행렬 대신 인접 리스트를 사용한다.

    **완전한 Java 코드**

    ```java
    import java.util.ArrayDeque;
    import java.util.ArrayList;
    import java.util.Arrays;
    import java.util.List;

    public class Exercise07 {
        public static int[] distances(int n, int[][] edges, int start) {
            List<List<Integer>> graph = new ArrayList<>(n + 1);
            for (int vertex = 0; vertex <= n; vertex++) {
                graph.add(new ArrayList<Integer>());
            }

            for (int[] edge : edges) {
                int from = edge[0];
                int to = edge[1];
                graph.get(from).add(to);
                graph.get(to).add(from);
            }

            int[] distance = new int[n + 1];
            Arrays.fill(distance, -1);
            ArrayDeque<Integer> queue = new ArrayDeque<>();
            distance[start] = 0;
            queue.addLast(start);

            while (!queue.isEmpty()) {
                int current = queue.removeFirst();
                for (int next : graph.get(current)) {
                    if (distance[next] != -1) {
                        continue;
                    }
                    distance[next] = distance[current] + 1;
                    queue.addLast(next);
                }
            }

            return distance;
        }

        public static void main(String[] args) {
            int[][] firstEdges = {
                {1, 2}, {1, 4}, {2, 3}, {4, 5}, {5, 3}, {6, 7}
            };
            int[][] secondEdges = {{2, 2}, {2, 3}, {2, 3}};

            System.out.println(Arrays.toString(distances(7, firstEdges, 1)));
            System.out.println(Arrays.toString(distances(4, secondEdges, 2)));
        }
    }
    ```

    예제 실행 시 기대 출력:

    ```text
    [-1, 0, 1, 2, 1, 2, -1, -1]
    [-1, -1, 0, 1, -1]
    ```

    **복잡도**

    - 시간: 인접 리스트 생성과 BFS를 합해 `O(n + m)`이다.
    - 추가 공간: 인접 리스트, 거리 배열, 큐를 합해 `O(n + m)`이다.

    **경계 조건**

    - 정점이 하나이고 통로가 없으면 반환값은 `[-1, 0]`이다.
    - 통로가 없어도 시작점의 거리는 `0`이다.
    - 시작점과 분리된 구역은 `-1`로 남는다.
    - 중복 간선과 자기 루프는 이미 거리를 기록한 정점을 다시 방문하지 않는다.
    - 최단 거리의 최댓값은 `n - 1`이므로 주어진 제약에서는 `int`로 표현할 수 있다.

## 5일차 구간 합과 최소 힙

<a id="exercise-08"></a>

### 08. 연속 측정 구간의 합 확인하기

#### 문제

장비의 상태 변화를 정수 배열 `values`에 시간순으로 기록했다. 양수는 증가량, 음수는 감소량을 뜻한다.

서로 이웃한 측정값을 정확히 `width`개씩 묶었을 때, 합이 `target`과 같은 구간이 몇 개인지 구하라. 시작 위치가 다르면 다른 구간이며, 구간끼리 겹쳐도 된다. 배열이 `width`보다 짧으면 가능한 구간이 없으므로 `0`을 반환한다.

#### 함수 계약과 제약

```java
public static long countWindows(long[] values, int width, long target)
```

- `values`는 `null`이 아니다.
- `0 <= values.length <= 200_000`
- 각 원소: `-1_000_000_000 <= values[i] <= 1_000_000_000`
- `1 <= width <= 200_000`
- `-1_000_000_000_000_000 <= target <= 1_000_000_000_000_000`
- 반환값: 조건을 만족하는 고정 길이 구간의 개수. 입력 배열을 변경하지 않는다.

#### 예시 1

```text
values = [2, -2, 2, -2, 2]
width = 3
target = 2
반환값 = 2
```

길이 3인 구간들의 합은 순서대로 `2`, `-2`, `2`다. 첫 번째 구간과 세 번째 구간이 조건을 만족한다.

#### 예시 2

```text
values = [7, -3]
width = 3
target = 4
반환값 = 0
```

배열 길이가 2이므로 길이 3인 구간을 만들 수 없다. 배열 전체의 합이 목표값과 같아도 세지 않는다.

??? success "정답과 Java 풀이 펼치기"

    **접근**

    첫 구간의 합을 구한 뒤, 창을 한 칸씩 옮긴다. 이전 구간에서 빠지는 값을 빼고 새로 들어오는 값을 더하면 다음 구간의 합을 구할 수 있다.

    예시 1에서는 첫 합 `2`에서 앞의 `2`를 빼고 뒤의 `-2`를 더해 다음 합 `-2`를 얻는다. 각 시작 위치의 합을 정확히 한 번 비교하므로 겹치는 구간도 빠뜨리지 않는다.

    이 문제는 구간 길이가 고정돼 있어 음수가 있어도 같은 방식으로 처리할 수 있다. 합이 목표보다 크거나 작다는 이유로 구간 길이를 늘이거나 줄일 필요가 없다.

    **Java 8 코드**

    ```java
    public class Exercise08 {
        public static long countWindows(long[] values, int width, long target) {
            if (values.length < width) {
                return 0L;
            }

            long sum = 0L;
            for (int i = 0; i < width; i++) {
                sum += values[i];
            }

            long count = sum == target ? 1L : 0L;
            for (int end = width; end < values.length; end++) {
                sum -= values[end - width];
                sum += values[end];
                if (sum == target) {
                    count++;
                }
            }
            return count;
        }

        public static void main(String[] args) {
            System.out.println(countWindows(new long[] {2, -2, 2, -2, 2}, 3, 2L));
            System.out.println(countWindows(new long[] {7, -3}, 3, 4L));
        }
    }
    ```

    예시 실행 시 기대 출력:

    ```text
    2
    0
    ```

    **복잡도와 경계 조건**

    - 시간: `O(n)`. 각 값은 처음 합을 만들거나 창을 옮길 때 상수 횟수만 사용한다.
    - 추가 공간: `O(1)`.
    - 빈 배열과 `width > n`은 `0`이다. `width == n`이면 배열 전체를 한 번만 비교한다.
    - `width == 1`, 모든 값이 `0`인 경우, 음수 목표값과 겹치는 정답 구간도 같은 로직으로 처리한다.
    - 구간 합의 절댓값은 최대 `200_000 × 1_000_000_000 = 200_000_000_000_000`이다. `int` 범위를 넘을 수 있으므로 합과 목표값에 `long`을 사용한다.

<a id="exercise-09"></a>

### 09. 보정 모듈의 점수 끌어올리기

#### 문제

실험용 보정 모듈마다 0 이상의 정수 점수가 있다. 모든 모듈의 점수가 기준 `threshold` 이상이 될 때까지 다음 절차를 반복한다.

1. 현재 점수가 가장 낮은 모듈 두 개를 선택한다. 두 점수를 `a`, `b`라고 할 때 `a <= b`다.
2. 두 모듈을 제거하고, 점수가 `a + 2 * b`인 새 모듈 한 개를 넣는다.

절차에 따라 필요한 결합 횟수를 구하라. 이미 모든 모듈이 기준을 만족하면 `0`, 모듈이 한 개만 남아 더 결합할 수 없는데도 기준을 만족하지 못하면 `-1`을 반환한다. 처음부터 모듈이 없으면 `0`을 반환한다.

#### 함수 계약과 제약

```java
public static int minimumMerges(long[] values, long threshold)
```

- `values`는 `null`이 아니다.
- `0 <= values.length <= 200_000`
- 각 원소: `0 <= values[i] <= 1_000_000_000`
- `0 <= threshold <= 1_000_000_000`
- 반환값: 기준을 만족할 때까지의 결합 횟수. 불가능하면 `-1`. 입력 배열을 변경하지 않는다.
- 점수가 같다면 어느 모듈을 먼저 선택해도 된다.

#### 예시 1

```text
values = [2, 4, 9, 16]
threshold = 10
반환값 = 2
```

첫 결합은 `2 + 2 × 4 = 10`이다. 남은 점수는 `[9, 10, 16]`이다. 다음 결합은 `9 + 2 × 10 = 29`이고, 남은 `[16, 29]`는 모두 기준을 만족한다.

#### 예시 2

```text
values = [0, 0]
threshold = 1
반환값 = -1
```

두 모듈을 합쳐도 점수는 `0`이다. 모듈이 한 개만 남아 기준을 달성할 수 없다.

??? success "정답과 Java 풀이 펼치기"

    **접근**

    매번 가장 작은 두 값을 꺼내야 하므로 최소 힙인 `PriorityQueue<Long>`을 사용한다. 입력값을 모두 힙에 넣고, 최솟값이 기준보다 작은 동안 두 값을 꺼내 결합한 뒤 다시 넣는다.

    최솟값이 기준 이상이면 나머지 값도 모두 기준 이상이다. 최솟값이 기준 미만인데 힙 크기가 1이라면 더 결합할 수 없으므로 실패다. 두 번째로 작은 값은 이미 기준 이상일 수도 있으며, 이때도 문제의 규칙에 따라 결합한다.

    **Java 8 코드**

    ```java
    import java.util.PriorityQueue;

    public class Exercise09 {
        public static int minimumMerges(long[] values, long threshold) {
            if (values.length == 0) {
                return 0;
            }

            PriorityQueue<Long> scores = new PriorityQueue<Long>();
            for (long value : values) {
                scores.offer(value);
            }

            int merges = 0;
            while (scores.peek() < threshold) {
                if (scores.size() < 2) {
                    return -1;
                }

                long smallest = scores.poll();
                long secondSmallest = scores.poll();
                scores.offer(smallest + 2L * secondSmallest);
                merges++;
            }
            return merges;
        }

        public static void main(String[] args) {
            System.out.println(minimumMerges(new long[] {2, 4, 9, 16}, 10L));
            System.out.println(minimumMerges(new long[] {0, 0}, 1L));
        }
    }
    ```

    예시 실행 시 기대 출력:

    ```text
    2
    -1
    ```

    **복잡도와 경계 조건**

    - 시간: `O(n log n)`. 위 코드는 원소를 하나씩 삽입하며, 결합은 최대 `n - 1`번 수행한다.
    - 추가 공간: `O(n)`.
    - 빈 배열은 `0`, `threshold == 0`이면 모든 입력값이 0 이상이므로 `0`이다.
    - 원소가 하나라면 그 값이 기준 이상일 때 `0`, 미만일 때 `-1`이다.
    - 점수가 같은 모듈, 점수가 `0`인 모듈도 처리한다. 결합마다 힙 크기가 1 줄어들므로 점수가 증가하지 않아도 반복은 끝난다.
    - 결합값은 `int`를 넘을 수 있으므로 `long`을 사용한다. 반복 중 가장 작은 값은 항상 기준 미만이다. 두 번째 값도 기준 미만이면 새 값은 `3_000_000_000` 미만이다. 두 번째 값이 이미 기준 이상이면 해당 결합 직후 모든 값이 기준 이상이 되어 반복이 끝난다. 이 마지막 결합의 두 번째 값은 초기값인 `1_000_000_000` 이하이거나 앞서 생성한 `3_000_000_000` 미만의 값이므로, 마지막 결합값도 `7_000_000_000` 미만이다. 이 제약에서는 `long` 범위 안에서 계산할 수 있다.
