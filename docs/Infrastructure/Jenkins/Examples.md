# Jenkins 사용 예시 (Pipeline)

실무에서 가장 많이 사용되는 **Declarative Pipeline**을 이용해 GitHub 저장소의 코드를 가져와 빌드하고 테스트하는 예시를 다룹니다.

## 1. Declarative Pipeline 구조

`Jenkinsfile`이라는 파일에 빌드 절차를 정의합니다. 기본 구조는 다음과 같습니다.

```groovy
pipeline {
    agent any // 어떤 에이전트(슬레이브)에서 실행할지 정의

    stages {
        stage('Checkout') {
            steps {
                // 소스 코드 가져오기
                git 'https://github.com/your-repo/project.git'
            }
        }
        stage('Build') {
            steps {
                // 빌드 실행 (예: Gradle)
                sh './gradlew build'
            }
        }
        stage('Test') {
            steps {
                // 테스트 실행
                sh './gradlew test'
            }
        }
    }
    post {
        success {
            echo '빌드 성공!'
        }
        failure {
            echo '빌드 실패...'
        }
    }
}
```

---

## 2. 실전 예제: Spring Boot 프로젝트 빌드

실제 Java Spring Boot 프로젝트를 빌드하고 테스트 결과를 수집하는 파이프라인 예시입니다.

1. **Pipeline Job 생성:** 'New Item' -> 'Pipeline' 선택.
2. **Pipeline 설정:** 하단 'Pipeline' 섹션에서 'Pipeline script' 선택 후 아래 내용 입력.

```groovy
pipeline {
    agent any

    tools {
        // Jenkins 관리에서 설정한 JDK나 Gradle 이름을 사용
        jdk 'openjdk-17'
        gradle 'gradle-8.0'
    }

    stages {
        stage('Prepare') {
            steps {
                echo 'Cleaning up workspace...'
                deleteDir()
                checkout scm // Git 설정이 되어 있는 경우 소스 코드 체크아웃
            }
        }

        stage('Build') {
            steps {
                echo 'Building Application...'
                sh './gradlew clean assemble'
            }
        }

        stage('Test') {
            steps {
                echo 'Running Unit Tests...'
                sh './gradlew test'
            }
            post {
                always {
                    // JUnit 결과 수집 플러그인 사용 시
                    junit '**/build/test-results/test/*.xml'
                }
            }
        }
    }
}
```

---

## 3. Jenkinsfile 활용 (Pipeline from SCM)

Pipeline 설정을 Jenkins 웹 UI에 직접 적지 않고, 프로젝트 소스 코드 루트에 `Jenkinsfile`을 포함시켜 관리하는 것이 베스트 프랙티스입니다.

1. 프로젝트 최상위 디렉토리에 `Jenkinsfile` 생성 및 위 코드 저장.
2. Jenkins Job 설정의 Pipeline 섹션에서 **'Pipeline script from SCM'** 선택.
3. **SCM:** Git 선택 및 저장소 URL 입력.
4. **Script Path:** `Jenkinsfile` 입력.

이렇게 설정하면 **코드 변경 시 빌드 절차도 함께 버전 관리**가 되며, 파이프라인 변경이 필요할 때 Jenkins UI에 접속할 필요 없이 코드만 수정하면 됩니다.

---

## 4. Monorepo 환경에서의 빌드 전략

하나의 리포지토리에 여러 프로젝트(예: `backend`, `frontend`)가 공존하는 Monorepo 환경에서는 **변경된 프로젝트만 선별적으로 빌드**하는 것이 중요합니다.

### `when { changeset }` 활용

Jenkins Pipeline의 `when` 지시어와 `changeset` 조건을 사용하면 특정 경로의 파일이 변경되었을 때만 스테이지를 실행할 수 있습니다.

```groovy
pipeline {
    agent any

    stages {
        stage('Backend Build') {
            // backend 디렉토리 하위의 파일이 변경되었을 때만 실행
            when {
                changeset 'backend/**'
            }
            steps {
                dir('backend') { // 작업 디렉토리 변경
                    sh './gradlew build'
                }
            }
        }

        stage('Frontend Build') {
            // frontend 디렉토리 하위의 파일이 변경되었을 때만 실행
            when {
                changeset 'frontend/**'
            }
            steps {
                dir('frontend') {
                    sh 'npm install && npm run build'
                }
            }
        }
    }
}
```

### 주의사항
- `changeset`은 SCM에서 가져온 변경 내역(changelog)을 기반으로 작동하므로, **Pipeline script from SCM** 방식으로 설정해야 정확하게 동작합니다.
- 첫 빌드이거나 강제로 전체 빌드가 필요한 경우를 대비해 `when { anyOf { changeset '...'; expression { params.FORCE_BUILD } } }`와 같이 파라미터를 조합해서 사용하는 것이 좋습니다.