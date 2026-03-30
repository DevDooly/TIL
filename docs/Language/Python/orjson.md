# orjson

Python 용 JSON 라이브러리.

Python 에서 기본적으로 제공하는 JSON 라이브러리는 성능이 아주 안좋다.

orjson 은 ujson, rapidjson, simplejson, json 라이브러리와 비교했을때 가장 훌륭한 성능을 보여주고 있다.

python 에서 기본적으로 제공하는 라이브러리가 있다해도 오픈소스와 비교해보고 더 뛰어난것을 사용하자.

## 설치 방법
```
pip install --upgrade "pip>=19.3" # manylinux2014 support
pip install --upgrade orjson
```
## 사용 방법
```
>>> import orjson, datetime, numpy
>>> data = {
    "type": "job",
    "created_at": datetime.datetime(1970, 1, 1),
    "status": "🆗",
    "payload": numpy.array([[1, 2], [3, 4]]),
}
>>> orjson.dumps(data, option=orjson.OPT_NAIVE_UTC | orjson.OPT_SERIALIZE_NUMPY)
b'{"type":"job","created_at":"1970-01-01T00:00:00+00:00","status":"\xf0\x9f\x86\x97","payload":[[1,2],[3,4]]}'
>>> orjson.loads(_)
{'type': 'job', 'created_at': '1970-01-01T00:00:00+00:00', 'status': '🆗', 'payload': [[1, 2], [3, 4]]}
```

## 출처

* https://github.com/ijl/orjson
