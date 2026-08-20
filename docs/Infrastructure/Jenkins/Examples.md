# Jenkins 실전 사용 예시 (Pipeline)

실무에서 자주 사용되는 표준적인 **Declarative Pipeline** 구성 예제들을 다룹니다.

---

## 1. 표준 CI 파이프라인 (Gradle + Docker Build & Push + Slack 알림)

가장 보편적인 백엔드 애플리케이션의 지속적 통합(CI) 파이프라인 예시입니다.

```groovy
pipeline {
    agent any

    tools {
        jdk 'openjdk-17'
        gradle 'gradle-8.5'
    }

    environment {
        DOCKER_REGISTRY = 'ghcr.io/my-org'
        IMAGE_NAME = 'backend-api'
        IMAGE_TAG = "${env.BUILD_NUMBER}-${env.GIT_COMMIT.take(7)}"
        DOCKER_CREDS = credentials('github-container-registry-token')
        SLACK_TOKEN = credentials('slack-webhook-url')
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Unit & Integration Test') {
            steps {
                echo 'Running tests...'
                sh './gradlew clean test'
            }
            post {
                always {
                    junit '**/build/test-results/test/*.xml'
                }
            }
        }

        stage('Build Application JAR') {
            steps {
                echo 'Building application artifact...'
                sh './gradlew bootJar'
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                script {
                    echo "Logging into Docker Registry: ${DOCKER_REGISTRY}"
                    sh "echo \$DOCKER_CREDS_PSW | docker login ${DOCKER_REGISTRY} -u \$DOCKER_CREDS_USR --password-stdin"
                    
                    def fullImage = "${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
                    def latestImage = "${DOCKER_REGISTRY}/${IMAGE_NAME}:latest"
                    
                    echo "Building Docker Image: ${fullImage}"
                    sh "docker build -t ${fullImage} -t ${latestImage} ."
                    
                    echo "Pushing Docker Image to Registry..."
                    sh "docker push ${fullImage}"
                    sh "docker push ${latestImage}"
                }
            }
        }
    }

    post {
        success {
            slackSend(
                color: '#00FF00',
                message: "✅ SUCCESS: Job '${env.JOB_NAME}' [Build #${env.BUILD_NUMBER}] finished successfully! (${env.BUILD_URL})"
            )
        }
        failure {
            slackSend(
                color: '#FF0000',
                message: "❌ FAILURE: Job '${env.JOB_NAME}' [Build #${env.BUILD_NUMBER}] failed! Please check console output: (${env.BUILD_URL})"
            )
        }
        always {
            cleanWs() // 작업 공간 정리
        }
    }
}
```

---

## 2. Kubernetes Pod Template 기반 동적 에이전트 빌드

Kubernetes 클러스터 내에서 Jenkins Controller가 빌드용 Pod를 동적으로 생성하여 격리된 환경에서 빌드를 수행하는 최신 패턴입니다.

```groovy
pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
metadata:
  labels:
    some-label: jenkins-agent
spec:
  containers:
  - name: gradle
    image: gradle:8.5-jdk17
    command: ['cat']
    tty: true
  - name: kaniko
    image: gcr.io/kaniko-project/executor:debug
    command: ['cat']
    tty: true
    volumeMounts:
    - name: docker-config
      mountPath: /kaniko/.docker
  volumes:
  - name: docker-config
    secret:
      secretName: docker-registry-secret
      items:
      - key: .dockerconfigjson
        path: config.json
'''
        }
    }

    environment {
        IMAGE_NAME = 'my-registry.io/app/order-service'
        IMAGE_TAG = "v${env.BUILD_NUMBER}"
    }

    stages {
        stage('Build & Test with Gradle Container') {
            steps {
                container('gradle') {
                    sh 'gradle clean test bootJar'
                }
            }
        }

        stage('Containerize with Kaniko (Daemonless Docker Build)') {
            steps {
                container('kaniko') {
                    sh "/kaniko/executor --context=dir://. --dockerfile=Dockerfile --destination=${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }
    }
}
```

---

## 3. GitOps 연계: CI 완료 후 배포 저장소 자동 커밋 (Jenkins + ArgoCD)

애플리케이션 소스 코드 저장소(App Repo)와 배포 매니페스트 저장소(GitOps Manifest Repo)가 분리되어 있을 때, Jenkins에서 Docker 이미지를 푸시한 후 **배포 저장소의 이미지 태그를 자동으로 수정하여 커밋/푸시**하는 실전 연동 스크립트입니다.

```mermaid
sequenceDiagram
    autonumber
    participant AppRepo as App Source Repo
    participant Jenkins as Jenkins (CI)
    participant Registry as Container Registry
    participant GitOpsRepo as GitOps Manifest Repo
    participant ArgoCD as ArgoCD (CD)

    Jenkins->>AppRepo: 1. 소스 코드 체크아웃 & 빌드/테스트
    Jenkins->>Registry: 2. Docker 이미지 푸시 (Tag: v1.2.3)
    Jenkins->>GitOpsRepo: 3. Manifest Repo 클론 및 values.yaml 이미지 태그 수정 (v1.2.3)
    Jenkins->>GitOpsRepo: 4. Git Commit & Push
    GitOpsRepo-->>ArgoCD: 5. Git 변경 감지 (Webhook or Polling)
    ArgoCD->>ArgoCD: 6. Kubernetes Cluster에 자동 배포(Sync)
```

### GitOps Commit Stage 추가 예시
```groovy
stage('Update GitOps Manifest') {
    environment {
        GITOPS_REPO = 'https://github.com/my-org/k8s-manifests.git'
        GIT_CREDS = credentials('github-ci-bot-pat')
    }
    steps {
        script {
            dir('gitops-repo') {
                // 1. 배포 매니페스트 저장소 클론
                sh """
                    git clone https://${GIT_CREDS_USR}:${GIT_CREDS_PSW}@github.com/my-org/k8s-manifests.git .
                """
                
                // 2. Kustomize 또는 yq를 사용하여 신규 이미지 태그로 수정
                sh """
                    # Kustomize 사용 시
                    cd overlays/prod
                    kustomize edit set image backend-app=${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
                    
                    # 또는 yq로 values.yaml 수정 시
                    # yq e '.image.tag = "${IMAGE_TAG}"' -i values-prod.yaml
                """
                
                // 3. 변경 사항 커밋 및 푸시 (ArgoCD가 이를 감지하여 배포)
                sh """
                    git config user.name "jenkins-bot"
                    git config user.email "jenkins@mycompany.com"
                    git add .
                    git commit -m "chore(release): update backend-app image tag to ${IMAGE_TAG} [skip ci]"
                    git push origin main
                """
            }
        }
    }
}
```

---

## 4. Monorepo 환경에서의 조건부 빌드 전략

`when { changeset ... }` 구문을 사용하여 변경된 서브 프로젝트만 선택적으로 빌드합니다.

```groovy
pipeline {
    agent any

    stages {
        stage('Backend API') {
            when {
                changeset 'services/api/**'
            }
            steps {
                dir('services/api') {
                    sh './gradlew test bootJar'
                }
            }
        }

        stage('Frontend Web') {
            when {
                changeset 'services/web/**'
            }
            steps {
                dir('services/web') {
                    sh 'npm ci && npm run test && npm run build'
                }
            }
        }
    }
}
```
