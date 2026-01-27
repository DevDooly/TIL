# GitHub Actions MkDocs 배포 실패 (Plugin Missing)

## 현상
GitHub Actions를 통해 MkDocs 사이트를 `github.io`로 배포하는 과정에서 빌드가 실패함. 로그에서 다음과 같은 에러가 발생할 수 있음:

```
ConfigurationError: Config value: 'plugins'. Failed to load plugin 'awesome-pages'.
ModuleNotFoundError: No module named 'mkdocs_awesome_pages_plugin'
```

## 원인
`mkdocs.yml` 파일에는 `awesome-pages`와 같은 플러그인이 설정되어 있으나, CI/CD 파이프라인(`ci.yml`)에서 해당 플러그인을 설치하지 않아서 발생함.

기존 `ci.yml` 설정이 단순히 `mkdocs-material`만 설치하도록 되어 있을 경우, 추가 플러그인에 대한 의존성이 누락됨.

## 해결 방법
`.github/workflows/ci.yml` 파일의 의존성 설치 단계를 수정하여 `requirements.txt` 파일을 통해 모든 의존성을 설치하도록 변경해야 함.

### 수정 전
```yaml
      - name: Install dependencies
        run: pip install mkdocs-material
```

### 수정 후
```yaml
      - name: Install dependencies
        run: pip install -r requirements.txt
```

`requirements.txt` 파일에는 사용 중인 모든 플러그인이 명시되어 있어야 함 (예: `mkdocs-awesome-pages-plugin`).
