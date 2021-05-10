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
