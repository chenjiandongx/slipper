# Slipper [![PyPI version](https://badge.fury.io/py/slipper.svg)](https://badge.fury.io/py/slipper) [![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/chenjiandongx/awesome-python-cn/issues) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

> 所有的第三方库，都需要站在巨人的肩膀上完成。 -- 尤世沃·兹基硕德

### 概述

习惯了 [requests](http://github.com/requests/requests) 写法后，写异步代码的时候用 [aiohttp](https://github.com/aio-libs/aiohttp) 总感觉不太舒服。所以基于 aiohttp 写了这个项目，使异步写法更加的 pythonic。slipper 是拖孩的意思（因为拖孩穿起来舒胡？）


### 安装

**pip 安装**
```bash
$ pip install slipper
```

**源码安装**
```bash
$ git clone https://github.com/chenjiandongx/slipper.git
$ cd slipper
$ pip install -r requirements.txt
$ python setup.py install
```


### API

参照注释文档，接口与 aiohttp 保持一致，另外新增了两个参数

* expect_resp: 参数为期待的 `Response` 类型，`expect_resp=Response.text()` 相当于 aiohttp 的 `session.get().text()` 其他属性如 `url`, `version`, `headers` 等是类似的。
* client_sess: 传入的是 `Session` 类实例，实例化参数与 aiohttp 的 `ClientSession` 参数一致。


### 示例

**单任务**
```python
import asyncio

from slipper import requests, Response

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
)


async def fetch(url):
    # expect_resp 指定要获取的 Response 类型，可选属性请 `tab`或查看 Response 注释文档
    text = await requests.get(
        url, headers={"User-Agent": USER_AGENT}, expect_resp=Response.text()
    )
    print(text)


loop = asyncio.get_event_loop()
loop.run_until_complete(fetch("http://chenjiandongx.com"))

# python3.7+ 可使用 asyncIo.run()
# asyncio.run(fetch("http://chenjiandongx.com"))
```

**多任务并发**
```python
import asyncio
from pprint import pprint

from slipper import requests, Response


async def fetch(url):
    text = await requests.get(url, expect_resp=Response.url)
    pprint(text)


tasks = [fetch(url) for url in ["http://chenjiandongx.com"] * 20]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
```

**多任务并发，控制并发量**
```python
import asyncio
from pprint import pprint

from slipper import requests, Response


async def fetch(url, sem):
    async with sem:
        text = await requests.get(url, expect_resp=Response.version)
        pprint(text)


sem = asyncio.Semaphore(5)
tasks = [fetch(url, sem) for url in ["http://chenjiandongx.com"] * 20]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
```

**使用 Session**
```python
import asyncio
from pprint import pprint

from slipper import requests, Response, Session

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
)


async def fetch(url, sem, sess):
    async with sem:
        text = await requests.get(
            url, expect_resp=Response.request_info, client_sess=sess
        )
        pprint(text)


sess = Session(headers={"User-Agent": USER_AGENT})
sem = asyncio.Semaphore(5)
tasks = [fetch(url, sem, sess) for url in ["http://chenjiandongx.com"] * 5]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
```
怎么样，是不是写起来很顺手 😄


### License
MIT [©chenjiandongx](http://github.com/chenjiandongx)
