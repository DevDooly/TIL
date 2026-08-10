# Antigravity CLI - 자동 승인(Auto-Approve) 및 권한 설정 가이드

Antigravity CLI(`agy`) 등 터미널 기반 AI 코딩 어시스턴트를 사용할 때, **파일 생성(`write_to_file`), 파일 수정(`replace_file_content`), 명령어 실행 시 매번 사용자의 수동 동의(Y/N 확인)를 묻지 않고 즉시 수행**하도록 설정하는 방법입니다.

---

## 1. 설정 파일(`settings.json`)을 통한 영구 자동 승인

CLI의 전역 설정 파일에서 도구별 또는 작업 유형별 자동 승인 권한(Permissions)을 부여할 수 있습니다.

### 설정 파일 위치
* **Linux / macOS**: `~/.gemini/antigravity-cli/settings.json`
* **Windows**: `%USERPROFILE%\.gemini\antigravity-cli\settings.json`

### `settings.json` 설정 예시

파일 생성 및 수정 작업에 대해 확인 절차를 생략하려면 아래와 같이 설정을 추가합니다.

```json
{
  "permissions": {
    "auto_approve": [
      "write_to_file",
      "replace_file_content",
      "multi_replace_file_content",
      "list_dir",
      "view_file",
      "grep_search"
    ],
    "allow_all_file_edits": true,
    "require_confirmation_for_commands": false
  },
  "approval_mode": "auto"
}
```

> **주요 옵션 설명**:
> * `auto_approve`: 지정된 개별 도구 호출 시 승인 프롬프트를 건너뜁니다.
> * `allow_all_file_edits`: 파일 생성, 수정, 삭제 작업을 자동으로 승인합니다.
> * `approval_mode`: `"auto"` 또는 `"always_allow"`로 설정 시 모든 비위험 작업을 즉시 실행합니다.

---

## 2. CLI 실행 플래그(Flag)를 통한 즉시 실행

명령어를 실행할 때 일회성으로 모든 승인 프롬프트를 건너뛰고 바로 실행할 수 있는 플래그입니다.

```bash
# 기본 자동 승인 플래그
agy --auto-approve

# 또는 단축 플래그
agy -y
```

---

## 3. 대화 세션 내 슬래시 명령어(Slash Command) 활용

CLI 대화 세션(TUI)이 이미 시작된 상태에서 승인 모드를 동적으로 변경할 수 있습니다.

```text
> /auto-approve on
Auto-approve enabled for file operations.
```
또는
```text
> /permissions auto
```

---

## 4. 에이전트 지침서(Rule)를 통한 행동 제약 해제

설정 외에도 에이전트가 자체 판단으로 "사용자에게 매번 묻는 행동"을 하지 않도록 프로젝트 루트의 `GEMINI.md` 또는 `AGENTS.md`에 지침을 추가합니다.

```markdown
## Agent Action Guidelines
- 파일 생성 및 수정이 필요한 작업은 사용자에게 별도로 확인을 묻지 말고 즉시 도구를 실행하여 반영할 것.
- 수정 사항에 대한 결과 요약은 작업 완료 후 보고할 것.
```

---

## 5. 주요 AI 코딩 CLI 도구별 자동 승인 옵션 비교

| CLI 도구 | 실행 플래그 (Flag) | 설정 파일 (Settings) 키 |
| :--- | :--- | :--- |
| **Antigravity CLI** (`agy`) | `agy --auto-approve` / `agy -y` | `"approval_mode": "auto"` |
| **Gemini CLI** (`gemini`) | `gemini --auto-approve` | `"autoApprove": true` |
| **Claude Code** (`claude`) | `claude --dangerously-skip-permissions` | `"autoApprove": ["EditFile", "WriteFile"]` |
| **OpenCode** | `opencode --yolo` | `"yolo_mode": true` |
