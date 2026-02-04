# Jenkins 설치 가이드

Jenkins를 설치하는 방법은 다양하지만, 가장 널리 사용되고 관리가 용이한 **Docker**를 이용한 방법과 **Linux (Ubuntu)** 환경에 직접 설치하는 방법 두 가지를 다룹니다.

## 1. Docker를 이용한 설치 (권장)

Docker를 사용하면 호스트 시스템의 환경을 더럽히지 않고 깔끔하게 Jenkins를 실행하고 관리할 수 있습니다.

### 사전 준비
- Docker 및 Docker Compose가 설치되어 있어야 합니다.

### Docker 명령어로 실행하기
가장 간단하게 Jenkins 컨테이너를 실행하는 명령어입니다.

```bash
docker run -d -p 8080:8080 -p 50000:50000 --name jenkins \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts
```

- `-p 8080:8080`: 웹 UI 접속을 위한 포트 매핑
- `-p 50000:50000`: 마스터-슬레이브 통신 포트
- `-v jenkins_home:/var/jenkins_home`: 데이터 영구 저장을 위한 볼륨 마운트

### Docker Compose 사용하기
설정을 파일로 관리하기 위해 `docker-compose.yml`을 사용하는 것을 추천합니다.

```yaml
version: '3' 
services:
  jenkins:
    image: jenkins/jenkins:lts
    container_name: jenkins
    ports:
      - "8080:8080"
      - "50000:50000"
    volumes:
      - ./jenkins_home:/var/jenkins_home
    restart: always
```

실행:
```bash
docker-compose up -d
```

---

## 2. Ubuntu/Debian 리눅스에 직접 설치

### Java (JDK) 설치
Jenkins는 Java 기반이므로 JDK(11 또는 17 권장)가 필요합니다.

```bash
sudo apt update
sudo apt install fontconfig openjdk-17-jre
java -version
```

### Jenkins 리포지토리 추가 및 설치

1. **GPG 키 다운로드:**
   ```bash
   sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
     https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
   ```
2. **리포지토리 추가:**
   ```bash
   echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc]" \
     https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
     /etc/apt/sources.list.d/jenkins.list > /dev/null
   ```
3. **설치:**
   ```bash
   sudo apt-get update
   sudo apt-get install jenkins
   ```

### 서비스 시작 및 상태 확인
```bash
sudo systemctl enable jenkins
sudo systemctl start jenkins
sudo systemctl status jenkins
```

---

## 3. 초기 설정 (Unlock Jenkins)

설치 후 브라우저에서 `http://localhost:8080` (서버 IP:8080)으로 접속하면 **Unlock Jenkins** 화면이 나옵니다.

### 초기 비밀번호 확인

**Docker 사용자:**
```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

**Linux 직접 설치 사용자:**
```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

위 명령어로 확인한 비밀번호를 입력하면 플러그인 설치 화면으로 넘어갑니다. 보통 **"Install suggested plugins"**를 선택하여 기본 플러그인들을 설치하는 것이 좋습니다.

```