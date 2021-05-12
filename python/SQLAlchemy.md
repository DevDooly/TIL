# SQLAlchemy

## python에서 사용가능한 ORM(Object-relational maping)

## 설치방법
```
pip install sqlalchemy
```

## 사용법 (1.x / mariadb )
### Version Check
```
>>> import sqlalchemy
>>> sqlalchemy.__version__
1.4.0
```
### Connecting
```
>>> from sqlalchemy import create_engine
>>> engine = create_engin('mysql+mysqldb://{ID}:{PASSWORD}@{IP}:{PORT}/{DB}')
```
### Declare a Mapping
```
>>> from sqlalchemy.orm import declarative_base
>>> Base = declarative_base()

>>> from sqlalchemy import Column, Integer, String
>>> class User(Base):
:::     __tablename__ = 'users'
:::     
:::     id = Column(Integer, primary_key=True)
:::     name = Column(String)
:::     fullname = Column(String)
:::     nickname = Column(String)
:::     
:::     def __repr__(self):
:::       return "<User(name='%s', fullname='%s', nickname='%s')>" % (
:::               self.name, self.fullname, self.nickname)
```

### Create a Schema
```
>>> User.__table__ 
Table('users', MetaData(),
            Column('id', Integer(), table=<users>, primary_key=True, nullable=False),
            Column('name', String(), table=<users>),
            Column('fullname', String(), table=<users>),
            Column('nickname', String(), table=<users>), schema=None)
```

```
# Create Table Example

from sqlalchemy import MetaData, Integer, String, Table, Column, text
from sqlalchemy.dialects.mysql import TIMESTAMP

def create_table(db_url):
    from sqlalchemy import create_engine
    engine = create_engine(db_url)
    metaData = MetaData()
    Table('cctv_images', metaData,
          Column('id', Integer, primary_key=True, autoincrement=True),
          Column('separator1', String(50),
          Column('separator2', String(50),
          Column('tag', String(50),
          Column('extention', String(50),
          Column(
                 'created_date',
                 TIMESTAMP,
                 server_default=text(
                     "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
                 ),
          Column(
                 'updated_date',
                 TIMESTAMP,
                 server_default=text(
                     "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
                 )
          )

    metaData.create_all(engine)
```
