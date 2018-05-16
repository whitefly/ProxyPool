REDIS_host = 'localhost'
REDIS_port = 6379
REDIS_password = None
REDIS_set = 'proxies'

INIT_score = 10
MIN_score = 0
MAX_score = 100

import redis
from random import choice
from proxy_DB.proxy_error import PoolEmptyError


class RedisClient(object):

    def __init__(self, host=REDIS_host, port=REDIS_port, password=REDIS_password):
        """
        功能:进行redis连接,官方写法
        :param host:
        :param port:
        :param password:
        """
        self.db = redis.StrictRedis(host=host, port=port, decode_responses=True)

    def add(self, proxy, score=INIT_score):
        """
        默认新插入的代理为10分
        :param proxy:
        :param score:
        :return:
        """

        if not self.db.zscore(name=REDIS_set, value=proxy):
            self.db.zadd(REDIS_set, score, proxy)

    def random(self):
        """
        功能:随机获取一个代理
        优先选择分数100,
        然后才是0~100
        :return:
        """
        proxy_pool = self.db.zrangebyscore(REDIS_set, MAX_score, MAX_score)
        if len(proxy_pool):
            return choice(proxy_pool)
        else:
            proxy_pool = self.db.zrangebyscore(REDIS_set, 0, 100)
            if len(proxy_pool):
                return choice(proxy_pool)
            else:
                raise PoolEmptyError

    def decreate(self, proxy):
        """
        检测到不可用时,减1分
        达到0时,进行删除
        :return:
        """
        score = self.db.zscore(name=REDIS_set, value=proxy)
        if score > MIN_score:
            print("代理:{}  当前分数:{}  暂时不可用 分数-1".format(proxy, score))
            return self.db.zincrby(REDIS_set, proxy, -1)
        else:
            print("代理:{} 移除".format(proxy))
            return self.db.zrem(REDIS_set, proxy)

    def set_max(self, proxy):
        """
        将可用代理分数设置:100
        :param proxy:
        :return:
        """
        print("代理:{}  检查可用 分数设置为为:{}".format(proxy, MAX_score))
        return self.db.zadd(REDIS_set, MAX_score, proxy)

    def get_count(self):
        """
        返回 所有存在的成员个数
        :return:
        """
        return self.db.zcard(REDIS_set)

    def get_all(self):
        """
        返回全部代理, list形式
        :return:
        """
        return self.db.zrangebyscore(REDIS_set, MIN_score, MAX_score)
