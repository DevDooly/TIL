# 🖥️ 현재 PC (Ubuntu) Ollama 설치 및 API 설정 가이드

본 문서는 현재 사용 중인 PC의 하드웨어 사양을 기반으로 **Ollama 설치**부터 **외부 API 개방(원격 접속) 설정**까지의 과정을 정리한 가이드입니다.

## 1. 현재 PC 사양 (System Specifications)

- **OS**: Ubuntu 22.04.5 LTS
- **CPU**: AMD Ryzen 7 5700U (8 코어 / 16 스레드)
- **RAM**: 약 32GB (여유 21GB 이상)
- **GPU**: AMD Radeon Graphics (내장 그래픽, Lucienne)

### 💡 사양 분석 및 구동 예상 성능

- 넉넉한 **32GB의 RAM** 덕분에 `llama3:8b`, `gemma:7b` 같은 중소형 모델은 물론, 필요하다면 `mixtral` 같은 큰 모델도 무난하게 메모리에 올려서 실행할 수 있습니다.
- GPU가 AMD 내장 그래픽(APU)이므로, Ollama의 공식 AMD GPU 가속(ROCm)이 완벽하게 지원되지 않을 수 있습니다. 하지만 이 경우 Ollama가 자동으로 **CPU 모드**로 전환하여 실행합니다. 8코어 16스레드의 우수한 CPU와 고용량 RAM 조합이므로 CPU 모드에서도 나쁘지 않은 추론 속도를 기대할 수 있습니다.

---

## 2. Ollama 설치 (Installation)

현재 Ubuntu 환경에서는 공식 설치 스크립트를 사용하여 간편하게 설치할 수 있습니다. 터미널을 열고 다음 명령어를 실행하세요.
(설치 과정 중 `sudo` 권한을 요구할 수 있습니다.)

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

설치가 완료되면, 아래 명령어로 정상 설치 여부를 확인합니다.

```bash
ollama --version
```

---

## 3. API 원격 접속 및 CORS 설정

Ollama는 보안상의 이유로 기본적으로 로컬호스트(`127.0.0.1:11434`)에서만 API 요청을 받습니다.
만약 외부 PC, 모바일 기기, 혹은 Docker 컨테이너 내부(예: n8n)에서 현재 PC의 Ollama API에 접속하려면 **Systemd 서비스 설정**을 수정해야 합니다.

### 설정 방법

1. **Systemd 서비스 설정 수정 모드 진입**
   터미널에서 아래 명령어를 실행하여 텍스트 편집기를 엽니다.

   ```bash
   sudo systemctl edit ollama.service
   ```

2. **환경변수 추가**
   편집기가 열리면 빈 주석 공간(`### Anything between here and the comment below will become the new contents of the file`) 부분에 아래 내용을 추가합니다.
   
   - `OLLAMA_HOST="0.0.0.0"`: 모든 IP의 접속 허용.
   - `OLLAMA_ORIGINS="*"`: 웹 프론트엔드 등에서 오는 모든 CORS 요청 허용.

   ```ini
   [Service]
   Environment="OLLAMA_HOST=0.0.0.0"
   Environment="OLLAMA_ORIGINS=*"
   ```
   저장 후 편집기를 종료합니다. (`nano` 편집기 기준: `Ctrl+O` -> `Enter` -> `Ctrl+X`)

3. **서비스 재시작 적용**
   변경된 설정을 시스템에 반영하고 Ollama 데몬 서비스를 재시작합니다.

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl restart ollama
   ```

---

## 4. API 동작 확인 테스트

설정이 완료된 후, 터미널에서 정상적으로 API 응답이 오는지 확인합니다.

```bash
# 로컬호스트 테스트
curl http://localhost:11434/api/tags

# 외부 IP 접속 테스트 (IP는 'ip addr' 명령어로 확인 가능)
curl http://<현재_PC_IP주소>:11434/api/tags
```

정상적으로 설정되었다면 현재 설치된 모델 목록인 `{"models":[]}` 형태의 JSON 응답이 출력됩니다.

이후 `ollama run llama3` 등의 명령어로 원하는 모델을 다운로드받아 외부에서 API를 통해 편리하게 활용하실 수 있습니다!