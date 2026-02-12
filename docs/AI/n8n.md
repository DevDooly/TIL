# n8n (Nodemation)

**n8n**은 확장성이 뛰어난 **워크플로우 자동화 도구**입니다. 노드 기반의 시각적 인터페이스를 통해 다양한 앱과 서비스를 연결하고 복잡한 로직을 자동화할 수 있습니다. 특히 최근에는 **LangChain**, **OpenAI** 등 AI 관련 노드들을 강력하게 지원하여 **AI 에이전트의 오케스트레이터**로서 주목받고 있습니다.

## 🌟 주요 특징

*   **Node-based Interface**: 드래그 앤 드롭 방식으로 노드를 연결하여 직관적으로 워크플로우를 설계할 수 있습니다.
*   **Fair-code License**: 소스 코드가 공개되어 있으며, 내부 비즈니스 목적으로는 무료로 자체 호스팅(Self-hosted)이 가능합니다.
*   **Extensive Integrations**: 700개 이상의 서비스 연동을 지원하며, HTTP Request 노드를 통해 API가 있는 모든 서비스와 통신할 수 있습니다.
*   **AI & LLM Support**: LangChain 통합을 통해 LLM 체인, 메모리 관리, 벡터 스토어 연동 등을 노드 연결만으로 구현할 수 있습니다.

## 🤖 AI 에이전트로서의 활용

n8n은 단순한 반복 작업 자동화를 넘어, **AI 에이전트의 두뇌 역할**을 수행할 수 있습니다.

1.  **챗봇 구축**: Slack, Discord, Telegram 등과 LLM을 연동하여 지능형 챗봇을 쉽게 만들 수 있습니다.
2.  **데이터 처리 파이프라인**: 문서 요약, 감성 분석, 데이터 분류 등 AI 모델을 활용한 데이터 처리 워크플로우를 자동화합니다.
3.  **RAG (Retrieval-Augmented Generation)**: 벡터 데이터베이스(Pinecone, Weaviate 등)와 연동하여 외부 지식을 참조하는 답변 생성 시스템을 구축할 수 있습니다.

## 🚀 설치 (Docker)

Docker를 사용하여 쉽게 자체 호스팅 환경을 구축할 수 있습니다.

```bash
docker run -it --rm \
	--name n8n \
	-p 5678:5678 \
	-v ~/.n8n:/home/node/.n8n \
	docker.n8n.io/n8nio/n8n
```

설치 후 브라우저에서 `http://localhost:5678`로 접속하여 설정을 진행합니다.
