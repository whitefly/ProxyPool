import time

from aiohttp import TCPConnector, ClientSession
from aiohttp import ClientError, ClientConnectionError
from asyncio import TimeoutError
from proxy_DB.my_client import RedisClient
import asyncio

Target_web = "http://wwww.baidu.com"
Valid_code = [200]
Bunch_size = 30


class Tester(object):
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_provy(self, proxy):
        async with  ClientSession() as session:
            try:
                real_provy = 'http://' + proxy
                async with session.get(Target_web, proxy=real_provy, timeout=10) as respose:
                    if respose.status in Valid_code:
                        self.redis.set_max(proxy)
                        print("代理可用", proxy)
                    else:
                        self.redis.decreate(proxy)
                        print("响应码{}不合法".format(respose.status), proxy)
            except(ClientError, ClientConnectionError, TimeoutError):
                self.redis.decreate(proxy)
                print("请求失败", proxy)

    def run(self):
        print("测试样例开始")
        try:
            proxies = self.redis.get_all()
            loop = asyncio.get_event_loop()
            for i in range(0, len(proxies), Bunch_size):
                test_bunch = proxies[i:i + Bunch_size]
                tasks = [self.test_single_provy(proxy) for proxy in test_bunch]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            print("测试发生错误")


T = Tester()
T.run()
