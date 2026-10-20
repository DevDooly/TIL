# TypeSafe AI Jev (`jev.`): 비생성형 인공지능 의사결정 모델(System One Model)

**Jev**(또는 `jev.`)는 2026년 9월 15일 샌프란시스코 기반 AI 스타트업 **TypeSafe AI**(Diogo Almeida, Erik Gafni, Sasha Sheng 공동 창업)가 공개한 **의사결정 전용 인공지능 모델(System One Model)**이다. 기존 대형 언어 모델(LLM)처럼 자연어 텍스트를 한 토큰씩 순차 생성(Autoregressive Generation)하지 않고, 애플리케이션 상태(텍스트·JSON·로그)와 타입이 지정된 질문들을 입력받아 **단 한 번의 병렬 패스(Single Parallel Pass)로 분류·점수·확률 분포를 반환**한다.

## 등장 배경: System 1 vs System 2와 제번스의 역설(Jevons Paradox)

TypeSafe AI는 대니얼 카너먼(Daniel Kahneman)의 행동경제학 프레임워크에서 모델 카테고리의 이름을 가져왔다.

- **System 2 모델 (기존 생성형 LLM)**: GPT, Claude, Gemini처럼 긴 추론 체인(Chain-of-Thought)과 에세이·코드 생성을 수행하는 느리고 무거운 모델이다.
- **System 1 모델 (`Jev`)**: 소프트웨어 파이프라인 내부에서 초당 수백~수천 번 일어나는 라우팅, 트리아지(Triage), 가드레일 판별, 의도 분류처럼 **빠르고 직관적인 판단만 수행하는 경량·고속 판별(Discriminative) 모델**이다.

모델 이름인 **Jev**는 경제학자 윌리엄 스탠리 제번스의 **제번스의 역설(Jevons Paradox)**에서 따왔다. 의사결정 1회당 비용과 지연 시간을 수십~수백 분의 일로 낮추면, 기존에는 규칙 기반(`if/else`)으로만 처리하던 모든 소프트웨어 분기문에 AI 판단을 심게 되어 전체 AI 의사결정 사용량이 폭발적으로 늘어난다는 설계 철학을 담고 있다.

## 핵심 특징과 기존 생성형 LLM과의 차이

기존 LLM으로 분류나 라우팅을 구현하려면 프롬프트로 JSON 출력을 유도한 뒤 문자열을 파싱해야 하고, 출력 토큰이 생성될 때까지 기다려야 했다. Jev는 자연어 생성 단계 자체를 제거해 이 병목을 없앴다.

| 비교 항목 | 기존 생성형 LLM (System 2) | TypeSafe AI `Jev` (System One) |
| :--- | :--- | :--- |
| **추론 방식** | 자기회귀(Autoregressive) 기반 순차 토큰 생성 | 비자기회귀(Non-Autoregressive) 단일 병렬 패스 판별 |
| **출력 형태** | 자유 형식 텍스트 또는 문자열 JSON (파싱 실패 위험 존재) | 스키마가 강제된 타입 값 + 보정된 확률 분포(Calibrated Probability) |
| **응답 지연 (Latency)** | 수백 ms ~ 수십 초 (출력 길이에 비례) | 약 70ms ~ 500ms (질문 여러 개를 한 번에 병렬 평가) |
| **학습 기법** | Next-token prediction + RLHF / 추론 강화학습 | **RLCD** (Reinforcement Learning for Calibrated Decisions) |
| **과금 구조** | 입력 토큰 + 출력(추론 포함) 토큰 과금 | 입력 토큰 중심 과금 (1M 입력 토큰당 약 $0.042, 출력 토큰 무료) |
| **주요 용도** | 코드·문서 작성, 다단계 복잡 추론, 대화형 챗봇 | 에이전트 라우팅, 고객 문의 분류, 콘텐츠 모더레이션, 실시간 랭킹·스코어링 |

특히 **RLCD(Reinforcement Learning for Calibrated Decisions)** 기법으로 학습되어, 모델이 반환하는 신뢰도(Confidence)와 확률값이 실제 정답 확률과 일치하도록 보정(Calibration)되어 있다. 개발자는 이 확률값을 코드의 임계치(`if probability > 0.95`) 조건문에 바로 사용할 수 있다.

## 3가지 핵심 의사결정 프리미티브 (Primitives)

Jev API는 자연어 답변 대신 소프트웨어 코드에서 바로 분기 처리할 수 있는 세 가지 타입 프리미티브를 제공한다. 하나의 요청에 여러 질문을 묶어 보내면 단일 패스로 동시에 평가한다.

1. **`Choice` (범주형 선택)**
   - 사전 정의된 선택지(최대 255개) 중 가장 적합한 항목을 고른다.
   - 선택된 항목(`choice`), 전체 선택지별 확률 분포(`probabilities`), 신뢰도 점수(`confidence`)를 함께 반환한다.
2. **`Score` (서열·척도 평가)**
   - 순서가 있는 기준(예: `["low", "medium", "high", "critical"]` 또는 수치 루브릭)에 따라 입력 상태를 평가해 연속적인 점수와 분포를 반환한다.
3. **`Noul` (이진 가설 검증 / Boolean 확률)**
   - 특정 명제나 조건이 참인지 거짓인지를 평가해 `0.0`~`1.0` 사이의 보정된 참(Yes/True) 확률을 반환한다.

## SDK 사용 예제 (Python · TypeScript)

다음 예제는 고객 지원 티켓 상태를 입력받아 담당 팀 라우팅(`Choice`), 고객 불만 수위(`Score`), 긴급 에스컬레이션 여부(`Noul`)를 단일 호출로 판단하는 코드다. 실행하려면 `TYPESAFE_API_KEY` 환경 변수가 필요하다.

### Python (`typesafe-sdk`)

```python
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

with TypeSafeClient() as client:
    ticket_state = {
        "message": "이번 달 구독료가 두 번 결제되었습니다. 즉시 환불 처리 부탁드립니다.",
        "account_tier": "enterprise",
    }

    response = client.system_one(
        model="jev-latest",
        state=ticket_state,
        questions={
            "routing_queue": Choice(
                instructions="이 문의를 처리할 담당 부서를 선택한다.",
                criteria={
                    "billing": "결제 오류, 이중 청구, 환불 및 구독 관련 문의",
                    "technical": "시스템 버그, 장애, API 연동 오류",
                    "general": "일반적인 제품 사용법 및 기타 피드백",
                },
            ),
            "frustration_level": Score(
                instructions="고객 메시지에 드러난 불만 및 시급성 수준을 평가한다.",
                levels=["low", "medium", "high", "critical"],
            ),
            "is_urgent_financial": Noul(
                instructions="금전적 손실이나 이중 결제로 인해 즉각적인 조치가 필요한 상태인가?",
            ),
        },
    )

    routing = response.answers["routing_queue"]
    frustration = response.answers["frustration_level"]
    urgent = response.answers["is_urgent_financial"]

    print(f"담당 부서: {routing.choice} (신뢰도: {routing.confidence:.2f})")
    print(f"불만 점수: {frustration.score}")
    print(f"긴급 금전 이슈 확률(Noul): {urgent.noul:.2f}")

    # 보정된 확률값을 이용한 결정론적 분기 처리
    if urgent.noul >= 0.90 and routing.choice == "billing":
        print("-> 결제 긴급 대응 큐로 즉시 이관합니다.")
```

### TypeScript (`@typesafe-ai/sdk`)

```typescript
import { TypeSafeClient, choice, score, noul } from "@typesafe-ai/sdk";

async function routeTicket() {
  const client = new TypeSafeClient();

  const response = await client.systemOne({
    model: "jev-latest",
    state: {
      message: "이번 달 구독료가 두 번 결제되었습니다. 즉시 환불 처리 부탁드립니다.",
      account_tier: "enterprise",
    },
    questions: {
      routing_queue: choice({
        instructions: "이 문의를 처리할 담당 부서를 선택한다.",
        criteria: {
          billing: "결제 오류, 이중 청구, 환불 및 구독 관련 문의",
          technical: "시스템 버그, 장애, API 연동 오류",
          general: "일반적인 제품 사용법 및 기타 피드백",
        },
      }),
      frustration_level: score({
        instructions: "고객 메시지에 드러난 불만 수준을 평가한다.",
        levels: ["low", "medium", "high", "critical"],
      }),
      is_urgent_financial: noul({
        instructions: "금전적 손실이나 이중 결제로 인해 즉각적인 조치가 필요한가?",
      }),
    },
  });

  if (
    response.answers.is_urgent_financial.noul >= 0.9 &&
    response.answers.routing_queue.choice === "billing"
  ) {
    console.log("결제 긴급 대응 워크플로우를 실행합니다.");
  }
}
```

## 아키텍처 적용 패턴과 주의점

- **System 1(`Jev`) + System 2(LLM) 하이브리드 파이프라인**: 모든 요청을 고비용 추론 모델(예: Gemini 4 Argon, Claude Opus 등)로 바로 보내지 않고, 앞단에서 `Jev`로 의도(`Choice`), 위험도(`Score`), 가드레일 위반 여부(`Noul`)를 100ms 이내에 먼저 판별해 단순 요청은 즉시 처리하고 복잡한 요청만 System 2 모델로 라우팅한다.
- **한계와 주의점**: `Jev`는 텍스트나 코드를 생성하지 못하는 순수 의사결정 모델이다. 요약문 작성, 번역, 코드 생성, 자유 형식의 이유 설명(Explanation Generation)이 필요한 작업에는 사용할 수 없으며, 선택지(`criteria`)와 평가 기준(`instructions`)을 명확히 정의할 수 있는 구조적 판단 문제에 한정해 적용해야 한다.

## 관련 문서 및 참고 자료

- 내부 문서
  - [AI Agent 개발 직군 및 엔지니어링 가이드](AI_Agent_Developer_Role_and_Engineering.md)
  - [Gemini 4 Argon 추론 단계(Low · Medium · High) 비교](Gemini_4_Argon_Reasoning_Levels.md)
- 외부 참고 자료
  - [InfoQ - TypeSafe AI Launches Jev, a "System One" Model for Fast, Typed Decisions](https://www.infoq.com/)
  - [LangChain Blog - Integrating TypeSafe AI's Jev for High-Speed Agent Routing](https://blog.langchain.com/)
