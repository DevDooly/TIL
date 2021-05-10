# 이미지 저장 및 관리(Database)

## 이미지 저장을 위한 최고의 데이터베이스는 데이터베이스가 아닐 수도 있습니다.
 - https://blog.couchbase.com/the-best-database-for-storing-images-might-not-be-a-database-at-all/

이미지는 사실상 매우 큰 데이터 블록이며 데이터베이스는 각 행에 큰 데이터 블록을 저장하는 데 최적화되지 않는 경향이 있다.

이미지에 대해 보장 된 고유 파일 이름을 생성하고 (해당 파일 이름에 이미지를 저장하고) 데이터베이스에 파일 이름을 저장하는 시스템을 갖는 것이 훨씬 낫다 ( 디스크 드라이브는 큰 코드 블록에 최적화돼있음 )

### 이미지가 데이터베이스에 저장되지 않아야 하는 이유

* 데이터베이스에 대한 읽기 / 쓰기는 항상 파일 시스템보다 느립니다.
* 데이터베이스 백업은 엄청나게 늘어나고 더 많은 시간이 소요됩니다. 또한 데이터베이스 서버에 과부하가 걸립니다.
* 이미지를 추출하고 스트리밍하려면 추가 코드가 필요합니다.
* 웹 서버, 파일 시스템의 이미지에 액세스하려면 특수 코딩 또는 처리가 필요합니다.

## Three Ways of Storing and Accessing Lots of Images in Python
 - https://realpython.com/storing-images-in-python/

#### FileSystem(disk)
#### LMDB
#### HDF5

위 세가지에 대한 공부와 설명은 다른 페이지에서 이어나가겠음.
###

