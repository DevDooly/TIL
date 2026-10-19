# Gemini 4 Argon 추론 단계(Low · Medium · High) 성능 및 비용 비교

`gemini-4-argon`은 응답을 생성하기 전에 내부 추론(Thought) 과정을 거치는 추론 중심 모델이다. 추론 기능을 완전히 끌 수는 없으며, `thinking_level` 파라미터를 `low`(최저), `medium`(중간, 기본값), `high`(최고) 세 단계로 조절해 추론 깊이와 응답 속도, 토큰 소비량을 제어한다.

클라이언트나 게이트웨이에 따라 노출되는 옵션 이름이 다를 수 있다. Google GenAI SDK의 Interactions API에서는 `thinking_level`을 사용하고, OpenAI 호환 엔드포인트에서는 `reasoning_effort`를 사용한다. Cursor 등 일부 도구에서 제공하는 `minimal` 옵션은 Argon 모델에서 `low`와 동일하게 매핑된다.

## 추론 단계별 동작과 선택 기준

세 단계는 같은 모델 가중치를 공유하지만, 최종 답변을 내기 전 내부적으로 생성하는 추론 토큰(`total_thought_tokens`)의 예산과 탐색 깊이에서 차이가 난다.

| 추론 단계 (`thinking_level`) | 추론 토큰 소비량 | 첫 토큰 응답 지연 (TTFT) | 품질 및 동작 특성 | 권장 작업 |
| :--- | :--- | :--- | :--- | :--- |
| `low` (최저) | 최소 | 가장 빠름 | 추론 과정을 최소화해 빠르게 응답한다. 복잡한 논리나 다단계 문제에서는 정확도가 떨어질 수 있다. | 단순 분류·라우팅, 정형 데이터 추출, 짧은 질의응답, 비용·지연 시간에 민감한 요청 |
| `medium` (중간, **기본값**) | 균형 | 보통 | 속도와 첫 시도 정확도(First-pass accuracy) 사이의 균형을 맞춘 설정이다. | 일반적인 소프트웨어 개발, 대화형 코딩 에이전트, 멀티턴 도구 호출(Function Calling) |
| `high` (최고) | 최대 | 가장 느림 | 다각도 검증과 긴 추론 체인을 생성한다. 64K 이상의 출력이 필요한 경우 Long Decode와 함께 사용한다. | 대규모 코드베이스 마이그레이션, 동시성·메모리 버그 근본 원인 분석, 보안 취약점 패치, 수학·과학 증명 |

Google 공식 가이드는 작업에 맞는 단계를 고를 때 보유한 평가 데이터셋을 `low`, `medium`, `high` 세 단계로 모두 실행해 본 뒤, 목표 품질 기준을 통과하는 가장 낮은 단계를 선택하도록 안내한다.

## 기본값(`medium`)과 공개 벤치마크(`high`)의 차이

`gemini-4-argon`의 공개 벤치마크 점수를 해석할 때 가장 주의해야 할 점은 **API 기본값은 `medium`이지만, 발표된 주요 벤치마크는 모두 `high`에서 측정되었다**는 사실이다.

Google의 공식 발표와 외부 평가 기관(Artificial Analysis, Vals AI)의 측정치에서 확인된 `high` 기준 주요 성능은 다음과 같다.

- **DeepSWE v1.1**: 77.9% (장기 실행 소프트웨어 엔지니어링 과제)
- **CWE-bench v1**: 68.0% (보안 취약점 분석 및 패치 생성)
- **AutomationBench**: 51.3% (비즈니스 워크플로우 엔드투엔드 자동화)
- **LVBench**: 91.7% (장시간 비디오 문맥 이해)

현재 Google이나 외부 평가 기관 모두 `low`와 `medium` 단계에서의 벤치마크 점수 변화를 별도 수치로 공개하지 않았다. 따라서 API 요청이나 에이전트 설정에서 `thinking_level`을 생략하면 기본값인 `medium`으로 실행되며, 이는 벤치마크 표에 적힌 `high` 설정보다 한 단계 낮은 추론 예산으로 동작한다.

일반적인 코드 작성이나 파일 탐색·수정이 반복되는 에이전트 루프에서는 `medium`이 지연 시간과 비용 면에서 유리하다. 반면 단일 프롬프트로 복잡한 아키텍처 결정을 내리거나 재현이 까다로운 버그를 추적할 때는 명시적으로 `high`로 올려야 모델의 최대 추론 성능을 끌어낼 수 있다.

## `high` 단계의 지연 시간과 토큰 비용

추론 토큰(`total_thought_tokens`)은 API 응답 본문에 전문이 노출되지 않고 요약(`summary`)만 반환되더라도, 과금 시에는 **출력 토큰과 동일한 단가**로 계산된다.

- **입력 토큰**: 100만 토큰당 $2.00 (2026년 12월 1일부터 $4.00)
- **암묵적 캐시(Implicit Cache) 적중 입력 토큰**: 100만 토큰당 $0.10, 기본 입력 단가의 95% 할인 (2026년 12월 1일부터 $0.20)
- **출력 토큰(추론 토큰 포함)**: 100만 토큰당 $10.00 (2026년 12월 1일부터 $20.00)

Artificial Analysis와 Vals AI가 `high` 설정에서 측정한 실행 지표를 보면 최고 추론 단계가 요구하는 비용과 시간을 가늠할 수 있다.

| 측정 항목 | `gemini-4-argon` (`high`) 측정치 | 비고 |
| :--- | :--- | :--- |
| 작업당 평균 출력 토큰 (추론 포함) | 약 62,000 토큰 | Artificial Analysis 지수 측정 기준 |
| 출력 생성 속도 | 초당 99.5 ~ 116.5 토큰 | Google AI Studio / Vertex AI 기준 |
| 첫 답변 토큰 도달 시간 (TTFT) | 약 45초 | 내부 추론 완료까지 대기 시간 포함 |
| 단일 고난도 과제 총 소요 시간 | 약 9 ~ 10분 (Vals Index 평균 46분 33초) | 62,000 토큰 생성 기준 (도구 호출·장기 추론 시 증가) |

`high` 단계에서는 과제 하나당 평균 62,000 토큰가량을 추론과 답변에 소비하므로, 단일 요청의 출력 비용만 약 $0.62(정식 단가 기준 약 $1.24)가 발생한다. 첫 답변 토큰이 나오기까지 약 45초가 걸리고 전체 응답 완료에 수 분이 소요되므로, 실시간 대화형 UI나 짧은 도구 호출을 수십 번 반복하는 에이전트에서 무조건 `high`를 고정하면 응답 지연과 비용이 급증한다.

## 추론 단계 설정 시 함께 조정해야 할 파라미터

### `max_output_tokens`와 빈 응답 문제

`max_output_tokens`는 추론 토큰과 최종 답변 토큰을 합산한 전체 생성 상한이다. 이 값을 낮게 설정해도 모델이 스스로 추론 과정을 압축하지는 않는다. 모델이 추론 도중 `max_output_tokens` 상한에 도달하면 생성 상태가 `incomplete`로 끝나면서 **답변 텍스트가 비어 있거나 잘린 채 반환되며, 그때까지 소비한 추론 토큰 비용은 그대로 청구된다.**

- 기존 애플리케이션에서 `max_output_tokens`를 4,096이나 8,192처럼 작게 설정해 두었다면, Argon 모델에서는 최소 `32,768` 이상(동기 호출 기본값 및 최대치인 `65,536` 권장)으로 높여야 추론 도중 끊기는 현상을 막을 수 있다.
- 토큰 소비량과 응답 시간을 줄이려면 `max_output_tokens`를 줄이는 대신 `thinking_level`을 `medium`이나 `low`로 낮춰야 한다.

### 64K 초과 추론을 위한 Long Decode

동기 호출(`background=False`)에서는 `max_output_tokens`를 최대 `65,536`까지만 지정할 수 있으며, 이를 초과하면 HTTP 400 오류가 발생한다. `high` 단계에서 난도가 높은 수학 증명이나 대규모 코드 생성을 수행해 추론과 출력을 합쳐 64K 토큰을 넘겨야 한다면, Interactions API에서 `background=True`와 함께 `max_output_tokens`를 `131,072` 또는 `262,144`(최대 `1,048,576 - 입력 토큰`)로 설정해 Long Decode를 활성화한다.

### 샘플링 파라미터 무시와 캐시 유지

- `gemini-4-argon`에서는 `temperature`, `top_p`, `top_k` 파라미터가 동작하지 않고 무시된다. 출력의 일관성이나 탐색 깊이는 샘플링 파라미터가 아니라 `thinking_level`로 조절한다.
- 토큰 수로 추론 예산을 직접 지정하던 이전 세대의 `thinking_budget` 설정 방식 대신 `thinking_level`을 사용한다.
- 4,096 토큰 이상의 프롬프트에는 별도 설정 없이 암묵적 캐싱(Implicit Caching, 95% 할인)이 적용된다. 멀티턴 대화 도중 매 턴마다 `thinking_level`을 변경하면 요청 파라미터가 달라져 캐시 적중이 깨질 수 있으므로, 한 세션 안에서는 동일한 추론 단계를 유지하는 편이 비용에 유리하다.

## API 호출 예제

아래 예제는 Python `google-genai` SDK(`2.0.0` 이상)의 Interactions API를 사용해 `thinking_level`을 지정하고, 응답 후 실제 소비된 추론 토큰(`total_thought_tokens`)과 답변 출력 토큰(`total_output_tokens`)을 확인하는 코드다. 실행하려면 `GEMINI_API_KEY` 환경 변수가 설정되어 있어야 한다.

```python
from google import genai

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-4-argon",
    input=(
        "결제 재시도 파이프라인에서 발생할 수 있는 경쟁 상태(Race Condition)를 분석하고, "
        "멱등성 키와 분산 락을 적용한 수정안을 제시해 줘."
    ),
    generation_config={
        "thinking_level": "medium",  # "low" | "medium" (기본값) | "high"
        "max_output_tokens": 32768,  # 추론 토큰 + 출력 토큰 합산 상한
        "thinking_summaries": "auto",
    },
)

for step in interaction.steps:
    if step.type == "thought" and step.summary:
        for block in step.summary:
            if block.type == "text":
                print(f"[추론 요약]\n{block.text}\n")

print(f"[최종 답변]\n{interaction.output_text}\n")

if interaction.usage:
    print("추론 토큰:", interaction.usage.total_thought_tokens)
    print("출력 토큰:", interaction.usage.total_output_tokens)
```

OpenAI 호환 엔드포인트를 사용하는 경우에는 `reasoning_effort`에 `"low"`, `"medium"`, `"high"`를 전달한다.

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key="YOUR_GEMINI_API_KEY",
)

response = client.chat.completions.create(
    model="gemini-4-argon",
    reasoning_effort="high",  # "low" | "medium" | "high"
    max_tokens=65536,
    messages=[
        {"role": "user", "content": "이 C++ 파서의 메모리 누수 가능 경로를 모두 찾아 수정해 줘."}
    ],
)
```

## 관련 문서 및 참고 자료

- 내부 문서
  - [Antigravity CLI 설정](Antigravity_CLI_Configuration.md)
  - [Antigravity CLI 스킬 및 확장 가이드](Antigravity_CLI_Skills_Guide.md)
  - [Gemini CLI](Gemini_CLI.md)
- 공식 문서 및 참고 자료
  - [Google AI for Developers - What's new in Gemini 4 Argon](https://ai.google.dev/gemini-api/docs/latest-model)
  - [Google AI for Developers - Gemini 4 Argon Model Page](https://ai.google.dev/gemini-api/docs/models/gemini-4-argon)
  - [Google AI for Developers - Gemini Thinking Guide](https://ai.google.dev/gemini-api/docs/thinking)
  - [Google AI for Developers - Long Decode Guide](https://ai.google.dev/gemini-api/docs/long-decode)
  - [Google Official Blog - Introducing Gemini 4 Argon](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/)
  - [Cursor Docs - Gemini 4 Argon Effort Levels](https://cursor.com/docs/models/gemini-4-argon)
