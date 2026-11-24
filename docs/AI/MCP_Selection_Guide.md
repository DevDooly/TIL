# 상황별 MCP 선택과 빠른 연결

MCP는 AI가 외부 도구를 호출하도록 연결하는 방식이다. Windows 화면을 조작할 때, Ubuntu 서버를 점검할 때, Kubernetes 배포를 살필 때 필요한 서버가 다르다. Java·Spring, SQL, 데이터 플랫폼, 배포·운영, Android 개발에 맞춰 아래 도구부터 고르면 된다.

## 작업에 맞게 고르기

별 수는 **2026-11-24 09시경 KST** GitHub API에서 조회한 각 저장소의 값이다. 사용 환경과 공식 설치 안내를 함께 확인해 선정했으며, 별 수는 계속 변한다. Context7처럼 MCP 외 CLI·Skills를 함께 제공하는 저장소도 있다.

| 하고 싶은 일 | MCP · 공식 저장소 | GitHub 별 |
| --- | --- | ---: |
| Windows 앱·설정 화면 조작 | [Windows MCP](https://github.com/CursorTouch/Windows-MCP) | 12,061 |
| Windows·Linux 파일·터미널 작업 | [Desktop Commander](https://github.com/wonderwhy-er/DesktopCommanderMCP) | 10,407 |
| SSH 키로 Ubuntu 등 원격 서버 점검 | [SSH MCP Server](https://github.com/classfang/ssh-mcp-server) | 1,070 |
| K8s·K3s 리소스·Pod 로그 확인 | [Kubernetes MCP Server](https://github.com/containers/kubernetes-mcp-server) | 2,278 |
| PR·Issue·GitHub Actions 확인 | [GitHub MCP Server](https://github.com/github/github-mcp-server) | 34,696 |
| Spring·프레임워크 문서와 버전 확인 | [Context7](https://github.com/upstash/context7) | 65,348 |
| 웹 사용자 흐름·모바일 화면 확인 | [Playwright MCP](https://github.com/microsoft/playwright-mcp) | 40,063 |
| MariaDB 등 SQL·스키마 탐색 | [DBHub](https://github.com/bytebase/dbhub) | 3,963 |
| 서비스 지표·Loki 로그 조회 | [Grafana MCP](https://github.com/grafana/mcp-grafana) | 3,695 |
| 여러 MCP를 컨테이너로 실행·관리 | [Docker MCP Gateway](https://github.com/docker/mcp-gateway) | 1,645 |
| Android 앱·에뮬레이터 UI 확인 | [Mobile MCP](https://github.com/mobile-next/mobile-mcp) | 10,829 |

## 클라이언트에 연결하는 방법

STDIO 방식은 **MCP 클라이언트를 실행하는 컴퓨터**에 Node.js·uv·Docker 같은 실행 도구가 있어야 한다. 아래 STDIO 명령을 클라이언트의 서버 설정에서 `command`와 `args`로 나눠 등록한다. 예를 들어 `npx -y @playwright/mcp@latest`라면 command는 `npx`, args는 `["-y", "@playwright/mcp@latest"]`다. Node 기반 예제는 Node **22.13 이상**으로 맞추면 아래 도구의 최소 요구 버전을 충족한다.

Node.js는 [공식 다운로드](https://nodejs.org/en/download)에서 운영체제에 맞는 LTS를 설치하고, uv는 [공식 설치 안내](https://docs.astral.sh/uv/getting-started/installation/)의 Windows 또는 Linux 명령을 사용한다.

HTTP 방식은 서버 URL을 등록하고 로그인이나 토큰 인증을 진행한다. 클라이언트마다 설정 파일 형식이 다르므로 같은 JSON을 공통으로 복사하지 않는다.

Codex CLI에서는 다음처럼 등록하고 목록을 확인한다. 설정 화면을 사용하는 클라이언트에서는 같은 명령·인자 또는 HTTP URL을 입력한 뒤 연결을 다시 시작한다. Codex 설정은 `~/.codex/config.toml`에서 관리한다. [Codex 공식 MCP 연결 안내](https://developers.openai.com/codex/mcp/)

```bash
codex mcp add playwright -- npx -y @playwright/mcp@latest
codex mcp list
```

등록 후에는 “Playwright로 이 페이지의 모바일 메뉴를 확인해줘”처럼 도구와 대상을 말하면 된다. 아래 명령은 연결 예제이며, 이 문서 작성 과정에서 각 MCP를 설치하거나 실제 서버에 연결하지는 않았다.

## Windows·Linux·Kubernetes

### Windows 화면 조작 · Windows MCP

Windows의 앱·파일 탐색기·설정 화면을 다룰 때 사용한다. **Windows 10 이상, Python 3.14 이상, uv**가 필요하다. 아래 명령의 `serve`까지 등록한다. [설치 안내](https://github.com/CursorTouch/Windows-MCP)

```powershell
uvx windows-mcp serve
```

사용 예시 — “현재 열린 앱을 확인하고 Windows 설정에서 디스플레이 배율을 찾아줘.”

### 로컬 파일·터미널 · Desktop Commander

Windows·macOS·Linux에서 파일 편집과 터미널 명령 실행을 연결한다. Node **22.12 이상**이 필요하다. Ubuntu에서 실행하면 그 Ubuntu의 파일과 셸을 다룬다. [설치 안내](https://github.com/wonderwhy-er/DesktopCommanderMCP) · [Node 요구 버전](https://github.com/wonderwhy-er/DesktopCommanderMCP/blob/main/package.json)

```bash
npx -y @wonderwhy-er/desktop-commander@latest
```

사용 예시 — “이 프로젝트의 Compose 파일과 최근 API 로그를 읽고 기동 실패 원인을 정리해줘.”

### 원격 Ubuntu 접속 · SSH MCP Server

PC에서 실행한 MCP가 기존 SSH 연결로 서버에 접속한다. **대상 서버에 MCP를 따로 설치할 필요가 없다.** Node.js, SSH 접속 경로, 로그인 계정과 개인 키가 필요하다. 다음 값은 자신의 서버와 키의 절대 경로로 바꾼다. [공식 영문 안내](https://github.com/classfang/ssh-mcp-server/blob/main/README_EN.md)

```bash
npx -y @fangjunjie/ssh-mcp-server --host SERVER_HOST --port 22 --username labadmin --privateKey /absolute/path/id_ed25519
```

Windows의 키 경로는 `C:/Users/USER/.ssh/id_ed25519`처럼 지정할 수 있다. 실행 범위는 SSH 계정 권한에 따른다. 키 내용은 설정 예제나 Git에 붙여 넣지 않는다.

사용 예시 — “이 Ubuntu의 디스크 사용량과 ssh·k3s 서비스 상태를 조회하고, 변경이 필요한 항목을 알려줘.”

### K8s·K3s 조회 · Kubernetes MCP Server

노드·워크로드·이벤트·Pod 로그를 살필 때 사용한다. 접근 가능한 클러스터의 **kubeconfig**가 필요하며, K3s도 Kubernetes API를 통해 연결한다. 현재 설정은 TOML 파일로 지정한다. [설치·설정 안내](https://github.com/containers/kubernetes-mcp-server) · [설정 항목](https://github.com/containers/kubernetes-mcp-server/blob/main/docs/configuration.md)

```bash
npx -y kubernetes-mcp-server@latest --config /absolute/path/k8s-mcp.toml
```

`k8s-mcp.toml`은 우선 조회용으로 시작한다.

```toml
read_only = true

[[denied_resources]]
group = ""
version = "v1"
kind = "Secret"
```

kubeconfig 계정의 RBAC 권한도 조회 범위로 맞춘다. Windows에서는 config 인자에 실제 Windows 절대 경로를 넣는다.

사용 예시 — “현재 context의 lab 네임스페이스에서 Ready가 아닌 Pod와 최근 이벤트·로그를 함께 확인해줘.”

대안인 [Flux159 Kubernetes MCP](https://github.com/Flux159/mcp-server-kubernetes)는 **1,616★**다. `npx -y mcp-server-kubernetes`로 등록하며 `ALLOW_ONLY_READONLY_TOOLS=true` 환경 변수로 조회 도구를 제한한다. 두 서버를 함께 등록하기보다 필요한 도구와 클라이언트 지원을 보고 하나를 고른다. [조회 모드 설명](https://github.com/Flux159/mcp-server-kubernetes/blob/main/ADVANCED_README.md#read-only-mode)

## 개발·데이터·운영

### PR·CI 확인 · GitHub MCP Server

PR·Issue·Actions를 GitHub API로 조회한다. 원격 HTTP를 지원하는 클라이언트에서 아래 URL을 등록하고 GitHub OAuth 또는 PAT로 인증한다. 인증 방식은 클라이언트 지원에 따라 고른다. [원격 서버 연결 안내](https://github.com/github/github-mcp-server)

```text
https://api.githubcopilot.com/mcp/
```

사용 예시 — “이 저장소의 최근 실패한 Actions와 해당 커밋의 변경 파일을 확인해 원인을 정리해줘.”

### 버전에 맞는 문서 · Context7

라이브러리 문서와 코드 예제를 조회한다. Java·Spring·웹 프레임워크를 수정할 때 프로젝트 버전에 맞는 근거를 찾는 데 쓰기 좋다. Node **22.13 이상**에서 설치 도우미를 실행하고 OAuth 로그인 후 MCP 연결을 선택한다. [설치 안내](https://github.com/upstash/context7)

```bash
npx ctx7 setup
```

`npx ctx7 setup`은 터미널에서 한 번 실행하는 설치 도우미다. STDIO 서버의 실행 명령으로 등록하지 않는다.

수동 HTTP 연결은 `https://mcp.context7.com/mcp`를 사용하며 API key를 `Authorization: Bearer <API_KEY>` 헤더에 지정한다.

사용 예시 — “프로젝트의 Spring Boot 버전을 먼저 읽고 Context7에서 그 버전의 설정 예제를 찾아줘.”

### 웹 화면·동작 확인 · Playwright MCP

브라우저를 열어 화면과 접근성 정보를 읽고 사용자 흐름을 확인한다. Node **20 이상**이 필요하다. [설치 안내](https://github.com/microsoft/playwright-mcp)

```bash
npx -y @playwright/mcp@latest
```

사용 예시 — “공개 데모에서 입장 후 회비 내역을 열고, 모바일 너비에서도 메뉴가 동작하는지 확인해줘.”

### MariaDB·SQL 탐색 · DBHub

MariaDB·MySQL·PostgreSQL 등 DB의 스키마와 SQL을 다룬다. Node **22.5 이상**, DB 접속 정보와 조회 계정이 필요하다. 아래 환경 변수를 MCP 프로세스에 전달하고 TOML을 절대 경로로 등록한다. [지원 DB·설치](https://github.com/bytebase/dbhub) · [TOML 설정](https://dbhub.ai/config/toml)

```bash
npx -y @bytebase/dbhub@latest --config /absolute/path/dbhub.toml
```

```toml
[[sources]]
id = "lab"
type = "mariadb"
host = "${DB_HOST}"
port = 3306
database = "${DB_NAME}"
user = "${DB_USER}"
password = "${DB_PASSWORD}"

[[tools]]
name = "execute_sql"
source = "lab"
readonly = true
max_rows = 100
```

`readonly`는 SQL 도구 설정이다. DB 계정도 SELECT 권한으로 제한하면 접속 권한과 도구 동작을 함께 맞출 수 있다.

사용 예시 — “테이블 관계를 조회하고 이 SELECT의 실행 계획에서 확인할 항목을 알려줘.”

### 서비스 지표·로그 · Grafana MCP

Grafana의 Prometheus·Loki 데이터 소스로 지표와 실제 로그를 조회한다. **Grafana 9 이상**, uv, Grafana URL과 서비스 계정 토큰, 구성된 데이터 소스가 필요하다. MCP 프로세스에 `GRAFANA_URL`과 `GRAFANA_SERVICE_ACCOUNT_TOKEN` 환경 변수를 전달한다. [연결 안내](https://github.com/grafana/mcp-grafana)

```bash
uvx mcp-grafana --disable-write
```

사용 예시 — “최근 15분 API 오류 지표가 증가한 시점과 같은 시간대 Loki 로그를 연결해줘.”

로그가 Grafana에 수집돼 있어야 조회할 수 있다. 이 MCP 설치만으로 서비스 로그 수집이 구성되지는 않는다.

### MCP 컨테이너 관리 · Docker MCP Gateway

여러 MCP를 Docker 컨테이너로 실행하고 프로필로 묶는다. Docker Desktop **4.59 이상**에서 MCP Toolkit을 활성화하고 필요한 서버를 프로필에 추가한다. 다음은 GitHub 서버를 넣는 예제로 GitHub 인증도 별도로 준비한다. [프로필·Gateway 안내](https://github.com/docker/mcp-gateway)

```bash
docker mcp catalog pull mcp/docker-mcp-catalog
docker mcp profile create --name dev-tools --server catalog://mcp/docker-mcp-catalog/github
```

카탈로그와 프로필을 준비한 뒤 아래 명령을 클라이언트의 STDIO 서버로 등록한다.

```bash
docker mcp gateway run --profile dev-tools
```

사용 예시 — “등록된 GitHub 도구로 이 저장소 PR의 상태를 확인해줘.” Gateway가 제공하는 기능은 프로필에 추가한 MCP에 따라 달라진다.

### Android 앱 확인 · Mobile MCP

Android 에뮬레이터·실기기의 화면을 읽고 탭·입력 동작을 수행한다. Node **20 이상**, Android SDK·adb와 실행 중인 에뮬레이터가 필요하다. 실기기는 USB 디버깅을 허용한다. iOS도 지원하지만 호스트 준비 조건은 별도다. [설치·기기 준비](https://github.com/mobile-next/mobile-mcp)

```bash
npx -y @mobilenext/mobile-mcp@latest
```

사용 예시 — “Slivue 테스트 빌드에서 알림 권한을 거부한 뒤 설정에서 허용하는 흐름을 확인해줘.”

## 내 프로젝트에 조합해서 적용하기

| 작업 | 함께 쓰기 좋은 도구 |
| --- | --- |
| Spring API 수정과 웹 동작 확인 | Context7으로 버전 문서 확인 → Playwright로 사용자 흐름 확인 |
| Ubuntu VM의 K3s 장애 점검 | SSH로 systemd·디스크 조회 → Kubernetes로 Pod·이벤트 확인 |
| CI/CD 배포 문제 분석 | GitHub로 Actions 확인 → Kubernetes로 Jenkins·Argo CD·앱 상태 확인 → Grafana로 지표·로그 조회 |
| MariaDB 데이터·API 문제 분석 | DBHub로 스키마·SELECT 확인 → Grafana로 API 로그 확인 |
| Kafka·MinIO·Garage·데이터 플랫폼 점검 | Kubernetes로 배포 상태 확인, SSH로 기존 관리 CLI 실행, Grafana에 수집된 지표·로그 조회 |
| Android 앱 회귀 확인 | Mobile MCP로 기기 UI 확인 → GitHub로 관련 Issue·빌드 기록 확인 |

이 조합은 공개 프로필의 기술 범위에 맞춘 사용 제안이다. 각 제품의 관리 CLI와 권한은 따로 필요하다. 예를 들어 Grafana로 Kafka 상태를 보려면 Kafka 지표가 먼저 수집돼 있어야 한다.

Kafka 전용 후보로는 [Confluent MCP](https://github.com/confluentinc/mcp-confluent) **171★**, [Aiven MCP](https://github.com/Aiven-Open/mcp-aiven) **28★**가 있다. 각각 해당 관리 서비스를 사용하는 경우에 살펴볼 후보이며, 현재 셀프 호스팅 Kafka에 그대로 연결하는 공통 도구로 가정하지 않는다.

MCP를 직접 만들고 싶다면 [MCP 서버 개발 가이드](MCP_Server_Development_Guide.md)를 이어서 보면 된다.

