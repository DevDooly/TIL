웹서버 프레임워크를 어떤것으로 할지 검색하였다.

### AIOHTTP 

비동기방식의 http client/server 프레임워크이다.

asyncio 와 python 을 기본으로 사용한다.

### Flask

마이크로 웹 프레임워크로 손쉽게 웹서버를 구축 할 수 있어 간단한 RESTful api 를 구축하는데 편리하다.

두 프레임워크 중 어떤것을 선택하느냐가 가장 큰 관건이였는데

aiohttp 는 asyncio 를 사용하기 때문에 비동기, 동시 다발적인 처리에 대해서 걱정할 필요가 없는 반면

flask 는 1 User 서비스만 가능하기 때문에 비동기 처리를 위해서 celery 나 Gunicorn 등 을 같이 사용한다고 한다.

[[ 참고자료 | https://stackabuse.com/asynchronous-vs-synchronous-python-performance-analysis/ ]]
를 보면, gunicorn 을 사용하여 aiohttp 와 flask 의 성능을 비교했을땐 flask 가 우세하게 나온다고 한다.

하지만 그렇게 큰 차이는 아닌듯 하며, 소규모 서비스의 경우 관리포인트를 염두하여 aiohttp 를 사용하는게 낫지 않나 판단된다.

#### aiohttp example
<pre>
<code>
# client.py

import aiohttp
import asyncio

async def main():

    async with aiohttp.ClientSession() as session:
        async with session.get('http://python.org') as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.text()
            print("Body:", html[:15], "...")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
</code>
</pre>

<pre>
<code>
# server.py

from aiohttp import web


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{name}', handle)])

if __name__ == '__main__':
    web.run_app(app)
</code>
</pre>

#### Flask example
<pre>
<code>
#hello.py

from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
    return ''


@app.route('/hello')
def hello():
    return 'Hello, World'
</code>
</pre>
