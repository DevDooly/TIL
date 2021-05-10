### Mac 에서 mongodb 설치 후 테스트를 진행한다.

#### 패키지 다운로드
 - https://www.mongodb.com/try/download/community
#### 설치
 - 해당 파일 이동
   - sudo mv mongodb-macos-???? /usr/local/mongodb
 - 경로 등록(zsh 기준)
   - echo "export MONGO_PATH=/usr/local/mongodb" >> ~/.zshrc
   - echo "PATH=$PATH:$MONGO_PATH/bin" >> ~/.zshrc
#### db 생성
 - 프로젝트 경로 하위에 데이터를 보관 할 폴더를 생성한다.
   - mkdir -p "" 프로젝트 경로 "" / data/db
#### mongo 실행 (서버)
 - 서버가 정상적으로 실행되는지 확인한다 (위에서 생성한 경로를 입력해야 함, 기본경로는 /data/db)
   - mongod --dbpath "" 프로젝트 경로 "" / data/db
#### mongo 실행 (클라이언트)
 - mongo
