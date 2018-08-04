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
