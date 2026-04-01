# Ollama

Ollama는 로컬 환경에서 대규모 언어 모델(LLM)을 손쉽게 실행하고 관리할 수 있게 해주는 오픈소스 도구입니다. 복잡한 설정 없이 간단한 CLI 명령어로 Llama 3, Mistral, Gemma 등의 모델을 다운로드하고 실행할 수 있습니다.

## 1. 설치 (Installation)

### Linux & macOS
가장 간편한 설치 방법은 공식 스크립트를 사용하는 것입니다.

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Docker
Docker 컨테이너로 실행할 수도 있습니다 (GPU 가속을 위해 NVIDIA Container Toolkit 설정 필요).

```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

---

## 2. 기본 사용법 (Usage)

### 모델 실행 (Run)
모델이 없으면 자동으로 다운로드(pull) 후 실행합니다.

```bash
# Llama 3 실행
ollama run llama3

# Mistral 실행
ollama run mistral
```

### 주요 명령어

| 명령어 | 설명 | 예시 |
| :--- | :--- | :--- |
| `run` | 모델 실행 (대화형 모드) | `ollama run llama3` |
| `pull` | 모델 다운로드 (실행 X) | `ollama pull gemma` |
| `rm` | 다운로드된 모델 삭제 | `ollama rm llama3` |
| `cp` | 모델 복사 | `ollama cp llama3 my-model` |
| `list` | 설치된 모델 목록 확인 | `ollama list` |
| `serve` | API 서버 모드로 실행 | `ollama serve` |

---

## 3. 커스텀 모델 만들기 (Modelfile)

`Dockerfile`과 유사한 문법의 `Modelfile`을 작성하여, 기본 모델에 시스템 프롬프트나 파라미터를 커스터마이징할 수 있습니다.

### 작성 예시 (Mario 페르소나)

1.   `Modelfile` 생성:
```dockerfile
FROM llama3

# 시스템 프롬프트 설정
SYSTEM "You are Mario from Super Mario Bros. You answer everything as if you are in the Mushroom Kingdom."

# 파라미터 튜닝 (창의성 높이기)
PARAMETER temperature 0.8
```

2.   모델 빌드:
```bash
ollama create mario -f Modelfile
```

3.   실행:
```bash
ollama run mario
>>> Hello!
It's-a me, Mario! Welcome to the Mushroom Kingdom!
```

---

## 4. REST API 활용

Ollama는 기본적으로 `11434` 포트에서 REST API를 제공합니다. 이를 통해 애플리케이션에 LLM 기능을 쉽게 통합할 수 있습니다.

### Generate (텍스트 생성)
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Why is the sky blue?",
  "stream": false
}'
```

### Chat (대화형)
```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llama3",
  "messages": [
    { "role": "user", "content": "Hello!" }
  ],
  "stream": false
}'
```

---

## 5. 자주 쓰는 모델 목록

Ollama 라이브러리에서 다양한 모델을 찾을 수 있습니다.

-   **llama3**: Meta의 최신 오픈 모델 (8B, 70B)
-   **gemma**: Google의 경량화 모델 (2B, 7B)
-   **mistral**: 성능 좋은 7B 모델
-   **phi3**: Microsoft의 소형 모델 (3.8B)

> **Tip**: 모델 뒤에 태그를 붙여 특정 버전을 받을 수 있습니다 (예: `llama3:70b`, `gemma:2b`).
